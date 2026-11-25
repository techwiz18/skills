---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title in your first sentence, before exploring. If the reference is ambiguous, ask.

Turn each acceptance criterion into a failing test at one stated seam before editing. If no seam is pre-agreed, choose one and state it beside the title. Call the Skill tool with "tdd" at that seam.

Run the repo's check command regularly, a single test file regularly, and the full test suite once at the end. If the repo documents no check command, find its lint/test entry point or ask.

Once done, call the Skill tool with "code-review" to review the work.

Commit your work to the current branch.
