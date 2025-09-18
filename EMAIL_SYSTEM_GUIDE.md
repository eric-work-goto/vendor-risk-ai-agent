# Assessment Completion Email System

## Overview
The vendor risk assessment system now includes automatic email notifications that are sent when assessment reports are generated. This feature sends the comprehensive PDF report to both the requester and the GRC team automatically.

## Email Configuration

### Current Status: Testing Mode
- **EMAIL_ENABLED = false** (Set in frontend JavaScript)
- Emails are currently **disabled for testing purposes**
- When disabled, detailed logs show what emails would be sent
- All functionality is ready but will not actually send emails

### Production Configuration
To enable email sending in production:

#### Frontend Configuration
In both `combined-ui.html` and `combined-ui-complete.html`, change:
```javascript
// Email Configuration - Set to false for testing, true for production
const EMAIL_ENABLED = false; // Change to true to enable email sending
```

To:
```javascript
// Email Configuration - Set to false for testing, true for production
const EMAIL_ENABLED = true; // PRODUCTION: Email sending enabled
```

#### Backend Configuration
In `web_app.py`, update the EMAIL_CONFIG dictionary with your SMTP settings:

```python
EMAIL_CONFIG = {
    "smtp_server": "your-smtp-server.com",  # e.g., "smtp.gmail.com" or "smtp.office365.com"
    "smtp_port": 587,
    "smtp_username": "your-email@company.com",  # Sending email address
    "smtp_password": "your-app-password",      # App password for Gmail, or regular password
    "from_email": "your-email@company.com"     # From address for emails
}
```

Then uncomment the email sending code in both `send_email()` and `send_assessment_completion_email()` functions:

```python
# Uncomment these lines in production:
with smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as server:
    server.starttls()
    server.login(EMAIL_CONFIG["smtp_username"], EMAIL_CONFIG["smtp_password"])
    server.send_message(msg)
```

## Email Functionality

### When Emails Are Sent
- **Trigger**: Automatically when a user successfully downloads a full assessment report
- **Timing**: After PDF generation completes successfully
- **Frequency**: One email per assessment completion

### Email Recipients
1. **Requester Email**: The email address entered in the assessment form
2. **GRC Team**: grc.risk@goto.com (hardcoded)

### Email Content

#### Subject Line
```
Assessment Completed for {vendor_domain}
```

#### Email Body (Plain Text)
```
{requester_email} has completed an assessment of {vendor_domain}. 
Please review the attached report to view the findings.
```

#### Email Body (HTML Version)
- Professional HTML formatting with company branding
- Assessment details including type and completion timestamp
- System identification footer

#### PDF Attachment
- **Filename**: `{vendor_domain}_assessment_report.pdf`
- **Content**: Complete assessment report with all corporate API sections
- **Size**: Automatically handled (typically 100KB - 500KB)

## Technical Implementation

### Frontend Integration
- `sendAssessmentCompletionEmail()` function handles email preparation
- Integrates with `downloadReport()` function after PDF generation
- Uses FormData to send multipart requests with PDF attachment
- Includes comprehensive error handling and user feedback

### Backend API Endpoint
- **Route**: `POST /api/v1/send-assessment-email`
- **Parameters**: 
  - `requester_email` (Form field)
  - `vendor_domain` (Form field) 
  - `assessment_mode` (Form field)
  - `pdf_report` (File upload)

### Error Handling
- **Frontend**: Shows user-friendly error messages if email fails
- **Backend**: Validates inputs, handles SMTP errors gracefully
- **Logging**: Comprehensive logging for troubleshooting
- **Fallback**: Assessment still completes even if email fails

## Testing & Validation

### Current Testing Mode
When `EMAIL_ENABLED = false`, the system will:
- Log detailed email information to console
- Show what recipients would receive emails
- Display email subject and body content
- Indicate PDF attachment details
- **No actual emails are sent**

### Example Test Output
```
📧 Email functionality disabled for testing. Would send email to: user@company.com and grc.risk@goto.com
Email would be sent with the following details: {
  to: ["user@company.com", "grc.risk@goto.com"],
  subject: "Assessment Completed for example.com",
  body: "user@company.com has completed an assessment of example.com. Please review the attached report to view the findings.",
  attachment: "PDF report attached"
}
```

### Production Verification
To verify email functionality in production:
1. Complete a test assessment with a valid email address
2. Check that both recipients receive the email
3. Verify PDF attachment opens correctly
4. Confirm email formatting appears professional
5. Test with different assessment modes (business risk vs technical due diligence)

## Security Considerations

### Email Security
- Uses STARTTLS for encrypted SMTP connections
- Requires app passwords for Gmail (not regular passwords)
- Email addresses are validated before sending
- PDF attachments are scanned for basic validity

### Data Privacy
- Only sends assessment results to intended recipients
- No sensitive system information in email content
- PDF reports follow existing data classification standards
- Email logs are sanitized (no sensitive data in logs)

## Troubleshooting

### Common Issues
1. **SMTP Authentication Errors**: Check username/password and server settings
2. **Attachment Too Large**: PDF reports should be under 10MB (automatically handled)
3. **Email Delivery Delays**: Normal for enterprise email systems (5-30 minutes)
4. **Spam Filtering**: Whitelist sender address in corporate email systems

### Debug Information
Check console logs and application logs for detailed error information:
- Frontend: Browser developer console
- Backend: Application logs with `📧` prefix for email-related messages

## Benefits

### For Users
- Automatic documentation distribution
- No manual sharing required
- Professional email formatting
- Immediate notification to GRC team

### For GRC Team
- Automatic assessment notifications
- Direct access to detailed reports
- Audit trail of completed assessments
- Reduced manual process overhead

### For Compliance
- Automated evidence collection
- Consistent report distribution
- Timestamped completion records
- Centralized GRC team visibility

## Next Steps

### Immediate
1. **Test the current implementation** with EMAIL_ENABLED = false
2. **Verify email content** appears as expected in logs
3. **Complete assessment workflows** to ensure no disruptions

### For Production
1. **Configure SMTP settings** for your email provider
2. **Set EMAIL_ENABLED = true** in frontend configuration
3. **Uncomment email sending code** in backend functions
4. **Test with sample assessments** to verify functionality
5. **Monitor logs** for successful email delivery confirmation

The email system is fully implemented and ready for production use with minimal configuration changes.