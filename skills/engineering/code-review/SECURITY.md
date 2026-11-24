# Security axis

Read this before opening the diff. It is the whole standard the Security sub-agent applies.

## The one question

Does this change let an untrusted actor reach data or authority it shouldn't?

Every real finding is a variant of one of three trust-boundary crossings:

- **Authority**: at the privileged operation, are *who is acting* and *which object* they act on both checked? A route-level `requireAuth` that never checks ownership is the classic gap (IDOR / BOLA). See ASVS 5.0 `8.2.1` (function-level) and `8.2.2` (data-specific).
- **Interpretation**: does untrusted data get read by the parser that owns it, or by string assembly? Owned parsers: bound query parameters, context-specific output encoding, argv arrays, canonicalise-then-contain for paths. String assembly is the bug.
- **Secrecy and unpredictability**: credentials absent from code, logs and error bodies; tokens from a CSPRNG; crypto from a vetted library in a safe mode.

That is deliberately small. **Control classes don't rot; function names do.** Name the invariant a fix enforces, then verify the exact API against the version in the repo.

## Evidence tiers

Every finding carries exactly one tier. No tier, no finding.

| Tier | Means | Effect |
|---|---|---|
| **Confirmed** | You can write the concrete path from untrusted input to the effect, quoting `file:line` at each step, or a test/PoC demonstrates it. | Blocks merge when Critical or High. |
| **Supported** | It matches a source you fetched **this session**, and the control you recommend is the one that source prescribes. | Advisory. |
| **Unverified** | Pattern-matched. Nothing fetched, nothing demonstrated. | Advisory, and it must say "not verified". Never name a specific API. |

Rules that keep the tiers honest:

- **Fetch or don't cite.** A CWE ID, ASVS requirement, RFC section or doc URL you did not fetch in this session may not appear as support. If the fetch fails, the finding drops to Unverified.
- **Cite the status.** CWE entries carry `Status` (`Stable`, `Draft`, `Incomplete`, `Deprecated`). Record it. `Draft` is weaker support than `Stable`; `Deprecated` means the citation itself is a finding.
- **Match the version.** Read the manifest (`package.json`, `pyproject.toml`, `go.mod`, `composer.json`) and cite docs for *that* version, not latest. A fix for the wrong major version is the failure mode this rule exists to stop.
- **Check the default first.** If the framework's current version already does the safe thing by default, there is no finding. Confirm the default before flagging.
- **A deleted check is a finding.** Removing auth, validation or escaping that used to be there outranks almost anything added.

## Method

1. Name the crossing (authority / interpretation / secrecy).
2. Locate the sink, then trace backwards to the source with `grep`. Quote each hop. Don't reason about what the code "probably" does upstream.
3. State the trust-boundary assumption you used ("assumed `/api/x` is public; `auth.ts:42` covers `/admin`"). Inferred assumptions go in the report; ask only when one is load-bearing and undeterminable.
4. Try to disprove the finding: what check already sits between source and sink?
5. Set the tier. For Supported, fetch the source now.
6. State the fix as the invariant plus the version-correct API, and say what the fix does *not* cover.

## Severity

Severity is about what an attacker gains, not about the tier:

- **Critical**: unauthenticated compromise of data or authority; auth bypass; RCE.
- **High**: authenticated escalation, cross-tenant or cross-user data access, secret exposure.
- **Medium**: needs an unusual precondition, or yields limited read.
- **Low**: defence-in-depth hardening.

## Scope

In scope for a diff: new or changed entry points, authorization decisions, query/HTML/shell/path sinks, secret handling, error bodies, and removed checks.

Out of scope, delegated to tooling: dependency CVEs, secret scanning, TLS/config/IaC. Say so in the report, so silence isn't read as a clean bill.

## Failed-controls register

Mechanisms that were a plausible fix at the time and are now known to fail. If the diff introduces one, or a review recommendation drifts toward one, that is the finding. The register is a backstop for the invariant analysis, never a substitute for it.

| Sold as the fix | Why it fails | Support (status) |
|---|---|---|
| Escaping or stripping quotes before concatenating SQL | Escaping cannot express typed parameters and breaks on numeric, identifier and charset contexts. Binding separates code from data structurally. | CWE-89 (Stable); ASVS 5.0 V1 |
| Stripping `<script>` or regex-"sanitising" HTML | Disallowed-input lists are incomplete by construction; attribute, URL, JS and CSS contexts differ from body text. | CWE-184 (Draft), CWE-79 (Stable) |
| Escaping once and reusing the result everywhere | Encoding is context-specific: HTML body, attribute, URL, JS and CSS all differ. Encode at the sink, for that sink. | CWE-116 (Draft), CWE-79 (Stable) |
| Password composition rules and forced periodic rotation | No measured entropy gain; it drives predictable patterns and weaker reuse. | NIST SP 800-63B-4 §3.1.1.2 ("SHALL NOT impose other composition rules... SHALL NOT require subscribers to change passwords periodically") |
| MD5 / SHA-1 / plain SHA-256 for passwords | Too fast; offline guessing succeeds at scale. Use a memory-hard or iterated KDF. | CWE-916 (Incomplete); ASVS 5.0 V11 |
| `Math.random()` / `random.random()` for tokens or IDs | Not a CSPRNG; internal state is recoverable. | CWE-338 (Draft); ASVS 5.0 V6 |
| Trusting the JWT header, or verifying without pinning the algorithm | The attacker chooses the algorithm (`none`, HS-vs-RS confusion). Pin the expected algorithm and verify the signature against it. | RFC 8725 §3.1; CWE-347 (Draft) |
| `pickle` / `yaml.load` / native deserialisation on untrusted bytes | Construction can execute code. Prefer a data-only format; sign if authenticity matters. | Python docs: "The pickle module is not secure"; CWE-502 (Draft) |
| "Fixing" CORS by reflecting the request `Origin` | Browsers refuse credentials with `*`, so developers echo `Origin` instead, which turns the allowlist into "anyone". Use a fixed allowlist. | MDN `CORSNotSupportingCredentials`; CWE-942 (Incomplete) |
| Client-side validation as the enforcement point | Trivially bypassed; the server is the only trust boundary. | CWE-602 (Draft) |
| `chmod 777` or world-writable to clear a permission error | Removes the control that was working. | CWE-732 (Draft) |
| `rejectUnauthorized: false` / `verify=NONE` to clear a TLS error | Converts a certificate failure into a silent MITM. | CWE-295 (Draft) |
| Stripping `../` once, or `startsWith` on the raw path | Encoded and absolute paths evade it. Canonicalise, then verify containment inside the root. | CWE-22 (Stable) |
| `==` on secrets, tokens or MACs | Early-exit comparison leaks length and prefix through timing. Use a constant-time compare. | CWE-208 (Incomplete) |

## Sources

Verified 2026-11-23. Re-verify before relying on any of them; update the date when you do.

- CWE API: `https://cwe-api.mitre.org/api/v1/cwe/weakness/<id>` (per-entry `Status`)
- CWE Top 25 (2025): `https://cwe.mitre.org/top25/`
- OWASP ASVS 5.0: `https://github.com/OWASP/ASVS/tree/master/5.0/en` (cite by requirement ID, e.g. `8.2.2`)
- OWASP Cheat Sheet Series: `https://cheatsheetseries.owasp.org/`
- NIST SP 800-63B-4: `https://pages.nist.gov/800-63-4/sp800-63b.html`
- RFC 8725, JSON Web Token Best Current Practices: `https://www.rfc-editor.org/rfc/rfc8725.txt`
- CISA KEV: `https://www.cisa.gov/known-exploited-vulnerabilities-catalog` (real-world exploitation evidence for products and dependencies)

## Language packs

The lens above is language-agnostic. Add `packs/<language>.md` only when a review hits something the base lens missed; the pack may add sinks and idioms, and may not weaken the tiers. Load a pack only when the diff touches that language.

Last verified: 2026-11-23.
