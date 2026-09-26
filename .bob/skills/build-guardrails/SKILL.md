---
name: build-guardrails
description: Rules for building the IncidentToPR repository during the IBM Bob 2.0 Hackathon — 40-Bobcoin budget, no bugs or hints written by Bob, protected folders, bob_sessions screenshots. Use for any build or setup task in this repo that is not an incident run.
---

# Build guardrails (build phase only)

This skill applies while the repository is being built. It is removed from
`.bob/skills/` before the experiment baseline is tagged.

## 1. Bobcoins are scarce

The hackathon account has **40 Bobcoins in total**, and no more are given when
they run out. Every build task spends from the same budget as the demo and the
A/B runs.

- Do one small, clearly scoped task at a time. If a request would touch more
  than about 5 files, propose splitting it first.
- Read only the files you need. Use `@file` references; never load the whole
  repository.
- Do not re-read large documents Hamza has already pasted; ask for the specific
  section instead.
- Do not run long exploratory command loops. If something fails twice, stop and
  report.
- At the end of each task, tell Hamza it is a good moment to note the Bobcoin
  usage (Settings → General).

## 2. Build a correct application — never the bugs

Build the ShopLite API exactly as described, with **correct** behavior.
Hamza adds the demo incidents himself, by hand, after the build.

- Do not write any intentionally wrong code.
- Do not write comments, TODOs, docstrings, variable names, commit messages or
  files that mention bugs, incidents, "off-by-one", rounding problems, shared
  state, or how anything could break.
- Do not create files under `incidents/`, `evidence/` or `metrics/`, and do not
  write regression tests under `tests/regression/`. Those belong to the
  experiment.

## 3. Documents with answers stay out

`srs.md`, `prd.md`, the technical spec and oracle tests must never be placed in
this repository, and you must not search for them. If you need a requirement,
ask Hamza to paste the relevant section.

## 4. Protected files

Do not modify `scripts/evidence.py` or `scripts/reset_demo.sh` after Hamza has
reviewed them, and never modify anything under `.bob/` unless Hamza asks for
that exact file.

## 5. Evidence of Bob usage (required for judging)

The hackathon requires task session summary screenshots in `bob_sessions/`.
After every task, remind Hamza to open **Tasks**, select this task, click the
task header, and save the consumption summary as a PNG named
`proofbeforepatch_taskNN_<short-topic>_summary.png`. You cannot take the
screenshot yourself; just remind him.

## 6. Git

Follow the git-identity skill for every commit. Never push.
