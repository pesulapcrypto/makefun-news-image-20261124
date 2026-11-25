#!/usr/bin/env python3
"""THE BULLION POST - NI24 Akun 12 G2 compose (fresh, written for this session).
Layout A classic grid; variant B = alternate lead/grid order + accent swap.
All numbers from ni24-pool.md + ni24-pool-refresh-0700.md only."""
import sys
from PIL import Image, ImageDraw, ImageFont

FD = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)
PF_BLACK = "PlayfairDisplay-Black.ttf"
PF_BOLD = "PlayfairDisplay-Bold.ttf"
PF_IT = "PlayfairDisplay-Italic.ttf"
AR = "Archivo.ttf"
AR_B = "Archivo-Bold.ttf"

W = H = 1024
PAPER = (247, 236, 210)
INK = (43, 29, 16)
BROWN = (74, 48, 20)
DARKBAR = (52, 33, 12)
GOLD = (198, 148, 32)
GOLD_L = (232, 190, 92)
CREAM = (255, 248, 228)
RED = (168, 38, 28)
TEAL = (24, 96, 104)
NAVY = (30, 52, 96)
GREEN = (46, 102, 52)
PURPLE = (96, 52, 120)
GREY = (90, 82, 70)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

# ---------------- DATA ----------------
# card: num, region_bucket, kicker, headline, deck, chip, tag, scene
CARDS = {
 "huang": (20, "AMERICAS", "NEW YORK · AMERICAS · MARKETS",
   "Nvidia brings back Jensen Huang as CEO",
   "Board reinstates Huang Mon 23 Nov after Trump intervened over the weekend; he had resigned 12 Nov. Shares +31% Mon, Nasdaq +6%, S&P 500 +5%, chip index +12%.",
   "+31% NVIDIA", "REPORTED · Reuters", "chip"),
 "gold": (8, "AMERICAS", "AMERICAS · MARKETS",
   "Gold rebounds 1.5% to $3,588 an ounce",
   "Bullion +1.5% Mon after its worst week in 8 months, off a 14-month low. 10-year Treasury yield ~4.96%; traders await the US PCE report due 25 Nov.",
   "GOLD 3588 · $/OZ", "REPORTED · Reuters", "bars"),
 "btc": (9, "WORLD", "GLOBAL · CRYPTO",
   "Bitcoin steadies near $61,284",
   "Bitcoin 61284 dollars Mon 12:52 UTC, +1.1% in 24 h and -4.5% in 7 days. Weekend low ~$55,100; Kraken CAD flash crash hit ~$17,000 Sat, trades stand.",
   "BITCOIN 61284", "REPORTED · CoinPaprika", "coin"),
 "merkury": (1, "EUROPE", "BENGHAZI, LIBYA · EUROPE · WAR",
   "Ukraine sinks Russian warship Merkury off Libya",
   "7 sea drones launched at Benghazi; corvette Merkury sunk, Ka-27 helicopter destroyed, MV Angara hit. Zelenskyy announced it Mon.",
   "7 SEA DRONES", "REPORTED · CNN / AP", "ship"),
 "kyiv": (3, "EUROPE", "KYIV REGION, UKRAINE · EUROPE · WAR",
   "Russian strikes kill at least 15 near Kyiv",
   "Kyiv strikes left 11 killed in a Dymer flat block; a drone hit a 6-floor Kyiv building, 5 injured. Zelenskyy: Putin 'a killer.'",
   "15 KILLED · 11 DYMER", "REPORTED · Times / AP", "flats"),
 "cop31": (4, "WORLD", "ANTALYA, TURKIYE · WORLD · CLIMATE",
   "COP31 ends with no deal - first since 2000",
   "The Antalya Pact was NOT adopted; final text dropped all mention of fossil fuels. 44 h overtime; COP32 in Addis Ababa, Nov 2027.",
   "NO DEAL · 44H OVERTIME", "REPORTED · Reuters", "globe"),
 "gaza": (6, "MIDDLE EAST", "GAZA CITY · MIDDLE EAST · CONFLICT",
   "Israeli strikes kill 3 in Gaza",
   "3 killed Mon in separate strikes, including a UNRWA employee. Shifa Hospital and the agency confirm the Gaza City toll.",
   "3 KILLED · UNRWA", "REPORTED · AP", "skyline"),
 "gta": (10, "AMERICAS", "LOS ANGELES · AMERICAS · BUSINESS",
   "GTA VI takes $3.8bn on day one",
   "GTA VI banked $3.8 bn on day one - biggest entertainment launch on record, past every game launch and film box office.",
   "$3.8BN DAY ONE", "REPORTED · ActiveInvestorMag", "palm"),
 "house": (14, "AMERICAS", "WASHINGTON · AMERICAS · POLITICS",
   "Democrats take both chambers of Congress",
   "Democrats 258-173 in the House, largest majority since 1992, after the NC pickup. Van Hollen challenges Schumer; ballot 1 Dec.",
   "DEMOCRATS 258-173", "REPORTED · BBC", "dome"),
 "wellington": (11, "OCEANIA", "WELLINGTON · OCEANIA · CRICKET",
   "New Zealand bat out a draw with India",
   "Wellington Test DRAWN: NZ 239/5, Mitchell 49* off 186, Phillips 26*. India 720/9d: Rahul 136, Pant 128, Gill 98.",
   "DRAWN · 239/5", "REPORTED · HS / WicketPulse", "cricket"),
 "liverpool": (12, "EUROPE", "LIVERPOOL · EUROPE · FOOTBALL",
   "Liverpool 4-0 Man Utd; Pochettino debut disaster",
   "Yoro sent off in the 8th minute; United played with 10 men. The 4-0 loss leaves United 19th, on 8 points.",
   "4-0 · YORO OFF 8'", "REPORTED · Mint", "pitch"),
 "solana": (16, "WORLD", "GLOBAL · TECH",
   "Solana launches solana.ai for AI agents",
   "Solana opens solana.ai, a platform for autonomous AI agents to transact, manage wallets and buy services.",
   "SOLANA.AI LIVE", "REPORTED · Gadgets360", "nodes"),
 "iran": (5, "MIDDLE EAST", "WASHINGTON · MIDDLE EAST · SANCTIONS",
   "Iran sanctions: US targets ~30 exchange houses",
   "Treasury Mon named ~30 Iran-linked exchange houses and executives, core of a shadow-banking sanctions network.",
   "~30 SANCTIONED", "REPORTED · AP / Treasury", "bank"),
}
LEADS_A = ["huang", "gold", "btc"]
GRID_A = ["merkury", "kyiv", "cop31", "gaza", "gta",
          "house", "wellington", "liverpool", "solana", "iran"]
LEADS_B = ["gold", "huang", "btc"]
GRID_B = ["kyiv", "merkury", "gaza", "cop31", "gta",
          "wellington", "house", "iran", "liverpool", "solana"]

BRIEFS = [
 (14, "EUROPE", "Sparta II towed clear of the Gulf of Finland Sun night: 121 m ship, 2 drone hits, all 16 crew safe (Reuters)"),
 (15, "MIDDLE EAST", "Strike kills 11 in western Yemen, 19 wounded; Houthi officials blame Saudi-backed forces (AP)"),
 (17, "AMERICAS", "FBI probe: Bureau investigates hack of its crime database; Washington State pauses van-dealer checks (AP)"),
 (18, "WORLD", "UN AI weapons: states agree to keep negotiating limits on lethal autonomous weapons systems (salonvision)"),
 (19, "AMERICAS", "Miley Cyrus marries Maxx Morando in California, her team confirms (BBC / Reuters)"),
 (21, "ASIA", "KCNA: North Korea weighs shutting its Swiss diplomatic office in Pyongyang over sanctions row (Reuters)"),
 (22, "AFRICA", "Congo halts cobalt exports from 30 Nov until further notice, tackling oversupply (Reuters)"),
 (23, "ASIA-PACIFIC", "Indonesia: 24 killed in a factory blaze; rescuers search for dozens still missing (Reuters)"),
 (24, "ASIA-PACIFIC", "Hong Kong restricts drones and Wan Chai roads for the Interpol summit, 30 Nov-3 Dec (HK News TV)"),
 (25, "SOUTH ASIA", "Nepal PM Balendra Shah ends Delhi state visit; he met Modi on Monday (IANS)"),
 (26, "SOUTH ASIA", "India considers rice export duties as domestic prices keep rising (Reuters)"),
 (27, "SOUTH ASIA", "Tata Steel sells its pipe business to APL Apollo for Rs 28,000 crore (ObserverVoice)"),
 (28, "SOUTH ASIA", "Modi inaugurates an AI Centre at IIT Patna plus Rs 400 crore of research projects (ObserverVoice)"),
 (29, "EUROPE", "Thousands march in Lisbon over the cost of living (JagranJosh)"),
 (30, "EUROPE", "UK-EU Brexit reset deal: Burnham calls it a 'landmark' in parliament (BBC)"),
 (31, "EUROPE", "Euro zone growth holds steady: PMI 51.7 in November, a fifth straight month of expansion (Reuters)"),
 (32, "ASIA", "KOSPI falls ~3% Monday to a 10-month low as AI shares swing; Taiwan steadies (Reuters)"),
 (33, "AMERICAS", "CrowdStrike snaps up Zscaler in a $44bn deal as cyber threats mount (Reuters)"),
 (35, "AMERICAS", "FORECAST: US PCE inflation report due 25 Nov - the market's next clue on Fed rates"),
 (36, "OCEANIA", "FORECAST: 2nd Test, India vs New Zealand, Christchurch, 27 Nov-1 Dec"),
 (37, "MIDDLE EAST", "US discussing military training for Syrian forces - first such mission since 2024 (Reuters)"),
]
REGION_ORDER = ["EUROPE", "MIDDLE EAST", "AFRICA", "AMERICAS", "ASIA",
                "SOUTH ASIA", "ASIA-PACIFIC", "OCEANIA", "WORLD"]
REGION_COLORS = {"EUROPE": NAVY, "MIDDLE EAST": RED, "AFRICA": (176, 96, 20),
                 "AMERICAS": TEAL, "ASIA": PURPLE, "SOUTH ASIA": (150, 60, 130),
                 "ASIA-PACIFIC": (20, 110, 140), "OCEANIA": GREEN, "WORLD": GREY}
NUMBERS = [("7", "SEA DRONES · MERKURY SUNK"), ("15", "KILLED NEAR KYIV · 11 DYMER"),
           ("$3,588", "GOLD 3588 · +1.5% MON"), ("$61,284", "BITCOIN 61284 · 12:52 UTC"),
           ("+31%", "NVIDIA · HUANG BACK"), ("$3.8bn", "GTA VI · DAY ONE"),
           ("258-173", "HOUSE · DEMOCRATS 258"), ("44 h", "COP31 OVERTIME · NO DEAL")]
TIMELINE = [
 "SUN NIGHT UTC - Sparta II towed clear; COP31 ends no-deal",
 "MON 12:52 UTC - Bitcoin prints $61,284 (CoinPaprika)",
 "MON EVE UTC - Zelenskyy announces Merkury sinking",
 "MON EVE UTC - Treasury announces Iran sanctions",
 "21:24 UTC MON = 04:24 WIB TUE - KCNA on Swiss office",
 "TUE 24 NOV - this edition, Tuesday 24 November 2026",
]
DATECHECK = ("D1 186-drone night over Ukraine (Fri 21-Sun 22 Nov) - D3 Alcaraz first ATP Finals title (Sun 22 Nov) - "
 "D4 Verstappen wins Las Vegas GP (Sun 22 Nov) - D5 Wembanyama 50 pts, Spurs 114-91 (Sun 22 Nov) - "
 "D7 Peru quake itself (Fri 20 Nov) - D10 Myanmar ICJ genocide ruling (Thu 19 Nov) - "
 "D14 Nvidia SEC probe first reported (Fri 20 Nov) - D17 Huang RESIGNS as Nvidia CEO (Thu 12 Nov; his RETURN is today's story). "
 "Tonight's real count: 7 sea drones, at the top of this page.")

# ---------------- SCENES (flat, layered, full-bleed strips) ----------------
def scene(d, kind, x, y, w, h):
    sky = (250, 240, 214)
    d.rectangle([x, y, x + w, y + h], fill=sky)
    cx, cy = x + w // 2, y + h // 2
    if kind == "chip":
        d.rectangle([x, y, x + w, y + h], fill=(38, 60, 44))
        gx, gy, gw, gh = cx - 52, cy - 26, 104, 52
        d.rectangle([gx, gy, gx + gw, gy + gh], fill=GOLD_L, outline=GOLD, width=3)
        d.rectangle([gx + 30, gy + 14, gx + 74, gy + 38], fill=BROWN)
        for i in range(6):
            px = gx - 14 + i * 4
            d.line([gx - 12, gy + 8 + i * 7, gx, gy + 8 + i * 7], fill=GOLD_L, width=2)
            d.line([gx + gw, gy + 8 + i * 7, gx + gw + 12, gy + 8 + i * 7], fill=GOLD_L, width=2)
        for i in range(5):
            d.line([gx + 10 + i * 20, gy + gh, gx + 10 + i * 20, gy + gh + 5], fill=GOLD_L, width=2)
    elif kind == "bars":
        d.rectangle([x, y, x + w, y + h], fill=(66, 44, 18))
        for bx, by, s in [(x + 26, y + h - 30, 1), (x + 96, y + h - 30, 1), (x + 61, y + h - 52, 1), (x + w - 90, y + h - 30, 1)]:
            d.polygon([(bx, by), (bx + 16, by - 14), (bx + 52, by - 14), (bx + 66, by)], fill=GOLD_L, outline=GOLD)
            d.rectangle([bx, by, bx + 66, by + 12], fill=GOLD, outline=(150, 108, 20))
        d.polygon([(x + w - 60, y + 12), (x + w - 44, y + 26), (x + w - 60, y + 40), (x + w - 76, y + 26)], fill=GOLD_L)
    elif kind == "coin":
        d.rectangle([x, y, x + w, y + h], fill=(84, 52, 16))
        for i, (ox, r) in enumerate([(-58, 26), (0, 32), (58, 26)]):
            d.ellipse([cx + ox - r, cy - r, cx + ox + r, cy + r], fill=GOLD_L, outline=GOLD, width=3)
            d.text((cx + ox, cy), "B", font=F(AR_B, r), fill=BROWN, anchor="mm")
    elif kind == "ship":
        d.rectangle([x, y, x + w, y + int(h * 0.55)], fill=(196, 216, 226))
        d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(36, 84, 120))
        for i in range(4):
            d.arc([x + 10 + i * 60, y + int(h * 0.55) + 6, x + 60 + i * 60, y + int(h * 0.55) + 22], 0, 180, fill=(220, 240, 250), width=2)
        hx, hy = cx - 70, y + int(h * 0.40)
        d.polygon([(hx, hy), (hx + 130, hy), (hx + 112, hy + 16), (hx + 16, hy + 16)], fill=(70, 74, 80))
        d.rectangle([hx + 30, hy - 16, hx + 84, hy], fill=(90, 94, 100))
        d.polygon([(hx + 118, hy + 2), (hx + 150, hy + 12), (hx + 118, hy + 14)], fill=RED)
        d.line([hx + 96, hy - 17, hx + 96, hy], fill=INK, width=3)
    elif kind == "flats":
        d.rectangle([x, y, x + w, y + h], fill=(210, 198, 178))
        for i, (bx, bh, dmg) in enumerate([(x + 12, 36, False), (x + 70, 42, True), (x + 128, 32, False)]):
            d.rectangle([bx, y + h - bh - 8, bx + 54, y + h - 8], fill=(150, 128, 96) if not dmg else (96, 84, 70))
            for r_ in range(3):
                for c_ in range(3):
                    wx, wy = bx + 7 + c_ * 15, y + h - bh + 3 + r_ * 11
                    d.rectangle([wx, wy, wx + 9, wy + 7], fill=(240, 220, 150))
            if dmg:
                d.polygon([(bx + 20, y + h - bh - 8), (bx + 44, y + h - bh - 8), (bx + 32, y + h - 30)], fill=(40, 34, 28))
        d.rectangle([x, y + h - 8, x + w, y + h], fill=(110, 96, 74))
    elif kind == "globe":
        d.rectangle([x, y, x + w, y + h], fill=(24, 62, 92))
        d.ellipse([cx - 23, cy - 23, cx + 23, cy + 23], fill=(64, 140, 96), outline=(220, 240, 220), width=2)
        d.ellipse([cx - 23, cy - 23, cx + 23, cy + 23], outline=(220, 240, 220), width=1)
        d.line([cx - 23, cy, cx + 23, cy], fill=(220, 240, 220), width=1)
        d.line([cx, cy - 23, cx, cy + 23], fill=(220, 240, 220), width=1)
        d.polygon([(x + w - 46, y + 10), (x + w - 38, y + 22), (x + w - 54, y + 22)], fill=RED)
        d.rectangle([x + w - 44, y + 22, x + w - 40, y + 52], fill=RED)
    elif kind == "skyline":
        d.rectangle([x, y, x + w, y + h], fill=(226, 205, 180))
        for i, (bx, bh) in enumerate([(x + 6, 36), (x + 52, 44), (x + 98, 32), (x + 142, 42)]):
            d.rectangle([bx, y + h - bh - 6, bx + 46, y + h - 6], fill=(140, 118, 92))
        d.ellipse([x + 104, y + 6, x + 140, y + 28], fill=(120, 110, 100))
        d.ellipse([x + 122, y + 3, x + 164, y + 25], fill=(140, 128, 116))
        d.rectangle([x, y + h - 6, x + w, y + h], fill=(100, 84, 62))
    elif kind == "palm":
        d.rectangle([x, y, x + w, y + h], fill=(250, 214, 130))
        d.ellipse([x + w - 66, y + 8, x + w - 22, y + 52], fill=(244, 160, 40))
        d.line([x + 44, y + h, x + 56, y + 22], fill=BROWN, width=6)
        for a in [(-30, -8), (-12, -20), (8, -22), (28, -12)]:
            d.arc([x + 56 + a[0] - 26, y + 22 + a[1] - 10, x + 56 + a[0] + 26, y + 22 + a[1] + 14], 180, 340, fill=GREEN, width=4)
        d.rectangle([x + 104, y + h - 26, x + 176, y + h - 12], fill=RED)
        d.polygon([(x + 114, y + h - 26), (x + 126, y + h - 36), (x + 156, y + h - 36), (x + 166, y + h - 26)], fill=(120, 26, 20))
        d.ellipse([x + 114, y + h - 16, x + 128, y + h - 4], fill=INK)
        d.ellipse([x + 152, y + h - 16, x + 166, y + h - 4], fill=INK)
    elif kind == "dome":
        d.rectangle([x, y, x + w, y + h], fill=(196, 214, 232))
        d.arc([cx - 46, cy - 22, cx + 46, cy + 26], 180, 360, fill=(240, 244, 248), width=8)
        d.rectangle([cx - 60, cy + 4, cx + 60, cy + 12], fill=(240, 244, 248))
        for i in range(6):
            d.rectangle([cx - 52 + i * 19, cy + 12, cx - 46 + i * 19, cy + 30], fill=(240, 244, 248))
        d.rectangle([cx - 64, cy + 30, cx + 64, cy + 36], fill=(210, 218, 226))
        d.line([cx, cy - 24, cx, cy - 15], fill=INK, width=3)
    elif kind == "cricket":
        d.rectangle([x, y, x + w, y + h], fill=(96, 156, 84))
        d.rectangle([cx - 14, y + 8, cx + 14, y + h - 8], fill=(226, 204, 158))
        for sx in (-8, 0, 8):
            d.line([cx + sx, y + 14, cx + sx, y + 26], fill=(240, 240, 230), width=2)
            d.line([cx + sx, y + h - 26, cx + sx, y + h - 14], fill=(240, 240, 230), width=2)
        d.ellipse([cx + 44, cy - 8, cx + 60, cy + 8], fill=RED)
        d.line([cx - 52, cy + 18, cx - 30, cy - 12], fill=BROWN, width=5)
    elif kind == "pitch":
        d.rectangle([x, y, x + w, y + h], fill=(52, 128, 62))
        d.rectangle([x + 14, y + 10, x + w - 14, y + h - 10], outline=(240, 248, 240), width=2)
        d.line([cx, y + 10, cx, y + h - 10], fill=(240, 248, 240), width=2)
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=(240, 248, 240), width=2)
        d.ellipse([cx + 52, cy - 11, cx + 74, cy + 11], fill=(245, 245, 245), outline=INK, width=2)
    elif kind == "nodes":
        d.rectangle([x, y, x + w, y + h], fill=(30, 34, 74))
        pts = [(x + 34, cy), (cx - 30, cy - 20), (cx + 16, cy + 16), (cx + 62, cy - 18), (x + w - 36, cy + 4), (cx, cy - 21)]
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                d.line([pts[i], pts[j]], fill=(110, 120, 200), width=1)
        for p in pts:
            d.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=GOLD_L, outline=GOLD, width=2)
    elif kind == "bank":
        d.rectangle([x, y, x + w, y + h], fill=(216, 200, 168))
        d.polygon([(cx - 66, cy - 12), (cx + 66, cy - 12), (cx, cy - 24)], fill=BROWN)
        d.rectangle([cx - 66, cy - 11, cx + 66, cy - 5], fill=BROWN)
        for i in range(5):
            d.rectangle([cx - 58 + i * 26, cy - 3, cx - 48 + i * 26, cy + 15], fill=(170, 148, 104))
        d.rectangle([cx - 70, cy + 15, cx + 70, cy + 21], fill=BROWN)
        d.line([cx + 42, cy - 20, cx + 68, cy + 2], fill=RED, width=4)
        d.line([cx + 68, cy - 20, cx + 42, cy + 2], fill=RED, width=4)

# ---------------- CARD ----------------
def card(img, d, key, disp, x, y, w, h, lead=False):
    num, bucket, kick, head, deck, chip, tag, sc = CARDS[key]
    d.rectangle([x, y, x + w, y + h], fill=CREAM, outline=BROWN, width=2)
    sh = 66 if lead else 50
    # scene is rendered on its own layer and pasted: nothing a scene draws
    # can ever escape its strip and paint over a neighbouring card
    layer = Image.new("RGB", (w - 4, sh), PAPER)
    scene(ImageDraw.Draw(layer), sc, 0, 0, w - 4, sh)
    img.paste(layer, (x + 2, y + 2))
    d.rectangle([x, y, x + w, y + h], outline=BROWN, width=2)
    d.rectangle([x + 6, y + 6, x + 34, y + 30], fill=RED)
    d.text((x + 20, y + 18), str(disp), font=F(AR_B, 15), fill=(255, 255, 255), anchor="mm")
    cw = d.textlength(chip, font=F(AR_B, 10))
    d.rectangle([x + w - cw - 16, y + sh - 16, x + w - 6, y + sh - 2], fill=DARKBAR)
    d.text((x + w - cw - 11, y + sh - 9), chip, font=F(AR_B, 10), fill=GOLD_L, anchor="lm")
    ty = y + sh + 5
    d.text((x + 8, ty), kick, font=F(AR_B, 9), fill=REGION_COLORS[bucket])
    ty += 12
    hf = F(AR_B, 15 if lead else 12)
    for ln in wrap(d, head, hf, w - 14)[:2]:
        d.text((x + 8, ty), ln, font=hf, fill=INK)
        ty += (18 if lead else 14.5)
    df = F(AR, 10 if lead else 9)
    for ln in wrap(d, deck, df, w - 14)[:4 if lead else 3]:
        d.text((x + 8, ty), ln, font=df, fill=(70, 56, 36))
        ty += (12 if lead else 10.5)
    d.text((x + 8, y + h - 13), tag, font=F(AR_B, 8.5), fill=GREY)

# ---------------- DOTTED MAP ----------------
LAND = [
"                                                                        ",
"        oooo  oo                                                        ",
"      oooooooooo ooo        oooooooooooooooooooooooooooooo              ",
"     oooooooooooo oo      ooooooooooooooooooooooooooooooooooooo         ",
"      oooooooooo         ooooooooooooooooooooooooooooooooooooooo        ",
"       ooooooo          ooooooooooooooooooooooooooooooooooooooooo       ",
"        ooooo            ooooo ooooooooooooooooooooooooooooooooooo      ",
"         ooo              ooo   ooooooooooooooooooooooooooooooooo       ",
"         oo                    ooooooooooooooooooo oooooooooooo         ",
"          o                     ooooooooooooooooo   ooooooooo           ",
"          oo                     ooooooooooooooo     ooooooo            ",
"           o                      ooooooooooooo       ooooo    oo       ",
"           oo                      oooooooooo          ooo    oooo      ",
"            o                       oooooooo           oo      oo       ",
"            oo                       oooooo            o                ",
"             o                        oooo                              ",
"             oo                        oo                               ",
"              o                                                         ",
"              oo                                                        ",
"               o                                                        ",
]
PINXY = {"huang": (20, 3), "gold": (22, 5), "btc": (34, 7), "merkury": (47, 5),
         "kyiv": (50, 3), "cop31": (52, 4), "gaza": (53, 6), "gta": (13, 4),
         "house": (24, 4), "wellington": (67, 14), "liverpool": (45, 2),
         "solana": (11, 4), "iran": (57, 5)}

def draw_map(d, x, y, w, h, pins):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.text((x + 8, y + 5), "WHERE IT HAPPENED", font=F(AR_B, 11), fill=GOLD_L)
    cols, rows = 72, 20
    cw, ch = (w - 16) / cols, (h - 40) / rows
    for r_, row in enumerate(LAND):
        for c_, ch_ in enumerate(row[:cols]):
            if ch_ == "o":
                px, py = x + 8 + c_ * cw, y + 30 + r_ * ch
                d.ellipse([px, py, px + 3.3, py + 3.3], fill=(214, 226, 240))
    for (gx, gy, label) in pins:
        px, py = x + 8 + gx * cw, y + 30 + gy * ch
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py), label, font=F(AR_B, 8), fill=(255, 255, 255), anchor="mm")
    d.text((x + 8, y + h - 13), "Red pins match story numbers on this page.",
           font=F(AR, 8.5), fill=(214, 226, 240))

# ---------------- PAGE ----------------
def build(variant, out):
    leads = LEADS_A if variant == "A" else LEADS_B
    grid = GRID_A if variant == "A" else GRID_B
    accent = GOLD if variant == "A" else GOLD_L
    counts = {r: 0 for r in REGION_ORDER}
    for k in leads + grid:
        counts[CARDS[k][1]] += 1
    for (_, b, _) in BRIEFS:
        counts[b] += 1
    total = len(leads) + len(grid) + len(BRIEFS)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # kicker
    d.rectangle([0, 0, W, 26], fill=DARKBAR)
    kick = f"{total} STORIES - 9 REGIONS - EVERY ONE DATED TUESDAY 24 NOVEMBER 2026"
    d.text((W // 2, 13), kick, font=F(AR_B, 13), fill=GOLD_L, anchor="mm")
    # masthead
    d.text((W // 2, 62), "THE BULLION POST", font=F(PF_BLACK, 58), fill=BROWN, anchor="mm")
    d.line([16, 96, W - 16, 96], fill=accent, width=3)
    d.rectangle([0, 100, W, 148], fill=GOLD)
    d.text((W // 2, 124), "TUESDAY 24 NOVEMBER 2026", font=F(PF_BLACK, 37), fill=DARKBAR, anchor="mm")
    d.text((W // 2, 162),
           "Huang returns at Nvidia, gold and Bitcoin steady - while war, climate and Congress fill the front page",
           font=F(PF_IT, 14.5), fill=BROWN, anchor="mm")
    # numbers strip
    ny = 176
    d.rectangle([8, ny, W - 8, ny + 44], fill=DARKBAR)
    nw = (W - 16) // 8
    for i, (big, lab) in enumerate(NUMBERS):
        bx = 8 + i * nw
        d.text((bx + nw // 2, ny + 13), big, font=F(AR_B, 19), fill=GOLD_L, anchor="mm")
        for j, ln in enumerate(wrap(d, lab, F(AR_B, 7.5), nw - 6)):
            d.text((bx + nw // 2, ny + 27 + j * 9), ln, font=F(AR_B, 7.5), fill=CREAM, anchor="mm")
        if i:
            d.line([bx, ny + 5, bx, ny + 39], fill=GOLD, width=1)
    # region strip
    ry = 226
    d.rectangle([8, ry, W - 8, ry + 22], fill=CREAM, outline=BROWN, width=1)
    rx = 14
    d.text((rx, ry + 11), "REGIONS:", font=F(AR_B, 10), fill=INK, anchor="lm")
    rx += 62
    for r in REGION_ORDER:
        t = f"{r} {counts[r]}"
        tw = d.textlength(t, font=F(AR_B, 9.5))
        d.rectangle([rx, ry + 4, rx + tw + 10, ry + 18], fill=REGION_COLORS[r])
        d.text((rx + 5, ry + 11), t, font=F(AR_B, 9.5), fill=(255, 255, 255), anchor="lm")
        rx += tw + 15
    # timeline
    ty = 254
    d.rectangle([8, ty, W - 8, ty + 38], fill=(238, 226, 192), outline=BROWN, width=1)
    d.text((14, ty + 6), "THE DAY IN UTC", font=F(AR_B, 9.5), fill=RED)
    tl = "  |  ".join(TIMELINE[:3])
    d.text((14, ty + 18), tl, font=F(AR, 8.2), fill=INK)
    tl2 = "  |  ".join(TIMELINE[3:])
    d.text((14, ty + 29), tl2, font=F(AR, 8.2), fill=INK)
    # date check strip
    cy = 294
    d.rectangle([8, cy, W - 8, cy + 30], fill=(250, 232, 224), outline=RED, width=2)
    d.text((14, cy + 4), "DATE CHECK - NOT TODAY:", font=F(AR_B, 9), fill=RED)
    for j, ln in enumerate(wrap(d, DATECHECK, F(AR, 7.8), W - 170)[:2]):
        d.text((150 if j == 0 else 14, cy + 4 + j * 13), ln, font=F(AR, 7.8), fill=INK)
    # leads
    ly, lh = 332, 168
    lw = (W - 32) // 3
    for i, k in enumerate(leads):
        card(img, d, k, i + 1, 8 + i * (lw + 8), ly, lw, lh, lead=True)
    # grid
    gy, gh = 508, 140
    gw = (W - 48) // 5
    for i, k in enumerate(grid):
        r_, c_ = divmod(i, 5)
        card(img, d, k, 4 + i, 8 + c_ * (gw + 8), gy + r_ * (gh + 8), gw, gh)
    # bottom band
    by = 796
    pins = []
    for i, k in enumerate(leads + grid):
        gx, gy2 = PINXY[k]
        pins.append((gx, gy2, str(i + 1)))
    draw_map(d, 8, by, 336, 168, pins)
    # briefs
    d.rectangle([352, by, W - 8, by + 168], fill=CREAM, outline=BROWN, width=1)
    d.text((360, by + 6), "ALSO ON THE BULLION POST", font=F(AR_B, 11), fill=BROWN)
    per = (len(BRIEFS) + 2) // 3
    for col in range(3):
        bx = 360 + col * 220
        yy = by + 24
        for j, (num, bucket, text) in enumerate(BRIEFS[col * per:(col + 1) * per]):
            disp = 14 + col * per + j
            lines = wrap(d, f"{disp}. {text}", F(AR, 7.8), 212)
            for ln in lines[:2]:
                d.text((bx, yy), ln, font=F(AR, 7.8), fill=INK)
                yy += 9.2
            yy += 1.2
    # footer
    fy = 978
    d.line([8, fy, W - 8, fy], fill=BROWN, width=1)
    d.text((8, fy + 5),
           "Sources: Reuters - AP - BBC - CNN - Times - Treasury - CoinPaprika - Gadgets360 - IANS - HK News TV - salonvision - ObserverVoice - JagranJosh - Mint - HS.",
           font=F(AR, 8.5), fill=GREY)
    d.text((8, fy + 17),
           "REPORTED = reported by the named source for 23-24 Nov 2026. Pictures and map: original, drawn in code.",
           font=F(AR, 8.5), fill=GREY)
    d.text((W - 8, fy + 17), "THE BULLION POST - one day, one page.", font=F(PF_BOLD, 9.5), fill=BROWN, anchor="ra")
    img.save(out, optimize=True)
    return total, counts

if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2]
    total, counts = build(variant, out)
    print("variant", variant, "total stories", total, "regions", counts)
