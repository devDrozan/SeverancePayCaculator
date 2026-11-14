#!/usr/bin/env python3
"""Check the static policy and fail closed before a manually approved deployment."""
import argparse
import hashlib
import json
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "privacy-site"


class PolicyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.dates = []
        self.errors = []
        self.draft = False
        self.interim = False
        self.h1 = 0
        self.csp = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag in {"script", "iframe", "form", "object", "embed", "video", "audio"}:
            self.errors.append(f"Unexpected active/embedded content: {tag}")
        if any(key.startswith("on") for key in attributes):
            self.errors.append("Inline event handler found")
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if "data-publication-draft" in attributes:
            self.draft = True
        if attributes.get("data-publication-status") == "interim":
            self.interim = True
        if tag == "h1":
            self.h1 += 1
        if tag == "time":
            self.dates.append(attributes.get("datetime", ""))
        if tag == "meta" and attributes.get("http-equiv", "").lower() == "content-security-policy":
            self.csp = "default-src 'none'" in attributes.get("content", "")
        if tag == "a":
            self.links.append(attributes.get("href", ""))
        if tag == "link" and (attributes.get("rel") != "stylesheet" or attributes.get("href") != "./styles.css"):
            self.errors.append("Only the local stylesheet is allowed")
        if "src" in attributes:
            self.errors.append("Unexpected asset request; review before changing this restriction")


def content_digest():
    digest = hashlib.sha256()
    for name in ("index.html", "styles.css", ".nojekyll"):
        digest.update(name.encode() + b"\0" + (SITE / name).read_bytes() + b"\0")
    return digest.hexdigest()


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--release", action="store_true", help="Require reviewed, approved final content")
    args = cli.parse_args()
    html = (SITE / "index.html").read_text()
    css = (SITE / "styles.css").read_text()
    status = json.loads((ROOT / "compliance/privacy-publication.json").read_text())
    parser = PolicyParser()
    parser.feed(html)
    errors = parser.errors
    if len(set(parser.ids)) != len(parser.ids):
        errors.append("Duplicate HTML IDs")
    if parser.h1 != 1 or not parser.csp:
        errors.append("Expected one main heading and a restrictive CSP")
    for link in parser.links:
        if link.startswith("#"):
            if link[1:] not in parser.ids:
                errors.append(f"Missing anchor target: {link}")
        elif not link.startswith(("https://", "mailto:")):
            errors.append(f"Unexpected link scheme: {link}")
    email = status.get("contactEmail", "")
    if not re.fullmatch(r"[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+", email) or f'mailto:{email}' not in parser.links:
        errors.append("Missing or inconsistent public contact email")
    if status.get("proposedEffectiveDate") not in parser.dates:
        errors.append("Effective date and review metadata disagree")
    for value in parser.dates:
        try:
            date.fromisoformat(value)
        except ValueError:
            errors.append("Invalid effective date")
    if re.search(r"@import|url\s*\(", css, re.I):
        errors.append("Stylesheet can request another resource")
    for required in ("https://policies.google.com/privacy", "https://policies.google.com/technologies/ads"):
        if required not in parser.links:
            errors.append(f"Required Google link missing: {required}")
    digest = content_digest()
    if args.release:
        if status.get("approved") is not True:
            errors.append("Owner content approval has not been recorded")
        if parser.draft or re.search(r"\bdraft\b", html, re.I):
            errors.append("Unresolved draft/publication text remains")
        interim_authorized = (status.get("publicationMode") == "interim"
                              and status.get("interimPublicationAuthorized") is True
                              and status.get("appReleaseReady") is False and parser.interim)
        if status.get("publicationMode") == "interim" and not interim_authorized:
            errors.append("Interim publication needs explicit authorization and a visible interim notice")
        if status.get("openItems") != [] and not interim_authorized:
            errors.append("Publication review items remain unresolved")
        if status.get("approvedContentSha256") != digest:
            errors.append("Current HTML/CSS do not match the approved content digest")
    if errors:
        print("Privacy site check failed:\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1
    print(f"Privacy site {'release' if args.release else 'draft'} checks passed.")
    print(f"Content SHA-256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
