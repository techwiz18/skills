# C# / .NET pack

Load when the diff touches `*.cs`, `*.cshtml`, `*.razor`, `*.csproj`, `*.sln`, or `web.config`.
Version: read `TargetFramework` in the `.csproj`. It changes the answer: `BinaryFormatter` throws on use from .NET 9.

## Sinks

| Untrusted data reaching | Owned parser | Fails when |
|---|---|---|
| SQL | `SqlCommand` with `Parameters.Add` | interpolation or `+` into `CommandText`, including via `FromSqlRaw` |
| HTML or Razor | Razor auto-encoding | `Html.Raw`, `MvcHtmlString`, hand-built `StringBuilder` responses, `@Html.Raw(Model.X)` |
| Shell | `ProcessStartInfo.ArgumentList` | `Process.Start("cmd /c " + input)`, or an `Arguments` string built from input (CWE-78, Stable) |
| Filesystem | `Path.GetFullPath` then a containment check against the base directory | string concatenation into a path, or `ZipFile` extraction without checking each entry stays under the target (CWE-22, Stable) |
| XML | `XmlReaderSettings` defaults (`DtdProcessing` is `Prohibit` by default) | enabling DTD processing, or setting an `XmlResolver` (CWE-611, Draft) |
| Deserialisation | `System.Text.Json` with a fixed type | `BinaryFormatter` (see below), or Newtonsoft `TypeNameHandling` other than `None` (CWE-502, Draft) |
| Model binding | an explicit DTO or `[Bind]` allowlist | binding request data straight onto an EF entity (over-posting, CWE-915, Incomplete) |
| Redirect | a fixed allowlist | `Redirect(Request.Query["next"])` (CWE-601, Draft) |

## Ecosystem failed controls

- `BinaryFormatter` gated behind a "trusted data" check. Microsoft: applications should stop using it "even if they believe the data they're processing to be trustworthy", and it is "insecure and can't be made secure". Microsoft's own migration guide is the fix.
- Request validation, or `[ValidateInput(false)]` toggled back on, as an XSS defence. It is a character blacklist. CWE-184 (Draft).
- `System.Random` for tokens, salts or password resets. Microsoft: use `RandomNumberGenerator` for anything cryptographically secure. CWE-338 (Draft).
- `[Authorize]` on the controller as the only check for an action that takes an id. That is function-level only; the object check is separate (ASVS 5.0 `8.2.1` and `8.2.2`).

## Docs (verified 2026-11-23)

- `https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide`
- `https://learn.microsoft.com/en-us/dotnet/api/system.xml.xmlreadersettings.dtdprocessing`
- `https://learn.microsoft.com/en-us/dotnet/api/system.random`
