import sys, math, cairo
sys.path.insert(0, '../..')
from engine import core
from engine.bp import B, bg, txt, stroke_pts, bez, missile, glow_dot, rgba, rrect
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

def base(ctx, vign=.6):
    bg(ctx)
    v = cairo.RadialGradient(W*.62, H*.42, 200, W/2, H/2, 1250); v.add_color_stop_rgba(0, 0, 0, 0, 0); v.add_color_stop_rgba(1, 0, 0, 0, vign)
    ctx.set_source(v); ctx.paint()

def release(c, apex=(1330, 330), ends=((900, 1010), (1430, 1040), (1850, 980))):
    up = bez((780, 1060), (1000, 620), apex, 36)
    stroke_pts(c, up, 1, AMB, .95, 7)
    for e in ends:
        stroke_pts(c, bez(apex, ((apex[0] + e[0])/2, apex[1] + 190), e, 30), 1, AMB, .95, 6)
        glow_dot(c, e[0], e[1], 15, AMB, 1)
    burst(c, apex[0], apex[1], 300, (1, .7, .2), .8)
    rgba(c, (0.03, 0.07, 0.12), .95); rrect(c, apex[0] - 86, apex[1] - 40, 172, 80, 10); c.fill()
    rgba(c, WH); c.set_line_width(6); rrect(c, apex[0] - 86, apex[1] - 40, 172, 80, 10); c.stroke()
    for k in range(3):
        glow_dot(c, apex[0] - 50 + k*50, apex[1], 12, AMB, 1)

# ---- A: one missile, several warheads
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); base(c)
release(c)
big(c, 'ONE MISSILE', 70, 300, 150, WH)
big(c, 'MANY', 70, 470, 200, AMB)
big(c, 'WARHEADS', 70, 650, 200, AMB)
c.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
tagbox(c, 'AGNI-5 · MIRV', 75, 790, CY, 46)
tagbox(c, 'WHAT INDIA ACTUALLY TESTED', 75, 890, RED, 36)
txt(c, 'GyaanXstudios', W - 80, H - 56, 38, WH, 1, 'black', 'r')
s.write_to_png('Def03_thumb.png')

# ---- B: the time angle
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); base(c, .72)
burst(c, 1430, 520, 480, (1, .6, .12), .8)
missile(c, 1430, 520, 820, -.95, 1, col=WH, fill_a=.5)
c.new_path(); rgba(c, CY, .85); c.set_line_width(10); c.arc(1430, 520, 300, -math.pi/2, -math.pi/2 + 1.1); c.stroke()
big(c, '5,000 KM', 70, 300, 180, WH)
big(c, 'IN UNDER', 70, 470, 150, WH)
big(c, '20 MINUTES', 70, 650, 190, AMB)
c.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
tagbox(c, 'A JET TAKES SIX HOURS', 75, 790, CY, 42)
tagbox(c, 'AGNI-5, EXPLAINED', 75, 890, AMB, 36)
txt(c, 'GyaanXstudios', W - 80, H - 56, 38, WH, 1, 'black', 'r')
s.write_to_png('Def03_thumb_B.png')
print('ok')
