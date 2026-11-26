# Evaluate skill behavior

**Status: proposed protocol; no matched native Copilot/Gemini efficacy study has been executed by this protocol.** Existing structural, calculation and synthetic task checks are recorded separately in [VALIDATION.md](VALIDATION.md). Counts of files, references, tests or public observations do not measure a model's accuracy or a skill's benefit.

This design adapts the matched skill/baseline approach in [Anthropic's skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) and the explicit acceptance criteria in [Microsoft's skills repository](https://github.com/microsoft/skills/blob/main/README.md). These are vendor-authored development practices, not evidence that this library improves a particular assistant.

## Runnable development kit

The [public evaluation kit](../evaluations/README.md) supplies five independently
invented cases: unmatched-key reconciliation, an ordered quantity/price/FX
bridge, ambiguous mappings, a post-cutoff revision with a missing internal
forecast, and early completion with an unsupported benchmark and a stale workbook
cache. Hashed prompts and answer keys are separate. Plans bind case set 1.1.0
and its manifest hash.
Because the answers are public, these cases support development and regressions;
they are not a hidden holdout or proof of general finance-task effectiveness.

`scripts/evaluation.py validate-kit` checks the fixtures. `init-plan` creates a
manual baseline/suite schedule for one declared host/model/tool setup with a
fixed repetition count and seeded, counterbalanced condition order. The tested
package version and SHA-256 are supplied explicitly or recorded as unknown;
neither is inferred from the repository. Every run starts `not-run`, with no
execution timestamp. Record the actual timezone-aware attempt/completion time
manually when changing its status. `summarize` grades completed JSON answers and retains all
scheduled denominators, failure statuses, individual cases and paired outcomes.
It rejects missing/duplicate scheduled records, fixture drift and invalid values.
See the kit guide for Windows commands and the exact recording procedure.

The release gate checks kit integrity and grader behavior only. No native runs,
model results or efficacy scores are shipped. A manually entered result is a
declaration, not an attestation of host execution; review its original evidence
before using it to support a public claim. Keep every actual run record private.

## Define the comparison before running it

Choose a focused task family, such as explaining an invented forecast variance or reconciling two invented extracts. Record the skill version and hash, task prompt, public or independently invented inputs, expected result and grading criteria before inspecting the model's answers. Include both routine cases and failures that a plausible answer could hide: missing populations, duplicate keys, wrong units, post-cutoff revisions or an unresolved difference.

Use a baseline with the same task and available tools but without the tested skill; when evaluating an update, compare the previous and proposed versions. Keep the host surface, visible model selection, settings, input artifacts and tool permissions equivalent. Record unknown settings as unknown. Use fresh conversations and separate evaluation data from examples used to revise the skill.

For each case, predefine the number of repeated runs per condition and vary their order. Three repeats can expose obvious variability but do not establish a stable success rate. Repeated runs of the same prompt are not independent task coverage. Preserve the task-family distinction when interpreting results, and avoid treating one assistant's outcome as evidence for another surface.

## Grade what matters

Define objective acceptance criteria that distinguish a correct result from a convincing failure. Examples include an exactly reconciled amount, an unresolved gap retained, protected formulas unchanged, correct source period and no unrequested worksheet. Use deterministic checks where possible; have an independent reviewer inspect explanatory quality and material omissions. Mask the condition label when practical. Keep judges' reasoning grounded in the returned artifact and expected contract.

Record failed, refused, truncated, interrupted and unavailable-tool runs separately. Do not silently discard them or score an unexecuted task as a pass. Retain a minimal non-sensitive result record: case ID, condition, repeat, visible host/model, date, acceptance results, evidence location and material error. Capture latency or token use only when actually exposed, with the measurement boundary stated.

## Report results and uncertainty

Report completed and attempted runs, task count, pass counts and denominators, failure types and paired differences by task family. Show repeated-run variability before any aggregate. If statistical intervals are justified, document their method and the independent sampling unit; do not use repeated outputs from a single case as separate independent tasks. For a small convenience sample, report descriptive counts and the cases tested without claiming broad performance or significance.

Explain the host, data, tool and sampling limitations. Report negative and unchanged outcomes alongside improvements. A better score on a development case is not validation on unseen cases. Store the exact release and public fixture versions needed to reproduce the comparison, without retaining credentials or private account identifiers.

## Publication boundary

Use independently invented inputs or public data with recorded rights. Never publish company files, private prompts, screenshots, mappings, names, thresholds or examples adapted from real work. Native tests in a work account stay within approved boundaries. Only independently reviewable, non-sensitive results may support a public performance claim; unavailable native access remains an explicit gap. This protocol adds no hosted runner, telemetry or automatic execution.
