"""Reusable military line-art props and chart helpers for India's Defence, Decoded.
Everything is stylised blueprint line work — no engineering drawings, no real likenesses."""
import math, random, cairo
from engine import core
from engine.core import W, H, seg, ease, eoc, eob, lerp, T
from engine.bp import B, rgba, rrect, txt, tw, stroke_pts, head_pt, rect_pts, fill, glow_dot, bez, missile, face

# ---------- sea and sky ----------
def waves(ctx, y, t, a, n=7, col=None, span=(0, W), step=40):
    col = col or B['cyan']
    for k in range(n):
        yy = y + k*22
        pts = [(x, yy + 4*math.sin(x*.012 + t*1.5 + k)) for x in range(span[0], span[1] + step, step)]
        stroke_pts(ctx, pts, 1, col, (.35 - k*.04)*a, 1.5, glow=False)

def horizon(ctx, cx, cy, r, a, col=None, p=1.):
    """a curved sea horizon: the arc of a very large circle"""
    col = col or B['ice']
    pts = [(cx + r*math.sin(th), cy - r*math.cos(th)) for th in [(-.55 + 1.1*i/80) for i in range(81)]]
    stroke_pts(ctx, pts, p, col, a, 3)
    return pts

# ---------- platforms ----------
def warship(ctx, x, y, s, a, t, p=1., cells=True):
    """generic surface warship in profile; optional vertical-launch cells on the foredeck"""
    ctx.save(); ctx.translate(x, y + 3*math.sin(t*.9)); ctx.scale(s, s)
    hull = [(-300, 0), (300, 0), (360, -42), (-250, -42), (-300, 0)]
    fill(ctx, lambda: [ctx.move_to(*hull[0])] + [ctx.line_to(*q) for q in hull[1:]] + [ctx.close_path()], B['cyan'], .10*a)
    stroke_pts(ctx, hull, p, B['ice'], a, 3)
    sup = [(-120, -42), (-120, -120), (40, -120), (60, -42)]
    fill(ctx, lambda: [ctx.move_to(*sup[0])] + [ctx.line_to(*q) for q in sup[1:]] + [ctx.close_path()], B['cyan'], .12*a)
    stroke_pts(ctx, sup, p, B['ice'], a, 3)
    stroke_pts(ctx, [(-40, -120), (-40, -210), (-70, -175), (-40, -165), (-10, -175), (-40, -210)], seg(p, .5, 1), B['ice'], a, 2.5)
    for k in range(3):
        stroke_pts(ctx, [(-108 + k*44, -60), (-78 + k*44, -60)], 1, B['dim'], a, 2, glow=False)
    if cells:
        for k in range(6):
            cx = 140 + (k % 3)*52; cy = -42 - (k//3)*0
            stroke_pts(ctx, rect_pts(cx, cy - 16, 44, 16), seg(p, .6, 1), B['amber'], a, 2, glow=False)
    ctx.restore()

def submarine(ctx, x, y, s, a, t, p=1.):
    """generic submarine, partly submerged"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    hull = bez((-320, 0), (-300, 70), (-180, 78), 14) + [(180, 78)] + bez((180, 78), (300, 70), (330, 0), 14)
    stroke_pts(ctx, hull, p, B['ice'], a, 3)
    fill(ctx, lambda: [ctx.move_to(*hull[0])] + [ctx.line_to(*q) for q in hull[1:]] + [ctx.close_path()], B['cyan'], .10*a)
    stroke_pts(ctx, [(-70, 0), (-70, -60), (40, -60), (60, 0)], seg(p, .4, 1), B['ice'], a, 3)
    stroke_pts(ctx, [(0, -60), (0, -110)], seg(p, .6, 1), B['dim'], a, 2, glow=False)
    ctx.restore()

def jet(ctx, x, y, s, a, t, p=1., load=True):
    """generic twin-tail fighter in profile, optionally with a missile under the belly"""
    ctx.save(); ctx.translate(x, y + 4*math.sin(t*1.2)); ctx.scale(s, s)
    body = [(-250, 0), (-170, -26), (90, -30), (230, -6), (250, 4), (90, 20), (-150, 22), (-250, 0)]
    fill(ctx, lambda: [ctx.move_to(*body[0])] + [ctx.line_to(*q) for q in body[1:]] + [ctx.close_path()], B['cyan'], .12*a)
    stroke_pts(ctx, body, p, B['ice'], a, 3)
    stroke_pts(ctx, [(70, -30), (130, -56), (190, -50), (200, -22)], seg(p, .3, 1), B['ice'], a, 2.5)   # canopy
    stroke_pts(ctx, [(-40, 10), (-150, 86), (-30, 80), (40, 16)], seg(p, .4, 1), B['ice'], a, 3)        # wing
    for dy in (-1, 1):
        stroke_pts(ctx, [(-190, -20), (-250, -92 if dy < 0 else -70), (-150, -22)], seg(p, .5, 1), B['ice'], a, 2.5)
    if load:
        missile(ctx, -20, 60, 190, 0, a*seg(p, .7, 1), col=B['amber'])
    ctx.restore()

def launcher(ctx, x, y, s, a, t, raise_=1.):
    """compact road launcher: cab, chassis, tilted canister"""
    from engine.bp import truck
    truck(ctx, x, y, s, a, t, raise_=raise_, wheels_spin=0)

# ---------- charts ----------
def axes(ctx, x0, y0, w, h, a, xlab, ylab, xticks, yticks, p=1.):
    stroke_pts(ctx, [(x0, y0), (x0, y0 - h)], p, B['dim'], a, 2, glow=False)
    stroke_pts(ctx, [(x0, y0), (x0 + w, y0)], p, B['dim'], a, 2, glow=False)
    for v, lab in xticks:
        xx = x0 + w*v
        stroke_pts(ctx, [(xx, y0), (xx, y0 + 12)], 1, B['dim'], a, 2, glow=False)
        txt(ctx, lab, xx, y0 + 46, 22, B['dim'], a, 'bold', 'c', mono=True)
    for v, lab in yticks:
        yy = y0 - h*v
        stroke_pts(ctx, [(x0 - 12, yy), (x0, yy)], 1, B['dim'], a, 2, glow=False)
        txt(ctx, lab, x0 - 26, yy + 8, 22, B['dim'], a, 'bold', 'r', mono=True)
    txt(ctx, xlab, x0 + w/2, y0 + 92, 26, B['cyan'], a, 'bold', 'c', mono=True)
    ctx.save(); ctx.translate(x0 - 100, y0 - h/2); ctx.rotate(-math.pi/2)
    txt(ctx, ylab, 0, 0, 26, B['cyan'], a, 'bold', 'c', mono=True); ctx.restore()

def dot(ctx, x, y, label, col, a, r=16, sprint=None, align='l', size=26, t=0., dy=0):
    glow_dot(ctx, x, y, r, col, a)
    dx = 26 if align == 'l' else -26
    txt(ctx, label, x + dx, y + 9 + dy, size, col, a, 'black', 'l' if align == 'l' else 'r')
    if sprint:
        pts = [(x, y), (x, y - sprint)]
        stroke_pts(ctx, pts, 1, B['amber'], a*.9, 4)
        for d in (-.6, .6):
            stroke_pts(ctx, [(x, y - sprint), (x + 14*math.sin(d), y - sprint + 20*math.cos(d))], 1, B['amber'], a*.9, 4, glow=False)

def bar(ctx, x, y, w, h, a, col, label=None, val=None, p=1., vsize=34):
    hh = h*eoc(p)
    fill(ctx, lambda: rrect(ctx, x, y - hh, w, hh, 6), col, .25*a)
    stroke_pts(ctx, rect_pts(x, y - hh, w, hh), 1, col, a, 2.5)
    if label: txt(ctx, label, x + w/2, y + 40, 22, col, a, 'bold', 'c', mono=True)
    if val: txt(ctx, val, x + w/2, y - hh - 20, vsize, B['ice'], a, 'black', 'c', glow=.5)

# ---------- schematic pin board (no boundaries, ever) ----------
def sea_board(ctx, t, a, washes=((640, 560, 380), (1340, 520, 330)), lanes=()):
    """schematic water board: halftone-free wash rings and moving sea lanes. No country outlines."""
    for (cx, cy, r) in washes:
        for k in range(4):
            ctx.new_path(); rgba(ctx, B['grid'], .30*a); ctx.set_line_width(2)
            ctx.arc(cx, cy, r - k*26, 0, 2*math.pi); ctx.stroke()
    for (p0, p1) in lanes:
        pts = bez(p0, ((p0[0] + p1[0])/2, min(p0[1], p1[1]) - 150), p1, 40)
        ctx.save(); ctx.set_dash([16, 14], -t*26); rgba(ctx, B['steel'], .5*a); ctx.set_line_width(3)
        ctx.move_to(*pts[0])
        for q in pts[1:]: ctx.line_to(*q)
        ctx.stroke(); ctx.restore()
        for k in range(2):
            s_ = (t*.1 + k/2) % 1
            px, py = pts[int(s_*40)]
            fill(ctx, lambda: rrect(ctx, px - 13, py - 7, 26, 14, 4), B['steel'], .8*a)

def pin(ctx, x, y, name, sub, col, a, p=1., t=0., align='c'):
    """a labelled pin with a landing ripple"""
    if p <= 0: return
    dy = -220*(1 - eob(min(p*1.3, 1), 1.35))
    for k in range(2):
        rp = seg(p, .35 + k*.18, 1.0 + k*.18)
        if rp > 0:
            ctx.new_path(); rgba(ctx, col, (1 - rp)*a); ctx.set_line_width(3); ctx.arc(x, y, 12 + 70*rp, 0, 2*math.pi); ctx.stroke()
    stroke_pts(ctx, [(x, y + dy - 54), (x, y + dy)], 1, col, a, 3, glow=False)
    glow_dot(ctx, x, y + dy, 11, col, a)
    txt(ctx, name, x, y + dy - 76, 32, B['ice'], a*ease(min(p*2, 1)), 'black', align, glow=.6)
    if sub: txt(ctx, sub, x, y + dy - 40, 22, col, a*ease(seg(p, .4, .9)), 'bold', align, mono=True)

def schematic_note(ctx, a):
    txt(ctx, 'SCHEMATIC · NOT TO SCALE · BOUNDARIES NOT SHOWN', W - 70, 1000, 18, B['steel'], a, 'reg', 'r', mono=True)
