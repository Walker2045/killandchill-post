import os, sys
s2 = open('/home/claude/rotto/make2.py').read()
exec(s2[:s2.index('BOX = (64')])
BOX = (64, 150, W - 64, 830)
which = sys.argv[1]


def frame(d, w, h):
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline=(90, 90, 110, 255), width=3)


def sheet(n, path):
    ims = [Image.open(OUT + f'{i}.jpg').resize((540, 720)) for i in range(1, n + 1)]
    c = Image.new('RGB', (540 * 4, 720 * 2))
    for k, x in enumerate(ims):
        c.paste(x, ((k % 4) * 540, (k // 4) * 720))
    c.save(path, quality=85)


def story():
    cov = Image.open(OUT + '1.jpg')
    st = Image.new('RGB', (1080, 1920), (6, 6, 9))
    st.paste(cov.resize((1000, 1333)), (40, 260))
    ds = ImageDraw.Draw(st)
    ds.text((540, 150), 'NUOVO POST', font=f(ANTON, 96), fill=OR, anchor='mm')
    ds.text((540, 1720), 'Tocca qui sotto per vederlo', font=f(INTERX, 42), fill=WH, anchor='mm')
    st.save(OUT + 'storia.jpg', quality=92)


def cover_title(im, y, lines, size=104, step=118):
    d = ImageDraw.Draw(im)
    for ln, col in lines:
        if col == OR:
            for off, c in [(-4, (0, 220, 255)), (4, (255, 30, 60))]:
                d.text((64 + off, y), ln, font=f(ANTON, size), fill=c, anchor='lt')
        d.text((64, y), ln, font=f(ANTON, size), fill=col, anchor='lt')
        y += step
    return y


# ================= ETERNAL DARKNESS =================
if which == 'ed':
    OUT = '/home/claude/rotto/ed/'
    os.makedirs(OUT, exist_ok=True)
    TOTAL = 8

    def scr_name(layer, d, w, h):
        d.rectangle((0, 0, w, h), fill=(14, 10, 26, 255))
        d.text((w // 2, h // 2 - 80), 'ETERNAL', font=f(ANTON, 170), fill=(255, 255, 255, 255), anchor='mm')
        d.text((w // 2, h // 2 + 90), 'DARKNESS', font=f(ANTON, 170), fill=(255, 60, 70, 255), anchor='mm')
        d.text((w // 2, h - 60), 'NINTENDO GAMECUBE · 2002', font=f(MONO, 40), fill=(180, 160, 255, 255), anchor='mm')
        frame(d, w, h)

    def scr_bar2(layer, d, w, h):
        d.rectangle((0, 0, w, h), fill=(8, 10, 8, 255))
        d.text((70, 80), 'SANITÀ MENTALE', font=f(MONO, 44), fill=(150, 255, 150, 255), anchor='lm')
        for i, (lvl, lab) in enumerate([(0.9, 'tutto normale'), (0.45, 'qualcosa non va'), (0.08, 'il gioco impazzisce')]):
            y = 160 + i * 155
            d.rectangle((70, y, w - 70, y + 64), outline=(150, 255, 150, 255), width=3)
            col = (80, 230, 90, 255) if lvl > 0.3 else (255, 60, 70, 255)
            d.rectangle((77, y + 7, 77 + int((w - 154) * lvl), y + 57), fill=col)
            d.text((70, y + 100), lab, font=f(MONO, 32), fill=(215, 215, 215, 255), anchor='lm')
        frame(d, w, h)

    def scr_three2(layer, d, w, h):
        d.rectangle((0, 0, w, h), fill=(8, 8, 12, 255))
        cw = (w - 80) // 3
        labels = [('la TV si', 'abbassa da sola'), ('controller', 'scollegato'), ('la TV si', 'spegne')]
        for i in range(3):
            x = 20 + i * (cw + 20)
            d.rectangle((x, 30, x + cw, h - 30), fill=(16, 16, 22, 255), outline=(80, 80, 95, 255), width=2)
            d.text((x + cw // 2, h - 120), labels[i][0], font=f(INTERX, 34), fill=(235, 235, 235, 255), anchor='mm')
            d.text((x + cw // 2, h - 78), labels[i][1], font=f(INTERX, 34), fill=(235, 235, 235, 255), anchor='mm')
        # volume
        x = 20
        d.text((x + cw // 2, 110), 'VOL', font=f(VT, 90), fill=(80, 255, 120, 255), anchor='mm')
        for k in range(8):
            bx = x + 30 + k * ((cw - 60) // 8)
            d.rectangle((bx, 360 - k * 22, bx + 20, 400), fill=(80, 255, 120, 255) if k < 2 else (45, 55, 50, 255))
        # gamepad
        x = 20 + cw + 20
        cx, cy = x + cw // 2, 250
        d.rounded_rectangle((cx - 120, cy - 60, cx + 120, cy + 60), radius=50, fill=(200, 200, 210, 255))
        d.rectangle((cx - 85, cy - 12, cx - 45, cy + 12), fill=(40, 40, 50, 255))
        d.rectangle((cx - 77, cy - 20, cx - 53, cy + 20), fill=(40, 40, 50, 255))
        d.ellipse((cx + 45, cy - 22, cx + 85, cy + 18), fill=(80, 200, 120, 255))
        d.line((cx, cy - 60, cx, cy - 150), fill=(200, 200, 210, 255), width=8)
        d.line((cx - 30, cy - 175, cx + 30, cy - 115), fill=(255, 60, 70, 255), width=10)
        d.line((cx + 30, cy - 175, cx - 30, cy - 115), fill=(255, 60, 70, 255), width=10)
        # tv off
        x = 20 + 2 * (cw + 20)
        d.rectangle((x + 4, 34, x + cw - 4, h - 160), fill=(0, 0, 0, 255))
        d.line((x + 40, (h - 126) // 2 + 17, x + cw - 40, (h - 126) // 2 + 17), fill=(255, 255, 255, 255), width=4)
        d.text((x + cw // 2, 110), 'OFF', font=f(VT, 80), fill=(90, 90, 90, 255), anchor='mm')
        for i in range(3):
            xx = 20 + i * (cw + 20)
            d.text((xx + cw // 2, h - 120), labels[i][0], font=f(INTERX, 34), fill=(235, 235, 235, 255), anchor='mm')
            d.text((xx + cw // 2, h - 78), labels[i][1], font=f(INTERX, 34), fill=(235, 235, 235, 255), anchor='mm')
        frame(d, w, h)

    def scr_empty(layer, d, w, h):
        d.rectangle((0, 0, w, h), fill=(10, 6, 8, 255))
        d.text((w // 2, 80), 'MEMORY CARD - SLOT A', font=f(VT, 52), fill=(160, 160, 170, 255), anchor='mm')
        for i in range(3):
            y = 150 + i * 120
            d.rectangle((70, y, w - 70, y + 90), outline=(90, 60, 66, 255), width=3)
            d.text((w // 2, y + 45), '- vuoto -', font=f(VT, 56), fill=(120, 90, 96, 255), anchor='mm')
        d.text((w // 2, h - 70), '0 SALVATAGGI', font=f(VT, 84), fill=(255, 60, 70, 255), anchor='mm')
        frame(d, w, h)

    def scr_saves2(layer, d, w, h):
        d.rectangle((0, 0, w, h), fill=(8, 12, 10, 255))
        d.text((w // 2, 70), 'MEMORY CARD - SLOT A', font=f(VT, 52), fill=(160, 160, 170, 255), anchor='mm')
        for i, s in enumerate(['PARTITA 1    14:32', 'PARTITA 2    09:05', 'PARTITA 3    21:47', 'PARTITA 4    03:12']):
            y = 130 + i * 128
            d.rectangle((70, y, w - 70, y + 100), outline=(110, 230, 140, 255), width=3)
            d.text((100, y + 50), s, font=f(VT, 64), fill=(240, 240, 240, 255), anchor='lm')
            d.text((w - 100, y + 50), 'OK', font=f(VT, 64), fill=(110, 255, 140, 255), anchor='rm')
        frame(d, w, h)

    # 1
    im = bg(1, (80, 10, 20))
    top(im, 1, 'SPECIALE HALLOWEEN')
    im = panel(im, scr_dialog('SI'), (64, 150, W - 64, 740), RED, 0.5)
    y = cover_title(im, 790, [('QUESTO GIOCO', WH), ('TI CANCELLA TUTTI', WH), ('I SALVATAGGI.', WH), ('APPOSTA.', OR)])
    d = ImageDraw.Draw(im)
    d.text((64, y + 14), 'Eternal Darkness · GameCube, 2002', font=f(INTERX, 34), fill=(225, 225, 230), anchor='lt')
    d.text((64, H - 72), '@killandchill_gg', font=f(INTERM, 26), fill=(160, 160, 170), anchor='lm')
    swipe(im)
    save(im, '1.jpg')
    # 2
    im = bg(2, (40, 20, 90)); top(im, 2)
    im = panel(im, scr_name, BOX, (130, 90, 255), 0.35)
    big_text(im, 900, [('ESISTE DAVVERO.', OR)], "Un horror pubblicato da Nintendo. E nasconde un trucco che ti spaventa fuori dallo schermo.")
    src_line(im, 'Fonte: Nintendo Life'); swipe(im); save(im, '2.jpg')
    # 3
    im = bg(3, (10, 60, 20)); top(im, 3)
    im = panel(im, scr_bar2, BOX, (80, 255, 120), 0.25)
    big_text(im, 900, [('HA UNA BARRA DELLA', WH), ('SANITÀ MENTALE.', OR)], "Più mostri incontri, più il tuo personaggio impazzisce. E a un certo punto impazzisce anche il gioco.")
    src_line(im, 'Fonte: StrategyWiki'); swipe(im); save(im, '3.jpg')
    # 4
    im = bg(4, (20, 30, 90)); top(im, 4)
    im = panel(im, scr_three2, BOX, (60, 120, 255), 0.3)
    big_text(im, 900, [('POI SE LA PRENDE', WH), ('CON TE.', OR)], "Finge di abbassarti il volume, di staccarti il controller, di spegnerti la TV.")
    src_line(im, 'Fonte: Dread Central · Eternal Darkness Wiki'); swipe(im); save(im, '4.jpg')
    # 5
    im = bg(5, (90, 10, 18)); top(im, 5)
    im = panel(im, scr_empty, BOX, RED, 0.5)
    big_text(im, 900, [('VAI A SALVARE E...', WH), ('PUFF. TUTTO SPARITO.', RED)], "Ti chiede se vuoi cancellare tutti i salvataggi. Qualunque cosa rispondi, spariscono.")
    src_line(im, 'Fonte: StrategyWiki · Giant Bomb'); swipe(im); save(im, '5.jpg')
    # 6 full-screen single phrase
    im = bg(6, (10, 60, 30)); top(im, 6)
    im = panel(im, scr_saves2, BOX, (90, 255, 140), 0.3)
    big_text(im, 900, [('ERA TUTTO FINTO.', OR)], "Rientri nel menu e i salvataggi sono ancora lì. Voleva solo farti venire un infarto.")
    src_line(im, 'Fonte: WhatCulture'); swipe(im); save(im, '6.jpg')
    # 7
    im = bg(7, (70, 50, 20)); top(im, 7)
    im = panel(im, scr_patent, BOX, (255, 200, 120), 0.25)
    big_text(im, 900, [('E NINTENDO', WH), ("L'HA BREVETTATO.", OR)], "Il \"sistema della sanità mentale\" è stato registrato come brevetto negli Stati Uniti.")
    src_line(im, 'Fonte: Nintendo Life (brevetto n. 6.935.954)'); swipe(im); save(im, '7.jpg')
    # 8
    im = bg(8, (70, 10, 40)); top(im, 8)
    d = ImageDraw.Draw(im)
    d.text((W // 2, 380), 'TU AVRESTI', font=f(ANTON, 120), fill=WH, anchor='mm')
    d.text((W // 2, 520), 'SPENTO LA CONSOLE?', font=f(ANTON, 118), fill=OR, anchor='mm')
    d.text((W // 2, 720), 'Scrivi SÌ o NO nei commenti', font=f(INTERX, 46), fill=WH, anchor='mm')
    d.line((260, 820, W - 260, 820), fill=(80, 70, 90), width=2)
    d.text((W // 2, 910), 'Mandalo a chi non salva mai', font=f(INTERX, 46), fill=OR, anchor='mm')
    d.text((W // 2, 990), 'Salvalo per la prossima partita persa.', font=f(INTERM, 36), fill=(205, 205, 212), anchor='mm')
    d.text((W // 2, H - 80), 'Segui @killandchill_gg per altri segreti dei videogiochi', font=f(INTERM, 30), fill=(170, 170, 180), anchor='mm')
    save(im, '8.jpg')
    story(); sheet(8, '/home/claude/rotto/sheet_ed.jpg')

# ================= FNAF =================
if which == 'fnaf':
    OUT = '/home/claude/rotto/fnaf/'
    os.makedirs(OUT, exist_ok=True)
    TOTAL = 8
    STAR = '★'

    def review_card(d, x0, y0, x1, y1, stars, text, who, big=False):
        d.rounded_rectangle((x0, y0, x1, y1), radius=22, fill=(246, 244, 238, 255))
        fs = 64 if big else 46
        if stars: d.text((x0 + 40, y0 + 40), STAR * stars + '☆' * (5 - stars), font=f('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', fs), fill=(240, 160, 20, 255), anchor='lt')
        ty = y0 + ((140 if big else 110) if stars else 50)
        for ln in text:
            d.text((x0 + 40, ty), ln, font=f(INTERX, 50 if big else 38), fill=(20, 20, 24, 255), anchor='lt')
            ty += 64 if big else 50
        d.text((x0 + 40, y1 - 40), who, font=f(INTERM, 30 if big else 26), fill=(110, 110, 118, 255), anchor='lb')

    def scr_review(layer, d, w, h):
        d.rectangle((0, 0, w, h), fill=(12, 10, 10, 255))
        review_card(d, 50, 50, w - 50, h - 50, 1, ['"Il personaggio sembra', 'un animatronico', 'inquietante."'], 'Giocatori, 2013 (tradotto)', big=True)
        frame(d, w, h)

    def scr_lumber(layer, d, w, h):
        for y in range(h):
            d.line((0, y, w, y), fill=(120 - y // 8, 190 - y // 6, 235 - y // 10, 255))
        d.rectangle((0, h - 140, w, h), fill=(90, 160, 70, 255))
        import random as R
        R.seed(4)
        for i in range(9):
            x = 40 + i * 110 + R.randint(-10, 10)
            d.rectangle((x + 20, h - 210, x + 36, h - 140), fill=(110, 70, 40, 255))
            d.polygon([(x - 20, h - 200), (x + 28, h - 340 - R.randint(0, 40)), (x + 76, h - 200)], fill=(40, 120 + R.randint(0, 40), 60, 255))
        d.rounded_rectangle((w // 2 - 330, 60, w // 2 + 330, 250), radius=18, fill=(150, 95, 50, 255), outline=(90, 55, 25, 255), width=8)
        d.text((w // 2, 125), 'CHIPPER & SONS', font=f(ANTON, 84), fill=(255, 240, 210, 255), anchor='mm')
        d.text((w // 2, 205), 'LUMBER CO.', font=f(ANTON, 54), fill=(255, 220, 160, 255), anchor='mm')
        d.text((w // 2, h - 70), 'gioco per famiglie · 2013', font=f(INTERX, 34), fill=(255, 255, 255, 255), anchor='mm')
        frame(d, w, h)

    def scr_critic(layer, d, w, h):
        d.rectangle((0, 0, w, h), fill=(12, 10, 10, 255))
        review_card(d, 50, 40, w - 50, 330, 0, ['"Involontariamente', 'terrificante."'], 'Jim Sterling, critico di videogiochi')
        review_card(d, 50, 350, w - 50, h - 40, 1, ['"Sembra un animale', 'animatronico spaventoso."'], 'giocatori, 2013 (tradotto)')
        frame(d, w, h)

    def scr_quit(layer, d, w, h):
        d.rectangle((0, 0, w, h), fill=(6, 6, 8, 255))
        d.text((70, 120), 'C:\\> lascio_i_videogiochi.exe', font=f(MONO, 40), fill=(220, 220, 220, 255), anchor='lm')
        d.text((70, 200), 'Sei sicuro? (S/N)', font=f(MONO, 40), fill=(220, 220, 220, 255), anchor='lm')
        d.text((70, 280), '> S', font=f(MONO, 40), fill=(255, 122, 26, 255), anchor='lm')
        d.rectangle((150, 310, 176, 356), fill=(255, 122, 26, 255))
        d.text((w // 2, h - 110), 'ERA PRONTO A MOLLARE', font=f(ANTON, 80), fill=(255, 60, 70, 255), anchor='mm')
        frame(d, w, h)

    def scr_cam(layer, d, w, h):
        import random as R
        R.seed(9)
        d.rectangle((0, 0, w, h), fill=(16, 18, 16, 255))
        for _ in range(2600):
            x, y = R.randint(0, w - 1), R.randint(0, h - 1)
            v = R.randint(30, 90)
            d.point((x, y), fill=(v, v, v, 255))
        # corridor perspective
        d.polygon([(w // 2 - 90, 200), (w // 2 + 90, 200), (w - 60, h - 40), (60, h - 40)], fill=(28, 30, 28, 255))
        d.rectangle((w // 2 - 90, 120, w // 2 + 90, 200), fill=(8, 8, 8, 255))
        d.text((40, 50), 'CAM 1A', font=f(VT, 70), fill=(255, 255, 255, 255), anchor='lm')
        d.ellipse((w - 90, 34, w - 50, 74), fill=(255, 40, 40, 255))
        d.text((w - 110, 54), 'REC', font=f(VT, 54), fill=(255, 255, 255, 255), anchor='rm')
        d.text((40, h - 50), '12:00 AM', font=f(VT, 60), fill=(255, 255, 255, 255), anchor='lm')
        d.text((w - 40, h - 50), 'NOTTE 1', font=f(VT, 60), fill=(255, 255, 255, 255), anchor='rm')
        frame(d, w, h)

    def scr_date(layer, d, w, h):
        d.rectangle((0, 0, w, h), fill=(14, 10, 8, 255))
        d.text((w // 2, h // 2 - 60), '08.08.2014', font=f(ANTON, 190), fill=(255, 255, 255, 255), anchor='mm')
        d.text((w // 2, h // 2 + 110), 'ESCE IL PRIMO FNAF', font=f(MONO, 50), fill=(255, 122, 26, 255), anchor='mm')
        frame(d, w, h)

    # 1
    im = bg(1, (80, 30, 6))
    top(im, 1, 'SPECIALE HALLOWEEN')
    im = panel(im, scr_review, (64, 150, W - 64, 740), OR, 0.35)
    y = cover_title(im, 790, [('QUESTA RECENSIONE', WH), ('CATTIVA HA CREATO', WH), ("FIVE NIGHTS", OR), ("AT FREDDY'S.", OR)])
    d = ImageDraw.Draw(im)
    d.text((64, H - 72), '@killandchill_gg', font=f(INTERM, 26), fill=(160, 160, 170), anchor='lm')
    swipe(im); save(im, '1.jpg')
    # 2
    im = bg(2, (20, 60, 30)); top(im, 2)
    im = panel(im, scr_lumber, BOX, (120, 220, 120), 0.25)
    big_text(im, 900, [('2013. UN GIOCO', WH), ('PER BAMBINI.', OR)], "Si chiama Chipper & Sons Lumber Co.: un castoro che gestisce una segheria. L'ha creato Scott Cawthon.")
    src_line(im, 'Fonte: Wikipedia · Film Stories'); swipe(im); save(im, '2.jpg')
    # 3
    im = bg(3, (80, 20, 10)); top(im, 3)
    im = panel(im, scr_critic, BOX, RED, 0.3)
    big_text(im, 900, [('LE RECENSIONI', WH), ('LO DISTRUGGONO.', RED)], "Il problema? I castori, che dovevano essere carini, mettevano paura a tutti.")
    src_line(im, 'Fonte: Wikipedia (citazione di Jim Sterling)'); swipe(im); save(im, '3.jpg')
    # 4
    im = bg(4, (30, 20, 50)); top(im, 4)
    im = panel(im, scr_quit, BOX, (150, 120, 255), 0.25)
    big_text(im, 900, [('LUI È DISTRUTTO.', WH)], "Cawthon racconta che aveva il cuore spezzato ed era pronto a smettere di fare videogiochi.")
    src_line(im, 'Fonte: intervista a Indie Game Magazine'); swipe(im); save(im, '4.jpg')
    # 5
    im = bg(5, (60, 40, 10)); top(im, 5)
    im = panel(im, scr_cam, BOX, (200, 200, 200), 0.18)
    big_text(im, 900, [('POI GLI VIENE', WH), ("UN'IDEA FOLLE.", OR)], "Se i suoi personaggi sembrano animatronici inquietanti, farà un gioco proprio su animatronici inquietanti.")
    src_line(im, 'Fonte: Slashfilm · Wikipedia'); swipe(im); save(im, '5.jpg')
    # 6
    im = bg(6, (90, 30, 6)); top(im, 6)
    im = panel(im, scr_date, BOX, OR, 0.35)
    big_text(im, 900, [('NASCE FNAF.', OR)], "Esce l'8 agosto 2014. Lo fa una sola persona, e diventa un fenomeno in tutto il mondo.")
    src_line(im, 'Fonte: Wikipedia'); swipe(im); save(im, '6.jpg')
    # 7 full text slide
    im = bg(7, (70, 10, 30)); top(im, 7)
    d = ImageDraw.Draw(im)
    d.text((W // 2, 380), 'OGGI È UNA SAGA', font=f(ANTON, 110), fill=WH, anchor='mm')
    d.text((W // 2, 510), 'CON DUE FILM', font=f(ANTON, 130), fill=OR, anchor='mm')
    d.text((W // 2, 640), 'AL CINEMA.', font=f(ANTON, 130), fill=OR, anchor='mm')
    for i, ln in enumerate(["Tutto grazie a chi aveva scritto", "che i suoi castori facevano paura."]):
        d.text((W // 2, 820 + i * 60), ln, font=f(INTERM, 42), fill=(215, 215, 222), anchor='mm')
    src_line(im, 'Fonte: Popverse · Slashfilm'); swipe(im); save(im, '7.jpg')
    # 8
    im = bg(8, (70, 30, 10)); top(im, 8)
    d = ImageDraw.Draw(im)
    d.text((W // 2, 380), 'TU A CHE NOTTE', font=f(ANTON, 130), fill=WH, anchor='mm')
    d.text((W // 2, 520), 'SEI ARRIVATO?', font=f(ANTON, 130), fill=OR, anchor='mm')
    d.text((W // 2, 720), 'Scrivilo nei commenti', font=f(INTERX, 46), fill=WH, anchor='mm')
    d.line((260, 820, W - 260, 820), fill=(80, 70, 90), width=2)
    d.text((W // 2, 910), 'Mandalo a chi ti critica sempre', font=f(INTERX, 46), fill=OR, anchor='mm')
    d.text((W // 2, H - 80), 'Segui @killandchill_gg per altri segreti dei videogiochi', font=f(INTERM, 30), fill=(170, 170, 180), anchor='mm')
    save(im, '8.jpg')
    story(); sheet(8, '/home/claude/rotto/sheet_fnaf.jpg')
print('ok')
