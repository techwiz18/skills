# Session logs (OpenCode)

The transcript lives in `~/.local/share/opencode/opencode.db` (SQLite).
`$OPENCODE_SESSION_ID` names the current session.

Use the bundled dumper. It defaults to `$OPENCODE_SESSION_ID`, prints user and
background messages, and each assistant text and tool call with a short result:

```bash
python3 /home/dan/.agents/skills/retro/scripts/dump-session.py [SESSION_ID] [--reasoning]
```

The schema, if you need to query directly:

- `session_v2` — one row of metadata per session (`id`, `title`, `directory`,
  `time_created`, `time_updated`).
- `session_message` — every event, ordered by `seq`. `type` is `user`,
  `assistant`, `system`, `synthetic`, or `idle`. `data` is JSON. User text is
  `data.text`; assistant rows carry metadata only, and their `data.content` is
  empty.
- `session_part` — the assistant's parts, keyed by `message_id` and `ordinal`.
  `type` is `reasoning`, `text` or `tool`; `data` holds the text, or the tool's
  `state.input` and `state.content` (the result).

For a retro, look for the expensive calls in that output: repeated commands,
failed paths, large result blobs, and turns where the agent had to rediscover
something the environment already knows.
