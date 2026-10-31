import random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H = 1080, 1440
F = '/home/claude/fonts/'
ANTON = F + 'Anton-Regular.ttf'
MONO = F + 'SpaceMono-Bold.ttf'
MONOR = F + 'SpaceMono-Regular.ttf'
VT = F + 'VT323-Regular.ttf'
INTER = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
INTERM = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
INTERX = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
OR = (255, 122, 26)
WH = (245, 243, 238)
GR = (150, 150, 160)
RED = (255, 48, 64)
OUT = '/home/claude/rotto/out/'


def f(p, s):
    return ImageFont.truetype(p, s)


def bg(seed, tint=(40, 8, 60)):
    random.seed(seed)
    im = Image.new('RGB', (W, H), (6, 6, 9))
    # radial glow
    g = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(g)
    d.ellipse((-300, 250, W + 300, 1250), fill=255)
    g = g.filter(ImageFilter.GaussianBlur(260))
    col = Image.new('RGB', (W, H), tint)
    im = Image.composite(col, im, g.point(lambda v: int(v * 0.55)))
    return im


def finish(im):
    # scanlines
    sl = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(sl)
    for y in range(0, H, 4):
        d.line((0, y, W, y), fill=38)
    im = Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), im, sl)
    # noise
    n = Image.effect_noise((W, H), 28).convert('RGB')
    im = ImageChops.add(im, ImageChops.multiply(n, Image.new('RGB', (W, H), (40, 40, 40))), 1, -14)
    # vignette
    v = Image.new('L', (W, H), 0)
    ImageDraw.Draw(v).rectangle((60, 60, W - 60, H - 60), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(120))
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), v.point(lambda x: 90 + int(x * 165 / 255)))
    return im


def rgb_split(layer, dx=6):
    r, g, b, a = layer.split()
    r = ImageChops.offset(r, -dx, 0)
    b = ImageChops.offset(b, dx, 0)
    return Image.merge('RGBA', (r, g, b, a))


def glitch_slices(layer, seed, n=7, amp=40):
    random.seed(seed)
    out = layer.copy()
    w, h = layer.size
    for _ in range(n):
        y = random.randint(0, h - 20)
        hh = random.randint(6, 34)
        dx = random.randint(-amp, amp)
        strip = layer.crop((0, y, w, y + hh))
        out.paste(Image.new('RGBA', (w, hh), (0, 0, 0, 0)), (0, y))
        out.paste(strip, (dx, y))
    return out


def text_c(d, xy, s, font, fill, anchor='mm'):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def header(im, label='SPECIALE HALLOWEEN'):
    d = ImageDraw.Draw(im)
    d.text((64, 62), 'KILL & CHILL', font=f(ANTON, 44), fill=WH)
    tw = d.textlength(label, font=f(INTERX, 24))
    x1 = W - 64
    d.rounded_rectangle((x1 - tw - 44, 62, x1, 108), radius=23, fill=OR)
    d.text((x1 - 22, 85), label, font=f(INTERX, 24), fill=(12, 8, 6), anchor='rm')


def screen_panel(content_fn, seed, box=(70, 170, W - 70, 760), glitch=True, tint=(18, 18, 26)):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, fill=tint + (255,), outline=(70, 70, 86, 255), width=3)
    content_fn(layer, d, w, h)
    if glitch:
        layer = glitch_slices(layer, seed, n=0, amp=0)
        layer = rgb_split(layer, 3)
    return layer, (x0, y0)


def paste_glow(im, layer, pos, color=OR, strength=0.35):
    a = layer.split()[3].filter(ImageFilter.GaussianBlur(40))
    glow = Image.new('RGB', im.size, color)
    m = Image.new('L', im.size, 0)
    m.paste(a, pos)
    im = Image.composite(glow, im, m.point(lambda v: int(v * strength)))
    im.paste(layer, pos, layer)
    return im


def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    lines.append(cur)
    return lines


def body(im, num, game, meta, title_lines, text, source, cta):
    d = ImageDraw.Draw(im)
    y = 800
    # number + game
    d.text((64, y), num, font=f(ANTON, 120), fill=OR, anchor='lt')
    nw = d.textlength(num, font=f(ANTON, 120))
    d.text((64 + nw + 26, y + 18), game, font=f(ANTON, 50), fill=WH, anchor='lt')
    d.text((64 + nw + 28, y + 86), meta, font=f(INTERM, 24), fill=GR, anchor='lt')
    y += 168
    for ln in title_lines:
        d.text((64, y), ln, font=f(ANTON, 70), fill=WH, anchor='lt')
        y += 84
    y += 10
    for ln in wrap(d, text, f(INTERM, 31), W - 128):
        d.text((64, y), ln, font=f(INTERM, 31), fill=(205, 205, 212), anchor='lt')
        y += 44
    # footer
    d.text((64, H - 70), source, font=f(INTERM, 21), fill=(120, 120, 130), anchor='lm')
    cw = d.textlength(cta + '  →', font=f(INTERX, 25))
    d.rounded_rectangle((W - 64 - cw - 64, H - 96, W - 64, H - 44), radius=26, outline=OR, width=3)
    d.text((W - 64 - 34, H - 70), cta + '  →', font=f(INTERX, 25), fill=OR, anchor='rm')
    return y


# ---------- screens ----------
def dialog_delete(layer, d, w, h, big=False):
    # fake memory-card dialog (original design)
    d.rectangle((0, 0, w, h), fill=None)
    bx0, by0, bx1, by1 = 60, 40, w - 60, h - 40
    d.rectangle((bx0, by0, bx1, by1), fill=(10, 10, 14, 255), outline=(230, 230, 230, 255), width=4)
    d.rectangle((bx0 + 10, by0 + 10, bx1 - 10, by1 - 10), outline=(120, 120, 130, 255), width=2)
    cx = w // 2
    d.text((cx, by0 + 62), 'MEMORY CARD - SLOT A', font=f(VT, 44), fill=(160, 160, 170, 255), anchor='mm')
    d.text((cx, by0 + 135), 'Vuoi cancellare TUTTI', font=f(VT, 70), fill=(250, 250, 250, 255), anchor='mm')
    d.text((cx, by0 + 198), 'i tuoi salvataggi?', font=f(VT, 70), fill=(250, 250, 250, 255), anchor='mm')
    py = by0 + 262
    d.rectangle((bx0 + 60, py, bx1 - 60, py + 44), outline=(230, 230, 230, 255), width=3)
    fillw = int((bx1 - 60 - (bx0 + 60) - 12) * 0.87)
    d.rectangle((bx0 + 66, py + 6, bx0 + 66 + fillw, py + 38), fill=(255, 48, 64, 255))
    d.text((cx, py + 82), 'ELIMINAZIONE... 87%', font=f(VT, 46), fill=(255, 80, 90, 255), anchor='mm')
    by = by1 - 62
    d.rectangle((cx - 230, by - 32, cx - 40, by + 32), fill=(250, 250, 250, 255))
    d.text((cx - 135, by), 'SÌ', font=f(VT, 54), fill=(10, 10, 10, 255), anchor='mm')
    d.rectangle((cx + 40, by - 32, cx + 230, by + 32), outline=(250, 250, 250, 255), width=3)
    d.text((cx + 135, by), 'NO', font=f(VT, 54), fill=(250, 250, 250, 255), anchor='mm')


def scr_batman(layer, d, w, h):
    random.seed(5)
    # frozen frame: dark gotham-like gradient + vertical corrupted bars
    for y in range(h):
        c = int(14 + 30 * (y / h))
        d.line((0, y, w, y), fill=(c, c + 4, c + 14, 255))
    for i in range(60):
        x = random.randint(0, w)
        ww = random.randint(4, 40)
        col = random.choice([(40, 255, 120), (255, 40, 200), (40, 200, 255), (240, 240, 240)])
        d.rectangle((x, random.randint(0, h // 2), x + ww, random.randint(h // 2, h)), fill=col + (random.randint(40, 140),))
    d.rectangle((0, h // 2 - 70, w, h // 2 + 70), fill=(0, 0, 0, 220))
    d.text((w // 2, h // 2 - 22), 'IL GIOCO NON RISPONDE', font=f(VT, 64), fill=(255, 255, 255, 255), anchor='mm')
    d.text((w // 2, h // 2 + 34), 'riavvio in corso...', font=f(VT, 42), fill=(180, 180, 190, 255), anchor='mm')
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(70, 70, 86, 255), width=3)


def scr_hell(layer, d, w, h):
    for y in range(h):
        c = int(8 + 18 * (y / h))
        d.line((0, y, w, y), fill=(c + 6, c, c, 255))
    # rot tendrils
    random.seed(11)
    for _ in range(26):
        x, y = random.randint(40, w - 40), h - 10
        pts = [(x, y)]
        for _ in range(14):
            x += random.randint(-30, 30)
            y -= random.randint(14, 34)
            pts.append((x, y))
        d.line(pts, fill=(25, 10, 12, 255), width=random.randint(4, 10), joint='curve')
    lines = ['Il marciume cresce', 'ogni volta che muori.', '', 'Se arriva alla testa,', 'PERDI TUTTI', 'I PROGRESSI.']
    yy = 110
    for ln in lines:
        col = (255, 60, 70, 255) if ln.isupper() else (240, 236, 230, 255)
        d.text((w // 2, yy), ln, font=f(ANTON, 58 if ln.isupper() else 46), fill=col, anchor='mm')
        yy += 66 if ln else 30
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(70, 70, 86, 255), width=3)


def window(d, x0, y0, x1, y1, title):
    d.rectangle((x0, y0, x1, y1), fill=(235, 235, 238, 255))
    d.rectangle((x0, y0, x1, y0 + 46), fill=(40, 40, 52, 255))
    d.text((x0 + 18, y0 + 23), title, font=f(MONOR, 22), fill=(230, 230, 235, 255), anchor='lm')
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse((x1 - 110 + i * 32, y0 + 14, x1 - 92 + i * 32, y0 + 32), fill=c + (255,))


def scr_ddlc(layer, d, w, h):
    d.rectangle((0, 0, w, h), fill=(16, 16, 22, 255))
    window(d, 60, 50, w - 60, h - 50, 'characters')
    files = [('sayori.chr', True), ('natsuki.chr', True), ('yuri.chr', True), ('monika.chr', False)]
    y = 130
    for name, gone in files:
        col = (150, 150, 155, 255) if gone else (20, 20, 24, 255)
        d.rectangle((110, y, 150, y + 48), outline=col, width=3)
        d.text((180, y + 24), name, font=f(MONO, 36), fill=col, anchor='lm')
        if gone:
            tw = d.textlength(name, font=f(MONO, 36))
            d.line((172, y + 26, 190 + tw, y + 26), fill=(255, 48, 64, 255), width=5)
            d.text((w - 110, y + 24), 'ELIMINATO', font=f(MONO, 26), fill=(255, 48, 64, 255), anchor='rm')
        else:
            d.rectangle((100, y - 10, w - 100, y + 58), outline=(255, 122, 26, 255), width=4)
            d.text((w - 110, y + 24), 'cancellalo TU', font=f(MONO, 26), fill=(255, 122, 26, 255), anchor='rm')
        y += 92
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(70, 70, 86, 255), width=3)


def scr_imscared(layer, d, w, h):
    # desktop
    for y in range(h):
        d.line((0, y, w, y), fill=(10, 40 + int(30 * y / h), 90 + int(40 * y / h), 255))
    def icon(x, y, label, folder=True, hl=False):
        if folder:
            d.rectangle((x, y + 14, x + 110, y + 90), fill=(250, 200, 70, 255))
            d.rectangle((x, y, x + 50, y + 20), fill=(250, 200, 70, 255))
        else:
            d.rectangle((x + 15, y, x + 95, y + 100), fill=(250, 250, 250, 255))
            for k in range(5):
                d.line((x + 28, y + 22 + k * 15, x + 82, y + 22 + k * 15), fill=(150, 150, 160, 255), width=3)
        if hl:
            d.rectangle((x - 22, y - 16, x + 132, y + 160), outline=(255, 48, 64, 255), width=4)
        d.text((x + 55, y + 130), label, font=f(MONO, 26), fill=(255, 255, 255, 255), anchor='mm')
    icon(90, 70, 'Cestino', folder=False)
    icon(90, 290, 'Documenti')
    icon(w // 2 - 55, 170, 'IMSCARED', hl=False)
    icon(w - 260, 300, 'heart.txt', folder=False, hl=True)
    d.text((w - 205, 260), 'È APPARSO DA SOLO', font=f(MONO, 22), fill=(255, 220, 220, 255), anchor='mm')
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(70, 70, 86, 255), width=3)


def scr_cover(layer, d, w, h):
    d.rectangle((0, 0, w, h), fill=(8, 8, 12, 255))
    dialog_delete(layer, d, w, h)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(90, 90, 110, 255), width=3)


def scr_ed(layer, d, w, h):
    d.rectangle((0, 0, w, h), fill=(8, 8, 12, 255))
    dialog_delete(layer, d, w, h)
    # cursor on SI
    cx = w // 2 - 135
    d.polygon([(cx + 40, h - 110), (cx + 40, h - 60), (cx + 54, h - 72), (cx + 66, h - 48), (cx + 76, h - 53), (cx + 64, h - 77), (cx + 82, h - 77)], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(90, 90, 110, 255), width=3)


def save(im, name):
    finish(im).save(OUT + name, quality=93)


import os
os.makedirs(OUT, exist_ok=True)

# ---- 1 COVER ----
im = bg(1, (70, 10, 20))
header(im)
layer, pos = screen_panel(scr_cover, 3, box=(70, 160, W - 70, 760))
im = paste_glow(im, layer, pos, RED, 0.45)
d = ImageDraw.Draw(im)
y = 812
for ln, col in [('5 GIOCHI HORROR', WH), ('CHE FINGONO DI', WH), ('ROVINARTI TUTTO', OR)]:
    # chromatic text
    for off, c in [(-4, (0, 220, 255)), (4, (255, 30, 60))]:
        d.text((64 + off, y), ln, font=f(ANTON, 118), fill=c, anchor='lt')
    d.text((64, y), ln, font=f(ANTON, 118), fill=col, anchor='lt')
    y += 140
d.text((64, y + 22), 'Il n.1 ti cancella i salvataggi. O almeno così sembra.', font=f(INTERM, 33), fill=(215, 215, 222), anchor='lt')
d.text((64, H - 70), '@killandchill_gg', font=f(INTERM, 24), fill=(140, 140, 150), anchor='lm')
d.text((W - 64, H - 70), 'SCORRI  →', font=f(INTERX, 30), fill=OR, anchor='rm')
save(im, '1.jpg')

# ---- 2 BATMAN ----
im = bg(2, (20, 30, 70))
header(im)
layer, pos = screen_panel(scr_batman, 21)
im = paste_glow(im, layer, pos, (60, 120, 255), 0.35)
body(im, '#5', 'BATMAN: ARKHAM ASYLUM', '2009 · PC, PS3, XBOX 360',
     ['IL GIOCO SI BLOCCA', 'E RIPARTE DA CAPO'],
     "Contro lo Spaventapasseri l'immagine si rompe come in un crash vero. Poi riparte il filmato iniziale... ma alla guida c'è il Joker.",
     'Fonte: Batman Wiki · IGN', 'N.4')
save(im, '2.jpg')

# ---- 3 HELLBLADE ----
im = bg(3, (70, 14, 14))
header(im)
layer, pos = screen_panel(scr_hell, 31)
im = paste_glow(im, layer, pos, RED, 0.35)
body(im, '#4', "HELLBLADE: SENUA'S SACRIFICE", '2017 · PC, PS4, XBOX',
     ['MUORI TROPPO?', 'PERDI TUTTO. O NO?'],
     "All'inizio il gioco ti minaccia: se il marciume arriva alla testa, addio progressi. Era un bluff: PCGamesN è morto 50 volte e non è successo niente.",
     'Fonte: PCGamesN · Game Informer', 'N.3')
save(im, '3.jpg')

# ---- 4 DDLC ----
im = bg(4, (70, 20, 60))
header(im)
layer, pos = screen_panel(scr_ddlc, 41)
im = paste_glow(im, layer, pos, (255, 90, 180), 0.32)
body(im, '#3', 'DOKI DOKI LITERATURE CLUB', '2017 · PC, CONSOLE',
     ['CANCELLA I PERSONAGGI', 'DAL TUO COMPUTER'],
     "Sembra un gioco di appuntamenti carino. Poi i file delle ragazze spariscono dalla cartella del gioco, e per andare avanti devi cancellare tu monika.chr.",
     'Fonte: Doki Doki Literature Club Wiki', 'N.2')
save(im, '4.jpg')

# ---- 5 IMSCARED ----
im = bg(5, (10, 40, 80))
header(im)
layer, pos = screen_panel(scr_imscared, 51)
im = paste_glow(im, layer, pos, (60, 160, 255), 0.32)
y = body(im, '#2', 'IMSCARED', '2016 · PC · DI UN ITALIANO 🇮🇹'.replace(' 🇮🇹', ''),
     ['TI LASCIA FILE', 'SUL DESKTOP'],
     "Crea una cartella sul tuo desktop e ti scrive messaggi. Se ti prende, si chiude e mostra una finta schermata di errore. Per vincere devi cancellare heart.txt. L'ha creato l'italiano Ivan Zanotti.",
     'Fonte: Wikipedia · Steam', 'N.1')
save(im, '5.jpg')

# ---- 6 ETERNAL DARKNESS ----
im = bg(6, (90, 10, 18))
header(im)
layer, pos = screen_panel(scr_ed, 61)
im = paste_glow(im, layer, pos, RED, 0.5)
body(im, '#1', 'ETERNAL DARKNESS', '2002 · NINTENDO GAMECUBE',
     ['TI CANCELLA TUTTI', 'I SALVATAGGI'],
     "Quando la sanità mentale è bassa e provi a salvare, ti chiede se vuoi cancellare tutto. Qualunque cosa scegli, spariscono. Era finto: rientri nel menu e sono ancora lì.",
     'Fonte: Nintendo Life · StrategyWiki', 'E TU?')
save(im, '6.jpg')

# ---- 7 CTA ----
im = bg(7, (60, 10, 50))
header(im)
d = ImageDraw.Draw(im)
d.text((W // 2, 300), 'QUALE TI AVREBBE FATTO', font=f(ANTON, 76), fill=WH, anchor='mm')
d.text((W // 2, 390), 'SPEGNERE TUTTO?', font=f(ANTON, 104), fill=OR, anchor='mm')
items = ['5  ARKHAM ASYLUM · finto crash', '4  HELLBLADE · minaccia di cancellare', '3  DOKI DOKI · cancella i file',
         '2  IMSCARED · file sul desktop', '1  ETERNAL DARKNESS · salvataggi finti']
y = 520
for it in items:
    d.rounded_rectangle((90, y, W - 90, y + 92), radius=18, fill=(20, 18, 26), outline=(70, 66, 84), width=2)
    num, rest = it.split('  ', 1)
    d.text((140, y + 46), num, font=f(ANTON, 54), fill=OR, anchor='mm')
    d.text((190, y + 46), rest, font=f(INTERX, 32), fill=WH, anchor='lm')
    y += 112
d.text((W // 2, y + 60), 'Scrivi il numero nei commenti 👇'.replace(' 👇', ''), font=f(INTERX, 36), fill=WH, anchor='mm')
d.rounded_rectangle((W // 2 - 380, y + 120, W // 2 + 380, y + 196), radius=38, fill=OR)
d.text((W // 2, y + 158), 'Mandalo a chi gioca al buio con le cuffie', font=f(INTERX, 30), fill=(14, 10, 8), anchor='mm')
d.text((W // 2, H - 70), 'Segui @killandchill_gg', font=f(INTERM, 26), fill=(160, 160, 170), anchor='mm')
save(im, '7.jpg')

# ---- STORY 1080x1920 from cover ----
cov = Image.open(OUT + '1.jpg')
st = Image.new('RGB', (1080, 1920), (6, 6, 9))
st.paste(cov.resize((1000, 1333)), (40, 240))
ds = ImageDraw.Draw(st)
ds.text((540, 140), 'NUOVO POST', font=f(ANTON, 90), fill=OR, anchor='mm')
ds.text((540, 1700), 'Tocca qui sotto per vederlo', font=f(INTERX, 40), fill=WH, anchor='mm')
st.save(OUT + 'storia.jpg', quality=92)

# contact sheet
ims = [Image.open(OUT + f'{i}.jpg').resize((540, 720)) for i in range(1, 8)]
c = Image.new('RGB', (540 * 4, 720 * 2), (0, 0, 0))
for k, x in enumerate(ims):
    c.paste(x, ((k % 4) * 540, (k // 4) * 720))
c.save('/home/claude/rotto/sheet.jpg', quality=85)
print('ok')
