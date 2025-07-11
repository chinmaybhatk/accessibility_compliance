app_name = "accessibility_compliance"
app_title = "Accessibility Compliance"
app_publisher = "Your Company"
app_description = "AI-Powered Accessibility Compliance Scanner for websites"
app_icon = "octicon octicon-shield"
app_color = "blue"
app_email = "developer@yourcompany.com"
app_license = "MIT"
app_version = "1.0.0"

# Frappe Framework version
required_apps = ["frappe"]

# DocTypes
fixtures = [
    "Custom Field",
    "Property Setter", 
    "Custom Script",
    "Role",
    "Workflow",
    "Print Format"
]

# Background Jobs
scheduler_events = {
    "cron": {
        "0 2 * * *": [  # Daily at 2 AM
            "accessibility_compliance.accessibility_compliance.scheduler.run_scheduled_scans"
        ],
        "0 */6 * * *": [  # Every 6 hours
            "accessibility_compliance.accessibility_compliance.scheduler.cleanup_old_scan_data"
        ]
    }
}

# Permissions
doc_events = {
    "Website Scan": {
        "before_insert": "accessibility_compliance.accessibility_compliance.utils.before_scan_insert",
        "on_update": "accessibility_compliance.accessibility_compliance.utils.on_scan_update"
    }
}

# Web pages
website_route_rules = [
    {"from_route": "/accessibility-scanner", "to_route": "accessibility_scanner"},
    {"from_route": "/accessibility-dashboard", "to_route": "accessibility_dashboard"}
]

# Boot session
boot_session = "accessibility_compliance.boot.boot_session"

# Installation
after_install = "accessibility_compliance.install.after_install"
before_uninstall = "accessibility_compliance.uninstall.before_uninstall"