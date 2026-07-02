from __future__ import annotations

import base64
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CUSTOM = ROOT / "dist" / "natdropp-home-custom-liquid.liquid"
ASSETS = ROOT / "Assets"


CRITICAL_ASSETS = {
    "nd_logo_url": ("nd-logo.svg", "image/svg+xml"),
    "nd_pack_hero_url": ("nd-pack-hero.webp", "image/webp"),
    "nd_olive_photo_url": ("nd-olive-photo.webp", "image/webp"),
    "nd_coconut_photo_url": ("nd-coconut-photo.webp", "image/webp"),
    "nd_vitamin_photo_url": ("nd-vitamin-photo.webp", "image/webp"),
    "nd_single_leaf_1_url": ("nd-single-leaf-1.webp", "image/webp"),
    "nd_single_leaf_2_url": ("nd-single-leaf-2.webp", "image/webp"),
    "nd_single_leaf_3_url": ("nd-single-leaf-3.webp", "image/webp"),
    "nd_single_leaf_4_url": ("nd-single-leaf-4.webp", "image/webp"),
}


def data_uri(file_name: str, mime: str) -> str:
    raw = (ASSETS / file_name).read_bytes()
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def main() -> None:
    content = CUSTOM.read_text(encoding="utf-8")
    for assign_name, (file_name, mime) in CRITICAL_ASSETS.items():
        replacement = "{% assign " + assign_name + " = '" + data_uri(file_name, mime) + "' %}"
        pattern = r"\{% assign " + re.escape(assign_name) + r" = '[^']*' %\}"
        content, count = re.subn(pattern, replacement, content, count=1)
        if count == 0:
            continue
    CUSTOM.write_text(content, encoding="utf-8")
    print(CUSTOM.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
