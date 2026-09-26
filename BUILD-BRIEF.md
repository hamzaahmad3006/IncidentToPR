# IncidentToPR — Build Brief

This is the only document Bob needs during the build. It describes a **correct**
application and the tooling around it. Build exactly this — nothing more.
Follow the skills in `.bob/skills/` (folder-structure, build-guardrails,
git-identity, srs-traceability).

Delete this file from the repository before the experiment baseline is tagged.

---

## B1. What we are building

1. **ShopLite API** — a tiny FastAPI shop API with correct behavior.
2. **Baseline tests** — 7 pytest tests.
3. **Evidence tooling** — `scripts/evidence.py` and `scripts/reset_demo.sh`.
4. **Bob configuration** — the Incident Responder custom mode and its rules.

Out of scope: database, frontend, authentication, middleware, external APIs,
MCP, CI, Docker, deployment. Python 3.11, standard library only in `scripts/`.

---

## B2. Project files

```
requirements.txt   fastapi==0.141.1, pydantic==2.13.3, httpx==0.28.1, pytest==9.1.1, uvicorn==0.46.0
pytest.ini         [pytest] testpaths = tests ; addopts = -q
.gitignore         .venv/ __pycache__/ .pytest_cache/ .env .env.*
.bobignore         .venv/ __pycache__/ .pytest_cache/ bob_sessions/
```

Empty placeholder folders with `.gitkeep`: `evidence/`, `bob_sessions/`,
`tests/regression/` (with `__init__.py`), `reports/`.
`metrics/runs.csv` contains only this header line:

```
run_id,incident,condition,operator,head,start_utc,t_repro_s,t_root_cause_s,t_fix_s,t_total_s,oracle_pass,files_changed,lines_changed,unrelated_changes,rule_violations,interventions,bobcoins,recording_ref,archive_path,notes
```

---

## B3. ShopLite API (layout per the folder-structure skill)

### Data — `app/data.py`

- `ORDERS`: list of 25 dicts for i = 1..25:
  `{"id": f"ORD-{i:04d}", "customer": f"customer-{(i % 7) + 1}", "amount": round(10 + i * 3.5, 2)}`
- `COUPONS = {"WELCOME10": 10, "SPRING5": 5}` (percent).

### Endpoints

| Method + path | Route module | Request | Response 200 | Errors |
| --- | --- | --- | --- | --- |
| `GET /orders` | `routes/orders.py` | query `page` int ≥ 1 (default 1), `size` int 1–50 (default 10) | `{page, size, total_pages, items}` | 422 on invalid query |
| `GET /orders/{order_id}` | `routes/orders.py` | path `order_id` | the order dict | 404 `{"detail": "order not found"}` |
| `POST /quotes` | `routes/quotes.py` | `{lines: [{sku: str, price: float > 0, qty: int ≥ 1}], discount_percent: float 0–100 = 0}` | `{total: float, currency: "USD"}` | 422 |
| `POST /checkout` | `routes/checkout.py` | `{cart_total: float, coupons: list[str] = []}` | `{discount_percent: int, payable: float}` | 422 |

Pydantic request models live in the route module that uses them.

### Controllers — exact function names and signatures

Use exactly these names and signatures. Keep every function short and plain.
No comments or docstrings that discuss edge cases.

`app/controllers/orders_controller.py`

- `paginate(items: list, page: int, size: int) -> dict` — 1-based page;
  `start = (page - 1) * size`; `end = start + size`; `total_pages = ceil(len/size)`;
  returns `{"page", "size", "total_pages", "items": items[start:end]}`.
- `list_orders(page: int, size: int) -> dict` — `paginate(ORDERS, page, size)`.
- `get_order(order_id: str) -> dict | None`.

`app/controllers/quotes_controller.py`

- `line_total(price: float, qty: int) -> Decimal` — `Decimal(str(price)) * qty`.
- `quote_total(lines: list[dict], discount_percent: float) -> float` — sum the
  line totals as `Decimal`, apply `(100 - discount_percent) / 100` using
  `Decimal(str(discount_percent))`, then
  `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` and return `float`.
- `create_quote(lines: list[dict], discount_percent: float) -> dict` —
  `{"total": quote_total(...), "currency": "USD"}`.

`app/controllers/checkout_controller.py`

- `resolve_coupons(codes: list[str], applied: list[str] | None = None) -> list[str]`
  — first line: `applied = [] if applied is None else applied`; then append each
  code that is in `COUPONS` and not already in `applied`; return `applied`.
- `discount_for(codes: list[str]) -> int` — sum of `COUPONS[c]` over
  `resolve_coupons(codes)`.
- `checkout(cart_total: float, coupons: list[str]) -> dict` —
  `pct = discount_for(coupons)`;
  `{"discount_percent": pct, "payable": round(cart_total * (100 - pct) / 100, 2)}`.

`app/server.py` creates `app = FastAPI(title="ShopLite API")` and includes the
three routers. Run with `uvicorn app.server:app`.

---

## B4. Baseline tests (exactly 7)

`tests/conftest.py`: a function-scoped `client` fixture returning `TestClient(app)`
(import `app` from `app.server`).

| File | Test | Assertion |
| --- | --- | --- |
| `test_orders.py` | page 2 starts after page 1 | `GET /orders?page=2&size=10` → first item id `ORD-0011` |
| `test_orders.py` | single order | `GET /orders/ORD-0010` → id `ORD-0010` |
| `test_orders.py` | unknown order | `GET /orders/ORD-9999` → 404 |
| `test_quotes.py` | quote without discount | 1 line, price 10.0, qty 2 → total 20.0 |
| `test_quotes.py` | quote with discount | 1 line, price 50.0, qty 2, 10% → total 90.0 |
| `test_checkout.py` | checkout with coupon | cart 100.0, `["WELCOME10"]` → `{"discount_percent": 10, "payable": 90.0}` |
| `test_checkout.py` | invalid coupon ignored | cart 100.0, `["NOPE"]` → status 200 |

Write only these 7. Do not add more tests.
Done when `python -m pytest -q` prints `7 passed`.

---

## B5. `scripts/evidence.py` (FR-021 to FR-028)

Python standard library only. Paths relative to the repository root. Never read
or write environment variables.

| Subcommand | Behavior | Exit code |
| --- | --- | --- |
| `start <ID> <A or B>` | append a `start` event with `condition` and `head` (`git rev-parse HEAD`) | 0; 2 on bad arguments |
| `run <ID> <red, green or suite> -- <command...>` | run the command as an argument list (no shell) from the repo root; write stdout + stderr to `evidence/<ID>/<stage>.txt` prefixed by `$ <command>` and suffixed by `[exit code: N]`; append the same text to `<stage>.history.txt`; append an event with `cmd`, `exit_code`, `ok`, `seconds` (2 decimals); print the output and `[evidence] stage=<stage> ok=<True/False>` | 0 if ok, else 1 |
| `diff <ID>` | write `git diff HEAD` to `diff.patch`; write `git diff --stat HEAD` plus untracked files to `diffstat.txt`; exclude `evidence/`, `reports/`, `metrics/`, `__pycache__`; append a `diff` event with `code_files`, `code_lines_added`, `code_lines_removed` (from `git diff --numstat` under `app/`) and `test_files` | 0; 1 if not a git repo |
| `render <ID>` | build `reports/<ID>.md` (sections below); compute the gate; append a `render` event with `gate` | 0 if PASSED, 1 if FAILED |

**`ok` rules:** `red` is ok **only when the exit code is exactly 1**; `green`
and `suite` are ok only when the exit code is 0.

**Events file:** `evidence/<ID>/events.jsonl`, one JSON object per line,
append-only, `ts` in UTC ISO-8601 (seconds) and `event` on every line.

**Gate:** PASSED only if the latest `red`, `green` and `suite` events are all
ok and occurred in the order red → green → suite.

**Report sections, in order:** `# Evidence report: <ID>`; the contents of
`reports/<ID>/notes.md` (or `_notes.md missing_`); a timeline table (event,
UTC time, exit code, ok); elapsed times start→RED, RED→GREEN, start→render;
RED output; GREEN output; full-suite output; diffstat; the line
`**Verification gate:** PASSED` or `FAILED`.

Keep the file under 250 lines.

## B6. `scripts/reset_demo.sh` (FR-040)

Usage: `scripts/reset_demo.sh <run_id> <A or B>`.

1. Abort with a message if `ITP_RUNS_DIR` is unset.
2. Copy `evidence/`, `reports/` and the output of `git diff HEAD` into
   `$ITP_RUNS_DIR/<run_id>/`.
3. `git switch main`; `git reset --hard baseline-v1-plain` for A or
   `baseline-v1` for B; `git clean -fd`.
4. Delete local branches whose names start with `fix/`.

---

## B7. Bob configuration (FR-033, FR-035)

### `.bob/custom_modes.yaml`

```yaml
customModes:
  - slug: incident-responder
    name: "Incident Responder"
    description: Turns an incident into a reproduced, minimally fixed, verified change.
    roleDefinition: You are a senior on-call engineer. You never change application code until a failing regression test proves the reported bug, and you only claim success from captured test output.
    whenToUse: Use this mode when handling an incident folder under incidents/.
    customInstructions: Always activate the incident-to-pr skill and follow its steps in order. Use scripts/evidence.py for every RED, GREEN and suite run. Keep the todo list updated.
    groups:
      - read
      - - edit
        - fileRegex: "^(app/.*\\.py|tests/regression/.*\\.py|reports/.*\\.md)$"
          description: App code, regression tests and incident notes only
      - execute
      - skill
      - todo
      - subagent
```

### `.bob/rules-incident-responder/01-protocol.md`

```markdown
# Incident Responder: non-negotiable rules

1. R1 No fix before RED. Do not modify any file under app/ until scripts/evidence.py has recorded stage "red" with ok=True for this incident.
2. R2 The reproduction test must fail first (exit code 1) with an assertion showing the incident's wrong value. A passing or erroring test is not a reproduction.
3. R3 Change only the function that causes the incident. No refactors, renames or formatting changes.
4. R4 Allowed changes: the root-cause file under app/, one new file under tests/regression/, and reports/<ID>/notes.md. Never edit evidence/, scripts/, incidents/, .bob/, baseline tests or conftest.py.
5. R5 Never delete, skip, xfail or rename a test.
6. R6 Never weaken an assertion: no pytest.approx, tolerance, loosened comparison or changed expected value.
7. R7 Never change fixtures or test setup to hide state.
8. R13 Keep the public API unchanged: paths, parameters, response fields and types.
9. R14 No numeric hacks, such as adding a small epsilon before rounding.
10. R9 After every fix run the targeted test. Before finishing run the full suite.
```

### `.bob/rules-incident-responder/02-evidence.md`

```markdown
# Evidence rules

1. R8 Run every RED, GREEN and suite test through scripts/evidence.py. Direct pytest output is never evidence.
2. R10 Never claim RED or GREEN without citing the evidence file and its exit code.
3. R11 Generate the report with scripts/evidence.py render. Commit only after it prints gate=PASSED.
4. R12 Review the diff with scripts/evidence.py diff before committing. Never git push.
5. R15 Quote commands and numbers exactly. Write "not verified" when something was not verified.
```

Do **not** create `.bob/rules/` or `AGENTS.md`.
