#!/usr/bin/env python3
"""Audit the machine-readable selection plan for slide memes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {"provisional", "selected", "dropped"}
ALLOWED_ORIGINS = {"searched", "user-provided"}
ALLOWED_ROLES = {"reaction", "analogy", "callback", "transition"}
ALLOWED_SEARCHED_ASSET_KINDS = {
    "meme-template",
    "reaction-image",
    "phrase-format",
}
DISALLOWED_SEARCHED_ASSET_KINDS = {
    "fandom-art",
    "illustration",
    "press-image",
    "promotional-art",
    "stock-image",
    "wallpaper",
}
ALLOWED_RECOGNITION_BASES = {
    "audience-evidence",
    "broad-recognition",
    "user-approved",
}
ALLOWED_IDENTITY_LEVELS = {"none", "low", "material"}
ALLOWED_RIGHTS_STATUSES = {"cleared", "unclear", "user-provided-unverified"}
ALLOWED_DISTRIBUTIONS = {"internal", "public"}

HARD_GATES = (
    "established_format",
    "semantic_match",
    "audience_fit",
    "two_second_recognition",
    "caption_clarity",
    "presenter_safe",
    "asset_matches_template",
)
USER_PROVIDED_REQUIRED_GATES = (
    "semantic_match",
    "audience_fit",
    "caption_clarity",
    "presenter_safe",
    "asset_matches_template",
)
SCORE_FIELDS = (
    "narrative_value",
    "template_semantics",
    "audience_recognition",
    "novelty_fatigue",
    "caption_clarity",
    "layout_fit",
    "safety_rights",
)
CORE_SCORE_FIELDS = (
    "narrative_value",
    "template_semantics",
    "audience_recognition",
    "caption_clarity",
)


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _required_string(record: dict[str, Any], field: str, label: str, errors: list[str]) -> None:
    if not _is_nonempty_string(record.get(field)):
        errors.append(f"{label}: missing or empty {field}.")


def _audit_hard_gates(
    record: dict[str, Any],
    label: str,
    required: tuple[str, ...],
    errors: list[str],
) -> None:
    gates = record.get("hard_gates")
    if not isinstance(gates, dict):
        errors.append(f"{label}: hard_gates must be an object.")
        return

    for gate in HARD_GATES:
        if gate not in gates:
            errors.append(f"{label}: hard_gates is missing {gate}.")
        elif not isinstance(gates[gate], bool):
            errors.append(f"{label}: hard_gates.{gate} must be true or false.")

    for gate in required:
        if gates.get(gate) is not True:
            errors.append(f"{label}: selected candidate failed hard gate {gate}.")


def _audit_scores(record: dict[str, Any], label: str, errors: list[str]) -> None:
    scores = record.get("scores")
    if not isinstance(scores, dict):
        errors.append(f"{label}: scores must be an object with all seven dimensions.")
        return

    valid_scores: dict[str, int] = {}
    for field in SCORE_FIELDS:
        value = scores.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 2:
            errors.append(f"{label}: scores.{field} must be an integer from 0 to 2.")
        else:
            valid_scores[field] = value

    if len(valid_scores) != len(SCORE_FIELDS):
        return

    total = sum(valid_scores.values())
    declared_total = record.get("score_total")
    if declared_total != total:
        errors.append(
            f"{label}: score_total is {declared_total!r}; expected {total} from dimensions."
        )

    penalty = record.get("ubiquity_penalty")
    if not isinstance(penalty, int) or isinstance(penalty, bool) or penalty not in {0, 1}:
        errors.append(f"{label}: ubiquity_penalty must be 0 or 1.")
        return

    adjusted = total - penalty
    if record.get("adjusted_score") != adjusted:
        errors.append(
            f"{label}: adjusted_score is {record.get('adjusted_score')!r}; "
            f"expected {adjusted}."
        )
    if adjusted < 12:
        errors.append(f"{label}: adjusted score {adjusted}/14 is below 12/14.")

    for field in CORE_SCORE_FIELDS:
        if valid_scores[field] == 0:
            errors.append(f"{label}: core score {field} is 0; candidate must be dropped.")


def _audit_identity(record: dict[str, Any], label: str, errors: list[str]) -> None:
    identity = record.get("identity_signal")
    if not isinstance(identity, dict):
        errors.append(f"{label}: identity_signal must be an object.")
        return

    level = identity.get("level")
    if level not in ALLOWED_IDENTITY_LEVELS:
        errors.append(
            f"{label}: identity_signal.level must be one of "
            f"{sorted(ALLOWED_IDENTITY_LEVELS)}."
        )
        return

    if level == "material":
        if not _is_nonempty_string(identity.get("domain")):
            errors.append(f"{label}: material identity signal requires a domain.")
        if identity.get("user_approved") is not True:
            errors.append(
                f"{label}: material presenter-identity signal requires explicit user approval."
            )


def audit_plan_data(
    plan: Any,
) -> tuple[list[str], list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(plan, dict):
        return ["Plan root must be a JSON object."], warnings, []
    if plan.get("plan_version") != 1:
        errors.append("Plan root: plan_version must be 1.")
    if not _is_nonempty_string(plan.get("audience")):
        errors.append("Plan root: audience must be a non-empty string.")

    placements = plan.get("placements")
    if not isinstance(placements, list):
        return errors + ["Plan root: placements must be an array."], warnings, []

    seen_ids: set[str] = set()
    selected: list[dict[str, Any]] = []

    for index, record in enumerate(placements, 1):
        label = f"placement-{index}"
        if not isinstance(record, dict):
            errors.append(f"{label}: placement must be an object.")
            continue

        plan_id = record.get("id")
        if not _is_nonempty_string(plan_id):
            errors.append(f"{label}: missing or empty id.")
        else:
            label = plan_id
            if plan_id in seen_ids:
                errors.append(f"{label}: duplicate placement id.")
            seen_ids.add(plan_id)

        status = record.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{label}: invalid status {status!r}.")
            continue
        if status == "dropped":
            if not _is_nonempty_string(record.get("drop_reason")):
                warnings.append(f"{label}: dropped placement should record drop_reason.")
            continue
        if status == "provisional":
            continue

        selected.append(record)
        for field in (
            "slide_id",
            "communicative_job",
            "intended_response",
            "template",
            "caption",
            "source",
            "layout",
            "risk",
        ):
            _required_string(record, field, label, errors)

        role = record.get("role")
        if role not in ALLOWED_ROLES:
            errors.append(f"{label}: invalid role {role!r}.")
        elif role == "callback" and not _is_nonempty_string(record.get("callback_to")):
            errors.append(f"{label}: callback requires an earlier callback_to slide ID.")

        origin = record.get("origin")
        if origin not in ALLOWED_ORIGINS:
            errors.append(f"{label}: invalid origin {origin!r}.")
            continue

        distribution = record.get("distribution")
        if distribution not in ALLOWED_DISTRIBUTIONS:
            errors.append(f"{label}: distribution must be internal or public.")
        rights_status = record.get("rights_status")
        if rights_status not in ALLOWED_RIGHTS_STATUSES:
            errors.append(
                f"{label}: rights_status must be one of {sorted(ALLOWED_RIGHTS_STATUSES)}."
            )
        if distribution == "public" and rights_status != "cleared":
            errors.append(f"{label}: public distribution requires cleared rights.")

        _audit_identity(record, label, errors)

        if origin == "searched":
            asset_kind = record.get("asset_kind")
            if asset_kind in DISALLOWED_SEARCHED_ASSET_KINDS:
                errors.append(
                    f"{label}: searched {asset_kind} is not a meme asset; drop the candidate."
                )
            elif asset_kind not in ALLOWED_SEARCHED_ASSET_KINDS:
                errors.append(
                    f"{label}: asset_kind must be one of "
                    f"{sorted(ALLOWED_SEARCHED_ASSET_KINDS)} for a searched candidate."
                )

            recognition_basis = record.get("recognition_basis")
            if recognition_basis not in ALLOWED_RECOGNITION_BASES:
                errors.append(
                    f"{label}: recognition_basis must be one of "
                    f"{sorted(ALLOWED_RECOGNITION_BASES)}; unsupported assumptions fail."
                )
            _required_string(record, "recognition_evidence", label, errors)
            _required_string(record, "semantic_source", label, errors)
            _required_string(record, "original_source", label, errors)
            _required_string(record, "asset_source", label, errors)
            _audit_hard_gates(record, label, HARD_GATES, errors)
            _audit_scores(record, label, errors)
        else:
            user_locked = record.get("user_locked")
            if not isinstance(user_locked, dict) or user_locked.get("asset") is not True:
                errors.append(
                    f"{label}: selected user-provided placement must lock the exact asset."
                )
            _audit_hard_gates(
                record,
                label,
                USER_PROVIDED_REQUIRED_GATES,
                errors,
            )

    return errors, warnings, selected


def load_and_audit_plan(
    path: Path,
) -> tuple[dict[str, Any] | None, list[str], list[str], list[dict[str, Any]]]:
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"Plan file not found: {path}"], [], []
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [f"Could not read plan {path}: {exc}"], [], []

    errors, warnings, selected = audit_plan_data(plan)
    return plan if isinstance(plan, dict) else None, errors, warnings, selected


def main() -> int:
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument("plan", type=Path, help="Machine-readable meme plan JSON")
    arg_parser.add_argument(
        "--strict",
        action="store_true",
        help="Return a failure status for warnings as well as errors",
    )
    args = arg_parser.parse_args()

    plan, errors, warnings, selected = load_and_audit_plan(args.plan.resolve())
    placement_count = (
        len(plan.get("placements", []))
        if isinstance(plan, dict) and isinstance(plan.get("placements"), list)
        else 0
    )
    print(
        f"Placements: {placement_count} | Selected: {len(selected)} | "
        f"Errors: {len(errors)} | Warnings: {len(warnings)}"
    )
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")

    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
