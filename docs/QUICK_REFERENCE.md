# Vendor Risk Assessment Tool - Quick Reference Card

## 🚀 Quick Start
1. **Access Tool**: `http://localhost:8028/static/combined-ui.html`
2. **Enter Domain**: Vendor's primary website (e.g., `salesforce.com`)
3. **Enter Email**: Your email for receiving reports
4. **Choose Mode**: Business Risk or Technical Due Diligence
5. **Start Assessment**: Click "Start Assessment" (takes 2-5 minutes)
6. **AI Analysis**: Advanced AI automatically analyzes all findings and generates intelligent insights

## 📊 Assessment Modes

| Mode | When to Use | Time | AI Analysis |
|------|-------------|------|-------------|
| **Business Risk** | Standard vendor evaluation | 2-3 min | AI-powered security, compliance, and risk analysis |
| **Technical Due Diligence** | Technical integrations, acquisitions | 3-5 min | Advanced AI assessment + technical deep-dive |

## 🤖 AI-Powered Features
- **Intelligent Risk Scoring**: AI analyzes multiple factors for accurate risk assessment
- **Content Analysis**: AI reviews vendor websites, policies, and documentation
- **Executive Insights**: AI generates summaries and recommendations for decision-makers
- **Smart Recommendations**: AI provides specific next steps and mitigation strategies

## 🎯 Risk Score Guide

| Score | Level | Action Required |
|-------|-------|-----------------|
| **80-100** | 🟢 Very Low | Standard monitoring |
| **60-79** | 🟡 Low | Regular monitoring |
| **40-59** | 🟠 Medium | Enhanced monitoring |
| **20-39** | 🔴 High | Risk mitigation required |
| **0-19** | ⚫ Critical | Immediate action required |

## 🔍 What Gets Assessed

### AI-Enhanced Analysis ✅
- **Security Intelligence**: AI-powered analysis of SSL/TLS, security headers, DNS configuration
- **Compliance**: SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS
- **Breaches**: Historical incidents, impact, remediation
- **AI Features**: AI/ML services, data processing, governance
- **Infrastructure**: Cloud setup, encryption, monitoring

### Technical Mode Adds 🔧
- **Network Security**: Port analysis, firewall config
- **App Security**: Authentication, input validation
- **API Security**: Rate limiting, third-party integrations
- **Code Quality**: Security controls, best practices

## 📋 Common Use Cases

### New Vendor Onboarding
```
1. Run Business Risk Assessment
2. If score < 60 → Security team review
3. If score ≥ 60 → Proceed with procurement
4. Document results in vendor file
```

### Technical Integration
```
1. Run Technical Due Diligence
2. Review network & API security sections
3. Validate with vendor documentation
4. Create integration security plan
```

### Quarterly Reviews
```
1. Run assessments for all critical vendors
2. Compare with previous scores
3. Flag significant changes
4. Update risk register
```

## 🚨 When to Escalate

| Situation | Notify | Timeline |
|-----------|--------|----------|
| Score < 30 | Security Team | Immediately |
| New breach discovered | CISO | Within 1 hour |
| Compliance gap | Legal/Compliance | Within 4 hours |
| Technical integration risk | IT Security | Within 1 day |

## 💡 Pro Tips

### Best Practices ✅
- Use vendor's primary domain (not subdomains)
- Save assessment reports for documentation
- Re-run assessments after major vendor changes
- Compare scores when evaluating multiple vendors

### Common Mistakes ❌
- Using incorrect domain format
- Not following up on medium/high risk scores
- Ignoring assessment recommendations
- Skipping technical due diligence for API integrations

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Assessment stuck | Refresh page, restart assessment |
| No AI detected | Verify primary company domain |
| Low score unexpected | Cross-check with vendor documentation |
| Can't access tool | Check URL, contact IT support |

## 📊 Bulk Assessments

### When to Use
- Multiple vendor evaluation
- Annual vendor reviews
- Portfolio risk analysis
- Compliance reporting

### Format
```
salesforce.com
microsoft.com
google.com
slack.com
```

### Best Practices
- Maximum 20 vendors per batch
- Use consistent domain format
- Monitor progress in bulk status
- Export results for analysis

## 📱 Mobile Usage
- Tool works on mobile browsers
- Best experience on desktop/laptop
- Results may take longer on mobile
- Consider desktop for bulk assessments

## 📞 Support Contacts

| Issue Type | Contact |
|------------|---------|
| Tool not working | IT Support |
| Risk interpretation | Security Team |
| Process questions | Vendor Management |
| Compliance questions | Legal Team |

## 🔗 Related Links
- **Tool Access**: `http://localhost:8028/static/combined-ui.html`
- **API Docs**: `http://localhost:8028/docs`
- **Health Check**: `http://localhost:8028/health`
- **User Guide**: See `docs/USER_GUIDE.md`

---

*Keep this card handy for quick reference while using the Vendor Risk Assessment Tool*

**Version 1.0 | August 2025**
