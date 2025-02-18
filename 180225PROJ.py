import pygame, random, sys, os, datetime

pygame.init()

W = 10
H = 20
BLK = 30
TW = W * BLK
TH = H * BLK
SB = 220
EX = 100
SW = TW + SB
SH = TH + EX
FPS = 60

BG = (10, 10, 10)
GR = (40, 40, 40)
TC = (255, 255, 255)

COL = {
    'I': (0, 240, 240),
    'J': (0, 0, 240),
    'L': (240, 160, 0),
    'O': (240, 240, 0),
    'S': (0, 240, 0),
    'T': (160, 0, 240),
    'Z': (240, 0, 0)
}

G2 = {
    'I': [
        [[0, -1], [0, 0], [0, 1], [0, 2]],
        [[-1, 0], [0, 0], [1, 0], [2, 0]]
    ],
    'J': [
        [[-1, -1], [-1, 0], [0, 0], [1, 0]],
        [[0, -1], [1, -1], [0, 0], [0, 1]],
        [[-1, 0], [0, 0], [1, 0], [1, 1]],
        [[0, -1], [0, 0], [-1, 1], [0, 1]]
    ],
    'L': [
        [[1, -1], [-1, 0], [0, 0], [1, 0]],
        [[0, -1], [0, 0], [0, 1], [1, 1]],
        [[-1, 0], [0, 0], [1, 0], [-1, 1]],
        [[-1, -1], [0, -1], [0, 0], [0, 1]]
    ],
    'O': [
        [[0, 0], [1, 0], [0, 1], [1, 1]]
    ],
    'S': [
        [[0, -1], [1, -1], [-1, 0], [0, 0]],
        [[0, -1], [0, 0], [1, 0], [1, 1]]
    ],
    'T': [
        [[0, -1], [-1, 0], [0, 0], [1, 0]],
        [[0, -1], [0, 0], [1, 0], [0, 1]],
        [[-1, 0], [0, 0], [1, 0], [0, 1]],
        [[0, -1], [-1, 0], [0, 0], [0, 1]]
    ],
    'Z': [
        [[-1, -1], [0, -1], [0, 0], [1, 0]],
        [[1, -1], [0, 0], [1, 0], [0, 1]]
    ]
}


class TT:
    def __init__(self, m, d, r):
        self.m = m
        self.d = d
        self.r = r
        self.gd = [[None for _ in range(W)] for _ in range(H)]
        self.sc = 0
        self.lv = 1
        self.cp = None
        self.np = self.np_()
        self.qp = self.np_()
        self.ov = False
        self.t0 = pygame.time.get_ticks()
        self.sp_()

    def np_(self):
        p = random.choice(list(G2.keys()))
        rr = random.randint(0, len(G2[p]) - 1) if self.m == 'r' else 0
        return [p, rr, W // 2, 0]

    def sp_(self):
        self.cp = self.np
        self.np = self.qp
        self.qp = self.np_()
        if not self.vl(self.cp[0], self.cp[1], self.cp[2], self.cp[3]):
            self.ov = True

    def vl(self, p, rr, x, y):
        for a in G2[p][rr]:
            i = x + a[0]
            j = y + a[1]
            if i < 0 or i >= W or j >= H:
                return False
            if j >= 0 and self.gd[j][i]:
                return False
        return True

    def fr(self):
        p, rr, x, y = self.cp
        for a in G2[p][rr]:
            i = x + a[0]
            j = y + a[1]
            if j >= 0:
                self.gd[j][i] = p
        self.cl()
        self.cp = None

    def cl(self):
        cnt = 0
        j = H - 1
        while j >= 0:
            if None not in self.gd[j]:
                del self.gd[j]
                self.gd.insert(0, [None for _ in range(W)])
                cnt += 1
            else:
                j -= 1
        if cnt > 0:
            self.sc += (cnt ** 2) * 100
            self.lv = self.sc // 1000 + 1

    def mv(self, h, v):
        try:
            p, rr, x, y = self.cp
        except:
            print("Вы проиграли")
            try:
                with open("scores.txt", "a") as f:
                    f.write(str('Проигрыш') + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
            except:
                pass
        if self.vl(p, rr, x + h, y + v):
            self.cp[2] += h
            self.cp[3] += v
            return True
        return False

    def rt(self):
        p, rr, x, y = self.cp
        nrr = (rr + 1) % len(G2[p])
        if self.vl(p, nrr, x, y):
            self.cp[1] = nrr

    def dr(self):
        while self.mv(0, 1):
            self.sc += 1

    def up(self):
        if self.cp is None:
            self.sp_()
        else:
            if not self.mv(0, 1):
                self.fr()

    def dw(self, s, f):
        for j in range(H):
            for i in range(W):
                rct = pygame.Rect(i * BLK, j * BLK, BLK, BLK)
                pygame.draw.rect(s, GR, rct, 1)
                if self.gd[j][i]:
                    pygame.draw.rect(s, COL[self.gd[j][i]], rct.inflate(-2, -2))
        if self.cp:
            p, rr, x, y = self.cp
            for a in G2[p][rr]:
                i = x + a[0]
                j = y + a[1]
                if j >= 0:
                    rct = pygame.Rect(i * BLK, j * BLK, BLK, BLK)
                    pygame.draw.rect(s, COL[p], rct.inflate(-2, -2))
        iy = 20
        tx = f.render("Счёт: " + str(self.sc), True, TC)
        s.blit(tx, (TW + 20, iy))
        iy += 40
        tx = f.render("Уровень: " + str(self.lv), True, TC)
        s.blit(tx, (TW + 20, iy))
        iy += 40
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tx = f.render(now, True, TC)
        s.blit(tx, (TW + 20, iy))
        iy += 40
        tel = (pygame.time.get_ticks() - self.t0) // 1000
        tx = f.render("Время: " + str(tel) + "с", True, TC)
        s.blit(tx, (TW + 20, iy))


class Btn:
    def __init__(self, x, y, w, h, txt, act, ft, bc=(70, 70, 70), hc=(100, 100, 100), tc=(255, 255, 255)):
        self.r = pygame.Rect(x, y, w, h)
        self.txt = txt
        self.act = act
        self.ft = ft
        self.bc = bc
        self.hc = hc
        self.tc = tc

    def dw(self, s, m):
        c = self.hc if self.r.collidepoint(m) else self.bc
        pygame.draw.rect(s, c, self.r)
        tx = self.ft.render(self.txt, True, self.tc)
        s.blit(tx, (self.r.x + (self.r.w - tx.get_width()) // 2, self.r.y + (self.r.h - tx.get_height()) // 2))

    def cl(self, m):
        return self.r.collidepoint(m)


def mm(sc, ft):
    bs = [
        Btn((SW - 200) // 2, 100, 200, 50, "Игра", "game", ft),
        Btn((SW - 200) // 2, 170, 200, 50, "Рейтинги", "rank", ft),
        Btn((SW - 200) // 2, 240, 200, 50, "Настройки", "set", ft),
        Btn((SW - 200) // 2, 310, 200, 50, "Будильник", "alarm", ft),
        Btn((SW - 200) // 2, 380, 200, 50, "Секундомер", "stopwatch", ft),
        Btn((SW - 200) // 2, 450, 200, 50, "Выход", "exit", ft)
    ]
    while True:
        m = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for b in bs:
                    if b.cl(m):
                        return b.act
        sc.fill(BG)
        tx = ft.render("Главное меню", True, TC)
        sc.blit(tx, ((SW - tx.get_width()) // 2, 30))
        for b in bs:
            b.dw(sc, m)
        sig = ft.render("Разработал: Равилов Роман Ринатович 9Б", True, TC)
        sc.blit(sig, ((SW - sig.get_width()) // 2, SH - sig.get_height() - 10))
        pygame.display.update()


def md(sc, ft):
    bs = [
        Btn((SW - 250) // 2, 150, 250, 50, "Классический тетрис", "c", ft),
        Btn((SW - 250) // 2, 220, 250, 50, "Случайный тетрис", "r", ft),
        Btn((SW - 250) // 2, 290, 250, 50, "Назад", "back", ft)
    ]
    while True:
        m = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for b in bs:
                    if b.cl(m):
                        return b.act
        sc.fill(BG)
        tx = ft.render("Выберите режим игры", True, TC)
        sc.blit(tx, ((SW - tx.get_width()) // 2, 80))
        for b in bs:
            b.dw(sc, m)
        pygame.display.update()


def tg(sc, ft, stt):
    m = md(sc, ft)
    if m == "back":
        return
    game = TT(m, stt["d"], stt["r"])
    btn_left = Btn(10, TH + 10, 80, 40, "Влево", "left", ft)
    btn_right = Btn(100, TH + 10, 80, 40, "Вправо", "right", ft)
    btn_rot = Btn(190, TH + 10, 80, 40, "Поворот", "rot", ft)
    btn_drop = Btn(280, TH + 10, 80, 40, "Ускорить", "drop", ft)
    btn_back = Btn(TW + 20, TH - 50, 180, 40, "Назад", "back", ft)
    clk = pygame.time.Clock()
    while True:
        dt = clk.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mp = pygame.mouse.get_pos()
                if btn_back.cl(mp):
                    return
                if btn_left.cl(mp):
                    game.mv(-1, 0)
                if btn_right.cl(mp):
                    game.mv(1, 0)
                if btn_rot.cl(mp):
                    game.rt()
                if btn_drop.cl(mp):
                    game.dr()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT:
                    game.mv(-1, 0)
                if ev.key == pygame.K_RIGHT:
                    game.mv(1, 0)
                if ev.key == pygame.K_UP:
                    game.rt()
                if ev.key == pygame.K_DOWN:
                    game.mv(0, 1)
                if ev.key == pygame.K_SPACE:
                    game.dr()
                if ev.key == pygame.K_ESCAPE:
                    return
        if pygame.time.get_ticks() - game.t0 > stt["d"]:
            game.up()
            game.t0 = pygame.time.get_ticks()
        sc.fill(BG)
        game.dw(sc, ft)
        for b in [btn_left, btn_right, btn_rot, btn_drop, btn_back]:
            b.dw(sc, pygame.mouse.get_pos())
        pygame.display.update()
        if game.ov:
            try:
                with open("scores.txt", "a") as f:
                    f.write(str(game.sc) + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
            except:
                pass
            go(sc, ft, game.sc)
            return


def go(sc, ft, s):
    btn = Btn((SW - 200) // 2, 300, 200, 50, "Главное меню", "back", ft)
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn.cl(pygame.mouse.get_pos()):
                    return
        sc.fill(BG)
        tx = ft.render("Игра окончена", True, TC)
        sc.blit(tx, ((SW - tx.get_width()) // 2, 200))
        tx2 = ft.render("Счёт: " + str(s), True, TC)
        sc.blit(tx2, ((SW - tx2.get_width()) // 2, 250))
        btn.dw(sc, pygame.mouse.get_pos())
        pygame.display.update()


def rk(sc, ft):
    btn = Btn(10, SH - 60, 100, 40, "Назад", "back", ft)
    lst = []
    if os.path.exists("scores.txt"):
        with open("scores.txt", "r") as f:
            for l in f:
                try:
                    sp = l.split()
                    lst.append((int(sp[0]), " ".join(sp[1:])))
                except:
                    pass
    lst.sort(key=lambda x: x[0], reverse=True)
    while True:
        m = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn.cl(m):
                    return
        sc.fill(BG)
        tx = ft.render("Рейтинги", True, TC)
        sc.blit(tx, ((SW - tx.get_width()) // 2, 20))
        y = 80
        for score, dt in lst[:10]:
            line = ft.render(str(score) + "  " + dt, True, TC)
            sc.blit(line, (50, y))
            y += 30
        btn.dw(sc, m)
        pygame.display.update()


def st(sc, ft, stt):
    btn_inc = Btn((SW - 250) // 2, 150, 250, 50, "Увеличить сложность", "inc", ft)
    btn_dec = Btn((SW - 250) // 2, 220, 250, 50, "Уменьшить сложность", "dec", ft)
    btn_reg = Btn((SW - 250) // 2, 290, 250, 50, "Сменить регион", "reg", ft)
    btn_back = Btn((SW - 250) // 2, 360, 250, 50, "Назад", "back", ft)
    regs = ["US", "EU", "RU"]
    i = regs.index(stt["r"]) if stt["r"] in regs else 0
    while True:
        m = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn_inc.cl(m):
                    stt["d"] = max(100, stt["d"] - 50)
                if btn_dec.cl(m):
                    stt["d"] += 50
                if btn_reg.cl(m):
                    i = (i + 1) % len(regs)
                    stt["r"] = regs[i]
                if btn_back.cl(m):
                    with open("settings.txt", "w") as f:
                        for k, v in stt.items():
                            f.write(k + "=" + str(v) + "\n")
                    return
        sc.fill(BG)
        tx = ft.render("Настройки", True, TC)
        sc.blit(tx, ((SW - tx.get_width()) // 2, 50))
        tx1 = ft.render("Сложность: " + str(stt["d"]), True, TC)
        sc.blit(tx1, ((SW - tx1.get_width()) // 2, 100))
        tx2 = ft.render("Регион: " + stt["r"], True, TC)
        sc.blit(tx2, ((SW - tx2.get_width()) // 2, 130))
        for b in [btn_inc, btn_dec, btn_reg, btn_back]:
            b.dw(sc, m)
        pygame.display.update()


def al(sc, ft):
    alarm_hour = 7
    alarm_minute = 0
    alarm_set = False
    alarm_triggered = False
    btn_inc_h = Btn((SW - 300) // 2, 120, 140, 50, "Увеличить час", "inc_h", ft)
    btn_dec_h = Btn((SW - 300) // 2 + 160, 120, 140, 50, "Уменьшить час", "dec_h", ft)
    btn_inc_m = Btn((SW - 300) // 2, 190, 140, 50, "Увеличить минуту", "inc_m", ft)
    btn_dec_m = Btn((SW - 300) // 2 + 160, 190, 140, 50, "Уменьшить минуту", "dec_m", ft)
    btn_set = Btn((SW - 300) // 2, 260, 300, 50, "Установить будильник", "set", ft)
    btn_back = Btn((SW - 300) // 2, 330, 300, 50, "Назад", "back", ft)
    btn_off = Btn((SW - 300) // 2, 400, 300, 50, "Отключить будильник", "off", ft)
    music_file = "spbu.mp3"
    if os.path.exists(music_file):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(music_file)
    clk = pygame.time.Clock()
    while True:
        m = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn_inc_h.cl(m):
                    alarm_hour = (alarm_hour + 1) % 24
                if btn_dec_h.cl(m):
                    alarm_hour = (alarm_hour - 1) % 24
                if btn_inc_m.cl(m):
                    alarm_minute = (alarm_minute + 1) % 60
                if btn_dec_m.cl(m):
                    alarm_minute = (alarm_minute - 1) % 60
                if btn_set.cl(m):
                    alarm_set = True
                    alarm_triggered = False
                if btn_back.cl(m):
                    pygame.mixer.music.stop()
                    return
                if btn_off.cl(m) and alarm_triggered:
                    pygame.mixer.music.stop()
                    alarm_set = False
                    alarm_triggered = False
        sc.fill(BG)
        tx = ft.render("Будильник", True, TC)
        sc.blit(tx, ((SW - tx.get_width()) // 2, 20))
        time_str = "Установленное время: {:02d}:{:02d}".format(alarm_hour, alarm_minute)
        tx = ft.render(time_str, True, TC)
        sc.blit(tx, ((SW - tx.get_width()) // 2, 70))
        status = "Будильник не установлен" if not alarm_set else "Будильник установлен"
        tx = ft.render(status, True, TC)
        sc.blit(tx, ((SW - tx.get_width()) // 2, 100))
        for b in [btn_inc_h, btn_dec_h, btn_inc_m, btn_dec_m, btn_set, btn_back]:
            b.dw(sc, m)
        if alarm_set and not alarm_triggered:
            now = datetime.datetime.now()
            if now.hour == alarm_hour and now.minute == alarm_minute:
                alarm_triggered = True
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
        if alarm_triggered:
            tx = ft.render("Будильник! Нажмите 'Отключить будильник'", True, (255, 0, 0))
            sc.blit(tx, ((SW - tx.get_width()) // 2, 370))
            btn_off.dw(sc, m)
        pygame.display.update()
        clk.tick(FPS)


def sw(sc, ft):
    btn_start = Btn((SW - 300) // 2, 150, 140, 50, "Старт", "start", ft)
    btn_stop = Btn((SW - 300) // 2 + 160, 150, 140, 50, "Стоп", "stop", ft)
    btn_reset = Btn((SW - 300) // 2, 220, 300, 50, "Сброс", "reset", ft)
    btn_lap = Btn((SW - 300) // 2, 290, 300, 50, "Круг", "lap", ft)
    btn_back = Btn((SW - 300) // 2, 360, 300, 50, "Назад", "back", ft)
    running = False
    start_time = 0
    elapsed = 0
    laps = []
    clk = pygame.time.Clock()
    while True:
        dt = clk.tick(FPS)
        m = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn_start.cl(m) and not running:
                    running = True
                    start_time = pygame.time.get_ticks() - elapsed
                if btn_stop.cl(m) and running:
                    running = False
                    elapsed = pygame.time.get_ticks() - start_time
                if btn_reset.cl(m):
                    running = False
                    elapsed = 0
                    laps = []
                    start_time = pygame.time.get_ticks()
                if btn_lap.cl(m) and running:
                    laps.append(pygame.time.get_ticks() - start_time)
                if btn_back.cl(m):
                    return
        if running:
            elapsed = pygame.time.get_ticks() - start_time
        ms = elapsed % 1000
        sec = (elapsed // 1000) % 60
        mn = (elapsed // 60000)
        time_str = "{:02d}:{:02d}.{:03d}".format(mn, sec, ms)
        sc.fill(BG)
        tx = ft.render("Секундомер", True, TC)
        sc.blit(tx, ((SW - tx.get_width()) // 2, 20))
        tx2 = ft.render(time_str, True, TC)
        sc.blit(tx2, ((SW - tx2.get_width()) // 2, 80))
        lap_y = 420
        for i, lap in enumerate(laps):
            lap_ms = lap % 1000
            lap_sec = (lap // 1000) % 60
            lap_mn = (lap // 60000)
            lap_str = "Круг {}: {:02d}:{:02d}.{:03d}".format(i + 1, lap_mn, lap_sec, lap_ms)
            tx3 = ft.render(lap_str, True, TC)
            sc.blit(tx3, (50, lap_y))
            pygame.draw.circle(sc, (0, 255, 0), (30, lap_y + 10), 5)
            lap_y += 30
        for b in [btn_start, btn_stop, btn_reset, btn_lap, btn_back]:
            b.dw(sc, m)
        pygame.display.update()


def ma():
    sc = pygame.display.set_mode((SW, SH))
    pygame.display.set_caption("Тетрис - Равилов Роман Ринатович 9Б")
    ft = pygame.font.SysFont("Arial", 24)
    stt = {"d": 500, "r": "US"}
    if os.path.exists("settings.txt"):
        try:
            with open("settings.txt", "r") as f:
                for l in f:
                    sp = l.split("=")
                    if len(sp) == 2:
                        k = sp[0].strip()
                        v = sp[1].strip()
                        if k == "d":
                            stt["d"] = int(v)
                        elif k == "r":
                            stt["r"] = v
        except:
            pass
    while True:
        c = mm(sc, ft)
        if c == "game":
            tg(sc, ft, stt)
        elif c == "rank":
            rk(sc, ft)
        elif c == "set":
            st(sc, ft, stt)
        elif c == "alarm":
            al(sc, ft)
        elif c == "stopwatch":
            sw(sc, ft)
        elif c == "exit":
            pygame.quit();
            sys.exit()


ma()
