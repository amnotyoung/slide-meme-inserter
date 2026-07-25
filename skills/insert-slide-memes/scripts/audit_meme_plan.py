#!/usr/bin/env python3
"""Audit the machine-readable selection plan for slide memes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


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
ALLOWED_DISCOVERY_ROUTES = {
    "imgflip-first",
    "regional-first",
    "fallback-other",
}
ALLOWED_IDENTITY_LEVELS = {"none", "low", "material"}
ALLOWED_RIGHTS_STATUSES = {
    "cleared",
    "exception-reviewed",
    "practical-reviewed",
    "unclear",
    "user-provided-unverified",
}
ALLOWED_RIGHTS_MODES = {"strict", "practical"}
ALLOWED_ATTRIBUTION_LOCATIONS = {
    "strict": {"on-slide", "credits-slide"},
    "practical": {"on-slide", "credits-slide", "speaker-notes"},
}
ALLOWED_DISTRIBUTIONS = {"internal", "external-limited", "public"}
ALLOWED_USE_MODES = {
    "live-internal",
    "internal-file-share",
    "live-client",
    "external-file-share",
    "paid-event",
    "public-pdf",
    "public-recording",
    "online-publication",
}
EXTERNAL_USE_MODES = {"live-client", "external-file-share", "paid-event"}
PUBLIC_USE_MODES = {"public-pdf", "public-recording", "online-publication"}
ALLOWED_LEGAL_BASES = {
    "license",
    "permission",
    "public-domain",
    "quotation-art-28",
    "fair-use-art-35-5",
    "school-education-art-25",
}
CLEARANCE_BASES = {"license", "permission", "public-domain"}
EXCEPTION_ANALYSIS_FIELDS = {
    "quotation-art-28": (
        "purpose",
        "main_subordinate",
        "necessary_amount",
        "fair_practice",
        "market_effect",
        "attribution",
    ),
    "fair-use-art-35-5": (
        "purpose_character",
        "work_nature",
        "amount_importance",
        "market_effect",
    ),
    "school-education-art-25": (
        "institution_basis",
        "class_purpose",
        "necessary_scope",
        "compensation_access",
    ),
}
ADDITIONAL_RIGHTS_FIELDS = {
    "moral_rights": {"not-modified", "permitted", "reviewed"},
    "portrait_publicity": {"not-applicable", "permission", "reviewed"},
    "trademark": {"not-applicable", "permission", "descriptive-use", "reviewed"},
}
PRACTICAL_REVIEW_FIELDS = (
    "transformative_context",
    "necessity",
    "amount_resolution",
    "market_substitution",
    "moral_personality_risk",
    "attribution_method",
    "checked_at",
)

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


def _is_imgflip_url(value: Any) -> bool:
    if not _is_nonempty_string(value):
        return False
    hostname = (urlparse(value).hostname or "").lower()
    return hostname in {"imgflip.com", "www.imgflip.com"}


def _audit_use_modes(
    record: dict[str, Any],
    label: str,
    errors: list[str],
) -> list[str]:
    use_modes = record.get("use_modes")
    if not isinstance(use_modes, list) or not use_modes:
        errors.append(f"{label}: use_modes must be a non-empty array.")
        return []
    if any(not _is_nonempty_string(value) for value in use_modes):
        errors.append(f"{label}: every use_modes value must be a non-empty string.")
        return []

    unknown = sorted(set(use_modes) - ALLOWED_USE_MODES)
    if unknown:
        errors.append(
            f"{label}: unsupported use_modes {unknown}; allowed values are "
            f"{sorted(ALLOWED_USE_MODES)}."
        )
    if len(set(use_modes)) != len(use_modes):
        errors.append(f"{label}: use_modes must not contain duplicates.")

    distribution = record.get("distribution")
    if distribution not in ALLOWED_DISTRIBUTIONS:
        errors.append(
            f"{label}: distribution must be one of {sorted(ALLOWED_DISTRIBUTIONS)}."
        )
    else:
        expected = "internal"
        if set(use_modes) & PUBLIC_USE_MODES:
            expected = "public"
        elif set(use_modes) & EXTERNAL_USE_MODES:
            expected = "external-limited"
        if distribution != expected:
            errors.append(
                f"{label}: distribution {distribution!r} does not match use_modes; "
                f"expected {expected!r}."
            )
    return use_modes


def _audit_additional_rights(
    record: dict[str, Any],
    label: str,
    errors: list[str],
) -> None:
    checks = record.get("additional_rights")
    if not isinstance(checks, dict):
        errors.append(f"{label}: additional_rights must be an object.")
        return

    for field, allowed_statuses in ADDITIONAL_RIGHTS_FIELDS.items():
        check = checks.get(field)
        if not isinstance(check, dict):
            errors.append(f"{label}: additional_rights.{field} must be an object.")
            continue
        status = check.get("status")
        if status not in allowed_statuses:
            errors.append(
                f"{label}: additional_rights.{field}.status must be one of "
                f"{sorted(allowed_statuses)}."
            )
        if not _is_nonempty_string(check.get("note")):
            errors.append(
                f"{label}: additional_rights.{field}.note must explain the check."
            )


def _audit_legal_basis(
    record: dict[str, Any],
    label: str,
    use_modes: list[str],
    errors: list[str],
) -> None:
    basis = record.get("legal_basis")
    if not isinstance(basis, dict):
        errors.append(f"{label}: selected placement requires a legal_basis object.")
        return

    basis_type = basis.get("type")
    if basis_type not in ALLOWED_LEGAL_BASES:
        errors.append(
            f"{label}: legal_basis.type must be one of {sorted(ALLOWED_LEGAL_BASES)}."
        )
        return

    _required_string(basis, "evidence", f"{label}.legal_basis", errors)
    _required_string(basis, "checked_at", f"{label}.legal_basis", errors)
    _required_string(basis, "jurisdiction", f"{label}.legal_basis", errors)

    rights_status = record.get("rights_status")
    expected_status = "cleared" if basis_type in CLEARANCE_BASES else "exception-reviewed"
    if rights_status != expected_status:
        errors.append(
            f"{label}: legal basis {basis_type} requires rights_status "
            f"{expected_status!r}, not {rights_status!r}."
        )

    if basis_type in {"license", "permission"}:
        _required_string(basis, "rights_holder", f"{label}.legal_basis", errors)
        scope = basis.get("scope")
        if not isinstance(scope, dict):
            errors.append(f"{label}: {basis_type} legal_basis requires a scope object.")
            return
        scoped_modes = scope.get("use_modes")
        if not isinstance(scoped_modes, list) or any(
            not _is_nonempty_string(value) for value in scoped_modes
        ):
            errors.append(
                f"{label}: legal_basis.scope.use_modes must be an array of strings."
            )
        else:
            unknown_scoped_modes = sorted(set(scoped_modes) - ALLOWED_USE_MODES)
            if unknown_scoped_modes:
                errors.append(
                    f"{label}: legal_basis.scope has unsupported use_modes "
                    f"{unknown_scoped_modes}."
                )
            uncovered = sorted(set(use_modes) - set(scoped_modes))
            if uncovered:
                errors.append(
                    f"{label}: legal_basis.scope does not cover use_modes {uncovered}."
                )
        for field in ("commercial_use", "modification"):
            if not isinstance(scope.get(field), bool):
                errors.append(
                    f"{label}: legal_basis.scope.{field} must be true or false."
                )
        if "paid-event" in use_modes and scope.get("commercial_use") is not True:
            errors.append(
                f"{label}: paid-event use requires commercial_use permission."
            )
        for field in ("territory", "expiration"):
            _required_string(scope, field, f"{label}.legal_basis.scope", errors)
    elif basis_type == "public-domain":
        _required_string(basis, "rationale", f"{label}.legal_basis", errors)
    else:
        analysis = basis.get("analysis")
        if not isinstance(analysis, dict):
            errors.append(
                f"{label}: {basis_type} legal_basis requires an analysis object."
            )
            return
        analyzed_modes = analysis.get("use_modes")
        if not isinstance(analyzed_modes, list) or any(
            not _is_nonempty_string(value) for value in analyzed_modes
        ):
            errors.append(
                f"{label}: legal_basis.analysis.use_modes must be an array of strings."
            )
        else:
            uncovered = sorted(set(use_modes) - set(analyzed_modes))
            if uncovered:
                errors.append(
                    f"{label}: statutory-exception analysis does not cover "
                    f"use_modes {uncovered}."
                )
        for field in EXCEPTION_ANALYSIS_FIELDS[basis_type]:
            _required_string(
                analysis,
                field,
                f"{label}.legal_basis.analysis",
                errors,
            )


def _audit_practical_scope(
    record: dict[str, Any],
    label: str,
    use_modes: list[str],
    errors: list[str],
) -> None:
    if set(use_modes) != {"live-internal"} or record.get("distribution") != "internal":
        errors.append(
            f"{label}: practical mode is limited to live-internal use with internal "
            "distribution; file sharing, clients, paid events, exports, recordings, "
            "and publication require strict mode."
        )


def _audit_practical_review(
    record: dict[str, Any],
    label: str,
    errors: list[str],
) -> None:
    review = record.get("practical_review")
    if not isinstance(review, dict):
        errors.append(
            f"{label}: rights_status 'practical-reviewed' requires a "
            "practical_review object."
        )
        return

    for field in PRACTICAL_REVIEW_FIELDS:
        _required_string(review, field, f"{label}.practical_review", errors)
    if (
        _is_nonempty_string(review.get("attribution_method"))
        and review["attribution_method"] != record.get("attribution_location")
    ):
        errors.append(
            f"{label}: practical_review.attribution_method must equal "
            "attribution_location."
        )
    if review.get("no_recording_or_distribution") is not True:
        errors.append(
            f"{label}: practical_review.no_recording_or_distribution must be true."
        )
    scores = record.get("scores")
    if isinstance(scores, dict) and scores.get("safety_rights") != 1:
        errors.append(
            f"{label}: practical-reviewed searched assets must score "
            "scores.safety_rights as 1, not as documented clearance."
        )


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
    if plan.get("plan_version") != 2:
        errors.append("Plan root: plan_version must be 2.")
    if not _is_nonempty_string(plan.get("audience")):
        errors.append("Plan root: audience must be a non-empty string.")
    rights_mode = plan.get("rights_mode")
    if rights_mode not in ALLOWED_RIGHTS_MODES:
        errors.append(
            f"Plan root: rights_mode must be one of {sorted(ALLOWED_RIGHTS_MODES)}."
        )

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
            "attribution_text",
            "attribution_url",
            "attribution_location",
            "layout",
            "risk",
        ):
            _required_string(record, field, label, errors)

        if (
            _is_nonempty_string(record.get("source"))
            and _is_nonempty_string(record.get("attribution_url"))
            and record["source"] != record["attribution_url"]
        ):
            errors.append(
                f"{label}: source must equal attribution_url so HTML exposes the "
                "actual attribution source, not a semantic or discovery page."
            )

        role = record.get("role")
        if role not in ALLOWED_ROLES:
            errors.append(f"{label}: invalid role {role!r}.")
        elif role == "callback" and not _is_nonempty_string(record.get("callback_to")):
            errors.append(f"{label}: callback requires an earlier callback_to slide ID.")

        origin = record.get("origin")
        if origin not in ALLOWED_ORIGINS:
            errors.append(f"{label}: invalid origin {origin!r}.")
            continue

        use_modes = _audit_use_modes(record, label, errors)
        if rights_mode == "practical":
            _audit_practical_scope(record, label, use_modes, errors)
        rights_status = record.get("rights_status")
        if rights_status not in ALLOWED_RIGHTS_STATUSES:
            errors.append(
                f"{label}: rights_status must be one of {sorted(ALLOWED_RIGHTS_STATUSES)}."
            )
        elif rights_status in {"unclear", "user-provided-unverified"}:
            errors.append(
                f"{label}: unresolved rights cannot be selected; keep the placement "
                "provisional, drop it, or complete the review required by rights_mode."
            )

        attribution_location = record.get("attribution_location")
        allowed_locations = ALLOWED_ATTRIBUTION_LOCATIONS.get(rights_mode, set())
        if attribution_location not in allowed_locations:
            errors.append(
                f"{label}: attribution_location must be one of "
                f"{sorted(allowed_locations)} in {rights_mode!r} mode."
            )

        if rights_mode == "practical" and rights_status == "practical-reviewed":
            _audit_practical_review(record, label, errors)
        elif rights_status in {"cleared", "exception-reviewed"}:
            _audit_legal_basis(record, label, use_modes, errors)
        elif rights_status == "practical-reviewed":
            errors.append(
                f"{label}: rights_status 'practical-reviewed' is allowed only in "
                "practical mode."
            )
        elif rights_mode == "strict":
            _audit_legal_basis(record, label, use_modes, errors)
        _audit_additional_rights(record, label, errors)
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
            discovery_route = record.get("discovery_route")
            if discovery_route not in ALLOWED_DISCOVERY_ROUTES:
                errors.append(
                    f"{label}: discovery_route must be one of "
                    f"{sorted(ALLOWED_DISCOVERY_ROUTES)}."
                )
            _required_string(record, "discovery_source", label, errors)
            _required_string(record, "humor_evidence", label, errors)
            if discovery_route == "imgflip-first":
                if not _is_imgflip_url(record.get("discovery_source")):
                    errors.append(
                        f"{label}: imgflip-first discovery_source must use imgflip.com."
                    )
            elif discovery_route in {"regional-first", "fallback-other"}:
                _required_string(
                    record,
                    "discovery_fallback_reason",
                    label,
                    errors,
                )
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
