#!/usr/bin/env python3
"""Draw the 26 November 2026 broadsheet front page (1024x1024 PNG).

Build-time generator for the make.fun news-image-20261126 entry.
The submitted program (main.ts) copies the PNG this script produces.
Everything is drawn with PIL shapes and text: no network, no photos.
Every story below was verified as first reported on Thu 26 Nov 2026.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
PAPER = (250, 246, 236)
INK = (24, 24, 28)
NAVY = (16, 34, 74)
RED = (178, 32, 40)
GREY = (96, 96, 104)
RULE = (196, 188, 172)
CREAM = (244, 238, 222)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
DEJA_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- data
# (kicker, headline, summary, why-or-None, source, badge, scene, region)
LEADS = [
    ("NEW YORK · WEATHER", "Nor'easter grounds Macy's 100th Thanksgiving parade",
     "60 mph gusts force the parade to Saturday — the first weather postponement in 100 years.",
     "A century-old ritual yields to a storm.", "AP", "REPORTED", "balloon", "N. AMERICA"),
    ("BRUSSELS · EUROPE", "EU summit splits over budget and €45bn Ukraine loan",
     "Leaders divide on the 2028-34 budget (~€1.58tn) and a €45bn loan for Kyiv.",
     "Ukraine's funding hangs on unity.", "EU COUNCIL · AP", "CONFIRMED", "eu", "EUROPE"),
    ("SEOUL · MARKETS", "Bank of Korea hikes rate to 3.25%, lifts growth view",
     "A 25bp rise; the 2026 GDP forecast is raised to 3.9%.",
     "Seoul tightens on chip-led growth.", "BOK · REUTERS", "OFFICIAL", "chart", "E. ASIA"),
]

PANELS = [
    ("KUWAIT CITY · M. EAST", "Drone strike kills two Italian technicians",
     "Italy and Kuwait blame Iran; Tehran denies it.", "REUTERS · AP", "REPORTED", "drone", "M. EAST"),
    ("KYIV · WAR", "Russia fires 112 drones at Ukraine overnight",
     "Kyiv and Kharkiv hit; power cut across six regions.", "AP · REUTERS", "CONFIRMED", "skyline", "EUROPE"),
    ("GAZA CITY · WAR", "Israeli strikes kill 10 in Gaza",
     "Hamas official Khaled Abu Nada among the dead.", "AP", "REPORTED", "smoke", "M. EAST"),
    ("MUMBAI · INDIA", "India marks 18 years since 26/11 attacks",
     "Tributes nationwide; also the 77th Constitution Day.", "PTI", "CONFIRMED", "candles", "S. ASIA"),
    ("GENEVA · CHESS", "Gukesh–Sindarov Game 3 ends drawn",
     "60 moves; the world title match is level 1.5–1.5.", "FIDE", "ONGOING", "chess", "EUROPE"),
    ("BANGKOK · ENERGY", "Refinery blast injures nine workers",
     "Explosion and fire at the Bangchak plant.", "AL JAZEERA", "REPORTED", "refinery", "SE ASIA"),
    ("KINSHASA · HEALTH", "DR Congo Ebola cases pass 12,000",
     "Responders evacuated amid fighting.", "WHO · UN", "OFFICIAL", "virus", "AFRICA"),
    ("MADRID · EUROPE", "De Cos picked to succeed Lagarde at ECB",
     "Spain's Pablo Hernández de Cos chosen as next president.", "EURONEWS", "REPORTED", "bank", "EUROPE"),
    ("PYONGYANG · ASIA", "Kim vows more nuclear weapons",
     "North Korea says it will expand its arsenal.", "KCNA", "CLAIM", "rocket", "E. ASIA"),
    ("BISSAU · AFRICA", "Guinea-Bissau junta delays elections to 2028",
     "The military rulers push the vote back two years.", "AP", "REPORTED", "ballot", "AFRICA"),
]

# (place, text, source, region) — one-line briefs, all first reported 26 Nov 2026
BRIEFS = [
    ("IBIZA", "Tanker capsizes, 1 dead", "AP", "EUROPE"),
    ("PARIS", "Depardieu ordered to stand trial", "AFP", "EUROPE"),
    ("LONDON", "Net migration falls to 77,000", "ONS", "EUROPE"),
    ("BLUE NILE", "Sudan drones kill 15+", "Reuters", "AFRICA"),
    ("KYIV", "250 fallen recovered in swap", "ICRC", "EUROPE"),
    ("CANBERRA", "Capex +12.2% on AI data", "ABS", "OCEANIA"),
    ("SYDNEY", "Virgin staff strike at 4 airports", "ABC", "OCEANIA"),
    ("BOGOR", "Flooded gold mine: 13 dead", "AP", "SE ASIA"),
    ("NEW YORK", "Storms cancel 1k+ flights", "NBC", "N. AMERICA"),
    ("MOSCOW", "Leak: war dead ~500,000", "BBC", "EUROPE"),
    ("RIYADH", "Houthi missiles stopped", "Reuters", "M. EAST"),
    ("BEIJING", "Unveils 6G roadmap", "Global Times", "E. ASIA"),
    ("PYONGYANG", "Swiss envoy out", "Yonhap", "E. ASIA"),
    ("DOHA", "Sri Lanka A beat India A", "Cricinfo", "S. ASIA"),
    ("NEW YORK", "Nvidia pauses sales", "Dow Jones", "N. AMERICA"),
    ("LONDON", "Babcock $11.4bn subs", "Dow Jones", "EUROPE"),
    ("LONDON", "BoE eyes capital cut", "Dow Jones", "EUROPE"),
    ("WASHINGTON", "ABC review halted", "Dow Jones", "N. AMERICA"),
    ("WASHINGTON", "GAO: stockpiles lag", "GAO", "N. AMERICA"),
    ("WASHINGTON", "FinCEN breach", "Treasury", "N. AMERICA"),
    ("LONDON", "US pulls bombers from UK", "Officials", "EUROPE"),
    ("ZURICH", "First AI-agent cyberattacks", "NCSC", "EUROPE"),
    ("LONDON", "Mandelson files row", "Guardian", "EUROPE"),
    ("MADRID", "FIU may freeze crypto", "Decrypt", "EUROPE"),
    ("ERBIL", "Protests at Baghdad oil plan", "DW", "M. EAST"),
    ("CALIFORNIA", "Tides, 9m waves", "Guardian", "N. AMERICA"),
    ("WASHINGTON", "Trump: pullback", "Guardian", "N. AMERICA"),
    ("MOSCOW", "Kremlin: war widens", "The Hindu", "EUROPE"),
    ("GENEVA", "Longest stretch >2°C", "Copernicus", "WORLD"),
    ("BELGRADE", "Serbia skips EU summit", "NRB", "EUROPE"),
    ("HONG KONG", "Always-on bonds", "NRB", "E. ASIA"),
    ("MUNICH", "Sentiment rises to 90.6", "Ifo", "EUROPE"),
    ("WARSAW", "Poland blames Russia", "NRB", "EUROPE"),
    ("NEW YORK", "Altria eyes Imperial", "Dow Jones", "N. AMERICA"),
    ("MILAN", "UniCredit seeks chair", "Dow Jones", "EUROPE"),
]

NUMBERS = [
    ("100th", "Macy's parade postponed"),
    ("€45bn", "Ukraine loan at stake"),
    ("3.25%", "Bank of Korea base rate"),
    ("112", "drones fired at Ukraine"),
    ("12,000+", "Ebola cases, DR Congo"),
    ("77,000", "UK net migration"),
]

TIMELINE = [
    ("00:00", "Thanksgiving (US)"),
    ("01:30", "Korea hikes rate"),
    ("06:00", "Delhi: Constitution Day"),
    ("09:00", "EU leaders in Brussels"),
    ("13:30", "Parade due to start"),
    ("14:00", "Chess G3, Geneva"),
    ("23:00", "48 stories filed"),
]

EXCLUDED = [
    "US tariff plan on 14 economies — 25 Nov",
    "Netanyahu bribery-charge suggestion — 25 Nov",
    "Cairo fuel-tanker fire, 31 dead — 25 Nov",
    "Malaysia sues Google over YouTube — 25 Nov",
    "Ras Tanura refinery strike — 25 Nov",
    "SpaceX 1m-satellite approval — 25 Nov",
    "Tempus $600m cash election — 24 Nov",
    "Cartagena supermarket siege — 24-25 Nov",
    "Suryavanshi 204 off 53 balls — 24 Nov",
    "Real Madrid 5-1 PSV — 24 Nov",
    "Gulf of Mexico plane crash — 24 Nov",
    "COP31 ends without deal — 22 Nov",
    "Swiss tourist killed by elephants — 19 Nov",
    "ICJ Rohingya ruling — 19 Nov",
]

BADGE_COLORS = {
    "OFFICIAL": (28, 122, 54),
    "CONFIRMED": (16, 34, 74),
    "REPORTED": (154, 92, 16),
    "CLAIM": (178, 32, 40),
    "ONGOING": (110, 52, 140),
}


# ---------------------------------------------------------------- helpers
def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def badge(draw, x, y, label):
    f = F(SANS_B, 10)
    tw = draw.textlength(label, font=f)
    c = BADGE_COLORS[label]
    draw.rounded_rectangle([x, y, x + tw + 12, y + 16], radius=3, fill=c)
    draw.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return tw + 12


def num_chip(draw, cx, cy, n):
    r = 11
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f = F(DEJA_B, 12)
    t = str(n)
    tw = draw.textlength(t, font=f)
    draw.text((cx - tw / 2, cy - 8), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- scenes
def scene_balloon(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(58, 74, 110))
    for i in range(9):  # rain streaks
        rx = x0 + 14 + i * ((x1 - x0 - 28) // 8)
        d.line([(rx, y0 + 8), (rx - 7, y0 + 30)], fill=(170, 190, 220), width=2)
    cx, cy = (x0 + x1) // 2, y0 + 52
    d.ellipse([cx - 52, cy - 26, cx + 52, cy + 26], fill=(240, 236, 224))
    d.ellipse([cx - 26, cy - 9, cx - 8, cy + 5], fill=INK)
    d.ellipse([cx + 8, cy - 9, cx + 26, cy + 5], fill=INK)
    d.arc([cx - 14, cy + 4, cx + 14, cy + 20], 200, 340, fill=INK, width=3)
    d.line([(cx - 30, cy + 22), (cx - 12, y1 - 8)], fill=(210, 210, 210), width=2)
    d.line([(cx + 30, cy + 22), (cx + 12, y1 - 8)], fill=(210, 210, 210), width=2)
    d.rectangle([cx - 16, y1 - 10, cx + 16, y1 - 2], fill=(120, 84, 48))
    f = F(DEJA_B, 13)
    d.ellipse([x1 - 46, y1 - 34, x1 - 10, y1 - 2], fill=(240, 180, 40))
    d.text((x1 - 42, y1 - 26), "100", font=f, fill=INK)
    d.rectangle([x0, y1 - 16, x0 + 150, y1], fill=RED)
    d.text((x0 + 6, y1 - 13), "POSTPONED TO SATURDAY", font=F(SANS_B, 10), fill=(255, 255, 255))


def scene_eu(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(22, 44, 120))
    cx, cy, r = x0 + 78, (y0 + y1) // 2, 30
    import math
    for k in range(12):
        a = k * math.pi / 6
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        d.regular_polygon((sx, sy, 6), 5, fill=(250, 205, 40))
    d.text((cx - 11, cy - 20), "€", font=F(DEJA_B, 34), fill=(250, 205, 40))
    d.rectangle([x0 + 150, y0 + 18, x1 - 14, y0 + 62], fill=(196, 40, 48))
    d.text((x0 + 162, y0 + 26), "€45bn LOAN", font=F(DEJA_B, 20), fill=(255, 255, 255))
    d.text((x0 + 162, y0 + 68), "SUMMIT SPLIT", font=F(SANS_B, 11), fill=(255, 255, 255))


def scene_chart(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(250, 246, 236), outline=RULE)
    d.text((x0 + 34, y0 + 6), "KRW", font=F(DEJA_B, 20), fill=INK)
    pts = []
    n = 9
    for i in range(n):
        px = x0 + 16 + i * ((x1 - x0 - 150) // (n - 1))
        py = y1 - 16 - int(i * i * 0.55 + i * 4)
        pts.append((px, py))
    d.line(pts, fill=RED, width=3)
    for p in pts:
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=RED)
    d.text((x1 - 128, y0 + 18), "3.25%", font=F(DEJA_B, 30), fill=RED)
    d.text((x1 - 126, y0 + 54), "BASE RATE +25bp", font=F(SANS_B, 10), fill=GREY)


def scene_drone(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(30, 34, 52))
    cx, cy = (x0 + x1) // 2, y0 + 26
    d.rectangle([cx - 18, cy - 5, cx + 18, cy + 5], fill=(200, 205, 215))
    for dx, dy in [(-26, -12), (26, -12), (-26, 12), (26, 12)]:
        d.line([(cx + dx, cy + dy), (cx, cy)], fill=(200, 205, 215), width=3)
        d.ellipse([cx + dx - 8, cy + dy - 3, cx + dx + 8, cy + dy + 3], fill=(150, 158, 175))
    d.polygon([(cx - 8, y1), (cx, y0 + 44), (cx + 8, y1)], fill=(245, 140, 40))
    d.polygon([(cx - 20, y1), (cx, y1 - 22), (cx + 20, y1)], fill=(220, 70, 30))


def scene_skyline(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(36, 40, 58))
    for i, hgt in enumerate([34, 48, 28, 54, 40, 30]):
        bx = x0 + 8 + i * ((x1 - x0 - 16) // 6)
        d.rectangle([bx, y1 - hgt, bx + 22, y1], fill=(16, 18, 28))
    for i in range(7):
        px = x0 + 16 + i * ((x1 - x0 - 32) // 6)
        py = y0 + 10 + (i % 3) * 7
        d.polygon([(px, py), (px + 12, py + 4), (px, py + 8)], fill=(220, 70, 30))
    d.text((x0 + 32, y0 + 4), "112 DRONES", font=F(SANS_B, 10), fill=(255, 255, 255))


def scene_smoke(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(52, 48, 44))
    for i in range(5):
        cx = x0 + 24 + i * ((x1 - x0 - 48) // 4)
        d.ellipse([cx - 16, y0 + 6, cx + 16, y0 + 40], fill=(120, 116, 110))
        d.polygon([(cx - 10, y1), (cx, y1 - 26), (cx + 10, y1)], fill=(235, 120, 40))


def scene_candles(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(40, 28, 30))
    d.text((x0 + 32, y0 + 6), "18 YEARS", font=F(SANS_B, 11), fill=(245, 200, 90))
    for i in range(6):
        cx = x0 + 22 + i * ((x1 - x0 - 44) // 5)
        d.rectangle([cx - 5, y1 - 26, cx + 5, y1 - 4], fill=(240, 232, 210))
        d.ellipse([cx - 4, y1 - 38, cx + 4, y1 - 26], fill=(250, 180, 60))


def scene_chess(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(30, 66, 44))
    s = 11
    bx, by = x0 + 12, y0 + 5
    for r in range(4):
        for c in range(4):
            col = (238, 230, 205) if (r + c) % 2 == 0 else (52, 92, 62)
            d.rectangle([bx + c * s, by + r * s, bx + (c + 1) * s, by + (r + 1) * s], fill=col)
    d.text((bx + 4 * s + 12, y0 + 12), "1.5 – 1.5", font=F(DEJA_B, 20), fill=(255, 255, 255))
    d.text((bx + 4 * s + 13, y0 + 40), "GAME 3 · GENEVA", font=F(SANS_B, 9), fill=(200, 230, 205))


def scene_refinery(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(44, 50, 66))
    for i, hgt in enumerate([52, 38, 60]):
        bx = x0 + 16 + i * 34
        d.rectangle([bx, y1 - hgt, bx + 16, y1], fill=(150, 158, 175))
        d.ellipse([bx - 4, y1 - hgt - 12, bx + 20, y1 - hgt], fill=(110, 118, 135))
    d.polygon([(x1 - 44, y1), (x1 - 30, y1 - 34), (x1 - 16, y1)], fill=(245, 140, 40))
    d.polygon([(x1 - 38, y1), (x1 - 30, y1 - 20), (x1 - 22, y1)], fill=(220, 70, 30))


def scene_virus(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(250, 246, 236), outline=RULE)
    import math
    for (cx, cy, r) in [(x0 + 34, y0 + 24, 14), (x0 + 82, y0 + 36, 10), (x1 - 36, y0 + 20, 12),
                        (x1 - 70, y0 + 16, 9), (x0 + 58, y1 - 18, 8)]:
        for k in range(8):
            a = k * math.pi / 4
            d.line([(cx, cy), (cx + (r + 6) * math.cos(a), cy + (r + 6) * math.sin(a))],
                   fill=(178, 32, 40), width=2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 32, 40))
    d.text((x0 + 84, y1 - 15), "12,000+ CASES", font=F(SANS_B, 10), fill=RED)


def scene_bank(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(22, 44, 120))
    d.text((x0 + 12, y0 + 8), "€", font=F(DEJA_B, 30), fill=(250, 205, 40))
    for i in range(4):
        bx = x0 + 58 + i * 26
        d.rectangle([bx, y0 + 26, bx + 12, y1 - 12], fill=(240, 236, 224))
    d.rectangle([x0 + 52, y0 + 18, x0 + 162, y0 + 26], fill=(240, 236, 224))
    d.rectangle([x0 + 52, y1 - 12, x0 + 162, y1 - 6], fill=(240, 236, 224))
    d.text((x1 - 118, y1 - 15), "NEXT ECB CHIEF", font=F(SANS_B, 10), fill=(255, 255, 255))


def scene_rocket(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(24, 26, 44))
    cx = (x0 + x1) // 2
    h = y1 - y0
    nose = y0 + max(4, h // 8)
    waist = y0 + h // 2
    d.polygon([(cx, nose), (cx - 11, waist), (cx + 11, waist)], fill=(225, 228, 235))
    d.rectangle([cx - 11, waist, cx + 11, y1 - 14], fill=(225, 228, 235))
    d.polygon([(cx - 11, y1 - 14), (cx - 22, y1 - 3), (cx - 11, y1 - 3)], fill=(200, 60, 60))
    d.polygon([(cx + 11, y1 - 14), (cx + 22, y1 - 3), (cx + 11, y1 - 3)], fill=(200, 60, 60))
    d.polygon([(cx - 7, y1 - 3), (cx, y1 + 1), (cx + 7, y1 - 3)], fill=(245, 160, 50))
    d.ellipse([cx - 5, waist + 3, cx + 5, waist + 12], fill=(22, 44, 120))


def scene_ballot(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(250, 246, 236), outline=RULE)
    d.rectangle([x0 + 16, y0 + 22, x0 + 84, y1 - 8], fill=(120, 84, 48))
    d.rectangle([x0 + 26, y0 + 30, x0 + 74, y0 + 36], fill=INK)
    d.rectangle([x0 + 38, y0 + 8, x0 + 62, y0 + 32], fill=(255, 255, 255), outline=GREY)
    d.text((x0 + 100, y0 + 16), "2028", font=F(DEJA_B, 26), fill=RED)
    d.line([(x0 + 96, y0 + 50), (x1 - 14, y0 + 50)], fill=RED, width=3)


SCENES = {
    "balloon": scene_balloon, "eu": scene_eu, "chart": scene_chart,
    "drone": scene_drone, "skyline": scene_skyline, "smoke": scene_smoke,
    "candles": scene_candles, "chess": scene_chess, "refinery": scene_refinery,
    "virus": scene_virus, "bank": scene_bank, "rocket": scene_rocket,
    "ballot": scene_ballot,
}


# ---------------------------------------------------------------- panels
def panel(d, box, n, kicker, headline, summary, why, source, badge_label, scene, big=False):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(255, 255, 255), outline=RULE, width=1)
    sh = 80 if big else 50
    SCENES[scene](d, (x0 + 1, y0 + 1, x1 - 1, y0 + sh))
    num_chip(d, x0 + 15, y0 + 15, n)
    ty = y0 + sh + 4
    d.text((x0 + 8, ty), kicker, font=F(SANS_B, 10), fill=RED)
    ty += 13
    hf = F(SERIF_B, 17 if big else 14)
    for line in wrap(d, headline, hf, x1 - x0 - 14)[:2]:
        d.text((x0 + 8, ty), line, font=hf, fill=INK)
        ty += 20 if big else 16
    sf = F(SANS, 11 if big else 10)
    for line in wrap(d, summary, sf, x1 - x0 - 14)[:2]:
        d.text((x0 + 8, ty), line, font=sf, fill=(52, 52, 60))
        ty += 13
    if why:
        for line in wrap(d, "WHY IT MATTERS: " + why, F(SANS_I, 10), x1 - x0 - 14)[:1]:
            d.text((x0 + 8, ty), line, font=F(SANS_I, 10), fill=(80, 80, 90))
            ty += 13
    d.text((x0 + 8, y1 - 15), "SOURCE: " + source, font=F(SANS, 9), fill=GREY)
    bw = d.textlength(badge_label, font=F(SANS_B, 10)) + 12
    badge(d, x1 - bw - 6, y1 - 20, badge_label)


# ---------------------------------------------------------------- map
# crude continent blobs in a 300x150 box, pins at (lon, lat)-ish positions
CONTINENTS = [
    [(8, 30), (46, 18), (78, 26), (84, 48), (66, 66), (50, 62), (40, 84), (30, 70), (16, 54)],
    [(52, 84), (66, 78), (76, 96), (68, 124), (58, 118), (52, 100)],
    [(138, 30), (158, 22), (172, 30), (168, 46), (152, 50), (142, 44)],
    [(146, 56), (172, 52), (186, 74), (176, 104), (160, 100), (150, 78)],
    [(178, 24), (232, 16), (268, 30), (260, 56), (236, 74), (214, 66), (196, 78), (184, 52)],
    [(238, 96), (268, 92), (278, 110), (258, 122), (240, 112)],
]
PINS = {  # story number -> (x, y) inside map box
    1: (64, 44), 2: (152, 32), 3: (252, 40), 4: (184, 48), 5: (166, 30),
    6: (178, 44), 7: (222, 58), 8: (148, 38), 9: (238, 70), 10: (162, 84),
    11: (144, 40), 12: (248, 36), 13: (140, 74),
}


def world_map(d, box):
    x0, y0, x1, y1 = box
    d.text((x0, y0), "WHERE IT HAPPENED — PINS 1-13", font=F(SANS_B, 10), fill=INK)
    my = y0 + 16
    sc = (x1 - x0) / 300.0
    for poly in CONTINENTS:
        pts = [(x0 + px * sc, my + py) for px, py in poly]
        d.polygon(pts, fill=(196, 200, 172), outline=(150, 152, 130))
    for n, (px, py) in PINS.items():
        cx, cy = x0 + px * sc, my + py
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
        f = F(DEJA_B, 9)
        t = str(n)
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 6), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- compose
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 16  # margin
    total_stories = len(LEADS) + len(PANELS) + len(BRIEFS)
    regions = {}
    sources = set()
    for s in LEADS:
        regions[s[7]] = regions.get(s[7], 0) + 1
        sources.add(s[4])
    for s in PANELS:
        regions[s[6]] = regions.get(s[6], 0) + 1
        sources.add(s[3])
    for s in BRIEFS:
        regions[s[3]] = regions.get(s[3], 0) + 1
        sources.add(s[2])

    # top strip
    d.rectangle([0, 0, W, 24], fill=NAVY)
    d.text((M, 5), "THE WORLD IN ONE DAY", font=F(SANS_B, 13), fill=(255, 255, 255))
    strip = (f"{total_stories} STORIES · {len(regions)} REGIONS · {len(sources)} SOURCES · "
             f"14 FIELDS · EVERY ONE FIRST REPORTED THU 26 NOV 2026")
    d.text((W - M - d.textlength(strip, font=F(SANS_B, 11)), 6), strip,
           font=F(SANS_B, 11), fill=(255, 255, 255))

    # masthead
    mast = "Thursday 26 November 2026"
    mf = F(SERIF_B, 58)
    d.text(((W - d.textlength(mast, font=mf)) / 2, 28), mast, font=mf, fill=INK)
    stand = ("A nor'easter grounds New York's 100th Thanksgiving parade, EU leaders split over "
             "Ukraine's €45bn loan, and Seoul raises rates as growth beats forecasts.")
    d.text(((W - d.textlength(stand, font=F(SERIF, 15))) / 2, 94), stand,
           font=F(SERIF, 15), fill=(60, 60, 68))

    # numbers strip
    ny = 118
    nw = (W - 2 * M) // 6
    for i, (big, small) in enumerate(NUMBERS):
        bx = M + i * nw
        d.rectangle([bx + 2, ny, bx + nw - 2, ny + 50], outline=RULE, fill=CREAM)
        d.text((bx + 10, ny + 5), big, font=F(DEJA_B, 23), fill=RED)
        d.text((bx + 10, ny + 34), small, font=F(SANS, 10), fill=GREY)

    # region chips
    cy = ny + 58
    chip_colors = [(16, 34, 74), (178, 32, 40), (28, 122, 54), (154, 92, 16),
                   (110, 52, 140), (16, 110, 120), (120, 60, 30), (60, 90, 160), (90, 90, 90)]
    items = sorted(regions.items(), key=lambda kv: -kv[1])
    cw = (W - 2 * M) // len(items)
    for i, (name, cnt) in enumerate(items):
        bx = M + i * cw
        d.rectangle([bx + 1, cy, bx + cw - 1, cy + 19], fill=chip_colors[i % len(chip_colors)])
        t = f"{name} {cnt}"
        d.text((bx + (cw - d.textlength(t, font=F(SANS_B, 10))) / 2, cy + 4), t,
               font=F(SANS_B, 10), fill=(255, 255, 255))

    # timeline
    ty = cy + 25
    d.rectangle([M, ty, W - M, ty + 19], fill=(238, 232, 216))
    d.text((M + 6, ty + 4), "THE DAY IN UTC", font=F(SANS_B, 11), fill=RED)
    tx = M + 118
    for t, what in TIMELINE:
        seg = f"{t} {what}"
        d.text((tx, ty + 4), seg, font=F(SANS, 10), fill=INK)
        tx += d.textlength(seg, font=F(SANS, 10)) + 10

    # leads
    ly = ty + 25
    lw = (W - 2 * M - 12) // 3
    for i, s in enumerate(LEADS):
        bx = M + i * (lw + 6)
        panel(d, (bx, ly, bx + lw, ly + 192), i + 1, s[0], s[1], s[2], s[3], s[4], s[5], s[6], big=True)

    # panel rows
    py = ly + 198
    pw = (W - 2 * M - 24) // 5
    for row in range(2):
        for col in range(5):
            s = PANELS[row * 5 + col]
            bx = M + col * (pw + 6)
            panel(d, (bx, py, bx + pw, py + 146), 4 + row * 5 + col,
                  s[0], s[1], s[2], None, s[3], s[4], s[5])
        py += 152

    # map + briefs
    by = py + 2
    world_map(d, (M, by, M + 270, by + 190))
    bx0 = M + 282
    d.text((bx0, by), f"ALSO ON THURSDAY 26 NOVEMBER — {len(BRIEFS)} MORE STORIES",
           font=F(SANS_B, 12), fill=INK)
    cols = 3
    per = (len(BRIEFS) + cols - 1) // cols
    colw = (W - M - bx0) // cols
    bf = F(SANS, 9.25)
    for i, (place, text, src, _reg) in enumerate(BRIEFS):
        c, r = divmod(i, per)
        x = bx0 + c * colw
        y = by + 20 + r * 13.5
        line = f"{14 + i}. {place} — {text} — {src}"
        while d.textlength(line, font=bf) > colw - 6 and len(line) > 20:
            line = line[:-2]
        d.text((x, y), line, font=bf, fill=(40, 40, 48))

    # date check footer
    dy = by + 178
    d.rectangle([M, dy, W - M, dy + 74], outline=RED, width=2, fill=(252, 244, 238))
    d.text((M + 8, dy + 4), "DATE CHECK — THESE ARE NOT 26 NOVEMBER, SO THEY ARE LEFT OUT",
           font=F(SANS_B, 11), fill=RED)
    per_col = (len(EXCLUDED) + 2) // 3
    for i, e in enumerate(EXCLUDED):
        c, r = divmod(i, per_col)
        x = M + 10 + c * ((W - 2 * M) // 3)
        d.text((x, dy + 20 + r * 11), "× " + e, font=F(SANS, 9), fill=(90, 40, 40))

    # legend + colophon
    gy = dy + 80
    d.text((M, gy), "HOW SURE: OFFICIAL = an authority's own word · CONFIRMED = wire or two sources · "
                    "REPORTED = one named outlet · CLAIM = one side's account · ONGOING = still unfolding",
           font=F(SANS, 9.5), fill=GREY)
    d.text((M, gy + 13), "Every story here happened or was first reported on Thursday 26 November 2026. "
                         "Sources are named on each story. Scenes are original drawings, not photographs.",
           font=F(SANS_I, 10), fill=(70, 70, 78))
    foot = f"THE WORLD IN ONE DAY · THU 26 NOV 2026 · {total_stories} STORIES · {len(regions)} REGIONS"
    d.text(((W - d.textlength(foot, font=F(SANS_B, 10))) / 2, gy + 27), foot,
           font=F(SANS_B, 10), fill=NAVY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
