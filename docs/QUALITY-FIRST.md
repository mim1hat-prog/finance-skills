# Quality-first defaults
Reviewed 2026-11-27.

Complete the requested work with available authorized tools. Follow material evidence gaps, check consequential conclusions independently, correct failed checks and read back requested changes. Scale the final detail to the decision and the requested audience. Keep routine verification in working context. A host limit calls for verified partial results and a concrete continuation point, with source locations and pending checks.

Use enterprise evidence for company figures and statuses. Open the underlying records and align entity, metric, period, units and approval version. Use permitted public sources for external facts, standards and benchmarks. Keep work details out of public queries and keep unsupported internal figures unresolved. Report people as HC and approved full-time-equivalent capacity as PC.

## Host boundaries

| Host | What to verify | Provider documentation |
| --- | --- | --- |
| Excel | Read the authorized workbook and its affected formulas. Verify the saved target and distinguish stored caches from native recalculation. The OneDrive package supplies instructions for normal Excel capabilities. | [Copilot in Excel skills](https://support.microsoft.com/en-gb/excel/copilot/copilot-in-excel-skills) |
| PowerPoint | Inspect the actual slides when available and cross-check figures, legibility, titles and labels. Creating a draft and editing an existing deck are distinct actions. Use the approved template. | [Create a presentation with Copilot](https://support.microsoft.com/en-us/powerpoint/create-a-new-presentation-with-copilot-in-powerpoint) |
| Word | Inspect the actual document after authorized edits where supported. Verify scoped content, citations and required styles. | [Copilot in Word](https://support.microsoft.com/en-us/word/welcome-to-copilot-in-word) |
| Power BI | Verify model, filters, grain, measure and relevant results. Availability depends on admin, capacity, region and permissions. A proposed measure and an observed refresh have different evidence. | [Copilot in Power BI overview](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-introduction) |
| Copilot Chat | Check permitted work grounding and public web search in the current session. Open primary sources for external facts. Web search is subject to administrator and user controls. | [Microsoft web-search policy](https://learn.microsoft.com/en-us/copilot/microsoft-365/manage-public-web-access) |
| Gemini | Verify the accessible file, calculation and output. Use Search or the separately available Deep Research feature only with permitted sources. If the feature cannot run the imported skill, use a brief carrying the objective, permitted source scope and verification criteria. | [Deep Research](https://support.google.com/gemini/answer/15719111) · [Related sources](https://support.google.com/gemini/answer/14143489) |

Instructions can set evidence and completion criteria. Model selection, hidden reasoning tokens, timeout, context, tools, quota, connectors and permissions remain under host or administrator control. Repo validation cannot measure how long a managed model thinks or guarantee a complete answer. Use the actual artifact and observations to judge completion.

## Check early stopping in an approved work account

1. Open a fresh session for the affected host. Record the host, package version, enabled tools and visible mode privately. Confirm it can open the requested workflow reference. Use invented data and public material for any public report.
2. Run the [mixed-evidence regression case](../evaluations/prompts/early-stop-and-source-coverage.md) with and without the updated skill in separate sessions with the same model and source access. Compare the actual final responses with the [expected values](../evaluations/answers/early-stop-and-source-coverage.json). Record an interruption or skipped deliverable as incomplete even if the response includes a plausible answer.
3. For actual public source access, make a separate request to compare an invented internal onboarding note with Microsoft's current official web-search controls. Ask Copilot to open the provider page and explain what the administrator controls. If policy disables search, record the missing source and the verified internal portion. [Microsoft web-search controls](https://learn.microsoft.com/en-us/copilot/microsoft-365/manage-public-web-access)
4. When testing a deliverable, inspect the edited Excel range, PowerPoint slide, Word passage or Power BI measure in the host. Record the state actually observed. For a visible interruption, give the assistant its last verified result and the exact remaining check in the same approved work context. Add any public report through the [Copilot quality issue form](https://github.com/mim1hat-prog/finance-skills/issues/new?template=copilot-quality.yml).

Research on test-time compute concerns experiments that control how models search and verify answers. It supports choosing useful checks for difficult tasks. These instructions set task and verification criteria within the tools exposed by the host. [Snell et al., test-time compute](https://arxiv.org/abs/2408.03314)

## Review of the eight proposed repositories

Only original workflow guidance is included. The review used upstream project descriptions, the linked issues or author paper where available. No upstream code, datasets, weights, attack examples or model runtime was imported or executed.

| Project | Finding and disposition |
| --- | --- |
| [vLLM](https://github.com/vllm-project/vllm) | The [reasoning parser](https://docs.vllm.ai/en/latest/features/reasoning_outputs/) extracts model-specific output when configured by the operator. [Issue 44676](https://github.com/vllm-project/vllm/issues/44676) describes a tool-call compatibility problem with a reasoning-budget setting. Managed Copilot and Gemini skills have no access to these settings. A future local experiment would require an approved server, a pinned release, a supported model, verified tool calls and synthetic inputs. |
| [FreeToken](https://github.com/FlashML-org/FreeToken) | [Issue 929](https://github.com/FlashML-org/FreeToken/issues/929) proposes an answer reserve and reports a run that exhausted its generation budget. It is an open issue. Adopted a portable workflow response to interruption: preserve completed results, sources and pending checks. No server-side answer reservation is implied. |
| [COT_steering](https://github.com/Marker-Inc-Korea/COT_steering) | This experiment manipulates response tokens and the chat template during decoding. It requires model and inference access unavailable to these skills. No method or code imported. |
| [TokenSkip](https://github.com/hemingkx/TokenSkip) | [The authors](https://arxiv.org/abs/2502.12067) study controllable reasoning compression with trained models. There is no evidence it improves accuracy on these finance workflows. Preserve evidence and task state when continuation is needed. No compression model or training imported. |
| [Token_Budget_cot_VLM](https://github.com/amit154154/Token_Budget_cot_VLM) | A multimodal experiment using a LoRA-trained component and image encoder for token-budget prediction. It depends on model training and does not establish Office or Gemini Apps behavior. No dependency imported. |
| [Chain-of-Thought-Reasoning-Attacks](https://github.com/scthornton/Chain-of-Thought-Reasoning-Attacks) | Reviewed at the defensive design level. Retrieved material cannot choose the conclusion or authorize a tool action or disclosure. Consequential claims must be independently verified. No attack material imported. |
| [Awesome-LLM-Reasoning](https://github.com/atfortes/awesome-llm-reasoning) | A discovery index. Candidate methods require their own primary evidence, scope and rights review before adoption. |
| [Awesome-Collection-Token-Reduction](https://github.com/ZLKong/Awesome-Collection-Token-Reduction) | A discovery index and position-paper collection. Token savings and answer quality are distinct measurements. No pruning or context compression tooling imported. |

## Evidence for the workflow rules

[PAL](https://proceedings.mlr.press/v202/gao23f.html) supports using actual computation for suitable problems. [ALCE](https://aclanthology.org/2023.emnlp-main.398/) evaluates how citations support claims. [Chain-of-Verification](https://aclanthology.org/2024.findings-acl.212/) motivates checking specific factual questions separately. [Huang et al.](https://arxiv.org/abs/2310.01798) found limits to intrinsic self-correction without external feedback on their tested tasks. Apply these findings by recomputing values, opening underlying records, investigating conflicting evidence and revising material failures.

[SpreadsheetBench](https://arxiv.org/abs/2406.14991) motivates diverse workbook cases. [Tashman](https://doi.org/10.1016/S0169-2070(00)00065-0) informs rolling-origin forecast checks by horizon. [Heer and Bostock](https://idl.uw.edu/papers/crowdsourcing-graphical-perception) inform aligned position and common scales for magnitude comparisons. These are specific uses recorded in the [research registry](../research/README.md). No study here establishes a measured quality gain for this pack in a managed tenant.
