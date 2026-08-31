#!/usr/bin/env python3
"""Compatibility entry point for Tsubaki's replacement oval-face build.

The former schema-v5 skin stencil is intentionally retired. Running this
script now rebuilds and validates the broad geometric face plates used by the
canonical ``build_tsubaki_faceplates.py`` pipeline; it cannot regenerate the
obsolete sparse masks.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import build_tsubaki_faceplates as faceplates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--staging",
        type=Path,
        default=faceplates.DEFAULT_STAGING,
        help="Oval build directory (default: %(default)s)",
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="Also regenerate the visual review sheets",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    staging = args.staging.resolve()
    print(f"Built: {faceplates.build(staging)}")
    faceplates.raise_validation(faceplates.validate(staging))
    print("Validated: 42 broad oval face layers")
    if args.review:
        for output in faceplates.review(staging):
            print(f"Review: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
