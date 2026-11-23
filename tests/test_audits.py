from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "insert-slide-memes" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from audit_meme_plan import audit_plan_data, load_and_audit_plan  # noqa: E402
from audit_memes import audit  # noqa: E402


def valid_plan() -> dict:
    return {
        "plan_version": 2,
        "audience": "Mixed internal training audience",
        "rights_mode": "strict",
        "placements": [
            {
                "id": "m01",
                "slide_id": "s08",
                "status": "selected",
                "origin": "searched",
                "role": "reaction",
                "callback_to": None,
                "communicative_job": "Release tension after inconsistent results",
                "intended_response": "Shared recognition",
                "template": "Licensed Reaction Template",
                "caption": "분명 저장했습니다. 어디에 저장했는지만 빼고.",
                "asset_kind": "meme-template",
                "recognition_basis": "broad-recognition",
                "recognition_evidence": "Documented recurring reaction-template use",
                "identity_signal": {
                    "level": "none",
                    "domain": None,
                    "user_approved": False,
                },
                "hard_gates": {
                    "established_format": True,
                    "semantic_match": True,
                    "audience_fit": True,
                    "two_second_recognition": True,
                    "caption_clarity": True,
                    "presenter_safe": True,
                    "asset_matches_template": True,
                },
                "scores": {
                    "narrative_value": 2,
                    "template_semantics": 2,
                    "audience_recognition": 2,
                    "novelty_fatigue": 1,
                    "caption_clarity": 2,
                    "layout_fit": 2,
                    "safety_rights": 2,
                },
                "score_total": 13,
                "ubiquity_penalty": 0,
                "adjusted_score": 13,
                "discovery_route": "imgflip-first",
                "discovery_source": "https://imgflip.com/meme/Two-Buttons",
                "discovery_fallback_reason": None,
                "humor_evidence": (
                    "Active variants use a compact dilemma structure suitable for "
                    "a slide-specific caption."
                ),
                "semantic_source": "https://example.com/licensed-template-meaning",
                "original_source": "https://example.com/original",
                "asset_source": "https://example.com/licensed-template.jpg",
                "attribution_text": "Example Creator — Licensed Template, CC BY 4.0",
                "attribution_url": "https://example.com/license",
                "attribution_location": "on-slide",
                "source": "https://example.com/license",
                "rights_status": "cleared",
                "distribution": "internal",
                "use_modes": ["live-internal"],
                "legal_basis": {
                    "type": "license",
                    "jurisdiction": "KR",
                    "evidence": "https://example.com/license",
                    "checked_at": "2026-07-25",
                    "rights_holder": "Example Creator",
                    "scope": {
                        "use_modes": ["live-internal"],
                        "commercial_use": False,
                        "modification": True,
                        "territory": "worldwide",
                        "expiration": "none",
                    },
                },
                "additional_rights": {
                    "moral_rights": {
                        "status": "not-modified",
                        "note": "The raster is not altered.",
                    },
                    "portrait_publicity": {
                        "status": "not-applicable",
                        "note": "No identifiable natural person appears.",
                    },
                    "trademark": {
                        "status": "not-applicable",
                        "note": "No third-party mark appears.",
                    },
                },
                "layout": "Sidecar",
                "risk": "Low",
            }
        ],
    }


def common_use_plan() -> dict:
    plan = valid_plan()
    plan["rights_mode"] = "common-use"
    placement = plan["placements"][0]
    placement["template"] = "Two Buttons"
    placement["rights_status"] = "common-use-unverified"
    placement["attribution_text"] = "Two Buttons — Imgflip template page"
    placement["attribution_url"] = placement["discovery_source"]
    placement["source"] = placement["attribution_url"]
    placement["risk"] = "License unverified; no concrete issue identified."
    for field in ("original_source", "legal_basis", "additional_rights"):
        placement.pop(field)
    return plan


class MemePlanAuditTests(unittest.TestCase):
    def test_common_use_allows_every_delivery_mode_without_clearance(self) -> None:
        uses = {
            "live-internal": "internal",
            "internal-file-share": "internal",
            "live-client": "external-limited",
            "external-file-share": "external-limited",
            "paid-event": "external-limited",
            "public-pdf": "public",
            "public-recording": "public",
            "online-publication": "public",
        }
        for use_mode, distribution in uses.items():
            with self.subTest(use_mode=use_mode):
                plan = common_use_plan()
                placement = plan["placements"][0]
                placement["use_modes"] = [use_mode]
                placement["distribution"] = distribution
                errors, warnings, selected = audit_plan_data(plan)
                self.assertEqual(errors, [])
                self.assertEqual(warnings, [])
                self.assertEqual(len(selected), 1)

    def test_omitted_mode_and_unknown_delivery_default_to_common_use(self) -> None:
        plan = common_use_plan()
        plan.pop("rights_mode")
        placement = plan["placements"][0]
        placement.pop("use_modes")
        placement.pop("distribution")
        placement["original_source"] = None
        errors, warnings, selected = audit_plan_data(plan)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(len(selected), 1)
        # The audit must not silently rewrite the caller's plan or rights status.
        self.assertNotIn("rights_mode", plan)
        self.assertEqual(selected[0]["rights_status"], "common-use-unverified")

    def test_common_use_allows_supplied_circulating_meme(self) -> None:
        plan = common_use_plan()
        placement = plan["placements"][0]
        placement["origin"] = "user-provided"
        placement["user_locked"] = {"asset": True}
        for field in ("discovery_route", "discovery_source", "semantic_source", "scores"):
            placement.pop(field)
        errors, warnings, selected = audit_plan_data(plan)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(len(selected), 1)

    def test_common_use_does_not_turn_supplied_art_into_a_meme(self) -> None:
        for field, value in (
            ("established_format", False),
            ("asset_kind", "wallpaper"),
            ("recognition_evidence", ""),
        ):
            with self.subTest(field=field):
                plan = common_use_plan()
                placement = plan["placements"][0]
                placement["origin"] = "user-provided"
                placement["user_locked"] = {"asset": True}
                if field == "established_format":
                    placement["hard_gates"][field] = value
                else:
                    placement[field] = value
                errors, _, _ = audit_plan_data(plan)
                self.assertTrue(errors)

    def test_common_use_does_not_ignore_a_failed_safety_gate(self) -> None:
        plan = common_use_plan()
        plan["placements"][0]["hard_gates"]["presenter_safe"] = False
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(any("hard gate presenter_safe" in error for error in errors))

    def test_common_use_validates_known_delivery_scope(self) -> None:
        for distribution in (None, "internal"):
            with self.subTest(distribution=distribution):
                plan = common_use_plan()
                placement = plan["placements"][0]
                placement["use_modes"] = ["public-pdf"]
                if distribution is None:
                    placement.pop("distribution")
                errors, _, _ = audit_plan_data(plan)
                self.assertTrue(any("distribution" in error for error in errors))

    def test_common_use_status_cannot_bypass_an_explicit_review_mode(self) -> None:
        for rights_mode in ("strict", "practical"):
            with self.subTest(rights_mode=rights_mode):
                plan = common_use_plan()
                plan["rights_mode"] = rights_mode
                errors, _, _ = audit_plan_data(plan)
                self.assertTrue(any("allowed only in common-use mode" in e for e in errors))

    def test_common_use_does_not_allow_an_unsupported_clearance_claim(self) -> None:
        for status in ("cleared", "exception-reviewed"):
            with self.subTest(status=status):
                plan = common_use_plan()
                plan["placements"][0]["rights_status"] = status
                errors, _, _ = audit_plan_data(plan)
                self.assertTrue(any("requires a legal_basis object" in e for e in errors))

    def test_valid_searched_plan_passes(self) -> None:
        errors, warnings, selected = audit_plan_data(valid_plan())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual([record["id"] for record in selected], ["m01"])

    def test_zero_memes_is_valid(self) -> None:
        errors, warnings, selected = audit_plan_data(
            {
                "plan_version": 2,
                "audience": "Executive briefing",
                "rights_mode": "strict",
                "placements": [],
            }
        )
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(selected, [])

    def test_searched_plan_requires_discovery_and_humor_evidence(self) -> None:
        plan = valid_plan()
        placement = plan["placements"][0]
        placement.pop("discovery_route")
        placement.pop("discovery_source")
        placement.pop("humor_evidence")
        errors, _, _ = audit_plan_data(plan)
        joined = "\n".join(errors)
        self.assertIn("discovery_route", joined)
        self.assertIn("discovery_source", joined)
        self.assertIn("humor_evidence", joined)

    def test_imgflip_first_route_requires_imgflip_page(self) -> None:
        plan = valid_plan()
        plan["placements"][0]["discovery_source"] = (
            "https://knowyourmeme.com/memes/daily-struggle-two-buttons"
        )
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(
            any(
                "imgflip-first discovery_source must use imgflip.com" in error
                for error in errors
            )
        )

    def test_regional_first_route_requires_fallback_reason(self) -> None:
        plan = valid_plan()
        placement = plan["placements"][0]
        placement["discovery_route"] = "regional-first"
        placement["discovery_source"] = "https://example.kr/meme"
        placement["discovery_fallback_reason"] = None
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(any("discovery_fallback_reason" in error for error in errors))

    def test_regional_first_route_with_reason_passes(self) -> None:
        plan = valid_plan()
        placement = plan["placements"][0]
        placement["discovery_route"] = "regional-first"
        placement["discovery_source"] = "https://example.kr/meme"
        placement["discovery_fallback_reason"] = (
            "This Korean phrase format is not meaningfully represented on Imgflip."
        )
        errors, warnings, selected = audit_plan_data(plan)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual([record["id"] for record in selected], ["m01"])

    def test_callback_requires_earlier_setup(self) -> None:
        plan = valid_plan()
        plan["placements"][0]["role"] = "callback"
        plan["placements"][0]["callback_to"] = None
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(any("callback_to" in error for error in errors))

    def test_failed_hard_gate_cannot_be_compensated_by_score(self) -> None:
        plan = valid_plan()
        plan["placements"][0]["hard_gates"]["semantic_match"] = False
        plan["placements"][0]["scores"]["novelty_fatigue"] = 2
        plan["placements"][0]["score_total"] = 14
        plan["placements"][0]["adjusted_score"] = 14
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(any("hard gate semantic_match" in error for error in errors))

    def test_user_provided_unverified_asset_stays_provisional(self) -> None:
        plan = valid_plan()
        placement = plan["placements"][0]
        placement["status"] = "provisional"
        placement["origin"] = "user-provided"
        placement["template"] = "User-provided exact asset"
        placement["source"] = "pending"
        placement["rights_status"] = "user-provided-unverified"
        placement["user_locked"] = {"asset": True, "placement": True, "caption": False}
        placement["hard_gates"]["established_format"] = False
        for field in (
            "asset_kind",
            "recognition_basis",
            "recognition_evidence",
            "discovery_route",
            "discovery_source",
            "discovery_fallback_reason",
            "humor_evidence",
            "semantic_source",
            "original_source",
            "asset_source",
            "scores",
            "score_total",
            "ubiquity_penalty",
            "adjusted_score",
        ):
            placement.pop(field, None)

        errors, warnings, selected = audit_plan_data(plan)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(selected, [])

    def test_user_provided_unverified_asset_cannot_be_selected(self) -> None:
        plan = valid_plan()
        placement = plan["placements"][0]
        placement["origin"] = "user-provided"
        placement["template"] = "User-provided exact asset"
        placement["rights_status"] = "user-provided-unverified"
        placement["user_locked"] = {"asset": True}
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(
            any("unresolved rights cannot be selected" in error for error in errors)
        )

    def test_practical_mode_allows_reviewed_user_provided_asset(self) -> None:
        plan = valid_plan()
        plan["rights_mode"] = "practical"
        placement = plan["placements"][0]
        placement["origin"] = "user-provided"
        placement["template"] = "User-provided exact asset"
        placement["rights_status"] = "practical-reviewed"
        placement["attribution_location"] = "speaker-notes"
        placement["user_locked"] = {"asset": True}
        placement.pop("legal_basis")
        for field in (
            "asset_kind",
            "recognition_basis",
            "recognition_evidence",
            "discovery_route",
            "discovery_source",
            "discovery_fallback_reason",
            "humor_evidence",
            "semantic_source",
            "original_source",
            "asset_source",
            "scores",
            "score_total",
            "ubiquity_penalty",
            "adjusted_score",
        ):
            placement.pop(field, None)
        placement["practical_review"] = {
            "transformative_context": "Contextual reaction to the team's workflow.",
            "necessity": "One supplied image at one discussion beat.",
            "amount_resolution": "Low resolution and no raster edits.",
            "market_substitution": "No substitute for the source work.",
            "moral_personality_risk": "No degrading or endorsement context.",
            "attribution_method": "speaker-notes",
            "checked_at": "2026-07-25",
            "no_recording_or_distribution": True,
        }

        errors, warnings, selected = audit_plan_data(plan)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual([record["id"] for record in selected], ["m01"])

    def test_internal_searched_asset_with_unclear_rights_is_rejected(self) -> None:
        plan = valid_plan()
        placement = plan["placements"][0]
        placement["rights_status"] = "unclear"
        placement.pop("legal_basis")
        errors, _, _ = audit_plan_data(plan)
        joined = "\n".join(errors)
        self.assertIn("unresolved rights cannot be selected", joined)
        self.assertIn("requires a legal_basis object", joined)

    def test_practical_mode_allows_reviewed_live_internal_use(self) -> None:
        plan = valid_plan()
        plan["rights_mode"] = "practical"
        placement = plan["placements"][0]
        placement["rights_status"] = "practical-reviewed"
        placement["attribution_location"] = "speaker-notes"
        placement.pop("legal_basis")
        placement["scores"]["safety_rights"] = 1
        placement["score_total"] = 12
        placement["adjusted_score"] = 12
        placement["practical_review"] = {
            "transformative_context": (
                "The image comments on the team's own workflow failure."
            ),
            "necessity": "One reaction image supports the specific discussion beat.",
            "amount_resolution": "A low-resolution copy is shown once without cropping.",
            "market_substitution": "The slide is not a substitute for the source work.",
            "moral_personality_risk": (
                "No degrading alteration, endorsement implication, or sensitive person."
            ),
            "attribution_method": "speaker-notes",
            "checked_at": "2026-07-25",
            "no_recording_or_distribution": True,
        }

        errors, warnings, selected = audit_plan_data(plan)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual([record["id"] for record in selected], ["m01"])

    def test_practical_mode_rejects_file_sharing(self) -> None:
        plan = valid_plan()
        plan["rights_mode"] = "practical"
        placement = plan["placements"][0]
        placement["rights_status"] = "practical-reviewed"
        placement["use_modes"] = ["internal-file-share"]
        placement.pop("legal_basis")
        placement["scores"]["safety_rights"] = 1
        placement["score_total"] = 12
        placement["adjusted_score"] = 12
        placement["practical_review"] = {
            "transformative_context": "Contextual reaction.",
            "necessity": "One image.",
            "amount_resolution": "Low resolution.",
            "market_substitution": "No substitute.",
            "moral_personality_risk": "Reviewed.",
            "attribution_method": "on-slide",
            "checked_at": "2026-07-25",
            "no_recording_or_distribution": True,
        }

        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(any("file sharing" in error for error in errors))

    def test_practical_mode_rejects_broader_use_even_when_licensed(self) -> None:
        plan = valid_plan()
        plan["rights_mode"] = "practical"
        placement = plan["placements"][0]
        placement["distribution"] = "external-limited"
        placement["use_modes"] = ["live-client"]
        placement["legal_basis"]["scope"]["use_modes"] = ["live-client"]

        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(any("need common-use or strict mode" in error for error in errors))

    def test_strict_external_file_share_is_external_limited(self) -> None:
        plan = valid_plan()
        placement = plan["placements"][0]
        placement["distribution"] = "external-limited"
        placement["use_modes"] = ["external-file-share"]
        placement["legal_basis"]["scope"]["use_modes"] = ["external-file-share"]

        errors, warnings, selected = audit_plan_data(plan)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual([record["id"] for record in selected], ["m01"])

    def test_practical_review_requires_no_distribution_confirmation(self) -> None:
        plan = valid_plan()
        plan["rights_mode"] = "practical"
        placement = plan["placements"][0]
        placement["rights_status"] = "practical-reviewed"
        placement.pop("legal_basis")
        placement["scores"]["safety_rights"] = 1
        placement["score_total"] = 12
        placement["adjusted_score"] = 12
        placement["practical_review"] = {
            "transformative_context": "Contextual reaction.",
            "necessity": "One image.",
            "amount_resolution": "Low resolution.",
            "market_substitution": "No substitute.",
            "moral_personality_risk": "Reviewed.",
            "attribution_method": "on-slide",
            "checked_at": "2026-07-25",
            "no_recording_or_distribution": False,
        }

        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(
            any("no_recording_or_distribution must be true" in error for error in errors)
        )

    def test_strict_mode_rejects_practical_review_status(self) -> None:
        plan = valid_plan()
        placement = plan["placements"][0]
        placement["rights_status"] = "practical-reviewed"
        placement.pop("legal_basis")
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(
            any("allowed only in practical mode" in error for error in errors)
        )

    def test_new_public_use_requires_matching_license_scope(self) -> None:
        plan = valid_plan()
        placement = plan["placements"][0]
        placement["distribution"] = "public"
        placement["use_modes"] = ["live-internal", "public-pdf"]
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(
            any("scope does not cover use_modes ['public-pdf']" in error for error in errors)
        )

    def test_paid_event_requires_commercial_permission(self) -> None:
        plan = valid_plan()
        placement = plan["placements"][0]
        placement["distribution"] = "external-limited"
        placement["use_modes"] = ["paid-event"]
        placement["legal_basis"]["scope"]["use_modes"] = ["paid-event"]
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(
            any("paid-event use requires commercial_use permission" in error for error in errors)
        )

    def test_reviewed_fair_use_basis_passes(self) -> None:
        plan = valid_plan()
        placement = plan["placements"][0]
        placement["rights_status"] = "exception-reviewed"
        placement["legal_basis"] = {
            "type": "fair-use-art-35-5",
            "jurisdiction": "KR",
            "evidence": "Documented four-factor review in the plan",
            "checked_at": "2026-07-25",
            "analysis": {
                "use_modes": ["live-internal"],
                "purpose_character": "The slide critiques the meme itself.",
                "work_nature": "The source was previously published.",
                "amount_importance": "Only the portion necessary for criticism is used.",
                "market_effect": "The low-resolution excerpt does not replace demand.",
            },
        }
        errors, warnings, selected = audit_plan_data(plan)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual([record["id"] for record in selected], ["m01"])

    def test_drx_wallpaper_regression_is_rejected(self) -> None:
        fixture = ROOT / "tests" / "fixtures" / "drx-wallpaper-selected.json"
        _, errors, _, _ = load_and_audit_plan(fixture)
        joined = "\n".join(errors)
        self.assertIn("callback_to", joined)
        self.assertIn("presenter-identity signal", joined)
        self.assertIn("searched wallpaper is not a meme asset", joined)
        self.assertIn("unsupported assumptions fail", joined)

    def test_safety_rights_or_layout_fit_zero_is_rejected(self) -> None:
        for field in ("safety_rights", "layout_fit"):
            with self.subTest(field=field):
                plan = common_use_plan()
                placement = plan["placements"][0]
                for key in placement["scores"]:
                    placement["scores"][key] = 2
                placement["scores"][field] = 0
                placement["score_total"] = 12
                placement["adjusted_score"] = 12
                errors, _, _ = audit_plan_data(plan)
                self.assertTrue(
                    any(f"core score {field} is 0" in error for error in errors)
                )

    def test_duplicate_selected_slide_id_is_rejected(self) -> None:
        plan = common_use_plan()
        second = json.loads(json.dumps(plan["placements"][0]))
        second["id"] = "m02"
        plan["placements"].append(second)
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(
            any("already has selected placement" in error for error in errors)
        )

    def test_callback_to_same_slide_is_rejected(self) -> None:
        plan = common_use_plan()
        placement = plan["placements"][0]
        placement["role"] = "callback"
        placement["callback_to"] = placement["slide_id"]
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(
            any("must reference an earlier slide" in error for error in errors)
        )

    def test_non_http_attribution_and_source_urls_are_rejected(self) -> None:
        for bad_url in ("internet", "javascript:alert(1)", "user-provided"):
            with self.subTest(bad_url=bad_url):
                plan = common_use_plan()
                placement = plan["placements"][0]
                placement["attribution_url"] = bad_url
                placement["source"] = bad_url
                errors, _, _ = audit_plan_data(plan)
                self.assertTrue(
                    any("must be a valid http(s) URL" in error for error in errors)
                )

    def test_user_provided_template_only_runs_searched_asset_checks(self) -> None:
        plan = common_use_plan()
        placement = plan["placements"][0]
        placement["origin"] = "user-provided"
        placement["user_locked"] = {"template": True, "asset": False}
        errors, warnings, selected = audit_plan_data(plan)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual([record["id"] for record in selected], ["m01"])

        placement.pop("discovery_source")
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(any("discovery_source" in error for error in errors))

    def test_derived_score_and_redundant_source_fields_can_be_omitted(self) -> None:
        plan = common_use_plan()
        placement = plan["placements"][0]
        for field in ("source", "score_total", "adjusted_score", "ubiquity_penalty"):
            placement.pop(field, None)
        errors, warnings, selected = audit_plan_data(plan)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual([record["id"] for record in selected], ["m01"])

    def test_practical_user_provided_with_scores_does_not_false_positive(self) -> None:
        plan = valid_plan()
        plan["rights_mode"] = "practical"
        placement = plan["placements"][0]
        placement["origin"] = "user-provided"
        placement["rights_status"] = "practical-reviewed"
        placement["attribution_location"] = "speaker-notes"
        placement["user_locked"] = {"asset": True}
        placement.pop("legal_basis")
        placement["practical_review"] = {
            "transformative_context": "Contextual reaction.",
            "necessity": "One image.",
            "amount_resolution": "Low resolution.",
            "market_substitution": "No substitute.",
            "moral_personality_risk": "Reviewed.",
            "attribution_method": "speaker-notes",
            "checked_at": "2026-07-25",
            "no_recording_or_distribution": True,
        }
        errors, warnings, _ = audit_plan_data(plan)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])


class HtmlPlanCrossCheckTests(unittest.TestCase):
    def test_common_use_public_deck_with_notes_passes_without_clearance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            plan = common_use_plan()
            plan.pop("rights_mode")
            placement = plan["placements"][0]
            placement["attribution_location"] = "speaker-notes"
            placement["use_modes"] = ["live-client", "online-publication"]
            placement["distribution"] = "public"
            plan_path = directory / "meme-plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            (directory / "meme.jpg").write_bytes(b"test-image")
            html_path = directory / "deck.html"
            html_path.write_text(
                f"""
                <section id="s08">
                  <figure class="slide-meme" data-meme-plan-id="m01"
                    data-meme-role="reaction" data-meme-template="Two Buttons"
                    data-meme-source="{placement['source']}" data-meme-origin="searched">
                    <img src="meme.jpg" alt="A person hesitates between two buttons" />
                    <figcaption>{placement['caption']}</figcaption>
                  </figure>
                  <aside class="speaker-notes">
                    <a class="meme-attribution" data-meme-plan-id="m01"
                      data-meme-attribution-location="speaker-notes"
                      href="{placement['attribution_url']}">{placement['attribution_text']}</a>
                  </aside>
                </section>
                """,
                encoding="utf-8",
            )
            errors, warnings, _ = audit(html_path, 0.20, plan_path)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_html_matches_selected_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            plan_path = tmp_path / "meme-plan.json"
            html_path = tmp_path / "deck.html"
            image_path = tmp_path / "meme.jpg"
            plan_path.write_text(json.dumps(valid_plan()), encoding="utf-8")
            image_path.write_bytes(b"test-image")
            html_path.write_text(
                """
                <section id="s08">
                  <figure
                    class="slide-meme"
                    data-meme-plan-id="m01"
                    data-meme-role="reaction"
                    data-meme-template="Licensed Reaction Template"
                    data-meme-source="https://example.com/license"
                    data-meme-origin="searched"
                  >
                    <img src="meme.jpg" alt="A confused person looks around" />
                    <figcaption>분명 저장했습니다. 어디에 저장했는지만 빼고.</figcaption>
                    <a class="meme-attribution" href="https://example.com/license">
                      Example Creator — Licensed Template, CC BY 4.0
                    </a>
                  </figure>
                </section>
                """,
                encoding="utf-8",
            )

            errors, warnings, _ = audit(html_path, 0.20, plan_path)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_visible_attribution_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            plan_path = tmp_path / "meme-plan.json"
            html_path = tmp_path / "deck.html"
            image_path = tmp_path / "meme.jpg"
            plan_path.write_text(json.dumps(valid_plan()), encoding="utf-8")
            image_path.write_bytes(b"test-image")
            html_path.write_text(
                """
                <section id="s08">
                  <figure
                    class="slide-meme"
                    data-meme-plan-id="m01"
                    data-meme-role="reaction"
                    data-meme-template="Licensed Reaction Template"
                    data-meme-source="https://example.com/license"
                    data-meme-origin="searched"
                  >
                    <img src="meme.jpg" alt="A confused person looks around" />
                    <figcaption>분명 저장했습니다. 어디에 저장했는지만 빼고.</figcaption>
                  </figure>
                </section>
                """,
                encoding="utf-8",
            )

            errors, _, _ = audit(html_path, 0.20, plan_path)
            self.assertTrue(
                any("missing .meme-attribution" in error for error in errors)
            )

    def test_visible_attribution_must_match_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            plan_path = tmp_path / "meme-plan.json"
            html_path = tmp_path / "deck.html"
            image_path = tmp_path / "meme.jpg"
            plan_path.write_text(json.dumps(valid_plan()), encoding="utf-8")
            image_path.write_bytes(b"test-image")
            html_path.write_text(
                """
                <section id="s08">
                  <figure
                    class="slide-meme"
                    data-meme-plan-id="m01"
                    data-meme-role="reaction"
                    data-meme-template="Licensed Reaction Template"
                    data-meme-source="https://example.com/license"
                    data-meme-origin="searched"
                  >
                    <img src="meme.jpg" alt="A confused person looks around" />
                    <figcaption>분명 저장했습니다. 어디에 저장했는지만 빼고.</figcaption>
                    <a class="meme-attribution" href="https://example.com/license">
                      Wrong attribution
                    </a>
                  </figure>
                </section>
                """,
                encoding="utf-8",
            )

            errors, _, _ = audit(html_path, 0.20, plan_path)
            self.assertTrue(
                any("attribution text" in error for error in errors)
            )

    def test_practical_speaker_notes_attribution_matches_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            plan = valid_plan()
            plan["rights_mode"] = "practical"
            placement = plan["placements"][0]
            placement["rights_status"] = "practical-reviewed"
            placement["attribution_location"] = "speaker-notes"
            placement.pop("legal_basis")
            placement["scores"]["safety_rights"] = 1
            placement["score_total"] = 12
            placement["adjusted_score"] = 12
            placement["practical_review"] = {
                "transformative_context": "Contextual reaction.",
                "necessity": "One image.",
                "amount_resolution": "Low resolution.",
                "market_substitution": "No substitute.",
                "moral_personality_risk": "Reviewed.",
                "attribution_method": "speaker-notes",
                "checked_at": "2026-07-25",
                "no_recording_or_distribution": True,
            }
            plan_path = tmp_path / "meme-plan.json"
            html_path = tmp_path / "deck.html"
            image_path = tmp_path / "meme.jpg"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            image_path.write_bytes(b"test-image")
            html_path.write_text(
                """
                <section id="s08">
                  <figure
                    class="slide-meme"
                    data-meme-plan-id="m01"
                    data-meme-role="reaction"
                    data-meme-template="Licensed Reaction Template"
                    data-meme-source="https://example.com/license"
                    data-meme-origin="searched"
                  >
                    <img src="meme.jpg" alt="A confused person looks around" />
                    <figcaption>분명 저장했습니다. 어디에 저장했는지만 빼고.</figcaption>
                  </figure>
                  <aside class="speaker-notes">
                    <a
                      class="meme-attribution"
                      data-meme-plan-id="m01"
                      data-meme-attribution-location="speaker-notes"
                      href="https://example.com/license"
                    >Example Creator — Licensed Template, CC BY 4.0</a>
                  </aside>
                </section>
                """,
                encoding="utf-8",
            )

            errors, warnings, _ = audit(html_path, 0.20, plan_path)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

            html_path.write_text(
                html_path.read_text(encoding="utf-8").replace(
                    'class="speaker-notes"',
                    'class="footnote"',
                ),
                encoding="utf-8",
            )
            errors, _, _ = audit(html_path, 0.20, plan_path)
            self.assertTrue(
                any(
                    "must be inside an element with class speaker-notes" in error
                    for error in errors
                )
            )

    def test_strict_credits_slide_attribution_matches_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            plan = valid_plan()
            plan["placements"][0]["attribution_location"] = "credits-slide"
            plan_path = tmp_path / "meme-plan.json"
            html_path = tmp_path / "deck.html"
            image_path = tmp_path / "meme.jpg"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            image_path.write_bytes(b"test-image")
            html_path.write_text(
                """
                <section id="s08">
                  <figure
                    class="slide-meme"
                    data-meme-plan-id="m01"
                    data-meme-role="reaction"
                    data-meme-template="Licensed Reaction Template"
                    data-meme-source="https://example.com/license"
                    data-meme-origin="searched"
                  >
                    <img src="meme.jpg" alt="A confused person looks around" />
                    <figcaption>분명 저장했습니다. 어디에 저장했는지만 빼고.</figcaption>
                  </figure>
                </section>
                <section id="credits" class="credits">
                  <a
                    class="meme-attribution"
                    data-meme-plan-id="m01"
                    data-meme-attribution-location="credits-slide"
                    href="https://example.com/license"
                  >Example Creator — Licensed Template, CC BY 4.0</a>
                </section>
                """,
                encoding="utf-8",
            )

            errors, warnings, _ = audit(html_path, 0.20, plan_path)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_html_plan_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            plan_path = tmp_path / "meme-plan.json"
            html_path = tmp_path / "deck.html"
            image_path = tmp_path / "meme.jpg"
            plan_path.write_text(json.dumps(valid_plan()), encoding="utf-8")
            image_path.write_bytes(b"test-image")
            html_path.write_text(
                """
                <section id="s08">
                  <figure
                    class="slide-meme"
                    data-meme-plan-id="m01"
                    data-meme-role="callback"
                    data-meme-template="Unrelated Wallpaper"
                    data-meme-source="https://example.com/wallpaper"
                    data-meme-origin="searched"
                  >
                    <img src="meme.jpg" alt="Promotional game wallpaper" />
                    <figcaption>Unrelated caption</figcaption>
                  </figure>
                </section>
                """,
                encoding="utf-8",
            )

            errors, _, _ = audit(html_path, 0.20, plan_path)
            joined = "\n".join(errors)
            self.assertIn("plan expects 'reaction'", joined)
            self.assertIn("plan expects 'Licensed Reaction Template'", joined)
            self.assertIn("plan expects 'https://example.com/license'", joined)

    def test_nested_div_inside_speaker_notes_preserves_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            plan = common_use_plan()
            placement = plan["placements"][0]
            placement["attribution_location"] = "speaker-notes"
            plan_path = directory / "meme-plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            (directory / "meme.jpg").write_bytes(b"test-image")
            html_path = directory / "deck.html"
            html_path.write_text(
                f"""
                <section id="s08">
                  <figure class="slide-meme" data-meme-plan-id="m01"
                    data-meme-role="reaction" data-meme-template="Two Buttons"
                    data-meme-source="{placement['attribution_url']}" data-meme-origin="searched">
                    <img src="meme.jpg" alt="A person hesitates between two buttons" />
                    <figcaption>{placement['caption']}</figcaption>
                  </figure>
                  <div class="speaker-notes">
                    <div class="notes-body"><p>Talking points</p></div>
                    <a class="meme-attribution" data-meme-plan-id="m01"
                      data-meme-attribution-location="speaker-notes"
                      href="{placement['attribution_url']}">{placement['attribution_text']}</a>
                  </div>
                </section>
                """,
                encoding="utf-8",
            )
            errors, warnings, _ = audit(html_path, 0.20, plan_path)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_void_element_inside_attribution_does_not_leak_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            plan = common_use_plan()
            placement = plan["placements"][0]
            placement["attribution_location"] = "on-slide"
            plan_path = directory / "meme-plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            (directory / "meme.jpg").write_bytes(b"test-image")
            html_path = directory / "deck.html"
            html_path.write_text(
                f"""
                <section id="s08">
                  <figure class="slide-meme" data-meme-plan-id="m01"
                    data-meme-role="reaction" data-meme-template="Two Buttons"
                    data-meme-source="{placement['attribution_url']}" data-meme-origin="searched">
                    <img src="meme.jpg" alt="A person hesitates between two buttons" />
                    <figcaption>{placement['caption']}</figcaption>
                    <a class="meme-attribution" href="{placement['attribution_url']}">
                      Two Buttons —<br>Imgflip template page
                    </a>
                  </figure>
                  <p>Trailing body text that must not leak into attribution</p>
                </section>
                """,
                encoding="utf-8",
            )
            errors, warnings, _ = audit(html_path, 0.20, plan_path)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_div_slides_and_nested_layout_sections_are_handled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            plan = common_use_plan()
            placement = plan["placements"][0]
            placement["attribution_location"] = "on-slide"
            plan_path = directory / "meme-plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            (directory / "meme.jpg").write_bytes(b"test-image")
            html_path = directory / "deck.html"
            html_path.write_text(
                f"""
                <div class="slide" id="s08">
                  <section class="layout-column">
                    <figure class="slide-meme" data-meme-plan-id="m01"
                      data-meme-role="reaction" data-meme-template="Two Buttons"
                      data-meme-source="{placement['attribution_url']}" data-meme-origin="searched">
                      <img src="meme.jpg" alt="A person hesitates between two buttons" />
                      <figcaption>{placement['caption']}</figcaption>
                      <a class="meme-attribution" href="{placement['attribution_url']}">
                        {placement['attribution_text']}
                      </a>
                    </figure>
                  </section>
                </div>
                """,
                encoding="utf-8",
            )
            errors, warnings, parser = audit(html_path, 0.20, plan_path)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])
            self.assertEqual(len(parser.slides), 1)
            self.assertEqual(parser.slides[0]["id"], "s08")

    def test_multifile_deck_with_separate_credits_slide_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            plan = common_use_plan()
            placement = plan["placements"][0]
            placement["attribution_location"] = "credits-slide"
            plan_path = directory / "meme-plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            (directory / "meme.jpg").write_bytes(b"test-image")
            slide1 = directory / "slide-01.html"
            slide1.write_text('<section id="s01"><h1>Intro</h1></section>', encoding="utf-8")
            slide2 = directory / "slide-08.html"
            slide2.write_text(
                f"""
                <section id="s08">
                  <figure class="slide-meme" data-meme-plan-id="m01"
                    data-meme-role="reaction" data-meme-template="Two Buttons"
                    data-meme-source="{placement['attribution_url']}" data-meme-origin="searched">
                    <img src="meme.jpg" alt="A person hesitates between two buttons" />
                    <figcaption>{placement['caption']}</figcaption>
                  </figure>
                </section>
                """,
                encoding="utf-8",
            )
            slide3 = directory / "slide-99.html"
            slide3.write_text(
                f"""
                <section id="credits" class="credits-slide">
                  <a class="meme-attribution" data-meme-plan-id="m01"
                    data-meme-attribution-location="credits-slide"
                    href="{placement['attribution_url']}">{placement['attribution_text']}</a>
                </section>
                """,
                encoding="utf-8",
            )
            errors, warnings, parser = audit([slide1, slide2, slide3], 0.50, plan_path)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])
            self.assertEqual(len(parser.slides), 3)

    def test_remote_hotlink_and_protocol_relative_urls_are_errors(self) -> None:
        for remote_src in ("https://cdn.example.com/meme.jpg", "//cdn.example.com/meme.jpg"):
            with self.subTest(remote_src=remote_src):
                with tempfile.TemporaryDirectory() as tmp:
                    html_path = Path(tmp) / "deck.html"
                    html_path.write_text(
                        f"""
                        <section id="s01">
                          <figure class="slide-meme" data-meme-role="reaction"
                            data-meme-source="https://example.com" data-meme-origin="searched">
                            <img src="{remote_src}" alt="A person hesitates" />
                            <figcaption>Caption</figcaption>
                            <a class="meme-attribution" href="https://example.com">Source</a>
                          </figure>
                        </section>
                        """,
                        encoding="utf-8",
                    )
                    errors, _, _ = audit(html_path, 0.20)
                    self.assertTrue(
                        any("remote URL" in error for error in errors)
                    )

    def test_local_image_query_string_and_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            deck_dir = root / "deck"
            deck_dir.mkdir()
            (deck_dir / "my meme.jpg").write_bytes(b"test-image")
            (root / "outside.jpg").write_bytes(b"outside")
            html_path = deck_dir / "slides.html"
            html_path.write_text(
                """
                <section id="s01">
                  <figure class="slide-meme" data-meme-role="reaction"
                    data-meme-source="https://example.com" data-meme-origin="searched">
                    <img src="my%20meme.jpg?v=2#top" alt="A person hesitates" />
                    <figcaption>Caption</figcaption>
                    <a class="meme-attribution" href="https://example.com">Source</a>
                  </figure>
                </section>
                """,
                encoding="utf-8",
            )
            errors, warnings, _ = audit(html_path, 0.20)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

            html_path.write_text(
                html_path.read_text(encoding="utf-8").replace(
                    "my%20meme.jpg?v=2#top", "../outside.jpg"
                ),
                encoding="utf-8",
            )
            errors, _, _ = audit(html_path, 0.20)
            self.assertTrue(
                any("escapes deck directory" in error for error in errors)
            )

    def test_orphan_attribution_and_callback_order_are_checked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            plan = common_use_plan()
            placement = plan["placements"][0]
            placement["role"] = "callback"
            placement["callback_to"] = "s10"
            placement["attribution_location"] = "on-slide"
            plan_path = directory / "meme-plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            (directory / "meme.jpg").write_bytes(b"test-image")
            html_path = directory / "deck.html"
            html_path.write_text(
                f"""
                <section id="s08">
                  <figure class="slide-meme" data-meme-plan-id="m01"
                    data-meme-role="callback" data-meme-template="Two Buttons"
                    data-meme-source="{placement['attribution_url']}" data-meme-origin="searched">
                    <img src="meme.jpg" alt="A person hesitates between two buttons" />
                    <figcaption>{placement['caption']}</figcaption>
                    <a class="meme-attribution" href="{placement['attribution_url']}">
                      {placement['attribution_text']}
                    </a>
                  </figure>
                </section>
                <section id="s10">
                  <a class="meme-attribution" data-meme-plan-id="m99"
                    href="https://example.com/orphan">Orphan</a>
                </section>
                """,
                encoding="utf-8",
            )
            errors, _, _ = audit(html_path, 0.50, plan_path)
            joined = "\n".join(errors)
            self.assertIn("callback_to slide 's10' must appear before 's08'", joined)
            self.assertIn("orphan .meme-attribution", joined)

    def test_duplicate_alt_and_figcaption_triggers_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "meme.jpg").write_bytes(b"test-image")
            html_path = directory / "deck.html"
            html_path.write_text(
                """
                <section id="s01">
                  <figure class="slide-meme" data-meme-role="reaction"
                    data-meme-source="https://example.com" data-meme-origin="searched">
                    <img src="meme.jpg" alt="Same punchline" />
                    <figcaption>Same punchline</figcaption>
                    <a class="meme-attribution" href="https://example.com">Source</a>
                  </figure>
                </section>
                """,
                encoding="utf-8",
            )
            errors, warnings, _ = audit(html_path, 0.20)
            self.assertEqual(errors, [])
            self.assertTrue(
                any("alt text duplicates figcaption" in warning for warning in warnings)
            )


class DensityAuditTests(unittest.TestCase):
    def write_deck(
        self,
        directory: Path,
        slide_count: int,
        meme_slides: set[int],
    ) -> Path:
        image_path = directory / "meme.jpg"
        image_path.write_bytes(b"test-image")
        sections = []
        for slide_number in range(1, slide_count + 1):
            figure = ""
            if slide_number in meme_slides:
                figure = f"""
                  <figure
                    class="slide-meme"
                    data-meme-role="reaction"
                    data-meme-source="user-provided"
                    data-meme-origin="user-provided"
                  >
                    <img src="meme.jpg" alt="A recognizable reaction" />
                    <figcaption>Reaction {slide_number}</figcaption>
                    <a class="meme-attribution" href="https://example.com/license">
                      Example Creator — Licensed Template, CC BY 4.0
                    </a>
                  </figure>
                """
            sections.append(
                f'<section id="s{slide_number:02d}">{figure}</section>'
            )
        html_path = directory / "deck.html"
        html_path.write_text("\n".join(sections), encoding="utf-8")
        return html_path

    def test_long_deck_may_exceed_three_memes_when_density_allows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            html_path = self.write_deck(
                Path(tmp),
                slide_count=60,
                meme_slides={8, 20, 34, 49},
            )
            errors, warnings, parser = audit(html_path, 0.10)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])
            self.assertEqual(len(parser.memes), 4)

    def test_density_ceiling_scales_down_for_short_decks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            html_path = self.write_deck(
                Path(tmp),
                slide_count=12,
                meme_slides={2, 6, 10},
            )
            errors, warnings, _ = audit(html_path, 0.10)
            self.assertEqual(errors, [])
            self.assertTrue(
                any("density ceiling allows about 2" in warning for warning in warnings)
            )


if __name__ == "__main__":
    unittest.main()
