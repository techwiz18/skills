# Java pack

Load when the diff touches `*.java`, `*.kt`, `*.jsp`, `pom.xml`, or `build.gradle*`.
Version: read `maven.compiler.release` / `sourceCompatibility`, and the Spring Boot version if present. Spring Security majors differ on defaults.

## Sinks

| Untrusted data reaching | Owned parser | Fails when |
|---|---|---|
| SQL | `PreparedStatement` and `setX` | `Statement.execute` with concatenation, or JPQL built by string concat |
| HTML or JSP | JSTL `<c:out>`, or the template engine's auto-escaping | `<%= %>`, `out.print(input)`, Thymeleaf `th:utext`, `th:attr` with a user URL |
| Shell | `ProcessBuilder` with a `List` | `Runtime.exec(String)`, or `sh -c` with a built string (CWE-78, Stable) |
| XML | `DocumentBuilderFactory` with `FEATURE_SECURE_PROCESSING`, `disallow-doctype-decl=true`, and external entities false; `XMLInputFactory.SUPPORT_DTD=false` for StAX | parser defaults left on, which resolve external entities (CWE-611, Draft). Verify each factory used, not just one |
| Deserialisation | JSON, not native Java serialisation | `ObjectInputStream.readObject` on untrusted bytes. The javadoc: "Deserialization of untrusted data is inherently dangerous and should be avoided" |
| Expression or script | never evaluate request data | SpEL, OGNL, or `ScriptEngine` on user input (CWE-94, Draft; CWE-470, Draft) |
| Filesystem | `Path.normalize()`, then a containment check, and reject absolute inputs | `new File(base + input)`, or zip entry extraction without a per-entry check (CWE-22, Stable) |
| XPath | variables through `XPathExpression` | concatenation into the expression (CWE-643, Incomplete) |
| Redirect | a fixed allowlist | `sendRedirect(request.getParameter("next"))` (CWE-601, Draft) |

## Ecosystem failed controls

- `ObjectInputFilter` allowlist as the fix for deserialisation. The javadoc's direction is to avoid deserialising untrusted data at all; a filter narrows the blast radius, it does not make the sink safe.
- `java.util.Random` for tokens. Use `SecureRandom`. CWE-338 (Draft).
- `input.replace("../", "")` for path traversal. Encoded and absolute forms survive it; canonicalise and check containment instead. CWE-22 (Stable).
- `csrf().disable()` added to make an API call work, with no other authentication. Check what replaced it (ASVS 5.0 V7).

## Docs (verified 2026-11-23)

- `https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/io/ObjectInputStream.html`
- `https://docs.oracle.com/en/java/javase/21/security/java-api-xml-processing-jaxp-security-guide.html`
