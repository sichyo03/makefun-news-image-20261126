#!/usr/bin/env python3
"""Draw the 26 November 2026 news image: a dense broadsheet infographic.

Layout (1024x1024, cream paper, navy/black/red, flat vector scenes):
giant date masthead, numbers strip, region bar, UTC timeline, 3 lead
panels + 10 small panels (each with scene, kicker, headline, summary,
source and a "how sure" badge), a world map with numbered pins,
22 one-line briefs, a DATE CHECK footer and the how-sure legend.
35 stories in all, every one first reported on Thursday 26 November 2026.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (24, 24, 24)
NAVY = (20, 33, 61)
RED = (179, 35, 27)
GOLD = (201, 148, 42)
GREY = (96, 96, 96)
LINE = (180, 174, 158)

F = "/usr/share/fonts/truetype/noto/"
SERIF_BLACK = F + "NotoSerif-Black.ttf"
SERIF_BOLD = F + "NotoSerif-Bold.ttf"
SERIF = F + "NotoSerif-Regular.ttf"
SANS = F + "NotoSans-Regular.ttf"
SANS_BOLD = F + "NotoSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_w(s, f):
    return d.textlength(s, font=f)

def wrap(s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if text_w(t, f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def draw_lines(x, y, lines, f, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y

def badge(x, y, label, fill, txt=(255, 255, 255)):
    f = font(SANS_BOLD, 8)
    w = text_w(label, f) + 8
    d.rounded_rectangle([x, y, x + w, y + 13], 3, fill=fill)
    d.text((x + 4, y + 2), label, font=f, fill=txt)
    return w

BADGE_COLORS = {
    "OFFICIAL": (31, 94, 46),
    "CONFIRMED": (20, 33, 61),
    "REPORTED": (120, 90, 20),
    "CLAIM": (179, 35, 27),
    "ONGOING": (110, 60, 140),
}

def num_chip(x, y, n, color=RED):
    d.ellipse([x, y, x + 18, y + 18], fill=color)
    f = font(SANS_BOLD, 10)
    s = str(n)
    d.text((x + 9 - text_w(s, f) / 2, y + 3), s, font=f, fill=(255, 255, 255))

# ---------------------------------------------------------------- top strip
d.rectangle([0, 0, W, 24], fill=NAVY)
f_top = font(SANS_BOLD, 11)
d.text((14, 6), "THE WORLD IN ONE DAY", font=f_top, fill=(255, 255, 255))
right = "35 STORIES · 9 REGIONS · 23 SOURCES · 14 FIELDS · EVERY ONE FIRST REPORTED THU 26 NOV 2026"
d.text((W - 14 - text_w(right, f_top), 6), right, font=f_top, fill=(255, 255, 255))

# ---------------------------------------------------------------- masthead
d.line([14, 32, W - 14, 32], fill=INK, width=2)
f_mast = font(SERIF_BLACK, 56)
title = "Thursday 26 November 2026"
d.text(((W - text_w(title, f_mast)) / 2, 36), title, font=f_mast, fill=INK)
d.line([14, 100, W - 14, 100], fill=INK, width=2)
f_deck = font(SERIF, 14)
deck = ("A nor'easter grounds New York's 100th Thanksgiving parade, EU leaders split over "
        "Ukraine's €45bn loan, and Seoul raises rates as growth beats forecasts.")
d.text(((W - text_w(deck, f_deck)) / 2, 104), deck, font=f_deck, fill=(60, 60, 60))

# ---------------------------------------------------------------- numbers strip
numbers = [
    ("100th", "Macy's parade postponed"),
    ("€45bn", "Ukraine loan at stake"),
    ("3.25%", "Bank of Korea base rate"),
    ("112", "drones fired at Ukraine"),
    ("12,000+", "Ebola cases, DR Congo"),
    ("77,000", "UK net migration"),
]
ny0, ny1 = 126, 176
cell_w = (W - 28) / 6
for i, (big, cap) in enumerate(numbers):
    x = 14 + i * cell_w
    d.rectangle([x, ny0, x + cell_w - 4, ny1], outline=LINE, width=1)
    fb = font(SERIF_BLACK, 24)
    col = RED if i % 2 == 0 else NAVY
    d.text((x + 8, ny0 + 4), big, font=fb, fill=col)
    fc = font(SANS, 9)
    draw_lines(x + 8, ny0 + 34, wrap(cap, fc, cell_w - 18)[:2], fc, GREY, 11)

# ---------------------------------------------------------------- region bar
regions = [
    ("EUROPE", 10, (20, 33, 61)), ("E. ASIA", 4, (179, 35, 27)),
    ("N. AMERICA", 4, (31, 94, 46)), ("AFRICA", 4, (201, 148, 42)),
    ("M. EAST", 3, (110, 60, 140)), ("SE ASIA", 3, (0, 110, 110)),
    ("S. ASIA", 2, (200, 100, 30)), ("OCEANIA", 2, (70, 130, 180)),
    ("S. AMERICA", 2, (150, 60, 90)), ("WORLD", 1, (90, 90, 90)),
]
ry0, ry1 = 180, 200
total = sum(c for _, c, _ in regions)
fr = font(SANS_BOLD, 8)
min_w = {name: text_w(f"{name} {cnt}", fr) + 8 for name, cnt, _ in regions}
extra = (W - 28) - sum(min_w.values())
x = 14.0
for name, cnt, col in regions:
    w = min_w[name] + extra * cnt / total
    d.rectangle([x, ry0, x + w - 1, ry1], fill=col)
    lab = f"{name} {cnt}"
    d.text((x + (w - text_w(lab, fr)) / 2, ry0 + 5), lab, font=fr, fill=(255, 255, 255))
    x += w

# ---------------------------------------------------------------- UTC timeline
uy0 = 206
d.rectangle([14, uy0, W - 14, uy0 + 26], outline=LINE, width=1)
f_utc_h = font(SANS_BOLD, 10)
d.text((20, uy0 + 7), "THE DAY IN UTC", font=f_utc_h, fill=RED)
utc_items = [
    ("00:00", "Thanksgiving begins (US)"),
    ("01:30", "Korea hikes rate"),
    ("06:00", "Delhi: Constitution Day"),
    ("09:00", "EU leaders in Brussels"),
    ("13:30", "Macy's parade due to step off"),
    ("14:00", "Chess Game 3, Geneva"),
    ("23:00", "35 stories filed"),
]
f_utc = font(SANS, 9)
f_utc_b = font(SANS_BOLD, 9)
x = 128
for t, s in utc_items:
    d.text((x, uy0 + 8), t, font=f_utc_b, fill=NAVY)
    x += text_w(t, f_utc_b) + 3
    d.text((x, uy0 + 8), s, font=f_utc, fill=INK)
    x += text_w(s, f_utc) + 9

# ---------------------------------------------------------------- scenes
def scene_parade(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 44, 74))
    for i in range(7):  # skyline
        bw = w / 8
        bh = h * (0.45 + 0.08 * ((i * 37) % 5))
        d.rectangle([x + i * bw + 2, y + h - bh, x + (i + 1) * bw - 3, y + h], fill=(16, 24, 44))
        for wy in range(3):
            d.rectangle([x + i * bw + 5, y + h - bh + 5 + wy * 9, x + i * bw + 9, y + h - bh + 8 + wy * 9],
                        fill=(240, 200, 90))
    for i in range(5):  # wind streaks
        wy = y + 8 + i * 7
        d.line([x + 6 + i * 14, wy, x + 60 + i * 14, wy - 3], fill=(180, 200, 230), width=2)
    # deflated balloon
    d.ellipse([x + w * 0.55, y + h * 0.30, x + w * 0.88, y + h * 0.62], fill=(245, 245, 240))
    d.ellipse([x + w * 0.66, y + h * 0.40, x + w * 0.70, y + h * 0.47], fill=INK)
    d.ellipse([x + w * 0.76, y + h * 0.40, x + w * 0.80, y + h * 0.47], fill=INK)
    d.ellipse([x + w * 0.70, y + h * 0.50, x + w * 0.76, y + h * 0.56], fill=RED)
    d.rectangle([x + 4, y + h - 18, x + 150, y + h - 3], fill=RED)
    d.text((x + 8, y + h - 15), "POSTPONED TO SATURDAY", font=font(SANS_BOLD, 9), fill=(255, 255, 255))
    d.ellipse([x + w - 34, y + h - 30, x + w - 6, y + h - 2], fill=GOLD)
    d.text((x + w - 28, y + h - 22), "100", font=font(SANS_BOLD, 10), fill=INK)

def scene_eu(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 52, 120))
    cx, cy, r = x + w * 0.30, y + h * 0.52, h * 0.34
    for i in range(12):
        a = 2 * math.pi * i / 12
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(245, 205, 60))
    d.text((cx - 9, cy - 13), "€", font=font(SERIF_BLACK, 24), fill=(255, 255, 255))
    # split bar
    bx = x + w * 0.55
    d.rectangle([bx, y + h * 0.30, bx + w * 0.40, y + h * 0.52], fill=(245, 205, 60))
    d.rectangle([bx, y + h * 0.30, bx + w * 0.22, y + h * 0.52], fill=(179, 35, 27))
    d.text((bx, y + h * 0.58), "€45bn LOAN", font=font(SANS_BOLD, 11), fill=(255, 255, 255))
    d.text((bx, y + h * 0.74), "SUMMIT SPLIT", font=font(SANS_BOLD, 9), fill=(200, 215, 245))

def scene_korea(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 248, 240))
    d.line([x + 10, y + h - 12, x + w - 70, y + h - 12], fill=GREY, width=1)
    pts = []
    for i in range(6):
        px = x + 14 + i * (w - 110) / 5
        py = y + h - 16 - (i * i) * (h * 0.55) / 25
        pts.append((px, py))
    d.line(pts, fill=RED, width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.text((x + w - 92, y + 8), "3.25%", font=font(SERIF_BLACK, 26), fill=NAVY)
    d.text((x + w - 92, y + 40), "BASE RATE +25bp", font=font(SANS_BOLD, 8), fill=GREY)
    d.text((x + 10, y + 8), "KRW", font=font(SERIF_BLACK, 18), fill=NAVY)

def scene_drone_strike(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 40, 48))
    cx, cy = x + w * 0.5, y + h * 0.35
    d.ellipse([cx - 10, cy - 5, cx + 10, cy + 5], fill=(200, 200, 200))
    for dx, dy in [(-18, -10), (18, -10), (-18, 10), (18, 10)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=(200, 200, 200), width=2)
        d.ellipse([cx + dx - 5, cy + dy - 2, cx + dx + 5, cy + dy + 2], fill=(160, 160, 160))
    d.polygon([(x + w * 0.3, y + h), (x + w * 0.5, y + h * 0.55), (x + w * 0.7, y + h)], fill=(230, 120, 40))
    d.polygon([(x + w * 0.38, y + h), (x + w * 0.5, y + h * 0.68), (x + w * 0.62, y + h)], fill=(245, 200, 60))

def scene_barrage(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 20, 38))
    for i in range(9):
        px = x + 10 + (i * 53) % (w - 20)
        py = y + 6 + (i * 29) % (h // 2)
        d.ellipse([px - 4, py - 2, px + 4, py + 2], fill=(220, 220, 220))
        d.line([px - 8, py - 4, px + 8, py + 4], fill=(150, 150, 150), width=1)
    for i in range(6):
        bw = w / 7
        bh = h * (0.3 + 0.06 * ((i * 41) % 4))
        d.rectangle([x + i * bw + 2, y + h - bh, x + (i + 1) * bw - 2, y + h], fill=(8, 10, 20))
    d.text((x + 4, y + h - 14), "112 DRONES", font=font(SANS_BOLD, 9), fill=(240, 200, 90))

def scene_gaza(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 195, 170))
    for i in range(4):
        bx = x + 8 + i * (w / 4)
        d.rectangle([bx, y + h * 0.55, bx + w / 5, y + h], fill=(150, 135, 110))
    for i in range(3):
        sx = x + w * (0.25 + 0.25 * i)
        for j in range(4):
            r = 5 + j * 3
            d.ellipse([sx - r, y + h * 0.5 - j * 9 - r, sx + r, y + h * 0.5 - j * 9 + r], fill=(90, 90, 90))

def scene_candles(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 30, 30))
    d.polygon([(x + w * 0.35, y + h * 0.75), (x + w * 0.5, y + h * 0.2), (x + w * 0.65, y + h * 0.75)],
              fill=(120, 90, 70))
    for i in range(7):
        cx = x + 8 + i * (w - 16) / 6
        d.rectangle([cx - 2, y + h - 14, cx + 2, y + h - 4], fill=(240, 235, 220))
        d.ellipse([cx - 2, y + h - 20, cx + 2, y + h - 13], fill=(245, 180, 60))
    d.text((x + w - 58, y + 3), "18 YEARS", font=font(SANS_BOLD, 9), fill=(255, 220, 160))

def scene_chess(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 60, 45))
    sq = (h - 8) / 8
    ox = x + 6
    for r in range(8):
        for c in range(8):
            col = (235, 225, 200) if (r + c) % 2 == 0 else (110, 130, 100)
            d.rectangle([ox + c * sq, y + 4 + r * sq, ox + (c + 1) * sq, y + 4 + (r + 1) * sq], fill=col)
    d.text((x + w * 0.55, y + 8), "1.5 – 1.5", font=font(SERIF_BLACK, 16), fill=(255, 255, 255))
    d.text((x + w * 0.55, y + 32), "GAME 3 · GENEVA", font=font(SANS_BOLD, 8), fill=(200, 230, 200))

def scene_refinery(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 210, 220))
    for i in range(3):
        tx = x + 12 + i * (w / 3.2)
        d.rectangle([tx, y + h * 0.25, tx + 12, y + h], fill=(120, 125, 135))
        d.rectangle([tx + 2, y + h * 0.18, tx + 10, y + h * 0.25], fill=(90, 95, 105))
    d.polygon([(x + w * 0.55, y + h * 0.6), (x + w * 0.68, y + h * 0.25), (x + w * 0.8, y + h * 0.6)],
              fill=(230, 120, 40))
    d.ellipse([x + w * 0.6, y + h * 0.1, x + w * 0.85, y + h * 0.3], fill=(80, 80, 80))

def scene_ebola(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 230, 220))
    for i in range(8):
        px = x + 12 + (i * 47) % (w - 24)
        py = y + 8 + (i * 31) % (h - 20)
        r = 6 + (i % 3) * 2
        d.ellipse([px - r, py - r, px + r, py + r], fill=(160, 40, 40))
        for a in range(6):
            ang = a * math.pi / 3 + i
            d.line([px, py, px + (r + 4) * math.cos(ang), py + (r + 4) * math.sin(ang)], fill=(160, 40, 40), width=2)
    d.rectangle([x + 2, y + h - 17, x + 92, y + h - 3], fill=(240, 230, 220))
    d.text((x + 4, y + h - 15), "12,000+ CASES", font=font(SANS_BOLD, 9), fill=(120, 20, 20))

def scene_ecb(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 232, 240))
    d.rectangle([x + w * 0.42, y + 6, x + w * 0.58, y + h], fill=(70, 90, 130))
    for r in range(4):
        for c in range(2):
            d.rectangle([x + w * 0.44 + c * 10, y + 10 + r * 10, x + w * 0.44 + c * 10 + 6, y + 16 + r * 10],
                        fill=(200, 220, 245))
    d.text((x + 6, y + 8), "€", font=font(SERIF_BLACK, 26), fill=NAVY)
    d.text((x + 6, y + h - 14), "NEXT ECB CHIEF", font=font(SANS_BOLD, 8), fill=NAVY)

def scene_missile(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 40))
    mx, my = x + w * 0.55, y + h * 0.55
    d.polygon([(mx, my - 26), (mx - 6, my), (mx + 6, my)], fill=(220, 220, 220))
    d.rectangle([mx - 6, my, mx + 6, my + 14], fill=(190, 190, 190))
    d.polygon([(mx - 6, my + 14), (mx, my + 26), (mx + 6, my + 14)], fill=(230, 120, 40))
    for i in range(4):
        d.ellipse([mx - 4, my + 28 + i * 5, mx + 4, my + 34 + i * 5], fill=(140, 140, 140))
    d.text((x + 4, y + 4), "KCNA", font=font(SANS_BOLD, 8), fill=(200, 200, 200))

def scene_ballot(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 240, 225))
    bx, by = x + w * 0.35, y + h * 0.45
    d.rectangle([bx, by, bx + w * 0.3, y + h - 4], fill=(90, 110, 70))
    d.rectangle([bx + 4, by - 3, bx + w * 0.3 - 4, by + 2], fill=INK)
    d.rectangle([bx + w * 0.08, by - 16, bx + w * 0.22, by - 2], fill=(255, 255, 255), outline=INK)
    d.line([bx + w * 0.08, by - 16, bx + w * 0.22, by - 2], fill=RED, width=2)
    d.line([bx + w * 0.22, by - 16, bx + w * 0.08, by - 2], fill=RED, width=2)
    d.text((x + w * 0.7, y + 8), "2028", font=font(SERIF_BLACK, 18), fill=RED)

# ---------------------------------------------------------------- panels
def panel(x, y, w, h, n, kicker, headline, summary, source, sure, scene, why=None, big=False):
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1)
    sh = 92 if big else 54
    scene(x + 1, y + 1, w - 2, sh)
    num_chip(x + 4, y + 4, n)
    ty = y + sh + 6
    fk = font(SANS_BOLD, 8.5 if big else 7.5)
    d.text((x + 6, ty), kicker, font=fk, fill=RED)
    ty += 13 if big else 11
    fh = font(SERIF_BOLD, 15 if big else 11)
    hl = wrap(headline, fh, w - 12)[:2]
    ty = draw_lines(x + 6, ty, hl, fh, INK, 17 if big else 13)
    ty += 1
    fs = font(SANS, 10 if big else 8.5)
    sl = wrap(summary, fs, w - 12)[:2]
    ty = draw_lines(x + 6, ty, sl, fs, (50, 50, 50), 12 if big else 10.5)
    if why:
        fw = font(SANS, 9)
        wl = wrap("WHY IT MATTERS: " + why, fw, w - 12)[:2]
        ty = draw_lines(x + 6, ty + 1, wl, fw, NAVY, 11)
    # source + badge pinned to bottom
    fsrc = font(SANS, 8)
    d.text((x + 6, y + h - 15), "SOURCE: " + source, font=fsrc, fill=GREY)
    bw = text_w(sure, font(SANS_BOLD, 8)) + 8
    badge(x + w - bw - 5, y + h - 16, sure, BADGE_COLORS[sure])

leads = [
    (1, "NEW YORK · WEATHER", "Nor'easter grounds Macy's 100th Thanksgiving parade",
     "60 mph gusts force the parade to Saturday — the first weather postponement in 100 years.",
     "AP", "REPORTED", scene_parade, "A century-old ritual yields to a storm."),
    (2, "BRUSSELS · EUROPE", "EU summit splits over budget and €45bn Ukraine loan",
     "Leaders divide on the 2028–34 budget (~€1.58tn) and a €45bn loan for Kyiv.",
     "EU COUNCIL · AP", "CONFIRMED", scene_eu, "Ukraine's funding hangs on the bloc's unity."),
    (3, "SEOUL · MARKETS", "Bank of Korea hikes rate to 3.25%, lifts growth view",
     "A 25bp rise; the 2026 GDP forecast is raised to 3.9%.",
     "BOK · REUTERS", "OFFICIAL", scene_korea, "Seoul tightens as chip-led growth beats forecasts."),
]
lw = (W - 28 - 16) / 3
for i, (n, k, hd, sm, src, sure, sc, why) in enumerate(leads):
    panel(14 + i * (lw + 8), 238, lw, 196, n, k, hd, sm, src, sure, sc, why, big=True)

row2 = [
    (4, "KUWAIT CITY · M. EAST", "Drone strike kills two Italian technicians",
     "Italy and Kuwait blame Iran; Tehran denies it.", "REUTERS · AP", "REPORTED", scene_drone_strike),
    (5, "KYIV · WAR", "Russia fires 112 drones at Ukraine overnight",
     "Kyiv and Kharkiv hit; power cut across six regions.", "AP · REUTERS", "CONFIRMED", scene_barrage),
    (6, "GAZA CITY · WAR", "Israeli strikes kill 10 in Gaza",
     "Hamas official Khaled Abu Nada among the dead.", "AP", "REPORTED", scene_gaza),
    (7, "MUMBAI · INDIA", "India marks 18 years since 26/11 attacks",
     "Tributes nationwide; also the 77th Constitution Day.", "PTI", "CONFIRMED", scene_candles),
    (8, "GENEVA · CHESS", "Gukesh–Sindarov Game 3 ends drawn",
     "60 moves; the world title match is level 1.5–1.5.", "FIDE", "ONGOING", scene_chess),
]
row3 = [
    (9, "BANGKOK · ENERGY", "Refinery blast injures nine workers",
     "Explosion and fire at the Bangchak plant.", "AL JAZEERA · CNA", "REPORTED", scene_refinery),
    (10, "KINSHASA · HEALTH", "DR Congo Ebola cases pass 12,000",
     "Responders evacuated amid fighting.", "WHO · UN", "OFFICIAL", scene_ebola),
    (11, "MADRID · EUROPE", "De Cos picked to succeed Lagarde at ECB",
     "Spain's Pablo Hernández de Cos chosen as next president.", "EURONEWS", "REPORTED", scene_ecb),
    (12, "PYONGYANG · ASIA", "Kim vows more nuclear weapons",
     "North Korea says it will expand its arsenal.", "KCNA", "CLAIM", scene_missile),
    (13, "BISSAU · AFRICA", "Guinea-Bissau junta delays elections to 2028",
     "The military rulers push the vote back two years.", "AP", "REPORTED", scene_ballot),
]
sw = (W - 28 - 32) / 5
for i, (n, k, hd, sm, src, sure, sc) in enumerate(row2):
    panel(14 + i * (sw + 8), 440, sw, 138, n, k, hd, sm, src, sure, sc)
for i, (n, k, hd, sm, src, sure, sc) in enumerate(row3):
    panel(14 + i * (sw + 8), 584, sw, 138, n, k, hd, sm, src, sure, sc)

# ---------------------------------------------------------------- map
mx0, my0, mw, mh = 14, 728, 330, 158
d.rectangle([mx0, my0, mx0 + mw, my0 + mh], outline=LINE, width=1)
d.text((mx0 + 6, my0 + 4), "WHERE IT HAPPENED — PINS 1–13", font=font(SANS_BOLD, 9), fill=RED)

CONTINENTS = [
    [(-168,66),(-140,70),(-125,71),(-110,68),(-95,69),(-85,66),(-80,73),(-75,72),(-65,60),(-55,52),(-60,46),(-70,44),(-74,40),(-76,35),(-80,32),(-81,26),(-84,30),(-89,30),(-94,29),(-97,26),(-97,22),(-94,18),(-90,15),(-83,9),(-79,9),(-81,13),(-87,15),(-92,15),(-97,16),(-102,18),(-105,20),(-110,23),(-114,29),(-117,33),(-122,37),(-124,46),(-130,54),(-140,60),(-152,60),(-162,61)],
    [(-79,9),(-72,12),(-64,10),(-52,5),(-44,-3),(-35,-8),(-39,-13),(-40,-20),(-48,-26),(-52,-33),(-58,-39),(-62,-41),(-65,-45),(-67,-50),(-69,-54),(-71,-54),(-73,-50),(-73,-44),(-72,-37),(-70,-30),(-70,-20),(-75,-15),(-79,-8),(-81,-4),(-80,1),(-77,4)],
    [(-9,43),(-2,44),(0,46),(-5,48),(-1,50),(2,51),(5,53),(8,55),(8,57),(10,59),(5,60),(5,62),(10,64),(14,67),(18,69),(25,71),(31,70),(40,68),(50,69),(60,69),(68,69),(75,72),(85,73),(95,76),(105,77),(115,73),(125,72),(135,71),(145,72),(155,70),(165,69),(175,66),(178,65),(170,60),(162,58),(158,52),(156,50),(142,50),(140,45),(135,35),(129,33),(122,31),(120,25),(110,20),(108,12),(105,9),(103,2),(100,6),(98,10),(97,15),(92,16),(89,22),(86,20),(80,13),(77,8),(72,20),(66,25),(61,25),(57,27),(52,28),(50,29),(48,30),(44,29),(43,12),(40,15),(38,20),(35,28),(34,31),(36,36),(30,36),(27,37),(23,36),(19,40),(15,38),(12,44),(10,44),(7,44),(3,43),(0,39),(-2,37),(-6,36),(-9,37)],
    [(-17,15),(-16,21),(-15,27),(-10,31),(-6,35),(0,36),(10,37),(11,34),(15,32),(20,32),(25,32),(30,31),(32,31),(34,28),(35,24),(37,22),(39,20),(40,15),(43,12),(48,11),(51,12),(51,10),(48,5),(42,-2),(40,-6),(40,-10),(38,-18),(36,-22),(33,-26),(31,-29),(28,-33),(20,-35),(17,-32),(15,-27),(12,-18),(13,-12),(9,-1),(9,4),(4,6),(-2,5),(-8,5),(-13,8),(-17,12)],
    [(113,-22),(114,-28),(115,-34),(118,-35),(124,-33),(129,-32),(132,-32),(135,-35),(138,-36),(140,-38),(145,-38),(150,-37),(153,-30),(153,-27),(151,-24),(149,-20),(146,-19),(142,-11),(142,-14),(141,-17),(136,-15),(135,-12),(132,-11),(130,-12),(126,-14),(122,-17),(118,-20)],
]
def proj(lon, lat):
    return (mx0 + 6 + (lon + 180) / 360 * (mw - 12),
            my0 + 20 + (78 - lat) / 138 * (mh - 26))
for poly in CONTINENTS:
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=(205, 212, 195), outline=(150, 155, 140))
PINS = {1: (-74, 40), 2: (4, 51), 3: (127, 37), 4: (48, 29), 5: (30, 50), 6: (34, 31),
        7: (73, 19), 8: (6, 46), 9: (100, 14), 10: (15, -4), 11: (-4, 40), 12: (126, 39), 13: (-15, 12)}
for n, (lon, lat) in PINS.items():
    px, py = proj(lon, lat)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED)
    f = font(SANS_BOLD, 8)
    s = str(n)
    d.text((px - text_w(s, f) / 2, py - 5), s, font=f, fill=(255, 255, 255))

# ---------------------------------------------------------------- briefs
briefs = [
    (14, "IBIZA — Diesel tanker capsizes; one crew dead", "AP"),
    (15, "PARIS — Depardieu ordered to stand trial", "AFP"),
    (16, "LONDON — UK net migration falls to 77,000", "ONS"),
    (17, "BLUE NILE — Sudan drone attacks kill 15+", "Reuters"),
    (18, "KYIV — 250 fallen soldiers recovered in swap", "ICRC"),
    (19, "CANBERRA — Capex jumps 12.2% on AI data centres", "ABS"),
    (20, "SYDNEY — Virgin Australia staff strike at 4 airports", "ABC"),
    (21, "BOGOR — Flooded gold mine: 13 dead, 13 missing", "AP"),
    (22, "NEW YORK — Storms cancel 1,000+ flights; 600k lose power", "NBC"),
    (23, "MOSCOW — Leaked data put war dead near 500,000", "BBC"),
    (24, "RIYADH — Houthi missiles aimed at capital intercepted", "Reuters"),
    (25, "BEIJING — China unveils 2030 6G roadmap", "Global Times"),
    (26, "PYONGYANG — Swiss envoy expelled, 48 hours to leave", "Yonhap"),
    (27, "CARTAGENA — Police free 20 supermarket hostages", "AP"),
    (28, "GULF OF MEXICO — Plane crashes into sea; six aboard", "AP"),
    (29, "MADRID — Bellingham stunner as Real Madrid rout PSV", "UEFA"),
    (30, "PATNA — Sooryavanshi, 15, hits 204 off 53 balls", "Cricinfo"),
    (31, "SAO PAULO — Mosquitoes cut viral infections 88%", "Study"),
    (32, "SPACE — Hera reveals DART crater on Dimorphos", "ESA"),
    (33, "NEW YORK — Tempus buys Personalis, $600m", "Investing.com"),
    (34, "KUALA LUMPUR — Malaysia sues Google over YouTube", "Reuters"),
    (35, "CAMEROON — Swiss tourist killed by elephants", "AP"),
]
bx0 = 356
d.text((bx0, my0 + 2), "ALSO ON THURSDAY 26 NOVEMBER — 22 MORE STORIES", font=font(SANS_BOLD, 10), fill=RED)
fb = font(SANS, 9.5)
fbn = font(SANS_BOLD, 9.5)
col_w = (W - 14 - bx0 - 8) / 2
for i, (n, txt, src) in enumerate(briefs):
    col = 0 if i < 11 else 1
    row = i if i < 11 else i - 11
    x = bx0 + col * (col_w + 8)
    y = my0 + 20 + row * 12.4
    d.text((x, y), f"{n}.", font=fbn, fill=RED)
    line = f"{txt} — {src}"
    while text_w(line, fb) > col_w - 22 and len(line) > 10:
        line = line[:-2]
    d.text((x + 20, y), line, font=fb, fill=INK)

# ---------------------------------------------------------------- date check
dy0 = 890
d.rectangle([14, dy0, W - 14, dy0 + 66], outline=RED, width=2)
d.text((22, dy0 + 5), "DATE CHECK — THESE ARE NOT 26 NOVEMBER, SO THEY ARE LEFT OUT", font=font(SANS_BOLD, 10), fill=RED)
excl = [
    "US tariff plan on 14 economies — 25 Nov",
    "Netanyahu bribery-charge suggestion — 25 Nov",
    "Solomon Islands–Australia treaty — 25 Nov",
    "Cairo tanker fire, 31 dead — 25 Nov",
    "Kospi −6.2% AI sell-off — 25 Nov",
    "Shenzhou-24 docking — 25 Nov",
    "Ras Tanura refinery strike — 25 Nov",
    "UK energy price cap — 25 Nov",
    "Dhaka garment wage rise — 25 Nov",
    "Nvidia reinstates Jensen Huang — 24 Nov",
    "Belgium national strike — 23 Nov",
    "COP31 ends without a deal — 22 Nov",
    "Ukraine sinks corvette off Libya — 22 Nov",
    "ICJ Rohingya ruling — 19 Nov",
]
fx = font(SANS, 8.5)
for i, e in enumerate(excl):
    col = i // 5
    row = i % 5
    x = 22 + col * 332
    y = dy0 + 20 + row * 9.5
    d.text((x, y), "x " + e, font=fx, fill=(70, 70, 70))

# ---------------------------------------------------------------- legend
ly = 960
d.line([14, ly, W - 14, ly], fill=INK, width=1)
f_leg = font(SANS, 8)
legend = ("HOW SURE: OFFICIAL = an authority's own word · CONFIRMED = wire or two sources · "
          "REPORTED = one named outlet · CLAIM = one side's account · ONGOING = still unfolding")
d.text((14, ly + 4), legend, font=f_leg, fill=GREY)
f_foot = font(SERIF, 9.5)
foot = ("Every story here happened or was first reported on Thursday 26 November 2026. Sources are named on each story. "
        "Scenes are original drawings, not photographs.")
d.text(((W - text_w(foot, f_foot)) / 2, ly + 18), foot, font=f_foot, fill=(60, 60, 60))
f_bot = font(SANS_BOLD, 9)
bot = "THE WORLD IN ONE DAY · THU 26 NOV 2026 · 35 STORIES · 9 REGIONS"
d.text(((W - text_w(bot, f_bot)) / 2, ly + 34), bot, font=f_bot, fill=INK)

img.save("entry.png", optimize=True)
print("saved entry.png")
