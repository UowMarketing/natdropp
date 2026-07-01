# Natdropp Home / Landing

Paquete final para una home de Natdropp centrada en Lavanda Flash, en español y lista para Shopify.

## Archivo principal

Pegar directamente en una sección **Custom Liquid**:

`dist/natdropp-home-custom-liquid.liquid`

El archivo incluye HTML, CSS y JS dentro de:

`<section id="nd-formula-home" class="nd-home" data-nd-home>`

No crea menú, no crea sticky nav y no depende de clases globales del theme.

## Sección Shopify formal

`sections/natdropp-formula-home.liquid`

Incluye schema para configurar:

- `product_handle`
- `main_cta_label`
- `secondary_cta_label`
- `product_url`
- `enable_motion`
- `show_ingredient_story`
- `show_faq`

## Preview

`dist/natdropp-preview.html`

Se genera con:

`python scripts/natdropp-build-preview.py`

## Assets

Manifest:

`Assets/nd-asset-manifest.json`

Assets principales usados:

- `nd-logo.svg`
- `nd-favicon.svg`
- `nd-product-main.png`
- `nd-product-main.webp`
- `nd-product-250.webp`
- `nd-product-500.webp`
- `nd-product-1l.webp`
- `nd-lavender-1.webp`
- `nd-lavender-2.webp`
- `nd-leaf-1.webp`
- `nd-leaf-2.webp`
- `nd-leaf-3.webp`
- `nd-acene-badge.webp`

El pipeline está en:

`scripts/natdropp-process-assets.py`

No destruye originales: copia fuentes en `Assets/raw` y regenera derivados optimizados.

## Cambios aplicados en la última reconstrucción

- Hero rehecho con pack recto, sin inclinaciones ni superposición artificial de botellas.
- Producto protagonista centrado y con composición de estudio.
- Se eliminó el rulo/splash dorado de la historia de fórmula.
- Fórmula reconstruida con olivo y lavanda reales detrás del producto, sin elementos delante.
- Multiuso pasó de tarjetas apiladas a dossier con separadores editoriales.
- Se corrigieron contrastes para evitar texto oscuro sobre fondos violetas.
- Se eliminaron labels flotantes/orbit labels y chips deformables.

## Shopify Files / Theme assets

El Custom Liquid usa URLs CDN reales ya subidas a Shopify para producto, logo, ACENE, olivo y lavanda, por lo que puede pegarse directamente.

Para usar la sección formal del theme, subir los assets `nd-*` a la carpeta `assets` del theme.

## Cambios rápidos

- Cambiar producto: editar `jabon-lavanda-flash` en el Custom Liquid o usar `product_handle` en la sección formal.
- Cambiar CTA principal: editar `nd_main_cta_label` o usar el setting de la sección.
- Cambiar CTA secundario: editar `nd_secondary_cta_label` o usar el setting de la sección.
- Desactivar motion: en Custom Liquid cambiar `data-nd-motion="true"` a `data-nd-motion="false"`; en sección formal usar el checkbox.

## IA / generación de assets

No se usó generación nueva con OpenAI API. Se trabajó con producto real, pack real, ACENE real, olivo/lavanda existentes y assets procesados locales. Generaciones nuevas realizadas: `0`.

## Pruebas realizadas

- `scripts/natdropp-build-section.py`
- `scripts/natdropp-build-preview.py`
- Validación Shopify Liquid: `sections/natdropp-formula-home.liquid` válido.
- Preview en `http://127.0.0.1:53802/dist/natdropp-preview.html`
- Capturas con Chrome/Playwright en 390 px, 768 px y 1440 px.
- Revisión de overflow horizontal: `0`.
- Revisión de hero: botellas rectas, sin rotación, sin solapamiento.
- Revisión de fórmula móvil: producto centrado dentro del canvas.
- Revisión de multiuso móvil: sin orbit labels y sin cards deformadas.

## Capturas generadas

- `dist/screenshots/natdropp-redesign-1440-hero-upright.png`
- `dist/screenshots/natdropp-redesign-formula-canvas-390-final.png`
- `dist/screenshots/natdropp-redesign-multiuse-390-final.png`
- `dist/screenshots/natdropp-redesign-1440-formula-botanical-final.png`

## Limitaciones conocidas

- La disponibilidad, precio y variantes finales dependen del producto real en Shopify.
- La sección formal requiere que los assets `nd-*` estén en `assets` del theme.
- El Custom Liquid está pensado para pegarse debajo del header existente del theme.
