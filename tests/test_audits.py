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


class MemePlanAuditTests(unittest.TestCase):
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
        self.assertTrue(any("require strict mode" in error for error in errors))

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


class HtmlPlanCrossCheckTests(unittest.TestCase):
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
