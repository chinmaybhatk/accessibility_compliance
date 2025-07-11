__version__ = '1.0.0'

# Frappe app configuration
app_name = "accessibility_compliance"
app_title = "Accessibility Compliance"
app_publisher = "Chinmay Bhat"
app_description = "Comprehensive web accessibility compliance tool for WCAG and ADA testing"
app_icon = "fa fa-universal-access"
app_color = "blue"
app_email = "chinmaybhatk@example.com"
app_license = "MIT"

# Required apps
required_apps = ["frappe"]

# Include js, css files in header of desk.html
app_include_css = "/assets/accessibility_compliance/css/accessibility.css"
app_include_js = "/assets/accessibility_compliance/js/accessibility.js"

# Include js, css files in header of web template
web_include_css = "/assets/accessibility_compliance/css/web.css"
web_include_js = "/assets/accessibility_compliance/js/web.js"

# Home Pages
website_route_rules = [
    {"from_route": "/accessibility-dashboard", "to_route": "accessibility_dashboard"},
    {"from_route": "/accessibility", "to_route": "accessibility_dashboard"}
]