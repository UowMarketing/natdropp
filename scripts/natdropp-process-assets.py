from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "Assets"
OUT = ROOT / "assets"
RAW = OUT / "raw"


def ensure_dirs() -> None:
    OUT.mkdir(exist_ok=True)
    RAW.mkdir(exist_ok=True)


def file_hash(path: Path) -> str:
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:10]


def first_existing(candidates: Iterable[Path]) -> Path | None:
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def copy_raw(path: Path) -> Path:
    target = RAW / path.name
    if target.exists():
        if file_hash(target) == file_hash(path):
            return target
        target = RAW / f"{path.stem}-{file_hash(path)}{path.suffix}"
    shutil.copy2(path, target)
    return target


def trim_alpha(image: Image.Image, padding: int = 16) -> Image.Image:
    if image.mode != "RGBA":
        return image
    alpha = image.getchannel("A").point(lambda value: 255 if value > 12 else 0)
    box = alpha.getbbox()
    if not box:
        return image
    left = max(0, box[0] - padding)
    top = max(0, box[1] - padding)
    right = min(image.width, box[2] + padding)
    bottom = min(image.height, box[3] + padding)
    return image.crop((left, top, right, bottom))


def load_image(path: Path, trim: bool = True) -> Image.Image:
    image = Image.open(path)
    image.load()
    if image.mode in ("P", "LA"):
        image = image.convert("RGBA")
    elif image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")
    if trim:
        image = trim_alpha(image)
    return image


def load_product_cutout(path: Path) -> Image.Image:
    image = load_image(path, trim=True).convert("RGBA")
    rgb = image.convert("RGB")
    hsv = rgb.convert("HSV")
    hue, sat, val = hsv.split()
    alpha = image.getchannel("A")
    clean = Image.new("L", image.size, 0)
    source = image.load()
    alpha_px = alpha.load()
    sat_px = sat.load()
    val_px = val.load()
    clean_px = clean.load()
    for y in range(image.height):
        for x in range(image.width):
            a = alpha_px[x, y]
            if a < 72:
                continue
            s = sat_px[x, y]
            v = val_px[x, y]
            if s > 20 or v > 166:
                clean_px[x, y] = a
            elif y < image.height * .82 and v > 112:
                clean_px[x, y] = a
    image.putalpha(clean)
    return trim_alpha(image, padding=4).convert("RGBA")


def save_webp(source: Path, target_name: str, max_side: int = 1400, quality: int = 84, trim: bool = True) -> dict:
    copy_raw(source)
    image = load_image(source, trim=trim)
    image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    target = OUT / target_name
    target.parent.mkdir(exist_ok=True)
    image.save(target, "WEBP", quality=quality, method=6)
    return asset_record(target, source)


def save_png(source: Path, target_name: str, max_side: int = 1400, trim: bool = True) -> dict:
    copy_raw(source)
    image = load_image(source, trim=trim)
    image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    target = OUT / target_name
    image.save(target, "PNG", optimize=True)
    return asset_record(target, source)


def save_transformed_webp(
    source: Path,
    target_name: str,
    max_side: int = 900,
    rotate: float = 0,
    flip: bool = False,
    quality: int = 82,
) -> dict:
    copy_raw(source)
    image = load_image(source, trim=True)
    if flip:
        image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if rotate:
        image = image.rotate(rotate, expand=True, resample=Image.Resampling.BICUBIC)
        image = trim_alpha(image)
    image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    target = OUT / target_name
    image.save(target, "WEBP", quality=quality, method=6)
    return asset_record(target, source)


def save_single_leaf_webps(source: Path) -> list[dict]:
    copy_raw(source)
    base = load_image(source, trim=False).convert("RGBA")
    crops = [
        ("nd-single-leaf-1.webp", (528, 270, 734, 402), -7, False, 220),
        ("nd-single-leaf-2.webp", (178, 512, 338, 780), 10, False, 260),
        ("nd-single-leaf-3.webp", (548, 730, 744, 838), -12, False, 190),
        ("nd-single-leaf-4.webp", (292, 330, 472, 462), 16, True, 210),
    ]
    records: list[dict] = []
    for target_name, box, rotate, flip, max_side in crops:
        image = trim_alpha(base.crop(box), padding=18).convert("RGBA")
        if flip:
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if rotate:
            image = image.rotate(rotate, expand=True, resample=Image.Resampling.BICUBIC)
            image = trim_alpha(image, padding=12).convert("RGBA")
        alpha = image.getchannel("A")
        rgb = image.convert("RGB")
        rgb = ImageEnhance.Color(rgb).enhance(.56)
        rgb = ImageEnhance.Brightness(rgb).enhance(.88)
        rgb = ImageEnhance.Contrast(rgb).enhance(.96)
        image = rgb.convert("RGBA")
        image.putalpha(alpha)
        image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
        target = OUT / target_name
        image.save(target, "WEBP", quality=82, method=6)
        records.append(asset_record(target, source))
    return records


def paste_product(canvas: Image.Image, source: Path, height: int, center_x: int, baseline: int, shadow_scale: float = 1.0) -> None:
    product = load_product_cutout(source)
    ratio = height / product.height
    product = product.resize((int(product.width * ratio), height), Image.Resampling.LANCZOS)
    x = int(center_x - product.width / 2)
    y = baseline - product.height

    shadow_pad = int(80 * shadow_scale)
    shadow_w = int(product.width * 1.18 * shadow_scale) + shadow_pad * 2
    shadow_h = int(48 * shadow_scale) + shadow_pad
    shadow = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))
    shadow_alpha = Image.new("L", (shadow_w, shadow_h), 0)
    shadow_alpha_draw = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))
    from PIL import ImageDraw

    draw = ImageDraw.Draw(shadow_alpha_draw)
    draw.ellipse((shadow_pad, int(shadow_pad * .42), shadow_w - shadow_pad, shadow_h - int(shadow_pad * .38)), fill=(31, 24, 20, 38))
    shadow_alpha_draw = shadow_alpha_draw.filter(ImageFilter.GaussianBlur(28))
    shadow.alpha_composite(shadow_alpha_draw)
    canvas.alpha_composite(shadow, (int(center_x - shadow_w / 2), baseline - int(shadow_h * .58)))

    canvas.alpha_composite(product, (x, y))


def save_pack_hero(product_1l: Path, product_500: Path, product_250: Path) -> list[dict]:
    canvas = Image.new("RGBA", (1500, 1080), (0, 0, 0, 0))

    paste_product(canvas, product_1l, 820, 502, 920, 1.15)
    paste_product(canvas, product_500, 760, 780, 920, 1.03)
    paste_product(canvas, product_250, 642, 1007, 920, .92)

    png = OUT / "nd-pack-hero.png"
    webp = OUT / "nd-pack-hero.webp"
    canvas.save(png, "PNG", optimize=True)
    canvas.save(webp, "WEBP", quality=86, method=6)
    return [asset_record(png, None), asset_record(webp, None)]


def preserve_svg(name: str) -> dict | None:
    target = OUT / name
    if not target.exists():
        return None
    copy_raw(target)
    return asset_record(target, target)


def write_svg(name: str, content: str) -> dict:
    target = OUT / name
    target.write_text(content.strip() + "\n", encoding="utf-8")
    return asset_record(target, None)


def asset_record(path: Path, source: Path | None) -> dict:
    size = None
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        with Image.open(path) as image:
            size = {"width": image.width, "height": image.height}
    return {
        "file": path.relative_to(ROOT).as_posix(),
        "source": source.relative_to(ROOT).as_posix() if source else "generated",
        "bytes": path.stat().st_size,
        "sha1": file_hash(path),
        "dimensions": size,
    }


def main() -> None:
    ensure_dirs()
    generated: list[dict] = []

    product_main = first_existing([
        SOURCE_ROOT / "prod ilustrativa.png",
        SOURCE_ROOT / "PNGS" / "prod ilustrativa.png",
        SOURCE_ROOT / "PNGS" / "prod.png",
    ])
    product_250 = first_existing([SOURCE_ROOT / "2-Photoroom.png", SOURCE_ROOT / "2.jpg"])
    product_500 = first_existing([SOURCE_ROOT / "1-Photoroom (1).png", SOURCE_ROOT / "1.jpg"])
    product_1l = first_existing([SOURCE_ROOT / "3-Photoroom.png", SOURCE_ROOT / "3.jpg"])
    lavender_1 = first_existing([SOURCE_ROOT / "lavanda 1.png", SOURCE_ROOT / "lavender-with-ai-generated-free-png-Photoroom.png"])
    lavender_2 = first_existing([SOURCE_ROOT / "lavanda 2.png", SOURCE_ROOT / "lavanda 3.png"])
    leaf = first_existing([SOURCE_ROOT / "591591-pixels-hojas-de-arbol-11563585679lindrkulsp-Photoroom.png"])
    acene = first_existing([SOURCE_ROOT / "logo-acene-certificacion-web.png", SOURCE_ROOT / "cert.png"])

    if product_main:
        generated.append(save_webp(product_main, "nd-product-main.webp", 1320, 86, True))
        generated.append(save_png(product_main, "nd-product-main.png", 1320, True))
    if product_250:
        generated.append(save_webp(product_250, "nd-product-250.webp", 1180, 84, True))
    if product_500:
        generated.append(save_webp(product_500, "nd-product-500.webp", 1180, 84, True))
    if product_1l:
        generated.append(save_webp(product_1l, "nd-product-1l.webp", 1180, 84, True))
    if product_1l and product_500 and product_250:
        generated.extend(save_pack_hero(product_1l, product_500, product_250))
    if lavender_1:
        generated.append(save_webp(lavender_1, "nd-lavender-1.webp", 900, 82, True))
    if lavender_2:
        generated.append(save_webp(lavender_2, "nd-lavender-2.webp", 900, 82, True))
    if leaf:
        generated.append(save_transformed_webp(leaf, "nd-leaf-1.webp", 760, 0, False))
        generated.append(save_transformed_webp(leaf, "nd-leaf-2.webp", 760, -16, True))
        generated.append(save_transformed_webp(leaf, "nd-leaf-3.webp", 620, 24, False))
        generated.extend(save_single_leaf_webps(leaf))
    if acene:
        generated.append(save_webp(acene, "nd-acene-badge.webp", 480, 86, True))

    generated.extend(item for item in [preserve_svg("nd-logo.svg"), preserve_svg("nd-favicon.svg")] if item)

    generated.append(write_svg("nd-liquid-ribbon.svg", """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 280" role="img" aria-label="Olive oil ribbon">
  <defs>
    <linearGradient id="oil" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#F3D36A" stop-opacity=".18"/>
      <stop offset=".45" stop-color="#D9A441" stop-opacity=".78"/>
      <stop offset="1" stop-color="#7E8B5B" stop-opacity=".22"/>
    </linearGradient>
    <filter id="soft" x="-8%" y="-20%" width="116%" height="140%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>
  <path d="M10 174C145 68 285 60 427 134c132 68 285 90 483-32" fill="none" stroke="url(#oil)" stroke-width="46" stroke-linecap="round" filter="url(#soft)"/>
  <path d="M13 171C148 76 284 73 421 141c143 71 286 72 486-34" fill="none" stroke="#D9A441" stroke-opacity=".58" stroke-width="18" stroke-linecap="round"/>
  <path d="M80 144c124-41 233-25 331 30 123 69 258 63 398-7" fill="none" stroke="#FFFFFF" stroke-opacity=".42" stroke-width="5" stroke-linecap="round"/>
</svg>
"""))
    generated.append(write_svg("nd-emulsion-drop.svg", """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 520" role="img" aria-label="Formula emulsion drop">
  <defs>
    <radialGradient id="drop" cx="46%" cy="34%" r="68%">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset=".45" stop-color="#ECE9FF"/>
      <stop offset=".78" stop-color="#C8B8FF"/>
      <stop offset="1" stop-color="#5A4FD3"/>
    </radialGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#FFFFFF" stop-opacity=".92"/>
      <stop offset="1" stop-color="#726DC9" stop-opacity=".74"/>
    </linearGradient>
  </defs>
  <path d="M211 18C277 118 357 207 357 314c0 106-64 178-146 178S65 420 65 314C65 207 146 118 211 18Z" fill="url(#drop)" opacity=".95"/>
  <path d="M211 18C277 118 357 207 357 314c0 106-64 178-146 178S65 420 65 314C65 207 146 118 211 18Z" fill="none" stroke="url(#edge)" stroke-width="8"/>
  <path d="M157 129c-42 55-62 100-61 166" fill="none" stroke="#fff" stroke-width="18" stroke-linecap="round" opacity=".54"/>
  <path d="M263 344c38-25 58-61 56-109" fill="none" stroke="#5A4FD3" stroke-width="10" stroke-linecap="round" opacity=".18"/>
</svg>
"""))
    generated.append(write_svg("nd-formula-particles.svg", """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 520" role="img" aria-label="Natural formula particles">
  <g fill="none" stroke-linecap="round">
    <path d="M72 392c76-64 142-86 224-61 73 22 128 20 197-25 46-30 93-43 150-38" stroke="#C8B8FF" stroke-width="2" opacity=".45"/>
    <path d="M142 132c84 52 161 62 251 30 84-31 151-13 227 55" stroke="#D9A441" stroke-width="2" opacity=".34"/>
  </g>
  <g fill="#D9A441" opacity=".72">
    <circle cx="115" cy="154" r="5"/><circle cx="184" cy="108" r="3"/><circle cx="643" cy="213" r="4"/><circle cx="536" cy="77" r="3"/>
  </g>
  <g fill="#5A4FD3" opacity=".5">
    <circle cx="246" cy="384" r="4"/><circle cx="415" cy="412" r="3"/><circle cx="686" cy="344" r="5"/>
  </g>
  <g fill="#7E8B5B" opacity=".45">
    <circle cx="86" cy="297" r="3"/><circle cx="331" cy="219" r="5"/><circle cx="585" cy="404" r="4"/>
  </g>
</svg>
"""))
    generated.append(write_svg("nd-botanical-shadow.svg", """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 760" role="img" aria-label="Soft botanical shadow">
  <g fill="none" stroke="#7E8B5B" stroke-linecap="round" opacity=".16">
    <path d="M360 704C334 555 340 420 392 286c29-75 32-137 8-192" stroke-width="12"/>
    <path d="M391 306c-82-26-139-67-172-124" stroke-width="7"/>
    <path d="M372 426c83-18 143-56 181-114" stroke-width="7"/>
    <path d="M350 565c-76-20-136-58-179-115" stroke-width="7"/>
    <path d="M222 185c55-16 100-7 137 26" stroke-width="5"/>
    <path d="M552 313c-52 3-92 24-122 63" stroke-width="5"/>
    <path d="M172 451c55-14 103-5 144 29" stroke-width="5"/>
  </g>
</svg>
"""))
    generated.append(write_svg("nd-multiuse-bg.svg", """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760" role="img" aria-label="Clean multiuse surface">
  <defs>
    <linearGradient id="surface" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#FFFFFF"/>
      <stop offset=".56" stop-color="#F5F5F7"/>
      <stop offset="1" stop-color="#ECE9FF"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="760" fill="url(#surface)"/>
  <path d="M-40 580C180 508 302 525 506 612c175 74 357 72 734-58" fill="none" stroke="#C8B8FF" stroke-width="2" opacity=".42"/>
  <path d="M74 151c160-32 322-21 486 35 181 61 356 65 566 7" fill="none" stroke="#7E8B5B" stroke-width="2" opacity=".18"/>
  <path d="M906 82c-39 77-41 151-5 222" fill="none" stroke="#D9A441" stroke-width="7" stroke-linecap="round" opacity=".16"/>
</svg>
"""))
    generated.append(write_svg("nd-trust-bg.svg", """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 620" role="img" aria-label="Trust background">
  <rect width="1200" height="620" fill="#FAFAF7"/>
  <g fill="none" stroke-linecap="round">
    <path d="M104 456c178-92 325-93 500-2 144 74 300 62 491-36" stroke="#5A4FD3" stroke-width="2" opacity=".22"/>
    <path d="M174 174c124-52 236-52 338 3 142 77 273 68 393-25" stroke="#7E8B5B" stroke-width="2" opacity=".24"/>
    <path d="M838 473c38-68 42-132 13-192" stroke="#D9A441" stroke-width="6" opacity=".18"/>
  </g>
</svg>
"""))
    generated.append(write_svg("nd-hero-studio.svg", """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 960" role="img" aria-label="Natdropp studio background">
  <defs>
    <radialGradient id="light" cx="58%" cy="36%" r="58%">
      <stop stop-color="#FFFFFF"/>
      <stop offset=".52" stop-color="#FAFAF7"/>
      <stop offset="1" stop-color="#F5F5F7"/>
    </radialGradient>
    <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
      <stop stop-color="#FFFFFF" stop-opacity=".82"/>
      <stop offset="1" stop-color="#ECE9FF" stop-opacity=".22"/>
    </linearGradient>
  </defs>
  <rect width="1440" height="960" fill="url(#light)"/>
  <path d="M0 704c220-76 422-90 642-42 280 61 498 42 798-86v384H0Z" fill="url(#floor)"/>
  <path d="M186 225c154-38 300-20 438 54 184 98 366 93 546-16" fill="none" stroke="#C8B8FF" stroke-width="2" opacity=".24"/>
  <path d="M218 618c196-40 371-14 524 76 180 105 349 110 526 15" fill="none" stroke="#7E8B5B" stroke-width="2" opacity=".16"/>
  <path d="M1110 156c-51 91-51 181 0 270" fill="none" stroke="#D9A441" stroke-width="8" stroke-linecap="round" opacity=".12"/>
</svg>
"""))
    generated.append(write_svg("nd-dossier-bg.svg", """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 860" role="img" aria-label="Formula dossier background">
  <rect width="1180" height="860" fill="#FFFFFF"/>
  <g fill="none">
    <path d="M92 152h996M92 286h996M92 420h996M92 554h996M92 688h996" stroke="#1D1D1F" stroke-opacity=".08"/>
    <path d="M212 84v692M500 84v692M788 84v692" stroke="#1D1D1F" stroke-opacity=".045"/>
    <path d="M99 735c142-62 264-58 367 12 123 84 259 77 408-22 74-49 143-65 207-47" stroke="#5A4FD3" stroke-opacity=".18" stroke-width="2"/>
    <path d="M132 203c118-36 224-28 318 24 116 65 236 57 360-24" stroke="#D9A441" stroke-opacity=".22" stroke-width="2"/>
  </g>
</svg>
"""))
    generated.append(write_svg("nd-quiet-icons.svg", """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 120" role="img" aria-label="Natdropp linear icon system">
  <g fill="none" stroke="#1D1D1F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
    <path d="M60 82c-18-18-22-44 0-68 22 24 18 50 0 68Zm0 0v22"/>
    <path d="M156 92c28-10 42-32 42-66-34 0-56 18-66 48"/>
    <path d="M270 88c-22-12-34-28-34-50 0-15 10-26 24-26s24 11 24 26c0 22-12 38-34 50Z"/>
    <path d="M350 76c22 18 54 18 76 0M362 42h52M362 58h52"/>
    <path d="M520 88c-18 0-32-14-32-32s14-32 32-32 32 14 32 32-14 32-32 32Z"/>
    <path d="M612 88h60M642 28v60M616 56h52"/>
  </g>
</svg>
"""))

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_root": SOURCE_ROOT.relative_to(ROOT).as_posix(),
        "assets": generated,
        "notes": [
            "Original files are copied into assets/raw without destructive edits.",
            "Raster derivatives are regenerated from local Natdropp product and botanical assets.",
            "Decorative formula assets are SVG/CSS-safe abstract graphics, not product or certification claims.",
        ],
    }
    (OUT / "nd-asset-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"generated": len(generated), "manifest": "assets/nd-asset-manifest.json"}, indent=2))


if __name__ == "__main__":
    main()
