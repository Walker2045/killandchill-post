import os, random
src = open('/home/claude/rotto/make.py').read()
exec(src[:src.index('import os\nos.makedirs')])
OUT = '/home/claude/rotto/v2/'
os.makedirs(OUT, exist_ok=True)
TOTAL = 8


def top(im, n, pill=None):
    d = ImageDraw.Draw(im)
    d.text((64, 66), 'KILL & CHILL', font=f(ANTON, 40), fill=(200, 200, 205))
    if pill:
        tw = d.textlength(pill, font=f(INTERX, 24))
        d.rounded_rectangle((W - 64 - tw - 44, 64, W - 64, 110), radius=23, fill=OR)
        d.text((W - 86, 87), pill, font=f(INTERX, 24), fill=(12, 8, 6), anchor='rm')
    else:
        d.text((W - 64, 88), f'{n}/{TOTAL}', font=f(INTERX, 30), fill=(175, 175, 185), anchor='rm')


def big_text(im, y, lines, sub=None, sw=W - 128):
    d = ImageDraw.Draw(im)
    for ln, col in lines:
        d.text((64, y), ln, font=f(ANTON, 96), fill=col, anchor='lt')
        y += 112
    if sub:
        y += 36
        for ln in wrap(d, sub, f(INTERM, 38), sw):
            d.text((64, y), ln, font=f(INTERM, 38), fill=(212, 212, 218), anchor='lt')
            y += 52
    return y


def swipe(im, txt='SCORRI'):
    d = ImageDraw.Draw(im)
    d.text((W - 64, H - 72), txt + '  →', font=f(INTERX, 30), fill=OR, anchor='rm')


def src_line(im, s):
    d = ImageDraw.Draw(im)
    d.text((64, H - 72), s, font=f(INTERM, 26), fill=(160, 160, 170), anchor='lm')


def panel(im, fn, box, color, strength=0.4):
    layer, pos = screen_panel(fn, 1, box=box)
    im = paste_glow(im, layer, pos, color, strength)
    ImageDraw.Draw(im).text((box[2] - 14, box[3] + 22), 'ricostruzione grafica', font=f(INTERM, 24), fill=(150, 150, 160), anchor='rm')
    return im


# --- screens ---
def scr_dialog(cursor_on='SI', pct=87):
    def fn(layer, d, w, h):
        d.rectangle((0, 0, w, h), fill=(8, 8, 12, 255))
        dialog_delete(layer, d, w, h)
        cx = w // 2 + (-60 if cursor_on == 'SI' else 210)
        by = h - 40 - 50
        d.polygon([(cx + 40, by + 8), (cx + 40, by + 58), (cx + 54, by + 46), (cx + 66, by + 70), (cx + 76, by + 65), (cx + 64, by + 41), (cx + 82, by + 41)], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
        d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(90, 90, 110, 255), width=3)
    return fn


def scr_gc(layer, d, w, h):
    d.rectangle((0, 0, w, h), fill=(14, 10, 26, 255))
    d.text((w // 2, h // 2 - 70), '2002', font=f(ANTON, 230), fill=(255, 255, 255, 255), anchor='mm')
    d.text((w // 2, h // 2 + 110), 'NINTENDO GAMECUBE', font=f(MONO, 44), fill=(170, 150, 255, 255), anchor='mm')
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(90, 90, 110, 255), width=3)


def scr_bar(layer, d, w, h):
    d.rectangle((0, 0, w, h), fill=(8, 10, 8, 255))
    d.text((70, 90), 'SANITÀ MENTALE', font=f(MONO, 40), fill=(150, 255, 150, 255), anchor='lm')
    for i, (lvl, lab) in enumerate([(0.9, 'tutto normale'), (0.45, 'qualcosa non va'), (0.08, 'il gioco impazzisce')]):
        y = 170 + i * 120
        d.rectangle((70, y, w - 70, y + 50), outline=(150, 255, 150, 255), width=3)
        col = (80, 230, 90, 255) if lvl > 0.3 else (255, 60, 70, 255)
        d.rectangle((76, y + 6, 76 + int((w - 152) * lvl), y + 44), fill=col)
        d.text((70, y + 80), lab, font=f(MONOR, 28), fill=(200, 200, 200, 255), anchor='lm')
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(90, 90, 110, 255), width=3)


def scr_three(layer, d, w, h):
    d.rectangle((0, 0, w, h), fill=(8, 8, 12, 255))
    cw = (w - 80) // 3
    # volume
    x = 20
    d.rectangle((x, 30, x + cw, h - 30), fill=(16, 16, 22, 255), outline=(80, 80, 95, 255), width=2)
    d.text((x + cw // 2, 110), 'VOL', font=f(VT, 70), fill=(80, 255, 120, 255), anchor='mm')
    for k in range(8):
        on = k < 2
        d.rectangle((x + 40 + k * ((cw - 80) // 8), 300 - k * 12, x + 40 + k * ((cw - 80) // 8) + 16, 330), fill=(80, 255, 120, 255) if on else (50, 60, 55, 255))
    d.text((x + cw // 2, h - 90), 'la TV si', font=f(INTERX, 30), fill=(230, 230, 230, 255), anchor='mm')
    d.text((x + cw // 2, h - 55), 'abbassa da sola', font=f(INTERX, 30), fill=(230, 230, 230, 255), anchor='mm')
    # controller
    x = 40 + cw
    d.rectangle((x, 30, x + cw, h - 30), fill=(16, 16, 22, 255), outline=(80, 80, 95, 255), width=2)
    d.rounded_rectangle((x + 50, 140, x + cw - 50, 250), radius=40, outline=(230, 230, 230, 255), width=5)
    d.line((x + 60, 120, x + cw - 60, 270), fill=(255, 60, 70, 255), width=9)
    d.text((x + cw // 2, h - 90), 'controller', font=f(INTERX, 30), fill=(230, 230, 230, 255), anchor='mm')
    d.text((x + cw // 2, h - 55), 'scollegato', font=f(INTERX, 30), fill=(230, 230, 230, 255), anchor='mm')
    # bsod
    x = 60 + 2 * cw
    d.rectangle((x, 30, x + cw, h - 30), fill=(20, 60, 200, 255), outline=(80, 80, 95, 255), width=2)
    d.text((x + cw // 2, 150), ':(', font=f(INTERX, 110), fill=(255, 255, 255, 255), anchor='mm')
    for k in range(4):
        d.line((x + 40, 250 + k * 22, x + cw - 40 - k * 30, 250 + k * 22), fill=(220, 230, 255, 255), width=6)
    d.text((x + cw // 2, h - 90), 'schermata', font=f(INTERX, 30), fill=(255, 255, 255, 255), anchor='mm')
    d.text((x + cw // 2, h - 55), 'di errore', font=f(INTERX, 30), fill=(255, 255, 255, 255), anchor='mm')
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(90, 90, 110, 255), width=3)


def scr_saves(layer, d, w, h):
    d.rectangle((0, 0, w, h), fill=(8, 12, 10, 255))
    d.text((w // 2, 70), 'MEMORY CARD - SLOT A', font=f(VT, 50), fill=(160, 160, 170, 255), anchor='mm')
    for i, s in enumerate(['PARTITA 1   - 14:32 h', 'PARTITA 2   - 09:05 h', 'PARTITA 3   - 21:47 h']):
        y = 150 + i * 120
        d.rectangle((70, y, w - 70, y + 90), outline=(110, 230, 140, 255), width=3)
        d.text((100, y + 45), s, font=f(VT, 58), fill=(240, 240, 240, 255), anchor='lm')
        d.text((w - 100, y + 45), 'OK', font=f(VT, 58), fill=(110, 255, 140, 255), anchor='rm')
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(90, 90, 110, 255), width=3)


def scr_patent(layer, d, w, h):
    d.rectangle((0, 0, w, h), fill=(236, 232, 220, 255))
    d.text((70, 70), 'UNITED STATES PATENT', font=f(MONO, 36), fill=(30, 30, 30, 255), anchor='lm')
    d.text((70, 130), 'N. 6.935.954', font=f(MONO, 60), fill=(30, 30, 30, 255), anchor='lm')
    d.line((70, 180, w - 70, 180), fill=(30, 30, 30, 255), width=3)
    d.text((70, 240), 'Titolare: NINTENDO', font=f(MONOR, 36), fill=(40, 40, 40, 255), anchor='lm')
    d.text((70, 300), 'Oggetto: "Sanity system"', font=f(MONOR, 36), fill=(40, 40, 40, 255), anchor='lm')
    d.text((70, 360), '(sistema della sanità mentale)', font=f(MONOR, 30), fill=(90, 90, 90, 255), anchor='lm')
    # stamp
    d.ellipse((w - 300, h - 260, w - 90, h - 50), outline=(200, 30, 40, 255), width=8)
    d.text((w - 195, h - 155), 'BREVETTATO', font=f(ANTON, 38), fill=(200, 30, 40, 255), anchor='mm')
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(90, 90, 110, 255), width=3)


BOX = (64, 150, W - 64, 830)

# 1 COVER
im = bg(1, (80, 10, 20))
top(im, 1, 'SPECIALE HALLOWEEN')
im = panel(im, scr_dialog('SI'), (64, 150, W - 64, 760), RED, 0.5)
d = ImageDraw.Draw(im)
y = 800
for ln, col in [('QUESTO GIOCO', WH), ('TI CANCELLA TUTTI', WH), ('I SALVATAGGI.', WH), ('APPOSTA.', OR)]:
    for off, c in [(-4, (0, 220, 255)), (4, (255, 30, 60))]:
        d.text((64 + off, y), ln, font=f(ANTON, 104), fill=c, anchor='lt')
    d.text((64, y), ln, font=f(ANTON, 104), fill=col, anchor='lt')
    y += 118
d.text((64, H - 72), '@killandchill_gg', font=f(INTERM, 24), fill=(140, 140, 150), anchor='lm')
swipe(im)
save(im, '1.jpg')

# 2
im = bg(2, (40, 20, 90))
top(im, 2)
im = panel(im, scr_gc, BOX, (130, 90, 255), 0.35)
big_text(im, 900, [('È TUTTO VERO.', OR)], "Il gioco si chiama Eternal Darkness. È uscito su GameCube nel 2002, pubblicato da Nintendo.")
src_line(im, 'Fonte: Nintendo Life')
swipe(im)
save(im, '2.jpg')

# 3
im = bg(3, (10, 60, 20))
top(im, 3)
im = panel(im, scr_bar, BOX, (80, 255, 120), 0.25)
big_text(im, 900, [('HA UNA BARRA DELLA', WH), ('SANITÀ MENTALE.', OR)], "Più mostri vedi, più il tuo personaggio impazzisce. E a un certo punto impazzisce anche il gioco.")
src_line(im, 'Fonte: StrategyWiki')
swipe(im)
save(im, '3.jpg')

# 4
im = bg(4, (20, 30, 90))
top(im, 4)
im = panel(im, scr_three, BOX, (60, 120, 255), 0.3)
big_text(im, 900, [('POI SE LA PRENDE', WH), ('CON TE.', OR)], "Finge di abbassarti il volume della TV, di staccarti il controller, di mandare in crash la console.")
src_line(im, 'Fonte: Dread Central · Superjump')
swipe(im)
save(im, '4.jpg')

# 5
im = bg(5, (90, 10, 18))
top(im, 5)
im = panel(im, scr_dialog('NO', 87), BOX, RED, 0.5)
big_text(im, 900, [('VAI A SALVARE E...', WH), ('PUFF. TUTTO SPARITO.', RED)], "Ti chiede se vuoi cancellare tutti i salvataggi. Qualunque cosa rispondi, li cancella.")
src_line(im, 'Fonte: StrategyWiki · Giant Bomb')
swipe(im)
save(im, '5.jpg')

# 6
im = bg(6, (10, 60, 30))
top(im, 6)
im = panel(im, scr_saves, BOX, (90, 255, 140), 0.3)
big_text(im, 900, [('ERA TUTTO FINTO.', OR)], "Torni nel menu e i salvataggi sono ancora lì. Voleva solo farti venire un infarto.")
src_line(im, 'Fonte: WhatCulture')
swipe(im)
save(im, '6.jpg')

# 7
im = bg(7, (70, 50, 20))
top(im, 7)
im = panel(im, scr_patent, BOX, (255, 200, 120), 0.25)
big_text(im, 900, [('E NINTENDO', WH), ('L\'HA BREVETTATO.', OR)], "Ha registrato negli Stati Uniti il brevetto del suo \"sistema della sanità mentale\". Oggi è scaduto.")
src_line(im, 'Fonte: Nintendo Life (brevetto n. 6.935.954)')
swipe(im)
save(im, '7.jpg')

# 8 CTA
im = bg(8, (70, 10, 40))
top(im, 8)
d = ImageDraw.Draw(im)
d.text((W // 2, 360), 'TU AVRESTI', font=f(ANTON, 120), fill=WH, anchor='mm')
d.text((W // 2, 500), 'SPENTO TUTTO?', font=f(ANTON, 140), fill=OR, anchor='mm')
d.text((W // 2, 680), 'Scrivi SÌ o NO nei commenti', font=f(INTERX, 44), fill=WH, anchor='mm')
d.rounded_rectangle((110, 800, W - 110, 920), radius=60, fill=OR)
d.text((W // 2, 860), 'Mandalo a chi non salva mai', font=f(INTERX, 44), fill=(14, 10, 8), anchor='mm')
d.text((W // 2, 1040), 'Salvalo: la prossima volta che perdi', font=f(INTERM, 34), fill=(200, 200, 208), anchor='mm')
d.text((W // 2, 1090), 'una partita, almeno sai che poteva andare peggio', font=f(INTERM, 34), fill=(200, 200, 208), anchor='mm')
d.text((W // 2, H - 80), 'Segui @killandchill_gg per altri segreti dei videogiochi', font=f(INTERM, 28), fill=(150, 150, 160), anchor='mm')
save(im, '8.jpg')

# story
cov = Image.open(OUT + '1.jpg')
st = Image.new('RGB', (1080, 1920), (6, 6, 9))
st.paste(cov.resize((1000, 1333)), (40, 260))
ds = ImageDraw.Draw(st)
ds.text((540, 150), 'NUOVO POST', font=f(ANTON, 96), fill=OR, anchor='mm')
ds.text((540, 1720), 'Tocca qui sotto per vederlo', font=f(INTERX, 42), fill=WH, anchor='mm')
st.save(OUT + 'storia.jpg', quality=92)

ims = [Image.open(OUT + f'{i}.jpg').resize((540, 720)) for i in range(1, 9)]
c = Image.new('RGB', (540 * 4, 720 * 2))
for k, x in enumerate(ims):
    c.paste(x, ((k % 4) * 540, (k // 4) * 720))
c.save('/home/claude/rotto/sheet2.jpg', quality=85)
print('ok')
