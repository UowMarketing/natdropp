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
    "{{ nd_pack_hero_url }}": "../Assets/nd-pack-hero.webp",
    "{{ nd_acene_url }}": "../Assets/nd-acene-badge.webp",
    "{{ nd_lavender_1_url }}": "../Assets/nd-lavender-1.webp",
    "{{ nd_lavender_2_url }}": "../Assets/nd-lavender-2.webp",
    "{{ nd_leaf_1_url }}": "../Assets/nd-leaf-1.webp",
    "{{ nd_leaf_2_url }}": "../Assets/nd-leaf-2.webp",
    "{{ nd_leaf_3_url }}": "../Assets/nd-leaf-3.webp",
    "{{ nd_single_leaf_1_url }}": "../Assets/nd-single-leaf-1.webp",
    "{{ nd_single_leaf_2_url }}": "../Assets/nd-single-leaf-2.webp",
    "{{ nd_single_leaf_3_url }}": "../Assets/nd-single-leaf-3.webp",
    "{{ nd_single_leaf_4_url }}": "../Assets/nd-single-leaf-4.webp",
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
    gate = """
  <div class="nd-preview-gate" data-preview-gate role="dialog" aria-modal="true" aria-labelledby="nd-preview-gate-title">
    <form class="nd-preview-gate-card" data-preview-gate-form>
      <p class="nd-preview-gate-label">Preview privado</p>
      <h1 id="nd-preview-gate-title">Natdropp Lavanda Flash</h1>
      <p>Introduce la contraseña para ver la landing completa.</p>
      <label>
        <span>Contraseña</span>
        <input data-preview-gate-input type="password" autocomplete="current-password" placeholder="Contraseña" aria-label="Contraseña del preview">
      </label>
      <button type="submit">Entrar al preview</button>
      <p class="nd-preview-gate-error" data-preview-gate-error aria-live="polite"></p>
    </form>
  </div>
"""
    gate_script = """
<script>
(function(){
  var password = "natdrop4321";
  var key = "natdropp_preview_access_v1";
  var body = document.body;
  var gate = document.querySelector("[data-preview-gate]");
  var form = document.querySelector("[data-preview-gate-form]");
  var input = document.querySelector("[data-preview-gate-input]");
  var error = document.querySelector("[data-preview-gate-error]");
  function unlock(){
    try { sessionStorage.setItem(key, "ok"); } catch (e) {}
    body.classList.remove("nd-preview-locked");
    if (gate) gate.remove();
  }
  try {
    if (sessionStorage.getItem(key) === "ok") {
      unlock();
      return;
    }
  } catch (e) {}
  if (input) setTimeout(function(){ input.focus(); }, 120);
  if (!form) return;
  form.addEventListener("submit", function(event){
    event.preventDefault();
    if (input && input.value === password) {
      unlock();
      return;
    }
    if (error) error.textContent = "Contraseña incorrecta.";
    if (input) {
      input.value = "";
      input.focus();
    }
  });
})();
</script>
"""
    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Natdropp Lavanda Flash Preview</title>
  <style>
    html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; background: #F5F5F7; }}
    body.nd-preview-locked {{ overflow: hidden; }}
    body.nd-preview-locked #nd-formula-home {{ filter: blur(10px); transform: scale(1.006); pointer-events: none; user-select: none; }}
    .nd-preview-gate {{ position: fixed; inset: 0; z-index: 2147483647; display: grid; place-items: center; padding: 24px; background: radial-gradient(ellipse at 52% 22%, rgba(236,233,255,.94), rgba(245,245,247,.9) 46%, rgba(250,250,247,.96)); font-family: Manrope, Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .nd-preview-gate-card {{ width: min(100%, 440px); padding: 34px; border-radius: 28px; background: rgba(255,255,255,.84); border: 1px solid rgba(52,52,58,.12); box-shadow: 0 34px 90px rgba(52,52,58,.16); backdrop-filter: blur(22px); }}
    .nd-preview-gate-label {{ margin: 0 0 12px; color: #5A4FD3; font-size: 12px; line-height: 1; font-weight: 900; text-transform: uppercase; letter-spacing: 0; }}
    .nd-preview-gate h1 {{ margin: 0; color: #34343A; font-size: clamp(34px, 7vw, 52px); line-height: .94; letter-spacing: -.045em; }}
    .nd-preview-gate p {{ margin: 18px 0 0; color: rgba(52,52,58,.72); font-size: 15px; line-height: 1.55; font-weight: 650; }}
    .nd-preview-gate label {{ display: grid; gap: 9px; margin-top: 24px; color: rgba(52,52,58,.72); font-size: 12px; font-weight: 850; text-transform: uppercase; }}
    .nd-preview-gate input {{ width: 100%; height: 50px; padding: 0 16px; border-radius: 16px; border: 1px solid rgba(52,52,58,.16); background: #fff; color: #34343A; font: inherit; font-size: 16px; outline: none; box-sizing: border-box; }}
    .nd-preview-gate input:focus {{ border-color: rgba(90,79,211,.72); box-shadow: 0 0 0 4px rgba(90,79,211,.12); }}
    .nd-preview-gate button {{ width: 100%; height: 50px; margin-top: 14px; border: 0; border-radius: 999px; color: #fff; background: linear-gradient(180deg, #655BE0, #5147CC); font: inherit; font-size: 14px; font-weight: 850; cursor: pointer; }}
    .nd-preview-gate-error {{ min-height: 20px; color: #9F2F2F !important; font-size: 13px !important; margin-top: 12px !important; }}
  </style>
</head>
<body class="nd-preview-locked">
{gate}
{content}
{gate_script}
</body>
</html>
"""
    PREVIEW.write_text(html, encoding="utf-8")
    print(PREVIEW.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()

