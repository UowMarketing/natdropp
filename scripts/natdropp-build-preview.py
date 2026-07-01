from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CUSTOM_LIQUID = ROOT / "dist" / "natdropp-home-custom-liquid.liquid"
PREVIEW = ROOT / "dist" / "natdropp-preview.html"


REPLACEMENTS = {
    "{{ nd_logo_url }}": "../Assets/nd-logo.svg",
    "{{ nd_product_main_url }}": "../Assets/nd-product-main.png",
    "{{ nd_product_250_url }}": "../Assets/nd-product-250.webp",
    "{{ nd_product_500_url }}": "../Assets/nd-product-500.webp",
    "{{ nd_product_1l_url }}": "../Assets/nd-product-1l.webp",
    "{{ nd_acene_url }}": "../Assets/nd-acene-badge.webp",
    "{{ nd_lavender_1_url }}": "../Assets/nd-lavender-1.webp",
    "{{ nd_lavender_2_url }}": "../Assets/nd-lavender-2.webp",
    "{{ nd_leaf_1_url }}": "../Assets/nd-leaf-1.webp",
    "{{ nd_leaf_2_url }}": "../Assets/nd-leaf-2.webp",
    "{{ nd_leaf_3_url }}": "../Assets/nd-leaf-3.webp",
    "{{ nd_product_url }}": "/products/jabon-lavanda-flash",
    "{{ nd_main_cta_label }}": "Descubrir Lavanda Flash",
    "{{ nd_secondary_cta_label }}": "Ver ingredientes",
    "{{ routes.root_url }}": "/",
}


STATIC_FORMATS = """
    <section class="nd-section nd-formats" aria-labelledby="nd-formats-title">
      <div class="nd-shell">
        <div class="nd-section-head">
          <div class="nd-reveal">
            <p class="nd-eyebrow">Formatos</p>
            <h2 class="nd-h2" id="nd-formats-title">Tres tamaños, una misma fórmula.</h2>
          </div>
          <p class="nd-copy nd-reveal">250 ml para probar, 500 ml para el uso diario y 1 L para convertir Lavanda Flash en básico de casa.</p>
        </div>
        <div class="nd-format-grid nd-reveal">
          <article class="nd-format-card"><img class="nd-format-img" src="{{ nd_product_250_url }}" width="760" height="1180" alt="Lavanda Flash 250 ml" loading="lazy"><div class="nd-format-info"><div><h3>250 ml</h3><p>Formato de entrada.</p></div><span class="nd-format-price">Probar</span></div></article>
          <article class="nd-format-card"><img class="nd-format-img" src="{{ nd_product_500_url }}" width="760" height="1180" alt="Lavanda Flash 500 ml" loading="lazy"><div class="nd-format-info"><div><h3>500 ml</h3><p>Formato diario.</p></div><span class="nd-format-price">Rutina</span></div></article>
          <article class="nd-format-card"><img class="nd-format-img" src="{{ nd_product_1l_url }}" width="760" height="1180" alt="Lavanda Flash 1 litro" loading="lazy"><div class="nd-format-info"><div><h3>1 L</h3><p>Formato familiar.</p></div><span class="nd-format-price">Reponer</span></div></article>
        </div>
        <div class="nd-shop-panel nd-reveal">
          <div>
            <p class="nd-eyebrow">Comprar</p>
            <h3 class="nd-h3">Lavanda Flash</h3>
            <p class="nd-copy">Preview estático con fallback de producto.</p>
          </div>
          <a class="nd-btn nd-btn-primary" href="{{ nd_product_url }}">Ver producto</a>
        </div>
      </div>
    </section>

"""


def replace_formats(content: str) -> str:
    start_marker = '    <section class="nd-section nd-formats" aria-labelledby="nd-formats-title">'
    next_marker = '    <section class="nd-section nd-trust" aria-labelledby="nd-trust-title">'
    start = content.index(start_marker)
    end = content.index(next_marker, start)
    return content[:start] + STATIC_FORMATS + content[end:]


def main() -> None:
    content = CUSTOM_LIQUID.read_text(encoding="utf-8")
    content = content.lstrip("\ufeff")
    content = replace_formats(content)
    content = re.sub(r"^\{% assign .+? %\}\r?\n", "", content, flags=re.MULTILINE)
    content = re.sub(r"\{%[^%]+%\}", "", content)
    for token, value in REPLACEMENTS.items():
        content = content.replace(token, value)
    content = re.sub(r"\{\{[^}]+\}\}", "", content)
    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Natdropp Lavanda Flash Preview</title>
  <style>
    html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; background: #F5F5F7; }}
  </style>
</head>
<body>
{content}
</body>
</html>
"""
    PREVIEW.write_text(html, encoding="utf-8")
    print(PREVIEW.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()

