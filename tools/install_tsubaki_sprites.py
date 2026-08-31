#!/usr/bin/env python3
"""Install the reviewed Himeko/Asahina-style Tsubaki face-plate bank.

This compatibility entry point deliberately installs only an already-built,
validated oval bank. Use ``build_tsubaki_faceplates.py build`` and ``review``
first so production can never be refreshed from the retired skin-stencil
pipeline by accident.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import build_tsubaki_faceplates as faceplates


# Kept as a narrow compatibility surface for the isolated render-probe builder.
DESTINATION = faceplates.ASSET_DIR


def production_manifest() -> dict[str, Path]:
    return {
        name: faceplates.DEFAULT_STAGING / "built" / name
        for name in faceplates.expected_face_names()
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--staging",
        type=Path,
        default=faceplates.DEFAULT_STAGING,
        help="Reviewed oval build directory (default: %(default)s)",
    )
    return parser.parse_args()


def main() -> int:
    staging = parse_args().staging.resolve()
    faceplates.raise_validation(faceplates.validate(staging))
    installed = faceplates.install(staging)
    faceplates.raise_validation(faceplates.validate(staging, installed=True))
    print(f"Installed and verified {len(installed)} Tsubaki oval face layers")
    print(f"Pre-install backup: {staging / 'pre_install_backup'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
