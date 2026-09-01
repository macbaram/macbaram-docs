#!/usr/bin/env python3
"""Validate the MacBaram public knowledge base without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "KNOWN_LIMITATIONS.md",
    "SUPPORT.md",
    "SECURITY.md",
    "docs/README.md",
    "docs/features.md",
    "docs/supported-macs.md",
    "docs/safety-and-permissions.md",
    "docs/troubleshooting.md",
    "docs/faq.md",
    "docs/roadmap.md",
    "docs/consistency-rules.md",
    "docs/update-policy.md",
    "data/public-facts.json",
    "assets/macbaram-icon.png",
    "assets/macbaram-dashboard.webp",
    "assets/social-preview.png",
}
ALLOWED_STATUSES = {"available", "roadmap", "concept", "unsupported"}
OFFICIAL_ORIGIN = "www.macbaram.com"
CANONICAL_DOWNLOAD = "https://www.macbaram.com/download"
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml"}
FORBIDDEN_PATTERNS = {
    "version-specific package URL": re.compile(r"https?://[^\s)>]+\.pkg\b", re.I),
    "technical download path": re.compile(r"(?:/downloads/|\blatest\.json\b)", re.I),
    "stale download preparation copy": re.compile(r"다운로드\s*준비\s*중"),
    "test-mode publication": re.compile(r"\btest mode\b", re.I),
    "duplicated dollar price": re.compile(r"\$\s*\d"),
    "duplicated monthly price": re.compile(r"\b(?:per month|monthly price)\b", re.I),
    "duplicated commercial state": re.compile(
        r"\b(?:free trial|trial (?:is )?available|subscription required|paid plan)\b",
        re.I,
    ),
    "private local path": re.compile(r"(?:/Users/|/private/tmp/|/var/folders/)"),
    "internal component name": re.compile(r"\b(?:MacBaramCloud|MacBaramPortal|MacBaramNode)\b"),
    "private key material": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "token-like secret": re.compile(r"\b(?:api[_-]?key|client[_-]?secret|access[_-]?token)\s*[:=]", re.I),
    "performance guarantee": re.compile(r"\bguarantee(?:s|d)? (?:better|higher|maximum) performance\b", re.I),
    "throttling guarantee": re.compile(r"\b(?:prevents?|stops?) thermal throttling\b", re.I),
    "battery lifespan guarantee": re.compile(r"\bguarantee(?:s|d)? (?:a )?(?:longer|extended) battery (?:life|lifespan)\b", re.I),
    "complete protection claim": re.compile(r"\b(?:complete|perfect|total) (?:hardware )?protection\b", re.I),
    "iMac support claim": re.compile(r"\biMac (?:is )?(?:fully )?supported\b", re.I),
}
EXPECTED_FACT_STATUSES = {
    "apple-silicon-requirement": "available",
    "fan-control": "available",
    "charging-controls": "available",
    "sleep-prevention": "available",
    "low-battery-sleep-return": "available",
    "heat-protection": "available",
    "virtual-clamshell": "available",
    "individual-plans": "available",
    "enterprise-single": "roadmap",
    "enterprise-fleet": "roadmap",
    "unified-dashboard": "available",
    "intel-mac": "unsupported",
    "imac": "unsupported",
}
ROADMAP_ONLY_TERMS = {
    "Enterprise Single",
    "Enterprise Fleet",
    "Creator Sponsorship",
    "Creator Access",
    "Supporters",
}
ROADMAP_TEXT_FILES = {
    Path("docs/roadmap.md"),
}
PROMOTION_PATTERNS = (
    re.compile(
        r"\b(?:(?:is|are)\s+(?:currently\s+)?(?:available|open|operational|live)|"
        r"currently\s+(?:available|open|operational|live)|available\s+now|"
        r"current\s+(?:product\s+)?plan|on\s+sale|(?:has\s+)?launched|"
        r"released\s+(?:today|now)|went\s+live)\b",
        re.I,
    ),
    re.compile(r"(?:현재\s*(?:판매|제공|이용|운영)|판매\s*중|운영\s*중|모집\s*중|정산\s*중|지급\s*중|출시(?:됐|되었|되었습니다|했습니다|함|됨))"),
)
NEGATED_PROMOTION_PATTERNS = (
    re.compile(r"\b(?:not|no|does\s+not|is\s+not|are\s+not)\b", re.I),
    re.compile(r"(?:아닙니다|않습니다|없습니다|미검증|증명\s*전|전에는)"),
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def text_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in TEXT_SUFFIXES
    ]


def validate_required(errors: list[str]) -> None:
    for relative in sorted(REQUIRED):
        if not (ROOT / relative).is_file():
            fail(errors, f"missing required file: {relative}")


def validate_public_facts(errors: list[str]) -> None:
    path = ROOT / "data/public-facts.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"invalid public facts JSON: {exc}")
        return

    if data.get("schema_version") != 1:
        fail(errors, "public facts schema_version must be 1")
    if data.get("official_download") != CANONICAL_DOWNLOAD:
        fail(errors, "official_download must use the canonical /download URL")
    if set(data.get("status_values", [])) != ALLOWED_STATUSES:
        fail(errors, "status_values must match the approved status vocabulary")

    seen: set[str] = set()
    facts_by_id: dict[str, dict[str, object]] = {}
    for index, fact in enumerate(data.get("facts", [])):
        prefix = f"facts[{index}]"
        required = {"id", "status", "summary", "verified_on", "source_url"}
        missing = required - set(fact)
        if missing:
            fail(errors, f"{prefix} missing fields: {', '.join(sorted(missing))}")
            continue
        if fact["id"] in seen:
            fail(errors, f"duplicate fact id: {fact['id']}")
        seen.add(fact["id"])
        facts_by_id[fact["id"]] = fact
        if fact["status"] not in ALLOWED_STATUSES:
            fail(errors, f"{prefix} has invalid status: {fact['status']}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fact["verified_on"]):
            fail(errors, f"{prefix} verified_on must be YYYY-MM-DD")
        parsed = urlparse(fact["source_url"])
        if parsed.scheme != "https" or parsed.netloc != OFFICIAL_ORIGIN:
            fail(errors, f"{prefix} source_url must use the official HTTPS origin")

    validate_fact_status_contract(errors, facts_by_id)


def validate_fact_status_contract(
    errors: list[str], facts_by_id: dict[str, dict[str, object]]
) -> None:
    unknown = set(facts_by_id) - set(EXPECTED_FACT_STATUSES)
    for fact_id in sorted(unknown):
        fail(errors, f"unregistered public fact: {fact_id}")

    for fact_id, expected_status in EXPECTED_FACT_STATUSES.items():
        fact = facts_by_id.get(fact_id)
        if fact is None:
            fail(errors, f"missing required public fact: {fact_id}")
        elif fact.get("status") != expected_status:
            fail(
                errors,
                f"public fact {fact_id} must be {expected_status}, got {fact.get('status')}",
            )
        elif expected_status in {"roadmap", "concept"}:
            summary = str(fact.get("summary", ""))
            claims = noncurrent_promotion_claims(summary)
            if claims:
                fail(errors, f"public fact {fact_id} promotes a non-current item: {claims[0]}")


def validate_content(errors: list[str]) -> None:
    for path in text_files():
        relative = path.relative_to(ROOT)
        content = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(content):
                fail(errors, f"{relative}: {label}")

        for url in re.findall(r"https?://[^\s)>\]`]+", content):
            if ".pkg" in url.lower():
                fail(errors, f"{relative}: package URLs are not public documentation links")


def validate_roadmap_boundaries(errors: list[str]) -> None:
    roadmap = (ROOT / "docs/roadmap.md").read_text(encoding="utf-8")
    if "Nothing on this page makes" not in roadmap:
        fail(errors, "docs/roadmap.md must state that roadmap copy does not activate a feature or operation")

    for path in text_files():
        relative = path.relative_to(ROOT)
        if relative == Path("data/public-facts.json") or relative in ROADMAP_TEXT_FILES:
            continue
        content = path.read_text(encoding="utf-8")
        for term in roadmap_only_terms(content):
            fail(errors, f"{relative}: non-current term outside roadmap surfaces: {term}")

    for relative in sorted(ROADMAP_TEXT_FILES):
        content = (ROOT / relative).read_text(encoding="utf-8")
        for claim in noncurrent_promotion_claims(content):
            fail(errors, f"{relative}: non-current item promoted as current: {claim}")


def roadmap_only_terms(content: str) -> set[str]:
    folded = content.casefold()
    return {term for term in ROADMAP_ONLY_TERMS if term.casefold() in folded}


def noncurrent_promotion_claims(content: str) -> list[str]:
    claims: list[str] = []
    for line in content.splitlines():
        for sentence in re.split(r"(?<=[.!?。！？])\s+", line):
            clauses = re.split(
                r"\s*(?:[,;]|\bbut\b|\bwhile\b|\bwhereas\b|\band\b|하지만|다만|그리고)\s*",
                sentence,
                flags=re.I,
            )
            for clause in clauses:
                if not roadmap_only_terms(clause):
                    continue
                if any(pattern.search(clause) for pattern in NEGATED_PROMOTION_PATTERNS):
                    continue
                if any(pattern.search(clause) for pattern in PROMOTION_PATTERNS):
                    claims.append(clause.strip())
    return claims


def validate_relative_links(errors: list[str]) -> None:
    link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    image_pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    for path in text_files():
        if path.suffix.lower() != ".md":
            continue
        content = path.read_text(encoding="utf-8")
        for target in link_pattern.findall(content) + image_pattern.findall(content):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(errors, f"{path.relative_to(ROOT)}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                fail(errors, f"{path.relative_to(ROOT)}: missing relative link target: {target}")


def validate_visual_assets(errors: list[str]) -> None:
    preview = ROOT / "assets/social-preview.png"
    try:
        content = preview.read_bytes()
    except OSError as exc:
        fail(errors, f"cannot read social preview: {exc}")
        return
    if len(content) >= 1_000_000:
        fail(errors, f"social preview must remain under 1 MB, got {len(content)} bytes")
    if content[:8] != b"\x89PNG\r\n\x1a\n" or len(content) < 24:
        fail(errors, "social preview must be a valid PNG")
        return
    width = int.from_bytes(content[16:20], "big")
    height = int.from_bytes(content[20:24], "big")
    if width < 640 or height < 320:
        fail(errors, f"social preview is too small: {width}x{height}")
    if width != height * 2:
        fail(errors, f"social preview must use a 2:1 aspect ratio, got {width}x{height}")


def validate_readme(errors: list[str]) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    rendered = re.sub(r"<[^>]+>", " ", readme)
    rendered = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", rendered)
    rendered = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", rendered)
    words = re.findall(r"\b[\w'-]+\b", rendered)
    if not 500 <= len(words) <= 900:
        fail(errors, f"README word count must be 500-900, got {len(words)}")
    if CANONICAL_DOWNLOAD not in readme:
        fail(errors, "README must contain the canonical download URL")
    if "closed-source" not in readme.lower():
        fail(errors, "README must state that MacBaram is closed-source")


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    validate_public_facts(errors)
    validate_content(errors)
    validate_roadmap_boundaries(errors)
    validate_relative_links(errors)
    validate_visual_assets(errors)
    validate_readme(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Public documentation validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
