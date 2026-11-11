#!/usr/bin/env bash
# Regenerate the Astryx CSS used by the site (run from repo root; needs Node/npm).
#   1) theme:  _src/kn2p-theme.ts  -> assets/css/kn2p-theme.css   (astryx theme build)
#   2) tokens: @astryxdesign/core dist/astryx.css :root blocks -> assets/css/astryx-tokens.css
#   3) reset:  @astryxdesign/core src/reset.css -> assets/css/astryx-reset.css
set -euo pipefail
VER="${ASTRYX_VERSION:-0.7.13}"
ROOT="$(pwd)"
TMP="$(mktemp -d)"
cp _src/kn2p-theme.ts "$TMP/kn2p-theme.ts"
cd "$TMP"
npm init -y >/dev/null
npm i -s "@astryxdesign/core@$VER" "@astryxdesign/cli@$VER" @stylexjs/stylex react@19 react-dom@19
npx astryx theme build kn2p-theme.ts --out out/kn2p-theme.css
CORE=node_modules/@astryxdesign/core
{
  echo "/* Copyright (c) Meta Platforms, Inc. and affiliates. MIT License."
  echo " * Base design tokens extracted from @astryxdesign/core@$VER dist/astryx.css (:root blocks only)."
  echo " * Regenerate with _src/build_astryx_tokens.sh — do not edit by hand. */"
  echo "@layer reset, astryx-base, astryx-theme;"
  echo "@layer astryx-base {"
  grep -E '^\s*:root, \.[a-z0-9]+\{' "$CORE/dist/astryx.css" | sed -E 's/^\s*:root, \.[a-z0-9]+\{/  :root{/'
  echo "}"
} > "$ROOT/assets/css/astryx-tokens.css"
cp "$CORE/src/reset.css" "$ROOT/assets/css/astryx-reset.css"
sed 's#Source: kn2p-theme.ts#Source: _src/kn2p-theme.ts#;s#--out out/kn2p-theme.css#--out assets/css/kn2p-theme.css#' out/kn2p-theme.css > "$ROOT/assets/css/kn2p-theme.css"
echo "done: assets/css/{kn2p-theme,astryx-tokens,astryx-reset}.css"
