"""Scene pieces for India's Defence, Decoded Ep 5 (Tejas).

Everything here is stylised blueprint line art, never an engineering drawing:
a delta planform with no panel lines, fasteners, intake geometry or dimensions,
and a turbine shown only as the three named stages any textbook gives.
Nothing in this module draws a map, a boundary, a coastline, a flag or a likeness.
"""
import math
from engine.core import W, H, seg, ease, eoc, eob, lerp
from engine.bp import (B, rgba, rrect, txt, tw, stroke_pts, rect_pts, fill, glow_dot, bez, card, tagb)

# ---------- the aircraft ----------
_HALF = [(0, -300), (20, -245), (32, -155), (42, -70), (292, 165), (292, 200),
         (150, 200), (118, 248), (52, 262)]


def jet_pts():
    """closed delta planform, nose up — a shape, not a drawing of a specific airframe"""
    right = list(_HALF)
    left = [(-x, y) for x, y in reversed(_HALF[:-1])]
    return right + [(0, 274)] + left + [(0, -300)]


def jet(ctx, cx, cy, s, p, a, col=None, fill_a=.09, rot=0.):
    """the airframe drawing itself on, without its engine"""
    col = col or B['ice']
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    pts = jet_pts()
    if p > .92:
        fill(ctx, lambda: ([ctx.move_to(*pts[0])] + [ctx.line_to(*q) for q in pts[1:]] + [ctx.close_path()]),
             B['cyan'], fill_a*a*ease(seg(p, .92, 1)))
    stroke_pts(ctx, pts, p, col, a, 3)
    q = seg(p, .55, .9)
    if q > 0:                                     # canopy
        cp = bez((-26, -150), (0, -230), (26, -150), 24) + bez((26, -150), (0, -108), (-26, -150), 24)
        stroke_pts(ctx, cp, q, B['cyan'], a*.9, 2.5)
    q2 = seg(p, .7, 1)
    if q2 > 0:                                    # intakes, as two short strakes
        for sg in (-1, 1):
            stroke_pts(ctx, [(sg*46, -58), (sg*62, 30)], q2, B['dim'], a*.8, 2, glow=False)
    ctx.restore()


def jet_engine(ctx, cx, cy, s, a, p=1., dotted=False, col=None):
    """the nozzle at the tail: solid when fitted, a dotted ghost when it is not"""
    col = col or (B['alert'] if dotted else B['ice'])
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    body = rect_pts(-52, 262, 104, 74)
    stroke_pts(ctx, body, p, col, a, 3, dash=[9, 9] if dotted else None, glow=not dotted)
    if not dotted:
        fill(ctx, lambda: rrect(ctx, -52, 262, 104, 74, 8), B['cyan'], .12*a)
        for k in range(3):
            stroke_pts(ctx, [(-52, 282 + k*18), (52, 282 + k*18)], p, B['dim'], a*.7, 1.5, glow=False)
    ctx.restore()


# ---------- the four problems ----------
def icon_shape(ctx, x, y, s, col, a, p=1.):
    ctx.save(); ctx.translate(x, y); ctx.scale(s*.17, s*.17)
    stroke_pts(ctx, jet_pts(), p, col, a, 14)
    ctx.restore()


def icon_chip(ctx, x, y, s, col, a, p=1.):
    stroke_pts(ctx, rect_pts(x - 40*s, y - 40*s, 80*s, 80*s), p, col, a, 3)
    stroke_pts(ctx, rect_pts(x - 17*s, y - 17*s, 34*s, 34*s), seg(p, .4, 1), col, a*.85, 2.5)
    for k in range(3):
        q = seg(p, .5 + k*.1, .9 + k*.1)
        for sg in (-1, 1):
            stroke_pts(ctx, [(x + sg*40*s, y + (k - 1)*24*s), (x + sg*64*s, y + (k - 1)*24*s)], q, col, a*.8, 2.5, glow=False)
            stroke_pts(ctx, [(x + (k - 1)*24*s, y + sg*40*s), (x + (k - 1)*24*s, y + sg*64*s)], q, col, a*.8, 2.5, glow=False)


def icon_dish(ctx, x, y, s, col, a, p=1., t=0.):
    stroke_pts(ctx, bez((x - 52*s, y + 18*s), (x, y - 76*s), (x + 52*s, y + 18*s), 30), p, col, a, 3)
    stroke_pts(ctx, [(x, y + 2*s), (x, y + 48*s)], seg(p, .4, 1), col, a, 2.5, glow=False)
    stroke_pts(ctx, [(x - 34*s, y + 48*s), (x + 34*s, y + 48*s)], seg(p, .5, 1), col, a, 2.5, glow=False)
    if p > .8:
        for k in range(3):
            ph = (t*.7 + k/3) % 1
            ctx.new_path(); rgba(ctx, col, a*(1 - ph)*.6); ctx.set_line_width(2)
            ctx.arc(x, y + 10*s, (26 + 70*ph)*s, -2.5, -.65); ctx.stroke()


def icon_turbine(ctx, x, y, s, col, a, p=1., t=0., spin=True, fill_p=0.):
    """a turbine seen end-on: a hub and blades. fill_p 0..1 tints it in"""
    r = 52*s
    ctx.new_path(); rgba(ctx, col, a*min(1, p*1.4)); ctx.set_line_width(3)
    ctx.arc(x, y, r, 0, 2*math.pi*min(p*1.2, 1)); ctx.stroke()
    if fill_p > 0:
        ctx.new_path(); rgba(ctx, B['amber'], .16*a*fill_p); ctx.arc(x, y, r, 0, 2*math.pi); ctx.fill()
    ang = t*1.9 if spin else 0.
    for k in range(10):
        q = seg(p, .25 + k*.05, .6 + k*.05)
        if q <= 0: continue
        th = ang + k*2*math.pi/10
        stroke_pts(ctx, [(x + 13*s*math.cos(th), y + 13*s*math.sin(th)),
                         (x + r*.92*math.cos(th + .32), y + r*.92*math.sin(th + .32))],
                   q, col, a*.85, 2.5, glow=False)
    if p > .5: glow_dot(ctx, x, y, 8*s, col, a)


def problem(ctx, x, y, label, n, icon, col, a, p, t=0., fill_p=0.):
    icon(ctx, x, y, 1., col, a, p) if icon is not icon_turbine else icon(ctx, x, y, 1., col, a, p, t, True, fill_p)
    txt(ctx, n, x, y + 108, 22, B['dim'], a*ease(seg(p, .4, .9)), 'bold', 'c', mono=True)
    txt(ctx, label, x, y + 146, 32, col, a*ease(seg(p, .5, 1)), 'black', 'c', glow=.4)


# ---------- timelines and markers ----------
def timeline(ctx, x0, x1, y, marks, a, p=1., col=None):
    """marks: [(x_frac, year, label, prog)] printing in along a rule"""
    col = col or B['cyan']
    stroke_pts(ctx, [(x0, y), (x1, y)], p, B['grid'], a, 3, glow=False)
    for xf, year, label, q in marks:
        if q <= 0: continue
        x = lerp(x0, x1, xf)
        stroke_pts(ctx, [(x, y - 16), (x, y + 16)], min(q*2, 1), col, a, 3, glow=False)
        glow_dot(ctx, x, y, 6, col, a*ease(min(q*2, 1)))
        txt(ctx, year, x, y - 36, 30, B['ice'], a*ease(q), 'black', 'c')
        if label:
            for i, ln in enumerate(label.split('|')):
                txt(ctx, ln, x, y + 54 + i*26, 21, B['steel'], a*ease(seg(q, .3, 1)), 'bold', 'c', mono=True)


def plane_row(ctx, y, n, a, gone=0., s=.055, col=None):
    """a row of small aircraft silhouettes, fading out left to right"""
    col = col or B['steel']
    for k in range(n):
        x = 240 + k*((W - 480)/max(n - 1, 1))
        al = a*(1 - min(1, max(0, gone*n - k)))
        if al <= 0.01: continue
        ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
        stroke_pts(ctx, jet_pts(), 1, col, al, 24)
        ctx.restore()


# ---------- the engine cutaway ----------
def turbine_cut(ctx, cx, cy, s, a, stages, hot=0.):
    """a side cutaway: intake, compressor, combustor, turbine, nozzle.
    `stages` is a list of three progress values for the three named stages."""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    shell = [(-440, -92), (-330, -78), (190, -78), (300, -118), (300, 118), (190, 78), (-330, 78), (-440, 92), (-440, -92)]
    stroke_pts(ctx, shell, 1, B['ice'], a, 3)
    stroke_pts(ctx, [(-440, 0), (300, 0)], 1, B['grid'], a*.8, 2, glow=False)
    bands = [(-330, 180, 'COMPRESSOR'), (-150, 120, 'COMBUSTOR'), (-30, 170, 'TURBINE')]
    for (x0, wdt, name), q in zip(bands, stages):
        if q <= 0: continue
        fill(ctx, lambda x0=x0, wdt=wdt: ctx.rectangle(x0, -76, wdt*ease(q), 152),
             B['amber'] if name == 'COMBUSTOR' else B['cyan'], (.20 if name == 'COMBUSTOR' else .10)*a)
        stroke_pts(ctx, rect_pts(x0, -76, wdt, 152), min(q*1.6, 1), B['ice'], a*.9, 2)
        if name == 'COMPRESSOR':
            for k in range(7):
                qq = seg(q, k*.09, .3 + k*.09)
                if qq > 0: stroke_pts(ctx, [(x0 + 14 + k*24, -70), (x0 + 14 + k*24, 70)], qq, B['dim'], a*.8, 2, glow=False)
        if name == 'TURBINE':
            for k in range(5):
                qq = seg(q, k*.1, .35 + k*.1)
                if qq > 0: stroke_pts(ctx, [(x0 + 20 + k*30, -70), (x0 + 20 + k*30, 70)], qq, B['ice'], a*.8, 2.5, glow=False)
        txt(ctx, name, x0 + wdt/2, 120, 22, B['ice'] if name != 'COMBUSTOR' else B['amber'],
            a*ease(seg(q, .3, 1)), 'bold', 'c', mono=True)
    if hot > 0:
        g = ctx.get_target()
        for k in range(14):
            ph = ((hot*1.3) + k/14) % 1
            x = lerp(-140, 290, ph)
            glow_dot(ctx, x, lerp(-40, 40, (k % 5)/4), 4, B['amber'], a*.5*(1 - ph))
    ctx.restore()


# ---------- the flying testbed ----------
def testbed(ctx, cx, cy, s, a, p=1., hi=1, t=0.):
    """a generic four-engine transport in side-on line art with one engine highlighted"""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    # fuselage, nose to the right
    body = [(-400, -34), (-360, -62), (300, -62), (392, -42), (424, -12), (392, 14), (-360, 14), (-400, -34)]
    stroke_pts(ctx, body, p, B['ice'], a, 3)
    # flight deck
    stroke_pts(ctx, [(330, -56), (384, -40)], seg(p, .25, .8), B['cyan'], a*.8, 2, glow=False)
    # tail fin and tailplane
    stroke_pts(ctx, [(-352, -62), (-300, -196), (-244, -196), (-236, -62)], seg(p, .35, .9), B['ice'], a, 3)
    stroke_pts(ctx, [(-330, -186), (-190, -176)], seg(p, .45, .95), B['ice'], a, 2.5, glow=False)
    # high wing, swept back and down towards the viewer
    wing = [(60, -54), (104, -44), (-120, 96), (-206, 92), (60, -54)]
    stroke_pts(ctx, wing, seg(p, .3, .9), B['ice'], a, 3)
    # two engine pods slung under the wing; the inboard one carries the test engine
    for k in range(2):
        ex = -6 - k*96; ey = 24 + k*40
        on = (k == 0 and hi == 1)
        col = B['amber'] if on else B['dim']
        q = seg(p, .55 + k*.12, .92 + k*.12)
        if q <= 0: continue
        stroke_pts(ctx, [(ex + 4, ey - 26), (ex - 10, ey - 6)], q, B['dim'], a*.8, 2.5, glow=False)   # pylon
        stroke_pts(ctx, rect_pts(ex - 44, ey - 4, 88, 38), q, col, a, 2.5)
        stroke_pts(ctx, [(ex - 30, ey - 4), (ex - 30, ey + 34)], q, col, a*.7, 1.8, glow=False)
        if on:
            glow_dot(ctx, ex + 24, ey + 15, 7, B['amber'], a*(.6 + .4*math.sin(t*4)))
    ctx.restore()


# ---------- three tracks ----------
def track(ctx, x, y0, y1, title, lines, col, a, p=1.):
    stroke_pts(ctx, [(x, y0), (x, y1)], p, col, a, 3, glow=False)
    glow_dot(ctx, x, y0, 7, col, a*min(1, p*3))
    txt(ctx, title, x, y0 - 28, 30, col, a*ease(min(p*1.6, 1)), 'black', 'c', glow=.4)
    for i, ln in enumerate(lines):
        q = seg(p, .35 + i*.2, .75 + i*.2)
        if q > 0:
            for j, w_ in enumerate(ln.split('|')):
                txt(ctx, w_, x, y0 + 86 + i*104 + j*28, 23, B['steel'], a*ease(q), 'bold', 'c', mono=True)


# ---------- squadron arithmetic ----------
def sqnbars(ctx, x, y, w, a, p=1., sanctioned=42.5, actual=31., falling=29.):
    unit = w/sanctioned
    txt(ctx, 'SANCTIONED  42½ SQUADRONS', x, y - 22, 24, B['dim'], a, 'bold', mono=True)
    stroke_pts(ctx, rect_pts(x, y, w, 56), p, B['grid'], a, 2.5, dash=[8, 8], glow=False)
    q = ease(seg(p, .2, 1))
    fill(ctx, lambda: rrect(ctx, x, y + 86, unit*actual*q, 56, 6), B['cyan'], .22*a)
    stroke_pts(ctx, rect_pts(x, y + 86, unit*actual*q, 56), 1, B['cyan'], a, 2.5)
    txt(ctx, 'ACTUAL  31  (SEP 2025, AS REPORTED)', x + 18, y + 124, 24, B['ice'], a*q, 'bold', mono=True)
    q2 = ease(seg(p, .62, 1))
    if q2 > 0:
        xf = x + unit*falling
        fill(ctx, lambda: ctx.rectangle(xf, y + 86, unit*(actual - falling), 56), B['alert'], .22*a*q2)
        stroke_pts(ctx, [(xf, y + 80), (xf, y + 148)], 1, B['alert'], a*q2, 3, glow=False)
        tagb(ctx, xf, y + 182, 'FALLING TO 29', B['alert'], a*q2, 22, align='c')


# ---------- the blueprint wall ----------
WALL = [('EP 1', 'PRALAY'), ('EP 2', 'BRAHMOS'), ('EP 3', 'AGNI-5'), ('EP 4', 'THE SHIELD'), ('EP 5', 'TEJAS')]


def wall(ctx, t, a, drop=0.):
    """four cards pinned, the fifth dropping into place"""
    y = 300
    for i, (ep, name) in enumerate(WALL):
        x = 150 + i*330
        if i < 4:
            yy, al, sc = y, a, 1.
        else:
            d = ease(min(max(drop, 0), 1))
            yy = lerp(y - 420, y, d); al = a*min(1, drop*2.5); sc = 1.
        if al <= 0: continue
        ctx.save(); ctx.translate(x + 140, yy + 110); ctx.scale(sc, sc); ctx.translate(-(x + 140), -(yy + 110))
        col = B['amber'] if i == 4 else B['cyan']
        fill(ctx, lambda: rrect(ctx, x, yy, 280, 220, 10), B['deep'], .9*al)
        stroke_pts(ctx, rect_pts(x, yy, 280, 220), 1, col, al, 2.5)
        ctx.save(); ctx.translate(x + 140, yy + 104); ctx.scale(.26, .26)
        stroke_pts(ctx, jet_pts() if i == 4 else [(-200, 60), (0, -200), (200, 60), (-200, 60)], 1, col, al*.9, 10)
        ctx.restore()
        txt(ctx, ep, x + 20, yy + 36, 22, B['dim'], al, 'bold', mono=True)
        txt(ctx, name, x + 140, yy + 200, 26, B['ice'], al, 'black', 'c')
        glow_dot(ctx, x + 140, yy + 12, 5, col, al)
        ctx.restore()
