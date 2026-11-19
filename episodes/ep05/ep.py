"""India's Defence, Decoded — Episode 5: The Forty-Year Jet (bilingual: English + Hindi).

No maps in this episode: bases and test institutes are named in text only, never plotted.
No flags, no logos, no likenesses. The Dubai beat draws no aircraft at all.
"""
import os, sys, math, random, cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 940.0
core.TOTAL = TOTAL
from engine.core import W, H, seg, ease, eoc, eob, lerp, T
from engine.bp import (B, rgba, rrect, bg, txt, tw, typed, wrap, para, stroke_pts, head_pt, rect_pts, fill, glow_dot,
                       bez, figure, hud, card, tagb, outro, camera, scene, subscribe_card)
from engine.shield import statusrow
from engine.jet import (jet, jet_pts, jet_engine, icon_shape, icon_chip, icon_dish, icon_turbine, problem,
                        timeline, plane_row, turbine_cut, testbed, track, sqnbars, wall)
from text import EN, HI as _HI

EP = 5
CODE = 'Def05'
TITLE = 'The_Forty_Year_Jet'
NAME = "Why India's Own Fighter Took Forty Years"
POST = 'engine.bp'
BED = 'pulse'
VOICE_EN = {'length': 0.98, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
VOICE_HI = {'length': 0.86, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
CRF, PRESET = 17, 'medium'
EXTRA = {'cold1': .8, 'cold2': .6, 'dub1': .6, 'dub2': 1.2, 'three1': 1.4, 'end1': 2.5}
HI = _HI


def Ts(x):
    try: return T(x)
    except ValueError: return 999.


def cue(t, s, lead=.2, dur=.45):
    c = Ts(s)
    return 0. if c >= 900 else seg(t, c - lead, c - lead + dur)


def fin(t, t0=.1, d=.6): return ease(seg(t, t0, t0 + d))


# ================= 1. cold open: the aircraft without engines =================
def s_cold(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'LCA TEJAS MK1A · CONTRACT 3 FEB 2021 · STATUS AS OF 19 NOV 2026', a, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), (0, -14))
        p = fin(t, .2, 2.6) if i == 0 else 1.
        jet(ctx, 760, 560, .95, p, a)
        dotted = True
        jet_engine(ctx, 760, 560, .95, a*(.55 + .25*math.sin(t*2.2)), min(1, max(0, (p - .8)*5)) if i == 0 else 1., dotted)
        if i == 0:
            q = cue(t, 'Forty-eight thousand crore', .25, .5)
            if q > 0:
                card(ctx, 1290, 250, 520, 190, a*ease(q), 'THE CONTRACT', B['cyan'], ease(q))
                txt(ctx, '3 FEB 2021', 1320, 350, 46, B['ice'], a*ease(seg(q, .3, 1)), 'black')
                txt(ctx, '₹48,000 CRORE  ·  83 JETS', 1320, 400, 24, B['steel'], a*ease(seg(q, .5, 1)), 'bold', mono=True)
            q2 = cue(t, 'The third year was 2024', .2, .5)
            if q2 > 0:
                card(ctx, 1290, 470, 520, 150, a*ease(q2), 'FIRST DELIVERY DUE', B['steel'], ease(q2))
                txt(ctx, 'FEBRUARY 2024', 1320, 570, 40, B['ice'], a*ease(seg(q2, .3, 1)), 'black')
        else:
            card(ctx, 1290, 250, 520, 190, a, 'HANDED OVER TO THE IAF', B['alert'], 1.)
            z = cue(t, 'the number handed over is zero', .2, .6)
            txt(ctx, '0', 1550, 400, 120, B['alert'], a*(.35 + .65*ease(z)), 'black', 'c', glow=1.2)
            q = cue(t, 'ten were already built', .25, .5)
            if q > 0:
                card(ctx, 1290, 470, 520, 240, a*ease(q), 'BUILT, SEPTEMBER 2025', B['cyan'], ease(q))
                txt(ctx, '10', 1400, 610, 86, B['ice'], a*ease(seg(q, .2, 1)), 'black', 'c')
                txt(ctx, 'HAL OFFICIALS,', 1500, 580, 22, B['steel'], a*ease(seg(q, .4, 1)), 'bold', mono=True)
                txt(ctx, 'AS REPORTED', 1500, 608, 22, B['steel'], a*ease(seg(q, .5, 1)), 'bold', mono=True)
            e = cue(t, 'is an engine', .2, .5)
            if e > 0: tagb(ctx, 760, 900, 'NO ENGINE', B['alert'], a*ease(e), 30, align='c')
        ctx.restore()
    return scene(f)


# ================= 2. the anchor: four problems =================
PROBS = [('SHAPE', 'ONE', icon_shape), ('CONTROL', 'TWO', icon_chip),
         ('SENSE', 'THREE', icon_dish), ('POWER', 'FOUR', icon_turbine)]


def s_four(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'FOUR PROBLEMS, NOT ONE', a, EP)
        cues = ['One: shape', 'Two: control', 'Three: sensing', 'Four: power']
        for k, ((lab, n, ic), c) in enumerate(zip(PROBS, cues)):
            x = 330 + k*434
            p = cue(t, c, .3, .8) if i == 0 else 1.
            if i == 1 and k < 3: p = 1.
            if p <= 0: continue
            col = B['amber'] if k == 3 else B['cyan']
            problem(ctx, x, 430, lab, n, ic, col, a, p, t, 0.)
        if i == 1:
            q = cue(t, 'Hold those four', .25, .6)
            if q > 0:
                txt(ctx, 'INDIA SOLVED THREE', 960, 790, 46, B['ice'], a*ease(q), 'black', 'c', glow=.6)
                stroke_pts(ctx, [(560, 816), (1360, 816)], ease(seg(q, .3, 1)), B['cyan'], a, 3, glow=False)
        else:
            q = cue(t, 'no human can fly it', .25, .5)
            if q > 0: tagb(ctx, 960, 800, 'UNSTABLE BY DESIGN · FLOWN BY COMPUTER', B['cyan'], a*ease(q), 26, align='c')
    return scene(f)


# ================= 3. four questions =================
QS = ['WHY START IN 1983?', 'WHAT NEARLY KILLED IT?', 'WHAT IS THE MARK 1A?', 'CAN INDIA BUILD THE ENGINE?']


def s_qs(ctx, t, D):
    bg(ctx); a = outro(t, D, .35)
    hud(ctx, t, 'FOUR QUESTIONS', a, EP)
    for k, q_ in enumerate(QS):
        p = ease(seg(t, .5 + k*.75, 1.3 + k*.75))
        if p <= 0: continue
        y = 250 + k*160
        x = lerp(-500, 300, eob(p, 1.6))
        col = B['amber'] if k == 3 else B['cyan']
        card(ctx, x, y, 1320, 124, a*p, None, col, 1.)
        txt(ctx, f'{k+1}', x + 46, y + 86, 56, col, a*p, 'black')
        txt(ctx, q_, x + 130, y + 82, 44, B['ice'], a*p, 'black')
s_qs = scene(s_qs)


# ================= 4. 1983 =================
def s_why(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'AUGUST 1983 · THE LIGHT COMBAT AIRCRAFT PROGRAMME', a, EP)
        if i == 0:
            plane_row(ctx, 300, 9, a*.9, gone=ease(seg(t, 1.2, 5.5))*.9)
            txt(ctx, 'MiG-21  ·  THE BACKBONE, AND AGEING', 960, 410, 28, B['steel'], a, 'bold', 'c', mono=True)
            q = cue(t, 'two choices', .25, .6)
            if q > 0:
                for k, (lab, sub, col) in enumerate((('BUY IT', 'as India always had', B['steel']),
                                                     ('BUILD IT', 'learn to make one', B['cyan']))):
                    qq = ease(seg(q, k*.25, .6 + k*.25))
                    if qq <= 0: continue
                    x = 330 + k*700
                    card(ctx, x, 520, 540, 180, a*qq, None, col, 1.)
                    txt(ctx, lab, x + 40, 600, 54, B['ice'], a*qq, 'black')
                    txt(ctx, sub, x + 40, 652, 24, col, a*qq, 'bold', mono=True)
            s = cue(t, 'five hundred and sixty crore', .25, .5)
            if s > 0: tagb(ctx, 960, 810, '₹560 CRORE · PROJECT DEFINITION PHASE', B['amber'], a*ease(s), 28, align='c')
        else:
            card(ctx, 180, 220, 740, 480, a, 'WHO WOULD DO IT', B['cyan'], 1.)
            for k, (name, role) in enumerate((('ADA', 'Aeronautical Development Agency  ·  design'),
                                              ('HAL', 'Hindustan Aeronautics Limited  ·  build'))):
                q = ease(seg(t, .3 + k*.7, 1.1 + k*.7))
                if q <= 0: continue
                txt(ctx, name, 220, 360 + k*150, 64, B['ice'], a*q, 'black')
                txt(ctx, role, 220, 400 + k*150, 22, B['steel'], a*q, 'bold', mono=True)
            miss = [('NO MODERN AVIONICS BASE', 'had very little of the industry'),
                    ('NO COMPOSITES INDUSTRY AT SCALE', 'no composites industry at scale'),
                    ('NO WORKING MILITARY TURBOFAN', 'no engine house')]
            for k, (lab, c) in enumerate(miss):
                q = cue(t, c, .2, .5)
                if q > 0: tagb(ctx, 1010, 300 + k*110, lab, B['alert'], a*ease(q), 26)
            fq = cue(t, 'First flight was targeted for 1994', .2, .5)
            if fq > 0: tagb(ctx, 1010, 660, 'FIRST FLIGHT TARGETED: 1994', B['amber'], a*ease(fq), 28)
    return scene(f)


# ================= 5. 1998: the embargo =================
def s_emb(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'MAY 1998 · THE TECHNOLOGY EMBARGO', a, EP)
        if i == 0:
            q = fin(t, .3, 1.0)
            txt(ctx, 'MAY 1998', 960, 300, 92, B['ice'], a*q, 'black', 'c', glow=.6)
            txt(ctx, 'POKHRAN  ·  US TECHNOLOGY EMBARGO', 960, 356, 28, B['alert'], a*ease(seg(t, .8, 1.6)), 'bold', 'c', mono=True)
            for k, lab in enumerate(('FOREIGN PARTNER', 'FOREIGN PARTNER')):
                qq = cue(t, 'Their engineers went home' if k else 'had both agreed to lend expertise', .2, .6)
                if qq <= 0: continue
                x = 330 + k*700
                grey = ease(cue(t, 'Their engineers went home', 0, 1.2))
                col = B['steel'] if grey > .5 else B['cyan']
                card(ctx, x, 470, 540, 180, a*ease(qq)*(1 - .45*grey), None, col, 1.)
                txt(ctx, 'ENGINEERS', x + 40, 550, 44, B['ice'], a*ease(qq)*(1 - .45*grey), 'black')
                txt(ctx, 'WITHDRAWN' if grey > .5 else 'ON THE PROGRAMME', x + 40, 602, 24, col,
                    a*ease(qq)*(1 - .3*grey), 'bold', mono=True)
            c = cue(t, 'turned the clock back by four years', .25, .6)
            if c > 0: tagb(ctx, 960, 800, 'ONE ACCOUNT: THE CLOCK TURNED BACK FOUR YEARS', B['alert'], a*ease(c), 26, align='c')
        elif i == 1:
            card(ctx, 240, 240, 1440, 300, a, 'WHAT THE EMBARGO LEFT BEHIND', B['cyan'], 1.)
            icon_chip(ctx, 420, 410, 1.5, B['cyan'], a, fin(t, .3, 1.2))
            lines = ['The flight control work had to be finished in India,',
                     'by Indian engineers, because nobody else was left.',
                     'India has that capability permanently now.']
            for k, ln in enumerate(lines):
                q = ease(seg(t, .6 + k*1.1, 1.6 + k*1.1))
                if q > 0: txt(ctx, ln, 600, 360 + k*58, 34, B['ice'], a*q, 'bold')
            c = cue(t, 'bought at a price nobody would have chosen to pay', .25, .6)
            if c > 0: txt(ctx, 'AT A PRICE NOBODY WOULD HAVE CHOSEN TO PAY', 960, 640, 28, B['steel'], a*ease(c), 'bold', 'c', mono=True)
        else:
            jet(ctx, 960, 540, .8, fin(t, .2, 2.2), a)
            q = cue(t, 'fourth of January 2001', .25, .6)
            if q > 0:
                txt(ctx, '4 JANUARY 2001', 960, 230, 76, B['amber'], a*ease(q), 'black', 'c', glow=.8)
                txt(ctx, 'EIGHTEEN YEARS AFTER THE PROGRAMME BEGAN', 960, 280, 26, B['steel'], a*ease(seg(q, .4, 1)), 'bold', 'c', mono=True)
            n = cue(t, 'named it Tejas', .25, .6)
            if n > 0: tagb(ctx, 960, 880, '2003 · NAMED TEJAS', B['cyan'], a*ease(n), 30, align='c')
    return scene(f)


# ================= 6. flying is not serving =================
MARKS = [(.02, '2001', 'FIRST|FLIGHT'), (.22, '2011', 'IOC'), (.38, 'DEC 2013', 'IOC-II'),
         (.60, 'FEB 2019', 'FOC'), (.78, 'JUL 2016', 'No. 45 SQN|FLYING DAGGERS'),
         (.96, '2020', 'No. 18 SQN|FLYING BULLETS')]


def s_clr(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'A FIRST FLIGHT IS ABOUT HALFWAY', a, EP)
        if i == 0:
            cues = ['Tejas got one in 2011', 'a fuller one in December 2013', '', '', '', '']
            marks = [(.02, '2001', 'FIRST|FLIGHT', fin(t, .3, .9)),
                     (.22, '2011', 'IOC', ease(cue(t, 'Tejas got one in 2011', .25, .7))),
                     (.38, 'DEC 2013', 'IOC-II', ease(cue(t, 'a fuller one in December 2013', .25, .7)))]
            timeline(ctx, 220, 1700, 470, marks, a)
            for k, (lab, body) in enumerate((('IOC', 'safe and useful enough to fly properly'),)):
                q = cue(t, 'Initial Operational Clearance', .25, .6)
                if q > 0:
                    card(ctx, 300, 640, 1320, 150, a*ease(q), 'INITIAL OPERATIONAL CLEARANCE', B['cyan'], ease(q))
                    txt(ctx, body, 330, 752, 34, B['ice'], a*ease(seg(q, .3, 1)), 'bold')
        elif i == 1:
            marks = [(.02, '2001', 'FIRST|FLIGHT', 1.), (.22, '2011', 'IOC', 1.), (.38, 'DEC 2013', 'IOC-II', 1.),
                     (.60, 'FEB 2019', 'FOC', ease(fin(t, .4, 1.0)))]
            timeline(ctx, 220, 1700, 470, marks, a)
            card(ctx, 300, 640, 1320, 190, a, 'FINAL OPERATIONAL CLEARANCE', B['amber'], 1.)
            for k, ln in enumerate(('all the weapons  ·  air-to-air refuelling  ·  the full envelope',
                                    'Aero India, February 2019 — years late')):
                q = ease(seg(t, .5 + k*1.0, 1.4 + k*1.0))
                if q > 0: txt(ctx, ln, 330, 740 + k*54, 32, B['ice'] if k == 0 else B['steel'], a*q, 'bold')
        else:
            marks = [(.02, '2001', 'FIRST|FLIGHT', 1.), (.22, '2011', 'IOC', 1.), (.38, 'DEC 2013', 'IOC-II', 1.),
                     (.60, 'FEB 2019', 'FOC', 1.),
                     (.78, 'JUL 2016', 'No. 45 SQN|FLYING DAGGERS', ease(cue(t, 'Number 45 Squadron', .25, .7))),
                     (.96, '2020', 'No. 18 SQN|FLYING BULLETS', ease(cue(t, 'Number 18, the Flying Bullets', .25, .7)))]
            timeline(ctx, 220, 1660, 420, marks, a)
            q = cue(t, 'Forty aircraft were ordered', .25, .6)
            if q > 0:
                card(ctx, 300, 630, 1320, 220, a*ease(q), 'THE FIRST BATCH · 40 AIRCRAFT', B['cyan'], ease(q))
                rows = [('32', 'FIGHTERS DELIVERED'), ('6 of 8', 'TRAINERS DELIVERED')]
                for k, (n, lab) in enumerate(rows):
                    qq = ease(seg(q, .3 + k*.2, .9 + k*.2))
                    txt(ctx, n, 360 + k*620, 760, 58, B['ice'], a*qq, 'black')
                    txt(ctx, lab, 360 + k*620, 800, 22, B['steel'], a*qq, 'bold', mono=True)
                z = cue(t, 'still closing out two decades later', .2, .6)
                if z > 0: txt(ctx, 'AS REPORTED, SEPTEMBER 2025', 1560, 800, 20, B['dim'], a*ease(z), 'bold', 'r', mono=True)
    return scene(f)


# ================= 7. what the Mark 1A is =================
CALLOUTS = [('AESA RADAR', 'electronically scanned, no moving parts', (1230, 300), 'an AESA radar'),
            ('ELECTRONIC WARFARE SUITE', '', (1230, 430), 'an electronic warfare suite'),
            ('BEYOND-VISUAL-RANGE MISSILE', 'shoot at what it has not seen', (1230, 560), 'a beyond-visual-range missile'),
            ('AIR-TO-AIR REFUELLING', '', (1230, 690), 'air-to-air refuelling')]


def s_mk1a(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'LCA TEJAS MK1A · WHAT CHANGED', a, EP)
        if i == 0:
            jet(ctx, 620, 560, .82, 1., a)
            jet_engine(ctx, 620, 560, .82, a*.5, 1., True)
            for k, (lab, sub, (x, y), c) in enumerate(CALLOUTS):
                q = cue(t, c, .25, .55)
                if q <= 0: continue
                stroke_pts(ctx, [(760, 420 + k*90), (x - 20, y - 14)], ease(q), B['cyan'], a*.7, 2, glow=False)
                tagb(ctx, x, y - 14, lab, B['cyan'], a*ease(q), 26)
                if sub: txt(ctx, sub, x + 6, y + 36, 21, B['steel'], a*ease(seg(q, .3, 1)), 'bold', mono=True)
            txt(ctx, 'SAME AIRFRAME', 620, 900, 30, B['steel'], a*ease(seg(t, .4, 1.2)), 'bold', 'c', mono=True)
        elif i == 1:
            for k, (n, d, val, sub, col) in enumerate((
                    ('83 JETS', '3 FEB 2021', '₹48,000 CRORE', '73 fighters + 10 trainers', B['cyan']),
                    ('97 JETS', '25 SEP 2025', '₹62,370 CRORE', '68 single-seat + 29 twin-seat', B['cyan']))):
                q = ease(seg(t, .2 + k*.8, 1.1 + k*.8))
                if q <= 0: continue
                x = 150 + k*830
                card(ctx, x, 230, 760, 330, a*q, d, col, q)
                txt(ctx, n, x + 40, 360, 64, B['ice'], a*q, 'black')
                txt(ctx, val, x + 40, 430, 40, B['amber'], a*q, 'black')
                txt(ctx, sub, x + 40, 490, 23, B['steel'], a*q, 'bold', mono=True)
            q = ease(seg(t, 2.0, 3.0))
            if q > 0:
                txt(ctx, '180', 960, 740, 150, B['ice'], a*q, 'black', 'c', glow=1.)
                txt(ctx, 'AIRCRAFT ON ORDER  ·  ON PAPER, ABOUT TEN SQUADRONS', 960, 810, 28, B['cyan'], a*ease(seg(q, .4, 1)), 'bold', 'c', mono=True)
        else:
            card(ctx, 240, 240, 1440, 420, a, 'THE 97-JET CONTRACT · 25 SEPTEMBER 2025', B['cyan'], 1.)
            rows = [('OVER 64%', 'INDIGENOUS CONTENT', 'indigenous content above sixty-four per cent'),
                    ('UTTAM', "INDIA'S OWN AESA RADAR", "India's own Uttam AESA radar"),
                    ('SWAYAM RAKSHA KAVACH', 'IN PLACE OF IMPORTED SYSTEMS', 'in place of imported ones')]
            for k, (n, lab, c) in enumerate(rows):
                q = cue(t, c, .25, .6)
                if q <= 0: continue
                txt(ctx, n, 300, 390 + k*110, 46, B['ice'], a*ease(q), 'black')
                txt(ctx, lab, 300, 426 + k*110, 22, B['steel'], a*ease(seg(q, .3, 1)), 'bold', mono=True)
            q = cue(t, 'about ten squadrons', .25, .6)
            if q > 0:
                txt(ctx, '180 AIRCRAFT  ·  ABOUT TEN SQUADRONS', 960, 760, 44, B['amber'], a*ease(q), 'black', 'c', glow=.6)
    return scene(f)


# ================= 8. the engine India buys =================
def s_f404(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'THE FOURTH PROBLEM · GE F404', a, EP)
        icon_turbine(ctx, 430, 470, 2.6, B['amber'] if i else B['ice'], a, fin(t, .2, 1.4), t, True, 0.)
        txt(ctx, 'GE F404', 430, 680, 44, B['ice'], a*ease(seg(t, .6, 1.4)), 'black', 'c')
        txt(ctx, 'AN AMERICAN ENGINE', 430, 722, 22, B['steel'], a*ease(seg(t, .8, 1.6)), 'bold', 'c', mono=True)
        if i == 0:
            q = cue(t, 'HAL ordered ninety-nine', .25, .6)
            if q > 0:
                card(ctx, 830, 230, 900, 230, a*ease(q), 'ORDERED · JANUARY 2021', B['cyan'], ease(q))
                txt(ctx, '99 ENGINES', 870, 350, 56, B['ice'], a*ease(seg(q, .2, 1)), 'black')
                txt(ctx, 'ABOUT $716 MILLION  ·  DUE FROM APRIL 2023  ·  16 A YEAR', 870, 410, 23, B['steel'],
                    a*ease(seg(q, .4, 1)), 'bold', mono=True)
            q2 = cue(t, 'The first arrived in March 2025', .25, .6)
            if q2 > 0: tagb(ctx, 830, 540, 'FIRST ENGINE: MARCH 2025 — TWO YEARS LATE', B['alert'], a*ease(q2), 28)
            q3 = cue(t, 'four had been delivered', .2, .6)
            if q3 > 0:
                card(ctx, 830, 600, 900, 240, a*ease(q3), 'DELIVERED BY OCTOBER 2025', B['alert'], ease(q3))
                txt(ctx, '4', 980, 790, 130, B['alert'], a*ease(seg(q3, .2, 1)), 'black', 'c', glow=1.)
                txt(ctx, 'AGAINST A PLAN', 1150, 740, 26, B['steel'], a*ease(seg(q3, .4, 1)), 'bold', mono=True)
                txt(ctx, 'OF 16 A YEAR', 1150, 776, 26, B['steel'], a*ease(seg(q3, .5, 1)), 'bold', mono=True)
                txt(ctx, 'THE TRIBUNE, AS REPORTED', 1150, 814, 20, B['dim'], a*ease(seg(q3, .6, 1)), 'bold', mono=True)
        else:
            card(ctx, 830, 240, 900, 300, a, 'WHAT IT IS NOT', B['steel'], 1.)
            for k, ln in enumerate(('not the airframe', 'not the software', "not HAL's factory floor")):
                q = ease(seg(t, .4 + k*.6, 1.2 + k*.6))
                if q > 0:
                    txt(ctx, ln, 880, 370 + k*58, 36, B['steel'], a*q, 'bold')
                    stroke_pts(ctx, [(872, 358 + k*58), (872 + tw(ctx, ln, 36, 'bold') + 16, 358 + k*58)],
                               ease(seg(q, .4, 1)), B['alert'], a*q*.8, 3, glow=False)
            q2 = cue(t, 'a hundred and thirteen more', .25, .6)
            if q2 > 0:
                card(ctx, 830, 570, 900, 180, a*ease(q2), 'NOVEMBER 2025', B['cyan'], ease(q2))
                txt(ctx, '113 MORE ENGINES', 870, 680, 46, B['ice'], a*ease(seg(q2, .2, 1)), 'black')
                txt(ctx, 'FOR DELIVERY BETWEEN 2027 AND 2032', 870, 722, 23, B['steel'], a*ease(seg(q2, .4, 1)), 'bold', mono=True)
            q3 = cue(t, 'why does India not simply build its own', .25, .6)
            if q3 > 0: txt(ctx, 'SO WHY NOT BUILD OUR OWN?', 960, 880, 48, B['amber'], a*ease(q3), 'black', 'c', glow=.8)
    return scene(f)


# ================= 9. Kaveri, and why engines are hard =================
def s_kav(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'KAVERI · GTRE, DRDO', a, EP)
        if i == 0:
            card(ctx, 240, 250, 1440, 330, a, 'KAVERI', B['cyan'], fin(t, .1, .8))
            for k, (n, lab, c) in enumerate((('~72 kN', 'THRUST REACHED, AS REPORTED', 'about seventy-two kilonewtons'),
                                             ('83–85 kN', 'THE AIRCRAFT NEEDED', 'the aircraft needed'),
                                             ('2008', 'DELINKED FROM THE FIGHTER PROGRAMME', 'delinked from the fighter programme'))):
                q = cue(t, c, .25, .6)
                if q <= 0: continue
                x = 300 + k*470
                txt(ctx, n, x, 400, 58, B['ice'] if k != 2 else B['alert'], a*ease(q), 'black')
                for j, ln in enumerate(wrap(ctx, lab, 21, 400, 'bold', True)):
                    txt(ctx, ln, x, 446 + j*28, 21, B['steel'], a*ease(seg(q, .3, 1)), 'bold', mono=True)
            q = cue(t, 'national failure', .25, .6)
            if q > 0: txt(ctx, 'USUALLY TOLD AS A NATIONAL FAILURE. IT IS HARDER THAN THAT.',
                          960, 700, 34, B['amber'], a*ease(q), 'black', 'c', glow=.5)
        elif i == 1:
            stages = [ease(cue(t, 'a compressor squeezes it', .25, .9)),
                      ease(cue(t, 'fuel burns', .25, .9)),
                      ease(cue(t, 'the gas leaves through a turbine', .25, .9))]
            turbine_cut(ctx, 960, 470, 1.25, a, stages, hot=t if stages[1] > .5 else 0.)
            q = cue(t, 'hotter than the temperature at which the turbine blades would melt', .3, .7)
            if q > 0:
                tagb(ctx, 960, 740, 'GAS HOTTER THAN THE BLADES’ OWN MELTING POINT', B['alert'], a*ease(q), 30, align='c')
        else:
            icon_turbine(ctx, 430, 480, 3.2, B['cyan'], a, 1., t, True, 0.)
            card(ctx, 830, 250, 900, 460, a, 'WHY THE BLADES SURVIVE', B['cyan'], fin(t, .1, .8))
            rows = [('GROWN AS ONE CRYSTAL', 'of nickel alloy', 'a single crystal of nickel alloy'),
                    ('COATED IN CERAMIC', '', 'coated in ceramic'),
                    ('COOLED FROM INSIDE', 'air bled through tiny holes', 'tiny holes inside it'),
                    ('THOUSANDS OF HOURS', 'without failing once', 'without failing once')]
            for k, (n, sub, c) in enumerate(rows):
                q = cue(t, c, .25, .55)
                if q <= 0: continue
                txt(ctx, n, 880, 370 + k*98, 34, B['ice'], a*ease(q), 'black')
                if sub: txt(ctx, sub, 880, 404 + k*98, 21, B['steel'], a*ease(seg(q, .3, 1)), 'bold', mono=True)
    return scene(f)


# ================= 10. and yet =================
def s_kde(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'KAVERI DERIVATIVE ENGINE · REPORTED 1 OCTOBER 2026', a, EP)
        if i == 0:
            card(ctx, 240, 250, 1440, 330, a, 'WHAT PROVING AN ENGINE NEEDS', B['steel'], fin(t, .1, .8))
            for k, lab in enumerate(('HIGH-ALTITUDE TEST BEDS', 'A FLYING TESTBED', 'A CERTIFICATION CHAIN')):
                q = ease(seg(t, .4 + k*.7, 1.2 + k*.7))
                if q > 0: tagb(ctx, 320 + k*470, 420, lab, B['steel'], a*q, 24)
            q = cue(t, 'India had almost none of that', .25, .6)
            if q > 0: txt(ctx, 'INDIA HAD ALMOST NONE OF IT WHEN KAVERI BEGAN', 960, 680, 36, B['alert'], a*ease(q), 'black', 'c')
            y = cue(t, 'And yet', .2, .5)
            if y > 0: txt(ctx, 'AND YET.', 960, 800, 64, B['amber'], a*ease(y), 'black', 'c', glow=1.)
        elif i == 1:
            testbed(ctx, 820, 460, .95, a, fin(t, .2, 1.8), 1, t)
            txt(ctx, 'MODIFIED Il-76 FLYING TESTBED', 820, 680, 26, B['steel'], a*ease(seg(t, 1.0, 1.8)), 'bold', 'c', mono=True)
            txt(ctx, 'TESTED IN RUSSIA  ·  ON THE GROUND, THEN IN THE AIR', 820, 718, 22, B['dim'], a*ease(seg(t, 1.2, 2.0)), 'bold', 'c', mono=True)
            q = cue(t, 'Peak dry thrust', .25, .6)
            if q > 0:
                card(ctx, 1350, 300, 480, 300, a*ease(q), 'PEAK DRY THRUST', B['amber'], ease(q))
                txt(ctx, '48.5', 1590, 440, 110, B['amber'], a*ease(seg(q, .2, 1)), 'black', 'c', glow=1.)
                txt(ctx, 'kN', 1590, 490, 34, B['ice'], a*ease(seg(q, .3, 1)), 'black', 'c')
                txt(ctx, 'AGAINST A TARGET OF 46', 1590, 550, 22, B['steel'], a*ease(seg(q, .5, 1)), 'bold', 'c', mono=True)
            g = cue(t, 'Ghatak unmanned combat aircraft', .25, .6)
            if g > 0: tagb(ctx, 1590, 660, 'FOR THE GHATAK UCAV', B['cyan'], a*ease(g), 26, align='c')
        else:
            q = cue(t, 'That is not an engine for Tejas', .2, .6)
            txt(ctx, 'NOT AN ENGINE FOR TEJAS', 960, 330, 52, B['steel'], a*ease(fin(t, .2, .8)), 'black', 'c')
            q2 = cue(t, 'flew and beat its own target', .25, .7)
            if q2 > 0:
                txt(ctx, 'AN INDIAN-DESIGNED MILITARY TURBOFAN', 960, 470, 48, B['ice'], a*ease(q2), 'black', 'c', glow=.5)
                txt(ctx, 'THAT FLEW, AND BEAT ITS OWN TARGET', 960, 540, 48, B['amber'], a*ease(seg(q2, .3, 1)), 'black', 'c', glow=.8)
            q3 = cue(t, 'thirty years', .25, .6)
            if q3 > 0: txt(ctx, 'A DIFFERENT SENTENCE FROM THE ONE INDIA HAS BEEN WRITING FOR THIRTY YEARS',
                           960, 680, 28, B['steel'], a*ease(q3), 'bold', 'c', mono=True)
            icon_turbine(ctx, 960, 820, 1.6, B['amber'], a*ease(fin(t, .3, 1.)), 1., t, True, .6)
    return scene(f)


# ================= 11. three tracks =================
TRACKS = [('ONE · LICENCE-BUILD', ['GE F414 for Tejas Mark 2', 'Made in India by HAL', 'Reported 80% technology|transfer'],
           'The GE F414'),
          ('TWO · CO-DEVELOP', ['120 kN or more, for AMCA', 'Rolls-Royce and Safran left', 'No partner announced'],
           'For the fifth-generation AMCA'),
          ('THREE · BUILD OUR OWN', ['From the bottom up', 'Starting with a drone|engine that works', ''],
           'build our own')]


def s_trk(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'THREE TRACKS AT ONCE', a, EP)
        for k, (title, lines, c) in enumerate(TRACKS):
            if i == 0 and k > 0: continue
            if i == 1 and k > 1: continue
            p = ease(cue(t, c, .3, 1.0)) if k == i else 1.
            if k < i: p = 1.
            if p <= 0: continue
            col = [B['cyan'], B['cyan'], B['amber']][k]
            track(ctx, 400 + k*560, 300, 760, title, [l for l in lines if l], col, a, p)
        if i == 2:
            q = cue(t, 'Watch which of the three the government signs', .25, .6)
            if q > 0:
                txt(ctx, 'OWN ONE IN THE 2030s, OR RENT ONE FOR ANOTHER GENERATION', 960, 870, 34,
                    B['ice'], a*ease(q), 'black', 'c', glow=.5)
    return scene(f)


# ================= 12. squadron arithmetic =================
def s_sqn(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'THE ARITHMETIC · SQUADRON STRENGTH', a, EP)
        sqnbars(ctx, 260, 330, 1400, a, fin(t, .2, 2.2) if i == 0 else 1.)
        if i == 0:
            q = cue(t, 'Arithmetic', .2, .5)
            if q > 0: txt(ctx, 'WHY A FACTORY SCHEDULE BECOMES A DEFENCE PROBLEM', 960, 250, 30, B['steel'], a*ease(q), 'bold', 'c', mono=True)
            m = cue(t, 'has now left service entirely', .25, .6)
            if m > 0: tagb(ctx, 960, 640, 'THE MiG-21 HAS LEFT SERVICE ENTIRELY', B['alert'], a*ease(m), 28, align='c')
        else:
            q = cue(t, 'the gap between them is the squadron shortfall', .25, .6)
            if q > 0: txt(ctx, 'THE OLD WENT FIRST. THE NEW ARE LATE. THE GAP IS THE SHORTFALL.',
                          960, 660, 34, B['ice'], a*ease(q), 'black', 'c', glow=.4)
            q2 = cue(t, 'the cost of starting late', .25, .6)
            if q2 > 0:
                card(ctx, 420, 720, 1080, 150, a*ease(q2), None, B['amber'], ease(q2))
                txt(ctx, 'NOT AN ARGUMENT AGAINST BUILDING YOUR OWN —', 960, 785, 30, B['steel'], a*ease(q2), 'bold', 'c')
                txt(ctx, 'AN ARGUMENT ABOUT THE COST OF STARTING LATE', 960, 830, 30, B['amber'], a*ease(seg(q2, .3, 1)), 'black', 'c')
    return scene(f)


# ================= 13. 21 November 2025 — text only, no aircraft =================
def s_dub(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .4)
        hud(ctx, t, '', a, EP)
        p = fin(t, .3, 1.2) if i == 0 else 1.
        card(ctx, 420, 300, 1080, 420, a*p, None, B['steel'], p)
        txt(ctx, 'DUBAI AIRSHOW', 960, 400, 34, B['steel'], a*p, 'bold', 'c', mono=True)
        txt(ctx, '21 NOVEMBER 2025', 960, 470, 56, B['ice'], a*ease(seg(t, .5, 1.3)) if i == 0 else a, 'black', 'c')
        q = ease(seg(t, 1.2, 2.2)) if i == 0 else 1.
        txt(ctx, 'WING COMMANDER NAMANSH SYAL', 960, 560, 40, B['ice'], a*q, 'black', 'c')
        txt(ctx, 'COURT OF INQUIRY ORDERED', 960, 620, 26, B['steel'], a*q, 'bold', 'c', mono=True)
        if i == 1:
            z = cue(t, 'the investigation is still under way', .25, .6)
            if z > 0: tagb(ctx, 960, 790, 'AS OF 19 NOV 2026 · NOT REPORTED PUBLICLY', B['steel'], a*ease(z), 26, align='c')
            z2 = cue(t, 'anyone who tells you otherwise is guessing', .25, .6)
            if z2 > 0: txt(ctx, 'NO CAUSE IS KNOWN. ANYONE WHO TELLS YOU OTHERWISE IS GUESSING.',
                           960, 880, 28, B['dim'], a*ease(z2), 'bold', 'c', mono=True)
    return scene(f)


# ================= 14. where people disagree =================
def s_deb(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'WHERE INFORMED PEOPLE DISAGREE', a, EP)
        sides = [('THE CASE FOR PATIENCE', [
                    'Every country that builds fighters took decades',
                    'India owns design authority: airframe,',
                    'flight control laws, increasingly the radar',
                    'It compounds into Mark 2 and AMCA'], B['cyan']),
                 ('THE CASE FOR URGENCY', [
                    'Squadrons are falling now',
                    'The threat does not wait for a learning curve',
                    'Signed 2021, nothing delivered by late 2026',
                    'An American engine in a jet built to end dependence'], B['amber'])]
        for k, (title, lines, col) in enumerate(sides):
            if i == 0 and k == 1: continue
            x = 120 + k*900
            p = 1. if (i > 0 or k == 0) else 1.
            card(ctx, x, 230, 840, 520, a, title, col, p)
            for j, ln in enumerate(lines):
                if i == 0 and k == 0: q = ease(seg(t, .5 + j*.9, 1.4 + j*.9))
                elif i == 1 and k == 1: q = ease(seg(t, .3 + j*.9, 1.2 + j*.9))
                else: q = 1.
                if q <= 0: continue
                for m, l2 in enumerate(wrap(ctx, ln, 28, 760, 'bold')):
                    txt(ctx, l2, x + 40, 350 + j*96 + m*34, 28, B['ice'], a*q, 'bold')
        if i == 2:
            q = cue(t, 'nobody argues the aircraft is bad', .25, .6)
            if q > 0:
                fill(ctx, lambda: rrect(ctx, 260, 790, 1400, 130, 10), B['deep'], .92*a*ease(q))
                stroke_pts(ctx, rect_pts(260, 790, 1400, 130), ease(q), B['ice'], a, 2.5)
                txt(ctx, 'NOBODY ARGUES THE AIRCRAFT IS BAD.', 960, 850, 38, B['ice'], a*ease(q), 'black', 'c')
                txt(ctx, 'THEY ARE ARGUING ABOUT TIME.', 960, 898, 34, B['amber'], a*ease(seg(q, .4, 1)), 'black', 'c')
    return scene(f)


# ================= 15. where it stands =================
ROWS = [('MARK 1', '40 ordered · 32 fighters and most trainers delivered', 'TWO SQUADRONS FLYING', 'cyan', 'forty ordered'),
        ('MARK 1A', '180 on order across two contracts · airframes built', 'DELIVERIES NOT BEGUN', 'alert', 'deliveries not begun'),
        ('ENGINES', '4 delivered by Oct 2025 against 16 a year planned', '113 MORE TO 2032', 'alert', 'four delivered by October 2025'),
        ('PRODUCTION', 'A third line at Nashik', '24 AIRCRAFT A YEAR', 'cyan', 'third assembly line at Nashik'),
        ('MARK 2', 'Prototypes in assembly', 'FIRST FLIGHT TARGETED 2027', 'cyan', 'prototypes in assembly'),
        ('THE ENGINE', "Kaveri's dry derivative flew and beat its target", 'AMCA PARTNER NOT ANNOUNCED', 'amber',
         "Kaveri's dry derivative has flown")]


def s_st(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'WHERE IT STANDS · 19 NOVEMBER 2026', a, EP)
        show = [(0, 2), (2, 4), (4, 6)][i]
        for k in range(show[0], show[1]):
            name, note, status, col, c = ROWS[k]
            q = ease(cue(t, c, .3, .8))
            if q <= 0: continue
            statusrow(ctx, 220, 260 + (k - show[0])*300, 1480, name, note, status, B[col], a*q, q)
    return scene(f)


# ================= 16. in three words =================
def s_three(ctx, t, D):
    bg(ctx); a = outro(t, D, .5)
    hud(ctx, t, 'IN THREE WORDS', a, EP)
    words = [('DESIGN', 'India can do this'), ('BUILD', 'India can do this'), ('POWER', 'half filled in')]
    for k, (w_, sub) in enumerate(words):
        q = ease(cue(t, ['Design.', 'Build.', 'Power.'][k], .25, .5))
        if q <= 0: continue
        y = 300 + k*190
        col = B['amber'] if k == 2 else B['cyan']
        if k < 2:
            txt(ctx, w_, 960, y, 110, col, a*q, 'black', 'c', glow=1.)
        else:
            # the third word fills only part of the way
            fillp = ease(cue(t, 'It is half filled in', .2, 1.0))
            txt(ctx, w_, 960, y, 110, B['dim'], a*q, 'black', 'c')
            ctx.save()
            wq = tw(ctx, w_, 110, 'black')
            ctx.rectangle(960 - wq/2, y - 96, wq*(.5*fillp), 120); ctx.clip()
            txt(ctx, w_, 960, y, 110, B['amber'], a*q, 'black', 'c', glow=1.2)
            ctx.restore()
        txt(ctx, sub, 960, y + 46, 24, B['steel'], a*ease(seg(q, .4, 1)), 'bold', 'c', mono=True)
    e = cue(t, 'stopped being an empty outline', .25, .6)
    if e > 0:
        txt(ctx, 'AFTER FORTY YEARS, NO LONGER AN EMPTY OUTLINE', 960, 900, 30, B['ice'], a*ease(e), 'bold', 'c', mono=True)
s_three = scene(s_three)


# ================= 17. the wall, next, subscribe =================
def s_end(ctx, t, D):
    bg(ctx); a = outro(t, D, .5)
    hud(ctx, t, 'THE BLUEPRINT WALL', a, EP)
    wall(ctx, t, a, drop=seg(t, .4, 1.6))
    tn = Ts('Next on')
    nq = seg(t, tn, tn + .6) if tn < 900 else 0
    if nq > 0:
        q = ease(nq)
        fill(ctx, lambda: ctx.rectangle(0, 700, W*eoc(nq), 90), B['deep'], .95*a*q)
        rgba(ctx, B['cyan'], a*q); ctx.rectangle(0, 700, W*eoc(nq), 3); ctx.fill()
        txt(ctx, 'NEXT  ·  INS VIKRANT, AND WHAT BUILDING A CARRIER AT HOME TAKES', 80, 758, 30, B['ice'], a*q, 'bold', mono=True)
    subscribe_card(ctx, t, Ts('subscribe'), a, x=1540, y=900)
s_end = scene(s_end)


# ================= beats =================
SC = {}
FACT = {'cold': s_cold, 'four': s_four, 'why': s_why, 'emb': s_emb, 'clr': s_clr, 'mk1a': s_mk1a,
        'f404': s_f404, 'kav': s_kav, 'kde': s_kde, 'trk': s_trk, 'sqn': s_sqn, 'dub': s_dub,
        'deb': s_deb, 'st': s_st}
STEMS = list(FACT) + ['qs', 'three', 'end']


def stem_of(k):
    """beat ids are <stem><n>, and some stems contain digits (f404), so match the
    longest known stem rather than stripping trailing digits"""
    m = [s for s in STEMS if k.startswith(s) and k[len(s):].isdigit()]
    assert m, k
    return max(m, key=len)


for stem, fn in FACT.items():
    ks = [k for k, _ in EN if stem_of(k) == stem]
    for i, k in enumerate(ks): SC[k] = fn(i)
SC['qs1'] = s_qs
SC['three1'] = s_three
SC['end1'] = s_end

BEATS = [(k, n, SC[k]) for k, n in EN]

GROUPS = {k: stem_of(k) for k, _ in EN}

KEYS = {
 'cold2': [('the number handed over is zero', 'ZERO', 'alert')],
 'why1': [('five hundred and sixty crore rupees', '₹560 CRORE', 'amber')],
 'emb1': [('May 1998', 'MAY 1998', 'alert')],
 'emb3': [('fourth of January 2001', '4 JAN 2001', 'amber')],
 'mk1a2': [('a hundred and eighty aircraft', '180 AIRCRAFT', 'amber')],
 'f4041': [('four had been delivered', 'FOUR ENGINES', 'alert')],
 'kav1': [('about seventy-two kilonewtons', '72 kN', 'steel')],
 'kde2': [('forty-eight point five kilonewtons', '48.5 kN', 'amber')],
 'sqn1': [('thirty-one', '31 SQUADRONS', 'alert')],
}
ANNOT = {
 'four2': [('India solving three of them', 'circle', 960, 430, 1500, 460)],
 'kde3': [('beat its own target', 'underline', 700, 575, 520, 0)],
}

_order = [k for k, _ in EN]
FX = [('whoosh', k, -.25, .22) for i, k in enumerate(_order) if i and GROUPS[k] != GROUPS[_order[i-1]]]
FX += [('beep', k, ph, .14) for k, items in KEYS.items() for ph, _, _ in items]
FX += [('tick', 'cold1', .15, .12),
       ('glitch', 'cold2', 'the number handed over is zero', .3),
       ('riser', 'cold2', 'What most of them do not have is an engine', .25),
       ('ping', 'four1', 'Four: power', .3),
       ('stamp', 'why1', 'In August 1983 the government sanctioned', .3),
       ('glitch', 'emb1', 'Their engineers went home', .3),
       ('riser', 'emb3', 'The aircraft flew on the fourth of January 2001', .2),
       ('boom', 'emb3', 'The aircraft flew on the fourth of January 2001', .5),
       ('stamp', 'mk1a2', 'twenty-fifth of September 2025', .3),
       ('glitch', 'f4041', 'four had been delivered', .35),
       ('boom', 'kav2', 'hotter than the temperature at which the turbine blades would melt', .3),
       ('riser', 'kde2', 'Peak dry thrust', .2),
       ('ding', 'kde2', 'against a target of forty-six', .25),
       ('ping', 'trk1', 'three tracks', .25),
       ('riser', 'three1', 'Design.', .12), ('ding', 'three1', 'Design.', .22),
       ('ding', 'three1', 'Build.', .22), ('ding', 'three1', 'Power.', .22),
       ('stamp', 'end1', .5, .35), ('ding', 'end1', 'subscribe', .2)]
