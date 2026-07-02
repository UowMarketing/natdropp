# Natdropp Home / Landing

Paquete final para la home de Natdropp centrada en Lavanda Flash, en espanol y lista para Shopify.

## Enlaces

- Preview live: https://natdropp-preview.vercel.app
- Repo GitHub: https://github.com/UowMarketing/natdropp

## Archivo principal

Pegar directamente en una seccion Custom Liquid:

`dist/natdropp-home-custom-liquid.liquid`

El archivo incluye HTML, CSS y JS dentro de:

`<section id="nd-formula-home" class="nd-home" data-nd-home>`

No crea menu, no crea sticky nav y no depende de clases globales del theme.

## Seccion Shopify formal

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

- Preview local: `dist/natdropp-preview.html`
- Preview deployable: `index.html`
- Contrasena del preview: `natdrop4321` (tambien acepta `natdropp4321`)

Se regenera con:

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
- `nd-single-leaf-1.webp`
- `nd-single-leaf-2.webp`
- `nd-single-leaf-3.webp`
- `nd-single-leaf-4.webp`
- `nd-acene-badge.webp`
- `nd-pack-hero.webp`
- `nd-olive-photo.webp`
- `nd-coconut-photo.webp`
- `nd-vitamin-photo.webp`

El pipeline esta en:

`scripts/natdropp-process-assets.py`

No destruye originales: copia fuentes en `Assets/raw` y regenera derivados optimizados.

## Ultima reconstruccion

- Hero con pack recto, sin inclinaciones ni superposiciones sobre botellas.
- Producto protagonista con composicion de estudio y fondo editorial.
- Hojas globales y acentos botanicos conservados como fondo estatico, sin caida, giro ni parallax.
- Fondos y acentos botanicos visibles resueltos con hojas individuales `nd-single-leaf-*`; no se usan ramas ni clusters como fondo decorativo.
- Historia de formula reconstruida como bloque estatico legible, sin stage sticky ni scroll-story animado.
- Chips de multiuso con iconos SVG y cards de Lavanda Flash con padding corregido.
- FAQ compacta en tres columnas desktop, dos en tablet y una columna mobile.
- CTA final reequilibrado con mas contenido de confianza y producto menos invasivo.
- Botones y CTAs con contraste corregido.
- `.theme-check.yml` desactiva solo `UndefinedObject` porque el validador local no reconoce `section.settings`, aunque es Liquid valido en secciones Shopify.

## Shopify Files / Theme assets

El Custom Liquid usa URLs CDN reales ya subidas a Shopify para producto, logo, ACENE, olivo y lavanda, por lo que puede pegarse directamente.

Tambien embebe como data URI el pack hero y las hojas sueltas generadas para que el archivo pegado sea autocontenido. Para usar la seccion formal del theme, subir los assets `nd-*` a la carpeta `assets` del theme.

## Cambios rapidos

- Cambiar producto: editar `jabon-lavanda-flash` en el Custom Liquid o usar `product_handle` en la seccion formal.
- Cambiar CTA principal: editar `nd_main_cta_label` o usar el setting de la seccion.
- Cambiar CTA secundario: editar `nd_secondary_cta_label` o usar el setting de la seccion.
- Motion: el Custom Liquid queda por defecto en `data-nd-motion="false"` y la seccion formal tiene `enable_motion` desactivado por defecto.

## IA / generacion de assets

No se uso generacion nueva con OpenAI API en esta pasada. Se trabajo con producto real, pack real, ACENE real, olivo/lavanda existentes y assets procesados locales, incluyendo imagenes ya presentes en el workspace. Generaciones nuevas realizadas: `0`.

## Pruebas realizadas

- `scripts/natdropp-build-section.py`
- `scripts/natdropp-build-preview.py`
- Validacion Shopify Liquid: `sections/natdropp-formula-home.liquid` valido.
- QA Playwright/Chromium en 390 px, 768 px y 1440 px.
- Revision de overflow horizontal: `0`.
- Revision de imagenes rotas: `0`.
- Revision de errores de consola: `0`.
- Motion global desactivado por pedido: sin `nd-leaf-rain`, sin parallax, sin reveals animados.
- Formula confirmada en modo estatico: no hay stage sticky ni progreso dependiente del scroll.
- Preview gate confirmado con contrasena `natdrop4321` y alias `natdropp4321`.
- Deploy Vercel verificado con HTTP y Playwright en URL live.
- Live confirmado: `https://natdropp-preview.vercel.app` responde 200, contiene gate, logo violeta y formula actual.
- Contrasena live confirmada con Playwright: `natdrop4321`.
- GitHub sincronizado en `main` con commit `993563b`.

## Capturas generadas

- `dist/qa-final/hero-390.png`
- `dist/qa-final/formula-390.png`
- `dist/qa-final/multiuse-390.png`
- `dist/qa-final/final-390.png`
- `dist/qa-final/hero-768.png`
- `dist/qa-final/formula-768.png`
- `dist/qa-final/multiuse-768.png`
- `dist/qa-final/final-768.png`
- `dist/qa-final/hero-1440.png`
- `dist/qa-final/formula-1440.png`
- `dist/qa-final/multiuse-1440.png`
- `dist/qa-final/final-1440.png`
- `dist/qa-final/formula-mid-390.png`
- `dist/qa-final/formula-mid-1440.png`

## Limitaciones conocidas

- La disponibilidad, precio y variantes finales dependen del producto real en Shopify.
- La seccion formal requiere que los assets `nd-*` esten en `assets` del theme.
- El Custom Liquid esta pensado para pegarse debajo del header existente del theme.
- La contrasena del preview es una barrera client-side para compartir el enlace; no sustituye una proteccion server-side de Vercel.
- El proyecto Vercel se creo por CLI desde el paquete local; el repo GitHub contiene el mismo paquete publicado.
- No se cargan fuentes externas; la pila tipografica usa Manrope si esta disponible localmente y fallback Inter/system UI.
