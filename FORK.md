# Fork notes

Personal fork of `mattpocock/skills`. Two branches, one rule each:

- `main` mirrors upstream. Never commit to it.
- `local` holds every local change. It is the default branch, and the skill symlinks in `~/.agents/skills` serve it.

## Taking upstream updates

```
git fetch upstream
git rebase upstream/main
git push --force-with-lease origin local
```

`git push origin upstream/main:main` keeps the mirror fresh as well, without checking anything out.

Because `local` is rebased rather than merged, upstream changes land underneath the local commits. They cannot overwrite them: overlapping edits show up as conflicts you resolve once, in the file both sides touched.

## Recovery

`origin/local` is the backup. Anything lost locally comes back with:

```
git fetch origin && git reset --hard origin/local
```

The tag `local-patches-v1` marks the first cut of the security axis, and `git reflog` covers everything after it.

## Conflicts to expect on a rebase

- `skills/engineering/code-review/SKILL.md`
- `docs/engineering/code-review.md`
- `README.md`, `skills/engineering/README.md`, `skills/engineering/ask-matt/SKILL.md`, `docs/engineering/implement.md`
- `.changeset/`

`SECURITY.md` and `packs/` are files upstream has no copy of, so they never conflict.
