import sys, math, cairo
sys.path.insert(0, '../..')
from engine import core
from engine.bp import B, bg, stroke_pts, bez, missile, glow_dot, rgba, rrect
W, H = 1920, 1080

def big(ctx, s, x, y, size, col, rot=0, align='l', stroke=14):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s); dx = -e.x_advance/2 if align == 'c' else 0
    ctx.move_to(dx + 8, 10); ctx.text_path(s); ctx.set_source_rgba(0, 0, 0, .55); ctx.fill()          # drop shadow
    ctx.move_to(dx, 0); ctx.text_path(s); ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(stroke); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    ctx.set_source_rgb(*col); ctx.fill(); ctx.restore()

def burst(ctx, x, y, r, col, a=1.):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 1, .95, .8, a); g.add_color_stop_rgba(.25, col[0], col[1], col[2], .85*a); g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    ctx.set_source(g); ctx.arc(x, y, r, 0, 2*math.pi); ctx.fill()

def arrow(ctx, x0, y0, x1, y1, col, w=34):
    ang = math.atan2(y1 - y0, x1 - x0); L = math.hypot(x1 - x0, y1 - y0)
    ctx.save(); ctx.translate(x0, y0); ctx.rotate(ang)
    def shape():
        ctx.move_to(0, -w/2); ctx.line_to(L - 90, -w/2); ctx.line_to(L - 90, -w*1.6); ctx.line_to(L, 0)
        ctx.line_to(L - 90, w*1.6); ctx.line_to(L - 90, w/2); ctx.line_to(0, w/2); ctx.close_path()
    shape(); ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(12); ctx.stroke_preserve(); ctx.set_source_rgb(*col); ctx.fill()
    ctx.restore()

def stamp(ctx, s, x, y, rot, col, size=70):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s); w, h = e.x_advance + 60, size*1.5
    rgba(ctx, col, 1); ctx.set_line_width(10); rrect(ctx, -w/2, -h/2, w, h, 12); ctx.stroke()
    ctx.move_to(-e.x_advance/2, size*.36); ctx.show_text(s); ctx.restore()

def base(ctx, vign=.65):
    bg(ctx)
    v = cairo.RadialGradient(W*.62, H*.45, 200, W/2, H/2, 1250); v.add_color_stop_rgba(0, 0, 0, 0, 0); v.add_color_stop_rgba(1, 0, 0, 0, vign)
    ctx.set_source(v); ctx.paint()

RED, YEL, WHITE = (0.95, 0.2, 0.18), (1.0, 0.82, 0.1), (1, 1, 1)

# --- A: the missile that fools radar
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); base(c)
pred = bez((1300, 330), (1650, 300), (1880, 900), 20)
stroke_pts(c, pred, 1, RED, 1, 8, glow=False, dash=[26, 20])
c.save(); c.translate(1880, 900); rgba(c, RED); c.set_line_width(16)
for d in (-1, 1): c.move_to(-40, -40*d); c.line_to(40, 40*d)
c.stroke(); c.restore()
real = bez((700, 1100), (950, 300), (1300, 330), 40) + bez((1300, 330), (1420, 340), (1500, 1000), 25)[1:]
stroke_pts(c, real, 1, YEL, 1, 16)
burst(c, 1300, 330, 260, (1, .6, .1), .9)
missile(c, 1390, 520, 420, 1.35, 1, col=WHITE, fill_a=.5)
arrow(c, 980, 140, 1250, 280, YEL)
big(c, 'RADAR', 70, 330, 250, WHITE)
big(c, 'FOOLED?', 70, 600, 250, YEL)
stamp(c, 'PREDICTION ✗', 1580, 770, -.12, RED, 64)
big(c, 'PRALAY', 80, 820, 130, (0.5, 0.85, 0.95), stroke=10)
c.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(44); c.move_to(85, 900); c.set_source_rgb(1, 1, 1); c.show_text("INDIA'S LATE-TURNING MISSILE")
s.write_to_png('thumb_A.png')

# --- B: 500 km in minutes
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); base(c)
for k in range(9):
    y = 300 + k*70; stroke_pts(c, [(900 + k*30, y), (1900, y - 120)], 1, (0.5, 0.85, 0.95), .25, 4, glow=False)
burst(c, 1350, 420, 420, (1, .45, .1), 1)
missile(c, 1350, 420, 820, -.35, 1, col=WHITE, fill_a=.55)
big(c, '500 KM', 60, 330, 280, YEL)
big(c, 'IN MINUTES', 60, 560, 190, WHITE)
stamp(c, 'INDIA', 1640, 840, .1, YEL, 80)
big(c, 'PRALAY', 70, 820, 160, (0.5, 0.85, 0.95), stroke=12)
s.write_to_png('thumb_B.png')

# --- C: why India wants it
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); base(c, .8)
burst(c, 1450, 1080, 700, (1, .4, .05), 1)
missile(c, 1450, 560, 900, -math.pi/2, 1, col=WHITE, fill_a=.55)
for k in range(5):
    glow_dot(c, 1450 + (k - 2)*60, 1010 - abs(k - 2)*20, 18, (1, .7, .2), .9)
big(c, 'INDIA', 60, 300, 240, WHITE)
big(c, 'JUST', 60, 520, 240, WHITE)
big(c, 'GOT THIS', 60, 740, 240, YEL)
arrow(c, 980, 880, 1300, 760, RED, 40)
stamp(c, 'PRALAY', 430, 920, -.04, (0.5, 0.85, 0.95), 80)
s.write_to_png('thumb_C.png')
print('ok')
