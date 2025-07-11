import frappe
from frappe import _

def after_install():
    """Run after installing the app"""
    create_default_settings()
    create_sample_data()
    
def create_default_settings():
    """Create default accessibility settings"""
    if not frappe.db.exists("Accessibility Settings", "Accessibility Settings"):
        settings = frappe.new_doc("Accessibility Settings")
        settings.name = "Accessibility Settings"
        settings.enabled = 1
        settings.default_wcag_level = "AA"
        settings.auto_scan = 1
        settings.scan_frequency = "Weekly"
        settings.email_notifications = 1
        settings.save(ignore_permissions=True)
        
    frappe.db.commit()
    
def create_sample_data():
    """Create sample accessibility scan data"""
    # Create sample WCAG guidelines
    guidelines = [
        {
            "title": "1.1.1 Non-text Content",
            "description": "All non-text content has a text alternative",
            "level": "A",
            "category": "Perceivable"
        },
        {
            "title": "1.4.3 Contrast (Minimum)",
            "description": "Text has a contrast ratio of at least 4.5:1",
            "level": "AA", 
            "category": "Perceivable"
        },
        {
            "title": "2.1.1 Keyboard",
            "description": "All functionality is available from keyboard",
            "level": "A",
            "category": "Operable"
        }
    ]
    
    for guideline in guidelines:
        if not frappe.db.exists("WCAG Guideline", guideline["title"]):
            doc = frappe.new_doc("WCAG Guideline")
            doc.update(guideline)
            doc.save(ignore_permissions=True)
            
    frappe.db.commit()