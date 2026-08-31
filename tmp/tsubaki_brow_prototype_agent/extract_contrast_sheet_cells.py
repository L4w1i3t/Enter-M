"""Extract native 2x current/fixed cells from the shared contrast-reject audit.

This is staging-only diagnostic code. It does not touch production assets.
"""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tmp" / "tsubaki_brow_diagnosis" / "contrast_reject"
OUTPUT = ROOT / "tmp" / "tsubaki_brow_prototype_agent" / "contrast_cells"
EXPRESSIONS = (
    "happy", "smug", "teasing", "thinking",
    "curious", "unamused", "annoyed", "frustrated",
    "angry", "sad", "crying", "embarrassed",
    "nervous", "worried", "shocked", "afraid",
    "panicked", "determined", "empty", "disgusted",
)
CELL_WIDTH = 490
CELL_HEIGHT = 268
IMAGE_HEIGHT = 230


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for outfit in ("uniform", "casual"):
        sheet = Image.open(SOURCE / f"{outfit}_thresholds.png").convert("RGB")
        extracted: dict[tuple[str, str], Image.Image] = {}
        for index, expression in enumerate(EXPRESSIONS):
            x = (index % 4) * CELL_WIDTH
            pair_row = index // 4
            for variant_index, variant in enumerate(("current", "fixed")):
                y = (pair_row * 2 + variant_index) * CELL_HEIGHT
                cell = sheet.crop((x, y, x + CELL_WIDTH, y + IMAGE_HEIGHT))
                cell.save(OUTPUT / f"{outfit}_{expression}_{variant}.png", optimize=True)
                extracted[(expression, variant)] = cell

        for group_index in range(4):
            names = EXPRESSIONS[group_index * 5 : group_index * 5 + 5]
            montage = Image.new(
                "RGB", (CELL_WIDTH * 2, (IMAGE_HEIGHT + 26) * len(names)), (22, 24, 28)
            )
            draw = ImageDraw.Draw(montage)
            for row, expression in enumerate(names):
                y = row * (IMAGE_HEIGHT + 26)
                montage.paste(extracted[(expression, "current")], (0, y))
                montage.paste(extracted[(expression, "fixed")], (CELL_WIDTH, y))
                draw.text(
                    (6, y + IMAGE_HEIGHT + 4),
                    f"{expression}: current",
                    fill=(245, 245, 248),
                )
                draw.text(
                    (CELL_WIDTH + 6, y + IMAGE_HEIGHT + 4),
                    f"{expression}: contrast reject",
                    fill=(245, 245, 248),
                )
            montage.save(OUTPUT / f"{outfit}_audit_{group_index + 1}.png", optimize=True)


if __name__ == "__main__":
    main()
