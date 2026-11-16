# -*- coding: utf-8 -*-
"""Allowlist HTML cleaner for microCMS rich-text bodies (standard library only).

Keeps document structure (headings, lists, tables, links, images, emphasis) and
drops everything else: scripts, styles, iframes, event handlers, classes and
inline styles other than text-align. <h1> becomes <h2> because the page title
is the only <h1>.
"""
import html
import re
from html.parser import HTMLParser

TAGS = {
    "h2", "h3", "h4", "h5", "h6", "p", "br", "hr", "strong", "b", "em", "i", "u", "s",
    "sup", "sub", "code", "pre", "blockquote", "ul", "ol", "li", "a", "img", "figure",
    "figcaption", "table", "thead", "tbody", "tfoot", "tr", "th", "td", "caption", "span", "div",
}
RENAME = {"h1": "h2", "strike": "s", "del": "s"}
DROP_WITH_CONTENT = {"script", "style", "iframe", "object", "embed", "noscript", "template", "svg", "math", "form"}
VOID = {"br", "hr", "img"}
IMPLIED = {"li": {"li", "p"}, "p": {"p"}, "tr": {"tr", "td", "th"}, "td": {"td", "th"}, "th": {"td", "th"}}
ATTRS = {
    "*": {"id", "style"},
    "a": {"href", "title"},
    "img": {"src", "alt", "width", "height"},
    "th": {"colspan", "rowspan", "scope"},
    "td": {"colspan", "rowspan"},
    "ol": {"start", "type"},
}
SAFE_URL = re.compile(r"^(https?:|mailto:|tel:|#|/)", re.I)
TEXT_ALIGN = re.compile(r"text-align\s*:\s*(left|right|center|justify)", re.I)


class _Cleaner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0  # depth inside a DROP_WITH_CONTENT element
        self.stack = []

    def _attrs(self, tag, attrs):
        allowed = ATTRS["*"] | ATTRS.get(tag, set())
        parts = []
        for k, v in attrs:
            k = k.lower()
            v = v or ""
            if k not in allowed:
                continue
            if k in ("href", "src") and not SAFE_URL.match(v.strip()):
                continue
            if k == "style":
                m = TEXT_ALIGN.search(v)
                if not m:
                    continue
                v = f"text-align:{m.group(1).lower()}"
            parts.append(f' {k}="{html.escape(v, quote=True)}"')
        if tag == "a" and any(k == "href" and re.match(r"https?:", (v or ""), re.I) for k, v in attrs):
            parts.append(' target="_blank" rel="noopener"')
        if tag == "img":
            parts.append(' loading="lazy"')
        return "".join(parts)

    def handle_starttag(self, tag, attrs):
        tag = RENAME.get(tag, tag)
        if tag in DROP_WITH_CONTENT:
            if tag not in VOID:
                self.skip += 1
            return
        if self.skip or tag not in TAGS:
            return
        # implied end tags (<li>a<li>b, <p>a<p>b) so loose markup does not nest
        if tag in IMPLIED and self.stack and self.stack[-1] in IMPLIED[tag]:
            self.out.append(f"</{self.stack.pop()}>")
        self.out.append(f"<{tag}{self._attrs(tag, attrs)}>")
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        tag = RENAME.get(tag, tag)
        if self.skip or tag not in TAGS:
            return
        self.out.append(f"<{tag}{self._attrs(tag, attrs)}>")
        if tag not in VOID:
            self.out.append(f"</{tag}>")

    def handle_endtag(self, tag):
        tag = RENAME.get(tag, tag)
        if tag in DROP_WITH_CONTENT:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag not in TAGS or tag in VOID or tag not in self.stack:
            return
        while self.stack:  # close anything left open inside it
            t = self.stack.pop()
            self.out.append(f"</{t}>")
            if t == tag:
                break

    def handle_data(self, data):
        if not self.skip:
            self.out.append(html.escape(data, quote=False))

    def close(self):
        super().close()
        while self.stack:
            self.out.append(f"</{self.stack.pop()}>")
        return "".join(self.out)


def clean_html(raw):
    c = _Cleaner()
    c.feed(raw or "")
    return c.close()
