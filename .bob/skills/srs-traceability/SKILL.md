---
name: srs-traceability
description: How IncidentToPR code stays traceable to its PRD and SRS — SRS ids (FR-nnn, NFR-nn, SEC-nn, AT-nn, WV-nn, CV-nn) in docstrings and test names, deviations recorded as D-nn entries in docs/DECISIONS.md, cuts following the PRD MoSCoW order. Use when adding a script, test, Bob configuration file or README section, when deviating from the SRS, or when cutting scope.
---

# SRS traceability

The PRD and SRS are the source of truth. PRD wins on product intent, SRS wins
on mechanism. **Both are kept outside this repository** because the SRS
contains the answers to the demo incidents. Never look for `srs.md` or
`prd.md` in the workspace, and never ask for Section 9 of the SRS. If you need
a requirement, ask Hamza to paste that section.

## The id families

| Prefix | Meaning | Range |
| --- | --- | --- |
| `FR-nnn` | Functional requirement | FR-001 … FR-043 (plus FR-004b) |
| `NFR-nn` | Non-functional requirement | NFR-01 … NFR-21 |
| `SEC-nn` | Security requirement | SEC-01 … SEC-10 |
| `R1` … `R15` | Incident Responder rules | `.bob/rules-incident-responder/` |
| `AT-nn` | Acceptance test | AT-01 … AT-27 |
| `WV-nn` | Workflow validation | WV-01 … WV-07 |
| `CV-nn` | Bob configuration validation | CV-01 … CV-06 |
| `E-nn` | Error-handling scenario | E-01 … E-10 |
| `D-nn` | Engineering decision / deviation | D-01 … D-15 in the SRS; new ones from D-16 |
| `OQ-nn` | Open question | OQ-01 … OQ-15 |

Do not invent ids outside these families.

## Ids in code

- **Tooling** (`scripts/evidence.py`, `scripts/reset_demo.sh`): the module
  docstring or header comment names the requirements it implements, e.g.
  `"""Evidence capture — FR-023 to FR-028, FR-021 gate."""`.
- **Bob configuration** (`.bob/custom_modes.yaml`, skills, rules): a comment or
  first line naming FR-033, FR-034 or FR-035.
- **Tests of the tooling** name the case: `def test_wv05_render_fails_without_suite()`.
- **Demo application (`app/`) is the exception.** Its docstrings may say what an
  endpoint does (SRS §8.2), but must **never** mention incidents, bugs,
  expected fixes, rounding modes, slicing, shared state or any other hint about
  what is wrong with it. No ids in `app/` at all. This protects the experiment.
- **Baseline tests** (`tests/test_*.py`) likewise carry no incident ids or hints.

## Deviations

A deviation is any place the code does something other than the SRS text.

1. Add a dated entry to `docs/DECISIONS.md` continuing the numbering (D-16,
   D-17, …): what the SRS says, the issue, the resolution, the impact.
2. Tell Hamza, so he can copy the row into SRS §27 outside the repo.
3. If it narrows a claim, add the limitation to the README "Limitations"
   section.
4. `docs/DECISIONS.md` is pushed, so write it without any incident answers.

Already known:

- **D-16** — Backend layout follows Hamza's convention: `app/server.py`,
  `app/routes/`, `app/controllers/` instead of the SRS's `app/main.py`,
  `app/routers/`, `app/services/`. No `middleware/` folder in the MVP. Run target
  becomes `uvicorn app.server:app`. Impact: file names only; endpoints, bugs
  and `fileRegex` (`^app/...`) are unchanged.

## Cuts

Cut order comes from PRD §15 (MoSCoW): cut **Could Have** first, then **Should
Have**. **Must Have is never cut:** the demo app with at least 2 incidents,
incident files, baseline tests, the Incident Responder mode, skill and rules,
the evidence gate, the hidden oracle, at least one A-vs-B pair per shipped
incident, the README, the demo video and the lablab submission.

A cut is written in `docs/DECISIONS.md` as `CUT <date> <item> — <reason>` and
removed from the README and slides in the same commit.
