import sys, math, cairo
sys.path.insert(0, '../..'); sys.path.insert(0, '.')
from engine import core
from engine.bp import B, bg, txt, stroke_pts, bez, missile, glow_dot, tagb, rgba
W, H = 1920, 1080
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(s)
bg(ctx)
path = bez((980, 980), (1180, 360), (1560, 400), 40) + bez((1560, 400), (1700, 420), (1820, 900), 25)[1:]
stroke_pts(ctx, path, 1, B['amber'], 1, 6)
pred = bez((1560, 400), (1760, 380), (1900, 700), 20)
stroke_pts(ctx, pred, 1, B['alert'], .7, 3, glow=False, dash=[14, 14])
missile(ctx, 1640, 470, 330, .9, 1)
glow_dot(ctx, 1575, 400, 10, B['amber'])
txt(ctx, "INDIA'S DEFENCE, DECODED", 110, 180, 44, B['cyan'], 1, 'bold', mono=True)
txt(ctx, 'PRALAY', 90, 470, 300, B['ice'], 1, 'black', glow=2)
txt(ctx, 'THE MISSILE THAT', 110, 600, 70, B['amber'], 1, 'black', glow=1)
txt(ctx, 'TURNS LATE', 110, 690, 70, B['amber'], 1, 'black', glow=1)
tagb(ctx, 110, 800, '150–500 KM', B['cyan'], 1, 40)
tagb(ctx, 480, 800, 'QUASI-BALLISTIC', B['cyan'], 1, 40)
txt(ctx, 'GyaanXstudios', W - 80, H - 60, 40, B['ice'], 1, 'black', 'r')
s.write_to_png('Def01_thumb.png'); print('ok')
