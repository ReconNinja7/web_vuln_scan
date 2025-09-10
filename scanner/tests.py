import requests
from urllib.parse import urljoin
from .utils import XSS_PAYLOADS, SQLI_PAYLOADS, COMMON_CSRF_FIELDS, guess_severity

class ScannerEngine:
    def __init__(self, timeout=6):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent":"WebScanner/1.0"})

    def test_form(self, base_url, form):
        findings = []
        action = form.get("action") or base_url
        if not action.startswith("http"):
            action = urljoin(base_url, action)
        method = form.get("method", "get").lower()
        inputs = form.get("inputs", [])

        # form param names
        param_names = [i['name'] for i in inputs if i.get('name')]

        # CSRF naive test: check for typical hidden token fields
        has_token = any(n in COMMON_CSRF_FIELDS for n in param_names)
        if not has_token:
            findings.append({"param": "(form)", "vuln": "CSRF", "evidence": "No CSRF token field found", "severity": guess_severity("CSRF")})

        # XSS testing: send payloads to each param
        for p in param_names:
            for payload in XSS_PAYLOADS:
                data = {name: (payload if name==p else "") for name in param_names}
                try:
                    if method == "post":
                        resp = self.session.post(action, data=data, timeout=self.timeout)
                    else:
                        resp = self.session.get(action, params=data, timeout=self.timeout)
                except Exception as e:
                    continue
                # look for payload reflection
                if payload in resp.text:
                    findings.append({"param": p, "vuln": "XSS", "evidence": f"Payload reflected in response: {payload}", "severity": guess_severity("XSS")})
                    break

        # SQLi testing: inject SQL payloads and look for errors or changes
        for p in param_names:
            for payload in SQLI_PAYLOADS:
                data = {name: (payload if name==p else "") for name in param_names}
                try:
                    if method == "post":
                        resp = self.session.post(action, data=data, timeout=self.timeout)
                    else:
                        resp = self.session.get(action, params=data, timeout=self.timeout)
                except Exception as e:
                    continue
                body = resp.text.lower()
                sql_errors = ["sql syntax", "mysql", "syntax error", "unclosed quotation mark", "syntaxerror"]
                if any(err in body for err in sql_errors):
                    findings.append({"param": p, "vuln": "SQLi", "evidence": f"SQL error in response for payload {payload}", "severity": guess_severity("SQLi")})
                    break
        return findings
