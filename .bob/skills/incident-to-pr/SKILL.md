---
name: incident-to-pr
description: Handle a production incident from incidents/INC-XXX by reproducing it with a failing regression test, applying the smallest fix, verifying RED to GREEN with scripts/evidence.py, and producing an evidence report and commit.
---

# Incident to PR protocol

You are handling one incident folder: `incidents/<ID>/`. Follow the steps in
order. Each step has an exit condition. Do not start a step until the previous
exit condition is met. If a step fails, stop, explain what you observed, and
follow that step's "If it fails" instruction. Never skip ahead.

Before starting, create a todo list with the step names (Step 0 to Step 11) and
update it as you go.

## Step 0: Start the clock

Run: `python scripts/evidence.py start <ID> B`
Exit: the command exits 0.

## Step 1: Read the incident

Read `incidents/<ID>/incident.md` and `incidents/<ID>/error.log`. If an
`incident.docx` exists in the folder, read it too.
Write down, with values copied exactly from the files: the endpoint, the exact
request input, the actual output, and the expected output.
Exit: all four are stated.
If it fails: if the expected behavior is unclear, ask the developer. Do not guess.

## Step 2: Inspect the relevant code

Trace the endpoint from `app/routes/` to the controller function it calls. Read
only the files on that path. Do not read regression tests of other incidents.
Exit: you can name the function that produces the wrong value.

## Step 3: State a root-cause hypothesis

In one or two sentences give the file, the line, and why that line produces the
observed output for the observed input. Label it "hypothesis".
Exit: the hypothesis predicts the exact wrong value seen in the log.
If it fails: go back to Step 2.

## Step 4: Write the reproduction test

Create `tests/regression/test_<id>.py`, where `<id>` is the incident id in
lower case without the hyphen (for example `tests/regression/test_inc003.py`).

- Use the `client` fixture from `tests/conftest.py`.
- Use the exact input from the incident.
- Assert the exact expected value from `incident.md`. No `pytest.approx`, no
  tolerance.
- If the bug needs more than one request to appear, make all of them in one test.

Do not change any file under `app/` in this step.
Exit: the test file exists and follows these rules.

## Step 5: Confirm RED

Run: `python scripts/evidence.py run <ID> red -- python -m pytest <test file> -q`
Exit: the script prints `ok=True` for stage red, and the assertion message shows
the wrong value from the incident.
If it fails:
- If the test passed, your hypothesis or your test is wrong. Go back to Step 3.
- If there is an import or collection error, fix the test (not the app) and rerun.

## Step 6: Apply the smallest fix

Change only the function named in your hypothesis. Keep the public API the same:
paths, parameters, response field names and types.
Do not edit tests, `scripts/`, `.bob/` or `incidents/`.
Exit: the diff is limited to the root-cause file.

## Step 7: Run the target test

Run: `python scripts/evidence.py run <ID> green -- python -m pytest <test file> -q`
Exit: `ok=True` for stage green.
If it fails: revise the fix (back to Step 6). After 3 failed attempts, stop and
ask the developer, showing the latest output.

## Step 8: Run the full suite

Run: `python scripts/evidence.py run <ID> suite -- python -m pytest -q`
Exit: `ok=True` for stage suite.
If it fails: your fix caused a regression. Go back to Step 6. Never edit, skip
or delete an existing test to make it pass.

## Step 9: Inspect the diff

Run: `python scripts/evidence.py diff <ID>`
Exit: the changed files are only the root-cause file and the new regression test.
If it fails: revert the unrelated changes, then rerun Steps 7 and 8.

## Step 10: Write the evidence report

Copy `notes-template.md` from this skill's folder to `reports/<ID>/notes.md` and
fill every section. Quote numbers only from files in `evidence/<ID>/`.
Then run: `python scripts/evidence.py render <ID>`
Exit: the script prints `gate=PASSED`.
If it fails: find which stage is missing or failed and redo it. Never edit
evidence files.

## Step 11: Commit

Only if Step 10 printed `gate=PASSED`:

```
git switch -c fix/<id-with-hyphen-lowercase>
git add app tests reports evidence
git commit -m "fix(<ID>): <one-line root cause>"
```

Follow the git-identity skill: no trailers of any kind. Do not push. Pushing and
opening a pull request are the developer's decisions.
Exit: `git log` shows the commit on the fix branch.
