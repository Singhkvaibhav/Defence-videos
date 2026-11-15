import sys, math, cairo
sys.path.insert(0, '../..')
from engine import core
from engine.bp import B, bg, txt, stroke_pts, bez, missile, glow_dot, rgba, rrect
from engine.mil import waves, horizon, warship
W, H = 1920, 1080
AMB, CY, WH, RED = B['amber'], B['cyan'], (1,1,1), (0.95,0.26,0.22)

def big(ctx, s, x, y, size, col, align='l', stroke=16, rot=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s); dx = -e.x_advance/2 if align=='c' else (-e.x_advance if align=='r' else 0)
    ctx.move_to(dx+9, 11); ctx.text_path(s); ctx.set_source_rgba(0,0,0,.6); ctx.fill()
    ctx.move_to(dx, 0); ctx.text_path(s); ctx.set_source_rgb(0,0,0)
    ctx.set_line_width(stroke); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    ctx.set_source_rgb(*col); ctx.fill(); ctx.restore()

def burst(ctx, x, y, r, col, a=1.):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0,1,.95,.8,a); g.add_color_stop_rgba(.25,col[0],col[1],col[2],.8*a); g.add_color_stop_rgba(1,col[0],col[1],col[2],0)
    ctx.set_source(g); ctx.arc(x,y,r,0,2*math.pi); ctx.fill()

def tagbox(ctx, s, x, y, col, size=42):
    ctx.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s); w, h = e.x_advance+46, size*1.6
    rgba(ctx,(0.03,0.07,0.12),.92); rrect(ctx,x,y-h/2,w,h,10); ctx.fill()
    rgba(ctx,col); ctx.set_line_width(6); rrect(ctx,x,y-h/2,w,h,10); ctx.stroke()
    ctx.move_to(x+23, y+size*.35); ctx.show_text(s)

def base(ctx, vign=.6):
    bg(ctx)
    v = cairo.RadialGradient(W*.6,H*.5,200,W/2,H/2,1250); v.add_color_stop_rgba(0,0,0,0,0); v.add_color_stop_rgba(1,0,0,0,vign)
    ctx.set_source(v); ctx.paint()

# ---- A: MACH 3 at 10 metres (the sea-skim)
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); base(c)
cx, cy, r = 960, 760+2400, 2400
hp = horizon(c, cx, cy, r, 1, col=WH)
c.save(); c.new_path(); c.move_to(*hp[0])
for q in hp[1:]: c.line_to(*q)
c.line_to(W+200,H+100); c.line_to(-200,H+100); c.close_path(); rgba(c,CY,.07); c.fill(); c.restore()
waves(c, 880, 1.2, .8)
stroke_pts(c, [(1860,620),(760,430)], 1, RED, .9, 5, glow=False, dash=[26,20])
big(c, 'RADAR HORIZON', 1840, 400, 34, RED, align='r', stroke=8)
mx = 1180; my = cy - math.sqrt(r*r-(mx-cx)**2) - 34
burst(c, mx, my, 240, (1,.6,.12), .9)
missile(c, mx, my, 520, -.06, 1, col=WH, fill_a=.5)
stroke_pts(c, [(mx-10,my+22),(mx-10,my+72)], 1, AMB, 1, 4, glow=False)
big(c, '10 M', mx-10, my+124, 46, AMB, align='c', stroke=10)
big(c, 'MACH 3', 80, 360, 240, AMB, stroke=18)
big(c, 'AT 10 METRES', 80, 530, 130, WH, stroke=14)
c.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
tagbox(c, 'BRAHMOS', 85, 650, CY, 46)
tagbox(c, 'BELOW THE RADAR HORIZON', 85, 740, RED, 36)
txt(c, 'GyaanXstudios', W-80, H-56, 38, WH, 1, 'black', 'r')
s.write_to_png('Def02_thumb.png')

# ---- B: the export angle
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); base(c, .7)
burst(c, 1420, 560, 520, (1,.55,.1), .85)
missile(c, 1420, 560, 760, -.22, 1, col=WH, fill_a=.5)
for i,(nm,x,y) in enumerate((('PHILIPPINES',1120,900),('VIETNAM',1480,880),('INDONESIA',1800,930))):
    glow_dot(c, x, y, 14, AMB, 1)
big(c, 'INDIA', 70, 300, 190, WH)
big(c, 'SELLS THIS', 70, 480, 190, AMB)
big(c, 'NOW', 70, 660, 190, WH)
tagbox(c, '3 COUNTRIES HAVE BOUGHT IT', 75, 790, CY, 40)
txt(c, 'GyaanXstudios', W-80, H-56, 38, WH, 1, 'black', 'r')
s.write_to_png('Def02_thumb_B.png')
print('ok')
