#!/usr/bin/env python3
"""Audit structural and accessibility conventions for memes in an HTML deck."""

from __future__ import annotations

import argparse
import base64
import binascii
import math
import os
from collections.abc import Sequence
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from audit_meme_plan import _is_http_url, load_and_audit_plan


SLIDE_TAGS = {"section", "article", "div"}
VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class DeckParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.source_file: Path | None = None
        self.slides: list[dict] = []
        self.slide_stack: list[int] = []
        self.figure_stack: list[dict | None] = []
        self.memes: list[dict] = []
        self.attributions: list[dict] = []
        self.active_attributions: list[dict] = []
        self.active_figcaptions: list[dict] = []
        self.speaker_notes_depth = 0
        self.element_stack: list[dict] = []

    def parse_file(self, path: Path) -> None:
        self.source_file = path
        self.slide_stack.clear()
        self.figure_stack.clear()
        self.active_attributions.clear()
        self.active_figcaptions.clear()
        self.speaker_notes_depth = 0
        self.element_stack.clear()
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def _is_slide_element(
        self,
        tag: str,
        classes: set[str],
        attrs: dict[str, str | None],
    ) -> bool:
        if tag not in SLIDE_TAGS:
            return False
        explicit_slide = "slide" in classes or "data-slide" in attrs
        if tag == "section":
            return explicit_slide or not self.slide_stack
        return explicit_slide

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        classes = set((attrs.get("class") or "").split())
        is_void = tag in VOID_ELEMENTS

        is_speaker_notes = "speaker-notes" in classes or "data-speaker-notes" in attrs
        if is_speaker_notes and not is_void:
            self.speaker_notes_depth += 1

        is_slide = self._is_slide_element(tag, classes, attrs)
        if is_slide and not is_void:
            slide = {
                "id": attrs.get("id") or f"slide-{len(self.slides) + 1}",
                "classes": classes,
                "memes": [],
                "source_file": self.source_file,
            }
            self.slides.append(slide)
            self.slide_stack.append(len(self.slides) - 1)

        is_figure = tag == "figure" and not is_void
        if is_figure:
            if "slide-meme" in classes:
                meme = {
                    "slide": self.slide_stack[-1] if self.slide_stack else None,
                    "source_file": self.source_file,
                    "plan_id": attrs.get("data-meme-plan-id"),
                    "role": attrs.get("data-meme-role"),
                    "template": attrs.get("data-meme-template"),
                    "source": attrs.get("data-meme-source"),
                    "origin": attrs.get("data-meme-origin"),
                    "images": [],
                    "has_caption": False,
                    "caption_text": [],
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

        is_figcaption = (
            tag == "figcaption"
            and not is_void
            and bool(self.figure_stack)
            and self.figure_stack[-1] is not None
        )
        if is_figcaption:
            meme = self.figure_stack[-1]
            assert meme is not None
            meme["has_caption"] = True
            self.active_figcaptions.append(meme)

        is_attribution = "meme-attribution" in classes
        if is_attribution:
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
                "inside_speaker_notes": self.speaker_notes_depth > 0,
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
            if not is_void:
                self.active_attributions.append(attribution)

        if not is_void:
            self.element_stack.append(
                {
                    "tag": tag,
                    "is_slide": is_slide,
                    "is_speaker_notes": is_speaker_notes,
                    "is_figure": is_figure,
                    "is_figcaption": is_figcaption,
                    "is_attribution": is_attribution,
                }
            )

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if not stripped:
            return
        if self.active_attributions:
            self.active_attributions[-1]["text"].append(stripped)
        if self.active_figcaptions:
            self.active_figcaptions[-1]["caption_text"].append(stripped)

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_ELEMENTS:
            return
        match_index: int | None = None
        for idx in range(len(self.element_stack) - 1, -1, -1):
            if self.element_stack[idx]["tag"] == tag:
                match_index = idx
                break
        if match_index is None:
            return

        while len(self.element_stack) > match_index:
            frame = self.element_stack.pop()
            if frame["is_attribution"] and self.active_attributions:
                self.active_attributions.pop()
            if frame["is_figcaption"] and self.active_figcaptions:
                self.active_figcaptions.pop()
            if frame["is_figure"] and self.figure_stack:
                self.figure_stack.pop()
            if frame["is_slide"] and self.slide_stack:
                self.slide_stack.pop()
            if frame["is_speaker_notes"] and self.speaker_notes_depth > 0:
                self.speaker_notes_depth -= 1


def is_remote(src: str) -> bool:
    stripped = src.strip()
    if stripped.startswith("//"):
        return True
    return urlparse(stripped).scheme.lower() in {"http", "https", "ftp"}


def valid_embedded_image(src: str) -> bool:
    header, separator, payload = src.partition(",")
    if not separator or not header.startswith("data:image/") or not header.endswith(";base64"):
        return False
    try:
        return bool(base64.b64decode(payload, validate=True))
    except (binascii.Error, ValueError):
        return False


def _expand_html_paths(paths: Path | Sequence[Path]) -> list[Path]:
    raw_paths = [paths] if isinstance(paths, Path) else list(paths)
    expanded: list[Path] = []
    for item in raw_paths:
        resolved = item.resolve()
        if resolved.is_dir():
            expanded.extend(sorted(p.resolve() for p in resolved.glob("*.html")))
        else:
            expanded.append(resolved)
    return expanded


def audit(
    path: Path | Sequence[Path],
    max_density: float,
    plan_path: Path | None = None,
) -> tuple[list[str], list[str], DeckParser]:
    html_paths = _expand_html_paths(path)
    parser = DeckParser()
    errors: list[str] = []
    warnings: list[str] = []

    if not html_paths:
        return ["No HTML files found to audit."], warnings, parser

    for html_file in html_paths:
        parser.parse_file(html_file)

    deck_root = Path(os.path.commonpath([str(p.parent) for p in html_paths])).resolve()

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

        caption_norm = " ".join(" ".join(meme["caption_text"]).split())
        base_dir = (meme["source_file"] or html_paths[0]).parent
        for image in meme["images"]:
            if image["alt"] is None:
                errors.append(f"{label}: image is missing an alt attribute.")
            else:
                alt_norm = " ".join(image["alt"].split())
                if alt_norm and caption_norm and alt_norm == caption_norm:
                    warnings.append(
                        f"{label}: image alt text duplicates figcaption; "
                        "describe the visual instead."
                    )
            src = image["src"].strip()
            if not src:
                errors.append(f"{label}: image has an empty src.")
            elif src.startswith("data:"):
                if not valid_embedded_image(src):
                    errors.append(f"{label}: image has an invalid embedded data URL.")
            elif is_remote(src):
                errors.append(f"{label}: image uses a remote URL; download it locally.")
            else:
                raw_local = unquote(urlparse(src).path)
                if not raw_local or Path(raw_local).is_absolute():
                    errors.append(
                        f"{label}: local image must use a relative path inside the deck: {src}"
                    )
                else:
                    local_path = (base_dir / raw_local).resolve()
                    if not local_path.is_relative_to(deck_root):
                        errors.append(
                            f"{label}: local image escapes deck directory: {src}"
                        )
                    elif not local_path.is_file():
                        errors.append(f"{label}: local image not found: {src}")

    for index, attribution in enumerate(parser.attributions, 1):
        label = attribution["plan_id"] or f"attribution-{index}"
        if attribution["tag"] != "a" or not _is_http_url(attribution["href"]):
            errors.append(
                f"{label}: .meme-attribution must be a link with a valid http(s) href."
            )
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
        slide_index_by_id = {
            slide["id"]: idx for idx, slide in enumerate(parser.slides)
        }
        html_by_id: dict[str, dict] = {}
        attributions_by_id: dict[str, list[dict]] = {}
        for index, attribution in enumerate(parser.attributions, 1):
            plan_id = attribution["plan_id"]
            if not isinstance(plan_id, str) or not plan_id:
                errors.append(
                    f"attribution-{index}: .meme-attribution is missing data-meme-plan-id."
                )
                continue
            if plan_id not in selected_by_id:
                errors.append(
                    f"{plan_id}: orphan .meme-attribution does not match a selected placement."
                )
                continue
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
                "source": record.get("source") or record.get("attribution_url"),
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

            if record.get("role") == "callback" and meme["slide"] is not None:
                callback_to = record.get("callback_to")
                if isinstance(callback_to, str) and callback_to:
                    target_idx = slide_index_by_id.get(callback_to)
                    if target_idx is None:
                        errors.append(
                            f"{label}: callback_to slide {callback_to!r} was not found in HTML."
                        )
                    elif target_idx >= meme["slide"]:
                        errors.append(
                            f"{label}: callback_to slide {callback_to!r} must appear "
                            f"before {slide_id!r}."
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
    arg_parser.add_argument(
        "html",
        type=Path,
        nargs="+",
        help="One or more HTML slide files (or a directory of slide HTML files) to audit",
    )
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
    for target in args.html:
        if not target.exists():
            arg_parser.error(f"file or directory not found: {target}")

    errors, warnings, parser = audit(
        [target.resolve() for target in args.html],
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
