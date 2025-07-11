import frappe

def execute():
    """Setup default accessibility compliance settings"""
    
    if not frappe.db.exists("Accessibility Settings", "Accessibility Settings"):
        settings = frappe.new_doc("Accessibility Settings")
        settings.name = "Accessibility Settings"
        settings.enabled = 1
        settings.default_wcag_level = "AA"
        settings.auto_scan = 1
        settings.scan_frequency = "Weekly"
        settings.save(ignore_permissions=True)
        
    frappe.db.commit()