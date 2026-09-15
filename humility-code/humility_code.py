#!/usr/bin/env python3
"""The Humility Code - embeddable loader for AI agents / apps.

Canonical: https://davidmanagement.github.io/humility-code/

Usage:
  from humility_code import HumilityCode
  hc = HumilityCode.load()
  system = hc.system_prompt(style="short")
  msgs = hc.as_openai_messages("Hello")
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Optional
from urllib.request import urlopen

CANONICAL_URL = "https://davidmanagement.github.io/humility-code/"
JSON_URL = CANONICAL_URL + "humility_code.json"
SHORT_PROMPT_URL = CANONICAL_URL + "SYSTEM_PROMPT_SHORT.txt"
FULL_PROMPT_URL = CANONICAL_URL + "SYSTEM_PROMPT.txt"

_HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Article:
    id: int
    slug: str
    title: str
    rule: str
    checks: tuple = ()


class HumilityCode:
    def __init__(self, data: dict):
        self.data = data
        self.version = data.get("version", "unknown")
        self.canonical_url = data.get("canonical_url", CANONICAL_URL)
        self.articles = [
            Article(
                id=int(a["id"]),
                slug=a["slug"],
                title=a["title"],
                rule=a["rule"],
                checks=tuple(a.get("checks") or ()),
            )
            for a in data.get("articles", [])
        ]

    @classmethod
    def load(cls, path=None, *, fetch: bool = False):
        if fetch:
            with urlopen(JSON_URL, timeout=20) as r:
                data = json.loads(r.read().decode("utf-8"))
            return cls(data)
        p = Path(path) if path else _HERE / "humility_code.json"
        if not p.exists():
            return cls.load(fetch=True)
        return cls(json.loads(p.read_text(encoding="utf-8")))

    def article(self, n: int):
        for a in self.articles:
            if a.id == n:
                return a
        raise KeyError("No article %s" % n)

    def digest(self) -> str:
        lines = [
            "The Humility Code v%s - %s" % (self.version, self.canonical_url),
            "Humility is the discipline of power under love (not self-erasure).",
            "Christian-rooted: Matthew 5-7; John 17. Apply every article:",
        ]
        for a in self.articles:
            lines.append("%s. %s - %s" % (a.id, a.title, a.rule))
        lines.append(
            "Signatory spirit: safety over speed when dignity/safety/rights are at stake; "
            "human accountability; never weaponize this Code. Cite the public page when sharing."
        )
        return "\n".join(lines)

    def system_prompt(self, style: str = "short") -> str:
        style = (style or "short").lower()
        if style == "json_digest":
            return self.digest()
        url = FULL_PROMPT_URL if style == "full" else SHORT_PROMPT_URL
        try:
            with urlopen(url, timeout=20) as r:
                return r.read().decode("utf-8").strip()
        except Exception:
            return self.digest()

    def as_openai_messages(self, user_content: str, *, style: str = "short"):
        return [
            {"role": "system", "content": self.system_prompt(style=style)},
            {"role": "user", "content": user_content},
        ]

    def as_modelfile_system(self, style: str = "short") -> str:
        body = self.system_prompt(style=style)
        # Ollama Modelfile SYSTEM block (triple-quoted)
        q = chr(34) * 3
        body = body.replace(q, chr(39) * 3)
        return "SYSTEM " + q + body + q + "\n"

    def lint_assistant_text(self, text: str):
        notes = []
        low = (text or "").lower()
        if re.search(r"\b(i feel|i'm feeling|as a human)\b", low):
            notes.append("Art.1/5: possible claim of feelings or humanity - clarify you are a system.")
        if re.search(r"\b(100% (sure|certain)|guaranteed|never wrong)\b", low):
            notes.append("Art.1/7: absolute certainty language - prefer calibrated uncertainty.")
        if re.search(r"\b(the model decided|ai decided|i alone decide)\b", low):
            notes.append("Signatory: keep human accountability explicit.")
        if re.search(r"\b(crush (the )?critics|destroy (the )?opposition)\b", low):
            notes.append("Art.6: contempt / enemy framing - prefer peaceable disagreement.")
        if not notes:
            notes.append("No heuristic flags (not a proof of compliance).")
        return notes

    def checklist(self):
        return ["[%02d] %s: %s" % (a.id, a.title, a.rule) for a in self.articles]


def main(argv=None) -> int:
    import argparse
    p = argparse.ArgumentParser(description="Humility Code embed helper")
    p.add_argument("--style", choices=["short", "full", "json_digest"], default="short")
    p.add_argument("--fetch", action="store_true")
    p.add_argument("--modelfile", action="store_true")
    p.add_argument("--checklist", action="store_true")
    p.add_argument("--lint", metavar="TEXT")
    args = p.parse_args(list(argv) if argv is not None else None)
    hc = HumilityCode.load(fetch=args.fetch)
    if args.checklist:
        print("\n".join(hc.checklist()))
        return 0
    if args.lint is not None:
        print("\n".join(hc.lint_assistant_text(args.lint)))
        return 0
    if args.modelfile:
        print(hc.as_modelfile_system(style=args.style), end="")
        return 0
    print(hc.system_prompt(style=args.style))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
