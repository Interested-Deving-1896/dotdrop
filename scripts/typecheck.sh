#!/usr/bin/env bash
# Run strict static type checks for the project.

set -euo pipefail

cur="$(cd "$(dirname "$0")/.." && pwd)"
cd "${cur}"

DEFAULT_TARGETS=(dotdrop)
TARGETS=()

if [[ "$#" -gt 0 ]]; then
  TARGETS=("$@")
else
  TARGETS=("${DEFAULT_TARGETS[@]}")
fi

echo "[typecheck] running mypy (strict) on: ${TARGETS[*]}"
mypy --strict "${TARGETS[@]}"

echo "[typecheck] running pytype on: ${TARGETS[*]}"
pytype -V 3.11 -j auto -k "${TARGETS[@]}"

echo "[typecheck] running pyright on: ${TARGETS[*]}"
pyright "${TARGETS[@]}"

echo "[typecheck] completed"
