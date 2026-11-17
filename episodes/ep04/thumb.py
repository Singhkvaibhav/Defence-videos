import sys, math, cairo
sys.path.insert(0, '../..')
from engine import core
from engine.bp import B, bg, txt, stroke_pts, bez, missile, glow_dot, rgba, rrect, radar
from engine.shield import ring, protected
W, H = 1920, 1080
AMB, CY, WH, RED = B['amber'], B['cyan'], (1, 1, 1), (0.95, 0.26, 0.22)

def big(ctx, s, x, y, size, col, align='l', stroke=16, rot=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s); dx = -e.x_advance/2 if align == 'c' else (-e.x_advance if align == 'r' else 0)
    ctx.move_to(dx + 9, 11); ctx.text_path(s); ctx.set_source_rgba(0, 0, 0, .6); ctx.fill()
    ctx.move_to(dx, 0); ctx.text_path(s); ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(stroke); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    ctx.set_source_rgb(*col); ctx.fill(); ctx.restore()

def burst(ctx, x, y, r, col, a=1.):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 1, .95, .8, a); g.add_color_stop_rgba(.25, col[0], col[1], col[2], .8*a); g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    ctx.set_source(g); ctx.arc(x, y, r, 0, 2*math.pi); ctx.fill()

def tagbox(ctx, s, x, y, col, size=42):
    ctx.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s); w, h = e.x_advance + 46, size*1.6
    rgba(ctx, (0.03, 0.07, 0.12), .92); rrect(ctx, x, y - h/2, w, h, 10); ctx.fill()
    rgba(ctx, col); ctx.set_line_width(6); rrect(ctx, x, y - h/2, w, h, 10); ctx.stroke()
    ctx.move_to(x + 23, y + size*.35); ctx.show_text(s)

def base(ctx, vign=.6, fx=.62, fy=.42):
    bg(ctx)
    v = cairo.RadialGradient(W*fx, H*fy, 200, W/2, H/2, 1250); v.add_color_stop_rgba(0, 0, 0, 0, 0); v.add_color_stop_rgba(1, 0, 0, 0, vign)
    ctx.set_source(v); ctx.paint()

# ---- A: the rings
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); base(c, .5, .72, .55)
burst(c, 1330, 640, 480, (1, .7, .2), .5)
for i, (r, col) in enumerate(((700, AMB), (520, CY), (350, CY), (190, B['steel']))):
    ring(c, 1330, 660, r, 1, col, .95, 6, None, 0, None, .55)
protected(c, 1330, 660, 1)
for ang in (-2.5, -2.1, -1.7):
    stroke_pts(c, bez((1330 + 820*math.cos(ang), 660 + 520*math.sin(ang)), (1330 + 400*math.cos(ang), 660 + 300*math.sin(ang)), (1330, 640), 24), 1, RED, .9, 5)
big(c, 'NOT A', 70, 300, 130, WH)
big(c, 'DOME.', 70, 450, 190, WH)
big(c, 'RINGS.', 70, 630, 200, AMB)
c.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
tagbox(c, "INDIA'S MISSILE SHIELD", 75, 780, CY, 46)
tagbox(c, 'S-400 · KUSHA · SUDARSHAN CHAKRA', 75, 880, AMB, 34)
txt(c, 'GyaanXstudios', W - 80, H - 56, 38, WH, 1, 'black', 'r')
s.write_to_png('Def04_thumb.png')

# ---- B: the thing nobody names
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); base(c, .72)
burst(c, 1420, 500, 430, (.5, .83, .94), .45)
for i, x in enumerate((1120, 1420, 1720)):
    rgba(c, (0.03, 0.07, 0.12), .95); rrect(c, x - 130, 400, 260, 130, 12); c.fill()
    rgba(c, AMB if i == 1 else CY); c.set_line_width(6); rrect(c, x - 130, 400, 260, 130, 12); c.stroke()
    txt(c, ('IACCS', 'AKASHTEER', 'TRIGUN')[i], x, 480, 34, B['ice'], 1, 'black', 'c')
for a, b_ in ((1120, 1420), (1420, 1720)):
    stroke_pts(c, bez((a, 530), ((a + b_)/2, 640), (b_, 530), 24), 1, CY, .85, 5)
for k in range(14):
    glow_dot(c, 1000 + k*62, 700 + (k % 3)*52, 7, CY, .8)
big(c, 'THE PART', 70, 300, 140, WH)
big(c, 'NOBODY', 70, 460, 170, WH)
big(c, 'NAMES', 70, 630, 190, AMB)
c.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
tagbox(c, 'IT IS NOT A MISSILE', 75, 780, RED, 46)
tagbox(c, "INDIA'S AIR DEFENCE, EXPLAINED", 75, 880, CY, 34)
txt(c, 'GyaanXstudios', W - 80, H - 56, 38, WH, 1, 'black', 'r')
s.write_to_png('Def04_thumb_B.png')
print('ok')
