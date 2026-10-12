"""Optimiza para web las capturas, los retratos de los rivales y el ícono → img/.
Uso: python3 tools/imagenes.py <repo de la app>
Las capturas originales viven fuera del repo (Escritorio y Descargas de Carlos);
si falta una, se avisa y se conserva la versión ya generada en img/."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

APP = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'img')
HOME = os.path.expanduser('~')
DESK = os.path.join(HOME, 'Desktop', 'Simulator Screenshot - iPhone 17 - 2026-10-11 at {}.png')
DL = os.path.join(HOME, 'Downloads', 'Ludeum capturas', '{}.png')

# id → (archivo, recorte (izq, arriba, der, abajo) en fracción, anchos)
PHONE = (360, 720)
WIDE = (720, 1280)
CAPTURAS = {
    'inicio':        (DESK.format('18.24.10'), None, PHONE),
    'partidas':      (DESK.format('18.26.27'), None, PHONE),
    'torneos':       (DESK.format('18.26.33'), None, PHONE),
    'ur-detalle':    (DESK.format('18.25.04'), None, PHONE),
    'tavli-detalle': (DESK.format('18.26.18'), None, PHONE),
    'ur':            (DESK.format('19.08.58'), None, PHONE),
    'pente':         (DESK.format('19.09.52'), None, PHONE),
    'latrunculi':    (DESK.format('19.21.23'), None, PHONE),
    'hnefatafl':     (DESK.format('19.22.06'), None, PHONE),
    'tavli':         (DESK.format('19.25.22'), None, PHONE),
    'cribbage':      (DESK.format('19.26.04'), None, PHONE),
    # Las de la ficha (10 oct) tienen la barra de pestañas vieja: se recorta abajo.
    'historia-ur':   (DL.format('iPhone/08-historia-ur'), (0, 0, 1, 0.86), PHONE),
    'logros':        (DL.format('iPhone/10-logros-oscuro'), (0, 0, 1, 0.86), PHONE),
    'patolli-rival': (DL.format('iPhone/09-configuracion-patolli-un-jugador'), None, PHONE),
    # Apaisadas: fuera la Dynamic Island de la izquierda (y lo mismo a la derecha).
    'ur-mesa':       (DL.format('iPhone/02-ur-realista'), (0.055, 0, 0.945, 1), WIDE),
    'oware-oscuro':  (DL.format('iPhone/05-oware-realista-oscuro'), (0.055, 0, 0.945, 1), WIDE),
    'hnefatafl-mesa': (DL.format('iPhone/13-hnefatafl-un-jugador'), (0.055, 0, 0.945, 1), WIDE),
    'konane':        (DL.format('iPhone/11-konane-realista'), (0.055, 0, 0.945, 1), WIDE),
    # iPad
    'ipad-inicio':   (DL.format('iPad vertical/01-inicio'), None, (480, 960)),
    'ipad-historia': (DL.format('iPad horizontal/08-historia-hnefatafl'), (0, 0, 0.97, 0.97), (720, 1280)),
}

def save(im, base, widths, quality=80):
    for w in widths:
        t = im.copy()
        if t.width > w:
            t = t.resize((w, round(t.height * w / t.width)), Image.LANCZOS)
        t.save(f'{base}-{w}.webp', 'WEBP', quality=quality, method=6)

def crop(im, c):
    if not c:
        return im
    W, H = im.size
    return im.crop((round(c[0] * W), round(c[1] * H), round(c[2] * W), round(c[3] * H)))

os.makedirs(os.path.join(OUT, 'capturas'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'rivales'), exist_ok=True)
sizes = {}
for k, (src, c, widths) in CAPTURAS.items():
    if not os.path.exists(src):
        print('FALTA', src)
        continue
    im = crop(Image.open(src).convert('RGB'), c)
    save(im, os.path.join(OUT, 'capturas', k), widths)
    sizes[k] = im.size

# Retratos: archivo del arte → id de juego de la app
RIV = {'ur': 'ur', 'pente': 'penteGrammai', 'latrunculi': 'latrunculi', 'scripta': 'xiiScripta',
       'morris': 'morris', 'hnefatafl': 'hnefatafl', 'ninemorris': 'nineMorris', 'oware': 'oware',
       'patolli': 'patolli', 'konane': 'konane', 'tavli': 'tavli', 'cribbage': 'cribbage', 'conquian': 'conquian'}
for f, g in RIV.items():
    for i, d in enumerate(['facil', 'normal', 'dificil']):
        im = Image.open(os.path.join(APP, 'Arte', 'rivales', f'{f}_{d}.jpg')).convert('RGB')
        save(im, os.path.join(OUT, 'rivales', f'{g}-{i}'), (128, 256), quality=78)

# Ícono: favicon, apple-touch-icon y logo
icon = Image.open(os.path.join(APP, 'Ludeum', 'Assets.xcassets', 'AppIcon.appiconset', 'icon.png')).convert('RGB')
icon.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, 'apple-touch-icon.png'), optimize=True)
icon.resize((32, 32), Image.LANCZOS).save(os.path.join(OUT, 'favicon-32.png'), optimize=True)
icon.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT, 'icono-512.png'), optimize=True)
save(icon, os.path.join(OUT, 'icono'), (96, 192))

# Imagen para compartir (Open Graph / Twitter), 1200×630 JPEG
fondo = Image.open(os.path.join(APP, 'Arte', 'torneos', 'fondo.png')).convert('RGB')
og = fondo.resize((1200, round(fondo.height * 1200 / fondo.width)), Image.LANCZOS)
og = og.crop((0, 0, 1200, og.height)).resize((1200, 630), Image.LANCZOS) if og.height < 630 else og.crop((0, (og.height - 630) // 2, 1200, (og.height - 630) // 2 + 630))
og = Image.blend(og, Image.new('RGB', og.size, (14, 28, 27)), 0.55)
d = ImageDraw.Draw(og)
ic = icon.resize((150, 150), Image.LANCZOS)
mask = Image.new('L', ic.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, 149, 149), 34, fill=255)
og.paste(ic, (90, 150), mask)
serif = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
sans = '/System/Library/Fonts/Supplemental/Georgia Italic.ttf'
d.text((90, 330), 'Ludéum', font=ImageFont.truetype(serif, 92), fill=(239, 227, 200))
d.text((92, 445), 'Juegos de mesa con historia', font=ImageFont.truetype(sans, 32), fill=(216, 180, 106))
d.text((92, 488), 'Board games with a history', font=ImageFont.truetype(sans, 32), fill=(216, 180, 106))
d.text((92, 545), '13 juegos · iPhone · iPad', font=ImageFont.truetype(sans, 24), fill=(200, 190, 170))
for k, x, y in (('inicio', 690, 40), ('hnefatafl', 940, 95)):
    p = os.path.join(OUT, 'capturas', f'{k}-360.webp')
    if os.path.exists(p):
        s = Image.open(p).convert('RGB').resize((230, 500), Image.LANCZOS)
        m = Image.new('L', s.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 229, 499), 30, fill=255)
        og.paste(s, (x, y), m)
og.save(os.path.join(OUT, 'compartir.jpg'), 'JPEG', quality=84, optimize=True, progressive=True)
print('listo', len(sizes), 'capturas')
for k, v in sizes.items():
    print(k, v)

# Fondo del encabezado: la sala de torneos de la app
sala = Image.open(os.path.join(APP, 'Arte', 'torneos', 'fondo.png')).convert('RGB')
save(sala, os.path.join(OUT, 'fondo-sala'), (1000, 2000), quality=70)
