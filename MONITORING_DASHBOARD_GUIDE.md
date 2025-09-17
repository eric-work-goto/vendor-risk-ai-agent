# Vendor Risk Monitoring Dashboard Guide

## Overview
The Enhanced Monitoring Dashboard provides real-time insights into vendor security risks using 100% real assessment data. No mock or demo data is used - all information comes from actual vendor security assessments.

## Dashboard Components

### 1. Risk Distribution Chart (Pie Chart)
**What it shows:** Visual breakdown of all assessed vendors by security risk level
**Data source:** Real assessment scores from completed vendor evaluations

**Risk Categories:**
- **Excellent (80-100)** - Low risk vendors with strong security compliance (Green)
- **Good (60-79)** - Moderate risk with acceptable compliance levels (Yellow) 
- **Moderate (40-59)** - Elevated risk requiring attention (Orange)
- **High Risk (<40)** - Critical risk requiring immediate action (Red)

**Score Calculation:** Based on comprehensive security assessments including:
- Security posture evaluation
- Compliance framework adherence (GDPR, SOC, ISO 27001, etc.)
- Technical security controls
- Data protection measures
- Incident response capabilities

### 2. Assessment Activity Timeline (Bar Chart)
**What it shows:** Real-time tracking of assessment completion across time periods
**Data source:** Timestamps from completed vendor assessments

**Time Periods:**
- **Last 24 Hours** - Recent assessment activity (Blue bars)
- **Last 7 Days** - Weekly assessment volume (Green bars)  
- **All Time Total** - Complete assessment history (Purple bars)

**Activity Indicators:**
- Bar length shows relative activity levels
- Numbers show exact assessment counts
- Summary shows activity trends (Active/Low, Increasing/Steady/Decreasing)

### 3. Recent Alerts
**What it shows:** Automatically generated alerts from real assessment results
**Data source:** Live analysis of assessment scores, compliance requirements, and vendor characteristics

**Alert Types Generated:**

#### Risk-Based Alerts:
- **🚨 CRITICAL RISK** - Vendors with scores <50 requiring immediate action
- **⚠️ HIGH RISK** - Vendors with scores 50-69 needing enhanced monitoring
- **⚡ MEDIUM RISK** - Vendors with scores 70-79 requiring attention

#### Compliance-Specific Alerts:
- **🛡️ GDPR COMPLIANCE** - GDPR-regulated vendors with scores <85
- **📋 SOC COMPLIANCE** - SOC-regulated vendors with scores <80

#### Special Category Alerts:
- **🤖 AI SERVICES** - Vendors offering AI services requiring governance review
- **🆕 NEW ASSESSMENT** - Recently completed assessments (within 24 hours)

**Alert Information Includes:**
- Vendor name and domain
- Security score and risk level
- Specific compliance frameworks affected
- Impact assessment
- Recommended actions
- Alert severity (Critical/High/Medium/Info)
- Timestamp of assessment

### 4. Score Changes (When Available)
**What it shows:** Historical comparison of vendor security scores over time
**Data source:** Comparison of current assessment scores with historical assessment data

**Change Indicators:**
- **Improved** - Score increased from previous assessment
- **Declined** - Score decreased from previous assessment  
- **New** - First-time assessment with no historical data

## Data Integrity

### Real Data Only
- **REAL_DATA_ONLY=True** mode enforced in backend
- All charts and alerts use actual assessment results
- No mock, demo, or placeholder data
- Live API integration with assessment database

### Refresh Behavior
- Data refreshes automatically when new assessments complete
- Manual refresh available via "Refresh Data" button
- Real-time monitoring integration updates dashboard immediately

## Understanding the Alerts

### Alert Triggers
Alerts are automatically generated when:
1. Assessment scores fall below risk thresholds
2. Compliance-regulated vendors show concerning scores
3. Special vendor characteristics are detected (AI services)
4. New assessments are completed

### Alert Actions
Each alert provides:
- **Clear description** of the risk or issue identified
- **Impact assessment** explaining potential consequences
- **Recommended actions** for risk mitigation
- **Severity classification** for prioritization

### Alert Priority
- **Critical** - Immediate action required (scores <50)
- **High** - Action needed within days (scores 50-69) 
- **Medium** - Attention needed (scores 70-79)
- **Info** - Awareness alerts (new assessments, AI services)

## Monitoring Best Practices

### Regular Review
1. Check dashboard daily for new critical/high alerts
2. Review weekly activity trends in Assessment Timeline
3. Monitor risk distribution changes over time
4. Act on recommended actions promptly

### Alert Management  
1. Address Critical and High severity alerts first
2. Use recommended actions as starting point for remediation
3. Track vendor improvements through score changes
4. Document actions taken for compliance audit trails

### Continuous Improvement
1. Monitor assessment frequency to ensure coverage
2. Track risk distribution improvements over time
3. Use compliance alerts to strengthen vendor contracts
4. Leverage AI service alerts for governance enhancement

## Technical Notes

### Performance
- Dashboard loads real data efficiently
- Charts render responsively across screen sizes
- Background refresh doesn't interrupt user interaction

### Browser Compatibility
- Works in all modern browsers
- JavaScript required for interactive features
- Mobile responsive design

### Data Privacy
- All vendor data handled according to privacy policies
- Assessment results displayed only to authorized users
- Secure API communication for data access