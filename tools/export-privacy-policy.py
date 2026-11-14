#!/usr/bin/env python3
"""Export the canonical policy HTML to the full, readable Markdown approval copy."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


class PolicyText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.parts = []
        self.links = []
        self.table = False
        self.rows = []
        self.row = []
        self.cell = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "article" and attributes.get("class") == "policy":
            self.active = True
            return
        if not self.active:
            return
        if tag == "table":
            self.table = True
            self.rows = []
        if self.table:
            if tag == "tr":
                self.row = []
            if tag in {"th", "td"}:
                self.cell = []
            return
        if tag in {"p", "section"}:
            self.parts.append("\n\n")
        elif tag == "h2":
            self.parts.append("\n\n## ")
        elif tag == "h3":
            self.parts.append("\n\n### ")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "strong":
            self.parts.append("**")
        elif tag == "code":
            self.parts.append("`")
        elif tag == "a":
            self.links.append(attributes["href"])
            self.parts.append("[")
        elif tag == "br":
            self.parts.append("  \n")

    def handle_endtag(self, tag):
        if not self.active:
            return
        if self.table:
            if tag in {"th", "td"}:
                self.row.append(" ".join("".join(self.cell or []).split()).replace("|", "\\|"))
                self.cell = None
            elif tag == "tr":
                self.rows.append(self.row)
            elif tag == "table":
                self.table = False
                self.parts.append("\n\n")
                for index, row in enumerate(self.rows):
                    self.parts.append("| " + " | ".join(row) + " |\n")
                    if index == 0:
                        self.parts.append("| " + " | ".join("---" for _ in row) + " |\n")
            return
        if tag == "article":
            self.active = False
        elif tag in {"h2", "h3", "p", "section", "ul"}:
            self.parts.append("\n\n")
        elif tag == "strong":
            self.parts.append("**")
        elif tag == "code":
            self.parts.append("`")
        elif tag == "a":
            self.parts.append("](" + self.links.pop() + ")")

    def handle_data(self, data):
        if not self.active:
            return
        if self.table:
            if self.cell is not None:
                self.cell.append(data)
        elif data.strip():
            self.parts.append(re.sub(r"\s+", " ", data))


def main():
    status = json.loads((ROOT / "compliance/privacy-publication.json").read_text())
    parser = PolicyText()
    parser.feed((ROOT / "privacy-site/index.html").read_text())
    body = re.sub(r"\n{3,}", "\n\n", "".join(parser.parts)).strip()
    header = (
        "# E9 Mate Myanmar — Privacy Policy\n\n"
        + ("> **Approved interim notice.** Open items remain disclosed; this is not app-release approval.\n\n"
           if status.get('approved') and status.get('publicationMode') == 'interim'
           else "> **Review copy — not approved or effective.** Owner confirmations and app-release checks remain open.\n\n")
        + f"**Effective date:** {status['proposedEffectiveDate']}  \n"
        "**Android package:** `com.e9mate.myanmar`  \n"
        f"**Privacy contact:** {status['contactEmail']}\n\n"
        "This is the full readable export of [the canonical policy website](privacy-site/index.html). "
        "Generated with `python3 tools/export-privacy-policy.py`; edit the HTML rather than this copy.\n\n"
    )
    notes = (
        "\n\n---\n\n"
        "**Approval notes (not part of the policy):** "
        "[Owner confirmations](compliance/owner-inputs.md) · "
        "[Source review](compliance/privacy-review-2026-11-09.md) · "
        "[Google Play checklist](compliance/google-play-checklist.md) · "
        "[AdMob checklist](compliance/admob-checklist.md) · "
        "[Deployment setup](privacy-site/README.md). "
        "Publication authorization is recorded separately in the publication metadata; generating this copy does not authorize future changes.\n"
    )
    (ROOT / "Privacy_Policy_Draft.md").write_text(header + body + notes)
    print("Updated the full Privacy_Policy_Draft.md review copy from canonical HTML.")


if __name__ == "__main__":
    main()
