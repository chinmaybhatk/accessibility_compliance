# accessibility_compliance/accessibility_compliance/install.py
import frappe
from frappe import _

def after_install():
    """Setup after app installation."""
    create_custom_roles()
    create_sample_data()
    setup_website_settings()

def create_custom_roles():
    """Create custom roles for accessibility management."""
    roles = [
        {
            "role_name": "Accessibility Manager",
            "description": "Can manage all accessibility scans and issues"
        },
        {
            "role_name": "Accessibility Viewer", 
            "description": "Can view accessibility reports and scans"
        }
    ]
    
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.role_name = role_data["role_name"]
            role.description = role_data["description"]
            role.insert()

def create_sample_data():
    """Create sample accessibility scan for demo."""
    # Only create if no scans exist
    if frappe.db.count("Website Scan") == 0:
        sample_scan = frappe.new_doc("Website Scan")
        sample_scan.website_url = "https://example.com"
        sample_scan.wcag_level = "AA"
        sample_scan.scan_status = "Completed"
        sample_scan.compliance_score = 75
        sample_scan.total_issues = 8
        sample_scan.critical_issues = 1
        sample_scan.major_issues = 4
        sample_scan.minor_issues = 3
        sample_scan.total_pages_scanned = 1
        sample_scan.last_scan_date = frappe.utils.now()
        sample_scan.insert()
        
        # Create sample issues
        sample_issues = [
            {
                "issue_type": "Missing Alt Text",
                "severity": "Major",
                "wcag_criterion": "1.1.1",
                "description": "Image missing alternative text",
                "auto_fixable": True
            },
            {
                "issue_type": "Poor Color Contrast", 
                "severity": "Critical",
                "wcag_criterion": "1.4.3",
                "description": "Text color contrast ratio below WCAG standards",
                "auto_fixable": True
            }
        ]
        
        for issue_data in sample_issues:
            issue = frappe.new_doc("Accessibility Issue")
            issue.website_scan = sample_scan.name
            issue.page_url = "https://example.com"
            issue.update(issue_data)
            issue.insert()

def setup_website_settings():
    """Setup website routing and settings."""
    try:
        # Add website route rules if not exists
        from frappe.website.utils import build_website_context
        frappe.clear_cache("website_context")
    except Exception as e:
        frappe.log_error(f"Website setup error: {str(e)}")