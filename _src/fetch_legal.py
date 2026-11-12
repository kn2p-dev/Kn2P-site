#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download the MoriPay legal documents from microCMS into _src/legal/*.json.

    MICROCMS_API_KEY=... python3 _src/fetch_legal.py
    python3 _src/build.py

The API key is read from the environment only (GitHub Actions secret
MICROCMS_API_KEY). Never write it into this repository.

The JSON files are committed so that `build.py` works without the key; the
pages under /legal/ are generated from them.
"""
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from content import LEGAL_DOCS, MICROCMS_ENDPOINT, MICROCMS_SERVICE  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "legal")
KEEP = ("id", "termKey", "version", "title", "body", "publishedAt", "revisedAt", "updatedAt")


def fetch(content_id, key):
    url = f"https://{MICROCMS_SERVICE}.microcms.io/api/v1/{MICROCMS_ENDPOINT}/{content_id}"
    req = urllib.request.Request(url, headers={"X-MICROCMS-API-KEY": key})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    key = os.environ.get("MICROCMS_API_KEY", "").strip()
    if not key:
        sys.exit("MICROCMS_API_KEY is not set. Add it as a GitHub Actions secret (see _src/README.md).")
    os.makedirs(OUT, exist_ok=True)
    failed, done = [], 0
    for slug, doc in LEGAL_DOCS.items():
        for lang, content_id in doc["ids"].items():
            try:
                data = fetch(content_id, key)
            except urllib.error.HTTPError as e:
                try:
                    reason = json.loads(e.read().decode("utf-8")).get("message", "")
                except Exception:
                    reason = ""
                failed.append(f"{content_id}: HTTP {e.code} {reason}".rstrip())
                continue
            except urllib.error.URLError as e:
                failed.append(f"{content_id}: {e.reason}")
                continue
            if not data.get("title") or not data.get("body"):
                failed.append(f"{content_id}: title/body empty")
                continue
            path = os.path.join(OUT, f"{slug}.{lang}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump({k: data.get(k) for k in KEEP}, f, ensure_ascii=False, indent=1)
                f.write("\n")
            done += 1
            print(f"ok   {slug}.{lang}  ({content_id}, version {data.get('version')})")
    for msg in failed:
        # GitHub Actions shows ::warning:: lines on the run summary
        print(f"::warning::microCMS {msg} (kept the previous copy, if any)")
    if not done:
        sys.exit("No document could be downloaded. Check the API key and content IDs.")


if __name__ == "__main__":
    main()
