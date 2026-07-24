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


SLIDE_TAGS = {"section", "article"}


class DeckParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.slides: list[dict] = []
        self.slide_stack: list[int] = []
        self.slide_tag_stack: list[bool] = []
        self.figure_stack: list[dict | None] = []
        self.memes: list[dict] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        classes = set((attrs.get("class") or "").split())

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
                    "role": attrs.get("data-meme-role"),
                    "source": attrs.get("data-meme-source"),
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

    def handle_endtag(self, tag: str) -> None:
        if tag == "figure" and self.figure_stack:
            self.figure_stack.pop()
        if tag in SLIDE_TAGS and self.slide_tag_stack:
            if self.slide_tag_stack.pop() and self.slide_stack:
                self.slide_stack.pop()


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


def audit(path: Path, max_density: float) -> tuple[list[str], list[str], DeckParser]:
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
        if not meme["source"]:
            errors.append(f"{label}: missing data-meme-source.")
        if len(meme["images"]) != 1:
            errors.append(f"{label}: expected exactly one image.")
        if not meme["has_caption"]:
            warnings.append(f"{label}: missing figcaption.")

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

    if parser.slides:
        allowed = max(1, math.ceil(len(parser.slides) * max_density))
        if len(parser.memes) > allowed:
            warnings.append(
                f"Deck has {len(parser.memes)} memes across {len(parser.slides)} slides; "
                f"density target allows about {allowed}."
            )

    return errors, warnings, parser


def main() -> int:
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument("html", type=Path, help="HTML slide deck to audit")
    arg_parser.add_argument(
        "--max-density",
        type=float,
        default=0.20,
        help="Maximum target meme-to-slide ratio (default: 0.20)",
    )
    arg_parser.add_argument(
        "--strict",
        action="store_true",
        help="Return a failure status for warnings as well as errors",
    )
    args = arg_parser.parse_args()

    if not 0 < args.max_density <= 1:
        arg_parser.error("--max-density must be greater than 0 and at most 1")
    if not args.html.is_file():
        arg_parser.error(f"file not found: {args.html}")

    errors, warnings, parser = audit(args.html.resolve(), args.max_density)
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
