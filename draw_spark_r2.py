#!/usr/bin/env python3
"""One Spark — round 2. A giant hand holds one match; its flame becomes
hundreds of paper lanterns rising over a sleeping city.

Drawn from scratch with PIL (no photos, no copied art). Fully deterministic:
fixed seed, no timestamps, no network. Run: python3 draw_spark_r2.py [out.png]
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entry.png")
RNG = random.Random(20261116)

SKIN = (201, 138, 94)
SKIN_DARK = (122, 74, 46)
SKIN_LIGHT = (232, 178, 128)
RIM = (255, 179, 71)
MATCH_WOOD = (217, 160, 102)
MATCH_CHAR = (58, 42, 26)
CITY = (11, 8, 23)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vertical_gradient(size, stops):
    """stops: list of (pos 0..1, rgb). Returns RGB image."""
    w, h = size
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                px[0, y] = lerp(c0, c1, (t - p0) / max(p1 - p0, 1e-9))
                break
        else:
            px[0, y] = stops[-1][1]
    return strip.resize((w, h), Image.BICUBIC)


def glow_layer(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def add_glow(base, glow, blur=18):
    base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(blur)))


def capsule(draw, p1, p2, width, fill):
    """Thick line with round caps."""
    draw.line([p1, p2], fill=fill, width=width)
    r = width // 2
    for p in (p1, p2):
        draw.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=fill)


def star_field(draw, glow, n=190):
    for _ in range(n):
        x = RNG.uniform(0, W)
        y = RNG.uniform(0, 640)
        r = RNG.uniform(0.6, 2.2)
        b = RNG.uniform(120, 255)
        c = (int(b), int(b * 0.95), 255)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=c)
        if r > 1.8 and RNG.random() < 0.35:
            gd = ImageDraw.Draw(glow)
            gd.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(180, 190, 255, 90))
            gd.line([x - 9, y, x + 9, y], fill=(200, 210, 255, 70), width=1)
            gd.line([x, y - 9, x, y + 9], fill=(200, 210, 255, 70), width=1)


def crescent_moon(base, glow):
    cx, cy, r = 872, 128, 46
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(235, 232, 210, 255))
    d.ellipse([cx - r + 20, cy - r - 8, cx + r + 20, cy + r - 8],
              fill=(0, 0, 0, 0))
    # cut the crescent by erasing with a sky-coloured disc offset up-right
    cut = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(cut)
    dc.ellipse([cx - r + 22, cy - r - 10, cx + r + 22, cy + r - 10],
               fill=(10, 12, 40, 255))
    layer = Image.alpha_composite(layer, cut)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - r - 26, cy - r - 26, cx + r + 26, cy + r + 26],
               fill=(200, 200, 170, 46))
    base.alpha_composite(layer)


def city_skyline(draw):
    x = -10
    while x < W + 10:
        bw = RNG.uniform(44, 112)
        # left side low (keeps the text clear), right side taller
        hmax = 120 if x < 420 else 210
        bh = RNG.uniform(56, hmax)
        top = H - bh
        col = (CITY[0] + RNG.randint(-2, 6), CITY[1] + RNG.randint(-1, 4),
               CITY[2] + RNG.randint(0, 10))
        draw.rectangle([x, top, x + bw, H], fill=col)
        # rooftop antenna on some buildings
        if RNG.random() < 0.3:
            ax = x + bw * 0.5
            ah = RNG.uniform(14, 34)
            ly = top - RNG.uniform(30, 40)
            draw.line([ax, top, ax, top - ah], fill=col, width=3)
            draw.ellipse([ax - 3, ly - 3, ax + 3, ly + 3],
                         fill=(255, 90, 60))
        # sparse sleepy windows
        for wy in range(int(top) + 14, H - 12, 18):
            for wx in range(int(x) + 8, int(x + bw) - 8, 16):
                if RNG.random() < 0.07:
                    warm = RNG.random() < 0.8
                    wc = (255, 210, 122) if warm else (127, 176, 255)
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=wc)
        x += bw + RNG.uniform(2, 10)
    # ground haze line
    draw.rectangle([0, H - 4, W, H], fill=(20, 12, 34))


def flame(base, glow, cx, cy):
    """Teardrop flame centred at (cx, cy) — tip up, base at cy+38."""
    gx, gy = cx, cy - 6
    gd = ImageDraw.Draw(glow)
    gd.ellipse([gx - 95, gy - 95, gx + 95, gy + 95], fill=(255, 140, 30, 70))
    gd.ellipse([gx - 55, gy - 55, gx + 55, gy + 55], fill=(255, 190, 80, 90))

    def teardrop(scale, color, wobble):
        pts = []
        for i in range(33):
            t = i / 32.0  # 0 bottom -> 1 tip
            y = cy + 38 - t * 96 * scale
            half = (math.sin(t * math.pi * 0.82) ** 0.8) * 30 * scale
            sway = math.sin(t * 3.2 + wobble) * 7 * t * scale
            pts.append((cx + sway - half, y))
        for i in range(32, -1, -1):
            t = i / 32.0
            y = cy + 38 - t * 96 * scale
            half = (math.sin(t * math.pi * 0.82) ** 0.8) * 30 * scale
            sway = math.sin(t * 3.2 + wobble) * 7 * t * scale
            pts.append((cx + sway + half, y))
        return pts

    d = ImageDraw.Draw(base)
    d.polygon(teardrop(1.0, None, 0.0), fill=(255, 123, 28))
    d.polygon(teardrop(0.68, None, 0.4), fill=(255, 179, 71))
    d.polygon(teardrop(0.42, None, 0.8), fill=(255, 243, 176))
    d.ellipse([cx - 9, cy + 12, cx + 9, cy + 30], fill=(255, 255, 240))


def matchstick(draw, p1, p2):
    capsule(draw, p1, p2, 17, MATCH_WOOD)
    # charred head near the flame end
    t = 0.86
    hx = p1[0] + (p2[0] - p1[0]) * t
    hy = p1[1] + (p2[1] - p1[1]) * t
    capsule(draw, (hx, hy), p2, 17, MATCH_CHAR)
    draw.ellipse([p2[0] - 9, p2[1] - 9, p2[0] + 9, p2[1] + 9],
                 fill=(255, 120, 40))


def hand(base, glow):
    """Giant stylised hand, flat-illustration style, entering from the
    bottom-right, fist wrapped around the matchstick. The stick runs
    down-right into the fist; four fingers cross it and end on the far
    side, the thumb presses it from below."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # forearm from bottom-right corner
    capsule(d, (1120, 1120), (950, 970), 200, SKIN + (255,))
    # palm blob, mostly off-canvas bottom-right
    palm = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dp = ImageDraw.Draw(palm)
    dp.ellipse([660, 820, 1060, 1120], fill=SKIN + (255,))
    palm = palm.rotate(-16, center=(860, 970))
    layer.alpha_composite(palm)

    # stick direction (flame end -> grip end) and its normals
    # grip points along the stick, from the lower end toward the flame
    grip = [(793, 871), (770, 847), (747, 823), (724, 798)]
    n_far = (0.72, -0.69)   # far side of the stick (up-right)
    n_near = (-0.72, 0.69)  # near side (down-left, palm side)
    for i, g in enumerate(grip):
        bx = g[0] + n_near[0] * 58
        by = g[1] + n_near[1] * 58
        tx = g[0] + n_far[0] * 92
        ty = g[1] + n_far[1] * 92
        capsule(d, (bx, by), g, 52, SKIN + (255,))
        capsule(d, g, (tx, ty), 46, SKIN + (255,))
        # fingertip nail on the far side, oriented along the finger
        d.ellipse([tx - 13, ty - 17, tx + 13, ty + 11],
                  fill=SKIN_LIGHT + (255,))
        # groove between this finger and the next
        if i < 3:
            ng = grip[i + 1]
            nbx = ng[0] + n_near[0] * 58
            nby = ng[1] + n_near[1] * 58
            ntx = ng[0] + n_far[0] * 92
            nty = ng[1] + n_far[1] * 92
            d.line([((bx + nbx) / 2, (by + nby) / 2),
                    ((g[0] + ng[0]) / 2, (g[1] + ng[1]) / 2),
                    ((tx + ntx) / 2, (ty + nty) / 2)],
                   fill=SKIN_DARK + (255,), width=9, joint="curve")
    # thumb pressing the stick from below, separated from the palm by a
    # dark edge line so it reads as its own digit
    capsule(d, (880, 980), (790, 900), 56, SKIN + (255,))
    capsule(d, (790, 900), (742, 858), 50, SKIN + (255,))
    d.ellipse([726, 838, 752, 864], fill=SKIN_LIGHT + (255,))
    d.line([(884, 952), (796, 876), (748, 836)],
           fill=SKIN_DARK + (255,), width=5, joint="curve")

    # warm rim light on the flame-facing edges
    gd = ImageDraw.Draw(glow)
    for g in grip:
        tx = g[0] + n_far[0] * 92
        ty = g[1] + n_far[1] * 92
        gd.line([g, (tx, ty)], fill=(255, 179, 71, 110), width=7)
    gd.line([(950, 970), (880, 920)], fill=(255, 179, 71, 60), width=10)

    base.alpha_composite(layer)


def lantern_stream(base, glow, flame_xy):
    """Lanterns rising from the flame, curving up-left, spreading and
    shrinking as they climb — the flame becoming a sky of lanterns."""
    fx, fy = flame_xy
    d = ImageDraw.Draw(base)
    gd = ImageDraw.Draw(glow)
    count = 0
    for i in range(150):
        t = RNG.random() ** 0.8
        # bezier-ish rise: up and left, widening with height
        x = fx - 445 * t + math.sin(t * 3.6) * 46 + RNG.uniform(-1, 1) * (26 + 165 * t)
        y = fy - 30 - 520 * t + RNG.uniform(-14, 14)
        size = 26 - 19 * t + RNG.uniform(-2, 2)
        if size < 5:
            size = 5
        # warm palette, brighter near the flame
        warm = RNG.random()
        if warm < 0.5:
            col = (255, 179, 71)
        elif warm < 0.8:
            col = (255, 140, 66)
        else:
            col = (255, 217, 122)
        alpha = int(255 - 70 * t)
        # glow halo
        gd.ellipse([x - size, y - size, x + size, y + size],
                   fill=col + (70,))
        # paper body: rounded rect, slightly taller than wide
        w2, h2 = size * 0.82, size
        d.rounded_rectangle([x - w2, y - h2, x + w2, y + h2],
                            radius=size * 0.45, fill=col + (alpha,))
        # top cap + bottom tassel
        d.rectangle([x - w2 * 0.55, y - h2 - 2, x + w2 * 0.55, y - h2 + 3],
                    fill=(120, 40, 20, alpha))
        d.line([x, y + h2, x + RNG.uniform(-2, 2), y + h2 + size * 0.55],
               fill=(255, 200, 120, alpha), width=2)
        # paper ribs
        d.line([x - w2 * 0.55, y - h2 * 0.4, x + w2 * 0.55, y - h2 * 0.4],
               fill=(255, 230, 170, int(alpha * 0.55)), width=1)
        d.line([x - w2 * 0.55, y + h2 * 0.4, x + w2 * 0.55, y + h2 * 0.4],
               fill=(255, 230, 170, int(alpha * 0.55)), width=1)
        count += 1
    # embers near the flame
    for _ in range(26):
        ex = fx + RNG.uniform(-70, 70)
        ey = fy + RNG.uniform(-60, 30)
        r = RNG.uniform(1.0, 2.6)
        gd.ellipse([ex - r * 3, ey - r * 3, ex + r * 3, ey + r * 3],
                   fill=(255, 170, 60, 120))
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 220, 150))
    return count


def text_caption(base):
    d = ImageDraw.Draw(base)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 46)
    except OSError:
        font = ImageFont.load_default()
    x, y = 56, 786
    d.text((x + 3, y + 3), "one spark.", font=font, fill=(10, 8, 30, 255))
    d.text((x, y), "one spark.", font=font, fill=(255, 233, 196, 255))


def main():
    sky = vertical_gradient(
        (W, H),
        [(0.0, (8, 10, 38)), (0.55, (24, 18, 66)),
         (0.82, (58, 32, 72)), (1.0, (26, 15, 42))])
    img = sky.convert("RGBA")
    glow = glow_layer((W, H))

    d = ImageDraw.Draw(img)
    star_field(d, glow)
    crescent_moon(img, glow)
    city_skyline(d)
    add_glow(img, glow, blur=14)
    glow = glow_layer((W, H))

    # horizon warmth above the sleeping city
    gd = ImageDraw.Draw(glow)
    gd.ellipse([120, 760, 900, 1060], fill=(255, 140, 60, 34))
    add_glow(img, glow, blur=42)
    glow = glow_layer((W, H))

    # match + flame first (hand grips over the match)
    d = ImageDraw.Draw(img)
    matchstick(d, (828, 908), (596, 664))
    flame(img, glow, 578, 622)
    add_glow(img, glow, blur=16)
    glow = glow_layer((W, H))

    hand(img, glow)
    # warm light wash over the hand from the flame
    gd = ImageDraw.Draw(glow)
    gd.ellipse([430, 470, 900, 1000], fill=(255, 150, 50, 26))
    add_glow(img, glow, blur=60)
    glow = glow_layer((W, H))

    n = lantern_stream(img, glow, (578, 600))
    add_glow(img, glow, blur=7)

    text_caption(img)

    img.convert("RGB").save(OUT, format="PNG")
    print(f"lanterns={n} bytes={OUT.stat().st_size} -> {OUT}")


if __name__ == "__main__":
    main()
