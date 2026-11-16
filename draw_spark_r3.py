#!/usr/bin/env python3
"""Draw "One Spark" for make.fun ai-excited-01 — round 3, written fresh.

One moment: a giant hand rises out of a sleeping city holding a single
lit match; the flame breaks apart into a river of paper lanterns that
climbs the night sky. Text: "one spark." — bottom left.

Everything is drawn with PIL primitives (no photos, no copied art).
Deterministic: fixed seed, no clock, no network. Two runs must produce
byte-identical PNG output.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
SEED = 20261116
OUT = "entry.png"

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return tuple(int(round(lerp(a, b, t))) for a, b in zip(c1, c2))


def bezier(p0, p1, p2, n=24):
    """Quadratic bezier points from p0 via p1 to p2."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts


def sky():
    """Night gradient: deep indigo up top, dusky violet at the horizon."""
    top = (7, 10, 38)
    mid = (16, 22, 66)
    bot = (38, 34, 86)
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        if t < 0.55:
            c = lerp_color(top, mid, t / 0.55)
        else:
            c = lerp_color(mid, bot, (t - 0.55) / 0.45)
        d.line([(0, y), (W, y)], fill=c + (255,))
    return img


def stars(base, rng):
    """Deterministic starfield, denser and brighter toward the top."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(240):
        x = rng.uniform(0, W)
        y = rng.uniform(0, H * 0.78) ** 0.92
        r = rng.choice([0.6, 0.8, 1.0, 1.2, 1.6, 2.0])
        a = int(rng.uniform(90, 235))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 240, 255, a))
    # a few bright cross sparkles
    for _ in range(10):
        x = rng.uniform(40, W - 40)
        y = rng.uniform(30, H * 0.5)
        s = rng.uniform(4, 9)
        a = int(rng.uniform(160, 230))
        d.line([(x - s, y), (x + s, y)], fill=(255, 255, 255, a), width=1)
        d.line([(x, y - s), (x, y + s)], fill=(255, 255, 255, a), width=1)
    return Image.alpha_composite(base, layer)


def skyline(base, rng):
    """Two layers of sleeping-city silhouettes + sparse warm windows."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    horizon = 1010
    # back layer: dark blue-violet blocks
    x = -10
    while x < W + 10:
        bw = rng.uniform(46, 110)
        bh = rng.uniform(90, 210)
        d.rectangle([x, horizon - bh, x + bw, horizon],
                    fill=(24, 28, 74, 255))
        if rng.random() < 0.4:  # antenna
            ax = x + bw / 2
            d.line([(ax, horizon - bh), (ax, horizon - bh - 26)],
                   fill=(24, 28, 74, 255), width=3)
            d.ellipse([ax - 2, horizon - bh - 30, ax + 2, horizon - bh - 26],
                      fill=(255, 90, 70, 220))
        x += bw + rng.uniform(2, 14)
    # front layer: near-black blocks
    x = -10
    while x < W + 10:
        bw = rng.uniform(60, 130)
        bh = rng.uniform(60, 150)
        d.rectangle([x, horizon - bh, x + bw, horizon],
                    fill=(8, 10, 30, 255))
        x += bw + rng.uniform(4, 18)
    # lit windows, sparse and warm
    for _ in range(90):
        wx = rng.uniform(0, W - 6)
        wy = rng.uniform(830, 995)
        if rng.random() < 0.75:
            d.rectangle([wx, wy, wx + 4, wy + 6],
                        fill=(255, 176, 92, int(rng.uniform(120, 220))))
    return Image.alpha_composite(base, layer)

HAND = (56, 34, 22, 255)
RIM = (255, 154, 60, 200)
MATCH_WOOD = (232, 214, 176, 255)
MATCH_HEAD = (122, 32, 24, 255)
FLAME_OUTER = (255, 106, 0, 235)
FLAME_MID = (255, 166, 43, 255)
FLAME_INNER = (255, 217, 77, 255)
FLAME_CORE = (255, 246, 200, 255)
TEXT_COL = (255, 233, 196, 255)
TEXT_SHADOW = (6, 8, 26, 220)

FLAME_X, FLAME_BASE_Y = 642, 748


def draw_hand(base):
    """Stylised cupped hand silhouette rising from the bottom edge,
    holding the match upright. Fingers are separate capsules with
    gaps of sky between them; the match passes between the index
    finger (behind it) and the thumb (in front of it) so the grip
    reads instead of melting into one blob."""
    d = ImageDraw.Draw(base)
    # palm: broad mass from the bottom edge up to the knuckles
    d.polygon([(470, 1024), (478, 940), (520, 884), (600, 856),
               (720, 852), (800, 884), (846, 950), (852, 1024)], fill=HAND)
    d.ellipse([505, 858, 825, 965], fill=HAND)
    # fingers: four capsules rising from the palm, tips converging
    # on the matchstick, gaps of sky left between them
    fingers = [
        ((556, 884), (588, 828), (604, 792)),
        ((622, 878), (640, 818), (648, 782)),
        ((688, 878), (694, 820), (690, 786)),
        ((748, 884), (742, 830), (730, 800)),
    ]
    for p0, p1, p2 in fingers:
        curve = bezier(p0, p1, p2, 20)
        d.line(curve, fill=HAND, width=40, joint="curve")
        d.ellipse([curve[-1][0] - 20, curve[-1][1] - 20,
                   curve[-1][0] + 20, curve[-1][1] + 20], fill=HAND)
    # match stick (in front of the fingers, behind the thumb)
    d.line([(FLAME_X, 1000), (FLAME_X, 752)], fill=MATCH_WOOD, width=11)
    d.rounded_rectangle([FLAME_X - 9, 724, FLAME_X + 9, 754],
                        radius=8, fill=MATCH_HEAD)
    # thumb: thick arc from the left of the palm, crossing IN FRONT
    # of the matchstick so the grip reads
    thumb = bezier((496, 990), (540, 906), (614, 866), 20)
    d.line(thumb, fill=HAND, width=50, joint="curve")
    d.ellipse([598, 850, 630, 882], fill=HAND)
    return base


def rim_light(base):
    """Thin warm highlight hugging the flame-facing edge of each
    finger and the thumb, offset toward the flame point."""
    d = ImageDraw.Draw(base)
    fx, fy = FLAME_X, 690

    def toward(pts):
        mx = sum(p[0] for p in pts) / len(pts)
        my = sum(p[1] for p in pts) / len(pts)
        dx, dy = fx - mx, fy - my
        dist = math.hypot(dx, dy) or 1
        return [(x + dx / dist * 17, y + dy / dist * 17) for x, y in pts]

    curves = [
        bezier((556, 884), (588, 828), (604, 792), 20),
        bezier((622, 878), (640, 818), (648, 782), 20),
        bezier((688, 878), (694, 820), (690, 786), 20),
        bezier((748, 884), (742, 830), (730, 800), 20),
        bezier((496, 990), (540, 906), (614, 866), 20),
    ]
    for curve in curves:
        # stop short of the tip so the highlight never pokes past
        # the fingertip into the sky
        d.line(toward(curve[: int(len(curve) * 0.8)]), fill=RIM,
               width=4, joint="curve")
    return base


def flame_polygon(scale):
    """Teardrop flame, leaning slightly right, scaled about its base."""
    cx, by = FLAME_X, FLAME_BASE_Y
    tip = (656, 628)
    left = bezier((616, 748), (600, 690), tip, 16)
    right = bezier((668, 748), (676, 694), tip, 16)
    pts = left + list(reversed(right))
    out = []
    for x, y in pts:
        out.append((cx + (x - cx) * scale, by + (y - by) * scale))
    return out


def draw_flame(base, glow):
    gd = ImageDraw.Draw(glow)
    # big soft halo around the flame
    gd.ellipse([FLAME_X - 130, 520, FLAME_X + 150, 830],
               fill=(255, 120, 20, 70))
    gd.ellipse([FLAME_X - 80, 570, FLAME_X + 96, 800],
               fill=(255, 160, 50, 90))
    d = ImageDraw.Draw(base)
    d.polygon(flame_polygon(1.0), fill=FLAME_OUTER)
    d.polygon(flame_polygon(0.68), fill=FLAME_MID)
    d.polygon(flame_polygon(0.45), fill=FLAME_INNER)
    d.ellipse([FLAME_X - 13, 700, FLAME_X + 15, 748], fill=FLAME_CORE)
    return base


def draw_lantern(base, glow, cx, cy, s):
    """One paper lantern: glow halo, warm body, dark caps."""
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - s * 1.9, cy - s * 1.9, cx + s * 1.9, cy + s * 1.9],
               fill=(255, 140, 40, 65))
    d = ImageDraw.Draw(base)
    d.ellipse([cx - s * 0.55, cy - s * 0.66, cx + s * 0.55, cy + s * 0.66],
              fill=(255, 140, 46, 255))
    d.ellipse([cx - s * 0.38, cy - s * 0.48, cx + s * 0.38, cy + s * 0.48],
              fill=(255, 179, 71, 255))
    d.ellipse([cx - s * 0.18, cy - s * 0.26, cx + s * 0.18, cy + s * 0.26],
              fill=(255, 230, 163, 255))
    d.rectangle([cx - s * 0.28, cy - s * 0.78, cx + s * 0.28, cy - s * 0.60],
                fill=(60, 30, 16, 255))
    d.rectangle([cx - s * 0.20, cy + s * 0.60, cx + s * 0.20, cy + s * 0.74],
                fill=(60, 30, 16, 255))


def lantern_streams(base, glow, rng):
    """A river of lanterns climbing out of the flame in three streams."""
    streams = [
        ((FLAME_X, 690), (800, 420), (960, 140), 58),
        ((FLAME_X, 690), (430, 430), (120, 190), 52),
        ((FLAME_X, 690), (640, 430), (660, 100), 34),
    ]
    lanterns = []
    for p0, p1, p2, count in streams:
        for _ in range(count):
            t = rng.uniform(0.04, 1.0)
            bx, by = bezier(p0, p1, p2, 40)[int(t * 40)]
            # perpendicular jitter, wider as the stream spreads
            jx = rng.uniform(-1, 1) * (26 + 70 * t)
            jy = rng.uniform(-1, 1) * (20 + 46 * t)
            size = (30 - 21 * t) * rng.uniform(0.8, 1.15)
            lanterns.append((bx + jx, by + jy, size))
    # a few dim strays high in the sky for depth
    for _ in range(16):
        lanterns.append((rng.uniform(60, W - 60), rng.uniform(60, 320),
                         rng.uniform(6, 11)))
    # small first so big lanterns overlap them
    lanterns.sort(key=lambda item: item[2])
    for cx, cy, s in lanterns:
        draw_lantern(base, glow, cx, cy, s)
    return base


def draw_text(base):
    d = ImageDraw.Draw(base)
    font = ImageFont.truetype(FONT_PATH, 54)
    x, y = 56, 914
    d.text((x + 3, y + 3), "one spark.", font=font, fill=TEXT_SHADOW)
    d.text((x, y), "one spark.", font=font, fill=TEXT_COL)
    return base


def main():
    rng = random.Random(SEED)
    base = sky()
    base = stars(base, rng)
    base = skyline(base, rng)
    base = draw_hand(base)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base = lantern_streams(base, glow, rng)
    base = draw_flame(base, glow)
    glow = glow.filter(ImageFilter.GaussianBlur(16))
    base = Image.alpha_composite(base, glow)
    base = rim_light(base)
    base = draw_text(base)
    base.convert("RGB").save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, base.size)


if __name__ == "__main__":
    main()
