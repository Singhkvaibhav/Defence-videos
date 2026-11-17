"""Air-defence scene pieces for India's Defence, Decoded Ep 4.
Coverage is drawn as abstract nested rings on blueprint paper — never over a map,
never over territory. Nothing here draws a boundary or a coastline."""
import math, random
from engine.core import W, H, seg, ease, eoc, eob, lerp
from engine.bp import (B, rgba, rrect, txt, tw, stroke_pts, rect_pts, fill, glow_dot, bez, missile, radar, truck, card, tagb)


def ring(ctx, cx, cy, r, p, col, a, w=3., label=None, lab_a=None, sub=None, squash=.55, dash=None):
    """one coverage ring, drawn as a flattened ellipse so it reads as ground coverage"""
    n = 90
    pts = [(cx + r*math.cos(th), cy - r*squash*math.sin(th)) for th in [2*math.pi*i/n for i in range(n + 1)]]
    stroke_pts(ctx, pts, p, col, a, w, dash=dash)
    if label and p > .5:
        la = a if lab_a is None else lab_a
        txt(ctx, label, cx, cy - r*squash - 16, 30, col, la, 'black', 'c', glow=.5)
        if sub: txt(ctx, sub, cx, cy - r*squash + 18, 20, B['steel'], la*.9, 'bold', 'c', mono=True)


def rings(ctx, cx, cy, specs, t, a, squash=.55):
    """specs: [(radius, colour, label, sub, p)] drawn outermost first"""
    for r, col, label, sub, p in specs:
        if p <= 0: continue
        ring(ctx, cx, cy, r, min(p*1.6, 1), col, a, 3, label, a*ease(min(p*2, 1)), sub, squash)


def protected(ctx, cx, cy, a, p=1.):
    """the abstract thing being defended: a small cluster of shapes, no real place"""
    if p <= 0: return
    stroke_pts(ctx, rect_pts(cx - 44, cy - 54, 36, 54), p, B['ice'], a, 2.5)
    stroke_pts(ctx, rect_pts(cx + 2, cy - 78, 34, 78), p, B['ice'], a, 2.5)
    stroke_pts(ctx, [(cx - 70, cy), (cx + 70, cy)], p, B['dim'], a, 2, glow=False)
    glow_dot(ctx, cx + 19, cy - 92, 5, B['amber'], a*p)


def icon_eye(ctx, x, y, s, col, a, p=1.):
    up = [(x - 46*s, y), (x, y - 30*s), (x + 46*s, y)]
    dn = [(x + 46*s, y), (x, y + 30*s), (x - 46*s, y)]
    stroke_pts(ctx, bez(*up, 30), p, col, a, 3)
    stroke_pts(ctx, bez(*dn, 30), p, col, a, 3)
    if p > .7: glow_dot(ctx, x, y, 11*s, col, a)


def icon_brain(ctx, x, y, s, col, a, p=1.):
    """a decision node: a box with branches, not an anatomical brain"""
    stroke_pts(ctx, rect_pts(x - 34*s, y - 26*s, 68*s, 52*s), p, col, a, 3)
    for k, dy in enumerate((-18, 0, 18)):
        q = min(1, max(0, (p - .4 - k*.12)*4))
        if q > 0:
            stroke_pts(ctx, [(x + 34*s, y + dy*s), (x + 70*s, y + dy*1.9*s)], q, col, a, 2.5, glow=False)
        qq = min(1, max(0, (p - .3 - k*.1)*4))
        if qq > 0:
            stroke_pts(ctx, [(x - 70*s, y + dy*1.9*s), (x - 34*s, y + dy*s)], qq, col, a, 2.5, glow=False)


def icon_launch(ctx, x, y, s, col, a, p=1.):
    stroke_pts(ctx, [(x - 40*s, y + 26*s), (x + 40*s, y + 26*s)], p, col, a, 3, glow=False)
    missile(ctx, x, y - 6*s, 86*s, -math.pi/2 - .35, a, p=p, col=col)
    if p > .8:
        for k in range(3):
            glow_dot(ctx, x - 16*s + k*5*s, y + 30*s + k*9*s, (5 - k)*s, B['amber'], a*(.8 - k*.2))


def inbound(ctx, t, a, n=22, seed=3, y0=120, y1=760, speed=.16):
    """small markers drifting down from the top of frame. No impacts are ever drawn."""
    rr = random.Random(seed)
    for k in range(n):
        x = 70 + rr.uniform(0, W - 140); ph = rr.uniform(0, 1); sp = speed*rr.uniform(.7, 1.4)
        q = (t*sp + ph) % 1
        y = lerp(y0, y1, q)
        al = a*min(1, q*4)*(1 - max(0, (q - .75)/.25))
        stroke_pts(ctx, [(x, y - 16), (x, y + 10)], 1, B['alert'], al*.85, 2.5, glow=False)
        glow_dot(ctx, x, y + 12, 4, B['alert'], al)


def sensor_grid(ctx, t, a, p=1., rows=3, cols=9, y0=790, step=46, col=None):
    """a field of sensor dots lighting up in sequence"""
    col = col or B['cyan']
    for r in range(rows):
        for c in range(cols):
            x = 180 + c*((W - 360)/(cols - 1)); y = y0 + r*step
            ph = (c + r*3)/(cols + rows*3)
            lit = ((t*.8 + ph) % 1) < .22
            glow_dot(ctx, x, y, 6 if lit else 4, col, a*p*(.95 if lit else .3))


def netbox(ctx, x, y, w, h, title, sub, col, a, p=1.):
    fill(ctx, lambda: rrect(ctx, x, y, w, h, 10), B['deep'], .88*a)
    stroke_pts(ctx, rect_pts(x, y, w, h), p, col, a, 2.5)
    txt(ctx, title, x + w/2, y + h*.46, 40, B['ice'], a*ease(min(p*2, 1)), 'black', 'c')
    txt(ctx, sub, x + w/2, y + h*.46 + 36, 21, col, a*ease(min(p*2, 1)), 'bold', 'c', mono=True)


def link(ctx, p0, p1, p, col, a, sag=70):
    pts = bez(p0, ((p0[0] + p1[0])/2, (p0[1] + p1[1])/2 + sag), p1, 30)
    stroke_pts(ctx, pts, p, col, a*.8, 2.5, glow=False)


def rampart(ctx, cx, y, s, a, p=1.):
    """a generic ceremonial rampart in line art: a long wall with a central gateway and
    two flanking turrets. Not a drawing of any particular building."""
    wdt = 520*s
    stroke_pts(ctx, [(cx - wdt, y), (cx + wdt, y)], p, B['ice'], a, 3, glow=False)
    stroke_pts(ctx, rect_pts(cx - wdt, y - 150*s, 2*wdt, 150*s), min(p*1.3, 1), B['ice'], a, 2.5)
    # crenellations
    for k in range(17):
        xx = cx - wdt + k*(2*wdt/16)
        q = min(1, max(0, (p - .3 - k*.02)*5))
        if q > 0: stroke_pts(ctx, rect_pts(xx - 9*s, y - 174*s, 18*s, 24*s), q, B['ice'], a, 2, glow=False)
    # gateway arch
    g = min(1, max(0, (p - .35)*2.2))
    if g > 0:
        arch = bez((cx - 58*s, y), (cx - 58*s, y - 110*s), (cx, y - 110*s), 20) + bez((cx, y - 110*s), (cx + 58*s, y - 110*s), (cx + 58*s, y), 20)
        stroke_pts(ctx, arch, g, B['cyan'], a, 3)
    # turrets
    for sgn in (-1, 1):
        q = min(1, max(0, (p - .5)*2.5))
        if q <= 0: continue
        tx = cx + sgn*wdt*.62
        stroke_pts(ctx, rect_pts(tx - 34*s, y - 250*s, 68*s, 100*s), q, B['ice'], a, 2.5)
        dome = bez((tx - 34*s, y - 250*s), (tx, y - 320*s), (tx + 34*s, y - 250*s), 24)
        stroke_pts(ctx, dome, q, B['ice'], a, 2.5)


def statusrow(ctx, x, y, w, name, note, status, col, a, p=1.):
    card(ctx, x, y, w, 128, a, None, col, p=p)
    txt(ctx, name, x + 44, y + 58, 40, B['ice'], a, 'black')
    txt(ctx, note, x + 44, y + 100, 22, B['steel'], a, 'bold', mono=True)
    tagb(ctx, x + w - 40, y + 66, status, col, a, 22, align='r')


def splitspeed(ctx, t, a, left_p=1., right_p=1.):
    """slow mover on the left, fast steep arc on the right — no map, no places"""
    if left_p > 0:
        stroke_pts(ctx, [(120, 640), (820, 640)], left_p, B['grid'], a, 2, glow=False)
        x = lerp(140, 800, (t*.14) % 1)
        stroke_pts(ctx, [(x - 46, 640), (x + 46, 640)], 1, B['steel'], a*left_p, 4, glow=False)
        stroke_pts(ctx, [(x - 6, 640), (x - 34, 672)], 1, B['steel'], a*left_p, 4, glow=False)
        stroke_pts(ctx, [(x - 6, 640), (x - 34, 608)], 1, B['steel'], a*left_p, 4, glow=False)
        txt(ctx, 'ABOUT 900 KM/H', 470, 740, 26, B['steel'], a*left_p, 'bold', 'c', mono=True)
    if right_p > 0:
        arc = bez((1080, 200), (1480, 420), (1660, 860), 34)
        q = (t*.55) % 1
        stroke_pts(ctx, arc, 1, B['grid'], a*right_p, 2, glow=False)
        tail = [arc[i] for i in range(max(0, int(q*33) - 6), int(q*33) + 1)]
        if len(tail) > 1: stroke_pts(ctx, tail, 1, B['alert'], a*right_p, 5)
        txt(ctx, 'SEVERAL KM EVERY SECOND', 1380, 940, 26, B['alert'], a*right_p, 'bold', 'c', mono=True)
