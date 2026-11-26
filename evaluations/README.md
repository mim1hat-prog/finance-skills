# Public development cases

**Prepared and unrun in native Copilot/Gemini.** Four independently invented
cases make the [evaluation protocol](../docs/EVALUATION.md) usable without
company data. The release gate validates fixture integrity and bookkeeping,
not model performance.

| Case | Objective check |
| --- | --- |
| Reconciliation | Exact bridge, retained unmatched keys and no invented cause |
| Quantity, price and FX | Ordered contributions with the declared JPY/USD quote |
| Ambiguous mapping | Duplicate and missing rules stay unresolved, including signs |
| Cutoff and missing input | Retained historical vintage; no public substitution for an internal blank |

`cases.json` identifies **case set 1.0.0** and binds each prompt and answer file
to its SHA-256. Plans and summaries retain that version and manifest hash. The answer keys
are deliberately public, so this is a **development set, not a holdout**.
Do not give answer files to the assistant during a run or treat improvement on
these familiar cases as evidence of general effectiveness. Each prompt defines
an exact JSON response contract; the grader checks every field and type with
exact decimal comparisons, without an LLM judge.

## Prepare a manual comparison

From the project root in Windows PowerShell:

```powershell
py -3 scripts\evaluation.py validate-kit
py -3 scripts\evaluation.py init-plan --output .local\evaluation-plan.json --host-surface "Copilot in Excel" --model unknown --tool-settings "Same approved tools in both conditions" --package-version unknown --package-sha256 unknown --repetitions 3 --seed 20261126
```

Replace `unknown` with an observed model label, tested package version and actual
suite ZIP SHA-256 when available. Package versions use `MAJOR.MINOR.PATCH` without
a `v` prefix; the tool never infers a version from the current repository because
the tested package may be older. Record unavailable settings explicitly as `unknown`. One plan
describes one host/model/tool setup; use separate plans for different setups.

The command creates 24 scheduled records: four unique cases, three repetitions,
two conditions. Every record starts `not-run`, with `executedAt` and response null. The
seed reproducibly shuffles case/repetition blocks by SHA-256 ordering and
counterbalances which condition goes first. Preserve the scheduled order and
run count. Three repetitions are a practical starting point, not a statistical
power calculation or 24 independent tasks.

1. Start a fresh conversation for every scheduled run. In **baseline**, disable
   this suite and any saved equivalent instructions; in **suite**, enable the
   recorded package. Keep the case prompt, inputs and tools identical. If a
   clean baseline cannot be established, record the limitation and do not make
   a causal claim about the skill's benefit.
2. Paste only the selected `prompts/` file. Do not expose `answers/`, previous
   answers or another condition's conversation. Do not let the assistant fetch
   this public repository during the case; record that restriction in the tool
   settings for both conditions.
3. Update that run's `status`, `executedAt`, `response` and `evidence` in the private plan.
   Record the actual completion or attempted-run time manually as a timezone-aware
   ISO timestamp, such as `2024-05-06T14:30:00+09:00`. Every attempted status,
   including `unavailable`, requires this timestamp; it dates the attempt and
   does not prove a model executed. `not-run` records must keep it null.
   For `completed`, copy the returned JSON object into `response` without
   correcting its values and record a private evidence locator. Preserve the
   original answer separately if it needs syntactic transcription; record any
   transcription in the evidence note. An answer that does not yield the
   requested JSON can remain null and is graded incorrect. Use `failed`,
   `refused`, `interrupted` or `unavailable` for those outcomes, leaving response
   null. An unavailable tool does not become a successful result.
4. Keep unfinished runs as `not-run`; never delete a scheduled row or add only
   successful retries. Predefine any later retry campaign in a separate plan.

```powershell
py -3 scripts\evaluation.py summarize .local\evaluation-plan.json --output .local\evaluation-summary.json
```

The tools make no model calls and never write an existing file. Keep plans and
evidence outside the public project or under ignored `.local/`. No native result
records are included in this repository.

## Read the summary

The summary retains the case-set/package versions, host description, attempt
timestamps, four unique cases, repetitions,
scheduled/attempted/completed/pass counts, all status counts, and per-case and
per-condition results. “Attempted” means any declared status except `not-run`;
it is an administrative count, not proof that a model executed. Paired outcomes
compare baseline and suite for the same case/repetition. A pair with either
condition incomplete stays `incomplete`; it is not scored as a tie or removed.

Missing scheduled rows, duplicate identities, changed order, fixture drift,
unknown statuses, missing or invalid attempted-run timestamps, nonfinite numbers
and malformed records fail validation.
A completed answer with wrong values, missing/extra keys, a wrong type or a
boolean used as a number is incorrect. Numeric strings are not numbers.

Checksums bind the chosen public files; they do not authenticate execution.
Manual records can be inaccurate or fabricated. The summary therefore makes no
native-execution attestation, confidence interval, pooled host score or claim
of statistical significance. Independently review the original outputs before
publishing any result, and keep private identifiers and company data out of it.
