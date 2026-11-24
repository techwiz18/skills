# PHP pack

Load when the diff touches `*.php`, `*.blade.php`, Twig templates, or `composer.json`.
Version: read `require.php` in `composer.json`, then cite the manual for that version.

## Sinks

| Untrusted data reaching | Owned parser | Fails when |
|---|---|---|
| SQL | PDO or mysqli prepared statements with bound parameters | interpolation into the query, or `mysqli_real_escape_string` / `addslashes` as the only defence |
| HTML or template | Twig/Blade auto-escaping; `htmlspecialchars` with `ENT_QUOTES` for the HTML body only | `{!! !!}`, `\|raw`, `echo` of request data, or one escape reused in attributes and JS |
| Shell | `proc_open`/`exec` with an argument array, or `escapeshellarg` per part | `shell_exec`, backticks, `system`, `passthru` on a built string |
| Filesystem | `realpath()` then verify the result is inside the base directory | `include`/`require` with request data (LFI), `file_get_contents` on a user path |
| Serialized data | `json_decode` | `unserialize()`: php.net warns against untrusted input "regardless of the options value of allowed_classes" |
| Code | none, do not evaluate input | `eval`, `assert` with a string, variable functions from request data |
| Request data into scope | explicit `$data['key']` access | `extract()` over request data, `$$name`, `compact()` over request data (CWE-915, Incomplete) |
| Redirect | a fixed map or allowlist | `header("Location: " . $_GET[...])` (CWE-601, Draft) |

## Ecosystem failed controls

- `unserialize` with `allowed_classes => false` as the fix. The manual still says not to pass untrusted input to it, and autoloading can still run.
- `md5`/`sha1` for passwords. Use `password_hash`/`password_verify`; `PASSWORD_DEFAULT` is designed to change, so the column has to hold the growth (255 bytes recommended). CWE-916 (Incomplete).
- `htmlspecialchars` as a global sanitiser. Encoding is per context, and that includes `href` and inline JS. CWE-116 (Draft).
- `addslashes` on data that will also be JSON-encoded, or any escape applied twice. Double encoding is its own bypass.

## Docs (verified 2026-11-23)

- `https://www.php.net/manual/en/function.unserialize.php`
- `https://www.php.net/manual/en/function.eval.php`
- `https://www.php.net/manual/en/function.password-hash.php`
