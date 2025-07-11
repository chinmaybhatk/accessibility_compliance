import frappe

def get_context(context):
    """Get context for accessibility dashboard"""
    context.no_cache = 1
    context.show_sidebar = True
    
    # Get dashboard data
    context.total_scans = frappe.db.count("Accessibility Scan")
    context.total_issues = frappe.db.sql("""
        SELECT SUM(total_issues) 
        FROM `tabAccessibility Scan` 
        WHERE docstatus = 1
    """)[0][0] or 0
    
    # Get recent scans
    context.recent_scans = frappe.get_list(
        "Accessibility Scan",
        fields=["name", "url", "scan_date", "total_issues", "compliance_score"],
        order_by="scan_date desc",
        limit=10
    )
    
    # Calculate average compliance score
    avg_score = frappe.db.sql("""
        SELECT AVG(compliance_score) 
        FROM `tabAccessibility Scan` 
        WHERE docstatus = 1 AND compliance_score > 0
    """)[0][0] or 0
    
    context.avg_compliance_score = round(avg_score, 1)
    
    return context