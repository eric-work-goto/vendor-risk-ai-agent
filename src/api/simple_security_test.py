import re

def detect_sql_injection(value: str) -> bool:
    """Detect potential SQL injection patterns"""
    if not isinstance(value, str):
        return False
    
    sql_patterns = [
        r"(?i)(union|select|insert|update|delete|drop|create|alter|exec|execute)",
        r"(?i)(script|javascript|vbscript|onload|onerror)",
        r"(?i)(\-\-|\#|\/\*|\*\/)",
        r"(?i)(or\s+1\s*=\s*1|and\s+1\s*=\s*1)",
        r"(?i)(xp_|sp_|exec\s*\()",
        r"(?i)(benchmark|sleep|waitfor|delay)"
    ]
    
    for pattern in sql_patterns:
        if re.search(pattern, value):
            return True
    return False

def sanitize_input(value: str, max_length: int = 1000) -> str:
    """Comprehensive input sanitization"""
    if not isinstance(value, str):
        return str(value)
    
    # Check for SQL injection
    if detect_sql_injection(value):
        raise ValueError("Potential SQL injection detected")
    
    # Remove non-printable characters except normal whitespace
    value = ''.join(char for char in value if char.isprintable() or char in ['\n', '\r', '\t', ' '])
    
    # Trim whitespace and limit length
    value = value.strip()[:max_length]
    
    # Additional security checks
    dangerous_patterns = [
        r"<script[^>]*>.*?</script>",  # Script tags
        r"javascript:",                # JavaScript URLs
        r"data:text/html",            # Data URLs
        r"vbscript:",                 # VBScript URLs
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValueError("Potentially dangerous content detected")
    
    return value

# Test the functions
print('Testing SQL injection detection:')
print(detect_sql_injection("'; DROP TABLE assessments; --"))
print('Testing sanitization:')
print(sanitize_input('test.com'))
