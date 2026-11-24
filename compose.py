#!/usr/bin/env python3
"""THE MERIDIAN POST - NI24 edition renderer (Akun 12, @pesulapcrypto).

Renders Tuesday 24 November 2026 in one image. Build-time only: run with
python3 compose.py [A|B] to produce variant PNGs in the work directory.
The shipped entry is produced by main.py, which only copies entry.png.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
WORK = os.environ.get("NI24_WORK", "/home/hatch/workspace/makefun/ni24-work-akun12")

W, H = 3000, 3760
M = 90
CW = W - 2 * M

IVORY = (247, 241, 227)
CREAM = (255, 253, 246)
INK = (30, 26, 22)
BURG = (107, 31, 42)
BURG_D = (74, 20, 32)
GOLD = (201, 162, 39)
GOLD_L = (232, 205, 120)
MUTED = (110, 98, 88)
NAVY = (34, 48, 74)
TEAL = (31, 92, 90)
CARD_LINE = (196, 178, 150)
RED = (200, 40, 50)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


F_BLACK = lambda s: font("PlayfairDisplay-Black.ttf", s)
F_BOLD = lambda s: font("Archivo-Bold.ttf", s)
F_REG = lambda s: font("Archivo.ttf", s)
F_MONO = lambda s: font("IBMPlexMono-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(draw, x, y, lines, fnt, fill, spacing=6):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def scene_band(draw, box, kind, base, accent):
    """Flat layered scene strip inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=base)
    w, h = x1 - x0, y1 - y0
    if kind == "cop":
        cx, cy = x0 + w * 0.50, y0 + h * 0.42
        r = h * 0.34
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD_L, width=8)
        draw.rectangle([cx - 6, cy - r - 4, cx + 6, cy - r + 26], fill=base)
        for i in range(5):
            fx = x0 + w * (0.08 + i * 0.17)
            draw.rectangle([fx, y0 + h * 0.62, fx + w * 0.10, y0 + h * 0.72], fill=accent)
            draw.rectangle([fx + 4, y0 + h * 0.50, fx + w * 0.10 - 4, y0 + h * 0.62],
                           fill=CREAM)
        draw.rectangle([x0, y0 + h * 0.78, x1, y1], fill=(60, 16, 26))
    elif kind == "sea":
        for i in range(3):
            yy = y0 + h * (0.34 + i * 0.20)
            draw.arc([x0 - 40, yy - 22, x0 + w * 0.55, yy + 22], 0, 180,
                     fill=CREAM, width=6)
            draw.arc([x0 + w * 0.45, yy - 22, x1 + 40, yy + 22], 0, 180,
                     fill=CREAM, width=6)
        draw.polygon([(x0 + w * 0.30, y0 + h * 0.56), (x0 + w * 0.62, y0 + h * 0.56),
                      (x0 + w * 0.58, y0 + h * 0.32), (x0 + w * 0.38, y0 + h * 0.32)],
                     fill=(20, 22, 30))
        draw.rectangle([x0 + w * 0.44, y0 + h * 0.14, x0 + w * 0.46, y0 + h * 0.34],
                       fill=(20, 22, 30))
        draw.polygon([(x0 + w * 0.60, y0 + h * 0.46), (x0 + w * 0.72, y0 + h * 0.60),
                      (x0 + w * 0.60, y0 + h * 0.60)], fill=(60, 16, 26))
        for cx, cy in [(0.16, 0.22), (0.80, 0.16), (0.88, 0.36)]:
            draw.ellipse([x0 + w * cx - 8, y0 + h * cy - 8, x0 + w * cx + 8,
                          y0 + h * cy + 8], fill=GOLD)
    elif kind == "gold":
        for i, bx in enumerate([0.12, 0.34, 0.56]):
            draw.polygon([(x0 + w * bx, y0 + h * 0.80), (x0 + w * bx, y0 + h * 0.56),
                          (x0 + w * (bx + 0.13), y0 + h * 0.42),
                          (x0 + w * (bx + 0.26), y0 + h * 0.56),
                          (x0 + w * (bx + 0.26), y0 + h * 0.80)], fill=GOLD_L)
        draw.line([(x0 + w * 0.08, y0 + h * 0.66), (x0 + w * 0.30, y0 + h * 0.50),
                   (x0 + w * 0.48, y0 + h * 0.56), (x0 + w * 0.90, y0 + h * 0.18)],
                  fill=CREAM, width=8)
        draw.polygon([(x0 + w * 0.86, y0 + h * 0.18), (x0 + w * 0.94, y0 + h * 0.18),
                      (x0 + w * 0.90, y0 + h * 0.10)], fill=CREAM)
    elif kind == "ship":
        draw.polygon([(x0 + w * 0.18, y0 + h * 0.62), (x0 + w * 0.80, y0 + h * 0.62),
                      (x0 + w * 0.72, y0 + h * 0.82), (x0 + w * 0.26, y0 + h * 0.82)],
                     fill=(20, 22, 30))
        for i in range(3):
            draw.rectangle([x0 + w * (0.30 + i * 0.13), y0 + h * 0.34,
                            x0 + w * (0.38 + i * 0.13), y0 + h * 0.62], fill=(60, 16, 26))
        draw.line([(x0 + w * 0.80, y0 + h * 0.62), (x0 + w * 0.97, y0 + h * 0.70)],
                  fill=GOLD, width=5)
        for i in range(2):
            yy = y0 + h * (0.88 + i * 0.06)
            draw.arc([x0, yy - 12, x1, yy + 12], 0, 180, fill=CREAM, width=4)
    elif kind == "city":
        for i, bh in enumerate([0.42, 0.62, 0.50, 0.72, 0.55, 0.66, 0.46]):
            bx = x0 + w * (0.04 + i * 0.135)
            draw.rectangle([bx, y0 + h * (0.88 - bh), bx + w * 0.105, y0 + h * 0.88],
                           fill=(20, 22, 30))
        for i in range(3):
            cx = x0 + w * (0.22 + i * 0.28)
            draw.ellipse([cx - 10, y0 + h * 0.16, cx + 10, y0 + h * 0.40],
                         fill=(120, 130, 145))
        draw.rectangle([x0, y0 + h * 0.88, x1, y1], fill=(60, 16, 26))
    elif kind == "bank":
        draw.rectangle([x0 + w * 0.30, y0 + h * 0.18, x0 + w * 0.70, y0 + h * 0.30],
                       fill=CREAM)
        draw.polygon([(x0 + w * 0.26, y0 + h * 0.30), (x0 + w * 0.74, y0 + h * 0.30),
                      (x0 + w * 0.70, y0 + h * 0.38), (x0 + w * 0.30, y0 + h * 0.38)],
                     fill=GOLD)
        for i in range(4):
            cx = x0 + w * (0.34 + i * 0.11)
            draw.rectangle([cx - 6, y0 + h * 0.38, cx + 6, y0 + h * 0.74], fill=CREAM)
        draw.ellipse([x0 + w * 0.72, y0 + h * 0.42, x0 + w * 0.94, y0 + h * 0.74],
                     outline=CREAM, width=7)
        draw.line([x0 + w * 0.76, y0 + h * 0.68, x0 + w * 0.90, y0 + h * 0.48],
                  fill=CREAM, width=7)
    elif kind == "cross":
        for i, bh in enumerate([0.50, 0.68, 0.44, 0.60]):
            bx = x0 + w * (0.06 + i * 0.23)
            draw.rectangle([bx, y0 + h * (0.88 - bh), bx + w * 0.16, y0 + h * 0.88],
                           fill=(20, 22, 30))
        draw.rectangle([x0 + w * 0.68, y0 + h * 0.22, x0 + w * 0.76, y0 + h * 0.62],
                       fill=CREAM)
        draw.rectangle([x0 + w * 0.60, y0 + h * 0.36, x0 + w * 0.84, y0 + h * 0.46],
                       fill=CREAM)
    elif kind == "mount":
        draw.polygon([(x0, y0 + h), (x0 + w * 0.30, y0 + h * 0.18),
                      (x0 + w * 0.55, y0 + h)], fill=(20, 22, 30))
        draw.polygon([(x0 + w * 0.38, y0 + h), (x0 + w * 0.68, y0 + h * 0.08),
                      (x0 + w * 0.98, y0 + h)], fill=(60, 16, 26))
        draw.ellipse([x0 + w * 0.62, y0 + h * 0.12, x0 + w * 0.74, y0 + h * 0.30],
                     fill=CREAM)
    elif kind == "coin":
        draw.ellipse([x0 + w * 0.34, y0 + h * 0.10, x0 + w * 0.66, y0 + h * 0.90],
                     fill=GOLD)
        draw.text((x0 + w * 0.44, y0 + h * 0.22), "B", font=F_BLACK(int(h * 0.52)),
                  fill=BURG_D)
    elif kind == "skyline":
        for i, bh in enumerate([0.55, 0.75, 0.62, 0.85, 0.68, 0.78]):
            bx = x0 + w * (0.03 + i * 0.16)
            draw.rectangle([bx, y0 + h * (0.92 - bh), bx + w * 0.12, y0 + h * 0.92],
                           fill=(20, 22, 30))
        draw.ellipse([x0 + w * 0.74, y0 + h * 0.10, x0 + w * 0.92, y0 + h * 0.42],
                     fill=GOLD)
        draw.rectangle([x0, y0 + h * 0.92, x1, y1], fill=(60, 16, 26))
    elif kind == "pitch":
        draw.rectangle([x0, y0 + h * 0.55, x1, y1], fill=TEAL)
        draw.rectangle([x0 + w * 0.10, y0 + h * 0.12, x0 + w * 0.20, y0 + h * 0.55],
                       outline=CREAM, width=5)
        draw.ellipse([x0 + w * 0.52, y0 + h * 0.16, x0 + w * 0.62, y0 + h * 0.38],
                     fill=CREAM)
    elif kind == "chip":
        draw.rectangle([x0 + w * 0.32, y0 + h * 0.16, x0 + w * 0.68, y0 + h * 0.84],
                       fill=(20, 22, 30))
        for i in range(3):
            yy = y0 + h * (0.28 + i * 0.22)
            draw.line([x0 + w * 0.10, yy, x0 + w * 0.32, yy], fill=GOLD, width=6)
            draw.line([x0 + w * 0.68, yy, x0 + w * 0.90, yy], fill=GOLD, width=6)
        draw.line([(x0 + w * 0.40, y0 + h * 0.74), (x0 + w * 0.56, y0 + h * 0.44),
                   (x0 + w * 0.68, y0 + h * 0.50), (x0 + w * 0.88, y0 + h * 0.18)],
                  fill=CREAM, width=8)
        draw.polygon([(x0 + w * 0.84, y0 + h * 0.18), (x0 + w * 0.92, y0 + h * 0.18),
                      (x0 + w * 0.88, y0 + h * 0.08)], fill=CREAM)


# Land grid: (row, x0, x1) on a 100 x 48 equirectangular world map.
# x = (lon+180)/3.6 ; y = (90-lat)/3.125
LAND = [
    (2, 36, 42), (3, 5, 32), (3, 35, 43), (3, 44, 45), (3, 60, 95),
    (4, 4, 33), (4, 36, 43), (4, 52, 57), (4, 58, 96),
    (5, 4, 33), (5, 37, 42), (5, 51, 58), (5, 57, 97),
    (6, 5, 32), (6, 48, 58), (6, 56, 97),
    (7, 6, 32), (7, 47, 59), (7, 55, 98),
    (8, 7, 31), (8, 47, 59), (8, 55, 98),
    (9, 8, 31), (9, 47, 60), (9, 56, 97),
    (10, 9, 30), (10, 48, 60), (10, 57, 97), (10, 95, 96),
    (11, 10, 30), (11, 48, 60), (11, 58, 96), (11, 95, 96),
    (12, 11, 29), (12, 49, 60), (12, 59, 95), (12, 96, 97),
    (13, 12, 29), (13, 50, 60), (13, 60, 94), (13, 96, 97),
    (14, 13, 28), (14, 51, 60), (14, 62, 93),
    (15, 14, 28), (15, 52, 59), (15, 57, 63), (15, 64, 92),
    (16, 15, 30), (16, 53, 58), (16, 57, 63), (16, 66, 91),
    (17, 16, 28), (17, 54, 57), (17, 58, 63), (17, 68, 90),
    (18, 17, 28), (18, 46, 62), (18, 60, 63), (18, 70, 89),
    (19, 18, 28), (19, 46, 63), (19, 60, 64), (19, 69, 74), (19, 72, 86),
    (20, 19, 28), (20, 46, 63), (20, 60, 65), (20, 69, 75), (20, 74, 85),
    (21, 20, 28), (21, 47, 63), (21, 60, 65), (21, 70, 75), (21, 76, 84),
    (22, 21, 28), (22, 47, 63), (22, 61, 65), (22, 70, 74), (22, 78, 84),
    (23, 22, 28), (23, 48, 62), (23, 61, 64), (23, 71, 74), (23, 80, 84),
    (24, 23, 28), (24, 48, 62), (24, 62, 64), (24, 71, 73), (24, 76, 80), (24, 81, 84),
    (25, 24, 28), (25, 49, 61), (25, 72, 73), (25, 76, 81), (25, 82, 84),
    (26, 26, 38), (26, 49, 61), (26, 77, 82), (26, 83, 85),
    (27, 27, 39), (27, 50, 60), (27, 78, 83), (27, 83, 86),
    (28, 27, 40), (28, 50, 60), (28, 79, 84), (28, 85, 92),
    (29, 28, 40), (29, 51, 59), (29, 85, 94),
    (30, 28, 40), (30, 51, 59), (30, 86, 94),
    (31, 29, 39), (31, 52, 58),
    (32, 29, 39), (32, 52, 58), (32, 62, 63), (32, 82, 92),
    (33, 30, 38), (33, 53, 57), (33, 62, 63), (33, 82, 93),
    (34, 30, 38), (34, 53, 57), (34, 62, 63), (34, 83, 93),
    (35, 31, 37), (35, 54, 56), (35, 83, 92),
    (36, 31, 37), (36, 54, 56), (36, 84, 91),
    (37, 32, 36), (37, 54, 55), (37, 85, 90),
    (38, 32, 36), (38, 55, 55), (38, 86, 89),
    (39, 33, 35), (39, 55, 55), (39, 97, 98),
    (40, 33, 35), (40, 55, 54), (40, 97, 98),
    (41, 34, 35), (41, 97, 98),
    (42, 34, 35),
]
# (display number, lon, lat, nudge_x, nudge_y) in grid units
PINS = [
    (1, 30.7, 36.9, -6, -4), (2, 20.1, 32.1, 0, 5), (3, -0.1, 51.5, -5, -4),
    (4, 25.0, 59.8, 4, -4), (5, 30.5, 50.4, 5, 1), (6, -77.0, 38.9, -4, 3),
    (7, 34.5, 31.5, 5, 4), (8, 44.0, 15.0, 6, 2), (9, -74.0, 40.7, 4, -3),
    (10, -118.0, 34.0, 3, 3), (11, 174.8, -41.3, 0, 0), (12, -3.0, 53.4, -6, 1),
    (13, -122.0, 37.4, -5, -3),
]

CARDS = [
    dict(n=1, place="ANTALYA, TÜRKIYE · WORLD · CLIMATE", scene="cop",
         base=BURG, accent=GOLD, size="lead",
         head="COP31 ends with no deal — the first since 2000",
         deck="The Antalya Pact was not adopted; final text dropped every mention of fossil fuels; the EU, UK, Panama and others rejected it. 44 hours overtime, the longest COP ever; talks carry to COP32 in Addis Ababa, Nov 2027.",
         chip="NO DEAL · FIRST SINCE 2000", tag="REPORTED · Times / Guardian · Mon 23 Nov"),
    dict(n=2, place="BENGHAZI, LIBYA · EUROPE · WAR", scene="sea",
         base=NAVY, accent=GOLD, size="mid",
         head="Ukraine sinks Russian warship Merkury off Libya",
         deck="7 sea drones launched; the corvette sank at Benghazi, a Ka-27 destroyed aboard. Zelenskyy: \u2018exemplary operation\u2019.",
         chip="7 SEA DRONES · SUNK", tag="REPORTED · CNN / Times · Mon 23 Nov"),
    dict(n=3, place="NEW YORK · AMERICAS · MARKETS", scene="gold",
         base=BURG_D, accent=GOLD, size="mid",
         head="Gold rebounds 1.5% to $3,588",
         deck="Bullion recovers after its worst week in 8 months. Traders await the US PCE report due 25 Nov; 10-year yield ~4.96%.",
         chip="$3,588 / OZ", tag="REPORTED · Reuters · Mon 23 Nov"),
    dict(n=4, place="GULF OF FINLAND · EUROPE · SEA", scene="ship",
         base=TEAL, accent=GOLD, size="mini",
         head="Sparta II hit by drones, towed clear",
         deck="Hit by 2 drones Saturday; all 16 crew off, towed out Sunday night.",
         chip="16 CREW SAFE", tag="REPORTED · Reuters / Times · 22\u201323 Nov"),
    dict(n=5, place="KYIV REGION · EUROPE · WAR", scene="city",
         base=(60, 16, 26), accent=GOLD, size="mini",
         head="Russian strikes kill 15 near Kyiv",
         deck="11 killed in a Dymer flat block; 5 hurt in Kyiv. Zelenskyy: Putin is \u2018a killer\u2019.",
         chip="KYIV STRIKES · 15 KILLED", tag="REPORTED · Times / AP · Mon 23 Nov"),
    dict(n=6, place="WASHINGTON · MIDDLE EAST · SANCTIONS", scene="bank",
         base=NAVY, accent=GOLD, size="mini",
         head="US sanctions ~30 Iran exchange houses",
         deck="Treasury names ~30 houses + executives in shadow banking. Rubio meets Qatar PM.",
         chip="IRAN SANCTIONS · ~30", tag="REPORTED · AP / Treasury · Mon 23 Nov"),
    dict(n=7, place="GAZA CITY · MIDDLE EAST · CONFLICT", scene="cross",
         base=BURG, accent=GOLD, size="mini",
         head="Israeli strikes kill 3 in Gaza",
         deck="3 killed Monday in separate strikes, incl. a UNRWA employee. Shifa confirms.",
         chip="3 KILLED", tag="REPORTED · AP · Mon 23 Nov"),
    dict(n=8, place="WESTERN YEMEN · MIDDLE EAST · WAR", scene="mount",
         base=TEAL, accent=GOLD, size="mini",
         head="Strike kills 11 in western Yemen",
         deck="Houthis say a Saudi-backed strike killed 11, wounded 19 on Monday.",
         chip="11 KILLED · 19 WOUNDED", tag="REPORTED · AP · Mon 23 Nov"),
    dict(n=9, place="GLOBAL · CRYPTO", scene="coin",
         base=BURG_D, accent=GOLD, size="mini",
         head="Bitcoin steadies near $61,284",
         deck="$61,284 at 12:52 UTC Mon, +1.1% in 24h. Kraken flash crash to ~$17,000 stands.",
         chip="$61,284", tag="REPORTED · CoinPaprika · Mon 23 Nov"),
    dict(n=10, place="LOS ANGELES · AMERICAS · BUSINESS", scene="skyline",
         base=NAVY, accent=GOLD, size="mini",
         head="GTA VI takes $3.8bn on day one",
         deck="Biggest entertainment launch on record \u2014 past every game and film opening.",
         chip="$3.8BN DAY ONE", tag="REPORTED · ActiveInvestorMag · Mon 23 Nov"),
    dict(n=11, place="WELLINGTON · OCEANIA · CRICKET", scene="pitch",
         base=TEAL, accent=GOLD, size="mini",
         head="New Zealand bat out draw with India",
         deck="NZ 239/5: Mitchell 49* (186), Phillips 26* (126). India 720/9d; 2nd Test 27 Nov.",
         chip="DRAW · 239/5", tag="REPORTED · HS / WicketPulse · Mon 23 Nov"),
    dict(n=12, place="LIVERPOOL · EUROPE · FOOTBALL", scene="pitch",
         base=BURG, accent=GOLD, size="mini",
         head="Liverpool 4\u20130 Man Utd in Pochettino debut",
         deck="Yoro off in the 8th minute; United down to 10. United 19th, on 8 points.",
         chip="4\u20130", tag="REPORTED · Mint / NextSportsWeb · Mon 23 Nov"),
    dict(n=13, place="NEW YORK · AMERICAS · MARKETS", scene="chip",
         base=(20, 22, 30), accent=GOLD, size="mini",
         head="Nvidia brings back Jensen Huang as CEO",
         deck="Board reinstates Huang after Trump intervened. Shares +31%; Nasdaq +6%.",
         chip="+31% · HUANG BACK", tag="REPORTED · Reuters · Mon 23 Nov"),
]

BRIEFS = [
    (14, "N. Korea weighs closing Swiss office (KCNA, Tue)"),
    (15, "Asia rallies Tue: MSCI +4.6%, Nikkei +4.5% (Reuters)"),
    (16, "Singapore lifts 2026 forecast after 6.1% Q3 (Reuters)"),
    (17, "Indonesia factory blaze kills 24 (Reuters, 23 Nov)"),
    (18, "CrowdStrike buys Zscaler in $44bn deal (Reuters)"),
    (19, "Congo halts cobalt exports from 30 Nov (Reuters)"),
    (20, "US weighs training Syrian forces (Reuters, 23 Nov)"),
    (21, "Euro zone PMI 51.7, fifth month of growth (Reuters)"),
    (22, "Nepal PM ends Delhi visit; met Modi Mon (IANS)"),
    (23, "Lisbon march over cost of living (JagranJosh)"),
    (24, "UK-EU reset deal \u2018landmark\u2019, says Burnham (BBC)"),
    (25, "India-EU trade pact likely signed 16 Dec (JagranJosh)"),
    (26, "Tata Steel sells pipe business (ObserverVoice)"),
    (27, "Modi opens AI Centre at IIT Patna (ObserverVoice)"),
    (28, "Solana launches solana.ai for AI agents (Gadgets360)"),
    (29, "UN AI weapons talks continue (salonvision)"),
    (30, "Miley Cyrus weds Maxx Morando (BBC, 23 Nov)"),
    (31, "FBI probes hack of crime database (AP, 23 Nov)"),
    (32, "Trump backs card-rate cap (ActiveInvestorMag)"),
    (33, "Democrats 258-173 take the House (BBC)"),
    (34, "Goldman: S&P +18% thru 2027 (ActiveInvestorMag)"),
    (35, "Mets, A.J. Ewing agree $95m, 8-year deal (AP)"),
    (36, "San Francisco AI boom, crash fears grow (BBC)"),
    (37, "Hong Kong CPI up 2.2% y/y in October (HK News TV)"),
]

TIMELINE = [
    ("04:24 WIB TUE", "KCNA: N. Korea weighs closing Swiss office (Reuters)"),
    ("TUE MORNING, ASIA", "Asia rallies: MSCI +4.6%, Nikkei +4.5% (Reuters)"),
    ("13:39 UTC MON", "Hong Kong sets Interpol curbs, 30 Nov\u20133 Dec (HK News TV)"),
    ("MON EVENING", "Zelenskyy announces Merkury sinking (CNN)"),
    ("MON 23 NOV", "Van Hollen challenges Schumer for Senate leader (1 Dec)"),
    ("12:52 UTC MON", "Bitcoin $61,284 (CoinPaprika)"),
]

DATECHECK = [
    "186-drone night over Ukraine, 161 downed \u2014 Fri 21\u2013Sun 22 Nov",
    "Alcaraz beats Zverev 6\u20132, 7\u20136(9\u20137), first ATP Finals title \u2014 Sun 22 Nov",
    "Verstappen wins Las Vegas Grand Prix \u2014 Sun 22 Nov",
    "Wembanyama scores 50, Spurs 114\u201391 Pelicans \u2014 Sun 22 Nov",
    "Hong Kong Election Committee: 856 candidates, 723 seats \u2014 Sun 22 Nov",
    "Huang resigns as Nvidia CEO after affair admission \u2014 Thu 12 Nov",
    "Peru quake itself \u2014 Fri 20 Nov (only the final toll count is newer)",
    "Myanmar ICJ genocide ruling \u2014 Thu 19 Nov",
]

NUMBERS = [
    ("7", "SEA DRONES LAUNCHED"),
    ("NO DEAL", "FIRST SINCE 2000"),
    ("44 H", "COP OVERTIME"),
    ("$3,588", "GOLD 3588 · +1.5%"),
    ("$61,284", "BITCOIN 61284"),
    ("+31%", "NVIDIA"),
]


def draw_card(draw, box, card):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=CREAM, outline=CARD_LINE, width=3)
    size = card["size"]
    if size == "lead":
        pad, bs, scene_h, hf_s, df_s, tf_s, chip_s = 22, 52, 140, 62, 40, 28, 32
    elif size == "mid":
        pad, bs, scene_h, hf_s, df_s, tf_s, chip_s = 18, 46, 120, 54, 38, 27, 30
    else:
        pad, bs, scene_h, hf_s, df_s, tf_s, chip_s = 13, 44, 76, 48, 36, 26, 26
    ix = x0 + pad
    iw = x1 - x0 - 2 * pad
    # number badge + place
    draw.ellipse([ix, y0 + pad, ix + bs, y0 + pad + bs], fill=BURG)
    nf = F_BOLD(bs - 16)
    num = str(card["n"])
    tw = draw.textlength(num, font=nf)
    draw.text((ix + (bs - tw) / 2, y0 + pad + 5), num, font=nf, fill=CREAM)
    pf = F_BOLD(30 if size != "mini" else 26)
    plines = wrap(draw, card["place"], pf, iw - bs - 14)
    text_lines(draw, ix + bs + 14, y0 + pad + 3, plines[:1], pf, BURG, spacing=2)
    # scene band
    sy = y0 + pad + bs + 12
    scene_band(draw, (ix, sy, x1 - pad, sy + scene_h), card["scene"], card["base"], card["accent"])
    cf = F_BOLD(chip_s)
    ctw = draw.textlength(card["chip"], font=cf)
    draw.rectangle([ix, sy + scene_h - 42, ix + ctw + 26, sy + scene_h], fill=GOLD)
    draw.text((ix + 13, sy + scene_h - 38), card["chip"], font=cf, fill=BURG_D)
    # headline
    hy = sy + scene_h + 12
    hf = F_BLACK(hf_s)
    hlines = wrap(draw, card["head"], hf, iw)
    hy = text_lines(draw, ix, hy, hlines[:2], hf, INK, spacing=2)
    # deck
    df = F_REG(df_s)
    dlines = wrap(draw, card["deck"], df, iw)
    max_deck = 2 if size == "lead" else (2 if size == "mid" else 3)
    text_lines(draw, ix, hy + 8, dlines[:max_deck], df, (58, 50, 44), spacing=4)
    # tag
    tf = F_BOLD(tf_s)
    draw.text((ix, y1 - pad - tf_s - 2), card["tag"], font=tf, fill=MUTED)
    return y1


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=NAVY, outline=CARD_LINE, width=3)
    tf = F_BOLD(36)
    draw.text((x0 + 18, y0 + 12), "WHERE IT HAPPENED", font=tf, fill=CREAM)
    inner_x0, inner_y0 = x0 + 18, y0 + 62
    inner_x1, inner_y1 = x1 - 18, y1 - 42
    cell = min((inner_x1 - inner_x0) / 100.0, (inner_y1 - inner_y0) / 48.0)
    map_w, map_h = cell * 100.0, cell * 48.0
    ox = inner_x0 + ((inner_x1 - inner_x0) - map_w) / 2
    oy = inner_y0 + ((inner_y1 - inner_y0) - map_h) / 2
    dot_r = max(2.5, cell * 0.40)
    land = set()
    for (r, a, b) in LAND:
        for xx in range(a, b + 1):
            land.add((xx, r))
    for (xx, r) in land:
        cx, cy = ox + (xx + 0.5) * cell, oy + (r + 0.5) * cell
        draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=GOLD_L)
    pf = F_BOLD(26)
    for (n, lon, lat, dx, dy) in PINS:
        gx = (lon + 180.0) / 360.0 * 100.0 + dx
        gy = (90.0 - lat) / 150.0 * 48.0 + dy
        cx, cy = ox + gx * cell, oy + gy * cell
        draw.ellipse([cx - 19, cy - 19, cx + 19, cy + 19], fill=RED,
                     outline=CREAM, width=3)
        s = str(n)
        tw = draw.textlength(s, font=pf)
        draw.text((cx - tw / 2, cy - 13), s, font=pf, fill=CREAM)
    sf = F_REG(30)
    draw.text((x0 + 18, y1 - 38), "Pins match story numbers.", font=sf, fill=(210, 205, 190))


def render(variant):
    img = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(img)
    y = 0
    d.rectangle([0, 0, W, 64], fill=BURG)
    kf = F_BOLD(40)
    ks = "37 STORIES  ·  7 REGIONS  ·  EVERY ONE FROM TUESDAY 24 NOVEMBER 2026"
    d.text(((W - d.textlength(ks, font=kf)) / 2, 12), ks, font=kf, fill=CREAM)
    y = 64
    if variant == "A":
        d.rectangle([0, y, W, y + 225], fill=BURG_D)
        mf = F_BLACK(180)
        ms = "THE MERIDIAN POST"
        d.text(((W - d.textlength(ms, font=mf)) / 2, y + 16), ms, font=mf, fill=CREAM)
        y += 225
        df_ = F_BLACK(100)
        ds = "Tuesday 24 November 2026"
        d.text(((W - d.textlength(ds, font=df_)) / 2, y + 4), ds, font=df_, fill=BURG)
        y += 118
    else:
        mf = F_BLACK(180)
        ms = "THE MERIDIAN POST"
        d.text(((W - d.textlength(ms, font=mf)) / 2, y + 8), ms, font=mf, fill=INK)
        y += 212
        d.rectangle([M, y, W - M, y + 6], fill=GOLD)
        y += 16
        df_ = F_BLACK(100)
        ds = "Tuesday 24 November 2026"
        d.text(((W - d.textlength(ds, font=df_)) / 2, y), ds, font=df_, fill=BURG)
        y += 116
    dkf = F_REG(46)
    dk = "COP31 collapses with no deal. A Russian warship sinks off Libya. Gold climbs to $3,588."
    d.text(((W - d.textlength(dk, font=dkf)) / 2, y + 2), dk, font=dkf, fill=(90, 40, 48))
    y += 68
    nb_w = (CW - 5 * 16) // 6
    for i, (num, lab) in enumerate(NUMBERS):
        bx = M + i * (nb_w + 16)
        d.rectangle([bx, y, bx + nb_w, y + 132], fill=CREAM, outline=CARD_LINE, width=3)
        nf = F_BLACK(64 if len(num) < 7 else 50)
        d.text((bx + (nb_w - d.textlength(num, font=nf)) / 2, y + 10), num, font=nf, fill=BURG)
        lf = F_BOLD(28)
        d.text((bx + (nb_w - d.textlength(lab, font=lf)) / 2, y + 88), lab, font=lf, fill=INK)
    y += 132 + 14
    d.rectangle([M, y, W - M, y + 62], fill=BURG)
    rf = F_BOLD(36)
    rs = "BY REGION  —  EUROPE 7  ·  MIDDLE EAST 4  ·  AMERICAS 11  ·  ASIA-PACIFIC 9  ·  AFRICA 1  ·  OCEANIA 1  ·  WORLD 4"
    d.text(((W - d.textlength(rs, font=rf)) / 2, y + 12), rs, font=rf, fill=CREAM)
    y += 62 + 16
    lead_h = 460
    draw_card(d, (M, y, W - M, y + lead_h), CARDS[0])
    y += lead_h + 16
    lw = (CW - 18) // 2
    lh = 465
    draw_card(d, (M, y, M + lw, y + lh), CARDS[1])
    draw_card(d, (M + lw + 18, y, W - M, y + lh), CARDS[2])
    y += lh + 16
    minis = CARDS[3:]
    mw_ = (CW - 4 * 18) // 5
    mh_ = 435
    for r in range(2):
        for c in range(5):
            idx = r * 5 + c
            bx = M + c * (mw_ + 18)
            draw_card(d, (bx, y, bx + mw_, y + mh_), minis[idx])
        y += mh_ + 16
    map_h = 420
    map_w = 1250
    draw_map(d, (M, y, M + map_w, y + map_h))
    tx = M + map_w + 18
    d.rectangle([tx, y, W - M, y + map_h], fill=CREAM, outline=CARD_LINE, width=3)
    tf = F_BOLD(36)
    d.text((tx + 22, y + 12), "TUESDAY 24 NOVEMBER \u2014 THE DAY IN TIME", font=tf, fill=BURG)
    d.text((tx + 22, y + 54), "Times as reported; Monday-evening items labelled so.",
           font=F_REG(30), fill=MUTED)
    ty = y + 100
    for (t, ev) in TIMELINE:
        d.text((tx + 22, ty), t, font=F_MONO(28), fill=BURG)
        ef = F_REG(32)
        elines = wrap(d, ev, ef, (W - M) - tx - 22 - 320)
        text_lines(d, tx + 22 + 320, ty - 2, elines[:1], ef, INK, spacing=2)
        ty += 52
    y += map_h + 16
    d.rectangle([M, y, W - M, y + 52], fill=BURG_D)
    af = F_BOLD(38)
    d.text((M + 22, y + 6), "ALSO ON  —  BRIEFS 14\u201337", font=af, fill=CREAM)
    y += 52
    bw = (CW - 2 * 24) // 3
    bf = F_REG(34)
    for i, (n, txt) in enumerate(BRIEFS):
        col, row = i % 3, i // 3
        bx = M + col * (bw + 24)
        by = y + row * 44
        d.text((bx, by), "%d." % n, font=F_BOLD(34), fill=BURG)
        lines = wrap(d, txt, bf, bw - 62)
        d.text((bx + 62, by + 1), lines[0] if lines else "", font=bf, fill=INK)
    y += 8 * 44 + 12
    d.rectangle([M, y, W - M, y + 200], fill=CREAM, outline=RED, width=4)
    d.text((M + 22, y + 8), "DATE CHECK \u2014 NOT TODAY\u2019S NEWS", font=F_BOLD(36), fill=RED)
    dcf = F_REG(32)
    cy = y + 54
    for i in range(0, 8, 2):
        d.text((M + 22, cy), "\u00b7 " + DATECHECK[i], font=dcf, fill=INK)
        d.text((M + CW // 2 + 10, cy), "\u00b7 " + DATECHECK[i + 1], font=dcf, fill=INK)
        cy += 34
    y += 200 + 14
    ff = F_REG(32)
    fl = "Sources: Reuters · AP · CNN · Times · Guardian · BBC · CoinPaprika · Treasury · HK News TV · IANS · JagranJosh · ObserverVoice · Gadgets360 · salonvision."
    d.text((M, y), fl, font=ff, fill=MUTED)
    y += 40
    fl2 = "REPORTED = confirmed by the source named. CLAIM = attributed, not independently confirmed. Pictures and map: original, drawn in code."
    d.text((M, y), fl2, font=ff, fill=MUTED)
    y += 40
    d.text((M, y), "Tonight\u2019s real count: 7 sea drones, at the top of this page.",
           font=F_BOLD(32), fill=BURG)
    y += 40
    print("render cursor end y=%d (canvas H=%d)" % (y, H))
    return img


def save_final(img, out_path, colors=256):
    small = img.resize((1024, 1024), Image.LANCZOS)
    q = small.quantize(colors=colors, method=Image.MEDIANCUT)
    q.save(out_path, optimize=True)
    return os.path.getsize(out_path)


def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    outdir = sys.argv[2] if len(sys.argv) > 2 else WORK
    os.makedirs(outdir, exist_ok=True)
    img = render(variant)
    big_path = os.path.join(outdir, "variant_%s_big.png" % variant)
    img.save(big_path)
    out_path = os.path.join(outdir, "variant_%s.png" % variant)
    size = save_final(img, out_path)
    print("variant %s -> %s (%d bytes)" % (variant, out_path, size))
    small300 = Image.open(out_path).resize((300, 300), Image.LANCZOS)
    small300.save(os.path.join(outdir, "variant_%s_300.png" % variant))
    print("300px preview -> %s" % os.path.join(outdir, "variant_%s_300.png" % variant))


if __name__ == "__main__":
    main()
