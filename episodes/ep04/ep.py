"""India's Defence, Decoded — Episode 4: The Shield (bilingual: English + Hindi).
No maps in this episode: coverage is drawn as abstract nested rings, never over territory."""
import os, sys, math, random, cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 770.0
core.TOTAL = TOTAL
from engine.core import W, H, seg, ease, eoc, eob, lerp, T
from engine.bp import (B, rgba, rrect, bg, txt, tw, typed, wrap, para, stroke_pts, head_pt, rect_pts, fill, glow_dot,
                       bez, missile, truck, figure, radar, hud, card, tagb, outro, camera, scene, subscribe_card)
from engine.shield import (ring, rings, protected, icon_eye, icon_brain, icon_launch, inbound, sensor_grid,
                           netbox, link, rampart, statusrow, splitspeed)
from text import EN, HI as _HI

EP = 4
CODE = 'Def04'
TITLE = 'The_Shield'
NAME = 'How India Is Actually Building a Missile Shield'
POST = 'engine.bp'
BED = 'pulse'
VOICE_EN = {'length': 0.98, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
VOICE_HI = {'length': 0.86, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
CRF, PRESET = 17, 'medium'
EXTRA = {'cold1': .8, 'cold3': .5, 'job3': .5, 'three1': 1.2, 'end1': 2.5}
HI = _HI

CX, CY = 960, 640          # centre of the ring diagram
RSPEC = [(715, 'S-400', 'LONG RANGE'), (560, 'MR-SAM', 'MEDIUM'), (380, 'AKASH · QRSAM · SPYDER', 'SHORT'),
         (210, 'GUNS AND MANPADS', 'CLOSE-IN')]


def Ts(x):
    try: return T(x)
    except ValueError: return 999.
def fin(t, t0=.1, d=.5): return ease(seg(t, t0, t0 + d))
def cue(t, s, lead=.2, dur=.45):
    c = Ts(s)
    return 0. if c >= 900 else seg(t, c - lead, c - lead + dur)


# ================= cold open: the night of 9 May 2025 =================
def s_cold(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D, .35)
        hud(ctx, t, 'OPERATION SINDOOR · NIGHT OF 9–10 MAY 2025', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=560)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        inbound(ctx, t, a*.9)
        sensor_grid(ctx, t, a, p=1. if first > 0 else fin(t, 1.2, 1.2))
        # the clock (cold2 opens on it)
        q = cue(t, 'It was a race against a clock', .3, .5)
        if q > 0:
            qa = ease(q)*a_out
            txt(ctx, 'A RACE AGAINST A CLOCK', W/2, 430, 72, B['ice'], qa, 'black', 'c', glow=.9)
            r = 86; cx2, cy2 = W/2, 560
            ctx.new_path(); rgba(ctx, B['dim'], qa); ctx.set_line_width(5); ctx.arc(cx2, cy2, r, 0, 2*math.pi); ctx.stroke()
            ang = -math.pi/2 + 2*math.pi*((t*.9) % 1)
            stroke_pts(ctx, [(cx2, cy2), (cx2 + r*.8*math.cos(ang), cy2 + r*.8*math.sin(ang))], 1, B['alert'], qa, 5, glow=False)
        # India's account, in two cards
        q = cue(t, 'India gave its account of that night', .3, .5)
        if q > 0:
            qa = ease(q)*a_out
            rgba(ctx, B['deep'], .95*qa); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
            txt(ctx, "INDIA'S ACCOUNT OF THAT NIGHT", W/2, 250, 48, B['ice'], qa, 'black', 'c', glow=.6)
            txt(ctx, 'PRESS INFORMATION BUREAU · 16 MAY 2025', W/2, 300, 24, B['cyan'], qa, 'bold', 'c', mono=True)
            for j, (quote, c, col) in enumerate((('"Intercepted and neutralised every inbound projectile."', 'The Press Information Bureau said', B['amber']),
                                                 ('"Failed to detect and intercept Indian strikes."', 'HQ-9 and HQ-16', B['steel']))):
                qq = cue(t, c, .2, .5)
                if qq <= 0: continue
                qb = ease(qq)*a_out; y = 360 + j*230
                card(ctx, 180, y, 1560, 190, qb, ('ON AKASHTEER', "ON PAKISTAN'S IMPORTED HQ-9 AND HQ-16")[j], col, p=qq)
                for i, l in enumerate(wrap(ctx, quote, 42, 1440, 'bold')):
                    txt(ctx, l, 230, y + 120 + i*52, 42, B['ice'], qb, 'bold')
        if first > 1:
            q = cue(t, "That is India's official account", .25, .5)
            if q > 0:
                qa = ease(q)*a_out
                rgba(ctx, B['deep'], .96*qa); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
                txt(ctx, "INDIA'S OFFICIAL ACCOUNT, PUBLISHED BY THE GOVERNMENT", W/2, 420, 44, B['ice'], qa, 'black', 'c', glow=.5)
                qq = cue(t, 'independent verification of the numbers is not public', .2, .45)
                if qq > 0:
                    tagb(ctx, W/2, 510, 'INDEPENDENT VERIFICATION OF THE NUMBERS IS NOT PUBLIC', B['steel'], ease(qq)*a_out, 26, align='c')
        q2 = cue(t, 'Akashteer is not a missile', .2, .5)
        if q2 > 0:
            qa = ease(q2)*a_out
            rgba(ctx, B['deep'], min(1., 1.12*qa)); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
            txt(ctx, 'AKASHTEER IS NOT A MISSILE', W/2, 520, 76, B['amber'], qa, 'black', 'c', glow=1)
            q3 = cue(t, 'It does not shoot anything', .2, .4)
            if q3 > 0: txt(ctx, 'IT DOES NOT SHOOT ANYTHING', W/2, 620, 46, B['ice'], ease(q3)*a_out, 'black', 'c')
        ctx.restore()
    return scene(f)


# ================= the anchor: three jobs, then rings =================
JOBS = [('SEE', icon_eye, 'It has to see something coming'), ('DECIDE', icon_brain, 'It has to decide what to do about it'),
        ('SHOOT', icon_launch, 'And then it has to shoot')]
def s_job(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'THE SIMPLE VERSION FIRST', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tdome = Ts('Forget the word dome')
        phase = ease(seg(t, tdome - .4, tdome + .4)) if tdome < 900 else (1. if first > 0 else 0)
        if phase < 1:
            aa = (1 - phase)*a
            for i, (nm, icon, c) in enumerate(JOBS):
                q = cue(t, c, .25, .55)
                if q <= 0: continue
                qa = ease(min(q*1.6, 1))*aa; x = 400 + i*560
                icon(ctx, x, 420, 1.5, B['cyan'] if i < 2 else B['amber'], qa, p=eoc(q))
                txt(ctx, nm, x, 580, 62, B['ice'], qa, 'black', 'c', glow=.6)
                txt(ctx, f'0{i+1}', x, 640, 26, B['steel'], qa, 'bold', 'c', mono=True)
            q = cue(t, 'the one with the fireworks', .2, .4)
            if q > 0: tagb(ctx, 1520, 700, 'THE ONLY ONE ANYONE THINKS ABOUT', B['amber'], ease(q)*aa, 22, align='c')
            q = cue(t, 'The first two are harder', .2, .4)
            if q > 0: tagb(ctx, 700, 790, 'THE FIRST TWO ARE THE HARD ONES', B['cyan'], ease(q)*aa, 30, align='c')
        if phase > 0:
            aa = phase*a_out
            # the struck-through word, then the rings
            td = ease(seg(t, tdome + .4, tdome + 1.6)) if tdome < 900 else 1.
            if td < 1:
                txt(ctx, 'DOME', W/2, 520, 150, B['steel'], aa*(1 - td*.4), 'black', 'c')
                ww = tw(ctx, 'DOME', 150, 'black')/2
                ctx.save(); ctx.set_line_width(12); rgba(ctx, B['alert'], aa*eoc(min(td*2, 1)))
                ctx.move_to(W/2 - ww - 20, 470); ctx.line_to(W/2 - ww - 20 + (2*ww + 40)*eoc(min(td*2, 1)), 470); ctx.stroke(); ctx.restore()
            if td > .3:
                ra = aa*ease(min((td - .3)/.5, 1))
                protected(ctx, CX, CY, ra)
                specs = []
                cues = ['The outermost ring carries a long-range system', 'Inside it is a medium ring',
                        'Inside that, a short-range ring', 'guns and shoulder-fired missiles']
                for i, (r, nm, sub) in enumerate(RSPEC):
                    c = cue(t, cues[i], .25, 1.1)
                    if c <= 0 and first > 1: c = 1.
                    cols = [B['amber'], B['cyan'], B['cyan'], B['steel']]
                    specs.append((r, cols[i], nm, sub, c))
                rings(ctx, CX, CY, specs, t, ra)
                if first > 1:
                    for j, (l, c) in enumerate((('MISSED BY ONE RING → THE NEXT ONE TRIES', 'the next ring in gets a turn at'),
                                                ('NEVER A CRORE INTERCEPTOR ON A LAKH DRONE', 'a drone worth a couple of lakhs'),
                                                ('EACH RING SAVES THE ONE OUTSIDE IT', 'does not have to waste itself'))):
                        q = cue(t, c, .2, .4)
                        if q > 0: tagb(ctx, 90, 250 + j*66, l, B['amber'] if j == 2 else B['cyan'], ease(q)*a_out, 24)
        ctx.restore()
    return scene(f)


# ================= four questions =================
QS = [('WHAT IS', 'THE S-400?', 'What is the S-400 India bought'), ('WHAT REPLACES IT?', 'BUILT HERE', 'What is India building to replace it'),
      ('WHY IS BALLISTIC', 'DIFFERENT?', 'completely different problem'), ('WHAT DOES THE', 'MISSION PROMISE?', 'actually promising')]
def s_qs(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, "INDIA'S DEFENCE, DECODED · EPISODE 4", a_out, EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
    txt(ctx, 'FOUR QUESTIONS', W/2, 240, 60, B['ice'], fin(t, .2, .6)*a_out, 'black', 'c', glow=.6)
    for i, (k1, k2, c) in enumerate(QS):
        q = cue(t, c, .2, .5)
        if q <= 0: continue
        x = 140 + i*430; y = 330; a = ease(min(q*2, 1))*a_out; s = eob(q, 1.7)
        ctx.save(); ctx.translate(x + 190, y + 190); ctx.scale(s, s); ctx.translate(-(x + 190), -(y + 190))
        card(ctx, x, y, 380, 380, a, None, B['cyan'] if i % 2 == 0 else B['amber'], p=q)
        txt(ctx, f'0{i+1}', x + 30, y + 130, 96, B['amber'] if i % 2 else B['cyan'], a, 'black', glow=.8)
        txt(ctx, k1, x + 30, y + 230, 24, B['steel'], a, 'bold', mono=True)
        for j, l in enumerate(wrap(ctx, k2, 44, 320, 'black')):
            txt(ctx, l, x + 30, y + 300 + j*50, 44, B['ice'], a, 'black')
        ctx.restore()
    ctx.restore()
scene(s_qs)


# ================= the rings India has =================
HAVE = [('S-400', 'RUSSIAN · OUTER RING', B['amber'], 'The outer ring is the S-400'),
        ('MR-SAM', 'DRDO + IAI · ~70 KM PUBLISHED', B['cyan'], 'Inside it sits MR-SAM'),
        ('AKASH · AKASH PRIME', 'INDIAN · SHORT RANGE', B['cyan'], 'Akash, which is Indian'),
        ('SPYDER', 'ISRAELI · SHORT RANGE', B['cyan'], 'the Israeli SPYDER'),
        ('QRSAM', 'INDIAN · SHOOTS ON THE MOVE', B['cyan'], 'a quick-reaction Indian system'),
        ('GUNS AND MANPADS', 'WITHIN A FEW KILOMETRES', B['steel'], 'anti-aircraft guns')]
def s_have(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'THE RINGS INDIA HAS · RANGES AS PUBLISHED', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=560)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tcall = Ts('Remember the five missiles')
        back = ease(seg(t, tcall - .4, tcall + .4)) if tcall < 900 else 0
        if back < 1:
            aa = (1 - back)*a
            protected(ctx, 620, 700, aa)
            specs = []
            for i, (r, nm, sub) in enumerate(RSPEC):
                cols = [B['amber'], B['cyan'], B['cyan'], B['steel']]
                p = 1. if first > 0 else fin(t, .3 + i*.25, .8)
                specs.append((r*.78, cols[i], None, None, p))
            rings(ctx, 620, 700, specs, t, aa*.55)
            for i, (nm, sub, col, c) in enumerate(HAVE):
                q = cue(t, c, .25, .5)
                if q <= 0 and first > 0 and Ts(c) >= 900: q = 1.
                if q <= 0: continue
                y = 230 + i*118; qa = ease(q)*aa
                card(ctx, 1130, y, 740, 100, qa, None, col, p=q)
                txt(ctx, nm, 1170, y + 48, 34, B['ice'], qa, 'black')
                txt(ctx, sub, 1170, y + 80, 20, col, qa, 'bold', mono=True)
        if back > 0:
            aa = back*a_out
            rgba(ctx, B['deep'], .96*aa); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
            txt(ctx, '1983', W/2, 290, 90, B['steel'], aa, 'black', 'c')
            names = ['PRITHVI', 'TRISHUL', 'AKASH', 'NAG', 'AGNI']
            qn = cue(t, 'Prithvi, Trishul, Akash, Nag, Agni', .2, .6)
            for i, nm in enumerate(names):
                x = 300 + i*330
                hot = nm == 'AKASH'
                qa = aa*ease(seg(t, Ts('Prithvi, Trishul, Akash, Nag, Agni') - .2 + i*.12, Ts('Prithvi, Trishul, Akash, Nag, Agni') + .25 + i*.12)) if qn > 0 else 0
                if qa <= 0: continue
                missile(ctx, x, 520, 170, -math.pi/2, qa*(1 if hot else .35), col=B['amber'] if hot else B['ice'])
                txt(ctx, nm, x, 640, 28, B['amber'] if hot else B['ice'], qa*(1 if hot else .4), 'black', 'c', glow=.6 if hot else 0)
            q = cue(t, 'forty years later', .2, .5)
            if q > 0:
                qa = ease(q)*a_out
                txt(ctx, 'SKETCHED IN THE 1980s · A WORKING LAYER TODAY', W/2, 770, 40, B['ice'], qa, 'black', 'c')
                txt(ctx, 'THESE PROGRAMMES TAKE THAT LONG', W/2, 830, 28, B['cyan'], qa*ease(cue(t, 'These programmes take that long', .2, .4)), 'bold', 'c', mono=True)
        ctx.restore()
    return scene(f)


# ================= the S-400 =================
def s_s400(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'THE S-400', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=540)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tpkg = Ts('It is a package')
        pkg = ease(seg(t, tpkg - .4, tpkg + .3)) if tpkg < 900 else (1. if first > 0 else 0)
        tlate = Ts('deliveries ran late')
        late = ease(seg(t, tlate - .4, tlate + .3)) if tlate < 900 else 0
        if pkg < 1:
            aa = (1 - pkg)*a
            truck(ctx, 760, 760, 1.25, aa*fin(t, .2, .8), t, raise_=.75, wheels_spin=0)
            q = cue(t, 'India signed for it on the fifth of October 2018', .25, .5)
            if q > 0:
                qa = ease(q)*aa
                card(ctx, 1150, 250, 700, 340, qa, 'THE CONTRACT', B['amber'], p=q)
                for j, (k, v) in enumerate((('SIGNED', '5 OCTOBER 2018'), ('FOR', '5 SQUADRONS'), ('VALUE', '~$5.43 BILLION'), ('', '~₹40,000 CRORE'))):
                    yy = 350 + j*58
                    if k: txt(ctx, k, 1195, yy, 22, B['cyan'], qa, 'bold', mono=True)
                    txt(ctx, v, 1810, yy, 34, B['ice'], qa, 'black', 'r')
            q = cue(t, 'The Air Force calls it Sudarshan Chakra', .2, .5)
            if q > 0: tagb(ctx, 760, 420, 'IAF NAME: SUDARSHAN CHAKRA', B['amber'], ease(q)*aa, 32, align='c')
        if pkg > 0 and late < 1:
            aa = pkg*(1 - late)*a_out
            parts = [('SEARCH RADAR', 'SCANS A WIDE AREA', 'a search radar that scans a wide area', 260),
                     ('ENGAGEMENT RADAR', 'LOCKS AND GUIDES', 'a second radar that locks and guides', 640),
                     ('COMMAND VEHICLE', 'DECIDES', 'a command vehicle', 1020),
                     ('LAUNCHERS', 'SEVERAL MISSILE TYPES', 'launchers carrying several different missiles', 1400)]
            for i, (nm, sub, c, x) in enumerate(parts):
                q = cue(t, c, .25, .5)
                if q <= 0 and first > 1: q = 1.
                if q <= 0: continue
                qa = ease(min(q*1.6, 1))*aa
                if i < 2: radar(ctx, x + 130, 430, 1.0, qa, t, aim=-.7 + i*.25)
                elif i == 2: stroke_pts(ctx, rect_pts(x + 60, 350, 150, 110), min(q*2, 1), B['ice'], qa, 3)
                else: missile(ctx, x + 130, 400, 180, -math.pi/2, qa, col=B['amber'])
                txt(ctx, nm, x + 130, 540, 26, B['ice'], qa, 'black', 'c')
                txt(ctx, sub, x + 130, 574, 19, B['cyan'], qa, 'bold', 'c', mono=True)
            q = cue(t, 'published figures put it out to around four hundred kilometres', .25, .5)
            if q > 0:
                qa = ease(q)*aa
                ring(ctx, CX, 860, 760, min(q*1.6, 1), B['amber'], qa, 3, 'UP TO ~400 KM, WITH ITS LONGEST MISSILE', qa, 'PUBLISHED FIGURE', .22)
            q = cue(t, 'track a large number of targets at once', .2, .4)
            if q > 0: tagb(ctx, W/2, 1000, 'MANY TARGETS TRACKED · MANY ENGAGED AT ONCE', B['cyan'], ease(q)*aa, 28, align='c')
        if late > 0:
            aa = late*a_out
            rgba(ctx, B['deep'], .96*aa); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
            q = cue(t, 'a law called CAATSA', .2, .5)
            if q > 0:
                tagb(ctx, W/2, 280, 'BOUGHT DESPITE CAATSA SANCTIONS RISK · NEVER IMPOSED', B['steel'], ease(q)*a_out, 28, align='c')
            txt(ctx, 'DELIVERIES RAN LATE', W/2, 420, 72, B['alert'], aa, 'black', 'c', glow=.8)
            for j, (l, c) in enumerate((('ORIGINAL SCHEDULE: 2023', 'the original schedule was 2023'),
                                        ('AS OF 17 NOVEMBER 2026, NO ANNOUNCEMENT', 'as of the seventeenth of November 2026'),
                                        ('THAT THE FIFTH AND FINAL SQUADRON IS HANDED OVER', 'fifth and final squadron'))):
                q = cue(t, c, .2, .4)
                if q > 0: txt(ctx, l, W/2, 540 + j*76, 42 if j else 46, B['ice'] if j < 2 else B['steel'], ease(q)*a_out, 'black', 'c')
        ctx.restore()
    return scene(f)


# ================= why buying is a problem =================
def s_buy(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'THE ARGUMENT ABOUT DEPENDENCE', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=500)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tnone = Ts('None of that is a criticism')
        sw = ease(seg(t, tnone - .4, tnone + .3)) if tnone < 900 else (1. if first > 0 else 0)
        if sw < 1:
            aa = (1 - sw)*a
            q = cue(t, 'made in another country', .25, .5)
            if q > 0:
                txt(ctx, 'THREE THINGS OUTSIDE YOUR CONTROL', W/2, 290, 56, B['ice'], ease(q)*aa, 'black', 'c', glow=.6)
            for i, (l, c) in enumerate((('WHEN IT ARRIVES', 'When it arrives'), ('WHETHER SPARES KEEP COMING', 'Whether spare parts keep coming'),
                                        ("SOMEONE ELSE'S FACTORY", 'what happens to that factory'))):
                q = cue(t, c, .2, .5)
                if q <= 0: continue
                qa = ease(q)*aa; x = 400 + i*560; s = eob(q, 1.5)
                ctx.save(); ctx.translate(x, 560); ctx.scale(s, s); ctx.translate(-x, -560)
                card(ctx, x - 250, 440, 500, 240, qa, None, B['alert'], p=q)
                txt(ctx, f'0{i+1}', x, 530, 44, B['alert'], qa, 'black', 'c')
                for j, ln in enumerate(wrap(ctx, l, 34, 440, 'black')):
                    txt(ctx, ln, x, 600 + j*42, 34, B['ice'], qa, 'black', 'c')
                ctx.restore()
        if sw > 0:
            aa = sw*a_out
            for j, (l, c, col) in enumerate((('NOT A CRITICISM OF THE SYSTEM', 'None of that is a criticism', B['steel']),
                                             ('OFFICIALS SAY IT PERFORMED WELL IN MAY 2025', 'it performed well in May 2025', B['cyan']),
                                             ('IT IS AN ARGUMENT ABOUT DEPENDENCE', 'an argument about dependence', B['amber']))):
                q = cue(t, c, .2, .5)
                if q <= 0: continue
                for i, ln in enumerate(wrap(ctx, l, 46, 1500, 'black')):
                    txt(ctx, ln, W/2, 350 + j*130 + i*50, 46, col, ease(q)*aa, 'black', 'c', glow=.5 if j == 2 else 0)
            q = cue(t, 'building quietly for most of a decade', .2, .5)
            if q > 0: tagb(ctx, W/2, 800, 'BUILT QUIETLY FOR MOST OF A DECADE', B['ice'], ease(q)*a_out, 32, align='c')
        ctx.restore()
    return scene(f)


# ================= Project Kusha =================
KINT = [('M1', '~150 KM', .30, 'a short one reaching about a hundred and fifty'),
        ('M2', '~250 KM', .62, 'a middle one at around two hundred and fifty'),
        ('M3', 'REPORTED 350–400 KM', 1.0, 'a long one reported at three hundred and fifty')]
def s_kus(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'PROJECT KUSHA', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=540)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tfly = Ts('Kusha flew for the first time')
        fly = ease(seg(t, tfly - .4, tfly + .3)) if tfly < 900 else (1. if first > 2 else 0)
        if fly < 1:
            aa = (1 - fly)*a
            if first == 0:
                txt(ctx, 'PROJECT KUSHA', W/2, 270, 72, B['ice'], aa*fin(t, .2, .6), 'black', 'c', glow=.8)
                txt(ctx, "DRDO · LONG-RANGE SURFACE-TO-AIR MISSILE", W/2, 325, 26, B['cyan'], aa*fin(t, .5, .5), 'bold', 'c', mono=True)
            rows = [('CCS CLEARED DEVELOPMENT', 'MAY 2022', 'cleared its development in May 2022'),
                    ('PROCUREMENT APPROVED', 'SEPTEMBER 2023', 'In September 2023'),
                    ('FOR', '5 SQUADRONS, INDIAN AIR FORCE', 'five squadrons for the Air Force'),
                    ('AT', '₹21,700 CRORE', 'twenty-one thousand seven hundred crore rupees')]
            for i, (k, v, c) in enumerate(rows):
                q = cue(t, c, .2, .45)
                if q <= 0: continue
                y = 430 + i*86; qa = ease(q)*aa
                stroke_pts(ctx, [(260, y + 20), (1660, y + 20)], min(q*2, 1), B['grid'], qa, 1.5, glow=False)
                txt(ctx, k, 260, y, 26, B['cyan'], qa, 'bold', mono=True)
                txt(ctx, v, 1660, y, 38, B['ice'], qa, 'black', 'r', glow=.4)
            q = cue(t, 'it is not one missile', .2, .5)
            if q > 0:
                qa = ease(q)*aa
                rgba(ctx, B['deep'], .95*qa); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
                txt(ctx, 'THREE INTERCEPTORS, ONE SYSTEM', W/2, 250, 54, B['ice'], qa, 'black', 'c', glow=.6)
                txt(ctx, 'ONE SET OF RADARS · ONE COMMAND SYSTEM', W/2, 300, 24, B['cyan'], qa, 'bold', 'c', mono=True)
                for i, (nm, rg, frac, c) in enumerate(KINT):
                    qq = cue(t, c, .2, .9)
                    if qq <= 0: continue
                    qa2 = ease(min(qq*1.6, 1))*a_out
                    ring(ctx, CX, 860, 760*frac, min(qq*1.6, 1), [B['cyan'], B['cyan'], B['amber']][i], qa2, 3, None, 0, None, .30)
                    txt(ctx, f'{nm}  {rg}', CX, 860 - 760*frac*.30 - 18, 28, [B['cyan'], B['cyan'], B['amber']][i], qa2, 'black', 'c', glow=.5)
        if fly > 0:
            aa = fly*a_out
            txt(ctx, '23 JULY 2026', W/2, 270, 90, B['amber'], aa, 'black', 'c', glow=1)
            txt(ctx, 'DR APJ ABDUL KALAM ISLAND · MAIDEN FLIGHT', W/2, 330, 26, B['cyan'], aa, 'bold', 'c', mono=True)
            p = eoc(seg(t, max(Ts('Kusha flew for the first time'), 0) + .3, max(Ts('Kusha flew for the first time'), 0) + 3.2)) if first < 3 else 1.
            arc = bez((420, 900), (900, 420), (1460, 380), 34)
            stroke_pts(ctx, arc, p, B['amber'], aa, 4)
            if p >= 1:
                for r_ in range(3):
                    rp = ((t*.5 + r_/3) % 1)
                    ctx.new_path(); rgba(ctx, B['amber'], (1 - rp)*aa*.8); ctx.set_line_width(3); ctx.arc(1460, 380, 16 + 90*rp, 0, 2*math.pi); ctx.stroke()
            elif p > 0:
                hx_, hy_, ang = head_pt(arc, p); missile(ctx, hx_, hy_, 110, ang, aa, col=B['amber'])
            for j, (l, c, col) in enumerate((('"SUCCESSFULLY INTERCEPTED A HIGH-SPEED, HIGH-ALTITUDE AERIAL TARGET"', 'successfully intercepted a high-speed', B['ice']),
                                             ('— MINISTRY OF DEFENCE', 'The Defence Ministry said', B['steel']),
                                             ('"POSSESSED ONLY BY A HANDFUL OF NATIONS" — RAJNATH SINGH', 'possessed only by a handful of nations', B['cyan']))):
                q = cue(t, c, .2, .5)
                if q <= 0: continue
                for i, ln in enumerate(wrap(ctx, l, 28, 1700, 'bold', True)):
                    txt(ctx, ln, W/2, 640 + j*58 + i*34, 28, col, ease(q)*aa, 'bold', 'c', mono=True)
            for j, (l, c) in enumerate((('A BEGINNING, NOT A SYSTEM', 'a beginning, not a system'),
                                        ('YEARS OF TESTING BEFORE A SQUADRON STANDS ON ALERT', 'a squadron standing on alert'),
                                        ('INDUCTION: TOWARDS THE END OF THIS DECADE', 'towards the end of this decade'))):
                q = cue(t, c, .2, .5)
                if q <= 0: continue
                qa = ease(q)*a_out
                rgba(ctx, B['deep'], .9*qa); ctx.rectangle(0, 560 + j*0, W, 1)  # keeps the band subtle
                tagb(ctx, 110, 640 + j*74, l, B['alert'] if j == 0 else B['cyan'], qa, 26)
            q = cue(t, 'now it has flown one', .2, .5)
            if q > 0: tagb(ctx, W/2, 900, 'THE LAYER INDIA COULD NOT BUILD HAS NOW FLOWN', B['amber'], ease(q)*a_out, 32, align='c')
        ctx.restore()
    return scene(f)


# ================= ballistic is a different problem =================
def s_bmd(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'A COMPLETELY DIFFERENT PROBLEM', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=540)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tprog = Ts('India has a separate programme')
        prog = ease(seg(t, tprog - .4, tprog + .3)) if tprog < 900 else (1. if first > 0 else 0)
        if prog < 1:
            aa = (1 - prog)*a
            lp = ease(cue(t, 'An airliner travels at roughly nine hundred', .3, .6)) or (1. if first > 0 else 0)
            rp = ease(cue(t, 'doing several kilometres every second', .3, .6))
            splitspeed(ctx, t, aa, lp, rp)
            stroke_pts(ctx, [(960, 230), (960, 880)], fin(t, .3, .8), B['dim'], aa*.9, 2.5, glow=False)
            q = cue(t, 'You are not tracking it', .2, .5)
            if q > 0:
                qa = ease(q)*aa
                txt(ctx, 'YOU ARE NOT TRACKING IT', W/2, 300, 50, B['ice'], qa, 'black', 'c', glow=.6)
                q2 = cue(t, 'putting something there first', .2, .4)
                if q2 > 0: txt(ctx, 'YOU PREDICT WHERE IT WILL BE, AND GET THERE FIRST', W/2, 360, 32, B['amber'], ease(q2)*a_out, 'black', 'c')
        if prog > 0:
            aa = prog*a_out
            txt(ctx, 'BALLISTIC MISSILE DEFENCE', W/2, 260, 56, B['ice'], aa, 'black', 'c', glow=.6)
            txt(ctx, 'SANCTIONED IN 2000', W/2, 312, 26, B['cyan'], aa*ease(cue(t, 'sanctioned back in 2000', .2, .4)), 'bold', 'c', mono=True)
            for i, (ph, cls, note, c, col) in enumerate((('PHASE 1', 'UP TO THE 2,000 KM CLASS', 'TWO INTERCEPTORS + A LONG-RANGE TRACKING RADAR · TESTED AND DEPLOYED', 'two thousand kilometre class', B['cyan']),
                                                          ('PHASE 2', 'THE 5,000 KM CLASS', 'FLIGHT-TESTED FROM CHANDIPUR', 'five thousand kilometre class', B['amber']))):
                q = cue(t, c, .25, .6)
                if q <= 0: continue
                y = 420 + i*200; qa = ease(q)*aa
                card(ctx, 220, y, 1480, 170, qa, None, col, p=q)
                txt(ctx, ph, 270, y + 62, 40, col, qa, 'black')
                txt(ctx, cls, 560, y + 62, 36, B['ice'], qa, 'black')
                txt(ctx, note, 270, y + 118, 22, B['steel'], qa, 'bold', mono=True)
            q = cue(t, 'that is deliberate', .2, .5)
            if q > 0: tagb(ctx, W/2, 880, 'WHERE IT IS DEPLOYED IS NOT PUBLIC — DELIBERATELY', B['steel'], ease(q)*a_out, 28, align='c')
        ctx.restore()
    return scene(f)


# ================= the part nobody names =================
NET = [('IACCS', 'INDIAN AIR FORCE', 'a system called IACCS', 180), ('AKASHTEER', 'INDIAN ARMY', 'The Army runs Akashteer', 710), ('TRIGUN', 'INDIAN NAVY', 'The Navy runs TRIGUN', 1240)]
def s_net(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'THE PART NOBODY NAMES', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=540)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tnet = Ts('So India built a network')
        net = ease(seg(t, tnet - .4, tnet + .3)) if tnet < 900 else (1. if first > 0 else 0)
        if net < 1:
            aa = (1 - net)*a
            q = cue(t, 'the hard question in air defence', .25, .5)
            if q > 0: txt(ctx, 'THE HARD QUESTION', W/2, 270, 56, B['ice'], ease(q)*aa, 'black', 'c', glow=.6)
            for j, (l, c) in enumerate((('WHICH OF A DOZEN WEAPONS SHOULD FIRE?', 'which one should fire'),
                                        ('HAVE WE ALREADY SHOT AT IT TWICE?', 'have we already shot at it twice'),
                                        ('IS THAT AIRCRAFT OURS?', 'is that aircraft ours'))):
                q = cue(t, c, .2, .5)
                if q <= 0: continue
                for i, ln in enumerate(wrap(ctx, l, 44, 1600, 'black')):
                    txt(ctx, ln, W/2, 420 + j*110 + i*50, 44, B['ice'], ease(q)*aa, 'black', 'c')
            q = cue(t, 'You have seconds to answer', .2, .4)
            if q > 0:
                qa = ease(q)*aa
                txt(ctx, 'SECONDS TO ANSWER', W/2, 790, 60, B['alert'], qa, 'black', 'c', glow=.9)
        if net > 0:
            aa = net*a_out
            pts = []
            for i, (nm, sub, c, x) in enumerate(NET):
                q = cue(t, c, .25, .5)
                if q <= 0 and first > 1: q = 1.
                if q <= 0: continue
                qa = ease(min(q*1.6, 1))*aa
                netbox(ctx, x, 280, 500, 170, nm, sub, [B['cyan'], B['amber'], B['cyan']][i], qa, p=q)
                pts.append((x + 250, 450))
            sensor_grid(ctx, t, aa*.5, rows=2, cols=11, y0=760, step=52)
            if len(pts) > 1:
                lq = ease(cue(t, 'They connect', .2, .6)) or (1. if first > 1 else 0)
                for i in range(len(pts) - 1): link(ctx, pts[i], pts[i + 1], lq, B['cyan'], aa, 110)
            q = cue(t, 'one picture of the sky', .2, .5)
            if q > 0:
                qa = ease(q)*a_out
                sensor_grid(ctx, t, qa, rows=2, cols=11, y0=640, step=52)
                txt(ctx, 'ONE PICTURE OF THE SKY', W/2, 600, 38, B['ice'], qa, 'black', 'c', glow=.5)
            q = cue(t, 'The PIB describes Akashteer', .25, .5)
            if q > 0:
                qa = ease(q)*a_out
                rgba(ctx, B['deep'], .95*qa); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
                card(ctx, 180, 250, 1560, 400, qa, 'HOW THE PIB DESCRIBES AKASHTEER', B['amber'], p=q)
                for j, l in enumerate(('Fully indigenous, automated air defence', 'control and reporting system',
                                       'Vehicle-mounted, so it can move', 'Pulls in several kinds of radar',
                                       'Gives everyone a common real-time air picture')):
                    txt(ctx, l, 230, 370 + j*54, 32, B['ice'], qa*ease(seg(t, Ts('The PIB describes Akashteer') + .2 + j*.25, Ts('The PIB describes Akashteer') + .6 + j*.25)), 'bold')
            for j, (l, c, col) in enumerate((('STOPS TWO UNITS SHOOTING THE SAME DRONE', 'two units firing at the same drone', B['cyan']),
                                             ('WHILE A THIRD GOES UNENGAGED', 'a third goes unengaged', B['cyan']),
                                             ('AND REDUCES SHOOTING AT YOUR OWN AIRCRAFT', 'shooting at your own aircraft', B['cyan']))):
                q = cue(t, c, .2, .45)
                if q > 0: tagb(ctx, 110, 700 + j*70, l, col, ease(q)*a_out, 26)
            q = cue(t, 'A better network makes every engagement better', .25, .5)
            if q > 0:
                qa = ease(q)*a_out
                rgba(ctx, B['deep'], .96*qa); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
                txt(ctx, 'A BETTER MISSILE', W/2, 420, 46, B['steel'], qa, 'black', 'c')
                txt(ctx, 'MAKES ONE ENGAGEMENT BETTER', W/2, 480, 36, B['steel'], qa, 'bold', 'c', mono=True)
                txt(ctx, 'A BETTER NETWORK', W/2, 620, 62, B['amber'], qa, 'black', 'c', glow=1)
                txt(ctx, 'MAKES EVERY ENGAGEMENT BETTER', W/2, 690, 40, B['ice'], qa, 'bold', 'c', mono=True)
        ctx.restore()
    return scene(f)


# ================= Mission Sudarshan Chakra =================
def s_mis(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'MISSION SUDARSHAN CHAKRA', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=540)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        tprec = Ts('worth being precise on')
        prec = ease(seg(t, tprec - .4, tprec + .3)) if tprec < 900 else (1. if first > 0 else 0)
        if prec < 1:
            aa = (1 - prec)*a
            rampart(ctx, W/2, 880, .85, aa, p=fin(t, .2, 1.4))
            txt(ctx, '15 AUGUST 2025', W/2, 250, 68, B['amber'], aa*fin(t, .4, .6), 'black', 'c', glow=.8)
            q = cue(t, 'a national security shield to be built out and modernised by 2035', .25, .6)
            if q > 0:
                qa = ease(q)*aa
                txt(ctx, 'A NATIONAL SECURITY SHIELD BY 2035', W/2, 330, 44, B['ice'], qa, 'black', 'c')
                ring(ctx, W/2, 700, 740, min(q*1.4, 1), B['amber'], qa*.8, 3, None, 0, None, .30)
            for j, (l, c) in enumerate((('"MUST KEEP EXPANDING SO THAT EVERY CITIZEN FEELS SECURE"', 'must keep expanding'),
                                        ('"OUR TECHNOLOGY MUST PROVE SUPERIOR"', 'our technology must prove superior'))):
                q = cue(t, c, .2, .5)
                if q <= 0: continue
                for i, ln in enumerate(wrap(ctx, l, 28, 1700, 'bold', True)):
                    txt(ctx, ln, W/2, 420 + j*60 + i*34, 28, B['cyan'], ease(q)*aa, 'bold', 'c', mono=True)
        if prec > 0:
            aa = prec*a_out
            for i, (nm, sub, c, col) in enumerate((('DEFENSIVE AND OFFENSIVE', 'Not only stopping an attack, but answering it', 'both defensive and offensive', B['amber']),
                                                   ('CIVILIAN SITES TOO', 'Hospitals, railways, places of worship', 'cover civilian sites too', B['cyan']))):
                q = cue(t, c, .25, .5)
                if q <= 0: continue
                y = 300 + i*230; qa = ease(q)*aa
                card(ctx, 260, y, 1400, 190, qa, None, col, p=q)
                txt(ctx, f'0{i+1}', 310, y + 80, 48, col, qa, 'black')
                txt(ctx, nm, 420, y + 72, 44, B['ice'], qa, 'black')
                txt(ctx, sub, 420, y + 128, 26, B['steel'], qa, 'reg')
            q = cue(t, 'the details have not been published', .25, .5)
            if q > 0:
                qa = ease(q)*a_out
                txt(ctx, 'BEYOND THAT, NOTHING IS PUBLISHED', W/2, 830, 44, B['steel'], qa, 'black', 'c')
                q2 = cue(t, 'informed speculation, not announcement', .2, .4)
                if q2 > 0: tagb(ctx, W/2, 900, 'INFORMED SPECULATION, NOT ANNOUNCEMENT', B['alert'], ease(q2)*a_out, 30, align='c')
        ctx.restore()
    return scene(f)


# ================= the debate =================
def s_deb(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'WHERE PEOPLE DISAGREE', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        a = fin(t, .1, .5)*a_out if first == 0 else a_out
        if first == 0:
            txt(ctx, 'BOTH SIDES ARE WORTH HEARING', W/2, 150, 46, B['ice'], fin(t, .3, .7)*a_out*(1 - seg(t, 6, 8)), 'black', 'c', glow=.5)
        sides = [('THE CASE FOR', ['May 2025 showed layered', 'air defence works', 'A cheap drone attack', 'can be absorbed', 'So build more of it at home,',
                                   'where it cannot be switched off'], B['cyan'], 'The case for: May 2025 showed'),
                 ('THE CASE FOR CAUTION', ['A shield invites bigger salvos', 'The cheapest way past any defence', 'is to send more than it can handle',
                                           'Drones are cheap', 'Interceptors are not'], B['steel'], 'The case for caution')]
        for i, (head, lines, col, c) in enumerate(sides):
            tc = Ts(c)
            q = seg(t, tc - .2, tc + .6) if tc < 900 else (1. if first > 0 else 0)
            if q <= 0: continue
            x = 110 + i*860; qa = ease(q)*a_out
            card(ctx, x, 210, 820, 600, qa, head, col, p=q)
            for j, l in enumerate(lines):
                la = ease(seg(t, tc + .2 + j*.2, tc + .6 + j*.2))*a_out if tc < 900 else qa
                txt(ctx, l, x + 50, 350 + j*62, 30, B['ice'], la, 'bold' if j == 0 else 'reg')
        q = cue(t, 'can look destabilising to a neighbour', .3, .5)
        if q > 0:
            qa = ease(q)*a_out
            rgba(ctx, B['deep'], .94*qa); ctx.rectangle(0, 200, W, 700); ctx.fill()
            card(ctx, 240, 260, 1440, 400, qa, 'SOME ANALYSTS ADD', B['steel'], p=q)
            for j, l in enumerate(wrap(ctx, 'Visible defences can look destabilising to a neighbour, who may build more offence in response.', 40, 1340, 'bold')):
                txt(ctx, l, 290, 390 + j*54, 40, B['ice'], qa, 'bold')
        q = cue(t, 'what other people do next', .25, .5)
        if q > 0:
            qa = ease(q)*a_out
            rgba(ctx, B['deep'], .96*qa); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
            txt(ctx, 'NEITHER ARGUMENT IS ABOUT', W/2, 440, 42, B['steel'], qa, 'black', 'c')
            txt(ctx, 'WHETHER THE EQUIPMENT WORKS', W/2, 500, 42, B['steel'], qa, 'black', 'c')
            txt(ctx, 'THEY ARE ABOUT WHAT OTHER PEOPLE DO NEXT', W/2, 630, 50, B['amber'], qa, 'black', 'c', glow=.9)
        ctx.restore()
    return scene(f)


# ================= where it stands =================
STAT = [('S-400', 'CONTRACTED FOR FIVE SQUADRONS', 'BEHIND SCHEDULE', B['steel'], 'contracted for five squadrons'),
        ('PROJECT KUSHA', 'FIRST FLIGHT DONE', 'INDUCTION LATE THIS DECADE', B['amber'], 'first flight done'),
        ('AKASH · MR-SAM · QRSAM', 'THE INDIAN AND JOINT LAYERS', 'IN SERVICE', B['cyan'], 'MR-SAM, QRSAM: in service'),
        ('AKASHTEER', 'THE NETWORK', 'FIELDED', B['cyan'], 'Akashteer: fielded'),
        ('MISSION SUDARSHAN CHAKRA', 'A STATED GOAL WITH A DATE ON IT', 'BY 2035', B['amber'], 'a stated goal')]
def s_st(first):
    def f(ctx, t, D):
        bg(ctx); a_out = outro(t, D)
        hud(ctx, t, 'WHERE IT STANDS · 17 NOVEMBER 2026', a_out, EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=540)
        for i, (nm, note, status, col, c) in enumerate(STAT):
            tc = Ts(c)
            q = seg(t, tc - .2, tc + .5) if tc < 900 else (1. if first > 0 else 0)
            if q <= 0: continue
            statusrow(ctx, 160, 230 + i*144, 1600, nm, note, status, col, ease(q)*a_out, p=q)
        ctx.restore()
    return scene(f)


# ================= in three words =================
def s_three(ctx, t, D):
    bg(ctx); a_out = outro(t, D)
    hud(ctx, t, 'IN THREE WORDS', a_out, EP)
    txt(ctx, 'THE ORDER OF THE THREE JOBS IS THE ORDER OF DIFFICULTY', W/2, 220, 38, B['ice'], fin(t, .2, .8)*a_out, 'black', 'c', glow=.5)
    specs = [(r, [B['amber'], B['cyan'], B['cyan'], B['steel']][i], None, None, 1.) for i, (r, _, _) in enumerate(RSPEC)]
    rings(ctx, CX, 820, specs, t, a_out*.16, .28)
    words = [('SEE', 'THE HARDEST ONE', 'See.', 400), ('DECIDE', 'THE ONE THAT WINS NIGHTS', 'Decide.', 960), ('SHOOT', 'THE EASY PART', 'Shoot.', 1520)]
    for i, (w_, sub, c, x) in enumerate(words):
        q = cue(t, c, .15, .35)
        if q <= 0: continue
        sc = lerp(1.7, 1, eob(q, 1.4))
        ctx.save(); ctx.translate(x, 480); ctx.scale(sc, sc)
        txt(ctx, w_, 0, 0, 104, B['amber'], ease(min(q*2, 1))*a_out, 'black', 'c', glow=2)
        ctx.restore()
        for j, l in enumerate(wrap(ctx, sub, 22, 420, 'bold', True)):
            txt(ctx, l, x, 560 + j*32, 22, B['ice'], ease(cue(t, c, -.15, .4))*a_out, 'bold', 'c', mono=True)
    q = cue(t, 'The missile is the easy part', .2, .5)
    if q > 0: txt(ctx, 'THE MISSILE IS THE EASY PART', W/2, 740, 50, B['ice'], ease(q)*a_out, 'black', 'c', glow=.6)
scene(s_three)


# ================= the wall =================
def _wcard(ctx, x, y, w, h, a, label, col=None):
    col = col or B['cyan']
    fill(ctx, lambda: rrect(ctx, x, y, w, h, 8), B['deep'], .9*a)
    stroke_pts(ctx, rect_pts(x, y, w, h), 1, col, a, 2.5)
    missile(ctx, x + w/2, y + h*.42, w*.8, 0, a, col=col)
    txt(ctx, label, x + 22, y + h - 28, 22, B['ice'], a, 'black')
    glow_dot(ctx, x + w/2, y + 14, 6, B['amber'], a)
def s_wall(ctx, t, D):
    bg(ctx); a_out = outro(t, D, .8)
    hud(ctx, t, 'THE BLUEPRINT WALL', a_out, EP)
    for i in (4,):
        x = 160 + i*330
        stroke_pts(ctx, rect_pts(x, 200, 290, 240), 1, B['grid'], a_out, 2, glow=False, dash=[10, 10])
        txt(ctx, f'EP {i+1}', x + 145, 330, 24, B['grid'], a_out, 'bold', 'c', mono=True)
    _wcard(ctx, 160, 200, 290, 240, a_out*.8, 'EP 1 · PRALAY', B['steel'])
    _wcard(ctx, 490, 200, 290, 240, a_out*.8, 'EP 2 · BRAHMOS', B['steel'])
    _wcard(ctx, 820, 200, 290, 240, a_out*.8, 'EP 3 · AGNI-5', B['steel'])
    q = seg(t, .3, 1.0)
    y4 = lerp(-300, 200, eob(q, 1.3))
    fill(ctx, lambda: rrect(ctx, 1150, y4, 290, 240, 8), B['deep'], .9*a_out)
    stroke_pts(ctx, rect_pts(1150, y4, 290, 240), 1, B['amber'], a_out, 2.5)
    specs = [(r*.17, [B['amber'], B['cyan'], B['cyan'], B['steel']][i], None, None, 1.) for i, (r, _, _) in enumerate(RSPEC)]
    rings(ctx, 1295, y4 + 110, specs, t, a_out, .55)
    txt(ctx, 'EP 4 · THE SHIELD', 1172, y4 + 212, 22, B['ice'], a_out, 'black')
    glow_dot(ctx, 1295, y4 + 14, 6, B['amber'], a_out)
    for i, (l, c) in enumerate((('TWO THAT STRIKE', 'Two missiles that strike'), ('ONE THAT DETERS', 'one that deters'),
                                ('AND THE THING THAT STOPS THEM', 'the thing that stops all of them'))):
        q = cue(t, c, .2, .45)
        if q > 0: tagb(ctx, 200, 560 + i*72, l, B['cyan'], ease(q)*a_out, 26)
    tn = Ts('Next on')
    nq = seg(t, tn, tn + .6) if tn < 900 else 0
    if nq > 0:
        a = ease(nq)*a_out
        fill(ctx, lambda: ctx.rectangle(0, 830, W*eoc(nq), 90), B['deep'], .95*a)
        rgba(ctx, B['cyan'], a); ctx.rectangle(0, 830, W*eoc(nq), 3); ctx.fill()
        txt(ctx, 'NEXT  ·  TEJAS, AND WHY A FIGHTER JET TOOK FORTY YEARS', 80, 888, 32, B['ice'], a, 'bold', mono=True)
    subscribe_card(ctx, t, Ts('subscribe'), a_out, x=1540, y=640)
scene(s_wall)


# ================= beats =================
SC = {}
for i, k in enumerate(['cold1', 'cold2', 'cold3']): SC[k] = s_cold(i)
for i, k in enumerate(['job1', 'job2', 'job3']): SC[k] = s_job(i)
SC['qs1'] = s_qs
for i, k in enumerate(['have1', 'have2', 'have3']): SC[k] = s_have(i)
for i, k in enumerate(['s4001', 's4002', 's4003']): SC[k] = s_s400(i)
for i, k in enumerate(['buy1', 'buy2']): SC[k] = s_buy(i)
for i, k in enumerate(['kus1', 'kus2', 'kus3', 'kus4']): SC[k] = s_kus(i)
for i, k in enumerate(['bmd1', 'bmd2']): SC[k] = s_bmd(i)
for i, k in enumerate(['net1', 'net2', 'net3']): SC[k] = s_net(i)
for i, k in enumerate(['mis1', 'mis2']): SC[k] = s_mis(i)
for i, k in enumerate(['deb1', 'deb2', 'deb3']): SC[k] = s_deb(i)
for i, k in enumerate(['st1', 'st2']): SC[k] = s_st(i)
SC['three1'] = s_three
SC['end1'] = s_wall

BEATS = [(k, n, SC[k]) for k, n in EN]

GROUPS = {}
for g in ('cold', 'job', 'have', 's400', 'buy', 'kus', 'bmd', 'net', 'mis', 'deb', 'st'):
    for k, _ in EN:
        if k.startswith(g): GROUPS[k] = g

KEYS = {
 'job1': [('And then it has to shoot', 'SEE · DECIDE · SHOOT', 'amber')],
 'have3': [('forty years later', '40 YEARS LATER', 'cyan')],
 's4001': [('fifth of October 2018', '5 OCT 2018', 'amber')],
 's4003': [('the original schedule was 2023', 'SCHEDULE: 2023', 'alert')],
 'kus1': [('twenty-one thousand seven hundred crore rupees', '₹21,700 CRORE', 'amber')],
 'mis1': [('by 2035', 'BY 2035', 'amber')],
 'st2': [('not much else public', 'NOT MUCH ELSE PUBLIC', 'steel')],
}
ANNOT = {
 'job2': [('What you build is a set of rings', 'circle', CX, CY, 1600, 880)],
 'net3': [('A better network makes every engagement better', 'underline', 700, 720, 520, 0)],
}

_order = [k for k, _ in EN]
FX = [('whoosh', k, -.25, .22) for i, k in enumerate(_order) if i and GROUPS.get(k, k) != GROUPS.get(_order[i-1], _order[i-1])]
FX += [('beep', k, ph, .14) for k, items in KEYS.items() for ph, _, _ in items]
FX += [('tick', 'cold1', .15, .12), ('riser', 'cold2', 'It was a race against a clock', .3),
       ('glitch', 'cold3', 'Akashteer is not a missile', .25),
       ('ping', 'job2', 'What you build is a set of rings', .3),
       ('boom', 'job2', 'The outermost ring carries a long-range system', .35),
       ('ping', 'have1', 'The outer ring is the S-400', .25),
       ('stamp', 's4001', 'fifth of October 2018', .3),
       ('glitch', 's4003', 'deliveries ran late', .3),
       ('riser', 'kus3', 'Kusha flew for the first time', .2), ('boom', 'kus3', 'Kusha flew for the first time', .5),
       ('ping', 'bmd1', 'doing several kilometres every second', .3),
       ('boom', 'net1', 'You have seconds to answer', .25),
       ('stamp', 'mis1', 'fifteenth of August 2025', .3),
       ('riser', 'three1', 'See.', .12), ('ding', 'three1', 'See.', .22), ('ding', 'three1', 'Decide.', .22), ('ding', 'three1', 'Shoot.', .22),
       ('stamp', 'end1', .5, .35), ('ding', 'end1', 'subscribe', .2)]
