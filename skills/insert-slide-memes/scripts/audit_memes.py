#!/usr/bin/env python3
"""Audit structural and accessibility conventions for memes in an HTML deck."""

from __future__ import annotations

import argparse
import base64
import binascii
import math
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from audit_meme_plan import load_and_audit_plan


SLIDE_TAGS = {"section", "article"}


class DeckParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.slides: list[dict] = []
        self.slide_stack: list[int] = []
        self.slide_tag_stack: list[bool] = []
        self.figure_stack: list[dict | None] = []
        self.memes: list[dict] = []
        self.attributions: list[dict] = []
        self.attribution_depth = 0
        self.active_attribution: dict | None = None
        self.speaker_notes_stack: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        classes = set((attrs.get("class") or "").split())
        if "speaker-notes" in classes or "data-speaker-notes" in attrs:
            self.speaker_notes_stack.append(tag)

        if tag in SLIDE_TAGS:
            is_slide = tag == "section" or "slide" in classes or "data-slide" in attrs
            self.slide_tag_stack.append(is_slide)
            if is_slide:
                slide = {
                    "id": attrs.get("id") or f"slide-{len(self.slides) + 1}",
                    "classes": classes,
                    "memes": [],
                }
                self.slides.append(slide)
                self.slide_stack.append(len(self.slides) - 1)

        if tag == "figure":
            if "slide-meme" in classes:
                meme = {
                    "slide": self.slide_stack[-1] if self.slide_stack else None,
                    "plan_id": attrs.get("data-meme-plan-id"),
                    "role": attrs.get("data-meme-role"),
                    "template": attrs.get("data-meme-template"),
                    "source": attrs.get("data-meme-source"),
                    "origin": attrs.get("data-meme-origin"),
                    "images": [],
                    "has_caption": False,
                }
                self.memes.append(meme)
                if self.slide_stack:
                    self.slides[self.slide_stack[-1]]["memes"].append(meme)
                self.figure_stack.append(meme)
            else:
                self.figure_stack.append(None)

        if tag == "img" and self.figure_stack and self.figure_stack[-1] is not None:
            self.figure_stack[-1]["images"].append(
                {"src": attrs.get("src") or "", "alt": attrs.get("alt")}
            )

        if tag == "figcaption" and self.figure_stack and self.figure_stack[-1] is not None:
            self.figure_stack[-1]["has_caption"] = True

        if "meme-attribution" in classes:
            containing_meme = (
                self.figure_stack[-1]
                if self.figure_stack and self.figure_stack[-1] is not None
                else None
            )
            attribution = {
                "tag": tag,
                "plan_id": attrs.get("data-meme-plan-id")
                or (containing_meme["plan_id"] if containing_meme else None),
                "location": attrs.get("data-meme-attribution-location")
                or ("on-slide" if containing_meme else None),
                "inside_figure": containing_meme is not None,
                "inside_speaker_notes": bool(self.speaker_notes_stack),
                "inside_credits_slide": bool(
                    self.slide_stack
                    and self.slides[self.slide_stack[-1]]["classes"]
                    & {"credits", "credits-slide", "references", "sources"}
                ),
                "containing_meme": containing_meme,
                "containing_plan_id": (
                    containing_meme["plan_id"] if containing_meme else None
                ),
                "href": attrs.get("href"),
                "text": [],
            }
            self.attributions.append(attribution)
            self.attribution_depth = 1
            self.active_attribution = attribution
        elif self.attribution_depth:
            self.attribution_depth += 1

    def handle_data(self, data: str) -> None:
        if self.attribution_depth and self.active_attribution is not None and data.strip():
            self.active_attribution["text"].append(data.strip())

    def handle_endtag(self, tag: str) -> None:
        if self.attribution_depth:
            self.attribution_depth -= 1
            if self.attribution_depth == 0:
                self.active_attribution = None
        if tag == "figure" and self.figure_stack:
            self.figure_stack.pop()
        if tag in SLIDE_TAGS and self.slide_tag_stack:
            if self.slide_tag_stack.pop() and self.slide_stack:
                self.slide_stack.pop()
        if self.speaker_notes_stack and self.speaker_notes_stack[-1] == tag:
            self.speaker_notes_stack.pop()


def is_remote(src: str) -> bool:
    return urlparse(src).scheme in {"http", "https"}


def valid_embedded_image(src: str) -> bool:
    header, separator, payload = src.partition(",")
    if not separator or not header.startswith("data:image/") or not header.endswith(";base64"):
        return False
    try:
        return bool(base64.b64decode(payload, validate=True))
    except (binascii.Error, ValueError):
        return False


def audit(
    path: Path,
    max_density: float,
    plan_path: Path | None = None,
) -> tuple[list[str], list[str], DeckParser]:
    parser = DeckParser()
    parser.feed(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    if not parser.slides:
        warnings.append("No slide sections detected; density and per-slide checks were skipped.")

    for slide in parser.slides:
        if len(slide["memes"]) > 1:
            errors.append(f"{slide['id']}: contains {len(slide['memes'])} memes; limit is one.")
        if slide["memes"] and ({"title", "agenda", "legal"} & slide["classes"]):
            warnings.append(f"{slide['id']}: meme appears on a potentially sensitive slide.")

    for index, meme in enumerate(parser.memes, 1):
        label = (
            parser.slides[meme["slide"]]["id"]
            if meme["slide"] is not None
            else f"meme-{index}"
        )
        if meme["role"] not in {"reaction", "analogy", "callback", "transition"}:
            errors.append(f"{label}: missing or invalid data-meme-role.")
        if meme["origin"] not in {"searched", "user-provided"}:
            errors.append(f"{label}: missing or invalid data-meme-origin.")
        if not meme["source"]:
            errors.append(f"{label}: missing data-meme-source.")
        if len(meme["images"]) != 1:
            errors.append(f"{label}: expected exactly one image.")
        if not meme["has_caption"]:
            warnings.append(f"{label}: missing figcaption.")
        if plan_path is None:
            matching_attributions = [
                attribution
                for attribution in parser.attributions
                if attribution["inside_figure"]
                and attribution["containing_meme"] is meme
            ]
            if not matching_attributions:
                errors.append(
                    f"{label}: missing .meme-attribution element inside the meme figure; "
                    "use --plan to validate a credits-slide or speaker-notes attribution."
                )

        for image in meme["images"]:
            if image["alt"] is None:
                errors.append(f"{label}: image is missing an alt attribute.")
            src = image["src"]
            if not src:
                errors.append(f"{label}: image has an empty src.")
            elif src.startswith("data:"):
                if not valid_embedded_image(src):
                    errors.append(f"{label}: image has an invalid embedded data URL.")
            elif is_remote(src):
                warnings.append(f"{label}: image uses a remote URL; download it locally.")
            else:
                local_path = (path.parent / src).resolve()
                if not local_path.is_file():
                    errors.append(f"{label}: local image not found: {src}")

    for index, attribution in enumerate(parser.attributions, 1):
        label = attribution["plan_id"] or f"attribution-{index}"
        if attribution["tag"] != "a" or not attribution["href"]:
            errors.append(f"{label}: .meme-attribution must be a link with an href.")
        if not attribution["text"]:
            errors.append(f"{label}: .meme-attribution must contain text.")

    if parser.slides:
        allowed = max(1, math.ceil(len(parser.slides) * max_density))
        if len(parser.memes) > allowed:
            warnings.append(
                f"Deck has {len(parser.memes)} memes across {len(parser.slides)} slides; "
                f"the selected density ceiling allows about {allowed}."
            )

    if plan_path is not None:
        _, plan_errors, plan_warnings, selected = load_and_audit_plan(plan_path)
        errors.extend(f"plan: {message}" for message in plan_errors)
        warnings.extend(f"plan: {message}" for message in plan_warnings)

        selected_by_id = {
            record["id"]: record
            for record in selected
            if isinstance(record.get("id"), str) and record["id"]
        }
        html_by_id: dict[str, dict] = {}
        attributions_by_id: dict[str, list[dict]] = {}
        for attribution in parser.attributions:
            plan_id = attribution["plan_id"]
            if isinstance(plan_id, str) and plan_id:
                attributions_by_id.setdefault(plan_id, []).append(attribution)
        for index, meme in enumerate(parser.memes, 1):
            plan_id = meme["plan_id"]
            label = (
                parser.slides[meme["slide"]]["id"]
                if meme["slide"] is not None
                else f"meme-{index}"
            )
            if not plan_id:
                errors.append(f"{label}: missing data-meme-plan-id required by --plan.")
                continue
            if plan_id in html_by_id:
                errors.append(f"{label}: duplicate data-meme-plan-id {plan_id}.")
                continue
            html_by_id[plan_id] = meme

            record = selected_by_id.get(plan_id)
            if record is None:
                errors.append(f"{label}: plan ID {plan_id} is not selected in the plan.")
                continue

            expected = {
                "role": record.get("role"),
                "template": record.get("template"),
                "source": record.get("source"),
                "origin": record.get("origin"),
            }
            for field, value in expected.items():
                if meme[field] != value:
                    errors.append(
                        f"{label}: data-meme-{field.replace('_', '-')} "
                        f"is {meme[field]!r}; plan expects {value!r}."
                    )

            slide_id = (
                parser.slides[meme["slide"]]["id"]
                if meme["slide"] is not None
                else None
            )
            if slide_id != record.get("slide_id"):
                errors.append(
                    f"{label}: meme is on slide {slide_id!r}; "
                    f"plan expects {record.get('slide_id')!r}."
                )
            matching_attributions = attributions_by_id.get(plan_id, [])
            if not matching_attributions:
                errors.append(
                    f"{label}: missing .meme-attribution for selected placement {plan_id}."
                )
                continue
            if len(matching_attributions) > 1:
                errors.append(
                    f"{label}: multiple .meme-attribution elements map to {plan_id}."
                )
                continue

            attribution = matching_attributions[0]
            expected_location = record.get("attribution_location")
            if attribution["location"] != expected_location:
                errors.append(
                    f"{label}: attribution location is {attribution['location']!r}; "
                    f"plan expects {expected_location!r}."
                )
            if expected_location == "on-slide" and (
                not attribution["inside_figure"]
                or attribution["containing_plan_id"] != plan_id
            ):
                errors.append(
                    f"{label}: on-slide attribution must be inside its meme figure."
                )
            if expected_location in {"credits-slide", "speaker-notes"} and attribution[
                "inside_figure"
            ]:
                errors.append(
                    f"{label}: {expected_location} attribution must be outside the "
                    "meme figure and identify data-meme-plan-id."
                )
            if (
                expected_location == "credits-slide"
                and not attribution["inside_credits_slide"]
            ):
                errors.append(
                    f"{label}: credits-slide attribution must be inside a slide "
                    "classed as credits, credits-slide, references, or sources."
                )
            if (
                expected_location == "speaker-notes"
                and not attribution["inside_speaker_notes"]
            ):
                errors.append(
                    f"{label}: speaker-notes attribution must be inside an element "
                    "with class speaker-notes or data-speaker-notes."
                )
            if attribution["href"] != record.get("attribution_url"):
                errors.append(
                    f"{label}: attribution href is {attribution['href']!r}; plan "
                    f"expects {record.get('attribution_url')!r}."
                )
            actual_attribution = " ".join(" ".join(attribution["text"]).split())
            expected_attribution = " ".join(
                str(record.get("attribution_text") or "").split()
            )
            if actual_attribution != expected_attribution:
                errors.append(
                    f"{label}: attribution text is {actual_attribution!r}; plan "
                    f"expects {expected_attribution!r}."
                )

        for plan_id in selected_by_id.keys() - html_by_id.keys():
            errors.append(f"plan: selected placement {plan_id} is missing from HTML.")

    return errors, warnings, parser


def main() -> int:
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument("html", type=Path, help="HTML slide deck to audit")
    arg_parser.add_argument(
        "--max-density",
        type=float,
        default=0.20,
        help=(
            "Soft maximum meme-to-slide ratio for structural QA "
            "(default: 0.20; choose an audience-appropriate value)"
        ),
    )
    arg_parser.add_argument(
        "--strict",
        action="store_true",
        help="Return a failure status for warnings as well as errors",
    )
    arg_parser.add_argument(
        "--plan",
        type=Path,
        help="Audited meme plan JSON to cross-check against the HTML",
    )
    args = arg_parser.parse_args()

    if not 0 < args.max_density <= 1:
        arg_parser.error("--max-density must be greater than 0 and at most 1")
    if not args.html.is_file():
        arg_parser.error(f"file not found: {args.html}")

    errors, warnings, parser = audit(
        args.html.resolve(),
        args.max_density,
        args.plan.resolve() if args.plan else None,
    )
    print(
        f"Slides: {len(parser.slides)} | Memes: {len(parser.memes)} | "
        f"Errors: {len(errors)} | Warnings: {len(warnings)}"
    )
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")

    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
