"""Genera el sitio de Ludéum (GitHub Pages) en los 7 idiomas de la app.

    python3 tools/generar.py

Lee tools/datos.json (juegos, rivales y próximos, sacados de la app con
tools/extraer_datos.py) y tools/textos/<idioma>.json (textos del sitio), y
escribe index.html, las páginas de privacidad y soporte de cada idioma,
404.html y sitemap.xml (robots.txt no sirve en un sitio de proyecto: va en la raíz del dominio). Las imágenes de img/ las hace
tools/imagenes.py. No editar los .html a mano: se pisan al regenerar.
"""
import html, json, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://carlos-carmona-777.github.io/ludeum/'
ORDER = ['es', 'en', 'fr', 'de', 'pt-BR', 'ca', 'it']
APP_ID = '6821357405'

DATA = json.load(open(os.path.join(ROOT, 'tools', 'datos.json')))
T = {}
for code in ORDER:
    p = os.path.join(ROOT, 'tools', 'textos', f'{code}.json')
    if os.path.exists(p):
        T[code] = json.load(open(p))
LANGS = [c for c in ORDER if c in T]

HALL_ORDER = ['antiquity', 'middleAges', 'world', 'cards']
ICONS = {  # trazos SVG sencillos, en línea (sin peticiones externas)
    'antiquity': '<path d="M3 21h18M5 21V10m4 11V10m6 11V10m4 11V10M2 10h20L12 3 2 10z"/>',
    'middleAges': '<path d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6l7-3z"/>',
    'world': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
    'cards': '<rect x="4" y="3" width="11" height="16" rx="2"/><path d="M9 21h9a2 2 0 0 0 2-2V7"/>',
}


def esc(s):
    return html.escape(s, quote=True)


def size(rel):
    with Image.open(os.path.join(ROOT, rel)) as im:
        return im.size


def pic(prefix, key, widths, sizes, alt, cls='', eager=False):
    """<img> con srcset de las variantes WebP de img/capturas/."""
    files = [f'img/capturas/{key}-{w}.webp' for w in widths]
    w, h = size(files[-1])
    srcset = ', '.join(f'{prefix}{f} {wd}w' for f, wd in zip(files, widths))
    load = 'eager" fetchpriority="high' if eager else 'lazy'
    return (f'<img class="{cls}" src="{prefix}{files[0]}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{esc(alt)}" loading="{load}" decoding="async">')


PHONE = (360, 720)
WIDE = (720, 1280)


def url(code, kind):
    return BASE + T[code]['paths'][kind]


def depth_prefix(path):
    return '../' * path.count('/')


# ---------------------------------------------------------------- piezas comunes

def head(code, kind, title, desc, prefix, noindex=False, extra=''):
    t = T[code]
    alts = ''.join(f'<link rel="alternate" hreflang="{T[c]["html_lang"]}" href="{url(c, kind)}">' for c in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{url("es", kind)}">'
    og_alts = ''.join(f'<meta property="og:locale:alternate" content="{T[c]["og_locale"]}">' for c in LANGS if c != code)
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ''
    return f'''<!doctype html>
<html lang="{t["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<link rel="canonical" href="{url(code, kind)}">
{alts}
<meta name="theme-color" content="#1f3a3d">
<meta name="color-scheme" content="light dark">
<link rel="icon" type="image/png" sizes="32x32" href="{prefix}img/favicon-32.png">
<link rel="apple-touch-icon" href="{prefix}img/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ludéum">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url(code, kind)}">
<meta property="og:image" content="{BASE}img/compartir.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Ludéum">
<meta property="og:locale" content="{t["og_locale"]}">
{og_alts}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}img/compartir.jpg">
<link rel="stylesheet" href="{prefix}estilo.css">
{extra}</head>
'''


def lang_menu(code, kind, prefix):
    items = ''.join(
        f'<li><a href="{prefix}{T[c]["paths"][kind]}" hreflang="{T[c]["html_lang"]}" lang="{T[c]["html_lang"]}"'
        + (' aria-current="true"' if c == code else '') + f'>{esc(T[c]["label"])}</a></li>'
        for c in LANGS)
    return (f'<details class="idiomas"><summary aria-label="{esc(T[code]["common"]["language"])}">'
            f'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/></svg>'
            f'<span>{esc(T[code]["label"])}</span></summary><ul>{items}</ul></details>')


def header(code, kind, prefix, nav=''):
    c = T[code]['common']
    return f'''<body class="pagina-{kind}">
<a class="saltar" href="#contenido">{esc(c["skip"])}</a>
<header class="barra">
  <a class="marca" href="{prefix}{T[code]["paths"]["home"]}"><img src="{prefix}img/icono-96.webp" width="36" height="36" alt=""><span>Ludéum</span></a>
  {nav}
  {lang_menu(code, kind, prefix)}
</header>
'''


def footer(code, prefix):
    t = T[code]
    c = t['common']
    return f'''<footer class="pie">
  <div class="pie-in">
    <a class="marca" href="{prefix}{t["paths"]["home"]}"><img src="{prefix}img/icono-96.webp" width="32" height="32" alt=""><span>Ludéum</span></a>
    <nav class="pie-enlaces"><a href="{prefix}{t["paths"]["support"]}">{esc(c["support"])}</a><a href="{prefix}{t["paths"]["privacy"]}">{esc(c["privacy"])}</a></nav>
    <p>{c["studio"]}</p>
    <p class="suave">{esc(c["photos_credit"])}</p>
    <p class="suave">© 2026 Carlos Carmona</p>
  </div>
</footer>
</body>
</html>
'''


def soon_badge(code):
    c = T[code]['common']
    return (f'<span class="insignia"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.4 12.6c0-2.3 1.9-3.4 2-3.5-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.1-2.8.9-3.5.9s-1.8-.9-3-.8C7 7.4 5.6 8.3 4.8 9.7c-1.7 2.9-.4 7.2 1.2 9.5.8 1.1 1.7 2.4 2.9 2.4 1.2 0 1.6-.8 3-.8s1.8.8 3 .7c1.3 0 2.1-1.1 2.8-2.3.9-1.3 1.3-2.6 1.3-2.7 0 0-2.6-1-2.6-3.9zM14.2 5.8c.6-.8 1.1-1.8 1-2.8-.9 0-2 .6-2.7 1.4-.6.7-1.1 1.7-1 2.7 1 .1 2-.5 2.7-1.3z"/></svg>'
            f'<span><small>{esc(c["devices"])}</small>{esc(c["soon_badge"])}</span></span>')


# ---------------------------------------------------------------- inicio

def game_card(code, g, prefix):
    h = T[code]['home']
    L = code
    nvar = g['variants']
    variants = h['variants_one'] if nvar == 1 else h['variants_many'].replace('{n}', str(nvar))
    faces = ''.join(
        f'<img src="{prefix}img/rivales/{g["id"]}-{i}-128.webp" srcset="{prefix}img/rivales/{g["id"]}-{i}-256.webp 2x" '
        f'width="44" height="44" loading="lazy" decoding="async" alt="">' for i in range(3))
    names = []
    for r in g['rivals']:
        n = r['name'][L]
        names.append(f'{n}, {r["role"][L]}' if r['role'] and r['role'][L] else n)
    names_txt = ' · '.join(names)
    return f'''<article class="juego">
  <p class="origen">{esc(g["origin"][L])}</p>
  <h4>{esc(g["name"][L])}</h4>
  <p class="sub">{esc(g["subtitle"][L])}</p>
  <p>{esc(g["blurb"][L])}</p>
  <div class="rivales-mini"><div class="caras">{faces}</div><p><span>{esc(h["rivals_label"])}</span>{esc(names_txt)}</p></div>
  <p class="variantes">{esc(variants)}</p>
</article>'''


def build_home(code):
    t = T[code]
    h, c = t['home'], t['common']
    path = t['paths']['home']
    prefix = depth_prefix(path)
    nav = (f'<nav class="secciones"><a href="#juegos">{esc(h["nav_games"])}</a><a href="#rivales">{esc(h["nav_rivals"])}</a>'
           f'<a href="#torneos">{esc(h["nav_tournaments"])}</a><a href="#mecenas">{esc(h["nav_patron"])}</a></nav>')
    ld = {
        '@context': 'https://schema.org', '@type': 'MobileApplication', 'name': 'Ludéum',
        'operatingSystem': 'iOS, iPadOS', 'applicationCategory': 'GameApplication',
        'inLanguage': [T[x]['html_lang'] for x in LANGS], 'description': h['description'],
        'image': BASE + 'img/icono-512.png', 'url': url(code, 'home'),
        'author': {'@type': 'Person', 'name': 'Carlos Carmona'},
    }
    extra = ('<link rel="preload" as="image" href="' + prefix + 'img/fondo-sala-1000.webp" media="(max-width: 900px)">'
             '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n')
    out = [head(code, 'home', h['title'], h['description'], prefix, extra=extra), header(code, 'home', prefix, nav)]

    stats = ''.join(f'<li><strong>{esc(n)}</strong><span>{esc(l)}</span></li>' for n, l in h['stats'])
    out.append(f'''<main id="contenido">
<section class="portada">
  <div class="portada-in">
    <div class="portada-texto">
      <p class="antetitulo">{esc(h["hero_kicker"])}</p>
      <h1>{esc(h["hero_title"])}</h1>
      <p class="entrada">{esc(h["hero_lead"])}</p>
      {soon_badge(code)}
      <p class="nota">{esc(h["hero_note"])}</p>
    </div>
    <div class="portada-telefonos">
      {pic(prefix, "hnefatafl", PHONE, "(max-width: 900px) 40vw, 240px", h["gallery_alts"]["hnefatafl"], "tel tel-atras", eager=True)}
      {pic(prefix, "inicio", PHONE, "(max-width: 900px) 50vw, 300px", h["hero_img_alt"], "tel tel-frente", eager=True)}
    </div>
  </div>
  <ul class="cifras">{stats}</ul>
</section>
''')

    # Salas y juegos
    halls = []
    for hid in HALL_ORDER:
        hall = DATA['halls'][hid]
        games = sorted((g for g in DATA['games'] if g['hall'] == hid), key=lambda g: g['order'])
        cards = '\n'.join(game_card(code, g, prefix) for g in games)
        halls.append(f'''<div class="sala">
  <div class="sala-cab"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[hid]}</svg><h3>{esc(hall["title"][code])}</h3><span>{esc(hall["span"][code])}</span></div>
  <div class="juegos">{cards}</div>
</div>''')
    out.append(f'''<section class="seccion" id="juegos">
  <div class="ancho">
    <h2>{esc(h["halls_title"])}</h2>
    <p class="entrada">{esc(h["halls_lead"])}</p>
    {"".join(halls)}
  </div>
</section>
''')

    # Rivales y modos
    modes = ''.join(f'<li><strong>{esc(a)}</strong>{esc(b)}</li>' for a, b in h['modes'])
    hard = ''.join(
        f'<li><img src="{prefix}img/rivales/{g["id"]}-2-128.webp" srcset="{prefix}img/rivales/{g["id"]}-2-256.webp 2x" width="72" height="72" loading="lazy" decoding="async" alt=""><span>{esc(g["rivals"][2]["name"][code])}</span></li>'
        for g in DATA['games'])
    out.append(f'''<section class="seccion oscura" id="rivales">
  <div class="ancho dos">
    <div>
      <h2>{esc(h["rivals_title"])}</h2>
      <p class="entrada">{esc(h["rivals_lead"])}</p>
      <ul class="galeria-rivales">{hard}</ul>
      <h3>{esc(h["modes_title"])}</h3>
      <ul class="modos">{modes}</ul>
    </div>
    <div class="par-telefonos">
      {pic(prefix, "patolli-rival", PHONE, "(max-width: 900px) 45vw, 260px", h["rivals_img_alt"], "tel")}
      {pic(prefix, "ur-detalle", PHONE, "(max-width: 900px) 45vw, 260px", h["online_img_alt"], "tel desfase")}
    </div>
  </div>
</section>
''')

    # Lo que sabemos
    out.append(f'''<section class="seccion">
  <div class="ancho dos invertido">
    <div class="par-telefonos">
      {pic(prefix, "historia-ur", PHONE, "(max-width: 900px) 45vw, 260px", h["learn_img_alt"], "tel")}
      {pic(prefix, "tavli-detalle", PHONE, "(max-width: 900px) 45vw, 260px", h["learn_img2_alt"], "tel desfase")}
    </div>
    <div>
      <h2>{esc(h["learn_title"])}</h2>
      <p class="entrada">{h["learn_lead"]}</p>
    </div>
  </div>
</section>
''')

    # Torneos
    items = ''.join(f'<li><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for a, b in h['tournaments_items'])
    out.append(f'''<section class="seccion papel" id="torneos">
  <div class="ancho dos">
    <div>
      <h2>{esc(h["tournaments_title"])}</h2>
      <ul class="lista-tarjetas">{items}</ul>
    </div>
    <div class="par-telefonos">
      {pic(prefix, "torneos", PHONE, "(max-width: 900px) 45vw, 260px", h["tournaments_img_alt"], "tel")}
      {pic(prefix, "logros", PHONE, "(max-width: 900px) 45vw, 260px", h["achievements_img_alt"], "tel desfase")}
    </div>
  </div>
</section>
''')

    # Hecho con cuidado + galería
    craft = ''.join(f'<li><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for a, b in h['craft_items'])
    g_alts = h['gallery_alts']
    phones = ''.join(f'<li>{pic(prefix, k, PHONE, "(max-width: 600px) 60vw, 240px", g_alts[k], "tel")}</li>'
                     for k in ['ur', 'pente', 'latrunculi', 'hnefatafl', 'tavli', 'cribbage'])
    wides = ''.join(f'<li>{pic(prefix, k, WIDE, "(max-width: 600px) 90vw, 560px", g_alts[k], "tel ancha")}</li>'
                    for k in ['ur-mesa', 'oware-oscuro', 'konane', 'hnefatafl-mesa'])
    out.append(f'''<section class="seccion">
  <div class="ancho">
    <h2>{esc(h["craft_title"])}</h2>
    <ul class="rejilla-seis">{craft}</ul>
    <h3 class="titulo-galeria">{esc(h["gallery_title"])}</h3>
  </div>
  <ul class="carrusel">{phones}</ul>
  <ul class="carrusel">{wides}</ul>
</section>
''')

    # iPad
    out.append(f'''<section class="seccion papel">
  <div class="ancho">
    <h2>{esc(h["ipad_title"])}</h2>
    <p class="entrada">{esc(h["ipad_lead"])}</p>
    <div class="ipads">
      {pic(prefix, "ipad-inicio", (480, 960), "(max-width: 900px) 40vw, 330px", h["ipad_alt"], "ipad")}
      {pic(prefix, "ipad-historia", WIDE, "(max-width: 900px) 58vw, 590px", h["ipad2_alt"], "ipad")}
    </div>
  </div>
</section>
''')

    # Mecenas
    perks = ''.join(f'<li>{esc(p)}</li>' for p in h['patron_items'])
    out.append(f'''<section class="seccion" id="mecenas">
  <div class="ancho">
    <div class="mecenas">
      <svg class="laurel" viewBox="0 0 64 64" aria-hidden="true"><path d="M32 54c-12-2-20-12-20-24M32 54c12-2 20-12 20-24M14 22c3 1 5 4 5 7-3-1-5-4-5-7zm-2 10c3 0 6 2 7 5-3 0-6-2-7-5zm4 9c3-1 6 0 8 3-3 1-6 0-8-3zM50 22c-3 1-5 4-5 7 3-1 5-4 5-7zm2 10c-3 0-6 2-7 5 3 0 6-2 7-5zm-4 9c-3-1-6 0-8 3 3 1 6 0 8-3z"/></svg>
      <h2>{esc(h["patron_title"])}</h2>
      <p class="entrada">{esc(h["patron_lead"])}</p>
      <ul class="ventajas">{perks}</ul>
      <p class="suave">{esc(h["patron_note"])}</p>
    </div>
  </div>
</section>
''')

    # Próximamente
    chips = ''.join(f'<li><strong>{esc(u["name"][code])}</strong><span>{esc(u["origin"][code])}</span></li>' for u in DATA['upcoming'])
    out.append(f'''<section class="seccion papel">
  <div class="ancho">
    <h2>{esc(h["upcoming_title"])} <span class="etiqueta">{esc(h["upcoming_badge"])}</span></h2>
    <p class="entrada">{h["upcoming_lead"]}</p>
    <ul class="proximos">{chips}</ul>
  </div>
</section>
''')

    out.append(f'''<section class="cierre">
  <div class="ancho">
    <img src="{prefix}img/icono-192.webp" width="96" height="96" alt="" loading="lazy">
    <h2>{esc(h["cta_title"])}</h2>
    <p>{esc(h["cta_lead"])}</p>
    {soon_badge(code)}
    <p><a class="boton-sec" href="{prefix}{t["paths"]["support"]}">{esc(c["support"])}</a></p>
  </div>
</section>
</main>
''')
    out.append(footer(code, prefix))
    return path, ''.join(out)


# ---------------------------------------------------------------- privacidad y soporte

def build_privacy(code):
    t = T[code]
    p = t['privacy']
    path = t['paths']['privacy']
    prefix = depth_prefix(path)
    links = {
        '{support}': f'<a href="{prefix}{t["paths"]["support"]}">{esc(p["support_link"])}</a>',
        '{apple_privacy}': f'<a href="{p["apple_privacy_url"]}">{esc(p["apple_privacy_link"])}</a>',
    }
    body = []
    for title, content in p['sections']:
        for k, v in links.items():
            content = content.replace(k, v)
        body.append(f'<h2>{esc(title)}</h2>\n{content}')
    out = [head(code, 'privacy', p['meta_title'], p['description'], prefix, noindex=True),
           header(code, 'privacy', prefix),
           f'''<main id="contenido" class="texto">
<h1>{esc(p["title"])}</h1>
<p class="fecha">{esc(p["updated"])}</p>
<div class="destacado"><p>{p["highlight"]}</p></div>
{chr(10).join(body)}
</main>
''', footer(code, prefix)]
    return path, ''.join(out)


def build_support(code):
    t = T[code]
    s = t['support']
    path = t['paths']['support']
    prefix = depth_prefix(path)
    faq = '\n'.join(f'<details class="pregunta"><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in s['faq'])
    out = [head(code, 'support', s['meta_title'], s['description'], prefix),
           header(code, 'support', prefix),
           f'''<main id="contenido" class="texto">
<h1>{esc(s["title"])}</h1>
<p class="fecha">{esc(s["lead"])}</p>
<!-- CONTACTO: cambiar «contact» en tools/textos/*.json por el enlace al formulario de Google cuando exista. -->
<div class="destacado"><p>{s["contact"]}</p></div>
<h2>{esc(s["faq_title"])}</h2>
{faq}
<p class="enlaces"><a href="{prefix}{t["paths"]["privacy"]}">{esc(s["privacy_link"])}</a></p>
</main>
''', footer(code, prefix)]
    return path, ''.join(out)


def build_404():
    links = ''.join(f'<li><a href="/ludeum/{T[c]["paths"]["home"]}" lang="{T[c]["html_lang"]}">{esc(T[c]["label"])}</a></li>' for c in LANGS)
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ludéum · 404</title>
<meta name="robots" content="noindex">
<link rel="icon" type="image/png" href="/ludeum/img/favicon-32.png">
<link rel="stylesheet" href="/ludeum/estilo.css">
</head>
<body>
<main id="contenido" class="texto centrado">
<img src="/ludeum/img/icono-192.webp" width="96" height="96" alt="">
<h1>404</h1>
<p>Esta sala del museo no existe. · This room of the museum doesn’t exist.</p>
<ul class="lista-idiomas">{links}</ul>
</main>
</body>
</html>
'''


def write(path, content):
    full = os.path.join(ROOT, path, 'index.html') if not path.endswith('.html') else os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)


def main():
    pages = []
    for code in LANGS:
        for build in (build_home, build_privacy, build_support):
            path, content = build(code)
            write(path, content)
            pages.append(path)
    write('404.html', build_404())
    # Sitemap: inicio y soporte (privacidad va con noindex)
    urls = []
    for kind in ('home', 'support'):
        for code in LANGS:
            alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{T[c]["html_lang"]}" href="{url(c, kind)}"/>' for c in LANGS)
            urls.append(f'<url><loc>{url(code, kind)}</loc>{alts}</url>')
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                + '\n'.join(urls) + '\n</urlset>\n')
    print(len(pages), 'páginas:', ', '.join(p or '/' for p in pages))


if __name__ == '__main__':
    main()
