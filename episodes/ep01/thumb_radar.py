import sys, math, cairo
sys.path.insert(0, '../..')
from engine import core
from engine.bp import B, bg, stroke_pts, bez, missile, glow_dot, rgba, rrect, radar
W, H = 1920, 1080
RED, YEL, WHITE, CY = (0.95, 0.2, 0.18), (1.0, 0.82, 0.1), (1, 1, 1), (0.5, 0.85, 0.95)

def big(ctx, s, x, y, size, col, rot=0, align='l', stroke=16):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s); dx = -e.x_advance/2 if align == 'c' else (-e.x_advance if align == 'r' else 0)
    ctx.move_to(dx + 9, 11); ctx.text_path(s); ctx.set_source_rgba(0, 0, 0, .6); ctx.fill()
    ctx.move_to(dx, 0); ctx.text_path(s); ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(stroke); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    ctx.set_source_rgb(*col); ctx.fill(); ctx.restore()
    return e.x_advance

def burst(ctx, x, y, r, col, a=1.):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 1, .95, .8, a); g.add_color_stop_rgba(.25, col[0], col[1], col[2], .85*a); g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    ctx.set_source(g); ctx.arc(x, y, r, 0, 2*math.pi); ctx.fill()

def cross(ctx, x, y, s, col, w=18):
    rgba(ctx, col); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(x - s, y - s); ctx.line_to(x + s, y + s); ctx.move_to(x + s, y - s); ctx.line_to(x - s, y + s); ctx.stroke()

def stamp(ctx, s, x, y, rot, col, size=62):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s); w, h = e.x_advance + 56, size*1.5
    rgba(ctx, (0, 0, 0), .55); rrect(ctx, -w/2 + 6, -h/2 + 6, w, h, 12); ctx.fill()
    rgba(ctx, (0.06, 0.10, 0.16), .92); rrect(ctx, -w/2, -h/2, w, h, 12); ctx.fill()
    rgba(ctx, col); ctx.set_line_width(9); rrect(ctx, -w/2, -h/2, w, h, 12); ctx.stroke()
    ctx.move_to(-e.x_advance/2, size*.36); ctx.show_text(s); ctx.restore()

def base(ctx, vx=.62, vy=.45, vign=.68):
    bg(ctx)
    v = cairo.RadialGradient(W*vx, H*vy, 200, W/2, H/2, 1250)
    v.add_color_stop_rgba(0, 0, 0, 0, 0); v.add_color_stop_rgba(1, 0, 0, 0, vign)
    ctx.set_source(v); ctx.paint()

def tag(ctx, s, x, y, col=CY, size=40):
    ctx.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s); w, h = e.x_advance + 44, size*1.6
    rgba(ctx, (0.06, 0.10, 0.16), .9); rrect(ctx, x, y - h/2, w, h, 10); ctx.fill()
    rgba(ctx, col); ctx.set_line_width(6); rrect(ctx, x, y - h/2, w, h, 10); ctx.stroke()
    ctx.move_to(x + 22, y + size*.35); ctx.show_text(s)

# ---------------- A1: text left, divergence right ----------------
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); base(c, .68, .40)
TURN = (1270, 340)
real = bez((760, 1120), (990, 330), TURN, 40) + bez(TURN, (1390, 350), (1470, 1040), 26)[1:]
pred = bez(TURN, (1650, 300), (1900, 880), 22)
stroke_pts(c, pred, 1, RED, 1, 9, glow=False, dash=[28, 22])
cross(c, 1890, 880, 44, RED, 20)
stroke_pts(c, real, 1, YEL, 1, 17)
burst(c, TURN[0], TURN[1], 250, (1, .6, .12), .95)
missile(c, 1360, 520, 430, 1.33, 1, col=WHITE, fill_a=.55)
radar(c, 1700, 1040, 1.5, 1, 0.6, aim=-1.0)
big(c, 'IT LIES', 70, 400, 265, WHITE)
big(c, 'TO RADAR', 70, 660, 265, YEL)
stamp(c, 'PREDICTED ✗', 1620, 700, -.13, RED, 58)
tag(c, 'PRALAY', 80, 840)
s.write_to_png('radar_1.png')

# ---------------- A2: text across top, wide trajectory below ----------------
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); base(c, .5, .68)
TURN = (1120, 620)
real = bez((180, 1080), (560, 600), TURN, 40) + bez(TURN, (1260, 640), (1340, 1060), 26)[1:]
pred = bez(TURN, (1560, 600), (1860, 1020), 22)
stroke_pts(c, pred, 1, RED, 1, 9, glow=False, dash=[28, 22])
cross(c, 1850, 1020, 40, RED, 18)
stroke_pts(c, real, 1, YEL, 1, 17)
burst(c, TURN[0], TURN[1], 230, (1, .6, .12), .95)
missile(c, 1210, 760, 380, 1.3, 1, col=WHITE, fill_a=.55)
big(c, 'THIS MISSILE', W/2, 300, 190, WHITE, align='c')
big(c, 'LIES TO RADAR', W/2, 500, 210, YEL, align='c')
stamp(c, 'PREDICTED ✗', 1600, 790, -.1, RED, 54)
tag(c, 'PRALAY · 150–500 KM', 90, 1000)
s.write_to_png('radar_2.png')

# ---------------- A3: split — radar view vs reality ----------------
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); base(c, .5, .5, .5)
rgba(c, (0.5, 0.85, 0.95), .30); c.set_line_width(5); c.move_to(W/2, 170); c.line_to(W/2, 890); c.stroke()
# left: what radar expects
pr = bez((170, 860), (480, 330), (790, 860), 40)
stroke_pts(c, pr, 1, RED, .95, 11, glow=False, dash=[26, 20])
cross(c, 790, 860, 34, RED, 16)
radar(c, 290, 870, 1.0, 1, 0.4, aim=-.8)
# right: what it does
TURN = (1390, 400)
rl = bez((1060, 870), (1220, 400), TURN, 40) + bez(TURN, (1510, 425), (1560, 870), 26)[1:]
stroke_pts(c, rl, 1, YEL, 1, 15)
burst(c, TURN[0], TURN[1], 200, (1, .6, .12), .95)
missile(c, 1468, 560, 330, 1.3, 1, col=WHITE, fill_a=.55)
big(c, 'RADAR SEES', 480, 290, 94, RED, align='c', stroke=12)
big(c, 'WHAT IT DOES', 1440, 290, 94, YEL, align='c', stroke=12)
rgba(c, (0.03, 0.06, 0.11), .92); c.rectangle(0, 900, W, 180); c.fill()
rgba(c, YEL, .9); c.rectangle(0, 900, W, 7); c.fill()
big(c, 'IT LIES TO RADAR', W/2, 1020, 130, WHITE, align='c')
s.write_to_png('radar_3.png')
print('ok')
