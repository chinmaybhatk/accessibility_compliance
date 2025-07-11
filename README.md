# AI-Powered Accessibility Compliance Scanner

[![Frappe](https://img.shields.io/badge/Frappe-v15-blue)](https://github.com/frappe/frappe)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green)](https://github.com/frappe/mcp)

## 🎯 Overview

A comprehensive Frappe Framework app that provides AI-powered accessibility compliance scanning for websites. Built for Frappe v15 with full MCP (Model Context Protocol) integration.

### 🚀 Key Features

- ✅ **Automated WCAG Scanning** - Comprehensive A/AA/AAA compliance checking
- 🤖 **AI-Powered Analysis** - OpenAI integration for intelligent fix suggestions
- 🔧 **One-Click Fixes** - Automated remediation for 60%+ of common issues
- 📊 **Real-time Dashboard** - Beautiful web interface with live progress
- 🔗 **MCP Integration** - Full Model Context Protocol server support
- 📋 **Detailed Reports** - Executive-ready compliance reports
- 🎯 **Priority Recommendations** - AI-driven issue prioritization
- 🔄 **Continuous Monitoring** - Scheduled scans and alerts

### 💡 Business Impact

- **Target Market**: 200M+ websites needing compliance
- **Problem**: 98% of websites fail ADA/WCAG standards
- **Market Size**: $2.1B compliance software market
- **Advantage**: AI-first approach vs manual tools

## 🚀 Quick Start

### Installation on Frappe Cloud

1. **Create Private Bench Group** in Frappe Cloud
2. **Add App from GitHub**:
   ```
   Repository: https://github.com/chinmaybhatk/accessibility_compliance
   Branch: main
   ```
3. **Deploy and Install** on your site
4. **Configure API Keys** in Site Config:
   ```json
   {
     "openai_api_key": "your-openai-api-key"
   }
   ```

### Local Installation

```bash
# Get the app
bench get-app https://github.com/chinmaybhatk/accessibility_compliance

# Install on site
bench --site your-site install-app accessibility_compliance

# Start the bench
bench start
```

## 🔧 Configuration

### Required Settings

Add to your site's `site_config.json`:

```json
{
  "openai_api_key": "sk-your-openai-api-key",
  "max_pages_per_scan": 50,
  "default_wcag_level": "AA",
  "scan_timeout_minutes": 30
}
```

### Chrome WebDriver Setup

For local installations, Chrome WebDriver is automatically managed via `webdriver-manager`.

## 🌐 Usage

### Web Interface

Access the scanner at: `http://your-site/accessibility-scanner`

Features:
- Enter website URL and scan configuration
- Real-time progress tracking
- Interactive results dashboard
- AI-powered insights and recommendations
- One-click automated fixes

### MCP Integration

**MCP Endpoint**: `http://your-site/api/method/accessibility_compliance.mcp.handle_mcp`

**Available Tools**:
- `scan_website_accessibility(website_url, wcag_level, max_pages)`
- `generate_remediation_report(scan_id)`
- `apply_automated_fixes(scan_id, fix_types)`
- `check_color_contrast(foreground_color, background_color, text_size)`

**Test with MCP Inspector**:
1. Set Transport: "Streamable HTTP"
2. URL: Your MCP endpoint
3. Go through OAuth flow or set `allow_guests=True`

### API Endpoints

```bash
# Start scan
POST /api/method/accessibility_compliance.api.start_website_scan
{
  "website_url": "https://example.com",
  "wcag_level": "AA"
}

# Get status
GET /api/method/accessibility_compliance.api.get_scan_status?scan_id=SCAN_ID

# Get report
GET /api/method/accessibility_compliance.api.get_scan_report?scan_id=SCAN_ID

# Apply fixes
POST /api/method/accessibility_compliance.api.apply_auto_fixes
{
  "scan_id": "SCAN_ID"
}
```

## 🏗️ Architecture

### DocTypes

1. **Website Scan** - Main scan configuration and results
2. **Accessibility Issue** - Individual violations with AI suggestions

### Core Modules

- `mcp.py` - Model Context Protocol server
- `api.py` - REST API endpoints  
- `scanner.py` - Selenium-based scanning engine
- `ai_analyzer.py` - OpenAI integration for analysis

### Supported Checks

#### Critical Issues ⚠️
- Missing alt text for images
- Form inputs without labels
- Missing page title/language
- Keyboard navigation barriers

#### Major Issues 🔶
- Poor color contrast
- Broken heading structure
- Missing ARIA landmarks
- Invalid form associations

#### Minor Issues 💡
- Verbose alt text
- Missing table captions
- Focus indicator issues
- WCAG AAA violations

## 🤖 AI Features

### Intelligent Analysis
- **Pattern Recognition** - Identifies common issue patterns
- **Priority Scoring** - Smart issue prioritization
- **Timeline Estimation** - Realistic fix timelines
- **Impact Assessment** - Business impact analysis

### Automated Fixes
- **Alt Text Generation** - AI-generated image descriptions
- **Color Contrast** - Automatic color adjustments
- **Form Labels** - Smart label suggestions
- **ARIA Landmarks** - Semantic structure improvements

## 📊 Reporting

### Executive Dashboard
- Compliance score trending
- Issue breakdown by severity
- Fix progress tracking
- ROI metrics

### Technical Reports
- Detailed WCAG violations
- Code-level fix instructions
- Implementation timelines
- Testing recommendations

## 🚀 Deployment

### Frappe Cloud (Recommended)

1. **Repository Setup**:
   - Fork this repository
   - Create private bench group
   - Add app from your fork

2. **Environment Variables**:
   ```bash
   OPENAI_API_KEY=your_api_key
   ACCESSIBILITY_MAX_PAGES=50
   ```

3. **Deploy and Test**:
   - Deploy bench group
   - Install on site
   - Access `/accessibility-scanner`

### Self-Hosted

Requirements:
- Frappe Framework v15+
- Python 3.8+
- Chrome/Chromium browser
- Redis for background jobs

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/chinmaybhatk/accessibility_compliance.git

# Install in development mode
bench get-app accessibility_compliance --branch main

# Install dependencies
cd apps/accessibility_compliance
pip install -r requirements.txt

# Install on site
bench --site your-site install-app accessibility_compliance
```

### Running Tests

```bash
# Run app tests
bench --site your-site run-tests --app accessibility_compliance

# Test MCP integration
frappe-mcp check --app accessibility_compliance --verbose
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📈 Roadmap

### v1.1 (Next Release)
- [ ] Lighthouse integration
- [ ] PDF report generation
- [ ] Email notifications
- [ ] Advanced scheduling

### v1.2 (Future)
- [ ] Multi-language support
- [ ] Custom rule engine
- [ ] Integration marketplace
- [ ] White-label solutions

## 🐛 Troubleshooting

### Common Issues

**Chrome Driver Problems**:
```bash
pip install --upgrade webdriver-manager
```

**Permission Errors**:
```bash
bench --site your-site set-config openai_api_key "your-key"
```

**Memory Issues**:
```bash
# Increase worker memory
echo 'worker_memory_limit = 2048' >> sites/common_site_config.json
```

### Debug Mode

Enable detailed logging:
```json
{
  "logging": {
    "accessibility_compliance": "DEBUG"
  }
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Frappe Framework](https://frappeframework.com/) - Amazing web framework
- [Frappe MCP](https://github.com/frappe/mcp) - Model Context Protocol integration
- [WebAIM](https://webaim.org/) - Accessibility guidelines and tools
- [WCAG](https://www.w3.org/WAI/WCAG21/quickref/) - Web Content Accessibility Guidelines

## 📞 Support

- 📧 **Email**: developer@yourcompany.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/chinmaybhatk/accessibility_compliance/issues)
- 💬 **Community**: [Frappe Forum](https://discuss.frappe.io)
- 📖 **Documentation**: [Wiki](https://github.com/chinmaybhatk/accessibility_compliance/wiki)

---

**Ready to make the web accessible for everyone? Start your first scan today!** 🌟