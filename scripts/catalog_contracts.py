"""Validate workflow/tool routing and generate their readable catalogues offline."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import re

ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
MODES = {"inspect", "prepare", "validate", "execute", "verify"}
AVAILABILITY = {"user-reported", "partial-user-reported", "confirm-at-work", "optional-evaluation", "capability-only", "local-implementation"}
SUPPORT = {"instructions-and-export-checks", "local-code", "candidate-only"}


def string_list(value: object, label: str, *, empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not empty) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValueError(f"{label}: expected {'a' if empty else 'a nonempty'} string list")
    if len(value) != len(set(value)):
        raise ValueError(f"{label}: duplicate values")
    return value


def test_reference(root: Path, reference: str) -> None:
    path, separator, symbol = reference.partition("::")
    if not separator or not re.fullmatch(r"tests/[A-Za-z0-9_]+\.py", path):
        raise ValueError(f"Use an exact test path::Class.method reference: {reference}")
    source = root / path
    if source.is_symlink() or not source.is_file():
        raise ValueError(f"Missing test reference: {reference}")
    wanted = symbol.split(".")
    nodes = ast.parse(source.read_text(encoding="utf-8")).body
    for part in wanted:
        found = [node for node in nodes if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == part]
        if len(found) != 1:
            raise ValueError(f"Missing test symbol: {reference}")
        nodes = found[0].body
    if not wanted[-1].startswith("test_"):
        raise ValueError(f"Not a test symbol: {reference}")


def validate(root: Path, catalog: dict) -> dict:
    names = {row["name"] for row in catalog["skills"]}
    tool_path = root / "tools/catalog.json"
    if tool_path.is_symlink():
        raise ValueError("Linked tool catalogue refused")
    inventory = json.loads(tool_path.read_text(encoding="utf-8"))
    if inventory.get("schemaVersion") != 1 or not isinstance(inventory.get("tools"), list):
        raise ValueError("Unsupported tool catalogue")
    seen = set()
    for tool in inventory["tools"]:
        id = tool.get("id", "")
        if not ID.fullmatch(id) or id in seen:
            raise ValueError(f"Invalid or duplicate tool ID: {id}")
        seen.add(id)
        for key in ("name", "group", "financeUse"):
            if not isinstance(tool.get(key), str) or not tool[key].strip():
                raise ValueError(f"Tool {id}: missing {key}")
        if tool.get("priority") not in {"P0", "P1", "P2"} or tool.get("availability") not in AVAILABILITY or tool.get("repositorySupport") not in SUPPORT:
            raise ValueError(f"Tool {id}: invalid support/availability/priority")
        for key in ("actions", "requiredEvidence", "skillIds"):
            string_list(tool.get(key), f"Tool {id}.{key}")
        if set(tool["skillIds"]) - names:
            raise ValueError(f"Tool {id}: unknown workflow skill")
        string_list(tool.get("researchIds"), f"Tool {id}.researchIds", empty=True)
    for row in catalog["skills"]:
        name = row["name"]
        contract = row.get("contract")
        if not isinstance(contract, dict):
            raise ValueError(f"{name}: missing workflow contract")
        for key in ("triggers", "requiredInputs", "outputs", "modes", "optionalCapabilities"):
            string_list(contract.get(key), f"{name}.{key}")
        conditional = string_list(contract.get("conditionalModes"), f"{name}.conditionalModes", empty=True)
        if set(contract["modes"] + conditional) - MODES or set(contract["modes"]) & set(conditional):
            raise ValueError(f"{name}: invalid or overlapping execution modes")
        if contract.get("sharedProcedure") != "workflow-controls-v1":
            raise ValueError(f"{name}: unsupported shared procedure")
        coverage = contract.get("validation", {})
        if coverage.get("nativeStatus") != "not-validated":
            raise ValueError(f"{name}: native validation needs an approved environment record, absent from this public library")
        for key in ("packageTests", "workflowTests"):
            for test in string_list(coverage.get(key), f"{name}.{key}", empty=key == "workflowTests"):
                test_reference(root, test)
        string_list(row.get("researchIds"), f"{name}.researchIds")
    return inventory


def generate(root: Path, catalog: dict) -> dict[Path, bytes]:
    inventory = validate(root, catalog)
    lines = ["# Tool and capability inventory", "", f"Reviewed {inventory['reviewedOn']} · {len(inventory['tools'])} entries.", "",
             "One skill per finance workflow; tools supply the capabilities available in the approved session. "
             "This inventory does not install products, activate connections or certify native integrations.", "",
             "Start with Excel/Power Query, planning-report coordinates and SAP/BW export validation. "
             "Then verify Power BI/Fabric freshness and release visibility. Use approved work sources for authority and ownership.", "",
             "## Availability labels", ""]
    for name, explanation in inventory["availabilityNotes"].items():
        lines += [f"- **{name}:** {explanation}"]
    for group in dict.fromkeys(tool["group"] for tool in inventory["tools"]):
        lines += ["", f"## {group}", ""]
        for tool in (x for x in inventory["tools"] if x["group"] == group):
            lines += [f"### {tool['name']}", "", f"**{tool['priority']} · {tool['availability']} · {tool['repositorySupport']}**", "",
                      tool["financeUse"] + ".", "",
                      " ".join(action.rstrip(".") + "." for action in tool["actions"]), "",
                      "**Evidence required:** " + "; ".join(tool["requiredEvidence"]) + ".", "",
                      "**Workflow skills:** " + ", ".join(f"[{id}](skills/{id}/SKILL.md)" for id in tool["skillIds"]) + ".", ""]
            if tool["researchIds"]:
                lines += ["**Source registry:** " + ", ".join(f"`{id}`" for id in tool["researchIds"]) + ".", ""]
    lines += ["## Connection boundary", "",
              "Use an approved existing connection when available. This repository provides generic interfaces and export checks, "
              "not tenant endpoints, credentials, master data or live enterprise connectors. A cloud assistant cannot automatically "
              "reach the local public-benchmark API. Public deployment or a company connector requires its own reviewed integration.", "",
              "[Machine-readable inventory](tools/catalog.json) · [Source registry](research/README.md) · [Workflow contracts](docs/SKILL-CONTRACTS.md)", ""]
    contracts = ["# Workflow contracts and validation coverage", "", f"Generated from catalog.json for version {catalog['version']}.", "",
                 "These contracts describe triggers, inputs, outputs, modes and source support. Shared controls are included in every generated host skill. "
                 "Package tests do not prove that a live finance workflow is production-ready. Conditional execution requires the actual host, authorization, "
                 "exact target and payload, preconditions and independent verification. Native work-account validation remains outstanding.", "",
                 "Workflow-test links identify partial deterministic helper checks. Their presence does not establish that a model completed "
                 "the workflow or that every task step was tested; inspect the named test's exact scope. Optional dependencies may affect "
                 "whether a check runs, so use the release report's actual executed and skipped counts.", ""]
    for row in catalog["skills"]:
        contract = row["contract"]
        coverage = contract["validation"]
        contracts += [f"## {row['title']} (`{row['name']}`)", "",
                      "**Triggers:** " + "; ".join(contract["triggers"]) + ".", "",
                      "**Inputs:** " + "; ".join(contract["requiredInputs"]) + ".", "",
                      "**Outputs:** " + "; ".join(contract["outputs"]) + ".", "",
                      "**Modes:** " + ", ".join(contract["modes"]) + ". **Conditional:** " + (", ".join(contract["conditionalModes"]) or "none") + ".", "",
                      "**Dependencies:** shared `workflow-controls-v1`; optional " + ", ".join(contract["optionalCapabilities"]) + ".", "",
                      "**Package tests:** " + ", ".join(f"`{x}`" for x in coverage["packageTests"]) + ".", "",
                      "**Workflow tests:** " + (", ".join(f"`{x}`" for x in coverage["workflowTests"]) or "No automated end-to-end workflow coverage claimed") + ".", "",
                      "**Native status:** not validated in the approved work account. **Research IDs:** " + ", ".join(f"`{x}`" for x in row["researchIds"]) + ".", ""]
    return {Path("TOOLS.md"): ("\n".join(lines) + "\n").encode(), Path("docs/SKILL-CONTRACTS.md"): ("\n".join(contracts) + "\n").encode()}
