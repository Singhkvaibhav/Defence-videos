"""India's Defence, Decoded — Episode 2: BrahMos (bilingual: English + Hindi)."""
import os, sys, math, random, cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 620.0
core.TOTAL = TOTAL
from engine.core import W, H, seg, ease, eoc, eob, lerp, T
from engine.bp import (B, rgba, rrect, bg, txt, tw, typed, wrap, para, stroke_pts, head_pt, rect_pts, fill, glow_dot, bez,
                       missile, truck, figure, radar, hud, card, tagb, outro, camera, india_map, map_point, scene, subscribe_card, face)
from engine.mil import (waves, horizon, warship, submarine, jet, axes, dot, bar, sea_board, pin, schematic_note)
from text import EN, HI as _HI

EP = 2
CODE = 'Def02'
TITLE = 'BrahMos'
NAME = 'BrahMos: the missile India built with Russia'
POST = 'engine.bp'
BED = 'pulse'
VOICE_EN = {'length': 0.98, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
VOICE_HI = {'length': 0.86, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
CRF, PRESET = 17, 'medium'
EXTRA = {'cold1': .7, 'three': 1.0, 'end2': 2.5}
HI = _HI

def Ts(x):
    try: return T(x)
    except ValueError: return 999.
def fin(t, t0=.1, d=.5): return ease(seg(t, t0, t0 + d))

# ================= cold open: the Lucknow factory =================
def s_factory(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D, .35)
        hud(ctx, t, 'LUCKNOW · 18 OCT 2025 · FIRST BATCH FLAGGED OFF', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=560, pan=(-15, 0))
        a = fin(t, .1, .6)*a_out if first == 0 else a_out
        # gantry rail overhead
        stroke_pts(ctx, [(60, 230), (1860, 230)], 1, B['dim'], a, 3, glow=False)
        for k in range(5):
            stroke_pts(ctx, [(200 + k*380, 230), (200 + k*380, 300)], 1, B['dim'], a*.7, 2, glow=False)
        # three missiles on cradles
        for k in range(3):
            q = fin(t, .2 + k*.25, .6) if first == 0 else 1.
            x = 500 + k*500; y = 560
            missile(ctx, x, y, 480, 0, a, p=q)
            for dx in (-150, 150):
                stroke_pts(ctx, [(x + dx - 50, y + 60), (x + dx, y + 24), (x + dx + 50, y + 60)], q, B['steel'], a, 3)
                stroke_pts(ctx, [(x + dx - 60, y + 60), (x + dx + 60, y + 60)], q, B['steel'], a, 3, glow=False)
        stroke_pts(ctx, [(0, 700), (W, 700)], 1, B['dim'], a, 2, glow=False)
        # the flag-off ribbon, cut as the beat opens
        rq = seg(t, .6, 2.2) if first == 0 else 1.
        if rq > 0:
            cut = eoc(rq)
            for sgn in (-1, 1):
                stroke_pts(ctx, [(960 + sgn*20 - sgn*360*cut, 400), (960 + sgn*20 - sgn*360*cut, 700)], 1, B['amber'], a*(1 - .3*cut), 4, glow=True)
        txt(ctx, 'BRAHMOS INTEGRATION & TESTING FACILITY', 90, 790, 26, B['cyan'], a, 'bold', mono=True)
        ctx.restore()
        # the quote
        tq = Ts('Every inch')
        q = seg(t, tq - .4, tq + .4)
        if q > 0:
            qa = ease(q)*a_out
            card(ctx, 240, 300, 1440, 420, qa, 'DEFENCE MINISTER · LUCKNOW · 18 OCT 2025', B['amber'], p=seg(t, tq - .4, tq + .4))
            lines = wrap(ctx, '"Every inch of Pakistan\'s territory is now within the reach of BrahMos."', 56, 1340, 'bold')
            for i, l in enumerate(lines):
                txt(ctx, typed(l, seg(t, tq, tq + 1.6)*1.6 - i*.5), 290, 470 + i*72, 56, B['ice'], qa, 'bold')
            t2 = Ts('just a trailer')
            if t > t2 - .5:
                txt(ctx, typed('"The operation was just a trailer."', seg(t, t2 - .5, t2 + .9)), 290, 660, 46, B['amber'], ease(seg(t, t2 - .5, t2 - .1))*a_out, 'bold')
    return scene(f)

# ================= four questions =================
QS = [('WHERE DID IT', 'COME FROM?', 'Where did it'), ('WHAT CAN IT', 'ACTUALLY DO?', 'What can it'),
      ('ANYTHING ELSE', 'LIKE IT?', 'Is there anything'), ('WHO IS', 'BUYING IT?', 'who is buying')]
def s_questions(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, "INDIA'S DEFENCE, DECODED · EPISODE 2", a_out, EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=500)
    tb = Ts('This is BrahMos')
    bq = seg(t, tb - .2, tb + .4)
    shrink = ease(seg(t, Ts('Four questions') - .4, Ts('Four questions') + .3))
    if bq > 0:
        sc = lerp(1.5, 1, eob(bq, 1.3))*(1 - .55*shrink)
        yy = lerp(500, 220, shrink)
        ctx.save(); ctx.translate(W/2, yy); ctx.scale(sc, sc)
        txt(ctx, 'BRAHMOS', 0, 0, 230, B['ice'], ease(bq*2)*a_out, 'black', 'c', glow=1.5)
        ctx.restore()
        if shrink < .6:
            for i, (l, cue) in enumerate((('BUILT WITH RUSSIA', 'built with Russia'), ('NAMED AFTER TWO RIVERS', 'two rivers'), ("INDIA'S FIRST EXPORT OF ITS CLASS", 'sold abroad'))):
                txt(ctx, l, W/2, 620 + i*54, 30, B['cyan'], ease(seg(t, Ts(cue) - .1, Ts(cue) + .4))*a_out*(1 - shrink*1.6), 'bold', 'c', mono=True)
    for i, (k1, k2, cue) in enumerate(QS):
        t0 = Ts(cue) - .1; q = seg(t, t0, t0 + .5)
        if q <= 0: continue
        x = 140 + i*430; y = 400; a = ease(q*2)*a_out; s = eob(q, 1.7)
        ctx.save(); ctx.translate(x + 190, y + 190); ctx.scale(s, s); ctx.translate(-(x + 190), -(y + 190))
        card(ctx, x, y, 380, 380, a, None, B['cyan'] if i % 2 == 0 else B['amber'], p=q)
        txt(ctx, f'0{i+1}', x + 30, y + 130, 96, B['amber'] if i % 2 else B['cyan'], a, 'black', glow=.8)
        txt(ctx, k1, x + 30, y + 230, 28, B['steel'], a, 'bold', mono=True)
        for j, l in enumerate(wrap(ctx, k2, 46, 320, 'black')):
            txt(ctx, l, x + 30, y + 296 + j*52, 46, B['ice'], a, 'black')
        ctx.restore()
    ctx.restore()
scene(s_questions)

# ================= Moscow, 1998 =================
def s_moscow(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'MOSCOW · 12 FEBRUARY 1998', a_out, EP)
        tn = Ts('the name is the giveaway')
        swap = ease(seg(t, tn - .5, tn + .4)) if first == 0 else 1.
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
        if swap < 1:
            a = (1 - swap)*(fin(t, .1, .6)*a_out if first == 0 else a_out)
            # the table, the two signatories, a document between them
            stroke_pts(ctx, [(420, 640), (1500, 640)], 1, B['ice'], a, 4, glow=False)
            stroke_pts(ctx, [(480, 640), (500, 790)], 1, B['dim'], a, 3, glow=False)
            stroke_pts(ctx, [(1440, 640), (1420, 790)], 1, B['dim'], a, 3, glow=False)
            fill(ctx, lambda: rrect(ctx, 860, 560, 200, 80, 4), B['ice'], .12*a)
            stroke_pts(ctx, rect_pts(860, 560, 200, 80), 1, B['ice'], a, 2.5)
            for k in range(3):
                stroke_pts(ctx, [(880, 580 + k*20), (1040 - k*40, 580 + k*20)], fin(t, .8 + k*.2, .4), B['dim'], a, 2, glow=False)
            for i, (nm, org, cue, x) in enumerate((('DR APJ ABDUL KALAM', 'DRDO · INDIA', 'Dr APJ Abdul Kalam', 620), ('N.V. MIKHAILOV', 'FIRST DEP. DEFENCE MIN. · RUSSIA', 'Mikhailov', 1300))):
                q = fin(t, .3 + i*.3, .5) if first == 0 else 1.
                figure(ctx, x, 560, 1.5, B['ice'], a*q, t, seed=i)
                txt(ctx, nm, x, 740, 30, B['ice'], a*ease(seg(t, Ts(cue) - .2, Ts(cue) + .3)) if Ts(cue) < 900 else a*q, 'black', 'c')
                txt(ctx, org, x, 782, 22, B['cyan'], a*ease(seg(t, Ts(cue) - .2, Ts(cue) + .3)) if Ts(cue) < 900 else a*q, 'bold', 'c', mono=True)
            tj = Ts('joint company')
            if t > tj - .3:
                tagb(ctx, W/2, 300, 'INTER-GOVERNMENTAL AGREEMENT · 12 FEB 1998', B['amber'], ease(seg(t, tj - .3, tj + .3))*a*1.4, 26, align='c')
                txt(ctx, 'BRAHMOS AEROSPACE', W/2, 390, 54, B['ice'], ease(seg(t, tj, tj + .5))*a*1.4, 'black', 'c', glow=.8)
                txt(ctx, 'DRDO (INDIA)  +  NPO MASHINOSTROYENIYA (RUSSIA)', W/2, 440, 26, B['cyan'], ease(seg(t, tj + .3, tj + .8))*a*1.4, 'bold', 'c', mono=True)
        if swap > 0:
            a = swap*a_out
            # two rivers flowing into one name
            for i, (nm, part, cue, y, col) in enumerate((('BRAHMAPUTRA', 'BRAH', 'from the Brahmaputra', 330, B['cyan']), ('MOSKVA', 'MOS', 'from the Moskva', 560, B['steel']))):
                q = ease(seg(t, Ts(cue) - .3, Ts(cue) + .4)) if Ts(cue) < 900 else 1.
                pts = [(140 + k*34, y + 46*math.sin(k*.5 + t*1.1 + i*2)) for k in range(26)]
                stroke_pts(ctx, pts, q, col, a*.85, 7)
                txt(ctx, nm, 140, y - 90, 44, col, a*q, 'black', glow=.5)
                if q > .6:
                    txt(ctx, part, 1070, y + 16, 110, B['ice'], a*ease(seg(t, Ts(cue) + .2, Ts(cue) + .6)) if Ts(cue) < 900 else a, 'black', glow=1)
            tr = Ts('Two rivers')
            q = seg(t, tr - .2, tr + .5)
            if q > 0:
                sc = lerp(1.4, 1, eob(q, 1.3))
                ctx.save(); ctx.translate(W/2, 810); ctx.scale(sc, sc)
                txt(ctx, 'BRAHMOS', 0, 0, 150, B['amber'], ease(q*2)*a, 'black', 'c', glow=1.5)
                ctx.restore()
                txt(ctx, 'TWO RIVERS · TWO COUNTRIES · ONE MISSILE', W/2, 880, 26, B['cyan'], ease(seg(t, tr + .4, tr + .9))*a, 'bold', 'c', mono=True)
        ctx.restore()
    return scene(f)

# ================= the Oniks shortcut =================
def s_oniks(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'THE SHORTCUT · P-800 ONIKS', a_out, EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=500)
    a = fin(t, .2, .6)*a_out
    to = Ts('P-800 Oniks')
    # the parent missile above, BrahMos below, with a lineage arrow
    missile(ctx, W/2, 330, 820, 0, a*.75, p=fin(t, .2, 1.2), col=B['steel'], fill_a=.06)
    txt(ctx, 'P-800 ONIKS  ·  RUSSIA', W/2, 230, 34, B['steel'], ease(seg(t, to - .2, to + .4))*a_out, 'black', 'c')
    aq = seg(t, to + .4, to + 1.4)
    if aq > 0:
        stroke_pts(ctx, [(W/2, 400), (W/2, 540)], aq, B['cyan'], a, 4)
        for d in (-.5, .5):
            stroke_pts(ctx, [(W/2, 540), (W/2 + 22*math.sin(d), 540 - 30*math.cos(d))], 1 if aq >= 1 else 0, B['cyan'], a, 4, glow=False)
    bq = seg(t, to + 1.0, to + 2.0)
    if bq > 0:
        missile(ctx, W/2, 640, 900, 0, a, p=bq)
        txt(ctx, 'BRAHMOS', W/2, 770, 48, B['amber'], ease(bq)*a_out, 'black', 'c', glow=1)
    for i, (lab, cue, x, y, col) in enumerate((('RUSSIAN RAMJET PROPULSION', 'Russian ramjet', 400, 880, B['steel']),
                                               ('INDIAN GUIDANCE · SOFTWARE · AIRFRAME', 'Indian guidance', 1340, 880, B['cyan']))):
        q = ease(seg(t, Ts(cue) - .2, Ts(cue) + .5))*a_out
        if q > 0: tagb(ctx, x, y, lab, col, q, 24, align='c')
    tf = Ts('arrived so fast'); q = seg(t, tf - .2, tf + .4)
    if q > 0: tagb(ctx, W/2, 140 + 0, 'THAT SHORTCUT IS WHY IT ARRIVED FAST', B['amber'], ease(q)*a_out, 26, align='c')
    ctx.restore()
scene(s_oniks)

# ================= the induction timeline =================
TLINE = [(330, '12 JUN 2001', 'FIRST TEST FLIGHT · CHANDIPUR', 'The first test flight', 'pad'),
         (800, '2005', 'INDIAN NAVY', 'inducted it in 2005', 'ship'),
         (1230, '2007', 'INDIAN ARMY', 'followed in 2007', 'truck'),
         (1680, 'JAN 2020', 'AIR FORCE · SU-30 SQUADRON', 'the Air Force commissioned', 'jet')]
def s_timeline(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'INTO SERVICE', a_out, EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
    stroke_pts(ctx, [(160, 620), (1800, 620)], fin(t, .1, 1.2), B['dim'], a_out, 2, glow=False)
    for i, (x, lab, sub, cue, ic) in enumerate(TLINE):
        q = seg(t, Ts(cue) - .2, Ts(cue) + .5)
        if q <= 0:
            glow_dot(ctx, x, 620, 4, B['dim'], .4*a_out); continue
        a = ease(q*1.5)*a_out; col = B['amber'] if i == 0 else B['cyan']
        glow_dot(ctx, x, 620, 10, col, a)
        stroke_pts(ctx, [(x, 620), (x, 540)], q, col, a, 2, glow=False)
        txt(ctx, lab, x, 500, 44 if len(lab) < 8 else 34, B['ice'], a, 'black', 'c', glow=.6)
        for j, l in enumerate(wrap(ctx, sub, 22, 400, 'bold', True)):
            txt(ctx, l, x, 680 + j*32, 22, col, a, 'bold', 'c', mono=True)
        yy = 800
        if ic == 'pad':
            stroke_pts(ctx, [(x - 60, yy + 50), (x - 60, yy - 50), (x + 60, yy - 50)], q, B['ice'], a, 3)
            missile(ctx, x, yy - 10, 130, -.3, a, p=q)
        elif ic == 'ship': warship(ctx, x, yy + 40, .22, a, t, p=q)
        elif ic == 'truck': truck(ctx, x, yy + 30, .24, a, t, raise_=.5)
        elif ic == 'jet': jet(ctx, x, yy, .30, a, t, p=q)
    ctx.restore()
scene(s_timeline)

# ================= capability 1: speed =================
def s_speed(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'ONE · SPEED', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tr = Ts('One: speed') if first == 0 else -3
        start = max(tr, 0) + .6
        for lane, (nm, sub, sp, col, y) in enumerate((('SUBSONIC CRUISE MISSILE', '~ SPEED OF AN AIRLINER', .33, B['steel'], 330),
                                                      ('BRAHMOS', 'CLOSE TO 3× THE SPEED OF SOUND', 1.0, B['amber'], 560))):
            stroke_pts(ctx, [(200, y + 70), (1780, y + 70)], 1, B['dim'], a, 2, glow=False)
            txt(ctx, nm, 200, y - 50, 34, col, a, 'black')
            txt(ctx, sub, 200, y - 14, 22, B['steel'], a, 'bold', mono=True)
            cyc = 5.0
            p = ((t - start)*sp/cyc) % 1 if t > start else 0
            if t > start:
                x = lerp(240, 1740, p)
                missile(ctx, x, y + 30, 150, 0, a, col=col)
                for k in range(5):
                    stroke_pts(ctx, [(x - 90 - k*48, y + 30), (x - 120 - k*48, y + 30)], 1, col, a*(.5 - k*.08), 3, glow=False)
            glow_dot(ctx, 1740, y + 30, 7, B['alert'], a*.8)
        # reaction-time bars
        tw_ = Ts("might have a couple of minutes")
        if t > tw_ - .3:
            for i, (lab, val, w, col, cue) in enumerate((('AGAINST SUBSONIC', 'MINUTES', 680, B['steel'], "a couple of minutes"),
                                                         ('AGAINST BRAHMOS', 'SECONDS', 110, B['alert'], 'they have seconds'))):
                q = seg(t, Ts(cue) - .2, Ts(cue) + .6)
                if q <= 0: continue
                qa = ease(q)*a_out; y = 790 + i*80
                txt(ctx, lab, 200, y + 26, 26, B['ice'], qa, 'bold', mono=True)
                ww = w*eoc(q)
                fill(ctx, lambda: rrect(ctx, 620, y, ww, 50, 6), col, .3*qa)
                stroke_pts(ctx, rect_pts(620, y, ww, 50), 1, col, qa, 2.5)
                txt(ctx, val, 640 + ww, y + 38, 34, col, qa, 'black', glow=.6)
            txt(ctx, "DEFENDER'S REACTION TIME", 200, 770, 22, B['cyan'], a_out*ease(seg(t, tw_ - .3, tw_ + .2)), 'bold', mono=True)
        ctx.restore()
    return scene(f)

# ================= capability 2: flying low under the radar horizon =================
def s_horizon(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'TWO · FLYING LOW', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=640)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        cx, cy, r = 960, 640 + 2600, 2600
        hpts = horizon(ctx, cx, cy, r, a, p=fin(t, .1, 1.0) if first == 0 else 1.)
        # the curve below the horizon, lightly filled
        ctx.save(); ctx.new_path(); ctx.move_to(hpts[0][0], hpts[0][1])
        for q in hpts[1:]: ctx.line_to(*q)
        ctx.line_to(W + 200, H + 100); ctx.line_to(-200, H + 100); ctx.close_path()
        rgba(ctx, B['cyan'], .05*a); ctx.fill(); ctx.restore()
        # a ship on the right of the curve, radar line straight out (tangent)
        sx = 1560
        sy = cy - math.sqrt(max(r*r - (sx - cx)**2, 1))
        warship(ctx, sx, sy + 6, .42, a, t)
        rq = fin(t, .4, .6) if first == 0 else 1.
        ang = math.atan2(sx - cx, -(sy - cy))
        bx, by = sx - 1500*math.cos(ang), sy - 1500*math.sin(ang)
        stroke_pts(ctx, [(sx, sy - 70), (bx, by - 70)], rq, B['alert'], a*.85, 3, dash=[18, 14])
        txt(ctx, 'RADAR HORIZON', 560, 430, 30, B['alert'], rq*a_out, 'black', glow=.6)
        txt(ctx, 'IT CANNOT SEE BELOW THIS LINE', 560, 472, 22, B['alert'], rq*a_out*.9, 'bold', mono=True)
        # the missile running low, hugging the curve
        tlow = Ts('ten metres above the sea') if first == 0 else Ts('appears over the horizon')
        go = max(Ts('it flies low'), Ts('A ship\'s radar looks out'), 0)
        p = min(1, max(0, (t - go - .3)/5.5))
        mpts = []
        for k in range(61):
            xx = lerp(180, sx - 120, k/60)
            yy = cy - math.sqrt(max(r*r - (xx - cx)**2, 1)) - 26
            mpts.append((xx, yy))
        if p > 0:
            stroke_pts(ctx, mpts, p, B['amber'], a*.75, 3)
            hx_, hy_, mang = head_pt(mpts, p)
            missile(ctx, hx_, hy_, 130, mang, a, col=B['amber'])
            if p > .55:
                stroke_pts(ctx, [(hx_, hy_ + 14), (hx_, hy_ + 48)], 1, B['amber'], a*.7, 2, glow=False)
                txt(ctx, '~10 M', hx_, hy_ + 76, 24, B['amber'], a, 'black', 'c')
        tc = Ts('the sea is curved'); q = seg(t, tc - .2, tc + .5)
        if q > 0: tagb(ctx, 400, 300, 'THE SEA IS CURVED', B['ice'], ease(q)*a_out, 30, align='c')
        tn = Ts('almost no time left'); q = seg(t, tn - .2, tn + .4)
        if q > 0: tagb(ctx, 1500, 300, 'ALMOST NO TIME LEFT', B['alert'], ease(q)*a_out, 28, align='c')
        ctx.restore()
    return scene(f)

# ================= capability 3: fire and forget =================
def s_guidance(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'THREE · NOBODY IS FLYING IT', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=540)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        waves(ctx, 820, t, a*.8)
        path = bez((230, 700), (480, 300), (900, 360), 30) + bez((900, 360), (1300, 400), (1700, 700), 26)[1:]
        go = max(Ts('Once it leaves the launcher'), 0)
        p = min(1, max(0, (t - go - .2)/4.5)) if go < 900 else 1.
        stroke_pts(ctx, path, p, B['amber'], a*.8, 3)
        if 0 < p < 1:
            hx_, hy_, mang = head_pt(path, p); missile(ctx, hx_, hy_, 140, mang, a, col=B['amber'])
        # phase 1: inertial + satellite
        q1 = ease(seg(t, Ts('inertial system') - .2, Ts('inertial system') + .5))*a_out
        if q1 > 0:
            glow_dot(ctx, 700, 180, 10, B['cyan'], q1)
            for k in range(3):
                stroke_pts(ctx, [(700, 196), (700 - 40 + k*40, 330)], 1, B['cyan'], q1*(.4 + .3*math.sin(t*4 + k)), 2, glow=False)
            tagb(ctx, 700, 130, 'INERTIAL + SATELLITE', B['cyan'], q1, 24, align='c')
        # phase 2: own radar
        q2 = ease(seg(t, Ts('its own radar') - .2, Ts('its own radar') + .5))*a_out
        if q2 > 0:
            for k in range(3):
                ph = (t*1.1 + k/3) % 1
                ctx.new_path(); rgba(ctx, B['alert'], q2*(1 - ph)*.8); ctx.set_line_width(3); ctx.arc(1480, 520, 40 + 110*ph, -1.3, .5); ctx.stroke()
            tagb(ctx, 1430, 330, 'ACTIVE RADAR SEEKER', B['alert'], q2, 24, align='c')
        # the crew leaves
        tl_ = Ts('turn around and leave')
        lx = lerp(250, -400, ease(seg(t, tl_, tl_ + 3.0))) if tl_ < 900 else 250
        truck(ctx, lx, 760, .42, a, t, raise_=.0 if t > tl_ else .9, wheels_spin=-lx*.04)
        if t > tl_ - .3 and tl_ < 900:
            tagb(ctx, 420, 880, 'FIRE AND FORGET', B['amber'], ease(seg(t, tl_ - .3, tl_ + .3))*a_out, 28, align='c')
        # target
        glow_dot(ctx, 1700, 700, 8, B['alert'], a*.8)
        tm = Ts('within about a metre'); q = seg(t, tm - .2, tm + .5)
        if q > 0:
            qa = ease(q)*a_out
            ctx.new_path(); rgba(ctx, B['ice'], qa); ctx.set_line_width(3); ctx.arc(1700, 700, 46, 0, 2*math.pi); ctx.stroke()
            tagb(ctx, 1640, 560, 'CLAIMED: WITHIN ~1 M', B['ice'], qa, 22, align='c')
        tw_ = Ts('two hundred to three hundred'); q = seg(t, tw_ - .3, tw_ + .4)
        if q > 0: tagb(ctx, 300, 300, 'WARHEAD 200–300 KG · CONVENTIONAL', B['cyan'], ease(q)*a_out, 24, align='c')
        ctx.restore()
    return scene(f)

# ================= launched from anywhere =================
PLAT = [('ROAD', 'truck', 'a truck on a road'), ('SHIP', 'ship', "a warship's deck"), ('SUBMARINE', 'sub', 'a submarine'), ('AIRCRAFT', 'jet', 'the belly of a fighter')]
def s_platforms(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'LAUNCHED FROM ALMOST ANYWHERE', a_out, EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
    for i, (nm, ic, cue) in enumerate(PLAT):
        t0 = Ts(cue) - .15; q = seg(t, t0, t0 + .5)
        if q <= 0: continue
        x = 120 + i*440; a = ease(q*1.6)*a_out; s = eob(q, 1.6)
        ctx.save(); ctx.translate(x + 200, 540); ctx.scale(s, s); ctx.translate(-(x + 200), -540)
        card(ctx, x, 230, 400, 560, a, nm, B['cyan'] if i % 2 == 0 else B['amber'], p=q)
        if ic == 'truck': truck(ctx, x + 200, 620, .42, a, t, raise_=.85)
        elif ic == 'ship':
            waves(ctx, 640, t, a*.7, n=4, span=(x + 20, x + 380), step=30); warship(ctx, x + 200, 620, .45, a, t)
        elif ic == 'sub':
            waves(ctx, 600, t, a*.7, n=4, span=(x + 20, x + 380), step=30); submarine(ctx, x + 200, 640, .42, a, t)
        else: jet(ctx, x + 200, 520, .52, a, t)
        # a small missile leaves each platform on a loop
        ph = ((t - t0)*.5) % 1
        if ph > .1:
            yy = lerp(560, 300, (ph - .1)/.9)
            missile(ctx, x + 200 + (60 if ic == 'jet' else 0), yy, 100, -math.pi/2 + (.4 if ic == 'jet' else 0), a*(1 - (ph - .1)/.9), col=B['amber'])
        ctx.restore()
    tf = Ts('cover all four'); q = seg(t, tf - .2, tf + .4)
    if q > 0: tagb(ctx, W/2, 880, 'VERY FEW MISSILES COVER ALL FOUR', B['ice'], ease(q)*a_out, 30, align='c')
    ctx.restore()
scene(s_platforms)

# ================= the range story =================
def s_range(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'RANGE · WHERE POLITICS SHAPED THE ENGINEERING', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=540)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        gx = 1020
        # the gate
        lift = ease(seg(t, Ts('India joined') - .2, Ts('India joined') + 1.0)) if Ts('India joined') < 900 else (1. if first == 2 else 0.)
        gy = lerp(300, -620, lift)
        fill(ctx, lambda: rrect(ctx, gx, gy, 46, 520, 6), B['alert'], .22*a)
        stroke_pts(ctx, rect_pts(gx, gy, 46, 520), 1, B['alert'], a, 3)
        for k in range(5):
            stroke_pts(ctx, [(gx, gy + 60 + k*100), (gx + 46, gy + 110 + k*100)], 1, B['alert'], a*.6, 2, glow=False)
        if lift < .8:
            txt(ctx, 'MTCR', gx + 23, 270, 36, B['alert'], a*(1 - lift), 'black', 'c', glow=.6)
            txt(ctx, '500 KG BEYOND 300 KM', gx + 23, 850, 22, B['alert'], a*(1 - lift), 'bold', 'c', mono=True)
        if lift > .2:
            tagb(ctx, gx + 23, 180, 'INDIA JOINS THE MTCR · 2016', B['cyan'], lift*a_out, 26, align='c')
        # the bars
        rows = [(290, '290 KM', 'about two hundred and ninety', B['steel'], 'FOR YEARS'),
                (450, '450 KM', 'four hundred and fifty', B['cyan'], 'TESTED'),
                (800, '800 KM', 'eight-hundred-kilometre', B['amber'], 'REPORTED · IN TRIALS')]
        for i, (km, lab, cue, col, note) in enumerate(rows):
            t0 = Ts(cue) - .2; q = seg(t, t0, t0 + 1.2) if Ts(cue) < 900 else (1. if (first == 2 and i == 0) or (first > 0 and i == 0) else 0)
            if q <= 0: continue
            y = 420 + i*130; qa = ease(min(q*2, 1))*a_out
            wmax = 1400*km/800.
            ww = min(wmax*eoc(q), (gx - 200) if (lift < .5 and km > 300) else wmax*eoc(q))
            fill(ctx, lambda: rrect(ctx, 200, y, ww, 70, 6), col, .25*qa)
            stroke_pts(ctx, rect_pts(200, y, ww, 70), 1, col, qa, 2.5)
            txt(ctx, lab, 220, y + 50, 40, B['ice'], qa, 'black', glow=.5)
            txt(ctx, note, 200 + ww - 20, y + 46, 22, col, qa, 'bold', 'r', mono=True)
        tx = Ts('other side of it'); q = seg(t, tx - .2, tx + .4)
        if q > 0: tagb(ctx, W/2, 900, 'INDIA MOVED TO THE OTHER SIDE OF THE TREATY', B['amber'], ease(q)*a_out, 28, align='c')
        te = Ts('Export customers still'); q = seg(t, te - .2, te + .4)
        if q > 0: tagb(ctx, 1500, 340, 'EXPORTS: 300 KM CLASS', B['steel'], ease(q)*a_out, 22, align='c')
        ctx.restore()
    return scene(f)

# ================= the speed-versus-range chart =================
def _cx(km): return 200 + (math.log10(km) - 2)*1029         # 100 km .. 3,000 km, matching the 1520 px axis
def _cy(mach): return 820 - mach/3.4*560
CHART = [('TOMAHAWK', 2000, .74, 'Tomahawk', B['steel'], None, 'l', 50),
         ('HARPOON', 240, .85, 'The Harpoon', B['steel'], None, 'l', 40),
         ('EXOCET', 180, .93, 'Exocet', B['steel'], None, 'r', -4),
         ('KALIBR', 1500, .80, "Russia's Kalibr", B['cyan'], 170, 'r', -50),
         ('YJ-18', 540, .80, 'YJ-18', B['cyan'], 170, 'l', -4),
         ('BRAHMOS', 400, 3.0, 'BrahMos makes the opposite', B['amber'], None, 'l', 0)]
def s_chart(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'SPEED VERSUS RANGE', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        axes(ctx, 200, 820, 1520, 560, a, 'RANGE  →', 'SPEED (MACH)  →',
             [(0, '100'), ((math.log10(300) - 2)/1.477, '300'), ((math.log10(1000) - 2)/1.477, '1,000'), (1, '3,000 KM')],
             [(0, '0'), (1/3.4, 'M 1'), (2/3.4, 'M 2'), (3/3.4, 'M 3')])
        stroke_pts(ctx, [(200, _cy(1.0)), (1720, _cy(1.0))], fin(t, .3, .6)*a_out, B['dim'], a*.7, 2, glow=False, dash=[12, 10])
        txt(ctx, 'SOUND BARRIER', 1700, _cy(1.0) - 14, 20, B['dim'], a*.8, 'bold', 'r', mono=True)
        for (nm, km, mach, cue, col, sprint, al, ldy) in CHART:
            t0 = Ts(cue) - .2
            q = seg(t, t0, t0 + .5) if Ts(cue) < 900 else (1. if first > 0 else 0)
            if q <= 0: continue
            qa = ease(q*1.6)*a_out
            dot(ctx, _cx(km), _cy(mach), nm, col, qa, r=18 if nm == 'BRAHMOS' else 14, sprint=sprint, align=al, size=30 if nm == 'BRAHMOS' else 26, dy=ldy)
        tp = Ts('See the pattern'); q = seg(t, tp - .2, tp + .5)
        if q > 0:
            qa = ease(q)*a_out
            pts = bez((_cx(150), _cy(2.9)), (_cx(500), _cy(1.6)), (_cx(2600), _cy(.55)), 40)
            stroke_pts(ctx, pts, eoc(seg(t, tp, tp + 1.4)), B['ice'], qa*.55, 5, dash=[20, 16])
            tagb(ctx, 1300, 280, 'SPEED  ⇄  RANGE', B['ice'], qa, 30, align='c')
        to = Ts('the opposite trade'); q = seg(t, to - .2, to + .4)
        if q > 0: tagb(ctx, 560, 230, 'BRAHMOS TAKES THE OPPOSITE TRADE', B['amber'], ease(q)*a_out, 26, align='c')
        ts = Ts('sprint supersonic'); q = seg(t, ts - .2, ts + .4)
        if q > 0: tagb(ctx, 1180, 480, 'TERMINAL SPRINT', B['cyan'], ease(q)*a_out*(1 - seg(t, ts + 4, ts + 5)), 22, align='c')
        ctx.restore()
    return scene(f)

# ================= so is it unique? =================
def s_unique(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'SO IS IT UNIQUE?', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=520)
        verdicts = [('UNIQUE?', 'NOT QUITE', 'unique? Not quite', B['steel'], 290),
                    ('RARE?', 'YES', 'in service anywhere are rare', B['cyan'], 520),
                    ("INDIA'S TO SELL?", 'THAT IS WHAT CHANGED', 'sold by India', B['amber'], 750)]
        for i, (k, v, cue, col, y) in enumerate(verdicts):
            t0 = Ts(cue) - .2
            q = seg(t, t0, t0 + .5) if Ts(cue) < 900 else (1. if (first > 0 and i == 0) else 0)
            if q <= 0: continue
            qa = ease(q*1.6)*a_out; dx = 90*(1 - eob(min(q*1.3, 1), 1.3))
            txt(ctx, k, 220 - dx, y, 56, B['steel'], qa, 'bold')
            txt(ctx, v, 820 - dx, y, 76 if len(v) < 12 else 52, col, qa, 'black', glow=1)
        tz = Ts("Zircon is faster"); q = seg(t, tz - .2, tz + .5)
        if q > 0:
            qa = ease(q)*a_out
            card(ctx, 1320, 200, 480, 260, qa, 'FASTER STILL', B['alert'], p=q)
            txt(ctx, 'ZIRCON', 1560, 340, 60, B['ice'], qa, 'black', 'c', glow=.8)
            txt(ctx, 'RUSSIA · HYPERSONIC', 1560, 390, 24, B['alert'], qa, 'bold', 'c', mono=True)
            txt(ctx, 'A DIFFERENT CLASS', 1560, 425, 22, B['steel'], qa, 'bold', 'c', mono=True)
        to = Ts('still a Russian missile'); q = seg(t, to - .2, to + .4)
        if q > 0: tagb(ctx, 1560, 540, 'ONIKS IS STILL RUSSIAN', B['steel'], ease(q)*a_out, 24, align='c')
        tb = Ts('built in India'); q = seg(t, tb - .2, tb + .5)
        if q > 0:
            for j, l in enumerate(('BUILT IN INDIA', 'IMPROVED IN INDIA', 'SOLD BY INDIA')):
                tagb(ctx, 400 + j*560, 900, l, B['amber'], ease(seg(t, tb + j*.25, tb + .5 + j*.25))*a_out, 26, align='c')
        ctx.restore()
    return scene(f)

# ================= the 2022 accident =================
def s_accident(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'THE ACCIDENT · 9 MARCH 2022', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        swap = ease(seg(t, Ts("accidental firing caused") - .5, Ts("accidental firing caused") + .3)) if Ts("accidental firing caused") < 900 else (1. if first > 0 else 0)
        if swap < 1:
            aa = (1 - swap)*a
            txt(ctx, '9 MARCH 2022', 200, 300, 96, B['alert'], aa, 'black', glow=1)
            txt(ctx, 'FIRED BY MISTAKE', 200, 370, 36, B['ice'], aa*ease(seg(t, Ts('fired by mistake') - .2, Ts('fired by mistake') + .3)), 'bold', mono=True)
            # a plain arc to a labelled pin: no borders, no geography
            p0, p1 = (330, 720), (1560, 720)
            pts = bez(p0, ((p0[0] + p1[0])/2, 380), p1, 40)
            go = Ts('fired by mistake')
            q = eoc(seg(t, go, go + 2.6)) if go < 900 else 1.
            truck(ctx, 300, 760, .4, aa, t, raise_=.9)
            stroke_pts(ctx, pts, q, B['alert'], aa, 4, dash=[18, 14])
            if q >= 1:
                glow_dot(ctx, p1[0], p1[1], 10, B['alert'], aa)
                txt(ctx, 'MIAN CHANNU', p1[0], p1[1] - 50, 34, B['ice'], aa, 'black', 'c', glow=.5)
                txt(ctx, 'PUNJAB PROVINCE, PAKISTAN', p1[0], p1[1] - 14, 22, B['alert'], aa, 'bold', 'c', mono=True)
            for j, (lab, cue, x) in enumerate((('NO WARHEAD', 'It carried no warhead', 560), ('NOBODY HURT', 'nobody was hurt', 940))):
                qq = seg(t, Ts(cue) - .2, Ts(cue) + .4)
                if qq > 0: tagb(ctx, x, 790, lab, B['cyan'], ease(qq)*a_out*(1 - swap), 26, align='c')
        if swap > 0:
            aa = swap*a_out
            sides = [('INDIA SAYS', ['Accidental firing', 'Technical malfunction during', 'routine maintenance', 'Deeply regretted', '3 IAF officers dismissed, Aug 2022'], B['cyan'], "accidental firing caused"),
                     ('PAKISTAN SAYS', ["India's explanation was", 'inadequate', 'Asked for a joint investigation', '(which did not happen)'], B['steel'], "called India's explanation")]
            for i, (head, lines, col, cue) in enumerate(sides):
                q = seg(t, Ts(cue) - .2, Ts(cue) + .6) if Ts(cue) < 900 else (1. if i == 0 else 0)
                if q <= 0: continue
                x = 140 + i*860; qa = ease(q)*aa
                card(ctx, x, 220, 820, 580, qa, head, col, p=q)
                figure(ctx, x + 110, 440, 1.0, B['ice'], qa, t, seed=i)
                for j, l in enumerate(lines):
                    txt(ctx, l, x + 230, 400 + j*62, 30, B['ice'], ease(seg(t, Ts(cue) + .2 + j*.2, Ts(cue) + .6 + j*.2))*aa if Ts(cue) < 900 else qa, 'bold' if j == 0 else 'reg')
            tn = Ts('only publicly known case'); q = seg(t, tn - .3, tn + .5)
            if q > 0:
                qa = ease(q)*a_out
                fill(ctx, lambda: rrect(ctx, 140, 830, 1640, 110, 10), B['deep'], .92*qa)
                stroke_pts(ctx, rect_pts(140, 830, 1640, 110), 1, B['alert'], qa, 3)
                for j, l in enumerate(wrap(ctx, 'The only publicly known case of one nuclear-armed state accidentally firing a missile into another.', 34, 1560, 'bold')):
                    txt(ctx, l, 180, 878 + j*42, 34, B['ice'], qa, 'bold')
        ctx.restore()
    return scene(f)

# ================= Operation Sindoor: on the record vs reported =================
def s_war(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'OPERATION SINDOOR · 9–10 MAY 2025', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tc = Ts('be careful here')
        warn = ease(seg(t, tc - .3, tc + .3)) if tc < 900 else 1.
        if first == 0:
            # the title lifts and shrinks as the caution lands; the cards wait for the next beat
            sc = 1 - .42*warn
            ctx.save(); ctx.translate(W/2, lerp(430, 270, warn)); ctx.scale(sc, sc)
            txt(ctx, 'OPERATION SINDOOR', 0, 0, 110, B['ice'], a, 'black', 'c', glow=1)
            ctx.restore()
            txt(ctx, 'MAY 2025', W/2, lerp(510, 350, warn), 44*(1 - .3*warn), B['amber'], a, 'black', 'c')
            td = Ts('ninth and tenth of May')
            if td < 900:
                txt(ctx, 'INDIA STRUCK TARGETS IN PAKISTAN', W/2, lerp(580, 410, warn), 28, B['steel'],
                    ease(seg(t, td - .2, td + .4))*a_out, 'bold', 'c', mono=True)
            if warn > 0:
                tagb(ctx, W/2, 600, 'BE CAREFUL WITH WHAT YOU READ ABOUT THIS', B['alert'], warn*a_out, 30, align='c')
            ctx.restore(); return
        q1 = ease(seg(t, Ts('media accounts') - .6, Ts('media accounts') + .3))*a_out if Ts('media accounts') < 900 else a_out
        if q1 > 0:
            card(ctx, 120, 220, 800, 560, q1*.75, 'REPORTED · NOT OFFICIAL', B['steel'], p=q1)
            for j, l in enumerate(('Exact numbers of missiles', 'Lists of airbases struck', 'Media accounts only')):
                txt(ctx, l, 170, 400 + j*64, 32, B['steel'], q1*.8, 'bold')
            ctx.save(); ctx.translate(520, 640); ctx.rotate(-.12)
            txt(ctx, 'NOT CONFIRMED', 0, 0, 52, B['alert'], q1*.9, 'black', 'c', glow=.5); ctx.restore()
            txt(ctx, 'NO OFFICIAL WEAPONS LIST PUBLISHED', 520, 740, 22, B['steel'], q1*.9, 'bold', 'c', mono=True)
        q2 = ease(seg(t, Ts('What is on the record') - .3, Ts('What is on the record') + .4))*a_out if Ts('What is on the record') < 900 else (a_out if first > 2 else 0)
        if q2 > 0:
            card(ctx, 1000, 220, 800, 560, q2, 'ON THE RECORD · 18 OCT 2025', B['amber'], p=q2)
            for j, l in enumerate(wrap(ctx, '"Every inch of Pakistan is within the reach of BrahMos."', 36, 700, 'bold')):
                txt(ctx, l, 1040, 380 + j*48, 36, B['ice'], q2, 'bold')
            for j, l in enumerate(wrap(ctx, '"The operation was just a trailer."', 36, 700, 'bold')):
                txt(ctx, l, 1040, 540 + j*48, 36, B['amber'], ease(seg(t, Ts('just a trailer') - .3, Ts('just a trailer') + .3))*a_out, 'bold')
            txt(ctx, 'DEFENCE MINISTER, AT THE LUCKNOW PLANT', 1040, 700, 22, B['cyan'], q2, 'bold', mono=True)
        tr = Ts('Read that how you like'); q = seg(t, tr - .2, tr + .4)
        if q > 0:
            qa = ease(q)*a_out
            fill(ctx, lambda: rrect(ctx, 300, 830, 1320, 100, 10), B['deep'], .92*qa)
            stroke_pts(ctx, rect_pts(300, 830, 1320, 100), 1, B['cyan'], qa, 3)
            txt(ctx, 'AN UNUSUALLY DIRECT STATEMENT', W/2, 896, 38, B['ice'], qa, 'black', 'c')
        ctx.restore()
    return scene(f)

# ================= who has it: the export board =================
BUY = [('PHILIPPINES', '19 APR 2024 · FIRST DELIVERY', 'That changed with the Philippines', 620, 520),
       ('VIETNAM', 'ORDER CONFIRMED · MAY 2026', 'Since then, Vietnam', 1010, 330),
       ('INDONESIA', 'SIGNED · JULY 2026', 'Indonesia signed', 1130, 700)]
def s_board(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'WHO HAS IT', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=520)
        a = fin(t, .1, .6)*a_out if first == 0 else a_out
        sea_board(ctx, t, a*.8, washes=((940, 540, 420), (1280, 640, 300)),
                  lanes=(((430, 760), (1130, 700)), ((620, 520), (1010, 330))))
        txt(ctx, 'SOUTH CHINA SEA', 1180, 500, 26, B['steel'], a*.75, 'bold', 'c', mono=True)
        for i, (nm, sub, cue, x, y) in enumerate(BUY):
            t0 = Ts(cue) - .2
            p = seg(t, t0, t0 + 1.2) if Ts(cue) < 900 else (1. if (first > 0 and i == 0) or (first > 1 and i < 2) else 0)
            if p <= 0: continue
            pin(ctx, x, y, nm, sub, B['amber'] if i == 0 else B['cyan'], a_out, p=p, t=t)
        tf = Ts('For twenty years'); q = seg(t, tf - .2, tf + .5)
        if q > 0 and first == 0:
            txt(ctx, "FOR 20 YEARS: INDIA'S ALONE", 300, 250, 34, B['steel'], ease(q)*a_out*(1 - seg(t, Ts('That changed') - .3, Ts('That changed'))), 'black')
        tm = Ts('three hundred and seventy-five million'); q = seg(t, tm - .3, tm + .5)
        if q > 0: tagb(ctx, 400, 300, 'PHILIPPINES · JAN 2022 · ~$375 MILLION', B['amber'], ease(q)*a_out, 24, align='c')
        tfe = Ts('exported a major missile system'); q = seg(t, tfe - .2, tfe + .5)
        if q > 0: tagb(ctx, 500, 880, "INDIA'S FIRST BIG MISSILE EXPORT", B['ice'], ease(q)*a_out, 28, align='c')
        ti = Ts('between two hundred and three hundred'); q = seg(t, ti - .3, ti + .5)
        if q > 0: tagb(ctx, 1480, 880, 'INDONESIA · REPORTED $200–350 MILLION', B['cyan'], ease(q)*a_out, 22, align='c')
        ctx.restore()
        schematic_note(ctx, a_out)
    return scene(f)

# ================= who wants it =================
WANT = [('UAE', 'United Arab Emirates'), ('SAUDI ARABIA', 'Saudi Arabia'), ('EGYPT', 'Egypt'), ('VIETNAM', 'and Vietnam')]
def s_interest(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'WHO ELSE WANTS IT', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
        tn = Ts('notice where the actual buyers')
        swap = ease(seg(t, tn - .4, tn + .4)) if Ts('notice where the actual buyers') < 900 else (1. if first > 0 else 0)
        if swap < 1:
            aa = (1 - swap)*a_out
            txt(ctx, 'REPORTED INTEREST', W/2, 280, 64, B['steel'], fin(t, .1, .5)*aa, 'black', 'c')
            txt(ctx, 'THE TRIBUNE · FEB 2025 · CITING UNNAMED SOURCES', W/2, 330, 24, B['alert'], fin(t, .2, .5)*aa, 'bold', 'c', mono=True)
            for i, (nm, cue) in enumerate(WANT):
                q = seg(t, Ts(cue) - .15, Ts(cue) + .4)
                if q <= 0: continue
                x = 180 + i*420; y = 470; qa = ease(q*1.6)*aa; s = eob(q, 1.6)
                ctx.save(); ctx.translate(x + 180, y + 90); ctx.scale(s, s); ctx.translate(-(x + 180), -(y + 90))
                card(ctx, x, y, 360, 180, qa, None, B['steel'], p=q)
                for j, l in enumerate(wrap(ctx, nm, 40, 300, 'black')):
                    txt(ctx, l, x + 180, y + (105 if len(wrap(ctx, nm, 40, 300, 'black')) == 1 else 80) + j*48, 40, B['steel'], qa, 'black', 'c')
                ctx.restore()
            tr = Ts('reports, not contracts'); q = seg(t, tr - .2, tr + .4)
            if q > 0:
                ctx.save(); ctx.translate(W/2, 760); ctx.rotate(-.03); ctx.scale(eob(q, 1.8), eob(q, 1.8))
                tagb(ctx, 0, 0, 'REPORTS, NOT CONTRACTS', B['alert'], ease(q*2)*aa, 34, align='c'); ctx.restore()
        if swap > 0:
            aa = swap*a_out
            sea_board(ctx, t, aa*.7, washes=((960, 540, 400),), lanes=(((700, 700), (1200, 380)),))
            for i, (nm, x, y) in enumerate((('PHILIPPINES', 700, 700), ('VIETNAM', 820, 380), ('INDONESIA', 1200, 640))):
                q = ease(seg(t, Ts('all three sit') - .4 + i*.2, Ts('all three sit') + i*.2))*aa if Ts('all three sit') < 900 else aa
                glow_dot(ctx, x, y, 13, B['amber'], q)
                txt(ctx, nm, x, y - 36, 32, B['ice'], q, 'black', 'c', glow=.6)
            q = ease(seg(t, Ts('South China Sea') - .2, Ts('South China Sea') + .4))*aa
            if q > 0:
                txt(ctx, 'SOUTH CHINA SEA', 1010, 540, 46, B['steel'], q, 'black', 'c')
                ctx.new_path(); rgba(ctx, B['amber'], q*.5); ctx.set_line_width(4); ctx.set_dash([18, 14])
                ctx.arc(1000, 540, 300, 0, 2*math.pi); ctx.stroke(); ctx.set_dash([])
            qq = ease(seg(t, Ts('very specific answer') - .2, Ts('very specific answer') + .4))*a_out
            if qq > 0: tagb(ctx, W/2, 900, 'A SPECIFIC ANSWER TO A SPECIFIC PROBLEM', B['ice'], qq, 30, align='c')
            schematic_note(ctx, aa)
        ctx.restore()
    return scene(f)

# ================= Lucknow =================
def s_lucknow(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'THE LUCKNOW PLANT · FLAGGED OFF OCT 2025', a_out, EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
    a = fin(t, .1, .5)*a_out
    stroke_pts(ctx, [(90, 800), (1830, 800)], 1, B['dim'], a, 2, glow=False)
    for k in range(4):
        x = 180 + k*430
        stroke_pts(ctx, [(x, 800), (x, 660), (x + 300, 660), (x + 300, 800)], fin(t, .2 + k*.12, .5), B['ice'], a*.8, 3)
        stroke_pts(ctx, [(x, 660), (x + 150, 600), (x + 300, 660)], fin(t, .3 + k*.12, .5), B['steel'], a*.8, 2.5)
    stats = [('200', 'ACRES', 'two hundred acres', 400), ('380', 'CRORE RUPEES', 'three hundred and eighty crore', 960), ('~100', 'SYSTEMS A YEAR', 'a hundred missile systems', 1520)]
    for (v, lab, cue, x) in stats:
        t0 = Ts(cue) - .3; q = seg(t, t0, t0 + 1.0)
        if q <= 0: continue
        qa = ease(min(q*2, 1))*a_out
        num = v if v.startswith('~') else str(int(int(v)*eoc(q)))
        if v.startswith('~'): num = '~' + str(int(100*eoc(q)))
        txt(ctx, num, x, 380, 130, B['amber'], qa, 'black', 'c', glow=1.2)
        txt(ctx, lab, x, 440, 28, B['cyan'], qa, 'bold', 'c', mono=True)
    ts = Ts('not a showpiece'); q = seg(t, ts - .2, ts + .4)
    if q > 0: tagb(ctx, W/2, 900, 'A SUPPLY LINE, NOT A SHOWPIECE', B['ice'], ease(q)*a_out, 32, align='c')
    ctx.restore()
scene(s_lucknow)

# ================= BrahMos-NG =================
def s_ng(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'BRAHMOS-NG · NEXT GENERATION', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        shrink = ease(seg(t, Ts('about six metres') - .3, Ts('about six metres') + 1.2)) if Ts('about six metres') < 900 else 1.
        # the current missile shrinking into the NG
        L = lerp(1300, 920, shrink)
        missile(ctx, 880, 290, 1240, 0, a*(1 - shrink*.75), p=fin(t, .1, .8), col=B['steel'], fill_a=.06)
        txt(ctx, 'BRAHMOS · 8.4 M · 3,000 KG', 880, 195, 30, B['steel'], a*(1 - shrink*.4), 'black', 'c')
        if shrink > .1:
            missile(ctx, 820, 500, L, 0, a*shrink, col=B['amber'])
            txt(ctx, 'BRAHMOS-NG · ~6 M · UNDER 1,500 KG', 820, 405, 32, B['amber'], a*shrink, 'black', 'c', glow=.6)
        # Tejas carrying more of them
        tq = ease(seg(t, Ts('including the Tejas') - .3, Ts('including the Tejas') + .5))*a_out
        if tq > 0:
            jet(ctx, 1480, 740, .62, tq, t, load=False)
            for k in range(2):
                missile(ctx, 1400 + k*170, 800, 190, 0, tq*ease(seg(t, Ts('including the Tejas') + .3 + k*.2, Ts('including the Tejas') + .7 + k*.2)), col=B['amber'])
            tagb(ctx, 1480, 900, 'FITS MORE AIRCRAFT · INCLUDING TEJAS', B['cyan'], tq, 24, align='c')
        rows = [('FIRST FLIGHT TEST', 'AROUND 2026', 'first flight test', B['cyan']),
                ('PRODUCTION', '2027–28', 'production from 2027', B['cyan']),
                ('BRAHMOS-II (HYPERSONIC)', 'STILL A CONCEPT', 'remains a concept', B['steel'])]
        for i, (k, v, cue, col) in enumerate(rows):
            q = seg(t, Ts(cue) - .2, Ts(cue) + .5)
            if q <= 0: continue
            y = 690 + i*92; qa = ease(q)*a_out
            txt(ctx, k, 140, y, 26, col, qa, 'bold', mono=True)
            txt(ctx, v, 140, y + 44, 40, B['ice'] if i < 2 else B['steel'], qa, 'black', glow=.4 if i < 2 else 0)
        tsrc = Ts('BrahMos Aerospace says'); q = seg(t, tsrc - .2, tsrc + .4)
        if q > 0: txt(ctx, 'SOURCE: BRAHMOS AEROSPACE', W - 70, 935, 18, B['steel'], ease(q)*a_out, 'reg', 'r', mono=True)
        ctx.restore()
    return scene(f)

# ================= in three words =================
def s_three(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'BRAHMOS IN THREE WORDS', a_out, EP)
    waves(ctx, 860, t, a_out*.7)
    path = [(120 + k*28, 800 - 300*min(1, (k/30)**.6) + 10*math.sin(k*.4)) for k in range(61)]
    stroke_pts(ctx, path, ease(seg(t, .3, 3.0)), B['amber'], a_out*.5, 3)
    words = [('FAST', 'CLOSE TO 3× THE SPEED OF SOUND', 'Fast:', 400), ('LOW', '~10 M ABOVE THE SEA', 'Low:', 960), ('ALONE', 'FIRE AND FORGET', 'Alone:', 1520)]
    for i, (w_, sub, cue, x) in enumerate(words):
        q = seg(t, Ts(cue) - .15, Ts(cue) + .35)
        if q <= 0: continue
        sc = lerp(1.7, 1, eob(q, 1.4))
        ctx.save(); ctx.translate(x, 520); ctx.scale(sc, sc)
        txt(ctx, w_, 0, 0, 140, B['amber'], ease(q*2)*a_out, 'black', 'c', glow=2)
        ctx.restore()
        for j, l in enumerate(wrap(ctx, sub, 24, 480, 'bold', True)):
            txt(ctx, l, x, 600 + j*34, 24, B['ice'], ease(seg(t, Ts(cue) + .3, Ts(cue) + .7))*a_out, 'bold', 'c', mono=True)
scene(s_three)

# ================= the blueprint wall =================
WALL = [('EP 1 · PRALAY', 1.), ('EP 2 · BRAHMOS', None)]
def _wcard(ctx, x, y, w, h, a, t, label, col=None):
    col = col or B['cyan']
    fill(ctx, lambda: rrect(ctx, x, y, w, h, 8), B['deep'], .9*a)
    stroke_pts(ctx, rect_pts(x, y, w, h), 1, col, a, 2.5)
    missile(ctx, x + w/2, y + h*.42, w*.8, 0, a, col=col)
    txt(ctx, label, x + 22, y + h - 28, 24, B['ice'], a, 'black')
    glow_dot(ctx, x + w/2, y + 14, 6, B['amber'], a)
def s_wall(ctx, t, D):
    bg(ctx); a_out = outro(t, D, .8)
    hud(ctx, t, "THE BLUEPRINT WALL", a_out, EP)
    for i in range(10):
        x = 160 + (i % 5)*330; y = 200 + (i//5)*300
        if i < 2: continue
        stroke_pts(ctx, rect_pts(x, y, 290, 240), 1, B['grid'], a_out, 2, glow=False, dash=[10, 10])
        txt(ctx, f'EP {i+1}', x + 145, y + 130, 24, B['grid'], a_out, 'bold', 'c', mono=True)
    _wcard(ctx, 160, 200, 290, 240, a_out*.85, t, 'EP 1 · PRALAY', B['steel'])
    q = seg(t, .3, 1.0)
    yy = lerp(-300, 200, eob(q, 1.3))
    _wcard(ctx, 490, yy, 290, 240, a_out, t, 'EP 2 · BRAHMOS', B['amber'])
    tb = Ts('built in Lucknow')
    for i, (l, cue) in enumerate((('RUSSIAN DESIGN · INDIAN NAME', 'a Russian design'), ('BUILT IN LUCKNOW', 'built in Lucknow'),
                                  ('REPORTED 75%+ INDIAN CONTENT', 'three-quarters Indian'), ('SOLD TO THREE COUNTRIES', 'sold to three countries'))):
        qq = seg(t, Ts(cue) - .2, Ts(cue) + .4)
        if qq > 0: tagb(ctx, 1150, 260 + i*76, l, B['cyan'] if i else B['steel'], ease(qq)*a_out, 26)
    tn = Ts('Next on'); nq = seg(t, tn, tn + .6)
    if nq > 0:
        a = ease(nq)*a_out
        stroke_pts(ctx, rect_pts(820, 200, 290, 240), nq, B['amber'], a, 2.5)
        txt(ctx, 'EP 3 · AGNI-5', 965, 330, 26, B['amber'], a, 'black', 'c')
        fill(ctx, lambda: ctx.rectangle(0, 830, W*eoc(nq), 90), B['deep'], .95*a)
        rgba(ctx, B['cyan'], a); ctx.rectangle(0, 830, W*eoc(nq), 3); ctx.fill()
        txt(ctx, 'NEXT  ·  AGNI-5, AND MANY WARHEADS ON ONE MISSILE', 80, 888, 32, B['ice'], a, 'bold', mono=True)
    subscribe_card(ctx, t, Ts('subscribe'), a_out, x=1540, y=700)
scene(s_wall)

# ================= beats =================
SC = {
 'cold1': s_factory(0), 'cold2': s_factory(1),
 'qs1': s_questions, 'qs2': s_questions,
 'born1': s_moscow(0), 'born2': s_moscow(1),
 'born3': s_oniks, 'born4': s_timeline,
 'cap1': s_speed(0), 'cap2': s_speed(1),
 'cap3': s_horizon(0), 'cap4': s_horizon(1),
 'cap5': s_guidance(0), 'cap6': s_guidance(1),
 'cap7': s_platforms,
 'rng1': s_range(0), 'rng2': s_range(1), 'rng3': s_range(2),
 'cmp1': s_chart(0), 'cmp2': s_chart(1), 'cmp3': s_chart(2),
 'unq1': s_unique(0), 'unq2': s_unique(1),
 'acc1': s_accident(0), 'acc2': s_accident(1), 'acc3': s_accident(2),
 'war1': s_war(0), 'war2': s_war(1), 'war3': s_war(2), 'war4': s_war(3),
 'exp1': s_board(0), 'exp2': s_board(1), 'exp3': s_board(2),
 'exp4': s_interest(0), 'exp5': s_interest(1),
 'nxt1': s_lucknow, 'nxt2': s_ng(0), 'nxt3': s_ng(1),
 'three': s_three, 'end1': s_wall, 'end2': s_wall,
}
BEATS = [(k, n, SC[k]) for k, n in EN]

GROUPS = {}
for g, ks in {'cold': ['cold1', 'cold2'], 'qs': ['qs1', 'qs2'], 'mos': ['born1', 'born2'], 'spd': ['cap1', 'cap2'],
              'hor': ['cap3', 'cap4'], 'gui': ['cap5', 'cap6'], 'rng': ['rng1', 'rng2', 'rng3'],
              'cmp': ['cmp1', 'cmp2', 'cmp3'], 'unq': ['unq1', 'unq2'], 'acc': ['acc1', 'acc2', 'acc3'],
              'war': ['war1', 'war2', 'war3', 'war4'], 'exp': ['exp1', 'exp2', 'exp3'], 'int': ['exp4', 'exp5'],
              'ng': ['nxt2', 'nxt3'], 'wall': ['end1', 'end2']}.items():
    for k in ks: GROUPS[k] = g

KEYS = {
 'cold2': [('just a trailer', 'JUST A TRAILER', 'amber')],
 'born2': [('Two rivers', 'TWO RIVERS', 'cyan')],
 'cap1': [('three times the speed of sound', 'MACH ~3, ALL THE WAY', 'amber')],
 'cap2': [('they have seconds', 'SECONDS TO REACT', 'alert')],
 'cap3': [('ten metres above the sea', '~10 METRES', 'amber')],
 'cap6': [('two hundred to three hundred', '200–300 KG', 'cyan')],
 'rng2': [('India joined', 'MTCR · 2016', 'cyan')],
 'cmp3': [('the opposite trade', 'THE OPPOSITE TRADE', 'amber')],
 'acc1': [('nobody was hurt', 'NO WARHEAD · NO CASUALTIES', 'cyan')],
 'war2': [('media accounts', 'NOT OFFICIAL', 'alert')],
 'exp2': [('nineteenth of April 2024', 'FIRST EXPORT DELIVERY', 'amber')],
 'nxt1': [('a hundred missile systems', '~100 A YEAR', 'amber')],
}
ANNOT = {
 'cap4': [('almost no time left', 'circle', 1500, 300, 420, 110)],
 'cmp3': [('the opposite trade', 'circle', _cx(400), _cy(3.0), 320, 150)],
 'unq2': [('sold by India', 'underline', 1330, 790, 460, 0)],
}

_order = [k for k, _ in EN]
FX = [('whoosh', k, -.25, .22) for i, k in enumerate(_order) if i and GROUPS.get(k, k) != GROUPS.get(_order[i-1], _order[i-1])]
FX += [('beep', k, ph, .14) for k, items in KEYS.items() for ph, _, _ in items]
FX += [('tick', 'cold1', .15, .12), ('boom', 'cold1', 'Then fire', .4),
       ('riser', 'qs1', 'This is BrahMos', .25), ('boom', 'qs1', 'This is BrahMos', .5),
       ('stamp', 'born2', 'Two rivers', .4), ('ping', 'cap4', "A ship's radar looks out", .3),
       ('boom', 'rng2', 'India joined', .4), ('ping', 'cmp1', "Let's line them up", .25),
       ('glitch', 'acc1', 'fired by mistake', .3), ('boom', 'acc3', 'only publicly known case', .4),
       ('boom', 'war3', 'What is on the record', .35),
       ('stamp', 'exp2', 'nineteenth of April 2024', .35), ('pluck', 'exp3', 'Since then, Vietnam', .3),
       ('riser', 'three', 'Fast:', .15), ('ding', 'three', 'Fast:', .25), ('ding', 'three', 'Low:', .25), ('ding', 'three', 'Alone:', .25),
       ('stamp', 'end1', .5, .35), ('ding', 'end2', 'subscribe', .2)]
