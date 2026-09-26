---
name: folder-structure
description: Required layout of the IncidentToPR repository — app/ with server.py, routes/ and controllers/, plus tests/, incidents/, reports/, evidence/, metrics/, scripts/ and .bob/. Use before creating, moving, renaming or deciding where to put any file in this project.
---

# Folder structure — where every file goes

Hamza specified this backend layout himself (he uses `server.py` + `routes/` +
`controllers/` across his projects) and reviews code against it. New files go
where it says, not where a tutorial or a generator would put them.

This project has **no frontend**. It is a small FastAPI demo API plus the
IncidentToPR tooling around it.

If a new file has no obvious home below, **stop and ask Hamza before inventing
a folder** — but do not ask about the folders already listed here.

## The tree

```
incident-to-pr/
├── app/                         the ShopLite demo API
│   ├── __init__.py
│   ├── server.py                builds the FastAPI app and mounts routers. Decides nothing.
│   ├── data.py                  in-memory ORDERS and COUPONS constants
│   ├── routes/                  one module per resource: path, method, params, body model
│   │   ├── __init__.py          collects the routers that server.py mounts
│   │   ├── orders.py
│   │   ├── quotes.py
│   │   └── checkout.py
│   └── controllers/             one module per resource: the actual logic
│       ├── __init__.py
│       ├── orders_controller.py
│       ├── quotes_controller.py
│       └── checkout_controller.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py              the `client` fixture (TestClient)
│   ├── test_orders.py           baseline tests
│   ├── test_quotes.py
│   ├── test_checkout.py
│   └── regression/              reproduction tests, one file per incident
│       └── __init__.py
├── incidents/INC-00X/           incident.md + error.log (input, never edited)
├── reports/                     reports/INC-00X/notes.md (Bob) → reports/INC-00X.md (script)
├── evidence/INC-00X/            raw evidence, written only by scripts/evidence.py
├── metrics/runs.csv             experiment record, written only by Hamza
├── scripts/
│   ├── evidence.py              start | run | diff | render
│   └── reset_demo.sh            archive a run and restore the baseline
├── bob_sessions/                task summary screenshots (PNG) for submission
├── .bob/
│   ├── custom_modes.yaml
│   ├── rules-incident-responder/
│   └── skills/<skill-name>/SKILL.md
├── .gitignore  .bobignore  requirements.txt  pytest.ini  README.md  LICENSE
```

## Backend rules (`app/`)

- **`server.py` decides nothing.** It creates the app and includes the routers
  from `routes/__init__.py`. No business logic. The run target is
  `uvicorn app.server:app`.
- **`routes/<resource>.py` only declares.** Path, HTTP method, query/body
  parameters and the Pydantic request model. Each route calls exactly one
  controller function and returns what it returns.
- **`controllers/<resource>_controller.py` does the work** and takes plain
  arguments — never a FastAPI `Request` — so every function can be called
  straight from a test without a server. Controllers return plain dicts or
  values.
- **`data.py` holds constants only.** Nothing mutates it at runtime.
- **No `middleware/` folder in the MVP.** There is no auth, request id or error
  envelope to wire. This bend is recorded as deviation D-16 (see the
  srs-traceability skill). Create it only if a real middleware is needed.
- **No `services/`, `utils/` or `helpers/` folders.** Logic belongs in the
  controller of its resource.

## Test rules (`tests/`)

- Baseline tests live in `tests/test_<resource>.py` and are **never edited**
  once the baseline is tagged.
- Reproduction tests live in `tests/regression/test_<id>.py`, e.g.
  `tests/regression/test_inc003.py`, one file per incident.
- Fixtures live only in `tests/conftest.py`.

## Ownership (who may write where)

| Path | Written by | Bob may edit? |
| --- | --- | --- |
| `app/**` | Hamza (baseline), Bob (fixes) | Yes |
| `tests/regression/**` | Bob | Yes |
| `reports/INC-00X/notes.md` | Bob | Yes |
| `tests/conftest.py`, `tests/test_*.py` | Hamza | No |
| `incidents/**` | Hamza | No |
| `evidence/**`, `reports/INC-00X.md` | `scripts/evidence.py` | No |
| `scripts/**`, `.bob/**`, `metrics/**`, `bob_sessions/**` | Hamza | No |

## Files that must never be inside this folder

`srs.md`, `prd.md`, any technical spec, oracle tests and reference fixes. They
contain the answers to the demo incidents. During the build phase they may sit
**outside** the repository; Bob gets only the sections Hamza pastes in.

## When the layout has to bend

Say so out loud when making the change, and record it as a new `D-nn` entry
(see the srs-traceability skill) rather than leaving silent drift.
