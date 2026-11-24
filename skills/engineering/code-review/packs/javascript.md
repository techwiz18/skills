# JavaScript / TypeScript pack

Load when the diff touches `*.js`, `*.jsx`, `*.ts`, `*.tsx`, `*.mjs`, `*.cjs`, or `package.json`.
Version: read `engines.node` and the framework majors in `dependencies`. React 19 and Express 5 differ from their predecessors on escaping and routing defaults.

## Sinks

| Untrusted data reaching | Owned parser | Fails when |
|---|---|---|
| HTML | framework escaping (JSX text), or Trusted Types | `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, jQuery `.html()`, `dangerouslySetInnerHTML`. MDN calls these "injection sinks ... potentially a vector for cross-site scripting" (CWE-79, Stable) |
| Shell | `execFile` or `spawn` with an argument array | `exec`, `execSync`, or `spawn(..., { shell: true })`. Node: "Never pass unsanitized user input to this function" |
| Code | none, do not evaluate input | `eval`, `new Function`, and `vm`, which Node says "is not a security mechanism. Do not use it to run untrusted code" |
| Outbound request | a host allowlist before `fetch` | `fetch(req.body.url)` or a proxy endpoint taking a URL (CWE-918, Incomplete) |
| Objects | schema validation, plus own-property checks | recursive merge or `Object.assign` of user JSON, which reaches `__proto__` (CWE-1321, Incomplete) |
| Regex | bounded input length, or a linear-time engine | nested quantifiers applied to long user input (CWE-1333, Draft) |
| Tokens | `crypto.randomUUID()` or `crypto.randomBytes()` | `Math.random()` (CWE-338, Draft) |
| Redirect | a fixed allowlist | `res.redirect(req.query.next)` (CWE-601, Draft) |

## Ecosystem failed controls

- `vm` or `vm2` as a sandbox for plugins or user templates. Node disclaims `vm` in its own docs, and a sandbox in the same process shares the agent's credentials. Use a separate process with none.
- A regex that strips `<script>` or `on\w+=`. Disallowed-input lists are incomplete. CWE-184 (Draft).
- `helmet()` as the XSS fix. Response headers help, but the sink is still the sink.
- Client-side validation as the boundary. CWE-602 (Draft).
- Escaping helpers applied without knowing the context: an `escapeHtml` used in an `href` or inside a `<script>` block. CWE-116 (Draft).

## Docs (verified 2026-11-23)

- `https://nodejs.org/api/vm.html`
- `https://nodejs.org/api/child_process.html`
- `https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML`
