#!/usr/bin/env python3
"""Normalize code-buddy day, lesson, and topic target text."""
from __future__ import annotations

import argparse
import json
import re

ONES = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19,
}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}


def number_word(value: str) -> int | None:
    words = value.lower().replace("-", " ").split()
    if len(words) == 1 and words[0].isdigit():
        return int(words[0])
    if len(words) == 1:
        return ONES.get(words[0]) or TENS.get(words[0])
    if len(words) == 2 and words[0] in TENS and words[1] in ONES:
        return TENS[words[0]] + ONES[words[1]]
    return None


def normalize(raw: str) -> dict:
    text = " ".join(raw.strip().split())
    cleaned = re.sub(r"[,:]+", " ", text)
    match = re.search(r"\b(?:day|lesson|d)\s*[-_ ]?\s*(\d+|[a-z]+(?:[- ]+[a-z]+)?)\b", cleaned, re.I)
    if match:
        value = number_word(match.group(1))
        if value is not None:
            return {"raw": raw, "kind": "day", "number": value, "query": text}
    if re.fullmatch(r"\d+", text):
        return {"raw": raw, "kind": "day", "number": int(text), "query": text}
    value = number_word(text)
    if value is not None:
        return {"raw": raw, "kind": "day", "number": value, "query": text}
    return {"raw": raw, "kind": "topic", "number": None, "query": text.lower()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="+", help="day, lesson, number word, or topic")
    args = parser.parse_args()
    print(json.dumps(normalize(" ".join(args.target)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
