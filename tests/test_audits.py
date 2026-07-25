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
        "plan_version": 1,
        "audience": "Mixed internal training audience",
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
                "template": "Confused Travolta",
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
                "semantic_source": "https://example.com/confused-travolta-meaning",
                "original_source": "https://example.com/original",
                "asset_source": "https://example.com/confused-travolta.jpg",
                "source": "https://example.com/confused-travolta-meaning",
                "rights_status": "unclear",
                "distribution": "internal",
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
                "plan_version": 1,
                "audience": "Executive briefing",
                "placements": [],
            }
        )
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(selected, [])

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

    def test_user_provided_exact_asset_may_bypass_format_gate(self) -> None:
        plan = valid_plan()
        placement = plan["placements"][0]
        placement["origin"] = "user-provided"
        placement["template"] = "User-provided exact asset"
        placement["source"] = "user-provided"
        placement["rights_status"] = "user-provided-unverified"
        placement["user_locked"] = {"asset": True, "placement": True, "caption": False}
        placement["hard_gates"]["established_format"] = False
        for field in (
            "asset_kind",
            "recognition_basis",
            "recognition_evidence",
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
        self.assertEqual([record["id"] for record in selected], ["m01"])

    def test_public_distribution_requires_cleared_rights(self) -> None:
        plan = valid_plan()
        plan["placements"][0]["distribution"] = "public"
        errors, _, _ = audit_plan_data(plan)
        self.assertTrue(
            any("public distribution requires cleared rights" in error for error in errors)
        )

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
                    data-meme-template="Confused Travolta"
                    data-meme-source="https://example.com/confused-travolta-meaning"
                    data-meme-origin="searched"
                  >
                    <img src="meme.jpg" alt="A confused person looks around" />
                    <figcaption>분명 저장했습니다. 어디에 저장했는지만 빼고.</figcaption>
                  </figure>
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
            self.assertIn("plan expects 'Confused Travolta'", joined)
            self.assertIn("plan expects 'https://example.com/confused-travolta-meaning'", joined)


if __name__ == "__main__":
    unittest.main()
