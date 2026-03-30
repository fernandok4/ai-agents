---
name: security-standards
description: Shared security criteria including OWASP Top 10 checklist, secrets detection patterns, and severity definitions used by security-reviewer agent.
user-invocable: false
---

# Security Standards

Shared security criteria. Agents referencing this skill use these as their baseline.

## OWASP Top 10 Coverage

**A01: Broken Access Control**
- Missing authorization checks
- Insecure direct object references
- Path traversal vulnerabilities
- CORS misconfiguration

**A02: Cryptographic Failures**
- Hardcoded secrets, API keys, passwords
- Weak encryption algorithms (MD5, SHA1 for security)
- Insecure random number generation
- Unencrypted sensitive data
- Missing HTTPS enforcement

**A03: Injection**
- SQL Injection: unsanitized database queries
- Command Injection: unvalidated shell commands
- LDAP/NoSQL Injection
- XSS: unescaped user input in HTML/templates
- Template Injection

**A04: Insecure Design**
- Missing rate limiting
- No input validation at boundaries
- Insecure state management
- Missing security controls in design

**A05: Security Misconfiguration**
- Default credentials still active
- Verbose error messages exposing internals
- Unnecessary features enabled
- Unpatched systems/dependencies

**A06: Vulnerable Components**
- Outdated dependencies with known CVEs
- Deprecated libraries
- Unverified third-party code

**A07: Authentication Failures**
- Weak password requirements
- No account lockout mechanism
- Insecure password reset
- Missing MFA support
- Session fixation vulnerabilities
- Weak session management

**A08: Software and Data Integrity Failures**
- Insecure deserialization
- Unsigned/unverified updates
- CI/CD pipeline vulnerabilities

**A09: Logging and Monitoring Failures**
- Insufficient logging
- Logs containing sensitive data
- No alerting for security events
- Missing audit trail

**A10: Server-Side Request Forgery (SSRF)**
- Unvalidated URLs in requests
- Internal service exposure
- Cloud metadata access

## Secrets Detection Patterns

Actively scan for these patterns using Grep:
- `password\s*=\s*["']` — hardcoded passwords
- `api[_-]?key\s*=\s*["']` — API keys in code
- `sk[_-]live[_-]` — Stripe live keys
- `AKIA[A-Z0-9]{16}` — AWS access keys
- `ghp_[a-zA-Z0-9]{36}` — GitHub personal tokens
- `-----BEGIN (RSA |EC )?PRIVATE KEY` — Private keys
- `secret\s*=\s*["']` — Generic secrets

If any match is found, classify as CRITICAL immediately.

## Security Severity Definitions

| Severity | Definition | Examples |
|----------|-----------|----------|
| CRITICAL | Exploitable now, direct data breach or system compromise | SQL injection, hardcoded secrets, auth bypass, RCE |
| HIGH | Exploitable with moderate effort, significant impact | Weak crypto (MD5/SHA1), missing auth on sensitive endpoints, SSRF |
| MEDIUM | Requires specific conditions to exploit | Missing rate limiting, verbose error messages, CORS too permissive |
| LOW | Hardening improvement, low exploitability | Missing security headers, optional HTTPS enforcement, info disclosure |

## False-Positive Handling

Before reporting a finding, verify:
- Is the code actually reachable in production? (Not dead code or test-only)
- Is there framework-level protection already in place? (e.g., ORM parameterization, CSRF middleware)
- Is the "secret" actually a placeholder/example value?

If uncertain, report the finding and append: `(Confidence: Low -- verify manually)`
