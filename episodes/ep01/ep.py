"""India's Defence, Decoded — Episode 1: Pralay (bilingual: English + Hindi)."""
import os, sys, math, random, cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 470.0
core.TOTAL = TOTAL
from engine.core import W, H, seg, ease, eoc, eob, lerp, T
from engine.bp import (B, rgba, rrect, bg, txt, tw, typed, wrap, para, stroke_pts, head_pt, rect_pts, fill, glow_dot, bez, missile, truck,
                       figure, radar, hud, card, tagb, outro, camera, india_map, map_point, scene, subscribe_card)
from text import EN, HI as _HI

EP = 1
CODE = 'Def01'
TITLE = 'Pralay'
NAME = "Pralay: India's quasi-ballistic missile"
POST = 'engine.bp'
BED = 'pulse'
VOICE_EN = {'length': 0.98, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
VOICE_HI = {'length': 0.86, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
CRF, PRESET = 17, 'medium'
EXTRA = {'cold1': .8, 'cold2': .6, 'three': 1.0, 'end': 2.5}
HI = _HI

def Ts(x):
    try: return T(x)
    except ValueError: return 999.
def _c(x): return Ts(x) if isinstance(x, str) else x

# ---------- cold open: the launch ----------
X0, Y0, S0 = 470, 760, .75
PIV = (X0 + -260*S0, Y0 - 86*S0)
TOP = (PIV[0], PIV[1] - 440*S0)
TGT = (1730, 700)
PATH = bez(TOP, (TOP[0] + 60, TOP[1] - 260), (900, 170), 30) + bez((900, 170), (1300, 150), (1460, 300), 30)[1:] + bez((1460, 300), (1560, 360), TGT, 30)[1:]
def s_cold1(ctx, t, D):
    bg(ctx); a_out = outro(t, D, .3)
    hud(ctx, t, '5 NOV 2026 · 11:10 HRS · DR APJ ABDUL KALAM ISLAND, ODISHA', a_out)
    ctx.save(); camera(ctx, t, D, (1.0, 1.06), cy=560)
    # sea and coast
    for k in range(7):
        y = 800 + k*22
        pts = [(x, y + 4*math.sin(x*.012 + t*1.5 + k)) for x in range(0, W + 40, 40)]
        stroke_pts(ctx, pts, 1, B['cyan'], (.35 - k*.04)*a_out, 1.5, glow=False)
    stroke_pts(ctx, [(0, 790), (900, 790), (1100, 770), (W, 770)], 1, B['ice'], .6*a_out, 2)
    # truck drives in
    xd = lerp(-500, X0, eoc(seg(t, .2, 3.0)))
    tr = seg(t, Ts('A sealed tube') - .2, Ts('A sealed tube') + 2.2)
    truck(ctx, xd, Y0, S0, a_out, t, raise_=tr, wheels_spin=-xd*.03)
    # countdown
    tf = Ts('Then fire')
    for k, n in enumerate(('3', '2', '1')):
        q = seg(t, tf - 2.4 + k*.8, tf - 1.7 + k*.8)
        if 0 < q < 1: txt(ctx, n, 1700, 300, 160*(1 + .3*(1 - q)), B['amber'], (1 - q)*a_out, 'black', 'c', glow=1)
    # launch
    if t > tf:
        fl = 1 - seg(t, tf, tf + .9)
        glow_dot(ctx, TOP[0], TOP[1] + 30, 30*fl + 4, B['amber'], fl*a_out)
        cues = [(tf, 0), (Ts('climbs') + .3, .22), (Ts('flattens out'), .45), (Ts('turns'), .72), (Ts('hits its target'), 1.)]
        p = 0
        for (t0, p0), (t1, p1) in zip(cues, cues[1:]):
            if t >= t0: p = lerp(p0, p1, min(1, (t - t0)/max(t1 - t0, .01)))
        stroke_pts(ctx, PATH, p, B['ice'], a_out*.9, 3)
        if p < 1:
            hx_, hy_, ang = head_pt(PATH, p)
            missile(ctx, hx_, hy_, 110, ang, a_out)
            glow_dot(ctx, hx_ - 60*math.cos(ang), hy_ - 60*math.sin(ang), 6, B['amber'], a_out)
        # the turn: a bracket marks the late change of course
        tk = Ts('turns'); q = seg(t, tk, tk + .5)
        if q > 0: tagb(ctx, 1480, 240, 'LATE TURN', B['amber'], ease(q)*a_out*(1 - seg(t, tk + 3, tk + 3.5)), 22, align='c')
    # target
    stroke_pts(ctx, [(TGT[0] - 50, TGT[1]), (TGT[0] + 50, TGT[1])], 1, B['dim'], a_out, 2, glow=False)
    stroke_pts(ctx, [(TGT[0], TGT[1] - 50), (TGT[0], TGT[1] + 50)], 1, B['dim'], a_out, 2, glow=False)
    th = Ts('hits its target'); hq = seg(t, th, th + 1.2)
    if hq > 0:
        for k in range(3):
            r = 20 + 160*seg(t, th + k*.15, th + 1.2 + k*.15)
            ctx.new_path(); rgba(ctx, B['amber'], (1 - seg(t, th + k*.15, th + 1.2 + k*.15))*a_out); ctx.set_line_width(4); ctx.arc(TGT[0], TGT[1], r, 0, 2*math.pi); ctx.stroke()
        tagb(ctx, TGT[0], TGT[1] - 120, 'TARGET HIT', B['amber'], ease(seg(t, th + .2, th + .6))*a_out, 24, align='c')
    ctx.restore()
scene(s_cold1)

def s_cold2(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'INDIA\'S DEFENCE, DECODED · EPISODE 1', a_out)
    ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=520)
    q = seg(t, .2, .6)
    tq = Ts('"has become imminent"')
    card(ctx, 330, 230, 1260, 190, ease(seg(t, tq - 1.4, tq - .9))*a_out, 'DEFENCE MINISTRY · 5 NOV 2026', B['cyan'], p=seg(t, tq - 1.4, tq - .4))
    txt(ctx, typed('"The induction of the system has become imminent."', seg(t, tq - .8, tq + .8)), 360, 360, 44, B['ice'], ease(seg(t, tq - 1, tq - .6))*a_out, 'bold')
    tp = Ts('This is Pralay'); pq = seg(t, tp, tp + .5)
    if pq > 0:
        sc = lerp(1.6, 1, eob(pq, 1.3))
        ctx.save(); ctx.translate(W/2, 680); ctx.scale(sc, sc)
        txt(ctx, 'PRALAY', 0, 0, 230, B['ice'], ease(pq*2)*a_out, 'black', 'c', glow=1.5)
        ctx.restore()
        rgba(ctx, B['cyan'], a_out*ease(pq)); ctx.rectangle(W/2 - 520*ease(pq), 720, 1040*ease(pq), 4); ctx.fill()
    td = Ts("Let's decode it"); dq = seg(t, td, td + .5)
    if dq > 0:
        txt(ctx, typed("LET'S DECODE IT_", dq), W/2, 800, 40, B['cyan'], a_out, 'bold', 'c', mono=True)
    ctx.restore()
scene(s_cold2)

# ---------- spec sheet ----------
def s_spec1(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'SPEC SHEET', a_out)
    ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=500)
    p = seg(t, .2, 2.2)
    missile(ctx, W/2, 300, 1250, 0, a_out, p=p, fill_a=.10)
    # dimension line
    dq = seg(t, 1.6, 2.4)
    if dq > 0:
        stroke_pts(ctx, [(W/2 - 625, 420), (W/2 + 625, 420)], dq, B['dim'], a_out, 1.5, glow=False)
        for xx in (W/2 - 625, W/2 + 625): stroke_pts(ctx, [(xx, 405), (xx, 435)], dq, B['dim'], a_out, 1.5, glow=False)
        txt(ctx, 'STYLISED · NOT TO SCALE', W/2, 455, 18, B['dim'], ease(dq)*a_out, 'bold', 'c', mono=True)
    rows = [('WEIGHT', '~5 TONNES', 'Weight'), ('FUEL', 'SOLID', 'Fuel'), ('RANGE', '150–500 KM', 'Range'), ('WARHEAD', '500–1,000 KG · CONVENTIONAL', 'Warhead')]
    for i, (k, v, cue) in enumerate(rows):
        t0 = Ts(cue); q = seg(t, t0 - .1, t0 + .4)
        if q <= 0: continue
        y = 540 + i*82; a = ease(q*2)*a_out
        stroke_pts(ctx, [(300, y + 22), (1620, y + 22)], q, B['grid'], a, 1.5, glow=False)
        txt(ctx, k, 300, y, 34, B['cyan'], a, 'bold', mono=True)
        if k == 'RANGE':
            r = seg(t, t0, t0 + 1.5)
            v = f'{int(150*min(1, r*3))}–{int(500*r)} KM'
        txt(ctx, v, 1620, y, 44, B['ice'], a, 'black', 'r', glow=.6)
    th = Ts('the heavier'); hq = seg(t, th, th + .6)
    if hq > 0:
        a = ease(hq)*a_out
        tagb(ctx, 1240, 930, 'HEAVIER WARHEAD  →  SHORTER REACH', B['amber'], a, 24, align='c')
    ctx.restore()
scene(s_spec1)

def s_spec2(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'SPEC SHEET · LAUNCHER AND MAKERS', a_out)
    ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
    truck(ctx, 760, 620, 1.05, fadein(t), t, raise_=.18 + .06*math.sin(t*.5), wheels_spin=0)
    for (cue, s_, x, y) in (('eight-by-eight', '8×8 ROAD-MOBILE LAUNCHER', 760, 760), ('sealed canister', 'SEALED CANISTER', 520, 330)):
        q = seg(t, Ts(cue) - .1, Ts(cue) + .4)
        if q > 0: tagb(ctx, x, y, s_, B['cyan'], ease(q)*a_out, 24, align='c')
    for (cue, s_, y) in (("DRDO's Research Centre", 'DESIGN · DRDO, RESEARCH CENTRE IMARAT, HYDERABAD', 860), ('Bharat Dynamics', 'PRODUCTION · BHARAT DYNAMICS LIMITED', 920)):
        q = seg(t, Ts(cue) - .1, Ts(cue) + .4)
        if q > 0: txt(ctx, typed(s_, q*1.5), 200, y, 26, B['ice'], a_out, 'bold', mono=True)
    tn = Ts('And the name'); q = seg(t, tn, tn + .6)
    if q > 0:
        a = ease(q*1.5)*a_out
        card(ctx, 1260, 180, 560, 300, a, 'THE NAME', B['amber'], p=q)
        txt(ctx, 'PRALAY', 1540, 330, 84, B['ice'], a, 'black', 'c', glow=1)
        txt(ctx, '"the great dissolution,', 1540, 395, 30, B['amber'], ease(seg(t, Ts('great dissolution') - .2, Ts('great dissolution') + .3))*a_out, 'bold', 'c')
        txt(ctx, 'the end of an age"', 1540, 440, 30, B['amber'], ease(seg(t, Ts('end of an age') - .2, Ts('end of an age') + .3))*a_out, 'bold', 'c')
    ctx.restore()
scene(s_spec2)
def fadein(t, t0=.1, d=.5): return ease(seg(t, t0, t0 + d))

# ---------- 500 km on the official map ----------
HYD, BLR = (460, 1100), (410, 1345)
def s_far(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'HOW FAR IS 500 KM?', a_out)
    mh = 900; mcx, mcy = 640, 560
    z = lerp(1.0, 2.0, ease(seg(t, .3, 3.0)))
    hx_, hy_ = map_point(mcx, mcy, mh, *HYD); bx, by = map_point(mcx, mcy, mh, *BLR)
    fx, fy = (hx_ + bx)/2, (hy_ + by)/2
    ctx.save(); ctx.translate(lerp(fx, 760, ease(seg(t, .3, 3.0))), lerp(fy, 540, ease(seg(t, .3, 3.0)))); ctx.scale(z, z); ctx.translate(-fx, -fy)
    india_map(ctx, mcx, mcy, mh, fadein(t, 0, .6)*a_out)
    th = Ts('start in Hyderabad'); q = seg(t, th, th + .4)
    if q > 0:
        glow_dot(ctx, hx_, hy_, 6/z*1.6, B['cyan'], a_out)
        txt(ctx, 'HYDERABAD', hx_ + 14/z*2, hy_ - 8/z*2, 26/z*1.6, B['ice'], ease(q)*a_out, 'bold', mono=True)
    tl_ = Ts('A straight line'); lq = eoc(seg(t, tl_, tl_ + 2.4))
    if lq > 0:
        stroke_pts(ctx, [(hx_, hy_), (bx, by)], lq, B['amber'], a_out, 4/z*1.5)
        if lq >= 1:
            glow_dot(ctx, bx, by, 6/z*1.6, B['cyan'], a_out)
            txt(ctx, 'BENGALURU', bx + 14/z*2, by + 8/z*2, 26/z*1.6, B['ice'], a_out, 'bold', mono=True)
    ctx.restore()
    txt(ctx, 'MAP: SURVEY OF INDIA (OFFICIAL DEPICTION)', W - 70, 1000, 18, B['steel'], a_out, 'reg', 'r', mono=True)
    if lq > 0:
        txt(ctx, f'{int(500*lq)} KM', 1450, 430, 140, B['amber'], a_out, 'black', 'c', glow=1)
        txt(ctx, 'STRAIGHT LINE', 1450, 490, 26, B['ice'], a_out, 'bold', 'c', mono=True)
    ta = Ts('An airliner'); q = seg(t, ta, ta + .5)
    if q > 0:
        card(ctx, 1150, 580, 600, 260, ease(q)*a_out, 'TIME TO COVER IT', B['cyan'], p=q)
        txt(ctx, 'AIRLINER', 1180, 690, 30, B['ice'], ease(q)*a_out, 'bold', mono=True)
        txt(ctx, '~1 HOUR', 1720, 690, 40, B['ice'], ease(q)*a_out, 'black', 'r')
        pq = seg(t, Ts('Pralay needs minutes'), Ts('Pralay needs minutes') + .4)
        txt(ctx, 'PRALAY', 1180, 780, 30, B['amber'], ease(pq)*a_out, 'bold', mono=True)
        txt(ctx, 'MINUTES', 1720, 780, 40, B['amber'], ease(pq)*a_out, 'black', 'r', glow=1)
scene(s_far)

# ---------- three ways to fly ----------
GND = 800
PATHS = {
    'BALLISTIC': bez((130, GND), (360, -150), (590, GND), 60),
    'CRUISE': [(130 + i*7.5, GND - 40 - 6*math.sin(i*.4)) for i in range(61)],
    'QUASI': bez((130, GND), (260, 560), (450, 570), 40) + bez((450, 570), (520, 575), (560, GND), 20)[1:],
}
def _panel_paths(ctx, t, D, show, a_out, snap=None, intercept=False, speed_tag=None):
    names = [('BALLISTIC', 'TALL ARC · FAST · PREDICTABLE', B['ice']), ('CRUISE', 'LOW · HARD TO SPOT · SLOWER', B['steel']), ('QUASI', 'FLAT ARC · TURNS LATE', B['amber'])]
    for i, (k, sub, col) in enumerate(names):
        t0 = show[i]
        if t0 is None or t < t0: continue
        ox = i*600; a = fadein(t, t0, .5)*a_out
        ctx.save(); ctx.translate(ox, 0)
        card(ctx, 60, 170, 560, 700, a, ('QUASI-BALLISTIC' if k == 'QUASI' else k) + (' · PRALAY' if k == 'QUASI' else ''), col, p=seg(t, t0, t0 + .8))
        stroke_pts(ctx, [(90, GND), (590, GND)], 1, B['dim'], a, 2, glow=False)
        sp = (.7 if k == 'CRUISE' else 1.4)
        p = min(1, max(0, (t - t0 - .4)*sp/3)) if k != 'QUASI' else min(1, max(0, (t - t0 - .4)/2.4))
        pts = list(PATHS[k])
        stroke_pts(ctx, pts, p, col, a, 3)
        if 0 < p < 1:
            hx_, hy_, ang = head_pt(pts, p); missile(ctx, hx_, hy_, 70, ang, a, col=col)
        txt(ctx, sub, 340, 920 - 70, 20, col, a, 'bold', 'c', mono=True)
        # radar watching
        radar(ctx, 560, GND, .5, a, t, aim=-.9)
        if k == 'BALLISTIC' and p > .25:
            # the radar predicts the landing point, and an interceptor rises to meet it
            stroke_pts(ctx, PATHS[k][int(60*p):], 1, B['ice'], a*.4, 2, glow=False, dash=[8, 10])
            glow_dot(ctx, 590, GND, 6, B['alert'], a*(.5 + .5*math.sin(t*6)))
            if intercept and p > .55:
                ip = min(1, (p - .55)/.4)
                ipts = bez((540, GND), (560, 600), (540, 420), 30)
                stroke_pts(ctx, ipts, ip, B['alert'], a, 2.5)
        ctx.restore()
    if snap is not None and t > snap:
        ox = 1200; q = seg(t, snap, snap + .6)
        ctx.save(); ctx.translate(ox, 0)
        # predicted path (dashed) continues straight; the real one bends away
        pred = bez((450, 570), (540, 565), (600, GND), 20)
        stroke_pts(ctx, pred, 1, B['alert'], a_out*(1 - .6*q), 2, glow=False, dash=[8, 10])
        glow_dot(ctx, 600, GND - 4, 6, B['alert'], a_out*(1 - q))
        tagb(ctx, 340, 300, 'PREDICTION: WRONG', B['alert'], ease(q)*a_out, 22, align='c')
        ctx.restore()
    if speed_tag is not None and t > speed_tag:
        q = seg(t, speed_tag, speed_tag + .5)
        tagb(ctx, W/2, 960, 'HYPERSONIC: MORE THAN 5× THE SPEED OF SOUND (DEFENCE SCIENTIST, NOV 2026)', B['amber'], ease(q)*a_out, 24, align='c')

def s_fly1(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'THREE WAYS TO FLY', a_out)
    _panel_paths(ctx, t, D, [Ts('One: ballistic') - .2, None, None], a_out, intercept=t > Ts('send an interceptor') - 2)
scene(s_fly1)
def s_fly2(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'THREE WAYS TO FLY', a_out)
    _panel_paths(ctx, t, D, [-5, Ts('Two: cruise') - .2, Ts('And three') - .2], a_out, intercept=True)
scene(s_fly2)
def s_fly3(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'THREE WAYS TO FLY', a_out)
    _panel_paths(ctx, t, D, [-5, -5, -1.5], a_out, snap=Ts('and then it doesn\'t') - .3, intercept=True, speed_tag=Ts('hypersonic speed'))
    q = seg(t, Ts('evade interceptor'), Ts('evade interceptor') + .4)
    if q > 0: tagb(ctx, W/2, 140 + 0, 'DESIGNED TO EVADE INTERCEPTORS (DEFENCE SOURCES TO THEPRINT)', B['cyan'], ease(q)*a_out*(1 - seg(t, Ts('hypersonic speed') - .3, Ts('hypersonic speed'))), 22, align='c')
scene(s_fly3)

# ---------- shoot and scoot ----------
def s_scoot1(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'THE LAUNCHER', a_out)
    ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
    tl_ = Ts('Older missiles'); q = seg(t, tl_ - .2, tl_ + .5)
    if q > 0:
        a = ease(q)*a_out
        card(ctx, 100, 180, 820, 640, a, 'OLDER: LIQUID FUEL', B['steel'], p=q)
        missile(ctx, 510, 470, 520, -math.pi/2, a, col=B['steel'])
        # fuel hose + filling gauge
        stroke_pts(ctx, bez((200, 760), (260, 560), (470, 560), 20), 1, B['dim'], a, 4, glow=False)
        g = min(1, max(0, (t - tl_)/6))
        fill(ctx, lambda: rrect(ctx, 720, 700 - 300*g, 60, 300*g, 4), B['steel'], .5*a)
        stroke_pts(ctx, rect_pts(720, 400, 60, 300), 1, B['steel'], a, 2, glow=False)
        txt(ctx, f'FUELLING… {int(g*100)}%', 750, 760, 22, B['steel'], a, 'bold', 'c', mono=True)
        tagb(ctx, 510, 860 - 40, 'TAKES TIME · CAN GIVE THE GAME AWAY', B['alert'], ease(seg(t, Ts('give the game away') - .2, Ts('give the game away') + .3))*a_out, 20, align='c')
    tp = Ts("Pralay's solid fuel"); q = seg(t, tp - .2, tp + .5)
    if q > 0:
        a = ease(q)*a_out
        card(ctx, 1000, 180, 820, 640, a, 'PRALAY: SOLID FUEL, SEALED', B['amber'], p=q)
        fill(ctx, lambda: rrect(ctx, 1350, 260, 120, 470, 14), B['cyan'], .1*a)
        stroke_pts(ctx, rect_pts(1350, 260, 120, 470), q, B['ice'], a, 3)
        missile(ctx, 1410, 500, 400, -math.pi/2, a)
        tagb(ctx, 1410, 820, 'ALREADY FUELLED · READY', B['amber'], ease(seg(t, tp + .8, tp + 1.2))*a_out, 22, align='c')
    ctx.restore()
scene(s_scoot1)

def s_scoot2(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'SHOOT AND SCOOT', a_out)
    stroke_pts(ctx, [(0, 760), (W, 760)], 1, B['dim'], a_out, 2, glow=False)
    td, ts, tr, tf, tm = Ts('drives in'), Ts('stops'), Ts('raises the tube'), Ts('fires'), Ts('moves on')
    x = lerp(-400, 820, eoc(seg(t, td - .5, ts))) + lerp(0, 1500, ease(seg(t, tm, tm + 3)))
    rz = ease(seg(t, tr - .2, tr + 1.4))*(1 - ease(seg(t, tf + .6, tm + .2)))
    truck(ctx, x, 760, .9, a_out, t, raise_=rz, canister=True, wheels_spin=-x*.03)
    if t > tf:
        q = seg(t, tf, tf + 2.2)
        px0, py0 = 820 - 260*.9, 760 - 86*.9 - 440*.9
        pts = bez((px0, py0), (px0 + 40, py0 - 300), (px0 + 500, -200), 30)
        stroke_pts(ctx, pts, q, B['ice'], a_out*(1 - seg(t, tf + 2.5, tf + 4)), 3)
        glow_dot(ctx, px0, py0 + 20, 26*(1 - seg(t, tf, tf + .8)) + 2, B['amber'], (1 - seg(t, tf, tf + .8))*a_out)
    steps = [('DRIVE IN', td), ('STOP', ts), ('RAISE', tr), ('FIRE', tf), ('MOVE ON', tm)]
    for i, (s_, t0) in enumerate(steps):
        on = t >= t0 - .1
        x0 = 230 + i*300
        fill(ctx, lambda: rrect(ctx, x0, 170, 250, 70, 8), B['amber'] if on else B['deep'], (.25 if on else .7)*a_out)
        ctx.new_path(); rgba(ctx, B['amber'] if on else B['dim'], a_out); ctx.set_line_width(2); rrect(ctx, x0, 170, 250, 70, 8); ctx.stroke()
        txt(ctx, f'{i+1} · {s_}', x0 + 125, 215, 24, B['ice'] if on else B['dim'], a_out, 'bold', 'c', mono=True)
    tq = Ts('shoot and scoot'); q = seg(t, tq, tq + .5)
    if q > 0:
        ctx.save(); ctx.translate(W/2, 420); ctx.scale(lerp(1.5, 1, eob(q, 1.4)), lerp(1.5, 1, eob(q, 1.4)))
        txt(ctx, 'SHOOT & SCOOT', 0, 0, 110, B['amber'], ease(q*2)*a_out, 'black', 'c', glow=1.2); ctx.restore()
    th = Ts('far harder to find'); q = seg(t, th, th + .4)
    if q > 0: tagb(ctx, W/2, 900, 'HARDER TO FIND · HARDER TO HIT BACK', B['cyan'], ease(q)*a_out, 26, align='c')
scene(s_scoot2)

# ---------- the road to Pralay ----------
ROAD = [  # (x, label, sub, cue)
    (0, '30+ YEARS AGO', 'PRITHVI JOINS THE FORCES', 'Prithvi'),
    (520, '2011', 'PRAHAAR FIRST TESTED', 'In 2011'),
    (1040, '2015', 'PROJECT SANCTIONED · ~₹333 CRORE', 'sanctioned in 2015'),
    (1560, '22–23 DEC 2021', 'FIRST TWO TEST FLIGHTS', 'The first two test flights'),
    (2080, 'MID-2020 → 2022', 'LAC CLASHES · ARMY ASKS FOR PRALAY', 'Meanwhile'),
    (2600, '7 NOV 2023', 'ANOTHER TEST', 'Another test'),
    (3120, '26 JAN 2025', 'REPUBLIC DAY PARADE', 'On the twenty-sixth of January'),
    (3640, '28–29 JUL 2025', 'BACK-TO-BACK: LONGEST + SHORTEST RANGE', 'twenty-eighth and twenty-ninth'),
    (4160, '5 NOV 2026', 'USER TRIAL BY THE ARMED FORCES', 'And on the fifth'),
]
def road(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'THE ROAD TO PRALAY', a_out)
        cx = ROAD[max(first - 1, 0)][0]
        for (x, l, s_, cue) in ROAD:
            tc = Ts(cue)
            if tc < 900: cx = lerp(cx, x, ease(seg(t, tc - .5, tc + .7)))
        ctx.save(); ctx.translate(W/2 - 260 - cx, 0)
        stroke_pts(ctx, [(-600, 560), (4800, 560)], 1, B['dim'], a_out, 2, glow=False)
        for i, (x, l, s_, cue) in enumerate(ROAD):
            tc = Ts(cue)
            q = 1. if (tc >= 900 and i < first) else (seg(t, tc - .2, tc + .5) if tc < 900 else 0)
            if q <= 0:
                glow_dot(ctx, x, 560, 4, B['dim'], .4*a_out); continue
            a = ease(q*1.5)*a_out
            glow_dot(ctx, x, 560, 9, B['amber'] if i in (3, 8) else B['cyan'], a)
            stroke_pts(ctx, [(x, 560), (x, 440)], q, B['cyan'], a, 2, glow=False)
            txt(ctx, l, x, 410, 46 if len(l) < 12 else 36, B['ice'], a, 'black', 'c', glow=.6)
            for j, ln in enumerate(wrap(ctx, s_, 24, 440, 'bold', True)):
                txt(ctx, ln, x, 630 + j*34, 24, B['cyan'], a, 'bold', 'c', mono=True)
            if i == 6:   # a parade: a small launcher rolls along
                truck(ctx, x, 800, .32, a, t, raise_=.0, wheels_spin=-t*3)
            if i in (3, 5, 7, 8):
                pts = bez((x - 120, 880), (x, 700), (x + 120, 880), 20)
                stroke_pts(ctx, pts, seg(t, tc + .2, tc + 1.6) if tc < 900 else 1, B['ice'], a*.8, 2.5)
        ctx.restore()
        if first == 6:
            tr = Ts('Reports say'); q = seg(t, tr, tr + .4)
            if q > 0: tagb(ctx, W/2, 960, 'REPORTS: ORDERS CLEARED FOR THE ARMY AND THE AIR FORCE', B['amber'], ease(q)*a_out, 24, align='c')
    return scene(f)

# ---------- the gap it fills ----------
def _xlog(km): return 260 + (math.log10(km) - 1)*470       # 10 km .. 10,000 km across the screen
def s_gap1(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'THE LADDER OF REACH', a_out)
    ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=540)
    y = 640
    stroke_pts(ctx, [(_xlog(10), y), (_xlog(10000), y)], fadein(t, .2, 1), B['dim'], a_out, 2, glow=False)
    for km in (10, 100, 1000, 10000):
        x = _xlog(km); stroke_pts(ctx, [(x, y - 10), (x, y + 10)], 1, B['dim'], a_out, 2, glow=False)
        txt(ctx, f'{km:,} KM', x, y + 50, 22, B['dim'], a_out, 'bold', 'c', mono=True)
    bars = [('PINAKA · ROCKETS', 10, 90, B['steel'], 'like Pinaka', 'TENS OF KM'), ('AGNI · STRATEGIC', 700, 8000, B['ice'], 'the Agni missiles', '700–8,000 KM')]
    for i, (nm, k0, k1, col, cue, sub) in enumerate(bars):
        q = seg(t, Ts(cue) - .1, Ts(cue) + .8)
        if q <= 0: continue
        x0, x1 = _xlog(k0), lerp(_xlog(k0), _xlog(k1), eoc(q))
        fill(ctx, lambda: rrect(ctx, x0, y - 120 - i*0, x1 - x0, 70, 8), col, .22*a_out)
        stroke_pts(ctx, rect_pts(x0, y - 120, x1 - x0, 70), 1, col, a_out, 2.5)
        txt(ctx, nm, x0 + 16, y - 75, 26, col, ease(q)*a_out, 'bold', mono=True)
        txt(ctx, sub, x0 + 16, y - 140, 22, col, ease(q)*a_out, 'bold', mono=True)
    tg = Ts('there was a gap'); q = seg(t, tg, tg + .5)
    if q > 0 and t < Ts('Pralay fills it') + .3:
        gx0, gx1 = _xlog(100), _xlog(600)
        stroke_pts(ctx, rect_pts(gx0, y - 260, gx1 - gx0, 90), q, B['alert'], a_out*(.6 + .4*math.sin(t*6)), 2.5, dash=[10, 8])
        txt(ctx, 'THE GAP', (gx0 + gx1)/2, y - 290, 32, B['alert'], ease(q)*a_out, 'black', 'c')
    tf = Ts('Pralay fills it'); q = seg(t, tf, tf + .7)
    if q > 0:
        x0, x1 = _xlog(150), _xlog(500)
        yy = lerp(160, y - 250, eob(q, 1.3))
        fill(ctx, lambda: rrect(ctx, x0, yy, x1 - x0, 70, 8), B['amber'], .3*a_out)
        stroke_pts(ctx, rect_pts(x0, yy, x1 - x0, 70), 1, B['amber'], a_out, 3)
        txt(ctx, 'PRALAY · 150–500 KM', (x0 + x1)/2, yy + 46, 26, B['ice'], a_out, 'black', 'c')
    for j, (cue, s_) in enumerate((('airfields', 'AIRFIELDS'), ('radar sites', 'RADAR SITES'), ('command centres', 'COMMAND CENTRES'))):
        q = seg(t, Ts(cue) - .1, Ts(cue) + .3)
        if q > 0: tagb(ctx, 600 + j*360, 820, s_, B['cyan'], ease(q)*a_out, 24, align='c')
    ctx.restore()
scene(s_gap1)

def s_gap2(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'CONVENTIONAL, NOT NUCLEAR', a_out)
    ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
    q = seg(t, .3, .9)
    txt(ctx, 'CONVENTIONAL', W/2, 270, 100, B['amber'], ease(q*2)*a_out, 'black', 'c', glow=1)
    for i, (head, lines, col, cue) in enumerate((('PRALAY', ['Conventional missile (DRDO)', 'For the battlefield'], B['amber'], 'DRDO describes'),
                                                  ('NUCLEAR WEAPONS', ['Held by a separate command:', 'Strategic Forces Command'], B['ice'], 'separate command'))):
        qq = seg(t, Ts(cue) - .2, Ts(cue) + .6)
        if qq <= 0: continue
        x = 260 + i*740; a = ease(qq)*a_out
        card(ctx, x, 380, 660, 380, a, head, col, p=qq)
        for j, l in enumerate(lines): txt(ctx, l, x + 40, 520 + j*60, 34, B['ice'], a, 'bold')
    tb = Ts('meant for the battlefield'); q = seg(t, tb, tb + .4)
    if q > 0: tagb(ctx, W/2, 860, 'BATTLEFIELD, NOT DETERRENCE', B['amber'], ease(q)*a_out, 30, align='c')
    ctx.restore()
scene(s_gap2)

# ---------- head to head ----------
def s_h2h1(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'HEAD TO HEAD · PRALAY VS BRAHMOS', a_out)
    for i, (nm, col, cue, path, edge) in enumerate((('BRAHMOS', B['steel'], 'with BrahMos', [(140 + k*12, 720 - 20*math.sin(k*.35)) for k in range(51)], 'AGILITY · STEALTH'),
                                                  ('PRALAY', B['amber'], 'Pralay climbs', bez((140, 760), (380, 260), (560, 420), 30) + bez((560, 420), (640, 470), (700, 760), 15)[1:], 'SPEED'))):
        tc = Ts(cue); q = seg(t, tc - .3, tc + .5)
        if q <= 0: continue
        x0 = 100 + i*880; a = ease(q)*a_out
        ctx.save(); ctx.translate(x0, 0)
        card(ctx, 0, 170, 820, 700, a, nm, col, p=q)
        stroke_pts(ctx, [(40, 780), (780, 780)], 1, B['dim'], a, 2, glow=False)
        pp = min(1, max(0, (t - tc)/(3.2 if i == 0 else 2.0)))
        pts = [(x_, y_) for x_, y_ in path]
        stroke_pts(ctx, pts, pp, col, a, 3)
        if 0 < pp < 1:
            hx_, hy_, ang = head_pt(pts, pp); missile(ctx, hx_, hy_, 80, ang, a, col=col)
        te = Ts("Pralay's edge is speed"); qe = seg(t, te + (0 if i else 1.2), te + .5 + (0 if i else 1.2))
        if qe > 0: tagb(ctx, 410, 840, 'EDGE: ' + edge, col, ease(qe)*a_out, 24, align='c')
        ctx.restore()
    tt = Ts('they\'re a team'); q = seg(t, tt, tt + .5)
    if q > 0:
        ctx.save(); ctx.translate(W/2, 520); ctx.scale(eob(q, 1.8), eob(q, 1.8))
        tagb(ctx, 0, 0, 'NOT RIVALS · A TEAM', B['cyan'], ease(q*2)*a_out, 34, align='c'); ctx.restore()
scene(s_h2h1)

COUS = [('ISKANDER', 'RUSSIA', "Russia's Iskander"), ('DONG FENG-12', 'CHINA', 'Dong Feng-12'), ('PrSM', 'UNITED STATES', 'Precision Strike'), ('HYUNMOO-2', 'SOUTH KOREA', 'Hyunmoo-2'), ('PRALAY', 'INDIA', 'Abroad')]
def s_h2h2(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'GLOBAL COUSINS', a_out)
    tq = Ts('And India\'s neighbours'); sw = ease(seg(t, tq - .3, tq + .5))
    ctx.save(); ctx.translate(0, -150*sw); ctx.translate(W/2, 470); ctx.scale(1 - .25*sw, 1 - .25*sw); ctx.translate(-W/2, -470)
    for i, (nm, ctry, cue) in enumerate(COUS):
        q = seg(t, Ts(cue) - .1, Ts(cue) + .5)
        if q <= 0: continue
        x = 230 + i*365; a = ease(q)*a_out*(1 - .5*sw); col = B['amber'] if nm == 'PRALAY' else B['ice']
        missile(ctx, x, 470, 300, -math.pi/2, a, p=seg(t, Ts(cue), Ts(cue) + 1), col=col)
        txt(ctx, nm, x, 690, 30, col, a, 'black', 'c')
        txt(ctx, ctry, x, 730, 20, B['cyan'], a, 'bold', 'c', mono=True)
        if nm == 'ISKANDER': txt(ctx, 'USED IN UKRAINE', x, 765, 18, B['dim'], ease(seg(t, Ts('used in the war') - .1, Ts('used in the war') + .3))*a, 'bold', 'c', mono=True)
    ctx.restore()
    if sw > 0:
        a = sw*a_out
        card(ctx, 260, 540, 1400, 330, a, 'ARMY CHIEF GEN UPENDRA DWIVEDI · 13 JAN 2026 (VIA ANI)', B['cyan'], p=sw)
        q1 = seg(t, Ts('"Pakistan has established'), Ts('"Pakistan has established') + 1.5)
        txt(ctx, typed('"Pakistan has established a rocket force."', q1), 300, 660, 44, B['ice'], a, 'bold')
        q2 = seg(t, Ts('"It is the need'), Ts('"It is the need') + 2.4)
        for j, l in enumerate(wrap(ctx, '"It is the need of the hour that we also establish such a force."', 40, 1320, 'bold')):
            txt(ctx, typed(l, q2*2 - j), 300, 740 + j*56, 40, B['amber'], a, 'bold')
scene(s_h2h2)

# ---------- the debate ----------
def s_deb1(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'THE BIG DEBATE · WHO CONTROLS THE MISSILES?', a_out)
    ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
    cols = [('ARMY', 340), ('AIR FORCE', 960), ('NAVY', 1580)]
    for nm, x in cols:
        card(ctx, x - 250, 360, 500, 460, fadein(t, .2)*a_out, nm, B['steel'], p=seg(t, .2, 1))
    assets = [('PRALAY', 340, 960), ('BRAHMOS', 960, 340), ('PINAKA', 340, 1580)]
    for i, (nm, x0, x1) in enumerate(assets):
        x = lerp(x0, x1, .5 + .5*math.sin(t*.7 + i*2)) if t > 2 else x0
        tagb(ctx, x, 520 + i*90, nm, B['amber'] if nm == 'PRALAY' else B['cyan'], fadein(t, .6 + i*.2)*a_out, 26, align='c')
    q = seg(t, Ts('who should control'), Ts('who should control') + .5)
    if q > 0: txt(ctx, 'WHO SHOULD CONTROL THEM?', W/2, 270, 64, B['ice'], ease(q)*a_out, 'black', 'c', glow=1)
    q = seg(t, Ts('General Bipin Rawat'), Ts('General Bipin Rawat') + .4)
    if q > 0: tagb(ctx, W/2, 900, "IDEA OF A ROCKET FORCE: GEN BIPIN RAWAT, INDIA'S FIRST CDS", B['cyan'], ease(q)*a_out, 24, align='c')
    ctx.restore()
scene(s_deb1)

def s_deb2(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'THE BIG DEBATE', a_out)
    sides = [('THE CASE FOR A ROCKET FORCE', 'BRIG ANIL RAMAN (RETD)', ['Strike weapons are spread across', 'the Army, Air Force and Navy', 'One command decides faster', 'in a crisis'], 'Supporters'),
             ('THE CASE AGAINST', 'AIR MARSHAL NARMDESHWAR TIWARI (RETD)', ['Only China and Russia have', 'created such a force', 'Invest in modern fighter', 'aircraft instead'], 'Critics')]
    for i, (head, who, lines, cue) in enumerate(sides):
        tc = Ts(cue); q = seg(t, tc - .2, tc + .6)
        if q <= 0: continue
        x = 120 + i*860; a = ease(q)*a_out
        card(ctx, x, 180, 820, 640, a, head, B['cyan'], p=q)
        figure(ctx, x + 120, 420, 1.0, B['ice'], a, t, seed=i)
        txt(ctx, who, x + 220, 330, 22, B['amber'], a, 'bold', mono=True)
        for j, l in enumerate(lines): txt(ctx, l, x + 50, 520 + j*58, 34, B['ice'], ease(seg(t, tc + .3 + j*.25, tc + .7 + j*.25))*a_out, 'bold' if j % 2 == 0 else 'reg')
    q = seg(t, Ts('The government has not'), Ts('The government has not') + .4)
    if q > 0: tagb(ctx, W/2, 900, 'NO FINAL STRUCTURE ANNOUNCED YET', B['ice'], ease(q)*a_out, 28, align='c')
scene(s_deb2)

# ---------- in three words ----------
def s_three(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'PRALAY IN THREE WORDS', a_out)
    path = bez((150, 820), (500, 300), (1150, 380), 40) + bez((1150, 380), (1450, 420), (1750, 820), 25)[1:]
    stroke_pts(ctx, path, ease(seg(t, .3, 3.0)), B['amber'], a_out*.6, 3)
    words = [('LOW', 'A FLATTER ARC', 'Low:', 420), ('LATE', 'TURNS IN THE FINAL STAGE', 'Late:', 960), ('LOADED', 'SEALED, SOLID FUEL, READY', 'Loaded:', 1500)]
    for i, (w_, sub, cue, x) in enumerate(words):
        q = seg(t, Ts(cue) - .15, Ts(cue) + .35)
        if q <= 0: continue
        sc = lerp(1.7, 1, eob(q, 1.4))
        ctx.save(); ctx.translate(x, 600); ctx.scale(sc, sc)
        txt(ctx, w_, 0, 0, 130, B['amber'], ease(q*2)*a_out, 'black', 'c', glow=2)
        ctx.restore()
        txt(ctx, sub, x, 680, 24, B['ice'], ease(seg(t, Ts(cue) + .3, Ts(cue) + .7))*a_out, 'bold', 'c', mono=True)
scene(s_three)

# ---------- what's next, and the blueprint wall ----------
def _wall_card(ctx, x, y, w, h, a, t):
    fill(ctx, lambda: rrect(ctx, x, y, w, h, 8), B['deep'], .9*a)
    stroke_pts(ctx, rect_pts(x, y, w, h), 1, B['cyan'], a, 2.5)
    missile(ctx, x + w/2, y + h*.42, w*.8, 0, a)
    txt(ctx, 'EP 1 · PRALAY', x + 24, y + h - 30, 26, B['ice'], a, 'black')
    glow_dot(ctx, x + w/2, y + 14, 6, B['amber'], a)

def s_next(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'WHAT\'S NEXT · AS OF 13 NOV 2026', a_out)
    items = [('INDUCTION', '"Imminent" (Defence Ministry)', 'induction is imminent'), ('HOW MANY?', 'Not announced', 'how many missiles'), ('WHO COMMANDS?', 'Not announced', 'who will command')]
    for i, (k, v, cue) in enumerate(items):
        q = seg(t, Ts(cue) - .2, Ts(cue) + .4)
        if q <= 0: continue
        y = 260 + i*190; a = ease(q)*a_out
        card(ctx, 260, y, 1400, 150, a, None, B['amber'] if i == 0 else B['cyan'], p=q)
        txt(ctx, f'0{i+1}', 310, y + 98, 64, B['amber'] if i == 0 else B['cyan'], a, 'black', glow=.8)
        txt(ctx, k, 460, y + 70, 40, B['ice'], a, 'black')
        txt(ctx, v, 460, y + 118, 28, B['steel'], a, 'bold')
scene(s_next)

def s_end(ctx, t, D):
    bg(ctx); a_out = outro(t, D, .8)
    hud(ctx, t, "THE BLUEPRINT WALL · INDIA'S DEFENCE, DECODED", a_out)
    # the wall: a grid of slots, the first one gets pinned
    for i in range(10):
        x = 160 + (i % 5)*330; y = 200 + (i//5)*300
        if i == 0: continue
        stroke_pts(ctx, rect_pts(x, y, 290, 240), 1, B['grid'], a_out, 2, glow=False, dash=[10, 10])
        txt(ctx, f'EP {i+1}', x + 145, y + 130, 24, B['grid'], a_out, 'bold', 'c', mono=True)
    q = seg(t, .3, 1.0)
    yy = lerp(-300, 200, eob(q, 1.3))
    _wall_card(ctx, 160, yy, 290, 240, a_out, t)
    tn = Ts('Next on'); nq = seg(t, tn, tn + .6)
    if nq > 0:
        a = ease(nq)*a_out
        fill(ctx, lambda: ctx.rectangle(0, 830, W*eoc(nq), 90), B['deep'], .95*a)
        rgba(ctx, B['cyan'], a); ctx.rectangle(0, 830, W*eoc(nq), 3); ctx.fill()
        txt(ctx, 'NEXT  ·  BRAHMOS, THE MISSILE INDIA BUILT WITH RUSSIA', 80, 888, 34, B['ice'], a, 'bold', mono=True)
        stroke_pts(ctx, rect_pts(490, 200, 290, 240), nq, B['amber'], a, 2.5)
        txt(ctx, 'EP 2 · BRAHMOS', 635, 330, 26, B['amber'], a, 'black', 'c')
    subscribe_card(ctx, t, Ts('subscribe'), a_out, x=1540, y=720)
scene(s_end)

# ---------- beats ----------
SC = {
 'cold1': s_cold1, 'cold2': s_cold2, 'spec1': s_spec1, 'spec2': s_spec2, 'far': s_far,
 'fly1': s_fly1, 'fly2': s_fly2, 'fly3': s_fly3, 'scoot1': s_scoot1, 'scoot2': s_scoot2,
 'road1': road(0), 'road2': road(3), 'road3': road(6), 'gap1': s_gap1, 'gap2': s_gap2,
 'h2h1': s_h2h1, 'h2h2': s_h2h2, 'deb1': s_deb1, 'deb2': s_deb2, 'three': s_three, 'next': s_next, 'end': s_end,
}
BEATS = [(k, n, SC[k]) for k, n in EN]
GROUPS = {'cold1': 'cold', 'cold2': 'cold', 'spec1': 'spec', 'spec2': 'spec', 'fly1': 'fly', 'fly2': 'fly', 'fly3': 'fly',
          'road1': 'road', 'road2': 'road', 'road3': 'road', 'deb1': 'deb', 'deb2': 'deb', 'next': 'nx', 'end': 'nx'}
KEYS = {
 'spec1': [('five tonnes', '~5 TONNES', 'cyan')],
 'far': [('almost exactly five hundred', '≈ 500 KM', 'amber')],
 'fly2': [('change course', 'CHANGES COURSE', 'amber')],
 'scoot2': [('never stays in one place', 'NEVER STAYS PUT', 'cyan')],
 'road1': [('three hundred and thirty-three crore', '~₹333 CRORE', 'cyan')],
 'gap2': [('Strategic Forces Command', 'STRATEGIC FORCES COMMAND', 'ice')],
 'h2h1': [('supersonic cruise missile', 'SUPERSONIC CRUISE', 'steel')],
}
ANNOT = {
 'fly3': [("and then it doesn't", 'circle', 1660, 640, 260, 360)],
 'gap1': [('Pralay fills it', 'circle', 1020, 425, 520, 140)],
}
_order = [k for k, _ in EN]
FX = [('whoosh', k, -.25, .22) for i, k in enumerate(_order) if i and GROUPS.get(k, k) != GROUPS.get(_order[i-1], _order[i-1])]
FX += [('beep', k, ph, .14) for k, items in KEYS.items() for ph, _, _ in items]
FX += [('tick', 'cold1', .15, .12), ('beep', 'cold1', 'Then fire', .3), ('boom', 'cold1', 'Then fire', .55), ('boom', 'cold1', 'hits its target', .35),
       ('riser', 'cold2', 'This is Pralay', .25), ('boom', 'cold2', 'This is Pralay', .55),
       ('ping', 'fly1', 'Once a radar', .3), ('glitch', 'fly3', "and then it doesn't", .3), ('boom', 'scoot2', 'fires', .45),
       ('stamp', 'scoot2', 'shoot and scoot', .3), ('boom', 'gap1', 'Pralay fills it', .35),
       ('riser', 'three', 'Low:', .15), ('ding', 'three', 'Low:', .25), ('ding', 'three', 'Late:', .25), ('ding', 'three', 'Loaded:', .25),
       ('stamp', 'end', .5, .35), ('ding', 'end', 'subscribe', .2)]
