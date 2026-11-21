"""Scene pieces for India's Defence, Decoded Ep 6 (INS Vikrant).

Stylised blueprint line art only: a profile with a ski-jump, a deck plan, a
bell, a steel plate, reach circles. No hull form detail, no sensors, no
weapons, no compartment layout, and nothing that is a map — the reach
diagram is two abstract circles with no coastline or landmass.
"""
import math
from engine.core import W, H, seg, ease, eob, eoc, lerp
from engine.bp import (B, rgba, rrect, txt, tw, stroke_pts, rect_pts, fill, glow_dot, bez, card, tagb)


# ---------- the ship, in profile ----------
def carrier(ctx, cx, cy, s, p, a, col=None, ski=True, island=True):
    """Side elevation: hull, flight deck, ski-jump at the bow, island to starboard."""
    col = col or B['ice']
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    hull = [(-470, 0), (-430, 54), (380, 54), (470, 10), (470, -34), (-470, -34), (-470, 0)]
    stroke_pts(ctx, hull, p, col, a, 3)
    # flight deck line
    stroke_pts(ctx, [(-470, -34), (300, -34)], seg(p, .25, .8), col, a, 3, glow=False)
    if ski:
        q = seg(p, .55, 1.)
        stroke_pts(ctx, bez((300, -34), (420, -40), (470, -96), 26), q, B['amber'], a, 4)
    if island:
        q = seg(p, .4, .9)
        stroke_pts(ctx, rect_pts(-150, -140, 150, 106), q, col, a, 2.5)
        stroke_pts(ctx, [(-96, -140), (-96, -212)], seg(p, .6, 1), col, a*.85, 2.5, glow=False)
        for k in range(3):
            stroke_pts(ctx, [(-134, -120 + k*28), (-20, -120 + k*28)], seg(p, .55 + k*.08, .9), B['dim'], a*.6, 1.5, glow=False)
    # waterline
    stroke_pts(ctx, [(-520, 54), (520, 54)], seg(p, .7, 1), B['grid'], a*.7, 2, dash=[14, 10], glow=False)
    ctx.restore()


def deck_plan(ctx, cx, cy, s, a, p=1., wires=0, approach=0.):
    """The flight deck from above: angled landing strip, three arrester wires."""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    outline = [(-430, -120), (330, -120), (470, -58), (470, 70), (330, 132), (-430, 132), (-470, 6), (-430, -120)]
    stroke_pts(ctx, outline, p, B['ice'], a, 3)
    stroke_pts(ctx, [(-430, 70), (380, 70)], seg(p, .3, .9), B['dim'], a*.7, 2, dash=[20, 14], glow=False)
    for k in range(3):
        q = 1. if wires > k else 0.
        if wires == 0: q = seg(p, .5 + k*.1, .85 + k*.1)
        if q <= 0: continue
        x = -210 + k*90
        stroke_pts(ctx, [(x, -96), (x - 40, 100)], 1, B['amber'] if wires > k else B['dim'],
                   a*(1. if wires > k else .7), 3 if wires > k else 2, glow=wires > k)
    if approach > 0:
        pts = bez((620, 300), (200, 180), (-150, 40), 40)
        stroke_pts(ctx, pts, approach, B['cyan'], a*.85, 2.5, dash=[16, 12])
        i = min(len(pts) - 1, int(approach*(len(pts) - 1)))
        glow_dot(ctx, pts[i][0], pts[i][1], 7, B['cyan'], a)
    ctx.restore()


def skijump(ctx, cx, cy, s, a, p=1., t=0., launch=0.):
    """Side view of the launch: deck run, ramp, climb-away arc."""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    deck = [(-520, 0), (240, 0)]
    stroke_pts(ctx, deck, p, B['ice'], a, 4)
    ramp = bez((240, 0), (390, -6), (470, -78), 26)
    stroke_pts(ctx, ramp, seg(p, .3, .9), B['amber'], a, 5)
    if launch > 0:
        arc = bez((470, -78), (760, -210), (1040, -250), 34)
        stroke_pts(ctx, arc, launch, B['cyan'], a*.8, 2.5, dash=[14, 12])
        path = [(lerp(-520, 240, min(launch/.45, 1)), 0)] if launch < .45 else None
        if path is None:
            u = (launch - .45)/.55
            seq = ramp + arc
            i = min(len(seq) - 1, int(u*(len(seq) - 1)))
            path = [seq[i]]
        x, y = path[0]
        ctx.save(); ctx.translate(x, y - 16); ctx.scale(.09, .09)
        stroke_pts(ctx, [(-300, 40), (0, -60), (300, 40), (120, 46), (0, 10), (-120, 46), (-300, 40)], 1, B['ice'], a, 26)
        ctx.restore()
    ctx.restore()


def catapult(ctx, cx, cy, s, a, p=1.):
    """A greyed catapult track, drawn only to be labelled NOT FITTED."""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    stroke_pts(ctx, [(-400, 0), (400, 0)], p, B['dim'], a*.7, 4, dash=[10, 8], glow=False)
    stroke_pts(ctx, rect_pts(-400, -26, 150, 26), seg(p, .3, 1), B['dim'], a*.6, 2, glow=False)
    ctx.restore()


# ---------- the bell ----------
def bell(ctx, cx, cy, s, a, p=1., t=0.):
    ctx.save(); ctx.translate(cx, cy)
    ctx.rotate(math.sin(t*1.1)*.035)
    ctx.scale(s, s)
    body = bez((-120, 150), (-96, -120), (0, -150), 26) + bez((0, -150), (96, -120), (120, 150), 26)
    stroke_pts(ctx, body, p, B['ice'], a, 3)
    stroke_pts(ctx, [(-120, 150), (120, 150)], seg(p, .5, .9), B['ice'], a, 3, glow=False)
    stroke_pts(ctx, [(-134, 150), (-120, 172), (120, 172), (134, 150)], seg(p, .6, 1), B['ice'], a*.9, 2.5, glow=False)
    q = seg(p, .7, 1)
    if q > 0:
        stroke_pts(ctx, [(0, -150), (0, -186)], q, B['dim'], a*.8, 3, glow=False)
        glow_dot(ctx, 0, 148, 9, B['amber'], a*q*(.55 + .45*math.sin(t*1.6)))
    ctx.restore()


# ---------- the three problems ----------
def icon_hull(ctx, x, y, s, col, a, p=1.):
    ctx.save(); ctx.translate(x, y); ctx.scale(s*.17, s*.17)
    stroke_pts(ctx, [(-430, -60), (-380, 60), (380, 60), (430, -60), (-430, -60)], p, col, a, 16)
    stroke_pts(ctx, [(-430, -60), (430, -60)], seg(p, .4, 1), col, a*.8, 14, glow=False)
    ctx.restore()


def icon_deck(ctx, x, y, s, col, a, p=1.):
    ctx.save(); ctx.translate(x, y); ctx.scale(s*.17, s*.17)
    stroke_pts(ctx, [(-420, 40), (300, 40)], p, col, a, 16)
    stroke_pts(ctx, bez((300, 40), (420, 34), (470, -40), 20), seg(p, .35, 1), col, a, 16)
    for k in range(3):
        stroke_pts(ctx, [(-300 + k*120, 0), (-330 + k*120, 76)], seg(p, .5 + k*.12, .9), col, a*.8, 11, glow=False)
    ctx.restore()


def icon_plane(ctx, x, y, s, col, a, p=1.):
    ctx.save(); ctx.translate(x, y); ctx.scale(s*.2, s*.2)
    stroke_pts(ctx, [(0, -180), (24, -96), (40, -30), (250, 110), (250, 140), (90, 140), (60, 190),
                     (-60, 190), (-90, 140), (-250, 140), (-250, 110), (-40, -30), (-24, -96), (0, -180)], p, col, a, 13)
    ctx.restore()


def problem3(ctx, x, y, label, n, icon, col, a, p, hollow=False):
    icon(ctx, x, y, 1., col, a, p)
    txt(ctx, n, x, y + 118, 22, B['dim'], a*ease(seg(p, .4, .9)), 'bold', 'c', mono=True)
    txt(ctx, label, x, y + 158, 34, col, a*ease(seg(p, .5, 1)), 'black', 'c', glow=.4)


# ---------- steel ----------
def steel_plate(ctx, cx, cy, s, a, p=1., stamped=0., shock=0.):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    stroke_pts(ctx, rect_pts(-300, -170, 600, 340), p, B['ice'], a, 3)
    for k in range(5):
        stroke_pts(ctx, [(-300, -112 + k*68), (300, -112 + k*68)], seg(p, .2 + k*.1, .7 + k*.1),
                   B['grid'], a*.55, 1.6, glow=False)
    if shock > 0:
        for k in range(4):
            r = 60 + k*90
            ph = (shock*1.1 - k*.12) % 1.6
            if ph <= 0 or ph > 1: continue
            ctx.new_path(); rgba(ctx, B['cyan'], a*(1 - ph)*.5); ctx.set_line_width(3)
            ctx.arc(-460, 0, r*ph + 40, -1.0, 1.0); ctx.stroke()
    if stamped > 0:
        e = ease(stamped)
        ctx.save(); ctx.translate(0, 0); ctx.rotate(-.06)
        sc = lerp(1.5, 1., eob(e, 1.5))
        ctx.scale(sc, sc)
        stroke_pts(ctx, rect_pts(-250, -56, 500, 112), 1, B['amber'], a*e, 4)
        txt(ctx, 'WARSHIP GRADE', 0, 18, 52, B['amber'], a*e, 'black', 'c', glow=.8)
        ctx.restore()
    ctx.restore()


# ---------- reach: two abstract circles, never a map ----------
def reach(ctx, a, p=1., t=0., moved=0.):
    """Left: a fixed base with a fixed circle. Right: a ship whose circle travels."""
    bx, by = 560, 500
    stroke_pts(ctx, rect_pts(bx - 46, by - 10, 92, 44), min(1, p*2), B['ice'], a, 3)
    stroke_pts(ctx, [(bx - 70, by + 34), (bx + 70, by + 34)], min(1, p*2), B['dim'], a*.8, 2, glow=False)
    txt(ctx, 'LAND BASE', bx, by + 90, 24, B['steel'], a*ease(min(1, p*2)), 'bold', 'c', mono=True)
    ctx.new_path(); rgba(ctx, B['steel'], a*.55*ease(p)); ctx.set_line_width(2.5); ctx.set_dash([12, 10])
    ctx.arc(bx, by, 300*ease(p), 0, 2*math.pi); ctx.stroke(); ctx.set_dash([])
    sx = 1380 + moved*220
    ctx.save(); ctx.translate(sx, by); ctx.scale(.26, .26)
    stroke_pts(ctx, [(-470, 0), (-430, 54), (380, 54), (470, 10), (470, -34), (-470, -34), (-470, 0)], min(1, p*2), B['ice'], a, 11)
    ctx.restore()
    txt(ctx, 'CARRIER', sx, by + 90, 24, B['cyan'], a*ease(min(1, p*2)), 'bold', 'c', mono=True)
    ctx.new_path(); rgba(ctx, B['cyan'], a*.6*ease(p)); ctx.set_line_width(2.5); ctx.set_dash([12, 10])
    ctx.arc(sx, by, 300*ease(p), 0, 2*math.pi); ctx.stroke(); ctx.set_dash([])


# ---------- three ships ----------
def fleet(ctx, a, labels, states, y=470, s=.34):
    """Three carrier profiles: solid for in service, dotted for proposed."""
    for k, (lab, st) in enumerate(zip(labels, states)):
        if st <= 0: continue
        x = 400 + k*560
        dotted = st < .99
        ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
        col = B['dim'] if dotted else B['ice']
        pts = [(-470, 0), (-430, 54), (380, 54), (470, 10), (470, -34), (-470, -34), (-470, 0)]
        stroke_pts(ctx, pts, 1, col, a*(.6 if dotted else 1), 9, dash=[18, 14] if dotted else None, glow=not dotted)
        stroke_pts(ctx, bez((300, -34), (420, -40), (470, -96), 20), 1, B['amber'] if not dotted else B['dim'],
                   a*(.6 if dotted else 1), 10, dash=[18, 14] if dotted else None, glow=False)
        ctx.restore()
        txt(ctx, lab, x, y + 110, 30, B['ice'] if not dotted else B['dim'], a, 'black', 'c')


# ---------- the blueprint wall ----------
WALL6 = [('EP 1', 'PRALAY'), ('EP 2', 'BRAHMOS'), ('EP 3', 'AGNI-5'),
         ('EP 4', 'THE SHIELD'), ('EP 5', 'TEJAS'), ('EP 6', 'VIKRANT')]


def wall6(ctx, t, a, drop=0.):
    y = 320
    for i, (ep, name) in enumerate(WALL6):
        x = 60 + i*310
        if i < 5:
            yy, al = y, a
        else:
            d = ease(min(max(drop, 0), 1))
            yy = lerp(y - 420, y, d); al = a*min(1, drop*2.5)
        if al <= 0: continue
        col = B['amber'] if i == 5 else B['cyan']
        fill(ctx, lambda: rrect(ctx, x, yy, 262, 210, 10), B['deep'], .9*al)
        stroke_pts(ctx, rect_pts(x, yy, 262, 210), 1, col, al, 2.5)
        ctx.save(); ctx.translate(x + 131, yy + 100); ctx.scale(.2, .2)
        if i == 5:
            stroke_pts(ctx, [(-470, 0), (-430, 54), (380, 54), (470, 10), (470, -34), (-470, -34), (-470, 0)], 1, col, al*.9, 14)
        else:
            stroke_pts(ctx, [(-200, 60), (0, -200), (200, 60), (-200, 60)], 1, col, al*.9, 14)
        ctx.restore()
        txt(ctx, ep, x + 18, yy + 34, 21, B['dim'], al, 'bold', mono=True)
        txt(ctx, name, x + 131, yy + 190, 25, B['ice'], al, 'black', 'c')
        glow_dot(ctx, x + 131, yy + 12, 5, col, al)
