"""India's Defence, Decoded — Episode 3: Agni-5 and MIRV (bilingual: English + Hindi).
No maps in this episode: range is expressed in time, never drawn over anyone's territory."""
import os, sys, math, random, cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 780.0
core.TOTAL = TOTAL
from engine.core import W, H, seg, ease, eoc, eob, lerp, T
from engine.bp import (B, rgba, rrect, bg, txt, tw, typed, wrap, para, stroke_pts, head_pt, rect_pts, fill, glow_dot, bez,
                       missile, truck, figure, radar, hud, card, tagb, outro, camera, scene, subscribe_card, face)
from engine.mil import waves, axes, dot, bar, pin, schematic_note
from text import EN, HI as _HI

EP = 3
CODE = 'Def03'
TITLE = 'Agni5_and_MIRV'
NAME = 'How India Actually Built an ICBM: Agni-5 and MIRV'
POST = 'engine.bp'
BED = 'pulse'
VOICE_EN = {'length': 0.98, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
VOICE_HI = {'length': 0.86, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
CRF, PRESET = 17, 'medium'
EXTRA = {'cold1': .8, 'bus3': .6, 'three1': 1.2, 'end1': 2.5}
HI = _HI

def Ts(x):
    try: return T(x)
    except ValueError: return 999.
def fin(t, t0=.1, d=.5): return ease(seg(t, t0, t0 + d))

# ---------- shared: a MIRV release, used in several scenes ----------
def mirv_arcs(ctx, t, a, p, apex=(960, 250), ends=((420, 880), (870, 900), (1500, 870)), col=None, bus=True, label_bus=0.):
    """the climb, the bus at apogee, and the separate descents. p drives the whole sequence 0..1"""
    col = col or B['amber']
    up = bez((230, 900), (430, 520), apex, 34)
    pu = min(1, p/.42)
    stroke_pts(ctx, up, pu, col, a*.85, 4)
    if pu < 1:
        hx_, hy_, ang = head_pt(up, pu); missile(ctx, hx_, hy_, 120, ang, a, col=col)
        return
    if bus:
        bq = min(1, (p - .42)/.12)
        bx, by = apex
        fill(ctx, lambda: rrect(ctx, bx - 56, by - 26, 112, 52, 8), B['deep'], .9*a)
        stroke_pts(ctx, rect_pts(bx - 56, by - 26, 112, 52), bq, B['ice'], a, 3)
        for k in range(3):
            glow_dot(ctx, bx - 32 + k*32, by, 8, col, a*bq*(1 if p < .55 + k*.14 else .25))
        if label_bus > 0:
            txt(ctx, 'THE BUS', bx, by - 56, 34, B['ice'], a*label_bus, 'black', 'c', glow=.8)
    for k, end in enumerate(ends):
        t0 = .56 + k*.13
        q = min(1, max(0, (p - t0)/.30))
        if q <= 0: continue
        down = bez(apex, (lerp(apex[0], end[0], .55), apex[1] + 120), end, 30)
        stroke_pts(ctx, down, q, col, a*.9, 3)
        hx_, hy_, ang = head_pt(down, q)
        if q < 1: glow_dot(ctx, hx_, hy_, 7, col, a)
        else:
            for r_ in range(2):
                rp = min(1, max(0, (p - t0 - .30 - r_*.08)*4))
                if rp > 0:
                    ctx.new_path(); rgba(ctx, col, (1 - rp)*a); ctx.set_line_width(3); ctx.arc(end[0], end[1], 14 + 70*rp, 0, 2*math.pi); ctx.stroke()

# ================= cold open: the mystery missile =================
def s_cold(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D, .35)
        hud(ctx, t, 'ODISHA COAST · 8 MAY 2026 · EVENING', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=600)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        waves(ctx, 880, t, a*.8)
        for _k in range(9):
            figure(ctx, 190 + _k*118, 836, .42, B['dim'], a*.55, t, seed=_k)
        stroke_pts(ctx, [(0, 850), (760, 850), (900, 836), (W, 836)], 1, B['ice'], a*.6, 2, glow=False)
        # the climb out of frame
        tr = Ts('climb out of the sky')
        p = eoc(seg(t, .4, 3.4)) if first == 0 else 1.
        up = bez((600, 846), (760, 400), (1180, -160), 34)
        stroke_pts(ctx, up, p, B['amber'], a*.8, 4)
        if 0 < p < 1:
            hx_, hy_, ang = head_pt(up, p); missile(ctx, hx_, hy_, 130, ang, a, col=B['amber'])
            glow_dot(ctx, hx_ - 60*math.cos(ang), hy_ - 60*math.sin(ang), 10, B['amber'], a)
        # the silence
        ts = Ts('And then: nothing')
        sq = seg(t, ts, ts + .5)
        if sq > 0:
            qa = ease(sq)*a_out
            txt(ctx, 'NO ANNOUNCEMENT', 180, 330, 62, B['steel'], qa*ease(seg(t, Ts('No announcement') - .2, Ts('No announcement') + .3)), 'black')
            cur = '_' if int(t*2) % 2 else ' '
            txt(ctx, 'DRDO' + ' '*6 + cur, 180, 420, 36, B['dim'], qa, 'bold', mono=True)
            txt(ctx, 'GOVERNMENT' + cur, 180, 480, 36, B['dim'], qa, 'bold', mono=True)
        # the speculation
        tm = Ts('mystery missile')
        if tm < 900 and t > tm - 1.0:
            rr = random.Random(2)
            for k in range(7):
                q = seg(t, tm - 1.0 + k*.22, tm - .5 + k*.22)
                if q <= 0: continue
                x = 1230 + rr.uniform(-150, 110); y = 250 + k*84
                tagb(ctx, x, y, 'MYSTERY MISSILE', B['steel'], ease(q)*a_out*.8, 26, align='c')
        ctx.restore()
        # the official post
        tp = Ts('the Defence Ministry finally posted')
        q = seg(t, tp - .3, tp + .4)
        if q > 0:
            qa = ease(q)*a_out
            card(ctx, 220, 300, 1480, 400, qa, 'MINISTRY OF DEFENCE', B['amber'], p=q)
            for j, l in enumerate(wrap(ctx, 'An advanced Agni missile carrying MIRV. Payloads aimed at different points, spread across a large area of the Indian Ocean.', 44, 1380, 'bold')):
                txt(ctx, l, 270, 450 + j*62, 44, B['ice'], qa*ease(seg(t, tp + .2 + j*.3, tp + .6 + j*.3)), 'bold')
    return scene(f)

# ================= the anchor: what MIRV actually is =================
def s_bus(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'THE SIMPLE VERSION FIRST', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        # the acronym unpacking
        tm = Ts('MIRV stands for')
        if tm < 900:
            q = seg(t, tm - .2, tm + .5)
            if q > 0:
                txt(ctx, 'M I R V', W/2, 300, 120, B['ice'], ease(q)*a_out, 'black', 'c', glow=1)
                for j, (w_, cue) in enumerate((('MANY', 'many,'), ('INDEPENDENT', 'independent,'), ('TARGETS', 'targets.'))):
                    qq = seg(t, Ts(cue) - .15, Ts(cue) + .35)
                    if qq > 0: tagb(ctx, 420 + j*540, 430, w_, B['amber'], ease(qq)*a_out, 40, align='c')
            tn = Ts('A normal ballistic missile')
            if tn < 900 and t > tn - .3:
                na = ease(seg(t, tn - .3, tn + .3))*a_out
                stroke_pts(ctx, bez((300, 880), (600, 560), (900, 880), 26), eoc(seg(t, tn, tn + 1.4)), B['steel'], na, 3)
                txt(ctx, 'ONE WARHEAD, ONE PLACE', 600, 930, 24, B['steel'], na, 'bold', 'c', mono=True)
            tv = Ts('A MIRVed missile carries several')
            if tv < 900 and t > tv - .3:
                va = ease(seg(t, tv - .3, tv + .3))*a_out
                base = bez((1080, 880), (1340, 540), (1600, 640), 26)
                stroke_pts(ctx, base, eoc(seg(t, tv, tv + 1.0)), B['amber'], va, 3)
                for k, ex in enumerate((1360, 1600, 1820)):
                    qq = eoc(seg(t, tv + .8 + k*.2, tv + 1.5 + k*.2))
                    if qq > 0: stroke_pts(ctx, bez((1600, 640), (lerp(1600, ex, .5), 760), (ex, 900), 20), qq, B['amber'], va, 3)
                txt(ctx, 'SEVERAL, EACH SOMEWHERE DIFFERENT', 1450, 950, 24, B['amber'], va, 'bold', 'c', mono=True)
        else:
            # the full sequence, with the bus named
            _c = [c for c in (Ts("Here's the picture"), Ts('That platform steers')) if c < 900]
            go = min(_c) if _c else None
            p = min(1, max(0, (t - go - .2)/7.0)) if go is not None else 1.
            mirv_arcs(ctx, t, a, p, label_bus=ease(seg(t, Ts('They call it the bus') - .2, Ts('They call it the bus') + .4)))
            for cue, lab, x, y in (('releases a platform', 'THE NOSE OPENS', 700, 300),
                                   ('lets one warhead go', 'ONE GOES', 1230, 420),
                                   ('own path', 'EACH ON ITS OWN PATH', 1500, 640)):
                q = seg(t, Ts(cue) - .2, Ts(cue) + .4)
                if q > 0: tagb(ctx, x, y, lab, B['cyan'], ease(q)*a_out*(1 - seg(t, Ts(cue) + 4, Ts(cue) + 5)), 24, align='c')
            tb = Ts('it carries passengers')
            q = seg(t, tb - .3, tb + .5)
            if q > 0:
                qa = ease(q)*a_out
                card(ctx, 1180, 170, 660, 300, qa, 'WHY "BUS"', B['amber'], p=q)
                for j, l in enumerate(('It carries passengers', 'and drops each one', 'at a different stop.')):
                    txt(ctx, l, 1220, 300 + j*54, 36, B['ice'], qa*ease(seg(t, tb + j*.25, tb + .4 + j*.25)), 'bold')
            te = Ts('Everything after this is detail')
            q = seg(t, te - .2, te + .4)
            if q > 0: tagb(ctx, W/2, 960, 'EVERYTHING AFTER THIS IS DETAIL', B['ice'], ease(q)*a_out, 30, align='c')
        ctx.restore()
    return scene(f)

# ================= four questions =================
QS = [('HOW DID INDIA', 'BUILD IT?', 'starting from almost nothing'), ('WHAT IS', 'AGNI-5?', 'exactly'),
      ('WHY MANY', 'WARHEADS?', 'never to strike first'), ('WHERE DOES IT', 'GO NEXT?', 'go next')]
def s_qs(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, "INDIA'S DEFENCE, DECODED · EPISODE 3", a_out, EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
    txt(ctx, 'FOUR QUESTIONS', W/2, 240, 60, B['ice'], ease(seg(t, .2, .8))*a_out, 'black', 'c', glow=.6)
    for i, (k1, k2, cue) in enumerate(QS):
        t0 = Ts(cue) - .2; q = seg(t, t0, t0 + .5)
        if q <= 0: continue
        x = 140 + i*430; y = 330; a = ease(q*2)*a_out; s = eob(q, 1.7)
        ctx.save(); ctx.translate(x + 190, y + 190); ctx.scale(s, s); ctx.translate(-(x + 190), -(y + 190))
        card(ctx, x, y, 380, 380, a, None, B['cyan'] if i % 2 == 0 else B['amber'], p=q)
        txt(ctx, f'0{i+1}', x + 30, y + 130, 96, B['amber'] if i % 2 else B['cyan'], a, 'black', glow=.8)
        txt(ctx, k1, x + 30, y + 230, 26, B['steel'], a, 'bold', mono=True)
        for j, l in enumerate(wrap(ctx, k2, 48, 320, 'black')):
            txt(ctx, l, x + 30, y + 300 + j*54, 48, B['ice'], a, 'black')
        ctx.restore()
    ctx.restore()
scene(s_qs)

# ================= 1983: the programme =================
FIVE = [('PRITHVI', 'SURFACE-TO-SURFACE', 'Prithvi, a short-range'), ('TRISHUL', 'SURFACE-TO-AIR', 'Trishul and Akash'),
        ('AKASH', 'SURFACE-TO-AIR', 'Trishul and Akash'), ('NAG', 'ANTI-TANK', 'Nag, an anti-tank'),
        ('AGNI', 'BALLISTIC', 'And Agni, the ballistic one')]
def s_prog(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'INTEGRATED GUIDED MISSILE DEVELOPMENT PROGRAMME · 1983', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        t83 = Ts('Start in 1983')
        if t83 < 900:
            txt(ctx, '1983', 150, 320, 150, B['amber'], ease(seg(t, t83 - .1, t83 + .4))*a_out, 'black', glow=1)
            txt(ctx, 'ALMOST NO MISSILE INDUSTRY', 150, 380, 28, B['steel'], ease(seg(t, Ts('almost no missile industry') - .2, Ts('almost no missile industry') + .4))*a_out, 'bold', mono=True)
        tk = Ts('Abdul Kalam')
        if t > tk - .3 and tk < 900:
            ka = ease(seg(t, tk - .3, tk + .4))*a_out
            figure(ctx, 1680, 420, 1.5, B['ice'], ka, t, seed=1)
            txt(ctx, 'A.P.J. ABDUL KALAM', 1680, 530, 28, B['ice'], ka, 'black', 'c')
            txt(ctx, 'PROGRAMME DIRECTOR', 1680, 568, 20, B['cyan'], ka, 'bold', 'c', mono=True)
        agni_lit = Ts('And Agni, the ballistic one') < 900 and t > Ts('And Agni, the ballistic one')
        for i, (nm, role, cue) in enumerate(FIVE):
            tc = Ts(cue)
            q = 1. if (tc >= 900 and first > 0) else (seg(t, tc - .15 + (.25 if nm == 'AKASH' else 0), tc + .4 + (.25 if nm == 'AKASH' else 0)) if tc < 900 else 0)
            if q <= 0: continue
            x = 180 + i*300; y = 700; qa = ease(q*1.5)*a_out
            hot = nm == 'AGNI'
            dim = .35 if (agni_lit and not hot) else 1.
            missile(ctx, x, y, 200, -math.pi/2, qa*dim, p=q, col=B['amber'] if hot else B['ice'])
            txt(ctx, nm, x, y + 130, 30, (B['amber'] if hot else B['ice']), qa*dim, 'black', 'c', glow=.5 if hot else 0)
            txt(ctx, role, x, y + 166, 18, B['cyan'], qa*dim*.9, 'bold', 'c', mono=True)
        tf = Ts('Five missiles, one programme')
        if tf < 900:
            q = seg(t, tf - .2, tf + .4)
            if q > 0: tagb(ctx, 560, 560, 'FIVE MISSILES · ONE PROGRAMME', B['cyan'], ease(q)*a_out, 28, align='c')
        # the 1989 re-entry demonstrator
        t89 = Ts('flown from Chandipur in 1989')
        if t89 >= 900 and first > 1: t89 = -2.
        if t89 < 900 and t > t89 - .4:
            qa = ease(seg(t, t89 - .4, t89 + .3))*a_out
            rgba(ctx, B['deep'], .82*qa); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
            txt(ctx, '1989 · CHANDIPUR', W/2, 300, 54, B['ice'], qa, 'black', 'c')
            txt(ctx, 'NOT A WEAPON — A TECHNOLOGY DEMONSTRATOR', W/2, 350, 26, B['cyan'], qa, 'bold', 'c', mono=True)
            # a re-entry glow building down a steep arc
            arc = bez((520, 380), (900, 560), (1180, 880), 30)
            p = eoc(seg(t, t89 + .4, t89 + 3.0)) if first < 2 else 1.
            stroke_pts(ctx, arc, p, B['amber'], qa, 4)
            if p > .2:
                hx_, hy_, ang = head_pt(arc, p)
                for k in range(4):
                    glow_dot(ctx, hx_ - k*18*math.cos(ang), hy_ - k*18*math.sin(ang), 16 - k*3, B['alert'], qa*(.9 - k*.2)*min(1, (p - .2)*3))
            tre = Ts('That problem, re-entry')
            if tre < 900 and t > tre - .2:
                tagb(ctx, 1420, 480, 'RE-ENTRY: THE HARD PART', B['alert'], ease(seg(t, tre - .2, tre + .4))*a_out, 28, align='c')
            trv = Ts('called a re-entry vehicle')
            if trv < 900 and t > trv - .2:
                tagb(ctx, 1420, 560, 'HENCE: RE-ENTRY VEHICLE', B['cyan'], ease(seg(t, trv - .2, trv + .4))*a_out, 24, align='c')
        ctx.restore()
    return scene(f)

# ================= the ladder =================
RUNGS = [('AGNI-1', '700–1,200 KM', 'Agni-1, reaching', .16, B['steel']),
         ('AGNI-2', '2,000–3,500 KM', 'Agni-2, two to three', .36, B['steel']),
         ('AGNI-3', '3,000–5,000 KM', 'Agni-3, three to five', .56, B['cyan']),
         ('AGNI-4', '4,000 KM · LIGHTER', 'Agni-4, four thousand', .72, B['cyan']),
         ('AGNI-5', 'BEYOND 5,000 KM', 'And then, on the nineteenth', 1.0, B['amber'])]
def s_ladder(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'THE LADDER', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=560)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        base, top = 880, 230
        for i, (nm, rng, cue, h, col) in enumerate(RUNGS):
            tc = Ts(cue)
            q = seg(t, tc - .2, tc + .8) if tc < 900 else (1. if first > 0 else 0)
            if q <= 0: continue
            x = 220 + i*320; wd = 230
            hh = (base - top)*h*eoc(q); qa = ease(min(q*2, 1))*a_out
            fill(ctx, lambda: rrect(ctx, x, base - hh, wd, hh, 6), col, .22*qa)
            stroke_pts(ctx, rect_pts(x, base - hh, wd, hh), 1, col, qa, 2.5)
            txt(ctx, nm, x + wd/2, base + 46, 30, col, qa, 'black', 'c')
            txt(ctx, rng, x + wd/2, base - hh - 24, 24, B['ice'], qa, 'bold', 'c', mono=True)
            if nm == 'AGNI-5':
                dq = seg(t, tc + .3, tc + .8)
                if dq > 0: tagb(ctx, x + wd/2, base - hh - 86, '19 APRIL 2012', B['amber'], ease(dq)*a_out, 28, align='c')
        tw_ = Ts('every extra thousand kilometres')
        if tw_ < 900:
            q = seg(t, tw_ - .2, tw_ + .4)
            if q > 0:
                for j, l in enumerate(('MORE STAGES', 'LIGHTER MATERIALS', 'BETTER GUIDANCE', 'A TOUGHER RE-ENTRY VEHICLE')):
                    txt(ctx, l, 150, 300 + j*48, 26, B['cyan'], ease(seg(t, tw_ + .2 + j*.25, tw_ + .6 + j*.25))*a_out, 'bold', mono=True)
        tr = Ts('can only deter your neighbour')
        if tr < 900:
            q = seg(t, tr - .2, tr + .4)
            if q > 0: tagb(ctx, 1280, 300, 'REACH DECIDES WHO TAKES YOU SERIOUSLY', B['amber'], ease(q)*a_out, 28, align='c')
        ctx.restore()
    return scene(f)

# ================= what Agni-5 actually is =================
def s_spec(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'WHAT AGNI-5 ACTUALLY IS', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tclock = Ts('Put it in time instead of distance')
        phase2 = ease(seg(t, tclock - .5, tclock + .3)) if tclock < 900 else (1. if first > 0 else 0)
        if phase2 < 1:
            aa = (1 - phase2)*a
            missile(ctx, W/2, 300, 1340, 0, aa, p=fin(t, .2, 1.2))
            for k, xx in enumerate((520, 900, 1230)):
                stroke_pts(ctx, [(xx, 268), (xx, 332)], fin(t, .6 + k*.15, .4), B['dim'], aa, 2, glow=False)
            txt(ctx, 'THREE STAGES', W/2, 410, 26, B['cyan'], fin(t, .8, .5)*aa, 'bold', 'c', mono=True)
            rows = [('FUEL', 'SOLID', 'running on solid fuel'), ('LENGTH', '~17.5 M', 'seventeen and a half metres'),
                    ('LAUNCH WEIGHT', '~50 TONNES', 'fifty tonnes'), ('RANGE (OFFICIAL)', 'IN EXCESS OF 5,000 KM', 'in excess of five thousand')]
            for i, (k, v, cue) in enumerate(rows):
                q = seg(t, Ts(cue) - .2, Ts(cue) + .4) if Ts(cue) < 900 else 0
                if q <= 0: continue
                y = 520 + i*86; qa = ease(q)*aa
                stroke_pts(ctx, [(300, y + 22), (1620, y + 22)], q, B['grid'], qa, 1.5, glow=False)
                txt(ctx, k, 300, y, 30, B['cyan'], qa, 'bold', mono=True)
                txt(ctx, v, 1620, y, 42, B['ice'], qa, 'black', 'r', glow=.4)
            te = Ts('Outside analysts estimate')
            if te < 900:
                q = seg(t, te - .2, te + .4)
                if q > 0: tagb(ctx, 1200, 930, 'ESTIMATED HIGHER · EXACT FIGURE CLASSIFIED', B['steel'], ease(q)*a_out, 24, align='c')
        if phase2 > 0:
            aa = phase2*a_out
            tcan = Ts('it is canisterised')
            can = ease(seg(t, tcan - .4, tcan + .3)) if tcan < 900 else (1. if first > 1 else 0)
            if can < 1:
                ca = (1 - can)*aa
                for i, (lab, val, col, x, cue) in enumerate((('PASSENGER JET', '6 HOURS', B['steel'], 520, 'about six hours'),
                                                             ('AGNI-5', 'UNDER 20 MINUTES', B['amber'], 1400, 'under twenty minutes'))):
                    q = ease(seg(t, Ts(cue) - .4, Ts(cue) + .3))*ca if Ts(cue) < 900 else ca
                    if q <= 0: continue
                    ctx.new_path(); rgba(ctx, B['dim'], q); ctx.set_line_width(5); ctx.arc(x, 480, 170, 0, 2*math.pi); ctx.stroke()
                    sp = (t*(1/6.0 if i == 0 else 1/0.33)) % 1
                    ctx.new_path(); rgba(ctx, col, q); ctx.set_line_width(9); ctx.arc(x, 480, 170, -math.pi/2, -math.pi/2 + 2*math.pi*sp); ctx.stroke()
                    txt(ctx, val, x, 495, 46 if len(val) < 10 else 36, col, q, 'black', 'c', glow=.6)
                    txt(ctx, lab, x, 700, 30, B['ice'], q, 'black', 'c')
                    txt(ctx, 'TO COVER 5,000 KM', x, 740, 20, B['cyan'], q, 'bold', 'c', mono=True)
            if can > 0:
                ca = can*a_out
                _sc = .85 if first < 2 else 1.2
                _tx = lerp(300, 1250, ease(seg(t, max(tcan, 0) + .6, max(tcan, 0) + 5.0))) if first < 2 else 1000
                _ra = .2 if first < 2 else lerp(.2, .5, ease(seg(t, 1.0, 4.0)))
                truck(ctx, _tx, 760 if first < 2 else 860, _sc, ca, t, raise_=_ra, wheels_spin=-t*2 if first < 2 else 0)
                for j, (l, cue) in enumerate((('SEALED IN A TUBE', 'sealed in a tube'), ('MOVES BY ROAD', 'able to move by road'),
                                              ('A KNOWN SILO CAN BE TARGETED', 'whose location is known'), ('SURVIVABILITY IS THE POINT', 'Survivability is the entire point'))):
                    q = seg(t, Ts(cue) - .2, Ts(cue) + .4)
                    if q > 0: tagb(ctx, 420, 280 + j*74, l, B['amber'] if j == 3 else B['cyan'], ease(q)*a_out, 26)
        ctx.restore()
    return scene(f)

# ================= the two MIRV tests =================
def s_mirv(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'TWO TESTS', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        t1 = Ts('On the eleventh of March 2024')
        q1 = seg(t, t1 - .2, t1 + .6) if t1 < 900 else (1. if first > 0 else 0)
        if q1 > 0:
            qa = ease(q1)*a_out
            card(ctx, 110, 220, 820, 580, qa, '11 MARCH 2024 · MISSION DIVYASTRA', B['cyan'], p=q1)
            for j, (l, cue) in enumerate((('First MIRV flight test', 'for the first time'), ('Dr APJ Abdul Kalam Island', 'It went up from Kalam Island'),
                                          ('Radar tracked multiple re-entry vehicles', 'tracked multiple re-entry vehicles'),
                                          ('"Met its designed parameters"', 'met its designed parameters'),
                                          ('"An exceptional success" — Defence Minister', 'exceptional success'))):
                qq = ease(seg(t, Ts(cue) - .2, Ts(cue) + .4))*a_out if Ts(cue) < 900 else (qa if first > 0 else 0)
                txt(ctx, l, 150, 360 + j*72, 30, B['ice'] if j < 3 else B['amber'], qq, 'bold' if j < 3 else 'reg')
        t2 = Ts('Then came the eighth of May 2026')
        q2 = seg(t, t2 - .2, t2 + .6) if t2 < 900 else (1. if first > 1 else 0)
        if q2 > 0:
            qa = ease(q2)*a_out
            card(ctx, 990, 220, 820, 580, qa, '8 MAY 2026 · ADVANCED AGNI', B['amber'], p=q2)
            for j, l in enumerate(wrap(ctx, '"Payloads aimed at different targets spatially distributed over a large geographical area."', 32, 740, 'bold')):
                txt(ctx, l, 1030, 360 + j*46, 32, B['ice'], qa, 'bold')
            txt(ctx, 'MINISTRY OF DEFENCE', 1030, 580, 22, B['cyan'], qa, 'bold', mono=True)
        tn = Ts('notice what it did not say')
        q3 = seg(t, tn - .2, tn + .5)
        if q3 > 0:
            qa = ease(q3)*a_out
            rgba(ctx, B['deep'], .985*qa); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
            txt(ctx, 'WHAT IT DID NOT SAY', W/2, 300, 64, B['alert'], qa, 'black', 'c', glow=.8)
            for j, (l, cue) in enumerate((('THE VARIANT', 'It did not name the variant'), ('THE RANGE', 'It did not give a range'),
                                          ('HOW MANY WARHEADS', 'how many warheads'))):
                qq = ease(seg(t, Ts(cue) - .2, Ts(cue) + .4))*a_out if Ts(cue) < 900 else 0
                if qq <= 0: continue
                y = 470 + j*120
                txt(ctx, l, W/2, y, 54, B['steel'], qq, 'black', 'c')
                ctx.save(); ctx.set_line_width(5); rgba(ctx, B['alert'], qq)
                ww = tw(ctx, l, 54, 'black')/2
                ctx.move_to(W/2 - ww, y - 16); ctx.line_to(W/2 + ww, y - 16); ctx.stroke(); ctx.restore()
            ti = Ts('Those are inferences')
            qq = seg(t, ti - .2, ti + .4)
            if qq > 0: tagb(ctx, W/2, 850, 'INFERENCES, NOT ANNOUNCEMENTS', B['ice'], ease(qq)*a_out, 32, align='c')
        ctx.restore()
    return scene(f)

# ================= why MIRV, really =================
MIRVERS = [('UNITED STATES', 'The United States'), ('RUSSIA', 'Russia'), ('CHINA', 'China'), ('UNITED KINGDOM', 'the United Kingdom'), ('FRANCE', 'and France')]
def s_why(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, "THE DEFENDER'S PROBLEM", a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        if first == 0:
            txt(ctx, 'ONE WORD: INTERCEPTION', W/2, 150, 54, B['ice'], ease(seg(t, .3, 1.0))*a_out*(1 - seg(t, 7, 9)), 'black', 'c', glow=.6)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tc = Ts('So who can do this')
        swap = ease(seg(t, tc - .4, tc + .3)) if tc < 900 else (1. if first > 1 else 0)
        if swap < 1:
            aa = (1 - swap)*a
            # left: one warhead, one interceptor, clean stop
            t1 = Ts('Against one warhead')
            q1 = ease(seg(t, t1 - .3, t1 + .3))*aa if t1 < 900 else aa
            if q1 > 0:
                card(ctx, 100, 210, 820, 620, q1, 'ONE WARHEAD', B['steel'], p=q1)
                arc = bez((160, 780), (420, 330), (700, 620), 26)
                pp = ((t*.35) % 1)
                stroke_pts(ctx, arc, min(pp*1.6, 1), B['steel'], q1, 3)
                ipts = bez((830, 790), (790, 640), (700, 620), 20)
                if pp > .45:
                    stroke_pts(ctx, ipts, min((pp - .45)*3, 1), B['cyan'], q1, 3)
                    if pp > .75:
                        ctx.new_path(); rgba(ctx, B['cyan'], q1*(1 - (pp - .75)*4)); ctx.set_line_width(4); ctx.arc(700, 620, 20 + 60*(pp - .75)*4, 0, 2*math.pi); ctx.stroke()
                txt(ctx, 'ONE PROBLEM TO SOLVE', 510, 790, 26, B['cyan'], q1, 'bold', 'c', mono=True)
            # right: several, defence splits
            t2 = Ts('Against a missile that splits')
            q2 = ease(seg(t, t2 - .3, t2 + .3))*aa if t2 < 900 else 0
            if q2 > 0:
                card(ctx, 990, 210, 820, 620, q2, 'SEVERAL, EACH ON ITS OWN PATH', B['amber'], p=q2)
                pp = ((t*.35) % 1)
                up = bez((1040, 780), (1230, 380), (1420, 400), 24)
                stroke_pts(ctx, up, min(pp*2.4, 1), B['amber'], q2, 3)
                for k, ex in enumerate((1250, 1520, 1760)):
                    dq = min(max((pp - .42 - k*.05)*3, 0), 1)
                    if dq > 0: stroke_pts(ctx, bez((1420, 400), (lerp(1420, ex, .5), 600), (ex, 790), 20), dq, B['amber'], q2, 3)
                if pp > .55:
                    stroke_pts(ctx, bez((1680, 800), (1600, 650), (1520, 580), 16), min((pp - .55)*4, 1), B['cyan'], q2, 3)
                txt(ctx, 'SEVERAL, AT ONCE, IN MINUTES', 1400, 790, 26, B['alert'], q2, 'bold', 'c', mono=True)
            ta = Ts('an answer to missile defence')
            qq = seg(t, ta - .2, ta + .4)
            if qq > 0: tagb(ctx, W/2, 920, 'MIRV IS AN ANSWER TO MISSILE DEFENCE', B['amber'], ease(qq)*aa*1.4, 30, align='c')
        if swap > 0:
            aa = swap*a_out
            txt(ctx, 'WHO CAN DO THIS', W/2, 280, 54, B['ice'], aa, 'black', 'c')
            for i, (nm, cue) in enumerate(MIRVERS):
                q = ease(seg(t, Ts(cue) - .15, Ts(cue) + .35))*aa if Ts(cue) < 900 else aa
                if q <= 0: continue
                x = 90 + i*356; y = 420; wd = 320
                card(ctx, x, y, wd, 150, q, None, B['cyan'], p=q)
                _ls = wrap(ctx, nm, 28, 280, 'black')
                for j, l in enumerate(_ls):
                    txt(ctx, l, x + wd/2, y + (90 if len(_ls) == 1 else 66) + j*38, 28, B['ice'], q, 'black', 'c')
            tp = Ts('Pakistan says its Ababeel')
            q = seg(t, tp - .2, tp + .5)
            if q > 0:
                qa = ease(q)*a_out
                card(ctx, 480, 640, 960, 220, qa, 'CLAIMED, NOT VERIFIED', B['steel'], p=q)
                txt(ctx, 'PAKISTAN · ABABEEL', 960, 770, 36, B['steel'], qa, 'black', 'c')
                txt(ctx, 'INDEPENDENT VERIFICATION LIMITED; SOME ANALYSTS DOUBT ITS MATURITY', 960, 815, 20, B['alert'], qa, 'bold', 'c', mono=True)
            ti = Ts("India's two tests")
            q = seg(t, ti - .2, ti + .4)
            if q > 0: tagb(ctx, W/2, 930, 'A GROUP THAT WAS FIVE COUNTRIES LONG', B['amber'], ease(q)*a_out, 28, align='c')
        ctx.restore()
    return scene(f)

# ================= the doctrine =================
DOCT = [('CREDIBLE MINIMUM DETERRENCE', 'Enough to deter — not to match anyone\'s numbers', 'credible minimum deterrence'),
        ('NO FIRST USE', 'Only in retaliation for a nuclear attack on India or Indian forces', 'no first use'),
        ('MASSIVE RETALIATION', '"Massive, and designed to inflict unacceptable damage"', 'it would be massive')]
def s_doc(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, "CABINET COMMITTEE ON SECURITY · 4 JANUARY 2003", a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tn = Ts('The Nuclear Command Authority has two councils')
        chart = ease(seg(t, tn - .4, tn + .3)) if tn < 900 else (1. if first > 1 else 0)
        if chart < 1:
            aa = (1 - chart)*a
            txt(ctx, '4 JANUARY 2003', 150, 300, 90, B['amber'], aa*fin(t, .2, .5), 'black', glow=.8)
            txt(ctx, "INDIA'S NUCLEAR DOCTRINE, PUBLISHED", 150, 356, 28, B['cyan'], aa*fin(t, .4, .5), 'bold', mono=True)
            for i, (k, v, cue) in enumerate(DOCT):
                q = seg(t, Ts(cue) - .2, Ts(cue) + .5) if Ts(cue) < 900 else (1. if first > 0 else 0)
                if q <= 0: continue
                y = 470 + i*150; qa = ease(q)*aa
                txt(ctx, f'0{i+1}', 150, y + 44, 64, B['amber'], qa, 'black', glow=.5)
                txt(ctx, k, 280, y + 20, 42, B['ice'], qa, 'black')
                for j, l in enumerate(wrap(ctx, v, 28, 1420, 'reg')):
                    txt(ctx, l, 280, y + 72 + j*36, 28, B['steel'], qa, 'reg')
        if chart > 0:
            aa = chart*a_out
            boxes = [('POLITICAL COUNCIL', 'CHAIRED BY THE PRIME MINISTER', '"THE SOLE BODY WHICH CAN AUTHORIZE USE"', B['amber'], 250, 'The Political Council'),
                     ('EXECUTIVE COUNCIL', 'CHAIRED BY THE NSA', 'ADVISES AND CARRIES OUT DIRECTIONS', B['cyan'], 490, 'The Executive Council'),
                     ('STRATEGIC FORCES COMMAND', 'THREE-STAR C-IN-C, ROTATING', 'HOLDS THE WEAPONS · EXECUTES ORDERS', B['cyan'], 730, 'Commander-in-Chief')]
            for i, (k, s1, s2, col, y, cue) in enumerate(boxes):
                q = ease(seg(t, Ts(cue) - .3, Ts(cue) + .5))*aa if Ts(cue) < 900 else (aa if i < 2 else 0)
                if q <= 0: continue
                card(ctx, 420, y, 1080, 190, q, None, col, p=q)
                txt(ctx, k, 470, y + 62, 38, B['ice'], q, 'black')
                txt(ctx, s1, 470, y + 104, 24, col, q, 'bold', mono=True)
                txt(ctx, s2, 470, y + 146, 22, B['steel'], q, 'bold', mono=True)
                if i > 0 and q > .4:
                    stroke_pts(ctx, [(960, y - 48), (960, y - 4)], 1, B['dim'], q, 3, glow=False)
                    for dsg in (-.5, .5):
                        stroke_pts(ctx, [(960, y - 4), (960 + 14*math.sin(dsg), y - 24)], 1, B['dim'], q, 3, glow=False)
            txt(ctx, 'NUCLEAR COMMAND AUTHORITY', 960, 200, 30, B['cyan'], aa, 'bold', 'c', mono=True)
        ctx.restore()
    return scene(f)

# ================= why that makes MIRV make sense =================
def s_frame(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'WHY THE DOCTRINE EXPLAINS THE HARDWARE', a_out, EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=500)
    q = fin(t, .2, .6)*a_out
    txt(ctx, 'NO FIRST USE', W/2, 300, 96, B['ice'], q, 'black', 'c', glow=1)
    aq = seg(t, Ts('everything rests on being able to strike second') - .3, Ts('everything rests on being able to strike second') + .6)
    if aq > 0:
        stroke_pts(ctx, [(W/2, 340), (W/2, 440)], eoc(aq), B['amber'], a_out, 5)
        for dsg in (-.5, .5):
            stroke_pts(ctx, [(W/2, 440), (W/2 + 20*math.sin(dsg), 440 - 28*math.cos(dsg))], 1 if aq > .8 else 0, B['amber'], a_out, 5, glow=False)
        txt(ctx, 'MUST SURVIVE, AND ANSWER', W/2, 530, 72, B['amber'], ease(aq)*a_out, 'black', 'c', glow=1)
    for j, (l, sub, cue, x) in enumerate((('MOBILITY', 'keeps the missile alive', 'Mobility keeps the missile alive', 600),
                                          ('MIRV', 'keeps the answer credible', 'MIRV keeps the answer credible', 1320))):
        qq = seg(t, Ts(cue) - .2, Ts(cue) + .4)
        if qq <= 0: continue
        qa = ease(qq)*a_out; s = eob(qq, 1.6)
        ctx.save(); ctx.translate(x, 740); ctx.scale(s, s); ctx.translate(-x, -740)
        txt(ctx, l, x, 740, 64, B['cyan'], qa, 'black', 'c', glow=.6)
        txt(ctx, sub, x, 790, 28, B['steel'], qa, 'bold', 'c', mono=True)
        ctx.restore()
    ctx.restore()
scene(s_frame)

# ================= the debate =================
def s_deb(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'WHERE ANALYSTS DISAGREE', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        if first == 0:
            txt(ctx, 'BOTH SIDES ARE WORTH HEARING', W/2, 150, 46, B['ice'], ease(seg(t, .3, 1.0))*a_out*(1 - seg(t, 6, 8)), 'black', 'c', glow=.5)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        sides = [('THE CASE FOR', ['A no-first-use country needs its', 'retaliation to be survivable', 'and credible', 'Mobility plus MIRV delivers that'], B['cyan'], 'The case for'),
                 ('THE CASE FOR CAUTION', ['MIRV puts many warheads on', 'one launcher', 'That makes each launcher', 'a bigger prize', 'Neighbours tend to answer in kind'], B['steel'], 'The case for caution')]
        for i, (head, lines, col, cue) in enumerate(sides):
            tc = Ts(cue)
            q = seg(t, tc - .2, tc + .6) if tc < 900 else (1. if first > 0 else 0)
            if q <= 0: continue
            x = 110 + i*860; qa = ease(q)*a_out
            card(ctx, x, 210, 820, 600, qa, head, col, p=q)
            for j, l in enumerate(lines):
                txt(ctx, l, x + 50, 350 + j*62, 30, B['ice'], ease(seg(t, tc + .2 + j*.2, tc + .6 + j*.2))*a_out if tc < 900 else qa, 'bold' if j == 0 else 'reg')
        tl_ = Ts('Ajey Lele argued')
        q = seg(t, tl_ - .4, tl_ + .5)
        if q > 0:
            qa = ease(q)*a_out
            rgba(ctx, B['deep'], .92*qa); ctx.rectangle(0, 200, W, 740); ctx.fill()
            card(ctx, 240, 250, 1440, 480, qa, 'AJEY LELE · MP-IDSA · MAY 2026', B['amber'], p=q)
            for j, l in enumerate(wrap(ctx, 'The test read as a restrained signal rather than a provocation. A much longer-range test could have been taken as escalatory by powers well beyond China and Pakistan.', 38, 1340, 'bold')):
                txt(ctx, l, 290, 390 + j*52, 38, B['ice'], qa*ease(seg(t, tl_ + .2 + j*.25, tl_ + .6 + j*.25)), 'bold')
        tb = Ts('what other people will believe')
        q = seg(t, tb - .2, tb + .4)
        if q > 0: tagb(ctx, W/2, 900, 'DETERRENCE IS AN ARGUMENT ABOUT BELIEF', B['ice'], ease(q)*a_out, 32, align='c')
        ctx.restore()
    return scene(f)

# ================= what's next =================
NEXT = [('AGNI-PRIME', '1,000–2,000 KM CLASS', 'IN TRIALS', B['cyan'], 'Agni-Prime'),
        ('AGNI-6', 'REPORTED 8,000–12,000 KM', 'NO OFFICIAL ANNOUNCEMENT', B['steel'], 'Agni-6 is reported'),
        ('AGNI-5 MIRV', 'THE VERSION IN THIS EPISODE', 'IN FLIGHT TRIALS', B['amber'], 'still in flight trials')]
def s_next(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'WHERE IT STANDS · 15 NOVEMBER 2026', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        for i, (nm, sub, status, col, cue) in enumerate(NEXT):
            tc = Ts(cue)
            q = seg(t, tc - .2, tc + .5) if tc < 900 else (1. if first > 0 else 0)
            if q <= 0: continue
            y = 260 + i*200; qa = ease(q)*a_out
            card(ctx, 180, y, 1560, 160, qa, None, col, p=q)
            txt(ctx, nm, 230, y + 70, 44, B['ice'] if i < 2 else B['steel'], qa, 'black')
            txt(ctx, sub, 230, y + 118, 24, B['steel'], qa, 'bold', mono=True)
            tagb(ctx, 1690, y + 80, status, col, qa, 24, align='r')
        ts = Ts('single-warhead version')
        q = seg(t, ts - .2, ts + .4)
        if q > 0: tagb(ctx, W/2, 900, 'IN SERVICE: THE SINGLE-WARHEAD VERSION', B['amber'], ease(q)*a_out, 30, align='c')
        ctx.restore()
    return scene(f)

# ================= in three words =================
def s_three(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'AGNI-5 IN THREE WORDS', a_out, EP)
    mirv_arcs(ctx, t, a_out*.18, min(1, max(0, (t - .2)/5.0)), apex=(960, 760),
              ends=((300, 980), (900, 990), (1620, 975)), bus=True)
    words = [('FAR', 'OFFICIALLY BEYOND 5,000 KM', 'Far:', 380), ('MANY', 'ONE MISSILE, SEVERAL TARGETS', 'Many:', 960), ('SECOND', 'USED SECOND, NEVER FIRST', 'And second:', 1540)]
    for i, (w_, sub, cue, x) in enumerate(words):
        q = seg(t, Ts(cue) - .15, Ts(cue) + .35)
        if q <= 0: continue
        sc = lerp(1.7, 1, eob(q, 1.4))
        ctx.save(); ctx.translate(x, 520); ctx.scale(sc, sc)
        txt(ctx, w_, 0, 0, 104, B['amber'], ease(q*2)*a_out, 'black', 'c', glow=2)
        ctx.restore()
        for j, l in enumerate(wrap(ctx, sub, 22, 420, 'bold', True)):
            txt(ctx, l, x, 596 + j*32, 22, B['ice'], ease(seg(t, Ts(cue) + .3, Ts(cue) + .7))*a_out, 'bold', 'c', mono=True)
scene(s_three)

# ================= the wall =================
def _wcard(ctx, x, y, w, h, a, t, label, col=None):
    col = col or B['cyan']
    fill(ctx, lambda: rrect(ctx, x, y, w, h, 8), B['deep'], .9*a)
    stroke_pts(ctx, rect_pts(x, y, w, h), 1, col, a, 2.5)
    missile(ctx, x + w/2, y + h*.42, w*.8, 0, a, col=col)
    txt(ctx, label, x + 22, y + h - 28, 23, B['ice'], a, 'black')
    glow_dot(ctx, x + w/2, y + 14, 6, B['amber'], a)
def s_wall(ctx, t, D):
    bg(ctx); a_out = outro(t, D, .8)
    hud(ctx, t, 'THE BLUEPRINT WALL', a_out, EP)
    for i in range(5):
        x = 160 + i*330; y = 200
        if i < 3: continue
        stroke_pts(ctx, rect_pts(x, y, 290, 240), 1, B['grid'], a_out, 2, glow=False, dash=[10, 10])
        txt(ctx, f'EP {i+1}', x + 145, y + 130, 24, B['grid'], a_out, 'bold', 'c', mono=True)
    _wcard(ctx, 160, 200, 290, 240, a_out*.8, t, 'EP 1 · PRALAY', B['steel'])
    _wcard(ctx, 490, 200, 290, 240, a_out*.8, t, 'EP 2 · BRAHMOS', B['steel'])
    q = seg(t, .3, 1.0)
    _wcard(ctx, 820, lerp(-300, 200, eob(q, 1.3)), 290, 240, a_out, t, 'EP 3 · AGNI-5', B['amber'])
    for i, (l, cue) in enumerate((('A QUESTION ABOUT RE-ENTRY', 'survive coming back down'), ('TESTED IN 1989', 'tested off a range in 1989'),
                                  ('BY A PROGRAMME THAT BARELY EXISTED', 'barely existed yet'))):
        qq = seg(t, Ts(cue) - .2, Ts(cue) + .4)
        if qq > 0: tagb(ctx, 200, 560 + i*72, l, B['cyan'], ease(qq)*a_out, 24)
    tn = Ts('Next on')
    nq = seg(t, tn, tn + .6)
    if nq > 0:
        a = ease(nq)*a_out
        stroke_pts(ctx, rect_pts(1150, 200, 290, 240), nq, B['amber'], a*.9, 2.5)
        txt(ctx, 'EP 4 · THE SHIELD', 1295, 330, 24, B['amber'], a, 'black', 'c')
        fill(ctx, lambda: ctx.rectangle(0, 830, W*eoc(nq), 90), B['deep'], .95*a)
        rgba(ctx, B['cyan'], a); ctx.rectangle(0, 830, W*eoc(nq), 3); ctx.fill()
        txt(ctx, 'NEXT  ·  MISSILE DEFENCE, AND THE SHIELD INDIA IS BUILDING', 80, 888, 32, B['ice'], a, 'bold', mono=True)
    subscribe_card(ctx, t, Ts('subscribe'), a_out, x=1540, y=700)
scene(s_wall)

# ================= beats =================
SC = {}
for i, k in enumerate(['cold1', 'cold2']): SC[k] = s_cold(i)
for i, k in enumerate(['bus1', 'bus2', 'bus3']): SC[k] = s_bus(i)
SC['qs1'] = s_qs
for i, k in enumerate(['prog1', 'prog2', 'prog3']): SC[k] = s_prog(i)
for i, k in enumerate(['ladder1', 'ladder2', 'ladder3']): SC[k] = s_ladder(i)
for i, k in enumerate(['spec1', 'spec2', 'spec3']): SC[k] = s_spec(i)
for i, k in enumerate(['mirv1', 'mirv2', 'mirv3']): SC[k] = s_mirv(i)
for i, k in enumerate(['why1', 'why2', 'why3']): SC[k] = s_why(i)
for i, k in enumerate(['doc1', 'doc2', 'doc3', 'doc4']): SC[k] = s_doc(i)
SC['frame1'] = s_frame
for i, k in enumerate(['deb1', 'deb2', 'deb3']): SC[k] = s_deb(i)
for i, k in enumerate(['next1', 'next2']): SC[k] = s_next(i)
SC['three1'] = s_three
SC['end1'] = s_wall

BEATS = [(k, n, SC[k]) for k, n in EN]

GROUPS = {}
for g in ('cold', 'bus', 'prog', 'ladder', 'spec', 'mirv', 'why', 'doc', 'deb', 'next'):
    for k, _ in EN:
        if k.startswith(g): GROUPS[k] = g

KEYS = {
 'cold2': [('advanced Agni missile carrying MIRV', 'ADVANCED AGNI · MIRV', 'amber')],
 'prog1': [('Start in 1983', '1983', 'cyan')],
 'ladder1': [('nineteenth of April 2012', '19 APRIL 2012', 'amber')],
 'spec2': [('under twenty minutes', 'UNDER 20 MINUTES', 'amber')],
 'mirv3': [('It did not give a range', 'NO RANGE GIVEN', 'alert')],
 'why2': [('an answer to missile defence', 'VS MISSILE DEFENCE', 'amber')],
 'doc2': [('no first use', 'NO FIRST USE', 'ice')],
 'next1': [('no official announcement', 'NOT ANNOUNCED', 'steel')],
}
ANNOT = {
 'bus3': [('They call it the bus', 'circle', 960, 250, 300, 150)],
 'frame1': [('MIRV keeps the answer credible', 'underline', 1130, 820, 380, 0)],
}

_order = [k for k, _ in EN]
FX = [('whoosh', k, -.25, .22) for i, k in enumerate(_order) if i and GROUPS.get(k, k) != GROUPS.get(_order[i-1], _order[i-1])]
FX += [('beep', k, ph, .14) for k, items in KEYS.items() for ph, _, _ in items]
FX += [('tick', 'cold1', .15, .12), ('boom', 'cold1', 'climb out of the sky', .5),
       ('glitch', 'cold1', 'And then: nothing', .25),
       ('riser', 'bus2', 'They call it the bus', .2), ('boom', 'bus2', 'They call it the bus', .45),
       ('ping', 'prog3', 'flown from Chandipur in 1989', .4),
       ('boom', 'ladder1', 'nineteenth of April 2012', .4),
       ('stamp', 'mirv1', 'Divyastra', .3),
       ('glitch', 'mirv3', 'notice what it did not say', .3),
       ('ping', 'why1', 'Against one warhead', .3),
       ('stamp', 'doc1', 'January 2003', .3), ('boom', 'frame1', 'strike second', .2),
       ('riser', 'three1', 'Far:', .15), ('ding', 'three1', 'Far:', .25), ('ding', 'three1', 'Many:', .25), ('ding', 'three1', 'And second:', .25),
       ('stamp', 'end1', .5, .35), ('ding', 'end1', 'subscribe', .2)]
