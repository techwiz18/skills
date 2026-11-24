---
"mattpocock-skills": minor
---

`code-review` gains a third axis. **Security** runs in its own sub-agent alongside Standards and Spec, and asks one question: does this change let an untrusted actor reach data or authority it shouldn't?

Findings carry an evidence tier (Confirmed, Supported, Unverified) and a severity. The reviewer must fetch any source it cites during the session, and must match docs to the version in the project's manifest, so a recommendation cannot rest on a fix that only worked against an older major. `SECURITY.md` carries the lens, the tiers, and a cited register of mechanisms that once looked like fixes and are known to fail.

Security is the one documented exception to the skill's no-ranking rule: a Confirmed Critical or High finding ends that block with a go/no-go.
