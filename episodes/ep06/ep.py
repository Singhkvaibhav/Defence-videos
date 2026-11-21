"""India's Defence, Decoded — Episode 6: The Ship That Carries Its Own Airfield.

No maps: the reach beat is two abstract circles, with no coastline, landmass or
boundary. No flags, logos or likenesses. 1971 and 1965 appear as text only.
Commentary from ThePrint is credited on screen wherever it is used.
"""
import os, sys, math, cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 822.0   # measured: 778.9 s of narration (longer of EN/HI per beat) + ~1.1 s pause each
core.TOTAL = TOTAL
from engine.core import W, H, seg, ease, eoc, eob, lerp, T
from engine.bp import (B, rgba, rrect, bg, txt, tw, wrap, stroke_pts, rect_pts, fill, glow_dot,
                       bez, hud, card, tagb, outro, camera, scene, subscribe_card)
from engine.shield import statusrow
from engine.jet import timeline
from engine.ship import (carrier, deck_plan, skijump, catapult, bell, icon_hull, icon_deck, icon_plane,
                         problem3, steel_plate, reach, fleet, wall6)
from text import EN, HI as _HI

EP = 6
CODE = 'Def06'
TITLE = 'The_Ship_That_Carries_Its_Own_Airfield'
NAME = 'INS Vikrant: What It Takes to Build an Aircraft Carrier at Home'
POST = 'engine.bp'
BED = 'pulse'
VOICE_EN = {'length': 0.98, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
VOICE_HI = {'length': 0.86, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
CRF, PRESET = 17, 'medium'
EXTRA = {'cold1': .9, 'cold2': .6, 'three1': 1.4, 'end1': 2.5}
HI = _HI


def Ts(x):
    try: return T(x)
    except ValueError: return 999.


def cue(t, s, lead=.2, dur=.45):
    c = Ts(s)
    return 0. if c >= 900 else seg(t, c - lead, c - lead + dur)


def fin(t, t0=.1, d=.6): return ease(seg(t, t0, t0 + d))


# ================= 1. cold open: the bell =================
def s_cold(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'INS VIKRANT · COMMISSIONED 2 SEPTEMBER 2022', a, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.05), (0, -10))
        bell(ctx, 700, 470, 1.25, a, fin(t, .2, 1.8) if i == 0 else 1., t)
        if i == 0:
            q = cue(t, 'The bell was made in 1961', .25, .6)
            if q > 0:
                txt(ctx, '1961', 700, 760, 72, B['amber'], a*ease(q), 'black', 'c', glow=.8)
            q2 = cue(t, 'broken up for scrap in 1997', .25, .6)
            if q2 > 0:
                card(ctx, 1200, 300, 600, 220, a*ease(q2), 'THE FIRST INS VIKRANT', B['steel'], ease(q2))
                txt(ctx, 'BOUGHT FROM BRITAIN', 1240, 400, 30, B['ice'], a*ease(seg(q2, .2, 1)), 'black')
                txt(ctx, '36 YEARS IN SERVICE  ·  SCRAPPED 1997', 1240, 452, 22, B['steel'],
                    a*ease(seg(q2, .4, 1)), 'bold', mono=True)
        else:
            card(ctx, 1200, 260, 600, 170, a, '22 MARCH 2023', B['cyan'], 1.)
            txt(ctx, 'THE BELL RETURNS', 1240, 360, 36, B['ice'], a, 'black')
            txt(ctx, 'VICE ADMIRAL S N GHORMADE', 1240, 404, 21, B['steel'], a, 'bold', mono=True)
            q = cue(t, 'The first Vikrant was bought', .25, .6)
            if q > 0:
                txt(ctx, 'THE FIRST ONE WAS BOUGHT.', 1500, 560, 38, B['steel'], a*ease(q), 'black', 'c')
            q2 = cue(t, 'This one India built', .2, .6)
            if q2 > 0:
                txt(ctx, 'THIS ONE INDIA BUILT.', 1500, 625, 44, B['amber'], a*ease(q2), 'black', 'c', glow=.7)
        ctx.restore()
    return scene(f)


# ================= 2. the anchor: three problems =================
PROBS = [('HULL', 'ONE', icon_hull, 'One: the hull'),
         ('DECK', 'TWO', icon_deck, 'Two: the deck'),
         ('WING', 'THREE', icon_plane, 'Three: the wing')]


def s_anchor(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'THREE PROBLEMS WEARING ONE NAME', a, EP)
        for k, (lab, n, ic, c) in enumerate(PROBS):
            p = cue(t, c, .3, .9) if i == 0 else 1.
            if p <= 0: continue
            col = B['amber'] if k == 2 else B['cyan']
            problem3(ctx, 390 + k*565, 470, lab, n, ic, col, a, p)
        if i == 1:
            q = cue(t, 'two out of three', .25, .6)
            if q > 0:
                txt(ctx, "INDIA'S SCORE: TWO OUT OF THREE", 960, 790, 46, B['ice'], a*ease(q), 'black', 'c', glow=.6)
                stroke_pts(ctx, [(520, 818), (1400, 818)], ease(seg(q, .3, 1)), B['cyan'], a, 3, glow=False)
    return scene(f)


# ================= 3. three questions, borrowed =================
QS = ['DOES INDIA NEED CARRIERS AT ALL?', 'IF SO, WHAT KIND — AND HOW MANY?', 'WHAT FLIES OFF THEM, AND FROM WHERE?']


def s_qs(ctx, t, D):
    bg(ctx); a = outro(t, D, .35)
    hud(ctx, t, 'THREE QUESTIONS', a, EP)
    for k, q_ in enumerate(QS):
        p = ease(seg(t, 2.0 + k*1.5, 2.9 + k*1.5))
        if p <= 0: continue
        y = 250 + k*150
        x = lerp(-500, 260, eob(p, 1.6))
        ctx.save(); ctx.rectangle(x, y, 1400, 118); ctx.clip()
        card(ctx, x, y, 1400, 118, a*p, None, B['cyan'], 1.)
        txt(ctx, f'{k+1}', x + 44, y + 82, 54, B['cyan'], a*p, 'black')
        txt(ctx, q_, x + 126, y + 78, 40, B['ice'], a*p, 'black')
        ctx.restore()
    c = cue(t, 'They are the right three questions', .3, .8)
    if c > 0:
        txt(ctx, 'SHEKHAR GUPTA  ·  THEPRINT  ·  3 SEPTEMBER 2022', 960, 790, 26,
            B['steel'], a*ease(c), 'bold', 'c', mono=True)
        txt(ctx, 'THE QUESTIONS ARE HIS. THE EPISODE TRIES TO ANSWER THEM.', 960, 836, 24,
            B['dim'], a*ease(seg(c, .3, 1)), 'bold', 'c', mono=True)
s_qs = scene(s_qs)


# ================= 4. the identity card =================
SPECS = [('262 m', 'LENGTH', 'Two hundred and sixty-two metres long'),
         ('62 m', 'BEAM', 'sixty-two metres across'),
         ('~43,000 t', 'FULL LOAD', 'forty-three thousand tonnes'),
         ('28 kn', 'TOP SPEED', 'twenty-eight knots'),
         ('7,500 nm', 'ENDURANCE', 'seven and a half thousand nautical miles'),
         ('~2,200', 'COMPARTMENTS', 'two thousand two hundred compartments'),
         ('~1,600', 'CREW', 'crew of about sixteen hundred'),
         ('30', 'AIRCRAFT', 'up to thirty aircraft')]


def s_id(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'IDENTITY CARD · LARGEST WARSHIP BUILT IN INDIA', a, EP)
        carrier(ctx, 930, 330, .84, fin(t, .15, 2.4) if i == 0 else 1., a)
        if i == 0:
            q = cue(t, 'commissioned at Kochi', .25, .6)
            if q > 0: tagb(ctx, 960, 560, 'COMMISSIONED AT KOCHI · 2 SEPTEMBER 2022', B['cyan'], a*ease(q), 30, align='c')
        for k, (n, lab, c) in enumerate(SPECS):
            q = cue(t, c, .22, .5)
            if q <= 0: continue
            x = 180 + (k % 4)*450
            y = 650 + (k//4)*130
            txt(ctx, n, x, y, 46, B['ice'], a*ease(q), 'black')
            txt(ctx, lab, x, y + 34, 21, B['steel'], a*ease(seg(q, .3, 1)), 'bold', mono=True)
        if i == 2:
            q = cue(t, 'Warship Design Bureau', .25, .6)
            if q > 0:
                for k, (nm, rl) in enumerate((('WARSHIP DESIGN BUREAU', 'designed it'),
                                              ('COCHIN SHIPYARD', 'built it'), ('~76%', 'indigenous content'))):
                    qq = ease(seg(q, k*.22, .6 + k*.22))
                    if qq <= 0: continue
                    tagb(ctx, 260 + k*560, 640, nm, B['cyan'], a*qq, 26)
                    txt(ctx, rl, 266 + k*560, 690, 22, B['steel'], a*qq, 'bold', mono=True)
    return scene(f)


# ================= 5. the steel =================
def s_steel(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'WARSHIP-GRADE STEEL · DRDO · SAIL · INDIAN NAVY', a, EP)
        shock = t if i == 0 else 0.
        stamped = ease(cue(t, 'self-sufficient', .3, 1.0)) if i == 1 else (1. if i == 2 else 0.)
        steel_plate(ctx, 640, 470, 1.15, a, fin(t, .15, 1.2) if i == 0 else 1., stamped, shock)
        if i == 0:
            q = cue(t, 'without cracking', .25, .6)
            if q > 0:
                card(ctx, 1200, 280, 600, 230, a*ease(q), 'WHAT A WARSHIP HULL MUST DO', B['cyan'], ease(q))
                for k, ln in enumerate(('Take shock through water', 'without cracking', 'and still be weldable in bulk')):
                    qq = ease(seg(q, .2 + k*.2, .7 + k*.2))
                    txt(ctx, ln, 1240, 370 + k*48, 28, B['ice'], a*qq, 'bold')
        elif i == 1:
            qa = cue(t, 'India did not make it', .25, .6)
            if qa > 0: tagb(ctx, 1150, 250, 'IN THE 2000s, INDIA DID NOT MAKE THIS GRADE', B['alert'], a*ease(qa), 26)
            q = cue(t, 'self-sufficient', .3, .7)
            if q > 0:
                txt(ctx, '"SELF-SUFFICIENT"', 1420, 430, 48, B['amber'], a*ease(q), 'black', 'c', glow=.8)
                txt(ctx, 'PRESS INFORMATION BUREAU', 1420, 480, 22, B['steel'], a*ease(seg(q, .3, 1)), 'bold', 'c', mono=True)
        else:
            q = cue(t, 'Notice the sequence', .25, .6)
            if q > 0:
                card(ctx, 1180, 300, 640, 290, a*ease(q), 'THE SEQUENCE', B['amber'], ease(q))
                for k, ln in enumerate(('First, the ability', 'to make the metal.', 'Then the ship.')):
                    qq = ease(seg(q, .2 + k*.25, .8 + k*.25))
                    txt(ctx, ln, 1220, 400 + k*62, 38, B['ice'] if k < 2 else B['amber'], a*qq, 'black')
    return scene(f)


# ================= 6. seventeen years =================
MARKS = [(.00, 'APR 2005', 'STEEL CUT', 'Ceremonial steel cutting in April 2005'),
         (.19, 'FEB 2009', 'KEEL LAID', 'Keel laid in February 2009'),
         (.38, 'AUG 2013', 'LAUNCHED', 'Launched in August 2013'),
         (.58, 'NOV 2020', 'BASIN TRIALS', 'Basin trials'),
         (.72, 'AUG 2021', 'SEA TRIALS', 'Sea trials from August 2021'),
         (.86, '28 JUL 2022', 'DELIVERED', 'Delivered on the twenty-eighth of July 2022'),
         (1.0, '2 SEP 2022', 'COMMISSIONED', 'commissioned on the second of September')]


def s_build(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'SEVENTEEN YEARS, FIRST CUT TO COMMISSIONING', a, EP)
        marks = []
        for xf, yr, lab, c in MARKS:
            q = ease(cue(t, c, .25, .6)) if i == 0 else 1.
            marks.append((xf, yr, lab, q))
        timeline(ctx, 230, 1690, 430, marks, a)
        if i == 1:
            q = cue(t, 'Seventeen years', .25, .6)
            if q > 0:
                txt(ctx, '17 YEARS', 960, 670, 96, B['amber'], a*ease(q), 'black', 'c', glow=1.)
            q2 = cue(t, 'some of it was avoidable', .25, .6)
            if q2 > 0:
                txt(ctx, 'LONG — AND SOME OF IT AVOIDABLE', 960, 760, 32, B['steel'], a*ease(q2), 'black', 'c')
            q3 = cue(t, 'at the same time as the ship', .25, .6)
            if q3 > 0:
                txt(ctx, 'INDIA WAS BUILDING THE YARD AND THE DESIGN SKILL AT THE SAME TIME',
                    960, 830, 26, B['cyan'], a*ease(q3), 'bold', 'c', mono=True)
    return scene(f)


# ================= 7. why there is a ramp =================
def s_ramp(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'STOBAR · SHORT TAKE-OFF BUT ARRESTED RECOVERY', a, EP)
        if i == 0:
            skijump(ctx, 760, 520, .78, a, fin(t, .2, 1.4), t, 0.)
            q = cue(t, 'That is a ski-jump', .25, .6)
            if q > 0: tagb(ctx, 1180, 390, 'SKI-JUMP', B['amber'], a*ease(q), 32)
            q2 = cue(t, 'Vikrant has no catapult', .25, .6)
            if q2 > 0:
                catapult(ctx, 760, 760, .78, a*ease(q2), ease(q2))
                tagb(ctx, 1180, 745, 'CATAPULT · NOT FITTED', B['dim'], a*ease(q2), 28)
        elif i == 1:
            lp = ease(cue(t, 'the ramp flings it upwards', .4, 2.2))
            skijump(ctx, 560, 600, .78, a, 1., t, max(lp, ease(cue(t, 'runs down the deck', .3, 2.6))))
            q = cue(t, 'slow to share it', .25, .6)
            if q > 0: txt(ctx, 'INDIA DOES NOT HAVE THAT TECHNOLOGY', 960, 880, 30, B['steel'], a*ease(q), 'black', 'c')
        else:
            skijump(ctx, 820, 360, .66, a, 1., t, 1.)
            qw = cue(t, 'three arrester wires', .25, .6)
            if qw > 0: tagb(ctx, 960, 520, 'BACK ABOARD: ONE OF THREE ARRESTER WIRES', B['cyan'], a*ease(qw), 28, align='c')
            q = cue(t, 'The honest cost', .25, .6)
            if q > 0:
                card(ctx, 300, 620, 1320, 240, a*ease(q), 'THE HONEST COST', B['alert'], ease(q))
                for k, ln in enumerate(('A ski-jump launch cannot be as heavy as a catapult launch.',
                                        'Less fuel, or fewer weapons, or both.')):
                    qq = ease(seg(q, .2 + k*.3, .8 + k*.3))
                    txt(ctx, ln, 340, 720 + k*58, 34, B['ice'] if k == 0 else B['amber'], a*qq, 'bold')
    return scene(f)


# ================= 8. the deck, which is a skill =================
def s_deck(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'THE DECK IS NOT METAL. IT IS SKILL.', a, EP)
        if i == 0:
            ap = ease(cue(t, 'made the first fixed-wing landing', .4, 2.0))
            deck_plan(ctx, 860, 470, .88, a, fin(t, .15, 1.4), wires=0, approach=ap)
            q = cue(t, 'sixth of February 2023', .25, .6)
            if q > 0:
                card(ctx, 1400, 280, 460, 210, a*ease(q), '6 FEB 2023', B['cyan'], ease(q))
                txt(ctx, 'FIRST FIXED-WING', 1430, 370, 28, B['ice'], a*ease(seg(q, .2, 1)), 'black')
                txt(ctx, 'LANDINGS', 1430, 404, 28, B['ice'], a*ease(seg(q, .3, 1)), 'black')
                txt(ctx, 'MiG-29K  ·  LCA (NAVY)', 1430, 448, 21, B['steel'], a*ease(seg(q, .5, 1)), 'bold', mono=True)
            q2 = cue(t, 'landed on her at night', .25, .6)
            if q2 > 0: tagb(ctx, 1400, 540, '24 MAY 2023 · FIRST NIGHT LANDING', B['amber'], a*ease(q2), 28)
        else:
            ap = ease(fin(t, .3, 2.4))
            deck_plan(ctx, 860, 450, .88, a*.9, 1., wires=3, approach=ap)
            q = cue(t, 'dark, moving, pitching rectangle', .3, .7)
            if q > 0:
                card(ctx, 300, 690, 1320, 200, a*ease(q), 'WHAT A NIGHT LANDING IS', B['cyan'], ease(q))
                txt(ctx, 'A dark, moving, pitching rectangle, almost no visual cues,', 340, 790, 32, B['ice'], a*ease(q), 'bold')
                txt(ctx, 'at a speed where there is no time to think.', 340, 838, 32, B['ice'], a*ease(seg(q, .3, 1)), 'bold')
            q2 = cue(t, 'That is problem two, solved', .25, .6)
            if q2 > 0: txt(ctx, 'PROBLEM TWO: SOLVED', 960, 950, 40, B['amber'], a*ease(q2), 'black', 'c', glow=.7)
    return scene(f)


# ================= 9. the wing, which is not =================
def s_wing(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'THE AIR WING', a, EP)
        icon_plane(ctx, 400, 400, 2.2, B['amber'], a, fin(t, .15, 1.2))
        if i == 0:
            q = cue(t, 'which are Russian', .25, .6)
            if q > 0: tagb(ctx, 250, 640, 'MiG-29K · IMPORTED', B['steel'], a*ease(q), 30)
            q2 = cue(t, 'twenty-six Rafale-Marine aircraft', .25, .6)
            if q2 > 0:
                card(ctx, 880, 250, 940, 280, a*ease(q2), 'INTER-GOVERNMENTAL AGREEMENT · 28 APRIL 2025', B['cyan'], ease(q2))
                txt(ctx, '26 RAFALE-MARINE', 920, 390, 54, B['ice'], a*ease(seg(q2, .2, 1)), 'black')
                txt(ctx, '22 SINGLE-SEAT  ·  4 TWIN-SEAT  ·  DELIVERY BY 2030', 920, 450, 23, B['steel'],
                    a*ease(seg(q2, .4, 1)), 'bold', mono=True)
        elif i == 1:
            tagb(ctx, 250, 640, 'MiG-29K · IMPORTED', B['steel'], a, 30)
            card(ctx, 880, 230, 940, 420, a, 'WHAT THE PACKAGE INCLUDES', B['cyan'], 1.)
            items = [('Training and simulators', 'training, simulators'),
                     ('Rafale fuselage production in India', 'a Rafale fuselage production facility in India'),
                     ('MRO for engines, sensors, weapons', 'maintenance and overhaul facilities'),
                     ('Technology transfer for Indian weapons', 'technology transfer to integrate Indian weapons')]
            for k, (lab, c) in enumerate(items):
                q = cue(t, c, .22, .5)
                if q <= 0: continue
                txt(ctx, lab, 920, 330 + k*82, 30, B['ice'], a*ease(q), 'bold')
                glow_dot(ctx, 900, 320 + k*82, 5, B['cyan'], a*ease(q))
        elif i == 2:
            q = cue(t, 'it is still a purchase', .25, .6)
            if q > 0: txt(ctx, 'A SERIOUS INDUSTRIAL DEAL — AND STILL A PURCHASE', 1150, 300, 36,
                          B['ice'], a*ease(q), 'black', 'c')
            q2 = cue(t, 'Twin Engine Deck Based Fighter', .25, .6)
            if q2 > 0:
                card(ctx, 830, 380, 1020, 170, a*ease(q2), "INDIA'S OWN ANSWER", B['cyan'], ease(q2))
                txt(ctx, 'TEDBF · IN DEVELOPMENT · YEARS AWAY', 870, 490, 34, B['ice'], a*ease(seg(q2, .3, 1)), 'black')
            q3 = cue(t, 'imported American GE engines', .25, .6)
            if q3 > 0:
                card(ctx, 830, 590, 1020, 190, a*ease(q3), 'AND NOT ONLY THE AIRCRAFT', B['alert'], ease(q3))
                txt(ctx, "THE SHIP'S GAS TURBINES ARE IMPORTED", 870, 690, 30, B['ice'], a*ease(seg(q3, .2, 1)), 'black')
                txt(ctx, 'SHEKHAR GUPTA · THEPRINT', 870, 736, 21, B['steel'], a*ease(seg(q3, .5, 1)), 'bold', mono=True)
        else:
            q = cue(t, 'India built the ship', .25, .7)
            lines = [('INDIA BUILT THE SHIP.', B['cyan']),
                     ('INDIA CAN FLY FROM THE SHIP.', B['cyan']),
                     ('THE THING THAT FLIES IS BOUGHT.', B['amber'])]
            for k, (ln, col) in enumerate(lines):
                qq = ease(seg(q, k*.22, .7 + k*.22))
                if qq <= 0: continue
                txt(ctx, ln, 1150, 350 + k*90, 46, col, a*qq, 'black', 'c', glow=.5 if k == 2 else .2)
            q2 = cue(t, 'the same story', .25, .6)
            if q2 > 0:
                txt(ctx, 'THE TEJAS STORY, ONE DECK HIGHER', 1150, 700, 32, B['steel'], a*ease(q2), 'bold', 'c', mono=True)
                txt(ctx, 'THE HULL IS THE EASY PART TO BE PROUD OF', 1150, 760, 28, B['dim'],
                    a*ease(seg(q2, .3, 1)), 'bold', 'c', mono=True)
    return scene(f)


# ================= 10. why a carrier at all =================
def s_why(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'REACH · SCHEMATIC, NOT A MAP', a, EP)
        mv = ease(cue(t, 'A carrier is an airfield that moves', .3, 2.4)) if i == 0 else 1.
        reach(ctx, a, fin(t, .2, 1.4) if i == 0 else 1., t, mv)
        if i == 0:
            q = cue(t, 'the runway stays where it is', .25, .6)
            if q > 0: txt(ctx, 'THE RUNWAY STAYS WHERE IT IS', 520, 920, 28, B['steel'], a*ease(q), 'bold', 'c', mono=True)
            q2 = cue(t, 'the day after a decision', .25, .6)
            if q2 > 0: txt(ctx, 'SOMEWHERE THE DAY AFTER A DECISION', 1420, 920, 28, B['cyan'], a*ease(q2), 'bold', 'c', mono=True)
        elif i == 1:
            q = cue(t, 'about a thousand kilometres', .3, .7)
            if q > 0:
                card(ctx, 300, 160, 1320, 210, a*ease(q), 'ASHLEY TELLIS, QUOTED IN GUPTA’S COLUMN', B['amber'], ease(q))
                txt(ctx, 'Within about 1,000 km of the peninsula you do not need a carrier:',
                    340, 260, 31, B['ice'], a*ease(q), 'bold')
                txt(ctx, 'shore-based aircraft with refuelling already cover it.',
                    340, 306, 31, B['ice'], a*ease(seg(q, .3, 1)), 'bold')
            q2 = cue(t, 'shore-based aircraft with air-to-air refuelling', .25, .6)
            if q2 > 0: tagb(ctx, 960, 880, 'SHORE-BASED AIRCRAFT ALREADY COVER IT', B['cyan'], a*ease(q2), 28, align='c')
        else:
            qe = cue(t, 'off East Africa', .25, .6)
            if qe > 0: tagb(ctx, 960, 180, 'CARRIERS EARN THEIR KEEP FURTHER OUT', B['cyan'], a*ease(qe), 28, align='c')
            q = cue(t, 'how far from home India intends to operate', .3, .7)
            if q > 0:
                txt(ctx, 'NOT: ARE CARRIERS USEFUL?', 960, 280, 40, B['steel'], a*ease(q), 'black', 'c')
                txt(ctx, 'BUT: HOW FAR FROM HOME?', 960, 350, 48, B['ice'], a*ease(seg(q, .3, 1)), 'black', 'c', glow=.5)
            q2 = cue(t, 'a political decision, not a naval one', .25, .6)
            if q2 > 0:
                txt(ctx, 'A POLITICAL DECISION, NOT A NAVAL ONE', 960, 840, 36, B['amber'], a*ease(q2), 'black', 'c', glow=.6)
    return scene(f)


# ================= 11. where people disagree =================
def s_deb(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'SEA CONTROL VERSUS SEA DENIAL', a, EP)
        sides = [('SEA CONTROL · CARRIERS', ['Hold an area of ocean', 'Everything in it answers to you', 'Seen — which is the point'], B['cyan']),
                 ('SEA DENIAL · SUBMARINES', ['Cannot hold the sea', 'Can make it unusable', 'Hidden by design'], B['amber'])]
        if i < 3:
            for k, (title, lines, col) in enumerate(sides):
                if i == 0 and k == 1: continue
                x = 120 + k*900
                card(ctx, x, 230, 840, 400, a, title, col, 1.)
                for j, ln in enumerate(lines):
                    if (i == 0 and k == 0) or (i == 1 and k == 1): q = ease(seg(t, .4 + j*.8, 1.3 + j*.8))
                    else: q = 1.
                    if q <= 0: continue
                    txt(ctx, ln, x + 40, 340 + j*86, 30, B['ice'], a*q, 'bold')
            if i == 2:
                q = cue(t, 'their strength and their exposure', .3, .7)
                if q > 0:
                    txt(ctx, 'THEIR STRENGTH AND THEIR EXPOSURE, IN THE SAME SENTENCE',
                        960, 740, 32, B['steel'], a*ease(q), 'black', 'c')
        else:
            card(ctx, 240, 230, 1440, 420, a, 'THE MONEY IS THE SAME MONEY · LT GEN PRAKASH MENON, THEPRINT', B['alert'], 1.)
            rows = [('1999', 'plan for 24 conventional submarines', 'a 1999 plan for twenty-four conventional submarines'),
                    ('~20 YEARS', 'Project 75 behind schedule', 'Project 75 running nearly two decades late'),
                    ('16', 'conventional boats, lives being extended', 'a force of sixteen conventional boats')]
            for k, (n, lab, c) in enumerate(rows):
                q = cue(t, c, .25, .55)
                if q <= 0: continue
                txt(ctx, n, 300, 360 + k*110, 50, B['ice'], a*ease(q), 'black')
                txt(ctx, lab, 620, 360 + k*110, 30, B['steel'], a*ease(seg(q, .3, 1)), 'bold')
            q2 = cue(t, 'a rupee not spent there', .25, .6)
            if q2 > 0:
                txt(ctx, 'EVERY RUPEE OF CARRIER IS A RUPEE NOT SPENT THERE', 960, 760, 36,
                    B['amber'], a*ease(q2), 'black', 'c', glow=.6)
    return scene(f)


# ================= 12. the third ship =================
def s_third(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'HOW MANY, AND HOW BIG', a, EP)
        if i == 0:
            st = [ease(cue(t, 'Vikramaditya, bought from Russia', .3, .7)),
                  ease(cue(t, 'and Vikrant', .25, .7)),
                  .6*ease(cue(t, 'The Navy has long said it wants three', .25, .9))]
            fleet(ctx, a, ['VIKRAMADITYA', 'VIKRANT', 'A THIRD'], st)
            q = cue(t, 'does not always have two carriers', .25, .6)
            if q > 0: txt(ctx, 'A NAVY WITH TWO CARRIERS DOES NOT ALWAYS HAVE TWO CARRIERS',
                          960, 760, 34, B['steel'], a*ease(q), 'black', 'c')
        elif i == 1:
            card(ctx, 300, 260, 1320, 300, a, '1965', B['alert'], fin(t, .1, .7))
            for k, ln in enumerate(('A Pakistani force shelled Dwarka.', 'No Indian carrier answered.',
                                    'The first Vikrant was in dry dock.')):
                q = ease(seg(t, .4 + k*.9, 1.3 + k*.9))
                if q > 0: txt(ctx, ln, 340, 370 + k*62, 36, B['ice'] if k < 2 else B['amber'], a*q, 'bold')
            q2 = cue(t, 'the skills disappear', .25, .6)
            if q2 > 0: tagb(ctx, 960, 680, 'MENON: STOP BUILDING AND THE YARD, DESIGNERS AND SKILLS GO', B['steel'], a*ease(q2), 26, align='c')
        elif i == 2:
            card(ctx, 300, 250, 1320, 330, a, 'IAC-2 · AS REPORTED, NOVEMBER 2023', B['cyan'], fin(t, .1, .7))
            for k, (n, lab, c) in enumerate((('~45,000 t', 'DISPLACEMENT', 'around forty-five thousand tonnes'),
                                             ('~₹40,000 cr', 'ESTIMATE', 'about forty thousand crore rupees'),
                                             ('REPEAT', 'OF VIKRANT', 'a repeat order of Vikrant'))):
                q = cue(t, c, .25, .55)
                if q <= 0: continue
                txt(ctx, n, 350 + k*440, 390, 44, B['ice'], a*ease(q), 'black')
                txt(ctx, lab, 350 + k*440, 428, 21, B['steel'], a*ease(seg(q, .3, 1)), 'bold', mono=True)
            txt(ctx, 'IN-PRINCIPLE CLEARANCE, DEFENCE PROCUREMENT BOARD · REPORTED, NOT ANNOUNCED',
                960, 530, 24, B['dim'], a*ease(fin(t, .5, .8)), 'bold', 'c', mono=True)
        elif i == 3:
            card(ctx, 140, 250, 800, 380, a, 'TELLIS, IN GUPTA’S COLUMN', B['amber'], 1.)
            for k, ln in enumerate(('India chose small carriers:', 'heavy on crew,', 'light on firepower.')):
                q = ease(seg(t, .3 + k*.7, 1.1 + k*.7))
                if q > 0: txt(ctx, ln, 180, 360 + k*62, 34, B['ice'], a*q, 'bold')
            q = cue(t, 'sixty-five thousand tonnes', .3, .7)
            if q > 0:
                card(ctx, 1000, 250, 780, 380, a*ease(q), 'THE SIZE AT WHICH THE NUMBERS WORK', B['cyan'], ease(q))
                txt(ctx, '65,000 t', 1390, 430, 76, B['amber'], a*ease(seg(q, .2, 1)), 'black', 'c', glow=.8)
                txt(ctx, 'ON AMERICAN EXPERIENCE', 1390, 490, 22, B['steel'], a*ease(seg(q, .4, 1)), 'bold', 'c', mono=True)
        else:
            for k, (title, lines, col) in enumerate((('A REPEAT ORDER', ['Cheaper', 'Faster', 'A design the yard has built once'], B['cyan']),
                                                     ('A BIGGER SHIP', ['Carries more', 'Launches it heavier', 'Another two decades to learn'], B['amber']))):
                x = 120 + k*900
                card(ctx, x, 230, 840, 380, a, title, col, 1.)
                for j, ln in enumerate(lines):
                    q = ease(seg(t, .3 + j*.5 + k*.3, 1.0 + j*.5 + k*.3))
                    if q > 0: txt(ctx, ln, x + 40, 340 + j*80, 32, B['ice'], a*q, 'bold')
            q = cue(t, 'no contract has been announced publicly', .3, .7)
            if q > 0:
                txt(ctx, 'AS OF 21 NOVEMBER 2026: NO CONTRACT ANNOUNCED', 960, 740, 38,
                    B['alert'], a*ease(q), 'black', 'c', glow=.6)
    return scene(f)


# ================= 13. where it stands =================
ROWS = [('THE SHIP', 'Commissioned September 2022, ~76% indigenous', 'LARGEST BUILT IN INDIA', 'cyan', 'commissioned September 2022'),
        ('THE DECK', 'Fixed-wing day and night landings done', 'WORKING UP', 'cyan', 'day and night landings done'),
        ('THE WING', 'MiG-29K in service; 26 Rafale-Marine on contract', 'DELIVERY BY 2030', 'amber', 'MiG-29K in service'),
        ('THE STEEL', 'Made in India, which it was not twenty years ago', 'SELF-SUFFICIENT', 'cyan', 'Made in India, which it was not'),
        ('THE THIRD SHIP', 'Cleared in principle as reported in 2023', 'NO CONTRACT ANNOUNCED', 'alert', 'cleared in principle')]


def s_st(i):
    def f(ctx, t, D):
        bg(ctx); a = outro(t, D, .35)
        hud(ctx, t, 'WHERE IT STANDS · 21 NOVEMBER 2026', a, EP)
        show = [(0, 3), (3, 5)][i]
        for k in range(show[0], show[1]):
            name, note, status, col, c = ROWS[k]
            q = ease(cue(t, c, .3, .8))
            if q <= 0: continue
            statusrow(ctx, 220, 300 + (k - show[0])*220, 1480, name, note, status, B[col], a*q, q)
    return scene(f)


# ================= 14. in three words =================
def s_three(ctx, t, D):
    bg(ctx); a = outro(t, D, .5)
    hud(ctx, t, 'IN THREE WORDS', a, EP)
    words = [('STEEL', 'INDIA MAKES IT'), ('DECK', 'INDIA EARNED IT'), ('WING', 'STILL ARRIVING')]
    fillp = ease(cue(t, 'The wing is still arriving', .2, 2.0))
    for k, (w_, sub) in enumerate(words):
        q = ease(cue(t, ['Steel.', 'Deck.', 'Wing.'][k], .25, .5))
        if q <= 0: continue
        y = 290 + k*180
        col = B['amber'] if k == 2 else B['cyan']
        wq = tw(ctx, w_, 110, 'black')
        if k < 2:
            txt(ctx, w_, 960, y, 110, col, a*q, 'black', 'c', glow=1.)
        else:
            txt(ctx, w_, 960, y, 110, B['dim'], a*q, 'black', 'c')
            ctx.save(); ctx.rectangle(960 - wq/2, y - 100, wq*(.5*fillp), 130); ctx.clip()
            txt(ctx, w_, 960, y, 110, B['amber'], a*q, 'black', 'c', glow=1.2)
            ctx.restore()
            bx = 960 - wq/2
            stroke_pts(ctx, rect_pts(bx, y + 26, wq, 16), q, B['dim'], a*q*.8, 2, glow=False)
            fill(ctx, lambda: ctx.rectangle(bx, y + 26, wq*.5*fillp, 16), B['amber'], .85*a*q)
        txt(ctx, sub, 960, y + (76 if k == 2 else 46), 24, B['amber'] if k == 2 else B['steel'],
            a*ease(seg(q, .4, 1)), 'bold', 'c', mono=True)
    e = cue(t, 'none of it finished', .25, .6)
    if e > 0:
        txt(ctx, 'SOME BOUGHT · SOME BEING DESIGNED · NONE OF IT FINISHED', 960, 900, 28,
            B['ice'], a*ease(e), 'bold', 'c', mono=True)
s_three = scene(s_three)


# ================= 15. the wall, next, subscribe =================
def s_end(ctx, t, D):
    bg(ctx); a = outro(t, D, .5)
    hud(ctx, t, 'THE BLUEPRINT WALL', a, EP)
    wall6(ctx, t, a, drop=seg(t, .4, 1.6))
    tn = Ts('Next on')
    nq = seg(t, tn, tn + .6) if tn < 900 else 0
    if nq > 0:
        q = ease(nq)
        fill(ctx, lambda: ctx.rectangle(0, 700, W*eoc(nq), 90), B['deep'], .95*a*q)
        rgba(ctx, B['cyan'], a*q); ctx.rectangle(0, 700, W*eoc(nq), 3); ctx.fill()
        txt(ctx, 'NEXT  ·  PINAKA: FROM A ROCKET THAT GOES WHERE IT IS POINTED', 80, 758, 30, B['ice'], a*q, 'bold', mono=True)
    subscribe_card(ctx, t, Ts('subscribe'), a, x=1540, y=900)
s_end = scene(s_end)


# ================= beats =================
SC = {}
FACT = {'cold': s_cold, 'anchor': s_anchor, 'id': s_id, 'steel': s_steel, 'build': s_build,
        'ramp': s_ramp, 'deck': s_deck, 'wing': s_wing, 'why': s_why, 'deb': s_deb,
        'third': s_third, 'st': s_st}
STEMS = list(FACT) + ['qs', 'three', 'end']


def stem_of(k):
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
 'cold2': [('This one India built', 'INDIA BUILT IT', 'amber')],
 'id1': [('forty-three thousand tonnes', '43,000 TONNES', 'cyan')],
 'steel2': [('self-sufficient', 'SELF-SUFFICIENT', 'amber')],
 'build2': [('Seventeen years', '17 YEARS', 'amber')],
 'deck2': [('That is problem two, solved', 'PROBLEM TWO', 'cyan')],
 'wing1': [('twenty-six Rafale-Marine aircraft', '26 RAFALE-M', 'cyan')],
 'why2': [('about a thousand kilometres', '1,000 km', 'amber')],
 'third4': [('sixty-five thousand tonnes', '65,000 TONNES', 'amber')],
}
ANNOT = {
 'wing4': [('the thing that flies is bought', 'underline', 1150, 540, 700, 0)],
 'deb4': [('a rupee not spent there', 'circle', 960, 760, 1100, 90)],
}

_order = [k for k, _ in EN]
FX = [('whoosh', k, -.25, .22) for i, k in enumerate(_order) if i and GROUPS[k] != GROUPS[_order[i-1]]]
FX += [('beep', k, ph, .14) for k, items in KEYS.items() for ph, _, _ in items]
FX += [('tick', 'cold1', .15, .12),
       ('ding', 'cold1', 'The bell was made in 1961', .3),
       ('riser', 'cold2', 'This one India built', .2),
       ('boom', 'cold2', 'This one India built', .45),
       ('ping', 'anchor1', 'Three: the wing', .3),
       ('stamp', 'steel2', 'self-sufficient', .35),
       ('riser', 'build2', 'Seventeen years', .2),
       ('ping', 'ramp2', 'the ramp flings it upwards', .3),
       ('ding', 'deck2', 'That is problem two, solved', .25),
       ('glitch', 'wing3', 'imported American GE engines', .3),
       ('boom', 'wing4', 'the thing that flies is bought', .3),
       ('ping', 'deb1', 'sea control versus sea denial', .3),
       ('glitch', 'third2', 'No Indian carrier answered', .3),
       ('riser', 'three1', 'Steel.', .12), ('ding', 'three1', 'Steel.', .22),
       ('ding', 'three1', 'Deck.', .22), ('ding', 'three1', 'Wing.', .22),
       ('stamp', 'end1', .5, .35), ('ding', 'end1', 'subscribe', .2)]
