#!/usr/bin/env python3
"""Print one OpenCode session transcript for a retro.

Usage: dump-session.py [SESSION_ID] [--reasoning]

Defaults to $OPENCODE_SESSION_ID. Prints user and background messages, and
each assistant text and tool call with a short result. Pass --reasoning to
include the model's reasoning parts.
"""
import json
import os
import sqlite3
import sys

DB = os.path.expanduser("~/.local/share/opencode/opencode.db")
TRUNC = 1200

QUERY = """
SELECT m.seq, m.type, m.data, p.type, p.data
FROM session_message m
LEFT JOIN session_part p ON p.message_id = m.id
WHERE m.session_id = ?
ORDER BY m.seq, p.ordinal
"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    reasoning = "--reasoning" in sys.argv
    sid = args[0] if args else os.environ.get("OPENCODE_SESSION_ID")
    if not sid:
        sys.exit("pass a session id or set OPENCODE_SESSION_ID")

    db = sqlite3.connect(DB)
    for seq, mtype, mraw, ptype, praw in db.execute(QUERY, (sid,)):
        mdata = json.loads(mraw)
        if mtype == "user":
            print("\n### USER\n%s" % mdata.get("text", ""))
        elif mtype == "synthetic":
            print("\n### BACKGROUND\n%s" % mdata.get("text", ""))
        elif mtype == "assistant" and ptype:
            part = json.loads(praw)
            if ptype == "text":
                print("\n### ASSISTANT\n%s" % part.get("text", ""))
            elif ptype == "tool":
                state = part.get("state", {})
                print("[tool %s] %s" % (part.get("name"),
                                        json.dumps(state.get("input", {}))[:TRUNC]))
                out = "".join(c.get("text", "")
                              for c in state.get("content", []) or [])
                print("   -> %s" % out[:TRUNC].replace("\n", " "))
            elif ptype == "reasoning" and reasoning:
                print("\n### REASONING\n%s" % part.get("text", ""))


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:  # piping into head/less
        sys.stdout = open(os.devnull, "w")
        sys.exit(0)
