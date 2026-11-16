# Ludéum — sitio

Sitio público de la app Ludéum (iPhone y iPad), servido con GitHub Pages en
https://carlos-carmona-777.github.io/ludeum/ — página de la app, privacidad, términos y
soporte en los 7 idiomas de la app.

| Idioma | Marketing | Privacidad | Términos | Soporte |
|---|---|---|---|---|
| es | `/` | `/privacidad/` | `/terminos/` | `/soporte/` |
| en | `/en/` | `/privacy/` | `/terms/` | `/support/` |
| fr | `/fr/` | `/fr/confidentialite/` | `/fr/conditions/` | `/fr/assistance/` |
| de | `/de/` | `/de/datenschutz/` | `/de/nutzungsbedingungen/` | `/de/support/` |
| pt-BR | `/pt-br/` | `/pt-br/privacidade/` | `/pt-br/termos/` | `/pt-br/suporte/` |
| ca | `/ca/` | `/ca/privadesa/` | `/ca/condicions/` | `/ca/suport/` |
| it | `/it/` | `/it/privacy/` | `/it/termini/` | `/it/assistenza/` |

Las de privacidad y términos no salen en el menú (solo en el pie) y llevan `noindex`.
La de términos la enlaza Google Play (declaración de estado de operador de la DSA):
no cambiar sus rutas.

## Cómo se genera

Los `.html` se generan; no se editan a mano.

```bash
python3 tools/extraer_datos.py <repo ludus>   # juegos, rivales y próximos de la app → tools/datos.json
python3 tools/imagenes.py <repo ludus>        # capturas, retratos, ícono y compartir.jpg → img/
python3 tools/generar.py                      # todas las páginas + 404.html + sitemap.xml
```

- Textos: `tools/textos/<idioma>.json` (el español es el original; los demás
  usan los términos de `Localizable.xcstrings` de la app).
- Contacto de soporte: `support.contact`/`form_url` de cada JSON llevan al formulario de
  soporte en Tzinitzcan (https://tzinitzcan.com/ludeum/soporte/, Xeenoj + Resend).
- Al salir en el App Store: cambiar la insignia «Próximamente» por el enlace a
  `https://apps.apple.com/app/id6821357405` y agregar
  `<meta name="apple-itunes-app" content="app-id=6821357405">`.
- Las capturas originales están fuera del repo (Escritorio y Descargas de
  Carlos); la lista vive en `tools/imagenes.py`.
