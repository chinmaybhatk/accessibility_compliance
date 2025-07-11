import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    """Add custom fields for accessibility compliance"""
    
    custom_fields = {
        "Website": [
            {
                "fieldname": "accessibility_enabled",
                "label": "Enable Accessibility Compliance",
                "fieldtype": "Check",
                "default": 1,
                "insert_after": "disable_signup"
            },
            {
                "fieldname": "wcag_level",
                "label": "WCAG Compliance Level",
                "fieldtype": "Select",
                "options": "A\nAA\nAAA",
                "default": "AA",
                "depends_on": "accessibility_enabled",
                "insert_after": "accessibility_enabled"
            }
        ]
    }
    
    create_custom_fields(custom_fields, update=True)