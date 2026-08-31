"""Prove the Tsubaki repair changes only the known uniform alpha island.

Build a fresh paired replay from the same live inputs: one output bypasses only
the interior-alpha promotion, while the other uses the production builder
unchanged. Compare their exact pixel delta with the detector-selected legacy
component, then prove the fresh repaired bytes match staging, canonical, and
installed production layers.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools import process_tsubaki_face_patches as builder  # noqa: E402


PRE_NORMALIZATION_ROOT = (
    PROJECT_ROOT
    / "tmp"
    / "tsubaki_expression_revision"
    / "pre_normalization_output"
)
REPLAYED_REPAIRED_ROOT = (
    PROJECT_ROOT
    / "tmp"
    / "tsubaki_expression_revision"
    / "replayed_repaired_output"
)
REPAIRED_ROOT = (
    PROJECT_ROOT / "tmp" / "tsubaki_expression_revision" / "repaired_output"
)
CANONICAL_ROOT = PROJECT_ROOT / "tmp" / "tsubaki_face_patch" / "output"
PRODUCTION_ROOT = (
    PROJECT_ROOT / "game" / "assets" / "characters" / "tsubaki"
)

UNIFORM_TOKENS = set(builder.EXPRESSIONS) - {"neut"}
EXPECTED_CHANGED = {f"face_{token}_uniform.png" for token in UNIFORM_TOKENS}
EXPECTED_NAMES = {
    f"face_{token}_{outfit}.png"
    for token in builder.EXPRESSIONS
    for outfit in builder.OUTFITS
}
EXPECTED_BBOX = [489, 402, 506, 418]
EXPECTED_PIXELS = 220


def build_fresh_pair() -> np.ndarray:
    """Build bypassed and repaired outputs and return the detected old island."""

    original_normalizer = builder.normalize_interior_partial_alpha
    original_expected = {
        outfit: [dict(item) for item in repairs]
        for outfit, repairs in builder.EXPECTED_INTERIOR_PARTIAL_REPAIRS.items()
    }
    original_argv = sys.argv[:]
    captured_components: list[tuple[np.ndarray, dict[str, object]]] = []

    def passthrough_normalization(
        alpha: np.ndarray,
        center: tuple[float, float],
    ) -> tuple[np.ndarray, dict[str, object]]:
        """Return the legacy mask and capture its detector-selected island."""

        candidates, considered = builder.interior_partial_alpha_components(
            alpha, center
        )
        captured_components.extend(
            (component.copy(), dict(metadata))
            for component, metadata in candidates
        )
        remaining = [dict(metadata) for _, metadata in candidates]
        partial = int(((alpha > 0) & (alpha < 255)).sum())
        visible = int((alpha > 0).sum())
        return alpha.copy(), {
            "considered_components": considered,
            "promoted_components": 0,
            "promoted_pixels": 0,
            "changed_pixels": 0,
            "visible_pixels_before": visible,
            "visible_pixels_after": visible,
            "partial_pixels_before": partial,
            "partial_pixels_after": partial,
            "components": [],
            "remaining_components": remaining,
        }

    try:
        builder.normalize_interior_partial_alpha = passthrough_normalization
        builder.EXPECTED_INTERIOR_PARTIAL_REPAIRS.clear()
        builder.EXPECTED_INTERIOR_PARTIAL_REPAIRS.update(
            {outfit: [] for outfit in builder.OUTFITS}
        )
        sys.argv = [
            str(Path(__file__).resolve()),
            "--output-dir",
            str(PRE_NORMALIZATION_ROOT),
        ]
        if builder.main() != 0:
            raise RuntimeError("pre-normalization baseline build failed")
    finally:
        builder.normalize_interior_partial_alpha = original_normalizer
        builder.EXPECTED_INTERIOR_PARTIAL_REPAIRS.clear()
        builder.EXPECTED_INTERIOR_PARTIAL_REPAIRS.update(original_expected)
        sys.argv = original_argv

    try:
        sys.argv = [
            str(Path(__file__).resolve()),
            "--output-dir",
            str(REPLAYED_REPAIRED_ROOT),
        ]
        if builder.main() != 0:
            raise RuntimeError("fresh repaired replay build failed")
    finally:
        sys.argv = original_argv

    if len(captured_components) != 1:
        raise RuntimeError(
            "expected exactly one detector-selected legacy component, got "
            f"{len(captured_components)}"
        )
    component, metadata = captured_components[0]
    identity = {
        "bbox": metadata.get("bbox"),
        "pixels": metadata.get("pixels"),
    }
    expected_identity = {"bbox": EXPECTED_BBOX, "pixels": EXPECTED_PIXELS}
    if identity != expected_identity or int(component.sum()) != EXPECTED_PIXELS:
        raise RuntimeError(
            "detector-selected legacy component mismatch: "
            f"metadata={identity} mask_pixels={int(component.sum())}"
        )
    return component


def rgba(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        return np.asarray(image.convert("RGBA"), dtype=np.uint8)


def main() -> int:
    expected_component = build_fresh_pair()

    names = {
        path.name for path in REPLAYED_REPAIRED_ROOT.glob("face_*.png")
    }
    if names != EXPECTED_NAMES:
        missing = sorted(EXPECTED_NAMES - names)
        extra = sorted(names - EXPECTED_NAMES)
        print(
            "ERROR: fresh repaired inventory mismatch "
            f"missing={missing} extra={extra}"
        )
        return 1
    pre_names = {
        path.name for path in PRE_NORMALIZATION_ROOT.glob("face_*.png")
    }
    if pre_names != EXPECTED_NAMES:
        missing = sorted(EXPECTED_NAMES - pre_names)
        extra = sorted(pre_names - EXPECTED_NAMES)
        print(
            "ERROR: bypassed inventory mismatch "
            f"missing={missing} extra={extra}"
        )
        return 1

    changed: list[str] = []
    bad: list[str] = []

    for name in sorted(names):
        old = rgba(PRE_NORMALIZATION_ROOT / name)
        new = rgba(REPLAYED_REPAIRED_ROOT / name)
        channel_delta = old != new
        pixel_delta = np.any(channel_delta, axis=2)
        alpha_delta = channel_delta[:, :, 3]
        changed_pixels = int(pixel_delta.sum())
        rgb_pixels = int(np.any(channel_delta[:, :, :3], axis=2).sum())
        alpha_pixels = int(alpha_delta.sum())
        support_delta = int(
            np.logical_xor(old[:, :, 3] > 0, new[:, :, 3] > 0).sum()
        )
        alpha_decreases = int((new[:, :, 3] < old[:, :, 3]).sum())
        new_alpha_values = (
            np.unique(new[:, :, 3][alpha_delta]).tolist()
            if alpha_pixels
            else []
        )

        bbox: list[int] | None = None
        if changed_pixels:
            changed.append(name)
            yy, xx = np.nonzero(pixel_delta)
            bbox = [
                int(xx.min()),
                int(yy.min()),
                int(xx.max()) + 1,
                int(yy.max()) + 1,
            ]
            print(
                f"{name}: bbox={bbox} pixels={changed_pixels} "
                f"rgb={rgb_pixels} alpha={alpha_pixels} "
                f"support={support_delta} decreases={alpha_decreases} "
                f"values={new_alpha_values}"
            )

        expected_delta = name in EXPECTED_CHANGED
        exact_repair = (
            bbox == EXPECTED_BBOX
            and changed_pixels == EXPECTED_PIXELS
            and rgb_pixels == 0
            and alpha_pixels == EXPECTED_PIXELS
            and support_delta == 0
            and alpha_decreases == 0
            and new_alpha_values == [255]
            and np.array_equal(pixel_delta, expected_component)
        )
        if (expected_delta and not exact_repair) or (
            not expected_delta and changed_pixels
        ):
            bad.append(name)

        repaired_bytes = (REPLAYED_REPAIRED_ROOT / name).read_bytes()
        for label, root in (
            ("staging", REPAIRED_ROOT),
            ("canonical", CANONICAL_ROOT),
            ("production", PRODUCTION_ROOT),
        ):
            if (root / name).read_bytes() != repaired_bytes:
                bad.append(f"{name}:{label}")

    print(
        f"files={len(names)} changed={len(changed)} "
        f"unchanged={len(names) - len(changed)} bad={bad}"
    )
    if bad or set(changed) != EXPECTED_CHANGED:
        return 1
    print(
        "PASS: a fresh paired replay proves only the 20 non-neutral uniform "
        "layers change; each delta exactly matches the detector-selected "
        "220-pixel legacy component and promotes its alpha to 255 with RGB "
        "and visible support intact. Fresh repaired, staging, canonical, and "
        "production PNG bytes all match."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
