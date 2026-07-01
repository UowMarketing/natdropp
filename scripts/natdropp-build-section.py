from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CUSTOM = ROOT / "dist" / "natdropp-home-custom-liquid.liquid"
SECTION = ROOT / "sections" / "natdropp-formula-home.liquid"


SECTION_ASSIGN = """{% liquid
  assign nd_product_handle = section.settings.product_handle | default: 'jabon-lavanda-flash'
  assign nd_product = all_products[nd_product_handle]
  assign nd_product_url = section.settings.product_url | default: '/products/jabon-lavanda-flash'
  assign nd_main_cta_label = section.settings.main_cta_label | default: 'Descubrir Lavanda Flash'
  assign nd_secondary_cta_label = section.settings.secondary_cta_label | default: 'Ver ingredientes'
  assign nd_logo_url = 'nd-logo.svg' | asset_url
  assign nd_product_main_url = 'nd-product-main.png' | asset_url
  assign nd_product_250_url = 'nd-product-250.webp' | asset_url
  assign nd_product_500_url = 'nd-product-500.webp' | asset_url
  assign nd_product_1l_url = 'nd-product-1l.webp' | asset_url
  assign nd_pack_hero_url = 'nd-pack-hero.webp' | asset_url
  assign nd_acene_url = 'nd-acene-badge.webp' | asset_url
  assign nd_lavender_1_url = 'nd-lavender-1.webp' | asset_url
  assign nd_lavender_2_url = 'nd-lavender-2.webp' | asset_url
  assign nd_leaf_1_url = 'nd-leaf-1.webp' | asset_url
  assign nd_leaf_2_url = 'nd-leaf-2.webp' | asset_url
  assign nd_leaf_3_url = 'nd-leaf-3.webp' | asset_url
  assign nd_single_leaf_1_url = 'nd-single-leaf-1.webp' | asset_url
  assign nd_single_leaf_2_url = 'nd-single-leaf-2.webp' | asset_url
  assign nd_single_leaf_3_url = 'nd-single-leaf-3.webp' | asset_url
  assign nd_single_leaf_4_url = 'nd-single-leaf-4.webp' | asset_url
%}
"""


SCHEMA = """
{% schema %}
{
  "name": "Natdropp home formula",
  "settings": [
    {
      "type": "text",
      "id": "product_handle",
      "label": "Handle del producto",
      "default": "jabon-lavanda-flash"
    },
    {
      "type": "text",
      "id": "main_cta_label",
      "label": "Texto CTA principal",
      "default": "Descubrir Lavanda Flash"
    },
    {
      "type": "text",
      "id": "secondary_cta_label",
      "label": "Texto CTA secundario",
      "default": "Ver ingredientes"
    },
    {
      "type": "text",
      "id": "product_url",
      "label": "URL fallback del producto",
      "default": "/products/jabon-lavanda-flash"
    },
    {
      "type": "checkbox",
      "id": "enable_motion",
      "label": "Activar motion",
      "default": true
    },
    {
      "type": "checkbox",
      "id": "show_ingredient_story",
      "label": "Mostrar historia de fórmula",
      "default": true
    },
    {
      "type": "checkbox",
      "id": "show_faq",
      "label": "Mostrar FAQ",
      "default": true
    }
  ],
  "presets": [
    {
      "name": "Natdropp home formula"
    }
  ]
}
{% endschema %}
"""


def main() -> None:
    content = CUSTOM.read_text(encoding="utf-8")
    content = content.lstrip("\ufeff")
    content = re.sub(r"(?s)\A(?:\{% assign .+? %\}\r?\n)+", SECTION_ASSIGN, content)
    content = content.replace('data-nd-motion="true"', 'data-nd-motion="{{ section.settings.enable_motion }}"')
    content = content.replace(
        '    <section class="nd-section nd-formula" id="nd-formula" data-nd-formula aria-labelledby="nd-formula-title">',
        '    {% if section.settings.show_ingredient_story %}\n    <section class="nd-section nd-formula" id="nd-formula" data-nd-formula aria-labelledby="nd-formula-title">',
    )
    content = content.replace(
        '    <section class="nd-section nd-reveal-product" aria-labelledby="nd-product-title">',
        '    {% endif %}\n\n    <section class="nd-section nd-reveal-product" aria-labelledby="nd-product-title">',
    )
    content = content.replace(
        '    <section class="nd-section nd-faq" aria-labelledby="nd-faq-title">',
        '    {% if section.settings.show_faq %}\n    <section class="nd-section nd-faq" aria-labelledby="nd-faq-title">',
    )
    content = content.replace(
        '    <section class="nd-final" aria-labelledby="nd-final-title">',
        '    {% endif %}\n\n    <section class="nd-final" aria-labelledby="nd-final-title">',
    )
    content = content.rstrip() + "\n" + SCHEMA.lstrip()
    SECTION.write_text(content, encoding="utf-8")
    print(SECTION.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
