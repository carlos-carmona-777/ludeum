# Ludéum — sitio

Sitio público de la app Ludéum (iPhone y iPad), servido con GitHub Pages en
https://carlos-carmona-777.github.io/ludeum/ — página de la app, privacidad y
soporte en los 7 idiomas de la app.

| Idioma | Marketing | Privacidad | Soporte |
|---|---|---|---|
| es | `/` | `/privacidad/` | `/soporte/` |
| en | `/en/` | `/privacy/` | `/support/` |
| fr | `/fr/` | `/fr/confidentialite/` | `/fr/assistance/` |
| de | `/de/` | `/de/datenschutz/` | `/de/support/` |
| pt-BR | `/pt-br/` | `/pt-br/privacidade/` | `/pt-br/suporte/` |
| ca | `/ca/` | `/ca/privadesa/` | `/ca/suport/` |
| it | `/it/` | `/it/privacy/` | `/it/assistenza/` |

Las de privacidad no salen en el menú (solo en el pie) y llevan `noindex`.

## Cómo se genera

Los `.html` se generan; no se editan a mano.

```bash
python3 tools/extraer_datos.py <repo ludus>   # juegos, rivales y próximos de la app → tools/datos.json
python3 tools/imagenes.py <repo ludus>        # capturas, retratos, ícono y compartir.jpg → img/
python3 tools/generar.py                      # todas las páginas + 404.html + sitemap.xml
```

- Textos: `tools/textos/<idioma>.json` (el español es el original; los demás
  usan los términos de `Localizable.xcstrings` de la app).
- Contacto de soporte: `support.contact` de cada JSON enlaza al formulario de
  la página de Ludéum en Tzinitzcan (https://tzinitzcan.com/ludeum/#avisame).
- Al salir en el App Store: cambiar la insignia «Próximamente» por el enlace a
  `https://apps.apple.com/app/id6821357405` y agregar
  `<meta name="apple-itunes-app" content="app-id=6821357405">`.
- Las capturas originales están fuera del repo (Escritorio y Descargas de
  Carlos); la lista vive en `tools/imagenes.py`.
