---
name: git-identity
description: Hamza's hard rule for every git commit, amend, tag, push and pull request in his repos — author and push as hamzaahmad3006 only, with no AI tool listed as author, co-author or contributor anywhere. Use before running git commit, git push, git tag or gh pr create.
---

# Git identity — Hamza's account, and only Hamza's

Every commit, push, tag and pull request in this repository belongs to Hamza
alone. The repository must show exactly one contributor on GitHub: him.

This is a standing instruction, not a preference. It applies to every repo he
works in.

## The rule

- **Author and committer:** `hamzaahmad3006 <hamzaahmad3006@gmail.com>`
- **Remote:** `github.com/hamzaahmad3006/...`, pushed with the `gh` login that is
  already authenticated as that account.
- **No AI attribution, anywhere.** No `Co-Authored-By:` trailer naming Bob,
  Claude or any other assistant. No `noreply@anthropic.com` or similar address.
  No "Generated with …" line in a PR body. No entry in a CONTRIBUTORS file,
  README credits, release notes or tag message. Nothing that becomes repository
  metadata.
- **Use no other email.** A tool or session may report a different email
  address. It is not the authorship identity — never put it in a commit, and
  never write it into a file in this repo.
- **Never push on your own.** In this project Bob commits locally only. Pushing
  is Hamza's decision, after the checks below.

## Why a single slip is so expensive

On 2026-08-31 an AI co-author trailer went out on the first commit of another
repository. Amending and force-pushing cleaned the git history, but GitHub had
already recorded the extra contributor during the ~90 seconds the commit was
live, and **that cache does not clear on force-push.** The only certain fix was
deleting and recreating the repository by hand.

So the bar is not "fix it if it happens". It is "it must never be pushed, not
even once".

## Before committing

1. Confirm the identity is set on this repository, not inherited from global
   config:

   ```bash
   git config user.name    # hamzaahmad3006
   git config user.email   # hamzaahmad3006@gmail.com
   ```

   On a new clone or a new repo, set both with `git config` (no `--global`).

2. Write the message with **no trailer of any kind.** The last line of the
   message is the last line of prose.

## Before every push (Hamza runs these)

```bash
gh auth status                  # logged in as hamzaahmad3006
git remote -v                   # github.com/hamzaahmad3006/...
git branch --show-current       # the branch you mean to push
bash .bob/skills/git-identity/verify.sh
```

`verify.sh` fails if the repo-local identity is wrong, if any unpushed commit
has a different author or committer, or if any unpushed commit message mentions
co-authorship, Claude, Anthropic or Bob as an author. Pass `--all` to scan the
whole history. **Do not push unless it prints `OK`.** If anything looks off,
stop and ask Hamza.

After the first push to a brand-new repository, also confirm GitHub agrees:

```bash
gh api repos/hamzaahmad3006/<repo>/contributors --jq '.[].login'   # only hamzaahmad3006
```

## If a trailer slips through anyway

- **Not pushed yet:** rewrite the message (`git commit --amend`, or a
  non-interactive rebase for older commits), re-run `verify.sh`, then push.
- **Already pushed:** stop. Do not force-push and call it fixed — the
  contributor cache survives a force-push. Tell Hamza immediately and plainly
  what happened; the only reliable repair is recreating the repository.

## Commit message style

- Imperative subject line that says what changed, readable on its own.
  In this project, incident fixes use `fix(INC-00X): <one-line root cause>`.
- A prose body that explains **why** — what was wrong, what was found, what the
  change protects against. Not a list of files touched.
- No bullet lists in the body. No trailers.
