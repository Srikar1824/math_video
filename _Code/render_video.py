"""
render_v3.py  –  Studio-grade final render for math vid 1.mp4
Upgrades over render_v2.py:
  1. Smooth cubic-eased crossfade transitions between every scene & sub-card
  2. Strict border padding (30-48px) and pixel-accurate word-wrapping (_wrap_text)
  3. Clipped 2D coordinate viewports so grids/vectors never bleed outside borders
  4. Pixel-perfect centered typography (_center_text) on Title & Credits cards
  5. Dark pill backgrounds on vector labels for crisp legibility
  6. Staggered, narration-synced element reveals across all 6 scenes
  7. Chaptered bottom progress bar with scene markers
"""

import os
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ─── Canvas & Audio ──────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1920, 1080
FPS = 30
AUDIO_SRC = "20261124_233858 (online-audio-converter.com).mp3"
TOTAL_SECONDS = 339.696
TOTAL_FRAMES = int(round(TOTAL_SECONDS * FPS))
OUTPUT_VIDEO = "math vid 1.mp4"

FONT_DIR = (
    "/Library/Frameworks/Python.framework/Versions/3.14"
    "/lib/python3.14/site-packages/matplotlib/mpl-data/fonts/ttf"
)

def _font(size, bold=False, mono=False):
    if mono:
        name = "DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    p = os.path.join(FONT_DIR, name)
    return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.load_default()

F60B = _font(60, bold=True)
F52B = _font(52, bold=True)
F44B = _font(44, bold=True)
F36B = _font(36, bold=True)
F30B = _font(30, bold=True)
F26B = _font(26, bold=True)
F26  = _font(26)
F24B = _font(24, bold=True)
F24  = _font(24)
F22B = _font(22, bold=True)
F22  = _font(22)
F20B = _font(20, bold=True)
F20  = _font(20)
F18B = _font(18, bold=True)
F18  = _font(18)
F16  = _font(16)
F26M = _font(26, mono=True, bold=True)
F22M = _font(22, mono=True)
F20M = _font(20, mono=True)

# ─── Palette ─────────────────────────────────────────────────────────────────
BG         = (13,  18,  28)
PLOT_BG    = (16,  22,  34)
GRID_C     = (28,  39,  58)
AXIS_C     = (82,  98, 122)
GOLD       = (255, 209, 102)
GREEN      = (6,   214, 160)
BLUE       = (76,  201, 240)
ORANGE     = (255, 128,  20)
RED        = (239,  71, 111)
WHITE      = (248, 250, 252)
MUTED      = (156, 172, 194)
DIM        = (95,  112, 136)
BOX_BG     = (20,  27,  41)
BOX_BORDER = (46,  60,  86)

# ─── Easing & Color Helpers ──────────────────────────────────────────────────
def _clamp01(x):
    return 0.0 if x <= 0.0 else (1.0 if x >= 1.0 else x)

def _ease_out(x):
    x = _clamp01(x)
    return 1.0 - (1.0 - x) ** 3

def _ease_io(x):
    x = _clamp01(x)
    return 4*x*x*x if x < 0.5 else 1.0 - ((-2*x + 2)**3) / 2.0

def _fade(t, start, dur=0.55):
    return _ease_out((t - start) / dur)

def _lerp_c(c1, c2, a):
    a = _clamp01(a)
    return (
        int(c1[0] + (c2[0] - c1[0]) * a),
        int(c1[1] + (c2[1] - c1[1]) * a),
        int(c1[2] + (c2[2] - c1[2]) * a),
    )

def _text_w(font, text):
    try:
        return font.getlength(text)
    except Exception:
        return len(text) * (font.size * 0.58)

def _center_text(draw, text, cx, y, font, fill):
    w = _text_w(font, text)
    draw.text((cx - w / 2.0, y), text, fill=fill, font=font)

def _wrap_text(draw, text, x, y, max_w, font, fill, line_h=None):
    """Word-wrap text cleanly inside max_w; returns final y after last line."""
    if line_h is None:
        line_h = int(font.size * 1.42)
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        cand = w if not cur else f"{cur} {w}"
        if _text_w(font, cand) <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        draw.text((x, y), ln, fill=fill, font=font)
        y += line_h
    return y

def _safe_line(draw, text, x, y, x_max, font, fill):
    """Single-line draw guaranteed not to exceed x_max."""
    if _text_w(font, text) > (x_max - x):
        while text and _text_w(font, text + "…") > (x_max - x):
            text = text[:-1]
        text = text + "…"
    draw.text((x, y), text, fill=fill, font=font)

# ─── Shared UI Elements ──────────────────────────────────────────────────────
def _header(draw, title, scene_num, scene_lbl):
    draw.rectangle([0, 0, WIDTH, 98], fill=(10, 14, 22))
    draw.line([(0, 98), (WIDTH, 98)], fill=(40, 52, 74), width=2)
    draw.rectangle([0, 0, 6, 98], fill=GREEN)

    draw.text((52, 16), "LINEAR ALGEBRA & CALCULUS (M3)  •  INTERNAL ASSESSMENT",
              fill=GREEN, font=F18B)
    _safe_line(draw, title, 52, 46, WIDTH - 470, F26B, WHITE)

    pill = f"Scene {scene_num} / 6  •  {scene_lbl}"
    pw = int(_text_w(F20B, pill)) + 44
    px1 = WIDTH - 50
    px0 = px1 - max(pw, 320)
    draw.rounded_rectangle([px0, 22, px1, 76], radius=10,
                           fill=(22, 31, 48), outline=BOX_BORDER, width=2)
    _center_text(draw, pill, (px0 + px1) / 2.0, 37, F20B, GOLD)

def _progress(draw, t):
    bar_y = HEIGHT - 10
    p = _clamp01(t / TOTAL_SECONDS)
    draw.rectangle([0, bar_y, WIDTH, HEIGHT], fill=(18, 24, 36))
    draw.rectangle([0, bar_y, int(WIDTH * p), HEIGHT], fill=GREEN)
    # Scene boundary ticks
    for ts in (51.3, 93.8, 152.3, 263.9, 313.0):
        tx = int(WIDTH * (ts / TOTAL_SECONDS))
        draw.line([(tx, bar_y), (tx, HEIGHT)], fill=BG, width=2)

def _dash(draw, p1, p2, color, lw=2, dl=12, gl=8):
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    dist = np.hypot(dx, dy)
    if dist < 1:
        return
    ux, uy = dx / dist, dy / dist
    c = 0.0
    while c < dist:
        e = min(c + dl, dist)
        draw.line([(x1 + ux * c, y1 + uy * c), (x1 + ux * e, y1 + uy * e)], fill=color, width=lw)
        c += dl + gl

def _vec(draw, ox, oy, vx, vy, color, lw=4, alen=16, lbl=None, pw=1080, ph=840):
    tx, ty = ox + vx, oy - vy
    draw.line([(ox, oy), (tx, ty)], fill=color, width=lw)
    L = np.hypot(vx, vy)
    if L > 4:
        ux, uy = vx / L, -vy / L
        px, py = -uy, ux
        a1x = tx - ux * alen + px * (alen * 0.45)
        a1y = ty - uy * alen + py * (alen * 0.45)
        a2x = tx - ux * alen - px * (alen * 0.45)
        a2y = ty - uy * alen - py * (alen * 0.45)
        draw.polygon([(tx, ty), (a1x, a1y), (a2x, a2y)], fill=color)
    if lbl:
        tw = _text_w(F18B, lbl)
        lx = tx + (14 if vx >= 0 else -(tw + 26))
        ly = ty + (10 if vy <= 0 else -34)
        # Keep pill strictly inside plot viewport padding
        lx = max(16, min(lx, pw - tw - 28))
        ly = max(16, min(ly, ph - 40))
        draw.rounded_rectangle([lx - 8, ly - 4, lx + tw + 8, ly + 26],
                               radius=6, fill=(13, 18, 28), outline=color, width=1)
        draw.text((lx, ly), lbl, fill=color, font=F18B)

# ─── SCENE 1: Title Card & Hook ──────────────────────────────────────────────
def _scene1(img, draw, t):
    if t < 6.5:
        # ── Opening Title Card (strictly centered & generously padded) ──
        a1 = _fade(t, 0.0, 0.7)
        a2 = _fade(t, 0.35, 0.7)
        a3 = _fade(t, 0.8, 0.7)

        for x in range(0, WIDTH, 80):
            draw.line([(x, 0), (x, HEIGHT)], fill=(19, 26, 39), width=1)
        for y in range(0, HEIGHT, 80):
            draw.line([(0, y), (WIDTH, y)], fill=(19, 26, 39), width=1)

        # Outer subtle frame
        draw.rounded_rectangle([64, 52, WIDTH - 64, HEIGHT - 52], radius=24,
                               outline=_lerp_c(BG, BOX_BORDER, a1), width=2)

        _center_text(draw, "LINEAR ALGEBRA AND CALCULUS (M3)  •  INTERNAL ASSESSMENT",
                     WIDTH / 2.0, 130, F24B, _lerp_c(BG, GOLD, a1))
        _center_text(draw, "EIGENVALUES & EIGENVECTORS",
                     WIDTH / 2.0, 195, F60B, _lerp_c(BG, WHITE, a1))

        # Animated accent bar
        bar_half = int(280 * _ease_out(t / 1.0))
        if bar_half > 2:
            draw.rounded_rectangle([WIDTH // 2 - bar_half, 282, WIDTH // 2 + bar_half, 287],
                                   radius=3, fill=GREEN)

        _center_text(draw, "Visualizing Invariant Directions of Linear Transformations",
                     WIDTH / 2.0, 310, F26, _lerp_c(BG, GREEN, a2))

        # Student card (960px wide, 48px padding on all sides)
        cx0, cy0, cx1, cy1 = WIDTH // 2 - 480, 405, WIDTH // 2 + 480, 775
        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=18,
                               fill=_lerp_c(BG, BOX_BG, a3),
                               outline=_lerp_c(BG, BOX_BORDER, a3), width=2)
        draw.text((cx0 + 48, cy0 + 34), "PROJECT SUBMISSION DETAILS",
                  fill=_lerp_c(BG, BLUE, a3), font=F22B)
        draw.line([(cx0 + 48, cy0 + 78), (cx1 - 48, cy0 + 78)],
                  fill=_lerp_c(BG, BOX_BORDER, a3), width=1)

        rows = [
            ("Student Name:", "Srikar Burgu"),
            ("Student ID:",   "E25B070605"),
            ("Course:",       "Linear Algebra & Calculus (M3)"),
            ("Format:",       "5-Min Programmatic Animation (Python + FFmpeg)"),
            ("Assessment:",   "10% Internal Assessment"),
        ]
        y = cy0 + 106
        for label, val in rows:
            draw.text((cx0 + 48, y), label, fill=_lerp_c(BG, MUTED, a3), font=F22)
            draw.text((cx0 + 250, y), val,  fill=_lerp_c(BG, WHITE, a3), font=F22B)
            y += 50

        _center_text(draw, "Prepared with Original Voice Narration  •  November 2026",
                     WIDTH / 2.0, 865, F20, _lerp_c(BG, DIM, a3))
        return

    # ── Hook Animation (6.5s -> 51.3s) ──
    _header(draw, "Scene 1: How Linear Transformations Warp 2D Space", 1, "The Hook & Context")

    # Left Viewport Card (clipped cleanly inside [50, 122, 1130, 968])
    vx0, vy0, vx1, vy1 = 50, 122, 1130, 968
    pw, ph = vx1 - vx0, vy1 - vy0
    plot_img = Image.new("RGB", (pw, ph), PLOT_BG)
    pd = ImageDraw.Draw(plot_img)

    ox, oy = pw // 2, ph // 2 + 20
    sc = 54.0
    wt = np.sin((t - 6.5) * 0.45) * 0.5 + 0.5
    M = (1 - wt) * np.eye(2) + wt * np.array([[1.8, 0.9], [0.4, 1.4]])

    # Subtle background grid & warped grid
    for i in range(-7, 8):
        pt = M @ np.array([float(i), 7.0]) * sc
        pb = M @ np.array([float(i), -7.0]) * sc
        pd.line([(ox + pt[0], oy - pt[1]), (ox + pb[0], oy - pb[1])], fill=GRID_C, width=1)
        pl = M @ np.array([-7.0, float(i)]) * sc
        pr = M @ np.array([7.0, float(i)]) * sc
        pd.line([(ox + pl[0], oy - pl[1]), (ox + pr[0], oy - pr[1])], fill=GRID_C, width=1)

    for d in [(-7.5, 0), (7.5, 0), (0, -7.5), (0, 7.5)]:
        p = M @ np.array(d) * sc
        pd.line([(ox, oy), (ox + p[0], oy - p[1])], fill=AXIS_C, width=2)

    # Vectors with dashed original span lines
    vecs = [
        (np.array([2.0, 2.5]),  ORANGE, "v (orange)"),
        (np.array([-2.2, 2.0]), RED,    "u"),
        (np.array([2.5, -1.6]), GOLD,   "w"),
    ]
    for v0, col, lbl in vecs:
        vt = M @ v0 * sc
        v0s = v0 * sc * 1.6
        _dash(pd, (ox - v0s[0] * 0.25, oy + v0s[1] * 0.25),
              (ox + v0s[0], oy - v0s[1]), (58, 72, 96), lw=1)
        _vec(pd, ox, oy, vt[0], vt[1], col, lw=4, lbl=lbl, pw=pw, ph=ph)

    # Origin dot
    pd.ellipse([ox - 6, oy - 6, ox + 6, oy + 6], fill=WHITE)

    # Viewport top-left badge (padded inside viewport)
    badge_txt = "2D LINEAR TRANSFORMATION SPACE"
    bw = int(_text_w(F18B, badge_txt)) + 32
    pd.rounded_rectangle([24, 22, 24 + bw, 62], radius=8, fill=(13, 18, 28), outline=BOX_BORDER, width=1)
    pd.text((40, 32), badge_txt, fill=MUTED, font=F18B)

    img.paste(plot_img, (vx0, vy0))
    draw.rounded_rectangle([vx0, vy0, vx1, vy1], radius=14, outline=BOX_BORDER, width=2)

    # Right Explanation Panel (padded 32px inside [1160, 122, 1870, 968])
    px0, py0, px1, py1 = 1160, 122, 1870, 968
    draw.rounded_rectangle([px0, py0, px1, py1], radius=14, fill=BOX_BG, outline=BOX_BORDER, width=2)
    pad = 32
    ix = px0 + pad
    iw = (px1 - px0) - 2 * pad

    a_p1 = _fade(t, 6.5, 0.7)
    a_p2 = _fade(t, 12.0, 0.7)

    draw.text((ix, py0 + 28), "OBSERVATION & MOTIVATION", fill=_lerp_c(BOX_BG, GOLD, a_p1), font=F22B)
    draw.line([(ix, py0 + 66), (ix + iw, py0 + 66)], fill=BOX_BORDER, width=1)

    y = py0 + 88
    draw.text((ix, y), "1. Matrices as Transformations:", fill=_lerp_c(BOX_BG, WHITE, a_p1), font=F22B)
    y = _wrap_text(draw, "A matrix stretches, shears, or rotates every point in 2D space.",
                   ix + 12, y + 36, iw - 12, F22, _lerp_c(BOX_BG, MUTED, a_p1))

    y += 20
    draw.text((ix, y), "2. General Behaviour:", fill=_lerp_c(BOX_BG, WHITE, a_p2), font=F22B)
    y = _wrap_text(draw, "Almost every vector rotates OFF its original span line when transformed.",
                   ix + 12, y + 36, iw - 12, F22, _lerp_c(BOX_BG, RED, a_p2))

    # Sub-card transition at t=36s
    card_top = y + 32
    if t < 36.0:
        qa = _fade(t, 18.0, 0.8)
        qb0, qb1 = card_top, py1 - 36
        draw.rounded_rectangle([ix, qb0, ix + iw, qb1], radius=12,
                               fill=_lerp_c(BOX_BG, (28, 36, 54), qa),
                               outline=_lerp_c(BOX_BG, GOLD, qa), width=2)
        cp = 26
        cy = qb0 + 28
        draw.text((ix + cp, cy), "THE GUIDING QUESTION:", fill=_lerp_c(BOX_BG, GOLD, qa), font=F22B)
        cy = _wrap_text(draw, "Are there special vectors that REFUSE to rotate?",
                        ix + cp, cy + 44, iw - 2 * cp, F24B, _lerp_c(BOX_BG, WHITE, qa))
        _wrap_text(draw, "Vectors that stay on their exact span line, merely stretching or shrinking?",
                   ix + cp, cy + 16, iw - 2 * cp, F22, _lerp_c(BOX_BG, MUTED, qa))
    else:
        aa = _fade(t, 36.0, 0.7)
        ab0, ab1 = card_top, py1 - 36
        draw.rounded_rectangle([ix, ab0, ix + iw, ab1], radius=12,
                               fill=_lerp_c(BOX_BG, (16, 44, 38), aa),
                               outline=_lerp_c(BOX_BG, GREEN, aa), width=2)
        cp = 26
        cy = ab0 + 26
        draw.text((ix + cp, cy), "YES — INVARIANT DIRECTIONS!", fill=_lerp_c(BOX_BG, GREEN, aa), font=F22B)
        cy += 48
        draw.text((ix + cp, cy), "Eigenvector (v):", fill=_lerp_c(BOX_BG, WHITE, aa), font=F22B)
        cy = _wrap_text(draw, "A non-zero vector that NEVER rotates under A. Stays locked on its 1D span line.",
                        ix + cp, cy + 34, iw - 2 * cp, F20, _lerp_c(BOX_BG, MUTED, aa))
        cy += 22
        draw.text((ix + cp, cy), "Eigenvalue (λ):", fill=_lerp_c(BOX_BG, WHITE, aa), font=F22B)
        _wrap_text(draw, "The scalar factor by which the eigenvector stretches, shrinks, or flips.",
                   ix + cp, cy + 34, iw - 2 * cp, F20, _lerp_c(BOX_BG, MUTED, aa))

# ─── SCENE 2: Concept Introduction ───────────────────────────────────────────
def _scene2(img, draw, t):
    _header(draw, "Scene 2: The Eigenvalue Equation  A v = λ v", 2, "Concept Introduction")

    a_top = _fade(t, 51.3, 0.7)
    draw.rounded_rectangle([120, 122, 1800, 342], radius=16,
                           fill=BOX_BG, outline=_lerp_c(BG, GOLD, a_top), width=3)
    _center_text(draw, "THE FUNDAMENTAL EIGENVALUE EQUATION", WIDTH / 2.0, 146, F22B, _lerp_c(BG, GOLD, a_top))
    _center_text(draw, "A  v   =   λ  v", WIDTH / 2.0, 200, F52B, _lerp_c(BG, WHITE, a_top))
    _center_text(draw, "(Matrix × Eigenvector  =  Pure Scalar Multiplication)", WIDTH / 2.0, 286, F22, _lerp_c(BG, MUTED, a_top))

    cols = [
        ("A", "Square Matrix", "(n × n)", GOLD, 53.0, [
            "Represents the linear transformation.",
            "Normally rotates & shears vectors.",
            "Models differential equations, graphs, and physics."
        ], 120),
        ("v", "Eigenvector", "(v ≠ 0)", GREEN, 58.0, [
            "A non-zero input vector.",
            "Defines an invariant direction.",
            "Does NOT rotate when hit by A.",
            "Locks onto its 1D span (eigenspace)."
        ], 695),
        ("λ", "Eigenvalue", "(Scalar)", BLUE, 64.0, [
            "An ordinary real or complex number.",
            "Stretch factor along the eigenvector.",
            "λ > 1 stretches  |  0 < λ < 1 shrinks.",
            "λ < 0 flips the vector's direction."
        ], 1270),
    ]

    bw = 530
    by0, by1 = 374, 835
    for sym, name, sub, col, reveal_t, bullets, lx in cols:
        ca = _fade(t, reveal_t, 0.7)
        draw.rounded_rectangle([lx, by0, lx + bw, by1], radius=14,
                               fill=BOX_BG, outline=_lerp_c(BOX_BG, col, ca), width=2)
        draw.text((lx + 28, by0 + 26), sym,  fill=_lerp_c(BOX_BG, col, ca),   font=F44B)
        draw.text((lx + 88, by0 + 24), name, fill=_lerp_c(BOX_BG, WHITE, ca), font=F24B)
        draw.text((lx + 88, by0 + 58), sub,  fill=_lerp_c(BOX_BG, MUTED, ca), font=F18)
        draw.line([(lx + 28, by0 + 98), (lx + bw - 28, by0 + 98)], fill=BOX_BORDER, width=1)

        yb = by0 + 120
        for b in bullets:
            yb = _wrap_text(draw, f"• {b}", lx + 28, yb, bw - 56, F20,
                            _lerp_c(BOX_BG, MUTED, ca), line_h=30)
            yb += 14

    ak = _fade(t, 72.0, 0.7)
    draw.rounded_rectangle([120, 865, 1800, 968], radius=12,
                           fill=_lerp_c(BG, (16, 44, 38), ak),
                           outline=_lerp_c(BG, GREEN, ak), width=2)
    draw.text((160, 886), "KEY INSIGHT:", fill=_lerp_c(BG, GREEN, ak), font=F22B)
    draw.text((345, 886), "For an eigenvector, A v = λ v means:", fill=_lerp_c(BG, WHITE, ak), font=F22)
    draw.text((345, 922), "No rotation — just scaling! Direction is completely preserved.",
              fill=_lerp_c(BG, GOLD, ak), font=F22B)

# ─── SCENE 3: Visual Intuition ────────────────────────────────────────────────
def _scene3(img, draw, t):
    _header(draw, "Scene 3: Visual Intuition — Invariant Directions in 2D", 3, "Visual Intuition")

    vx0, vy0, vx1, vy1 = 50, 122, 1130, 968
    pw, ph = vx1 - vx0, vy1 - vy0
    plot_img = Image.new("RGB", (pw, ph), PLOT_BG)
    pd = ImageDraw.Draw(plot_img)

    ox, oy = pw // 2, ph // 2 + 20
    sc = 66.0
    wt = _ease_io((t - 96.0) / 10.0)
    M = (1 - wt) * np.eye(2) + wt * np.array([[2.0, 1.0], [1.0, 2.0]])

    for i in range(-6, 7):
        p1 = M @ np.array([float(i), 6.0]) * sc
        p2 = M @ np.array([float(i), -6.0]) * sc
        pd.line([(ox + p1[0], oy - p1[1]), (ox + p2[0], oy - p2[1])], fill=GRID_C, width=1)
        p3 = M @ np.array([-6.0, float(i)]) * sc
        p4 = M @ np.array([6.0, float(i)]) * sc
        pd.line([(ox + p3[0], oy - p3[1]), (ox + p4[0], oy - p4[1])], fill=GRID_C, width=1)

    # Dashed eigen-span lines
    _dash(pd, (ox - 6 * sc, oy + 6 * sc), (ox + 6 * sc, oy - 6 * sc), (14, 105, 72), lw=2)
    _dash(pd, (ox - 6 * sc, oy - 6 * sc), (ox + 6 * sc, oy + 6 * sc), (16, 75, 118), lw=2)

    for d in [(-6.5, 0), (6.5, 0), (0, -6.5), (0, 6.5)]:
        p = M @ np.array(d) * sc
        pd.line([(ox, oy), (ox + p[0], oy - p[1])], fill=AXIS_C, width=2)

    # Dashed original span for orange vector
    _dash(pd, (ox, oy), (ox + 3.0 * sc, oy - 6.0 * sc), (90, 55, 28), lw=1)
    wt_v = M @ np.array([1.0, 2.0]) * sc
    _vec(pd, ox, oy, wt_v[0], wt_v[1], ORANGE, lw=5, lbl="v (orange)", pw=pw, ph=ph)

    if t >= 111.0:
        v1 = M @ np.array([1.0, 1.0]) * sc
        _vec(pd, ox, oy, v1[0], v1[1], GREEN, lw=6, lbl="v1 (green, λ=3)", pw=pw, ph=ph)

    if t >= 130.0:
        v2 = M @ np.array([1.0, -1.0]) * sc
        _vec(pd, ox, oy, v2[0], v2[1], BLUE, lw=6, lbl="v2 (blue, λ=1)", pw=pw, ph=ph)

    pd.ellipse([ox - 6, oy - 6, ox + 6, oy + 6], fill=WHITE)
    pd.rounded_rectangle([24, 22, 390, 62], radius=8, fill=(13, 18, 28), outline=BOX_BORDER, width=1)
    pd.text((40, 32), "MATRIX  A = [[2, 1], [1, 2]]", fill=GOLD, font=F18B)

    img.paste(plot_img, (vx0, vy0))
    draw.rounded_rectangle([vx0, vy0, vx1, vy1], radius=14, outline=BOX_BORDER, width=2)

    # Right panel
    px0, py0, px1, py1 = 1160, 122, 1870, 968
    draw.rounded_rectangle([px0, py0, px1, py1], radius=14, fill=BOX_BG, outline=BOX_BORDER, width=2)
    pad = 28
    ix = px0 + pad
    iw = (px1 - px0) - 2 * pad

    draw.text((ix, py0 + 24), "TRANSFORMATION ANALYSIS", fill=GOLD, font=F22B)
    draw.text((ix, py0 + 56), "A = [[2, 1],  [1, 2]]", fill=WHITE, font=F22M)
    draw.line([(ix, py0 + 96), (ix + iw, py0 + 96)], fill=BOX_BORDER, width=1)

    # Card 1: Orange vector
    c1y0, c1y1 = py0 + 114, py0 + 286
    draw.rounded_rectangle([ix, c1y0, ix + iw, c1y1], radius=10, fill=(38, 22, 14), outline=ORANGE, width=2)
    draw.text((ix + 20, c1y0 + 16), "Orange Vector  v = [1, 2]^T", fill=ORANGE, font=F22B)
    draw.text((ix + 20, c1y0 + 52), "A·v = [4, 5]^T", fill=WHITE, font=F22M)
    draw.text((ix + 20, c1y0 + 88), "• Angle changes  →  NOT an eigenvector", fill=RED, font=F20B)
    draw.text((ix + 20, c1y0 + 122), "✕ Rotates off its original span line", fill=RED, font=F20)

    # Card 2: Green eigenvector
    c2y0, c2y1 = py0 + 306, py0 + 518
    is_v1 = (t >= 111.0)
    a_v1 = _fade(t, 111.0, 0.6) if is_v1 else 0.0
    col1 = _lerp_c(DIM, GREEN, a_v1) if is_v1 else DIM
    draw.rounded_rectangle([ix, c2y0, ix + iw, c2y1], radius=10,
                           fill=_lerp_c((24, 30, 44), (16, 46, 40), a_v1),
                           outline=_lerp_c(BOX_BORDER, GREEN, a_v1), width=2 if is_v1 else 1)
    draw.text((ix + 20, c2y0 + 16), "Green  v1 = [1, 1]^T   (along y = x)", fill=col1, font=F22B)
    draw.text((ix + 20, c2y0 + 54), "A·v1 = [3, 3]^T = 3·[1, 1]^T", fill=_lerp_c(DIM, WHITE, a_v1), font=F22M)
    draw.text((ix + 20, c2y0 + 92), "✓ Stays on span!  Stretches 3×", fill=col1, font=F20B)
    draw.text((ix + 20, c2y0 + 126), "✓ Eigenvalue  λ₁ = 3", fill=_lerp_c(DIM, GOLD, a_v1), font=F20B)
    draw.text((ix + 20, c2y0 + 162), "(Zero rotation — purely scales!)", fill=MUTED, font=F18)

    # Card 3: Blue eigenvector
    c3y0, c3y1 = py0 + 538, py0 + 750
    is_v2 = (t >= 130.0)
    a_v2 = _fade(t, 130.0, 0.6) if is_v2 else 0.0
    col2 = _lerp_c(DIM, BLUE, a_v2) if is_v2 else DIM
    draw.rounded_rectangle([ix, c3y0, ix + iw, c3y1], radius=10,
                           fill=_lerp_c((24, 30, 44), (16, 32, 54), a_v2),
                           outline=_lerp_c(BOX_BORDER, BLUE, a_v2), width=2 if is_v2 else 1)
    draw.text((ix + 20, c3y0 + 16), "Blue  v2 = [1, -1]^T   (along y = -x)", fill=col2, font=F22B)
    draw.text((ix + 20, c3y0 + 54), "A·v2 = [1, -1]^T = 1·[1, -1]^T", fill=_lerp_c(DIM, WHITE, a_v2), font=F22M)
    draw.text((ix + 20, c3y0 + 92), "✓ Stays on span!  Length unchanged", fill=col2, font=F20B)
    draw.text((ix + 20, c3y0 + 126), "✓ Eigenvalue  λ₂ = 1", fill=_lerp_c(DIM, GOLD, a_v2), font=F20B)
    draw.text((ix + 20, c3y0 + 162), "(Perfectly invariant — 1× scaling!)", fill=MUTED, font=F18)

    _wrap_text(draw, "v1 and v2 are orthogonal — together they form an eigenbasis for R².",
               ix, py0 + 772, iw, F18, MUTED, line_h=26)

# ─── SCENE 4: Worked Example ──────────────────────────────────────────────────
def _scene4(img, draw, t):
    _header(draw, "Scene 4: Algebraic Derivation — Characteristic Equation", 4, "Worked Example")

    lb0, lb1, lb2, lb3 = 50, 122, 945, 968
    rb0, rb1, rb2, rb3 = 975, 122, 1870, 968
    draw.rounded_rectangle([lb0, lb1, lb2, lb3], radius=14, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.rounded_rectangle([rb0, rb1, rb2, rb3], radius=14, fill=BOX_BG, outline=BOX_BORDER, width=2)

    # ── LEFT: Eigenvalues ──
    pad = 32
    lx = lb0 + pad
    lxm = lb2 - pad
    draw.text((lx, lb1 + 22), "PART 1: FIND EIGENVALUES (λ)", fill=GOLD, font=F24B)
    draw.line([(lx, lb1 + 64), (lxm, lb1 + 64)], fill=BOX_BORDER, width=1)

    steps_l = [
        (152.3, lb1 +  80, WHITE, F22B, "1. Given matrix:"),
        (152.3, lb1 + 112, GOLD,  F22M, "   A = [[2, 1], [1, 2]]"),
        (160.0, lb1 + 156, WHITE, F22B, "2. Eigenvalue equation:"),
        (160.0, lb1 + 188, WHITE, F22M, "   A v = λ v   →   (A - λI) v = 0"),
        (170.0, lb1 + 232, WHITE, F22B, "3. For non-zero v, require singularity:"),
        (170.0, lb1 + 264, GREEN, F22M, "   det(A - λI) = 0"),
        (182.0, lb1 + 308, WHITE, F22B, "4. Compute determinant:"),
        (182.0, lb1 + 340, WHITE, F20M, "   | 2-λ    1  |"),
        (182.0, lb1 + 368, WHITE, F20M, "   |  1    2-λ | = 0"),
        (194.0, lb1 + 402, MUTED, F20M, "   (2-λ)² - 1 = 0"),
        (194.0, lb1 + 432, MUTED, F20M, "   4 - 4λ + λ² - 1 = 0"),
        (206.0, lb1 + 468, WHITE, F22M, "   λ² - 4λ + 3 = 0"),
        (214.0, lb1 + 504, GOLD,  F22M, "   (λ - 3)(λ - 1) = 0"),
    ]
    for st, y, col, fnt, txt in steps_l:
        a = _fade(t, st, 0.5)
        _safe_line(draw, txt, lx, y, lxm, fnt, _lerp_c(BOX_BG, col, a))

    ae = _fade(t, 222.0, 0.6)
    ec0, ec1 = lb1 + 560, lb3 - 32
    draw.rounded_rectangle([lx, ec0, lxm, ec1], radius=10,
                           fill=_lerp_c(BOX_BG, (16, 46, 40), ae),
                           outline=_lerp_c(BOX_BORDER, GREEN, ae), width=2)
    draw.text((lx + 24, ec0 + 22),  "EIGENVALUES FOUND:", fill=_lerp_c(BOX_BG, GREEN, ae), font=F22B)
    draw.text((lx + 24, ec0 + 68),  "λ₁ = 3", fill=_lerp_c(BOX_BG, WHITE, ae), font=F36B)
    draw.text((lx + 24, ec0 + 122), "λ₂ = 1", fill=_lerp_c(BOX_BG, WHITE, ae), font=F36B)
    draw.text((lx + 24, ec0 + 188), "Distinct real eigenvalues → orthogonal eigenbasis!",
              fill=_lerp_c(BOX_BG, MUTED, ae), font=F18)

    # ── RIGHT: Eigenvectors ──
    rx = rb0 + pad
    rxm = rb2 - pad
    draw.text((rx, rb1 + 22), "PART 2: FIND EIGENVECTORS (v)", fill=BLUE, font=F24B)
    draw.line([(rx, rb1 + 64), (rxm, rb1 + 64)], fill=BOX_BORDER, width=1)

    # Case A: λ=3
    is_c1 = (t >= 235.0)
    ac1 = _fade(t, 235.0, 0.6) if is_c1 else 0.0
    ca0, ca1 = rb1 + 82, rb1 + 408
    draw.rounded_rectangle([rx, ca0, rxm, ca1], radius=10,
                           fill=_lerp_c((24, 30, 44), (18, 42, 34), ac1),
                           outline=_lerp_c(BOX_BORDER, GREEN, ac1), width=2 if is_c1 else 1)
    fc1 = _lerp_c(DIM, GREEN, ac1)
    wc1 = _lerp_c(DIM, WHITE, ac1)
    gc1 = _lerp_c(DIM, GOLD, ac1)
    mc1 = _lerp_c(DIM, MUTED, ac1)
    _safe_line(draw, "Case A:  λ₁ = 3",                      rx + 22, ca0 + 16, rxm - 18, F22B, fc1)
    _safe_line(draw, "(A - 3I) v = 0   →   [[-1, 1],[1, -1]] · v = 0", rx + 22, ca0 + 52, rxm - 18, F20M, wc1)
    _safe_line(draw, "-x + y = 0   →   y = x",               rx + 22, ca0 + 88, rxm - 18, F22M, gc1)
    _safe_line(draw, "Eigenvector:   v1 = [1, 1]^T",         rx + 22, ca0 + 128, rxm - 18, F22B, fc1)
    _safe_line(draw, "Verify:  A·[1, 1]^T = [3, 3]^T = 3·[1, 1]^T  ✓", rx + 22, ca0 + 168, rxm - 18, F20, mc1)
    _safe_line(draw, "Stretches 3× along y = x (stays on span line)", rx + 22, ca0 + 202, rxm - 18, F18, mc1)
    if is_c1:
        draw.rounded_rectangle([rx + 22, ca0 + 244, rxm - 22, ca0 + 298],
                               radius=8, fill=(12, 58, 42), outline=GREEN, width=1)
        draw.text((rx + 40, ca0 + 258), "λ₁ = 3   →   Stretches 3× along y = x", fill=GREEN, font=F22B)

    # Case B: λ=1
    is_c2 = (t >= 250.0)
    ac2 = _fade(t, 250.0, 0.6) if is_c2 else 0.0
    cb0, cb1 = rb1 + 426, rb1 + 742
    draw.rounded_rectangle([rx, cb0, rxm, cb1], radius=10,
                           fill=_lerp_c((24, 30, 44), (16, 32, 54), ac2),
                           outline=_lerp_c(BOX_BORDER, BLUE, ac2), width=2 if is_c2 else 1)
    fc2 = _lerp_c(DIM, BLUE, ac2)
    wc2 = _lerp_c(DIM, WHITE, ac2)
    gc2 = _lerp_c(DIM, GOLD, ac2)
    mc2 = _lerp_c(DIM, MUTED, ac2)
    _safe_line(draw, "Case B:  λ₂ = 1",                      rx + 22, cb0 + 16, rxm - 18, F22B, fc2)
    _safe_line(draw, "(A - 1I) v = 0   →   [[1, 1],[1, 1]] · v = 0", rx + 22, cb0 + 52, rxm - 18, F20M, wc2)
    _safe_line(draw, "x + y = 0   →   y = -x",               rx + 22, cb0 + 88, rxm - 18, F22M, gc2)
    _safe_line(draw, "Eigenvector:   v2 = [1, -1]^T",        rx + 22, cb0 + 128, rxm - 18, F22B, fc2)
    _safe_line(draw, "Verify:  A·[1, -1]^T = [1, -1]^T = 1·[1, -1]^T  ✓", rx + 22, cb0 + 168, rxm - 18, F20, mc2)
    _safe_line(draw, "Length unchanged along y = -x",        rx + 22, cb0 + 202, rxm - 18, F18, mc2)
    if is_c2:
        draw.rounded_rectangle([rx + 22, cb0 + 244, rxm - 22, cb0 + 298],
                               radius=8, fill=(12, 34, 64), outline=BLUE, width=1)
        draw.text((rx + 40, cb0 + 258), "λ₂ = 1   →   Invariant (1×) along y = -x", fill=BLUE, font=F22B)

    sb0, sb1 = rb1 + 760, rb3 - 26
    draw.rounded_rectangle([rx, sb0, rxm, sb1], radius=8, fill=(22, 29, 44), outline=GOLD, width=1)
    draw.text((rx + 20, sb0 + 14), "Eigenpairs:  (3, [1, 1]^T)  and  (1, [1, -1]^T)", fill=GOLD, font=F20B)

# ─── SCENE 5: Geometric Interpretation & Applications ────────────────────────
def _scene5(img, draw, t):
    _header(draw, "Scene 5: Geometric Interpretation & Real-World Applications", 5, "Applications")

    # Left panel
    lb0, lb1, lb2, lb3 = 50, 122, 920, 968
    draw.rounded_rectangle([lb0, lb1, lb2, lb3], radius=14, fill=BOX_BG, outline=BOX_BORDER, width=2)
    pad = 30
    lx = lb0 + pad
    lxm = lb2 - pad
    lw = lxm - lx

    draw.text((lx, lb1 + 24), "GEOMETRIC DECOUPLING", fill=GOLD, font=F24B)
    draw.line([(lx, lb1 + 64), (lxm, lb1 + 64)], fill=BOX_BORDER, width=1)

    # Clipped mini 2D diagram inside [lx, lb1+82, lxm, lb1+470]
    mx0, my0, mx1, my1 = lx, lb1 + 82, lxm, lb1 + 470
    mw, mh = mx1 - mx0, my1 - my0
    mimg = Image.new("RGB", (mw, mh), PLOT_BG)
    md = ImageDraw.Draw(mimg)
    mox, moy = mw // 2 - 40, mh // 2 + 20
    sc = 48.0
    for gx in range(-6, 7):
        md.line([(mox + gx * sc, 0), (mox + gx * sc, mh)], fill=GRID_C, width=1)
        md.line([(0, moy + gx * sc), (mw, moy + gx * sc)], fill=GRID_C, width=1)
    _dash(md, (mox - 4 * sc, moy + 4 * sc), (mox + 4 * sc, moy - 4 * sc), (14, 105, 72), lw=2)
    _dash(md, (mox - 4 * sc, moy - 4 * sc), (mox + 4 * sc, moy + 4 * sc), (16, 75, 118), lw=2)

    anim = np.sin((t - 263.9) * 0.9) * 0.5 + 0.5
    l1 = (1.0 + 2.0 * anim) * sc
    _vec(md, mox, moy, l1, l1, GREEN, lw=6, lbl="v1 (3×)", pw=mw, ph=mh)
    _vec(md, mox, moy, sc, -sc, BLUE, lw=5, lbl="v2 (1×)", pw=mw, ph=mh)
    md.ellipse([mox - 5, moy - 5, mox + 5, moy + 5], fill=WHITE)

    img.paste(mimg, (mx0, my0))
    draw.rounded_rectangle([mx0, my0, mx1, my1], radius=10, outline=BOX_BORDER, width=1)

    draw.text((lx, lb1 + 492), "What the Math Tells Us:", fill=WHITE, font=F22B)
    draw.text((lx + 12, lb1 + 530), "• y = x  direction: stretches 3×  (λ₁ = 3)", fill=GREEN, font=F22)
    draw.text((lx + 12, lb1 + 566), "• y = -x direction: length fixed (λ₂ = 1)", fill=BLUE,  font=F22)

    ic0, ic1 = lb1 + 620, lb3 - 30
    draw.rounded_rectangle([lx, ic0, lxm, ic1], radius=10, fill=(26, 35, 52), outline=GOLD, width=2)
    draw.text((lx + 24, ic0 + 20), "Profound Insight:", fill=GOLD, font=F22B)
    cy = _wrap_text(draw, "Eigenvectors DECOUPLE a complex 2D warp into independent 1D stretches along orthogonal axes!",
                    lx + 24, ic0 + 58, lw - 48, F22, WHITE, line_h=32)
    draw.text((lx + 24, cy + 12), "This is why matrix diagonalisation works.", fill=MUTED, font=F20)

    # Right panel: Applications
    rx0, ry0, rx1, ry1 = 950, 122, 1870, 968
    draw.rounded_rectangle([rx0, ry0, rx1, ry1], radius=14, fill=BOX_BG, outline=BOX_BORDER, width=2)
    rxx = rx0 + pad
    rxxm = rx1 - pad
    rw = rxxm - rxx

    draw.text((rxx, ry0 + 24), "REAL-WORLD ENGINEERING & COMPUTING", fill=GREEN, font=F24B)
    draw.line([(rxx, ry0 + 64), (rxxm, ry0 + 64)], fill=BOX_BORDER, width=1)

    apps = [
        ("1. Google PageRank", GOLD, 272.0, [
            "Models the Web as a giant hyperlink graph.",
            "Dominant eigenvector of the link matrix ranks global page importance."
        ], ry0 + 84),
        ("2. Principal Component Analysis (PCA)", BLUE, 286.0, [
            "Core dimensionality-reduction algorithm in Machine Learning.",
            "Eigenvectors of the covariance matrix find directions of maximum variance."
        ], ry0 + 332),
        ("3. Structural Vibration Analysis", ORANGE, 299.0, [
            "Civil & aerospace engineers compute natural vibration frequencies.",
            "Prevents catastrophic resonance (e.g. Tacoma Narrows Bridge)."
        ], ry0 + 580),
    ]
    for title, col, st, pts, ay0 in apps:
        aa = _fade(t, st, 0.7)
        ay1 = ay0 + 226
        draw.rounded_rectangle([rxx, ay0, rxxm, ay1], radius=12,
                               fill=_lerp_c(BOX_BG, (18, 25, 38), aa),
                               outline=_lerp_c(BOX_BORDER, col, aa), width=2)
        draw.text((rxx + 24, ay0 + 20), title, fill=_lerp_c(BOX_BG, col, aa), font=F22B)
        yp = ay0 + 62
        for pt in pts:
            yp = _wrap_text(draw, f"• {pt}", rxx + 24, yp, rw - 48, F20,
                            _lerp_c(BOX_BG, WHITE, aa), line_h=28)
            yp += 12

# ─── SCENE 6: Summary & Credits ──────────────────────────────────────────────
def _scene6(img, draw, t):
    if t < 331.0:
        _header(draw, "Scene 6: 3 Core Takeaways to Remember", 6, "Summary")

        cards = [
            ("1", "INVARIANT DIRECTIONS", GREEN, 313.5, [
                "Eigenvectors NEVER rotate under a linear transformation — they stay locked onto their own 1D span line.",
                "That span line forms the invariant eigenspace associated with the eigenvalue."
            ], 145),
            ("2", "SCALING FACTORS", GOLD, 319.0, [
                "Eigenvalues (λ) give the exact stretch, shrink, or flip factor along each eigen-direction.",
                "λ > 1 stretches  |  0 < λ < 1 shrinks  |  λ < 0 reverses direction."
            ], 415),
            ("3", "CHARACTERISTIC EQUATION", BLUE, 324.5, [
                "det(A − λI) = 0 is the fundamental algebraic pathway to find eigenvalues.",
                "It forces (A − λI) to be singular so non-zero eigenvectors v can exist."
            ], 685),
        ]
        for num, title, col, st, lines, y0 in cards:
            ca = _fade(t, st, 0.6)
            y1 = y0 + 235
            draw.rounded_rectangle([120, y0, 1800, y1], radius=14,
                                   fill=BOX_BG, outline=_lerp_c(BOX_BG, col, ca), width=2)
            draw.rounded_rectangle([160, y0 + 36, 232, y0 + 108], radius=12,
                                   fill=_lerp_c(BOX_BG, col, ca))
            _center_text(draw, num, 196, y0 + 48, F36B, BG)
            draw.text((264, y0 + 48), title, fill=_lerp_c(BOX_BG, col, ca), font=F30B)
            yl = y0 + 116
            for ln in lines:
                yl = _wrap_text(draw, ln, 264, yl, 1480, F22,
                                _lerp_c(BOX_BG, WHITE, ca), line_h=30)
                yl += 10
        return

    # ── Closing Credits Card ──
    ac = _fade(t, 331.0, 0.8)
    # Gentle fade out in final 1.2s
    if t > 338.5:
        ac *= _clamp01((339.7 - t) / 1.2)

    draw.rounded_rectangle([90, 72, WIDTH - 90, HEIGHT - 72], radius=22,
                           fill=_lerp_c(BG, (18, 24, 36), ac),
                           outline=_lerp_c(BG, BOX_BORDER, ac), width=3)

    _center_text(draw, "LINEAR ALGEBRA AND CALCULUS (M3)  •  INTERNAL ASSESSMENT",
                 WIDTH / 2.0, 124, F22B, _lerp_c(BG, GOLD, ac))
    _center_text(draw, "EIGENVALUES & EIGENVECTORS",
                 WIDTH / 2.0, 174, F44B, _lerp_c(BG, WHITE, ac))
    _center_text(draw, "Thank You for Watching!",
                 WIDTH / 2.0, 248, F26B, _lerp_c(BG, GREEN, ac))
    draw.line([(200, 306), (WIDTH - 200, 306)], fill=_lerp_c(BG, BOX_BORDER, ac), width=2)

    lx = 200
    draw.text((lx, 344), "STUDENT", fill=_lerp_c(BG, BLUE, ac), font=F22B)
    for y, lab, val in [
        (392, "Name:",   "Srikar Burgu"),
        (438, "ID:",     "E25B070605"),
        (484, "Course:", "Linear Algebra & Calculus (M3)"),
        (530, "Type:",   "10% Internal Assessment"),
        (576, "Voice:",  "Srikar Burgu (original narration)"),
    ]:
        draw.text((lx, y),       lab, fill=_lerp_c(BG, MUTED, ac), font=F22)
        draw.text((lx + 150, y), val, fill=_lerp_c(BG, WHITE, ac), font=F22B)

    rx = 980
    draw.text((rx, 344), "PRODUCTION & AI DISCLOSURE", fill=_lerp_c(BG, GOLD, ac), font=F22B)
    for y, lab, val in [
        (392, "Code:",       "Python · Pillow · NumPy · Manim"),
        (438, "Render:",     "FFmpeg 9.1  (1920×1080  30fps)"),
        (484, "Alignment:",  "Whisper.cpp transcript timing"),
        (530, "AI Tools:",   "Script & animation code assistance"),
        (576, "Storyboard:", "6-scene PDF included in submission"),
    ]:
        draw.text((rx, y),       lab, fill=_lerp_c(BG, MUTED, ac), font=F22)
        draw.text((rx + 185, y), val, fill=_lerp_c(BG, WHITE, ac), font=F22B)

    _center_text(draw, "Prepared for M3 Evaluation  •  November 2026",
                 WIDTH / 2.0, 880, F20, _lerp_c(BG, MUTED, ac))

# ─── Scene Dispatcher with Smooth Crossfade Transitions ──────────────────────
SCENES = [
    (6.5,   "title"),
    (51.3,  "s1"),
    (93.8,  "s2"),
    (152.3, "s3"),
    (263.9, "s4"),
    (313.0, "s5"),
    (331.0, "s6"),
    (999.0, "credits"),
]
TRANS_DUR = 0.65

def _render_raw(tag, t):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=BG)
    draw = ImageDraw.Draw(img)
    if tag == "title":
        _scene1(img, draw, min(t, 6.49))
    elif tag == "s1":
        _scene1(img, draw, max(t, 6.5))
    elif tag == "s2":
        _scene2(img, draw, t)
    elif tag == "s3":
        _scene3(img, draw, t)
    elif tag == "s4":
        _scene4(img, draw, t)
    elif tag == "s5":
        _scene5(img, draw, t)
    elif tag == "s6":
        _scene6(img, draw, min(t, 330.99))
    else:
        _scene6(img, draw, max(t, 331.0))
    return img

def _frame(frame_idx):
    t = frame_idx / float(FPS)

    # Identify active scene & check proximity to next boundary for crossfade
    idx = 0
    for i, (end_t, _) in enumerate(SCENES):
        if t < end_t:
            idx = i
            break

    end_t, cur_tag = SCENES[idx]
    half = TRANS_DUR / 2.0

    if idx < len(SCENES) - 1 and (end_t - half) <= t < (end_t + half):
        alpha = _ease_io((t - (end_t - half)) / TRANS_DUR)
        img_a = _render_raw(cur_tag, t)
        img_b = _render_raw(SCENES[idx + 1][1], t)
        img = Image.blend(img_a, img_b, alpha)
    elif idx > 0 and (SCENES[idx - 1][0] - half) <= t < (SCENES[idx - 1][0] + half):
        prev_end, prev_tag = SCENES[idx - 1]
        alpha = _ease_io((t - (prev_end - half)) / TRANS_DUR)
        img_a = _render_raw(prev_tag, t)
        img_b = _render_raw(cur_tag, t)
        img = Image.blend(img_a, img_b, alpha)
    else:
        img = _render_raw(cur_tag, t)

    draw = ImageDraw.Draw(img)
    _progress(draw, t)
    return img

# ─── Main Render ─────────────────────────────────────────────────────────────
def main():
    print(f"Rendering {TOTAL_FRAMES} frames ({TOTAL_SECONDS:.2f}s @ {FPS} fps) -> '{OUTPUT_VIDEO}'")

    print("Building ambient pad...")
    amb_cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-f", "lavfi", "-i", "sine=frequency=110:duration=350",
        "-f", "lavfi", "-i", "sine=frequency=165:duration=350",
        "-f", "lavfi", "-i", "sine=frequency=220:duration=350",
        "-filter_complex",
        "[0:a][1:a][2:a]amix=inputs=3,lowpass=f=280,volume=0.025[ao]",
        "-map", "[ao]", "/tmp/ambient_pad.wav",
    ]
    subprocess.run(amb_cmd, stderr=subprocess.DEVNULL, check=True)

    print("Mixing audio...")
    mix_cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-i", AUDIO_SRC,
        "-i", "/tmp/ambient_pad.wav",
        "-filter_complex",
        "[0:a]volume=1.25,highpass=f=80,lowpass=f=8000[v];[1:a]volume=0.03[m];[v][m]amix=inputs=2:duration=first[ao]",
        "-map", "[ao]", "/tmp/final_audio.wav",
    ]
    subprocess.run(mix_cmd, stderr=subprocess.DEVNULL, check=True)

    ffmpeg_cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-",
        "-i", "/tmp/final_audio.wav",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO,
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    for fi in range(TOTAL_FRAMES):
        proc.stdin.write(_frame(fi).tobytes())
        if fi % 300 == 0:
            pct = fi / TOTAL_FRAMES * 100.0
            print(f"  {fi:5d}/{TOTAL_FRAMES}  ({pct:5.1f}%)  t={fi / FPS:.1f}s")

    proc.stdin.close()
    proc.wait()
    print(f"\nDone! -> '{OUTPUT_VIDEO}'")

if __name__ == "__main__":
    main()
