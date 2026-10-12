"""Saca de la app (repo ludus) los datos de los juegos en los 7 idiomas → tools/datos.json.
Uso: python3 tools/extraer_datos.py <ruta del repo de la app>"""
import json, re, sys, os

APP = sys.argv[1]
LANGS = ['es', 'en', 'fr', 'de', 'pt-BR', 'ca', 'it']
strings = json.load(open(os.path.join(APP, 'Ludeum/Localizable.xcstrings')))['strings']

def tr(s):
    out = {'es': s}
    loc = strings.get(s, {}).get('localizations', {})
    for l in LANGS[1:]:
        v = loc.get(l, {}).get('stringUnit', {}).get('value')
        out[l] = v if v else s
    return out

def switch(src, prop):
    """Valores de `var <prop>: String { switch self { case .x: … } }`."""
    m = re.search(r'var ' + prop + r': String \{\s*switch self \{(.*?)\n        \}', src, re.S)
    res = {}
    for line in m.group(1).splitlines():
        c = re.match(r'\s*case \.(\w+): (?:String\(localized: )?"(.*)"\)?\s*$', line)
        if c:
            res[c.group(1)] = c.group(2)
    return res

cat = open(os.path.join(APP, 'Ludeum/Home/GameCatalog.swift')).read()
ids = re.search(r'enum GameID.*?\n    case (.*?)\n', cat, re.S).group(1).replace(' ', '').split(',')
hall_of = {}
for line in re.search(r'var hall: GameHall \{\s*switch self \{(.*?)\n        \}', cat, re.S).group(1).splitlines():
    c = re.match(r'\s*case (.*?): \.(\w+)', line)
    if c:
        for g in re.findall(r'\.(\w+)', c.group(1)):
            hall_of[g] = c.group(2)
order = {}
for line in re.search(r'var hallOrder: Int \{\s*switch self \{(.*?)\n        \}', cat, re.S).group(1).splitlines():
    c = re.match(r'\s*case \.(\w+): (\d+)', line)
    if c:
        order[c.group(1)] = int(c.group(2))

rivsrc = open(os.path.join(APP, 'Ludeum/Core/Rival.swift')).read()
def lit(x):
    x = x.strip()
    m = re.match(r'String\(localized: "(.*)"\)$', x)
    return m.group(1) if m else x.strip('"')
rivals = {}
for g, body in re.findall(r'\.(\w+): \[(\(.*?\))\],\n', rivsrc):
    rivals[g] = [{'name': tr(lit(n)), 'role': tr(lit(r)) if lit(r) else None}
                 for n, r in re.findall(r'\(((?:String\(localized: )?"[^"]*"\)?), ((?:String\(localized: )?"[^"]*"\)?)\)', body)]

props = {p: switch(cat, p) for p in ['name', 'subtitle', 'origin', 'blurb']}
nvariants = {g: len(re.findall(r'\.\w+', v)) for g, v in re.findall(r'case \.(\w+): \[([^\]]*)\]', re.search(r'var variants: \[GameVariant\] \{(.*?)\n    \}', cat, re.S).group(1))}
games = [{'id': g, 'hall': hall_of[g], 'order': order[g],
          **{p: tr(props[p][g]) for p in props}, 'variants': nvariants[g], 'rivals': rivals[g]} for g in ids]

halls = {}
for h, t in switch(cat, 'title').items():
    halls[h] = {'title': tr(t), 'span': tr(switch(cat, 'span')[h])}

up = open(os.path.join(APP, 'Ludeum/Home/UpcomingGames.swift')).read()
uids = re.findall(r'case \.(\w+): "', re.search(r'var name: String \{(.*?)\n    \}', up, re.S).group(1))
uprops = {p: switch(up, p) for p in ['name', 'subtitle', 'origin']}
uhall = {}
for line in re.search(r'var hall: GameHall \{\s*switch self \{(.*?)\n        \}', up, re.S).group(1).splitlines():
    c = re.match(r'\s*case (.*?): \.(\w+)', line)
    if c:
        for g in re.findall(r'\.(\w+)', c.group(1)):
            uhall[g] = c.group(2)
enum_order = re.findall(r'\w+', ' '.join(re.findall(r'^    case ([\w, ]+)$', up.split('var id')[0], re.M)))
upcoming = [{'id': g, 'hall': uhall[g], **{p: tr(uprops[p][g]) for p in uprops}} for g in enum_order]

json.dump({'games': games, 'halls': halls, 'upcoming': upcoming}, open(os.path.join(os.path.dirname(__file__), 'datos.json'), 'w'), ensure_ascii=False, indent=1)
print(len(games), 'juegos,', len(upcoming), 'próximamente,', sum(len(r) for r in rivals.values()), 'rivales')
