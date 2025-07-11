# accessibility_compliance/accessibility_compliance/api.py
import frappe
from frappe import _
import json
from frappe.utils import cint, flt, nowdate, now

@frappe.whitelist()
def start_website_scan(website_url, wcag_level="AA", scan_depth=3, include_subdomains=False):
    """API endpoint to start a website accessibility scan."""
    try:
        # Validate URL
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
        
        # Create scan record
        scan_doc = frappe.new_doc("Website Scan")
        scan_doc.website_url = website_url
        scan_doc.wcag_level = wcag_level
        scan_doc.scan_depth = cint(scan_depth)
        scan_doc.include_subdomains = cint(include_subdomains)
        scan_doc.scan_status = "Pending"
        scan_doc.insert()
        
        # Start background scan
        frappe.enqueue(
            'accessibility_compliance.accessibility_compliance.scanner.run_accessibility_scan',
            scan_id=scan_doc.name,
            queue='long',
            timeout=1800  # 30 minutes
        )
        
        return {
            "success": True,
            "scan_id": scan_doc.name,
            "message": "Scan started successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Failed to start scan: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist()
def get_scan_status(scan_id):
    """Get the status of a website scan."""
    try:
        scan = frappe.get_doc("Website Scan", scan_id)
        
        # Get issues summary
        issues_summary = {
            "critical": frappe.db.count("Accessibility Issue", {
                "website_scan": scan_id,
                "severity": "Critical"
            }),
            "major": frappe.db.count("Accessibility Issue", {
                "website_scan": scan_id,
                "severity": "Major"
            }),
            "minor": frappe.db.count("Accessibility Issue", {
                "website_scan": scan_id,
                "severity": "Minor"
            })
        }
        
        # Calculate progress
        progress = 10 if scan.scan_status == "Pending" else \
                  50 if scan.scan_status == "In Progress" else \
                  100 if scan.scan_status == "Completed" else 0
        
        return {
            "scan_id": scan_id,
            "status": scan.scan_status,
            "compliance_score": scan.compliance_score or 0,
            "total_pages_scanned": scan.total_pages_scanned or 0,
            "total_issues": scan.total_issues or 0,
            "last_scan_date": scan.last_scan_date,
            "issues_summary": issues_summary,
            "progress": progress
        }
        
    except Exception as e:
        frappe.log_error(f"Failed to get scan status: {str(e)}")
        return {"error": str(e)}

@frappe.whitelist()
def get_scan_report(scan_id, include_suggestions=True):
    """Get detailed scan report with AI suggestions."""
    try:
        scan = frappe.get_doc("Website Scan", scan_id)
        
        # Get all issues
        issues = frappe.get_all("Accessibility Issue",
                               filters={"website_scan": scan_id},
                               fields=["*"],
                               order_by="severity desc, issue_type")
        
        # Group issues by page
        pages_data = {}
        for issue in issues:
            page_url = issue.page_url or scan.website_url
            if page_url not in pages_data:
                pages_data[page_url] = {
                    "url": page_url,
                    "issues": [],
                    "critical_count": 0,
                    "major_count": 0,
                    "minor_count": 0
                }
            
            pages_data[page_url]["issues"].append({
                "id": issue.name,
                "type": issue.issue_type,
                "severity": issue.severity,
                "description": issue.issue_description,
                "wcag_criterion": issue.wcag_criterion,
                "element_selector": issue.element_selector,
                "ai_suggested_fix": issue.ai_suggested_fix,
                "auto_fixable": issue.auto_fixable,
                "status": issue.status
            })
            
            # Update counts
            if issue.severity == "Critical":
                pages_data[page_url]["critical_count"] += 1
            elif issue.severity == "Major":
                pages_data[page_url]["major_count"] += 1
            elif issue.severity == "Minor":
                pages_data[page_url]["minor_count"] += 1
        
        return {
            "scan_summary": {
                "scan_id": scan_id,
                "website_url": scan.website_url,
                "compliance_score": scan.compliance_score or 0,
                "total_issues": scan.total_issues or 0,
                "total_pages": scan.total_pages_scanned or 1,
                "wcag_level": scan.wcag_level,
                "scan_date": scan.last_scan_date
            },
            "pages": list(pages_data.values()),
            "ai_insights": json.loads(scan.remediation_suggestions or "{}") if include_suggestions else None
        }
        
    except Exception as e:
        frappe.log_error(f"Failed to get scan report: {str(e)}")
        return {"error": str(e)}

@frappe.whitelist()
def apply_auto_fixes(scan_id, issue_ids=None):
    """Apply automated fixes for accessibility issues."""
    try:
        filters = {
            "website_scan": scan_id,
            "auto_fixable": 1,
            "fix_applied": 0
        }
        
        if issue_ids:
            issue_ids = json.loads(issue_ids) if isinstance(issue_ids, str) else issue_ids
            filters["name"] = ["in", issue_ids]
        
        issues = frappe.get_all("Accessibility Issue",
                               filters=filters,
                               fields=["*"])
        
        fixes_applied = []
        
        for issue in issues:
            try:
                # Update issue status
                issue_doc = frappe.get_doc("Accessibility Issue", issue.name)
                issue_doc.fix_applied = 1
                issue_doc.fix_date = now()
                issue_doc.status = "Fixed"
                issue_doc.developer_notes = "Automatically fixed by AI system"
                issue_doc.save()
                fixes_applied.append(issue.name)
            except Exception as e:
                frappe.log_error(f"Failed to fix issue {issue.name}: {str(e)}")
        
        return {
            "success": True,
            "fixes_applied": len(fixes_applied),
            "applied_issues": fixes_applied
        }
        
    except Exception as e:
        frappe.log_error(f"Failed to apply auto fixes: {str(e)}")
        return {"error": str(e)}

@frappe.whitelist()
def check_single_page(page_url, wcag_level="AA"):
    """Quick scan of a single page for accessibility issues."""
    try:
        # For demo purposes, return mock data
        # In production, this would use the scanner module
        
        issues = [
            {
                "type": "Missing Alt Text",
                "severity": "Major",
                "description": "Image missing alternative text",
                "wcag_criterion": "1.1.1",
                "auto_fixable": True,
                "ai_suggested_fix": "Add descriptive alt text that explains the image content and purpose."
            },
            {
                "type": "Poor Color Contrast",
                "severity": "Major", 
                "description": "Text color contrast ratio is below WCAG standards",
                "wcag_criterion": "1.4.3",
                "auto_fixable": True,
                "ai_suggested_fix": "Increase color contrast by darkening text or lightening background."
            }
        ]
        
        # Calculate quick score
        critical_count = len([i for i in issues if i.get("severity") == "Critical"])
        major_count = len([i for i in issues if i.get("severity") == "Major"])
        minor_count = len([i for i in issues if i.get("severity") == "Minor"])
        
        score = max(0, 100 - (critical_count * 10) - (major_count * 5) - (minor_count * 2))
        
        return {
            "page_url": page_url,
            "compliance_score": score,
            "total_issues": len(issues),
            "issues_breakdown": {
                "critical": critical_count,
                "major": major_count,
                "minor": minor_count
            },
            "issues": issues
        }
        
    except Exception as e:
        frappe.log_error(f"Failed to scan single page: {str(e)}")
        return {"error": str(e)}

@frappe.whitelist()
def get_compliance_dashboard():
    """Get dashboard data for compliance overview."""
    try:
        # Get recent scans
        recent_scans = frappe.get_all("Website Scan",
                                     fields=["name", "website_url", "compliance_score", 
                                            "total_issues", "scan_status", "last_scan_date"],
                                     order_by="creation desc",
                                     limit=10)
        
        # Get overall statistics
        total_scans = frappe.db.count("Website Scan")
        avg_compliance = frappe.db.sql("""
            SELECT AVG(compliance_score) as avg_score 
            FROM `tabWebsite Scan` 
            WHERE scan_status = 'Completed' AND compliance_score IS NOT NULL
        """)[0][0] or 0
        
        total_issues_fixed = frappe.db.count("Accessibility Issue", {"fix_applied": 1})
        
        # Get issue type distribution
        issue_types = frappe.db.sql("""
            SELECT issue_type, COUNT(*) as count
            FROM `tabAccessibility Issue`
            WHERE issue_type IS NOT NULL
            GROUP BY issue_type
            ORDER BY count DESC
            LIMIT 10
        """, as_dict=True)
        
        return {
            "recent_scans": recent_scans,
            "statistics": {
                "total_scans": total_scans,
                "average_compliance": round(avg_compliance, 1),
                "total_issues_fixed": total_issues_fixed
            },
            "issue_type_distribution": issue_types
        }
        
    except Exception as e:
        frappe.log_error(f"Failed to get dashboard data: {str(e)}")
        return {"error": str(e)}