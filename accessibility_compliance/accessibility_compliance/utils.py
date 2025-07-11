# accessibility_compliance/accessibility_compliance/utils.py
import frappe
from frappe import _

def before_scan_insert(doc, method):
    """Validate scan before insertion."""
    # Ensure URL format
    if not doc.website_url.startswith(('http://', 'https://')):
        doc.website_url = 'https://' + doc.website_url
    
    # Set default values
    if not doc.wcag_level:
        doc.wcag_level = "AA"
    
    if not doc.scan_depth:
        doc.scan_depth = 3

def on_scan_update(doc, method):
    """Handle scan status updates."""
    if doc.scan_status == "Completed" and not doc.last_scan_date:
        doc.last_scan_date = frappe.utils.now()

def get_compliance_score_color(score):
    """Get color for compliance score display."""
    if score >= 90:
        return "success"
    elif score >= 70:
        return "warning" 
    else:
        return "danger"

def format_scan_date(date):
    """Format scan date for display."""
    if not date:
        return "Never"
    return frappe.format(date, {"fieldtype": "Datetime"})

def get_issue_icon(issue_type):
    """Get icon for issue type."""
    icons = {
        "Missing Alt Text": "fa fa-image",
        "Poor Color Contrast": "fa fa-eye",
        "Form Labels": "fa fa-tags",
        "Missing Headings": "fa fa-header",
        "Skip Links": "fa fa-link",
        "Focus Indicators": "fa fa-crosshairs",
        "ARIA Landmarks": "fa fa-map-marker"
    }
    return icons.get(issue_type, "fa fa-exclamation-triangle")