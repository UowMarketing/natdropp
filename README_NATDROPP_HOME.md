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
- `nd-acene-badge.webp`
- `nd-pack-hero.webp`

El pipeline esta en:

`scripts/natdropp-process-assets.js`

No destruye originales: copia fuentes en `Assets/raw` y regenera derivados optimizados.

## Ultima reconstruccion

- Hero con pack recto, sin inclinaciones ni superposiciones sobre botellas.
- Producto protagonista con composicion de estudio y fondo editorial.
- Hojas globales semitransparentes con movimiento natural de scroll, giro y caida suave.
- Ramas de olivo/lavanda como capas de borde, nunca delante de producto o texto critico.
- Historia de formula con movimiento por progreso de scroll, particulas de formula y producto limpio.
- FAQ compacta en dos columnas desktop y una columna mobile.
- CTA final reequilibrado con mas contenido de confianza y producto menos invasivo.
- Botones y CTAs con contraste corregido.

## Shopify Files / Theme assets

El Custom Liquid usa URLs CDN reales ya subidas a Shopify para producto, logo, ACENE, olivo y lavanda, por lo que puede pegarse directamente.

Para usar la seccion formal del theme, subir los assets `nd-*` a la carpeta `assets` del theme.

## Cambios rapidos

- Cambiar producto: editar `jabon-lavanda-flash` en el Custom Liquid o usar `product_handle` en la seccion formal.
- Cambiar CTA principal: editar `nd_main_cta_label` o usar el setting de la seccion.
- Cambiar CTA secundario: editar `nd_secondary_cta_label` o usar el setting de la seccion.
- Desactivar motion: en Custom Liquid cambiar `data-nd-motion="true"` a `data-nd-motion="false"`; en seccion formal usar el checkbox.

## IA / generacion de assets

No se uso generacion nueva con OpenAI API. Se trabajo con producto real, pack real, ACENE real, olivo/lavanda existentes y assets procesados locales. Generaciones nuevas realizadas: `0`.

## Pruebas realizadas

- `scripts/natdropp-build-section.py`
- `scripts/natdropp-build-preview.py`
- Validacion Shopify Liquid: `sections/natdropp-formula-home.liquid` valido.
- QA Playwright/Chromium instalado en 390 px, 768 px y 1440 px.
- Revision de overflow horizontal: `0`.
- Revision de imagenes rotas: `0`.
- Motion global confirmado: `nd-leaf-fall`.
- Formula flow confirmado: `.nd-formula-flow`.
- Deploy Vercel verificado con HTTP `200`.
- GitHub sincronizado en `main`.

## Capturas generadas

- `dist/screenshots/natdropp-vercel-root-390-final.png`
- `dist/screenshots/natdropp-vercel-root-768-final.png`
- `dist/screenshots/natdropp-vercel-root-1440-final.png`

## Limitaciones conocidas

- La disponibilidad, precio y variantes finales dependen del producto real en Shopify.
- La seccion formal requiere que los assets `nd-*` esten en `assets` del theme.
- El Custom Liquid esta pensado para pegarse debajo del header existente del theme.
- El proyecto Vercel se creo por CLI desde el paquete local; el repo GitHub contiene el mismo paquete publicado.
