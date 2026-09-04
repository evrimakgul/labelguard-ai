"""Generate deterministic label fixtures with embedded demo-provider OCR text."""

from __future__ import annotations

import shutil
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from PIL.PngImagePlugin import PngInfo

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "labels"
PUBLIC_DIR = ROOT / "apps" / "web" / "public" / "demo-labels"
WARNING = (
    "GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink "
    "alcoholic beverages during pregnancy because of the risk of birth defects. "
    "(2) Consumption of alcoholic beverages impairs your ability to drive a car or operate "
    "machinery, and may cause health problems."
)
CASES = {
    "demo-pass.png": {
        "brand": "OLD TOM DISTILLERY",
        "class_type": "KENTUCKY STRAIGHT BOURBON WHISKEY",
        "abv": "45% ALC./VOL. (90 PROOF)",
        "volume": "750 mL",
        "warning": WARNING,
    },
    "demo-brand-mismatch.png": {
        "brand": "ACME SPIRITS",
        "class_type": "KENTUCKY STRAIGHT BOURBON WHISKEY",
        "abv": "45% ALC./VOL. (90 PROOF)",
        "volume": "750 mL",
        "warning": WARNING,
    },
    "demo-abv-mismatch.png": {
        "brand": "OLD TOM DISTILLERY",
        "class_type": "KENTUCKY STRAIGHT BOURBON WHISKEY",
        "abv": "40% ALC./VOL. (80 PROOF)",
        "volume": "750 mL",
        "warning": WARNING,
    },
    "demo-warning-error.png": {
        "brand": "OLD TOM DISTILLERY",
        "class_type": "KENTUCKY STRAIGHT BOURBON WHISKEY",
        "abv": "45% ALC./VOL. (90 PROOF)",
        "volume": "750 mL",
        "warning": WARNING.replace("GOVERNMENT WARNING", "Government Warning").replace(
            "machinery,", "machinery"
        ),
    },
    "demo-rotated.png": {
        "brand": "OLD TOM DISTILLERY",
        "class_type": "KENTUCKY STRAIGHT BOURBON WHISKEY",
        "abv": "45% ALC./VOL. (90 PROOF)",
        "volume": "750 mL",
        "warning": WARNING,
        "effect": "rotated",
    },
    "demo-low-contrast.png": {
        "brand": "OLD TOM DISTILLERY",
        "class_type": "KENTUCKY STRAIGHT BOURBON WHISKEY",
        "abv": "45% ALC./VOL. (90 PROOF)",
        "volume": "750 mL",
        "warning": WARNING,
        "effect": "low_contrast",
    },
}


def load_font(
    size: int, bold: bool = False
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    candidates = [
        Path("C:/Windows/Fonts") / filename,
        Path(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default(size=size)


def render_case(name: str, data: dict[str, str]) -> Path:
    image = Image.new("RGB", (1200, 1000), "#f3ead5")
    draw = ImageDraw.Draw(image)
    navy = "#142b42"
    copper = "#a66032"
    draw.rounded_rectangle((45, 45, 1155, 955), radius=26, outline=navy, width=6)
    draw.rounded_rectangle((68, 68, 1132, 932), radius=18, outline=copper, width=2)
    draw.text(
        (600, 115), data["brand"], font=load_font(54, True), fill=navy, anchor="ma"
    )
    draw.line((240, 183, 960, 183), fill=copper, width=3)
    draw.text(
        (600, 222), data["class_type"], font=load_font(29), fill=navy, anchor="ma"
    )
    draw.text((600, 330), data["abv"], font=load_font(31, True), fill=navy, anchor="ma")
    draw.text((600, 390), data["volume"], font=load_font(28), fill=navy, anchor="ma")
    draw.text(
        (600, 475),
        "DISTILLED AND BOTTLED IN THE USA",
        font=load_font(19),
        fill="#52606d",
        anchor="ma",
    )

    warning_lines = textwrap.wrap(data["warning"], width=84)
    y = 605
    for index, line in enumerate(warning_lines):
        is_heading = index == 0 and line.startswith("GOVERNMENT WARNING")
        draw.text((115, y), line, font=load_font(20, is_heading), fill=navy)
        y += 34

    metadata_lines = [data["brand"], data["class_type"], data["abv"], data["volume"]]
    metadata_lines.extend(warning_lines)
    if data.get("effect") == "rotated":
        image = image.rotate(4, resample=Image.Resampling.BICUBIC, fillcolor="#f3ead5")
    elif data.get("effect") == "low_contrast":
        image = ImageEnhance.Contrast(image).enhance(0.18)
    metadata = PngInfo()
    metadata.add_text("labelguard_ocr", "\n".join(metadata_lines))
    path = FIXTURE_DIR / name
    image.save(path, format="PNG", optimize=True, pnginfo=metadata)
    return path


def main() -> None:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    for name, data in CASES.items():
        source = render_case(name, data)
        shutil.copy2(source, PUBLIC_DIR / name)

    with Image.open(FIXTURE_DIR / "demo-pass.png") as source:
        unreadable = source.convert("RGB").filter(ImageFilter.GaussianBlur(20))
    unreadable = ImageEnhance.Contrast(unreadable).enhance(0.08)
    unreadable_path = FIXTURE_DIR / "demo-unreadable.png"
    unreadable.save(unreadable_path, format="PNG", optimize=True)
    shutil.copy2(unreadable_path, PUBLIC_DIR / unreadable_path.name)


if __name__ == "__main__":
    main()
