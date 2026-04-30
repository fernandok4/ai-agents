---
name: frontend-security-standards
description: Shared frontend security criteria including client-side OWASP checklist, XSS patterns, and severity definitions used by frontend-security-reviewer agent.
---

# Frontend Security Standards

Shared security criteria for client-side code. Agents referencing this skill use these as their baseline.

## Client-Side OWASP Coverage

**A01: Broken Access Control (Client-Side)**
- UI showing admin features to non-admin users (even if API blocks it)
- Client-side route guards without server-side enforcement
- Sensitive data in client-accessible storage
- Open redirects after login/logout

**A02: Cryptographic Failures**
- Secrets, API keys, or tokens in client-side code or public env vars
- Sensitive data in localStorage/sessionStorage without encryption
- Tokens in URL parameters (visible in browser history, logs, referrer headers)

**A03: Injection (Client-Side)**
- XSS via `dangerouslySetInnerHTML`, `v-html`, `innerHTML`, `[innerHTML]`
- XSS via template literals injected into DOM
- URL injection — user-controlled values in `href`, `src` without validation
- `javascript:` URI schemes in links
- Dynamic script/style injection with user content
- Unsanitized Markdown/rich-text rendering
- SVG injection with embedded scripts
- PostMessage handling without origin validation

**A04: Insecure Design**
- Security decisions made client-side only (role checks, feature flags with sensitive data)
- Missing CSRF tokens on state-changing forms
- Auto-complete on sensitive fields (password change, credit card)
- No confirmation for destructive actions

**A05: Security Misconfiguration**
- Source maps enabled in production
- Verbose error messages exposing internals to users
- Console.log statements with sensitive data in production
- Debug/development modes enabled in production builds

**A06: Vulnerable Components**
- Frontend dependencies with known CVEs
- Outdated libraries with security patches available
- CDN scripts without Subresource Integrity (SRI)

**A07: Authentication Failures (Client-Side)**
- Access tokens stored in localStorage (vulnerable to XSS)
- Refresh tokens accessible to JavaScript
- No token expiry handling (stale sessions)
- Missing logout cleanup (tokens, state, cache)
- Session state only in client memory (lost on refresh)

## XSS Detection Patterns

Actively scan for these patterns:

| Pattern | Risk | Detection |
|---------|------|-----------|
| `dangerouslySetInnerHTML` | High — raw HTML injection | Grep for the property name |
| `v-html` | High — Vue raw HTML | Grep in .vue files |
| `innerHTML =` | High — DOM manipulation | Grep in .js/.ts files |
| `[innerHTML]` | High — Angular binding | Grep in .html/.component files |
| `document.write` | High — DOM injection | Grep in all JS/TS |
| `eval(` | Critical — code execution | Grep in all JS/TS |
| `new Function(` | Critical — dynamic code | Grep in all JS/TS |
| `javascript:` | High — URI scheme | Grep in JSX/HTML/templates |
| `location.href = userInput` | High — open redirect | Manual review |
| `postMessage(` without origin | Medium — cross-origin | Grep + context review |

## Secrets Detection Patterns

Scan for exposed secrets in client code:
- `REACT_APP_` / `NEXT_PUBLIC_` / `VITE_` env vars containing secrets
- `api[_-]?key\s*=\s*["']` — API keys in code
- `sk[_-]live[_-]` — Stripe live keys
- `AKIA[A-Z0-9]{16}` — AWS access keys
- `ghp_[a-zA-Z0-9]{36}` — GitHub personal tokens
- `password\s*=\s*["']` — hardcoded passwords
- `secret\s*=\s*["']` — generic secrets
- `-----BEGIN (RSA |EC )?PRIVATE KEY` — private keys

If any match is found in client-side code, classify as CRITICAL immediately.

## Security Severity Definitions

| Severity | Definition | Frontend Examples |
|----------|-----------|-------------------|
| CRITICAL | Exploitable now, direct data breach or code execution | XSS with user content, exposed secrets in bundle, `eval()` with user input |
| HIGH | Exploitable with moderate effort, significant impact | Tokens in localStorage, open redirects, missing origin validation on PostMessage, URL injection |
| MEDIUM | Requires specific conditions to exploit | Missing SRI on CDN scripts, console.log with sensitive data, source maps in production, missing CSRF |
| LOW | Hardening improvement, low exploitability | Overly permissive CORS (non-credentialed), missing security headers (informational), autocomplete on sensitive fields |

## False-Positive Handling

Before reporting a finding, verify:
- Is the code actually reachable in production? (Not dev-only or test-only)
- Is there a sanitization library in use that handles the input? (DOMPurify, sanitize-html)
- Is the "secret" actually a public key or a placeholder?
- Is the framework providing built-in protection? (React auto-escapes JSX, Angular sanitizes by default)

If uncertain, report the finding and append: `(Confidence: Low — verify manually)`
