# Security Review Command

Performs deep security analysis following OWASP Top 10 and 2026 security best practices. Focuses exclusively on vulnerabilities, threats, and security concerns.

## Objective

Conduct comprehensive security assessment to identify vulnerabilities, insecure patterns, and security risks before code reaches production.

## Usage

**Pattern**: `/security-review [what to review]`

**Examples**:
- `/security-review` → security scan of uncommitted changes
- `/security-review my branch` → security scan of current branch
- `/security-review src/auth/login.ts` → specific file security audit
- `/security-review the authentication code` → security audit of auth logic
- `/security-review for SQL injection` → focused vulnerability scan

## Instructions

### 1. Target Identification

Same as general code review:
- Parse natural language to identify what to review
- Default to uncommitted changes if not specified
- Use Grep/Glob to locate specific methods/classes
- Check conversation history for context

### 2. Security Analysis Layers

#### OWASP Top 10 Coverage

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
- SQL Injection: Unsanitized database queries
- Command Injection: Unvalidated shell commands
- LDAP/NoSQL Injection
- XSS: Unescaped user input in HTML/templates
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

#### Input Validation

**User Input Validation**:
- All user input validated at entry points?
- Type checking enforced?
- Range/format validation?
- Whitelist validation where possible?
- File upload restrictions (type, size)?

**Sanitization**:
- SQL parameters properly escaped/parameterized?
- HTML output properly encoded?
- Command-line arguments sanitized?
- Path traversal protection?

#### Authentication & Authorization

**Authentication**:
- No hardcoded credentials
- Strong password hashing (bcrypt, Argon2, PBKDF2)
- Secure session management
- Token expiration implemented
- Secure password reset flow

**Authorization**:
- Role-based access control (RBAC) enforced
- Principle of least privilege
- Authorization checks on all sensitive operations
- No client-side only authorization

#### Secrets Management

**Scan for**:
- API keys in code/comments/config
- Database credentials
- Private keys
- OAuth secrets
- Third-party service tokens
- Encryption keys

**Check**:
- Environment variables used correctly
- Secrets management service integrated (Vault, AWS Secrets Manager)
- No secrets in version control history
- `.env` files in `.gitignore`

#### Cryptography

**Algorithm Strength**:
- No MD5 or SHA1 for security purposes
- AES-256 or ChaCha20 for encryption
- RSA ≥ 2048 bits or ECDSA
- TLS 1.2+ only

**Implementation**:
- Proper IV/nonce generation
- Secure key derivation
- Authenticated encryption (GCM, Poly1305)
- No custom crypto implementations

#### Error Handling & Information Disclosure

**Check for**:
- Stack traces exposed to users
- Database errors revealing schema
- Detailed error messages in production
- Debug mode enabled in production
- Sensitive data in logs
- Comments containing sensitive info

#### Session Management

**Validate**:
- Secure session cookie flags (HttpOnly, Secure, SameSite)
- Session timeout implemented
- Session regeneration after login
- Proper logout implementation
- No session tokens in URLs

#### API Security

**REST APIs**:
- Rate limiting implemented
- Authentication required
- Input validation on all endpoints
- CORS properly configured
- Content-Type validation
- API versioning

**GraphQL APIs**:
- Query depth limiting
- Query complexity analysis
- Introspection disabled in production
- Proper authentication/authorization

### 3. Risk Assessment

For each finding, assess:

**Severity**:
- **CRITICAL**: Immediate exploitation possible, severe impact
- **HIGH**: Exploitable with moderate effort, significant impact
- **MEDIUM**: Requires specific conditions, moderate impact
- **LOW**: Difficult to exploit, minimal impact
- **INFO**: Security improvement opportunity

**Exploitability**:
- Easy (common tools, no authentication needed)
- Moderate (requires some skill/access)
- Difficult (requires significant expertise)

**Impact**:
- Data breach
- Privilege escalation
- Denial of service
- Information disclosure
- System compromise

### 4. Security Report

```markdown
# Security Review Report

**Target**: [what was reviewed]
**Date**: [timestamp]
**Overall Risk**: 🔴 HIGH | 🟡 MEDIUM | 🟢 LOW

## Executive Summary

[Brief security posture assessment]

**Production Ready**: [Yes/No - must be ZERO critical vulnerabilities]

---

## Critical Vulnerabilities (X)

### [OWASP Category] - [Vulnerability Name]
**Severity**: CRITICAL
**File**: path/to/file.ext:line
**CWE**: CWE-XXX

**Description**: [What is vulnerable]

**Exploit Scenario**: [How an attacker could exploit this]

**Impact**: [Consequences of exploitation]

**Proof of Concept**:
```language
[Example of vulnerable code]
```

**Fix**:
```language
[Secure code example]
```

**References**: [OWASP link, CVE, etc.]

---

## High-Risk Issues (X)

[Same format as critical, but HIGH severity]

---

## Medium-Risk Issues (X)

[Same format, MEDIUM severity]

---

## Low-Risk Issues & Recommendations (X)

[Security improvements and hardening suggestions]

---

## OWASP Top 10 Checklist

- [✅/❌] A01: Broken Access Control
- [✅/❌] A02: Cryptographic Failures
- [✅/❌] A03: Injection
- [✅/❌] A04: Insecure Design
- [✅/❌] A05: Security Misconfiguration
- [✅/❌] A06: Vulnerable Components
- [✅/❌] A07: Authentication Failures
- [✅/❌] A08: Data Integrity Failures
- [✅/❌] A09: Logging Failures
- [✅/❌] A10: SSRF

---

## Security Metrics

| Metric | Count | Status |
|--------|-------|--------|
| Critical Vulnerabilities | X | Must be 0 |
| High-Risk Issues | X | Should be 0 |
| Medium-Risk Issues | X | Review needed |
| Hardcoded Secrets | X | Must be 0 |
| Outdated Dependencies | X | Review needed |

---

## Remediation Priority

### Immediate (Fix Before Deploy)
1. [Critical vulnerabilities that block deployment]

### High Priority (Fix Within 24h)
2. [High-risk issues]

### Standard Priority (Fix Within Week)
3. [Medium-risk issues]

### Backlog (Security Hardening)
4. [Low-risk improvements]

---

## Deployment Decision

**APPROVE FOR PRODUCTION**: ✅ YES | ❌ NO

**Reasoning**: [Must have ZERO critical vulnerabilities]

**Required Actions Before Deploy**:
1. [List of must-fix items]

**Recommended Follow-up**:
1. [Additional security improvements]
```

## Special Focus Areas

**Authentication/Authorization Code**:
- Require manual security expert review
- Test for privilege escalation
- Verify token validation
- Check session management

**Payment Processing**:
- PCI-DSS compliance considerations
- No card data stored insecurely
- Secure communication with payment gateway
- Transaction validation

**File Operations**:
- Path traversal protection
- File type validation
- Size limits enforced
- Malware scanning for uploads

**Database Operations**:
- Parameterized queries only
- Principle of least privilege for DB user
- Encrypted connections
- No dynamic SQL with user input

## Principles

1. **Zero Tolerance**: Critical vulnerabilities always block deployment
2. **Defense in Depth**: Multiple layers of security
3. **Fail Secure**: Errors should deny access, not grant it
4. **Least Privilege**: Minimal permissions by default
5. **Trust Nothing**: Validate all input, even from "trusted" sources
6. **Security by Design**: Not an afterthought
7. **Assume Breach**: Plan for when, not if

## Notes

- This review identifies common vulnerabilities but is not a substitute for:
  - Penetration testing
  - Security expert manual review
  - Dynamic application security testing (DAST)
  - Static application security testing (SAST) tools
- Always require human security review for critical paths
- Stay updated on latest CVEs and attack techniques
