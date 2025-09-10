# payload lists and helpers
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "\"'><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>"
]

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "'; DROP TABLE users; --"
]

COMMON_CSRF_FIELDS = ["csrf_token", "csrfmiddlewaretoken", "token", "authenticity_token"]

def guess_severity(vuln_type):
    if vuln_type == "XSS":
        return "High"
    if vuln_type == "SQLi":
        return "Critical"
    if vuln_type == "CSRF":
        return "Medium"
    return "Low"
 