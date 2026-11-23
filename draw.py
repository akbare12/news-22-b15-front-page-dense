#!/usr/bin/env python3
"""news-image-20261122 — dense front page, 36 stories, 7 regions.
Drawn with PIL only. Output: entry.png 1024x1024."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 232)
PAPER = (250, 246, 236)
INK = (26, 26, 26)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
NAVY = (24, 48, 84)
GREY = (110, 110, 105)
LINE = (200, 192, 175)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SERIF_I = lambda s: F("DejaVuSerif.ttf", s)  # no italic file on this box
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_O = lambda s: F("DejaVuSans.ttf", s)  # no oblique file on this box

def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_wrapped(d, x, y, text, font, maxw, fill=INK, leading=None, max_lines=None):
    lines = wrap(d, text, font, maxw)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(font.size * 1.25)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def chip(d, x, y, label, fill):
    f = SANS_B(9)
    tw = d.textlength(label, font=f)
    w = int(tw) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w

CHIP_FILL = {
    "CONFIRMED": (34, 120, 60),
    "REPORTED": (40, 90, 160),
    "CLAIM": (190, 130, 20),
    "OFFICIAL": (90, 90, 100),
    "ONGOING": (180, 90, 20),
    "PENDING": (120, 90, 140),
    "FORECAST": (90, 140, 150),
}

def vgrad(d, x, y, w, h, top, bot):
    for i in range(h):
        t = i / max(1, h - 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)

# ---------------- hero scenes ----------------

def scene_cop31(d, x, y, w, h):
    vgrad(d, x, y, w, h, (255, 190, 110), (200, 110, 60))
    d.ellipse([x + w - 52, y + 8, x + w - 8, y + 52], fill=(255, 230, 150))
    # conference hall
    d.rectangle([x, y + h - 46, x + w, y + h], fill=(70, 45, 30))
    d.rectangle([x + 14, y + h - 62, x + w - 14, y + h - 46], fill=(120, 80, 50))
    # flags along the table
    cols = [(200, 40, 40), (40, 90, 160), (40, 140, 70), (220, 180, 40),
            (150, 60, 140), (40, 160, 160), (230, 120, 30), (90, 90, 180)]
    fw = (w - 40) // len(cols)
    for i, c in enumerate(cols):
        fx = x + 20 + i * fw
        d.line([(fx + 6, y + h - 62), (fx + 6, y + h - 92)], fill=(60, 40, 25), width=2)
        d.rectangle([fx + 6, y + h - 92, fx + 6 + fw - 8, y + h - 78], fill=c)
    # cracked globe
    gx, gy, gr = x + 26, y + 14, 26
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(90, 150, 200),
              outline=(30, 70, 110), width=2)
    d.arc([gx - gr + 4, gy - gr + 4, gx + gr - 4, gy + gr - 4], 200, 340, fill=(50, 110, 60), width=3)
    d.arc([gx - gr + 4, gy - gr + 4, gx + gr - 4, gy + gr - 4], 20, 110, fill=(50, 110, 60), width=3)
    d.line([(gx - 8, gy - gr + 4), (gx + 2, gy - 6), (gx - 4, gy + 8), (gx + 8, gy + gr - 4)],
           fill=(20, 20, 20), width=2)

def scene_drones(d, x, y, w, h):
    vgrad(d, x, y, w, h, (16, 24, 48), (50, 40, 70))
    for sx, sy in [(x + 20, y + 14), (x + 90, y + 30), (x + 180, y + 10),
                   (x + 250, y + 26), (x + 300, y + 12)]:
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 220))
    # explosion glow
    ex, ey = x + w - 70, y + 55
    for r, a in [(46, 60), (34, 90), (22, 140)]:
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 140, 40))
    d.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=(255, 220, 120))
    # skyline
    base = y + h
    blds = [(0, 70, 46), (52, 40, 80), (98, 58, 60), (160, 44, 92),
            (208, 66, 70), (278, 50, 58)]
    for bx, bw, bh in blds:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(14, 16, 30))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(x + bx + 6, x + bx + bw - 6, 12):
                if (wx * 7 + wy * 13) % 5 < 2:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 110))
    # drones with trails
    for dx, dy, ln in [(x + 40, y + 40, 26), (x + 130, y + 26, 34),
                       (x + 210, y + 48, 22), (x + 280, y + 30, 30)]:
        d.line([(dx - ln, dy + 8), (dx, dy)], fill=(255, 90, 60), width=2)
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(255, 220, 120))
    # smoke
    d.ellipse([ex - 30, ey - 34, ex + 6, ey - 6], fill=(70, 66, 80))
    d.ellipse([ex - 12, ey - 48, ex + 18, ey - 20], fill=(90, 86, 100))

def scene_radar(d, x, y, w, h):
    vgrad(d, x, y, w, h, (12, 20, 40), (40, 34, 60))
    d.ellipse([x + w - 46, y + 10, x + w - 10, y + 46], fill=(235, 230, 210))
    # radar dome
    dx, dy = x + 70, y + h - 30
    d.pieslice([dx - 52, dy - 52, dx + 52, dy + 52], 180, 360, fill=(180, 185, 195),
               outline=(120, 125, 135), width=2)
    d.rectangle([dx - 58, dy - 4, dx + 58, dy + 30], fill=(60, 62, 72))
    # antenna mast + beam
    mx = x + w - 90
    d.line([(mx, y + h - 30), (mx, y + 26)], fill=(140, 145, 155), width=4)
    d.line([(mx - 16, y + 30), (mx + 16, y + 30)], fill=(140, 145, 155), width=3)
    d.ellipse([mx - 6, y + 22, mx + 6, y + 34], fill=(255, 220, 120))
    d.line([(mx, y + 28), (mx + 44, y + 52)], fill=(255, 200, 90), width=2)
    # fire glow at base
    fx = x + w - 40
    for r in [30, 20, 11]:
        d.ellipse([fx - r, y + h - 30 - r // 2, fx + r, y + h - 6], fill=(255, 130, 30))
    d.ellipse([fx - 8, y + h - 22, fx + 8, y + h - 6], fill=(255, 220, 120))
    # smoke plumes
    d.ellipse([fx - 34, y + 52, fx - 4, y + 78], fill=(80, 76, 90))
    d.ellipse([fx - 22, y + 36, fx + 8, y + 60], fill=(100, 96, 110))
    # fence lights
    for lx in range(x + 8, x + w - 8, 26):
        d.ellipse([lx, y + h - 12, lx + 4, y + h - 8], fill=(255, 200, 90))

# ---------------- small-card illustration strips ----------------

def strip_base(d, x, y, w, h, top, bot):
    vgrad(d, x, y, w, h, top, bot)

def motif(d, x, y, w, h, kind, accent):
    cx, cy = x + w // 2, y + h // 2
    if kind == "ballot":
        d.rectangle([cx - 34, cy - 12, cx + 34, cy + 12], fill=(255, 255, 255),
                    outline=(40, 60, 110), width=2)
        d.line([(cx - 22, cy + 1), (cx - 8, cy + 8), (cx + 24, cy - 8)],
               fill=(40, 140, 60), width=4)
        d.ellipse([cx + 40, cy - 14, cx + 52, cy - 2], fill=accent)
    elif kind == "trophy":
        d.polygon([(cx - 14, cy - 14), (cx + 14, cy - 14), (cx + 9, cy + 6),
                   (cx - 9, cy + 6)], fill=(255, 200, 60))
        d.rectangle([cx - 4, cy + 6, cx + 4, cy + 14], fill=(200, 160, 40))
        d.rectangle([cx - 14, cy + 14, cx + 14, cy + 18], fill=(200, 160, 40))
        d.arc([cx - 22, cy - 14, cx - 8, cy + 2], 90, 270, fill=(255, 200, 60), width=4)
        d.arc([cx + 8, cy - 14, cx + 22, cy + 2], 270, 90, fill=(255, 200, 60), width=4)
    elif kind == "ball":
        d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 255, 255),
                  outline=(30, 30, 30), width=2)
        d.polygon([(cx, cy - 8), (cx + 8, cy - 2), (cx + 5, cy + 8),
                   (cx - 5, cy + 8), (cx - 8, cy - 2)], fill=(30, 30, 30))
        for a in range(5):
            ang = math.radians(a * 72 - 90)
            ex, ey = cx + int(16 * math.cos(ang)), cy + int(16 * math.sin(ang))
            d.line([(cx, cy), (ex, ey)], fill=(30, 30, 30), width=1)
    elif kind == "bat":
        d.line([(cx - 26, cy + 14), (cx + 10, cy - 12)], fill=(160, 110, 60), width=6)
        d.ellipse([cx + 12, cy - 18, cx + 26, cy - 4], fill=(200, 60, 50))
        d.ellipse([cx + 14, cy - 16, cx + 24, cy - 6], fill=(255, 255, 255))
    elif kind == "flame":
        d.polygon([(cx, cy - 18), (cx + 12, cy - 2), (cx + 8, cy + 12),
                   (cx - 8, cy + 12), (cx - 12, cy - 2)], fill=(255, 120, 20))
        d.polygon([(cx, cy - 6), (cx + 6, cy + 4), (cx - 6, cy + 10)],
                  fill=(255, 220, 80))
    elif kind == "bolt":
        d.polygon([(cx + 4, cy - 18), (cx - 10, cy + 2), (cx - 1, cy + 2),
                   (cx - 4, cy + 18), (cx + 10, cy - 2), (cx + 1, cy - 2)],
                  fill=(255, 220, 60))
    elif kind == "virus":
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(120, 60, 140))
        for a in range(8):
            ang = math.radians(a * 45)
            ex, ey = cx + int(19 * math.cos(ang)), cy + int(19 * math.sin(ang))
            d.line([(cx, cy), (ex, ey)], fill=(120, 60, 140), width=3)
            d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(120, 60, 140))
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(200, 150, 220))
    elif kind == "chip":
        d.rectangle([cx - 16, cy - 12, cx + 16, cy + 12], fill=(40, 60, 90),
                    outline=(180, 200, 220), width=2)
        d.rectangle([cx - 7, cy - 5, cx + 7, cy + 5], fill=(120, 200, 120))
        for px in (-16, 16):
            for py in (-8, 0, 8):
                d.line([(cx + px, cy + py), (cx + px + (6 if px > 0 else -6), cy + py)],
                       fill=(180, 200, 220), width=2)
    elif kind == "rocket":
        d.polygon([(cx, cy - 20), (cx + 9, cy - 2), (cx + 9, cy + 10),
                   (cx - 9, cy + 10), (cx - 9, cy - 2)], fill=(230, 235, 240))
        d.ellipse([cx - 4, cy - 12, cx + 4, cy - 4], fill=(60, 140, 220))
        d.polygon([(cx - 9, cy + 6), (cx - 17, cy + 16), (cx - 9, cy + 12)], fill=(200, 60, 50))
        d.polygon([(cx + 9, cy + 6), (cx + 17, cy + 16), (cx + 9, cy + 12)], fill=(200, 60, 50))
        d.polygon([(cx - 4, cy + 12), (cx + 4, cy + 12), (cx, cy + 20)], fill=(255, 160, 40))

STRIPS = {
    "ballot": ((70, 100, 160), (30, 50, 110)),
    "trophy": ((40, 90, 60), (20, 50, 35)),
    "ball": ((60, 120, 90), (30, 70, 50)),
    "bat": ((120, 90, 50), (70, 50, 25)),
    "flame": ((180, 70, 40), (110, 35, 20)),
    "bolt": ((140, 110, 40), (90, 70, 20)),
    "virus": ((110, 70, 130), (70, 40, 90)),
    "chip": ((60, 90, 130), (35, 55, 90)),
    "rocket": ((40, 70, 110), (20, 40, 70)),
}

# ---------------- world map ----------------

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 71), (-95, 80), (-75, 73), (-60, 62),
     (-55, 47), (-70, 42), (-80, 32), (-97, 26), (-105, 20), (-115, 30),
     (-125, 40), (-125, 49), (-150, 60)],
    # Greenland
    [(-58, 64), (-45, 60), (-30, 68), (-22, 70), (-40, 76), (-58, 74)],
    # South America
    [(-80, 10), (-70, 12), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-48, -28), (-58, -35), (-70, -40), (-75, -50), (-70, -55),
     (-75, -40), (-80, -20), (-80, -5)],
    # Africa
    [(-18, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 10), (48, 0), (40, -10), (35, -20), (32, -28),
     (20, -35), (15, -30), (12, -18), (9, -1), (9, 4), (-8, 4)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (30, 60), (30, 70), (25, 71), (18, 69),
     (12, 65), (5, 60), (5, 58), (-2, 50), (-5, 48), (-10, 43)],
    # Asia
    [(30, 70), (40, 68), (55, 68), (70, 72), (90, 75), (110, 76), (130, 72),
     (160, 70), (180, 66), (170, 60), (160, 55), (155, 50), (140, 45),
     (135, 40), (130, 33), (127, 35), (122, 30), (115, 22), (108, 18),
     (105, 8), (100, 8), (95, 15), (90, 22), (85, 20), (80, 10), (75, 8),
     (70, 22), (60, 25), (55, 26), (50, 29), (45, 29), (40, 30), (35, 36),
     (30, 36), (30, 42), (30, 46)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (124, -33), (129, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -32), (153, -27), (146, -19),
     (142, -11), (137, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
    # UK
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-2, 51)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 37), (141, 39),
     (142, 42), (144, 44), (141, 45), (139, 41), (137, 37), (135, 34)],
    # Indonesia
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -8), (130, -4), (135, -3), (140, -8), (135, -8), (120, -5),
     (110, -2), (100, 2)],
    # New Zealand
    [(167, -45), (170, -42), (173, -40), (175, -38), (178, -37),
     (174, -41), (170, -44)],
]

def project(lon, lat, mx, my, mw, mh):
    x = mx + (lon + 180) / 360.0 * mw
    y = my + (85 - lat) / 145.0 * mh
    return (x, y)

def draw_map(d, mx, my, mw, mh, pins):
    d.rectangle([mx, my, mx + mw, my + mh], fill=(222, 234, 242),
                outline=(150, 165, 180), width=1)
    # graticule
    for lon in range(-150, 181, 30):
        x = mx + (lon + 180) / 360.0 * mw
        d.line([(x, my), (x, my + mh)], fill=(200, 214, 226), width=1)
    for lat in range(-45, 86, 30):
        y = my + (85 - lat) / 145.0 * mh
        d.line([(mx, y), (mx + mw, y)], fill=(200, 214, 226), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx, my, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=(222, 205, 165), outline=(160, 145, 110))
    for num, lon, lat, kind in pins:
        px, py = project(lon, lat, mx, my, mw, mh)
        col = (178, 34, 34) if kind == "rep" else (200, 140, 20)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=col, outline=(255, 255, 255), width=1)
        f = SANS_B(8)
        tw = d.textlength(str(num), font=f)
        d.text((px - tw / 2, py - 4), str(num), font=f, fill=(255, 255, 255))

# ---------------- content ----------------

NUM_STRIP = [
    ("186", "drones fired", "overnight, 18 sites hit"),
    ("161", "shot down", "or jammed by defences"),
    ("720/9", "India declare", "top Test total in NZ"),
    ("98.79%", "HK turnout", "723 seats, 856 candidates"),
    ("$120bn", "adaptation dropped", "dropped from final text"),
    ("35%", "2035 power target", "kept in final text"),
    ("50", "Wembanyama pts", "Spurs 114–91"),
    ("258", "Dems seats", "biggest since 1992"),
]

REGIONS = [
    ("EUROPE 8", 8, (40, 90, 160)),
    ("MIDDLE EAST 7", 7, (200, 100, 30)),
    ("ASIA-PACIFIC 7", 7, (40, 130, 70)),
    ("AMERICAS 5", 5, (130, 70, 150)),
    ("AFRICA 3", 3, (150, 110, 40)),
    ("OCEANIA 3", 3, (40, 140, 140)),
    ("WORLD 3", 3, (110, 110, 110)),
]

UTC_ITEMS = "01:00 HK polls open · 03:00 COP31 objections close · 06:00 adoption vote · ~16:00 COP31 fails · 18:13 Dems 258 · 20:43 Alcaraz wins"

HEROES = [
    ("ANTALYA · POLITICS", "COP31 COLLAPSES — NO DEAL",
     "Final text drops all fossil-fuel language; the EU and ~130 parties reject it. "
     "Talks end after 44 hours overtime — the first failure since 2009.",
     "Reuters · AP · Guardian", "CONFIRMED", scene_cop31),
    ("KYIV · WAR", "186 DRONES OVER UKRAINE",
     "Russia fires 186 drones overnight; 161 shot down or jammed. A five-storey block "
     "in Dymer falls: 1 dead, 14 unaccounted for. Strikes hit 18 sites.",
     "Ukrainian Air Force · AP", "REPORTED", scene_drones),
    ("BAHRAIN · WAR", "IRAN CLAIMS 2 PATRIOT RADARS HIT",
     "Tehran says US Patriot radars at al-Riffa and Awali were hit. Bahrain denies "
     "a strike; Sitra burns, 2 hurt.",
     "IRGC vs Bahrain MoI", "CLAIM", scene_radar),
]

SMALL = [
    ("HONG KONG · POLITICS", "Hong Kong votes: 98.79% turnout",
     "5,640 of 5,709 voters voted.",
     "SCMP · Reuters", "CONFIRMED", "ballot"),
    ("LAS VEGAS · SPORT", "Verstappen wins by 0.639s",
     "Beats Norris; 75th win.",
     "F1 · Reuters", "CONFIRMED", "trophy"),
    ("TURIN · SPORT", "Alcaraz takes ATP Finals",
     "Beats Zverev 6–2, 7–6(7); first title.",
     "ATP · BBC", "CONFIRMED", "ball"),
    ("NEW ZEALAND · SPORT", "India declare 720/9",
     "Highest Test total in NZ; Rahul 136, Pant 128.",
     "ESPNcricinfo", "CONFIRMED", "bat"),
    ("CIKANDE · SOCIETY", "Candy-factory fire: 3 dead, 36 missing",
     "Began Sat. night; 15 survived.",
     "Detiknews · Basarnas", "REPORTED", "flame"),
    ("TEHRAN · SOCIETY", "Iran starts power rationing",
     "Blackouts ~2h a day; gas hit.",
     "Reuters", "REPORTED", "bolt"),
    ("DR CONGO · HEALTH", "Ebola cases reach 11,613",
     "WHO count; fighting traps medics.",
     "WHO · Reuters", "OFFICIAL", "virus"),
    ("SEOUL · SOCIETY", "Minister quits in AI-cheat scandal",
     "111 device cases; Choi resigns.",
     "Yonhap", "CONFIRMED", "chip"),
    ("CAPE CANAVERAL · SCIENCE", "Falcon 9 launches NROL-136",
     "32h turnaround; booster lands.",
     "SpaceX", "OFFICIAL", "rocket"),
    ("LIVERPOOL · SPORT", "Liverpool rout Man Utd 4–0",
     "Pochettino debut ends in a rout.",
     "BBC Sport", "CONFIRMED", "ball"),
]

ALSO = [
    (14, "Estonia closes 5 Russia crossings"),
    (15, "Denmark expels Russian attaché"),
    (16, "Belgium controllers join Monday strike"),
    (17, "Sparta II still burning, towed home"),
    (18, "Merkury corvette hit off Benghazi"),
    (19, "Saudi intercepts Houthi missile"),
    (20, "Gaza: aid-van strike, 3 dead"),
    (21, "Eisenkot invites Likud to coalition talks"),
    (22, "Settlers burn 12 cars, West Bank"),
    (23, "Nepal PM lands in Delhi"),
    (24, "Manipur liquor toll rises, ~600 treated"),
    (25, "EU–Indonesia deal signed (date split)"),
    (26, "Marles rejects AUKUS sub report"),
    (27, "Bolsonaro in intensive care"),
    (28, "Wembanyama scores 50"),
    (29, "FBI probes NCIC crime-database hack"),
    (30, "Drones kill 4 near Khartoum"),
    (31, "Nigeria boat capsizes: 24 dead"),
    (32, "Melbourne: 70 years since 1956 Games"),
    (33, "Fred Nile dies, 92"),
    (34, "Cummins stays Test captain"),
    (35, "Bitcoin back above $60,000"),
    (36, "Nvidia faces SEC accounting probe"),
]

# (num, lon, lat, kind) kind: rep = red pin, claim = amber pin.
# ME-cluster pins use small display offsets so their numbers stay readable.
PINS = [
    (1, 30.7, 36.9, "rep"), (2, 30.5, 50.45, "rep"), (3, 53.5, 27.5, "claim"),
    (4, 114.2, 22.3, "rep"), (5, -115.2, 36.1, "rep"), (6, 7.7, 45.07, "rep"),
    (7, 174.8, -41.3, "rep"), (8, 106.2, -6.1, "rep"), (9, 54.0, 37.0, "rep"),
    (10, 23.7, -2.9, "rep"), (11, 127.0, 37.6, "rep"), (12, -80.6, 28.4, "rep"),
    (13, -3.0, 53.4, "rep"), (14, 24.7, 59.4, "rep"), (15, 12.6, 55.7, "rep"),
    (16, 4.35, 50.85, "rep"), (17, 24.0, 35.5, "rep"), (18, 19.0, 33.5, "claim"),
    (19, 44.0, 22.5, "rep"), (20, 29.5, 29.5, "rep"), (21, 38.0, 33.5, "rep"),
    (22, 34.5, 39.5, "rep"), (23, 77.2, 28.6, "rep"), (24, 93.9, 24.8, "rep"),
    (25, 107.6, -6.8, "rep"), (26, 149.1, -35.3, "rep"), (27, -47.9, -15.8, "rep"),
    (28, -98.5, 29.4, "rep"), (29, -77.0, 38.9, "rep"), (30, 31.0, 14.0, "rep"),
    (31, 6.3, 4.9, "rep"), (32, 145.0, -37.8, "rep"), (33, 151.2, -33.9, "rep"),
    (34, 153.0, -27.5, "rep"), (35, -74.0, 40.7, "rep"), (36, -121.9, 37.4, "rep"),
]

# ---------------- build ----------------

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX, CW = 14, 996

    # top rule + kicker + masthead
    d.rectangle([0, 0, W, 4], fill=RED)
    d.text((MX, 10), "THE WORLD IN ONE DAY", font=SANS_B(13), fill=RED)
    r = d.textlength("36 STORIES · 7 REGIONS", font=SANS_B(12))
    d.text((MX + CW - r, 11), "36 STORIES · 7 REGIONS", font=SANS_B(12), fill=INK)
    d.text((MX, 26), "Sunday 22 November 2026", font=SERIF_B(40), fill=INK)
    d.text((MX, 70), "COP31 fails · 186 drones · Bahrain radar claim — the day the world said no",
           font=SERIF_I(15), fill=RED)
    d.line([(MX, 90), (MX + CW, 90)], fill=INK, width=2)

    # number strip
    y0, y1 = 94, 146
    cw = CW / 8
    for i, (num, lab, sub) in enumerate(NUM_STRIP):
        cx = MX + i * cw + cw / 2
        d.text((cx - d.textlength(num, font=SANS_B(25)) / 2, y0 + 2), num,
               font=SANS_B(25), fill=INK)
        d.text((cx - d.textlength(lab, font=SANS_B(10)) / 2, y0 + 30), lab,
               font=SANS_B(10), fill=INK)
        d.text((cx - d.textlength(sub, font=SANS(9)) / 2, y0 + 42), sub,
               font=SANS(9), fill=GREY)
        if i:
            d.line([(MX + i * cw, y0 + 4), (MX + i * cw, y1 - 4)], fill=LINE, width=1)
    d.line([(MX, y1), (MX + CW, y1)], fill=LINE, width=1)

    # region bar
    y0, y1 = 150, 172
    x = MX
    total = sum(c for _, c, _ in REGIONS)
    for name, cnt, col in REGIONS:
        wseg = CW * cnt / total
        d.rectangle([x, y0, x + wseg, y1], fill=col)
        f = SANS_B(11)
        tw = d.textlength(name, font=f)
        d.text((x + (wseg - tw) / 2, y0 + 5), name, font=f, fill=(255, 255, 255))
        x += wseg

    # UTC strip
    y0, y1 = 176, 194
    d.rectangle([MX, y0, MX + CW, y1], fill=NAVY)
    d.text((MX + 8, y0 + 3), "THE DAY IN UTC", font=SANS_B(11), fill=(255, 210, 90))
    d.text((MX + 118, y0 + 3), UTC_ITEMS, font=SANS(11), fill=(255, 255, 255))

    # heroes
    hy, hh, hw, gap = 198, 220, 326, 9
    for i, (kicker, title, body, src, chiplabel, scene) in enumerate(HEROES):
        hx = MX + i * (hw + gap)
        d.rectangle([hx, hy, hx + hw, hy + hh], outline=(170, 160, 145), width=1)
        scene(d, hx + 1, hy + 1, hw - 2, 104)
        ty = hy + 110
        d.text((hx + 8, ty), kicker, font=SANS_B(10), fill=RED)
        ty += 14
        n_title = len(wrap(d, title, SERIF_B(16), hw - 16))
        ty = text_wrapped(d, hx + 8, ty, title, SERIF_B(16), hw - 16, leading=19, max_lines=2)
        ty += 3
        body_max = 3 if n_title == 1 else 2
        text_wrapped(d, hx + 8, ty, body, SANS(11), hw - 16, leading=14, max_lines=body_max)
        by = hy + hh - 18
        wch = chip(d, hx + 8, by, chiplabel, CHIP_FILL[chiplabel])
        d.text((hx + 14 + wch, by + 2), "Source: " + src, font=SANS(9), fill=GREY)

    # small cards: 5 cols x 2 rows
    cy0, ch, cw2, gap2 = 418, 106, 192, 9
    for i, (kicker, title, body, src, chiplabel, kind) in enumerate(SMALL):
        row, col = divmod(i, 5)
        cx = MX + col * (cw2 + gap2)
        cy = cy0 + row * (ch + 8)
        d.rectangle([cx, cy, cx + cw2, cy + ch], outline=(170, 160, 145), width=1)
        top, bot = STRIPS[kind]
        strip_base(d, cx + 1, cy + 1, cw2 - 2, 34, top, bot)
        motif(d, cx + 1, cy + 1, cw2 - 2, 34, kind, (255, 255, 255))
        ty = cy + 38
        d.text((cx + 6, ty), kicker, font=SANS_B(8), fill=RED)
        ty += 11
        n_title = len(wrap(d, title, SANS_B(12), cw2 - 12))
        ty = text_wrapped(d, cx + 6, ty, title, SANS_B(12), cw2 - 12, leading=14, max_lines=2)
        ty += 2
        body_max = 2 if n_title == 1 else 1
        text_wrapped(d, cx + 6, ty, body, SANS(10), cw2 - 12, leading=12, max_lines=body_max)
        by = cy + ch - 15
        wch = chip(d, cx + 6, by, chiplabel, CHIP_FILL[chiplabel])
        sw = d.textlength(src, font=SANS(8))
        d.text((cx + cw2 - 6 - sw, by + 2), src, font=SANS(8), fill=GREY)

    # map + also list
    my = 640
    d.text((MX, my), "THE WORLD — WHERE IT HAPPENED", font=SANS_B(12), fill=RED)
    lg = "Red pin = reported · Amber pin = claim"
    d.text((MX + 456 - d.textlength(lg, font=SANS(9)), my + 2), lg, font=SANS(9), fill=GREY)
    d.text((482, my), "ALSO ON SUNDAY — 23 MORE STORIES", font=SANS_B(12), fill=RED)
    draw_map(d, MX, my + 18, 456, 182, PINS)
    lx = 482
    col_w = 264
    for i, (num, item) in enumerate(ALSO):
        col = 0 if i < 12 else 1
        row = i if i < 12 else i - 12
        x = lx + col * col_w
        y = my + 20 + row * 15
        d.text((x, y), f"{num}", font=SANS_B(10), fill=RED)
        d.text((x + 20, y), item, font=SANS(10), fill=INK)

    # DATE CHECK
    dy0, dy1 = 850, 956
    d.rectangle([MX, dy0, MX + CW, dy1], outline=RED, width=2)
    d.text((MX + 8, dy0 + 6), "DATE CHECK", font=SANS_B(13), fill=RED)
    d.text((MX + 108, dy0 + 7),
           "Every story above happened or was first reported on Sunday 22 Nov 2026. "
           "Wires read up to 23:00 UTC.", font=SANS_B(11), fill=INK)
    d.text((MX + 8, dy0 + 28), "LEFT OUT (not 22 Nov):", font=SANS_B(11), fill=INK)
    text_wrapped(d, MX + 8, dy0 + 44,
                 "400-drone barrage (19–20 Nov) · El Chapo Isidro captured (Fri 20 Nov) · "
                 "BepiColombo Mercury orbit (Sat 21 Nov, burn 18:24 GMT) · Kryvyi Rih "
                 "(Fri 20 Nov night) · Peru quake (Fri 20 Nov) · Hormuz tankers hit "
                 "(Sat 21 Nov 05:00 GMT, reported Sun 17:13 UTC) · Gaza toll 1.661 · "
                 "Mongolia vote · cartel boss · Fidan/Druze · Pezeshkian · Hind Rajab",
                 SANS(10), CW - 16, leading=13, max_lines=2)
    d.text((MX + 8, dy0 + 74), "NOT YET:", font=SANS_B(11), fill=INK)
    d.text((MX + 72, dy0 + 74),
           "Dymer final toll · 4 House races uncalled · EU–Indonesia deal date split "
           "(Sat 21 vs Sun 22) · Sparta II hit Sat 21, still burning Sun · COP32 venue undecided",
           font=SANS(10), fill=INK)

    # footer
    fy = 962
    d.text((MX, fy), "SOURCES: AP · Reuters · BBC · CNN · Guardian · France 24 · Al Jazeera · "
           "Yonhap · Anadolu · Detiknews · WHO · SpaceX", font=SANS(9), fill=GREY)
    d.text((MX, fy + 13),
           "CONFIRMED = 2+ outlets · REPORTED = carried by the wires today · "
           "CLAIM = one side, unverified · OFFICIAL = recorded result",
           font=SANS(9), fill=GREY)
    d.text((MX, fy + 26), "Scenes are drawn illustrations, not photographs.",
           font=SANS_O(9), fill=GREY)

    img.save("entry.png")
    print("saved entry.png", img.size)

if __name__ == "__main__":
    build()
