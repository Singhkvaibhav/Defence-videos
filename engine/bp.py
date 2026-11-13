"""Blueprint look for India's Defence, Decoded: navy blueprint paper, cyan and white line art that draws itself on,
HUD readouts, amber used only for the 'in three words' moment. Lines are drawn OVER the dark paper (no multiply)."""
import math, random, os, cairo
import numpy as np
from engine import core
from engine.core import W, H, seg, ease, eoc, eob, lerp, T

def hx(s): return tuple(int(s[i:i+2], 16)/255 for i in (0, 2, 4))
B = {k: hx(v) for k, v in dict(navy='0E2034', navy2='15304B', deep='0A1828', grid='24476A', cyan='7FD4F0', ice='EAF4FA',
                                dim='5F84A6', amber='F2B544', alert='E86A5C', steel='A9C3D6').items()}
_cache = {}

def rgba(ctx, c, a=1.): ctx.set_source_rgba(c[0], c[1], c[2], a)
def rrect(ctx, x, y, w, h, r): core.rrect(ctx, x, y, w, h, r)

# ---------- paper ----------
def _paper():
    if 'paper' in _cache: return _cache['paper']
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    g = cairo.RadialGradient(W*.45, H*.4, 100, W/2, H/2, 1300)
    g.add_color_stop_rgb(0, *B['navy2']); g.add_color_stop_rgb(1, *B['deep'])
    c.set_source(g); c.paint()
    c.set_line_width(1); rgba(c, B['grid'], .35)
    for x in range(0, W, 24): c.move_to(x + .5, 0); c.line_to(x + .5, H)
    for y in range(0, H, 24): c.move_to(0, y + .5); c.line_to(W, y + .5)
    c.stroke()
    c.set_line_width(1.5); rgba(c, B['grid'], .7)
    for x in range(0, W, 120): c.move_to(x + .5, 0); c.line_to(x + .5, H)
    for y in range(0, H, 120): c.move_to(0, y + .5); c.line_to(W, y + .5)
    c.stroke()
    # paper fibre noise
    rng = np.random.default_rng(3)
    n = (rng.normal(0, 1, (H//2, W//2))*14 + 128).clip(0, 255).astype(np.uint8)
    arr = np.dstack([n, n, n, np.full_like(n, 255)])
    ns = cairo.ImageSurface.create_for_data(bytearray(arr.tobytes()), cairo.FORMAT_ARGB32, W//2, H//2, (W//2)*4)
    c.save(); c.scale(2, 2); c.set_operator(cairo.OPERATOR_OVERLAY); c.set_source_surface(ns, 0, 0); c.paint_with_alpha(.18); c.restore()
    _cache['paper'] = s
    return s

def bg(ctx):
    ctx.set_source_surface(_paper(), 0, 0); ctx.paint()

# ---------- type ----------
def face(ctx, size, weight='reg', mono=False):
    if mono: ctx.select_font_face('DejaVu Sans Mono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if weight != 'reg' else cairo.FONT_WEIGHT_NORMAL)
    elif weight == 'black': ctx.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    else: ctx.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if weight == 'bold' else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def tw(ctx, s, size, weight='reg', mono=False):
    face(ctx, size, weight, mono); return ctx.text_extents(s).x_advance

def txt(ctx, s, x, y, size, col, a=1., weight='reg', align='l', mono=False, glow=0.):
    if a <= 0 or not s: return 0
    face(ctx, size, weight, mono); e = ctx.text_extents(s)
    xx = x - (e.x_advance/2 if align == 'c' else e.x_advance if align == 'r' else 0)
    if glow > 0:
        ctx.save(); ctx.move_to(xx, y); ctx.text_path(s); rgba(ctx, col, .18*a*glow); ctx.set_line_width(size*.18); ctx.stroke(); ctx.restore()
    ctx.move_to(xx, y); rgba(ctx, col, a); ctx.show_text(s)
    return e.x_advance

def typed(s, p): return s[:int(round(len(s)*max(0, min(1, p))))]

def wrap(ctx, s, size, maxw, weight='reg', mono=False):
    face(ctx, size, weight, mono); out, cur = [], ''
    for w_ in s.split():
        t_ = (cur + ' ' + w_).strip()
        if ctx.text_extents(t_).x_advance > maxw and cur: out.append(cur); cur = w_
        else: cur = t_
    if cur: out.append(cur)
    return out

def para(ctx, s, x, y, size, col, maxw, a=1., lh=1.32, weight='reg', align='l', mono=False):
    ls = wrap(ctx, s, size, maxw, weight, mono)
    for i, l in enumerate(ls): txt(ctx, l, x, y + i*size*lh, size, col, a, weight, align, mono)
    return len(ls)

# ---------- line art ----------
def stroke_pts(ctx, pts, p, col, a=1., w=3., glow=True, dash=None, closed=False):
    """draw a polyline progressively (0..1) with a soft glow"""
    if p <= 0 or a <= 0 or len(pts) < 2: return
    if closed: pts = list(pts) + [pts[0]]
    L = [0.]
    for i in range(1, len(pts)): L.append(L[-1] + math.hypot(pts[i][0]-pts[i-1][0], pts[i][1]-pts[i-1][1]))
    tot = L[-1]*min(p, 1)
    def path():
        ctx.new_path(); ctx.move_to(*pts[0])
        for i in range(1, len(pts)):
            if L[i] <= tot: ctx.line_to(*pts[i])
            else:
                f = (tot - L[i-1])/max(L[i] - L[i-1], 1e-6)
                ctx.line_to(lerp(pts[i-1][0], pts[i][0], f), lerp(pts[i-1][1], pts[i][1], f)); break
    ctx.save(); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    if dash: ctx.set_dash(dash)
    if glow:
        path(); rgba(ctx, col, .14*a); ctx.set_line_width(w*4); ctx.stroke()
    path(); rgba(ctx, col, a); ctx.set_line_width(w); ctx.stroke()
    ctx.restore()

def head_pt(pts, p):
    """the point reached at progress p along a polyline"""
    L = [0.]
    for i in range(1, len(pts)): L.append(L[-1] + math.hypot(pts[i][0]-pts[i-1][0], pts[i][1]-pts[i-1][1]))
    tot = L[-1]*max(0, min(p, 1))
    for i in range(1, len(pts)):
        if L[i] >= tot:
            f = (tot - L[i-1])/max(L[i] - L[i-1], 1e-6)
            return lerp(pts[i-1][0], pts[i][0], f), lerp(pts[i-1][1], pts[i][1], f), math.atan2(pts[i][1]-pts[i-1][1], pts[i][0]-pts[i-1][0])
    return pts[-1][0], pts[-1][1], 0.

def rect_pts(x, y, w, h): return [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]

def fill(ctx, path, col, a=1.):
    if a <= 0: return
    ctx.new_path(); path(); rgba(ctx, col, a); ctx.fill()

def glow_dot(ctx, x, y, r, col, a=1.):
    if a <= 0: return
    g = cairo.RadialGradient(x, y, 0, x, y, r*4)
    g.add_color_stop_rgba(0, col[0], col[1], col[2], .55*a); g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    ctx.set_source(g); ctx.arc(x, y, r*4, 0, 2*math.pi); ctx.fill()
    rgba(ctx, B['ice'], a); ctx.arc(x, y, r, 0, 2*math.pi); ctx.fill()

def bez(p0, p1, p2, n=60):
    return [((1-s)**2*p0[0] + 2*(1-s)*s*p1[0] + s*s*p2[0], (1-s)**2*p0[1] + 2*(1-s)*s*p1[1] + s*s*p2[1]) for s in [i/n for i in range(n + 1)]]

# ---------- props ----------
def missile(ctx, x, y, L, ang, a=1., p=1., col=None, fill_a=.12):
    """a generic, stylised missile outline (body, nose, fins), pointing along ang; not an engineering drawing"""
    col = col or B['ice']
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    r = L*.06
    body = [(-L/2, -r), (L*.32, -r), (L/2, 0), (L*.32, r), (-L/2, r), (-L/2, -r)]
    fill(ctx, lambda: [ctx.move_to(*body[0])] + [ctx.line_to(*q) for q in body[1:]], B['cyan'], fill_a*a*min(1, p*2))
    stroke_pts(ctx, body, p, col, a, 2.5)
    for sg in (-1, 1):
        fin = [(-L/2, sg*r), (-L/2 - L*.04, sg*r*2.6), (-L/2 + L*.14, sg*r), ]
        stroke_pts(ctx, fin, seg(p, .6, 1), col, a, 2.5)
    stroke_pts(ctx, [(L*.2, -r), (L*.2, r)], seg(p, .7, 1), col, a*.6, 1.5, glow=False)
    ctx.restore()

def truck(ctx, x, y, s, a, t, raise_=0., canister=True, wheels_spin=0.):
    """generic 8x8 launcher truck in line art; raise_ 0..1 tilts the canister upright"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    stroke_pts(ctx, rect_pts(-300, -70, 600, 60), 1, B['ice'], a, 3)            # chassis
    fill(ctx, lambda: rrect(ctx, -300, -70, 600, 60, 4), B['cyan'], .08*a)
    cab = [(200, -70), (200, -160), (260, -160), (300, -110), (300, -70)]
    stroke_pts(ctx, cab, 1, B['ice'], a, 3)
    fill(ctx, lambda: [ctx.move_to(*cab[0])] + [ctx.line_to(*q) for q in cab[1:]] + [ctx.close_path()], B['cyan'], .10*a)
    stroke_pts(ctx, [(215, -150), (255, -150), (285, -112), (215, -112), (215, -150)], 1, B['cyan'], a*.8, 2)
    for k in range(4):
        wx = -240 + k*95 + (60 if k >= 2 else 0)
        ctx.new_path(); rgba(ctx, B['ice'], a); ctx.set_line_width(3); ctx.arc(wx, 0, 34, 0, 2*math.pi); ctx.stroke()
        ang = wheels_spin
        for m in range(3):
            ctx.move_to(wx, 0); ctx.line_to(wx + 24*math.cos(ang + m*2.1), 24*math.sin(ang + m*2.1))
        rgba(ctx, B['dim'], a); ctx.set_line_width(2); ctx.stroke()
    if canister:
        ctx.save(); ctx.translate(-260, -86); ctx.rotate(-math.pi/2*ease(raise_))
        cv = rect_pts(0, -34, 440, 52)
        fill(ctx, lambda: rrect(ctx, 0, -34, 440, 52, 10), B['cyan'], .12*a)
        stroke_pts(ctx, cv, 1, B['ice'], a, 3)
        for k in range(1, 4): stroke_pts(ctx, [(k*110, -34), (k*110, 18)], 1, B['dim'], a, 1.5, glow=False)
        ctx.restore()
        # lift arm
        ax0, ay0 = -150, -80
        ax1, ay1 = -260 + 180*math.cos(-math.pi/2*ease(raise_)), -86 + 180*math.sin(-math.pi/2*ease(raise_))
        stroke_pts(ctx, [(ax0, ay0), (ax1, ay1)], 1, B['dim'], a, 4, glow=False)
    ctx.restore()

def figure(ctx, x, y, s, col, a, t, seed=0):
    """generic person in line art (no likeness)"""
    if a <= 0: return
    ctx.save(); ctx.translate(x, y + 2*math.sin(t*1.6 + seed)); ctx.scale(s, s)
    ctx.new_path(); rgba(ctx, col, a); ctx.set_line_width(3); ctx.arc(0, -110, 22, 0, 2*math.pi); ctx.stroke()
    stroke_pts(ctx, [(-34, 0), (-30, -70), (0, -84), (30, -70), (34, 0)], 1, col, a, 3)
    ctx.restore()

def radar(ctx, x, y, s, a, t, aim=-.6):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    stroke_pts(ctx, [(-40, 0), (0, -50), (40, 0)], 1, B['ice'], a, 3)
    ctx.save(); ctx.translate(0, -50); ctx.rotate(aim)
    stroke_pts(ctx, bez((-50, -20), (0, 30), (50, -20)), 1, B['ice'], a, 3)
    stroke_pts(ctx, [(0, 5), (0, -40)], 1, B['ice'], a, 2)
    ctx.restore()
    for k in range(3):
        ph = (t*.8 + k/3) % 1
        ctx.new_path(); rgba(ctx, B['cyan'], a*(1 - ph)*.7); ctx.set_line_width(2); ctx.arc(0, -50, 30 + 80*ph, -2.4 + aim*.5, -.8 + aim*.5); ctx.stroke()
    ctx.restore()

# ---------- HUD ----------
def hud(ctx, t, line, a=1., ep=1):
    if a <= 0: return
    rgba(ctx, B['cyan'], .7*a); ctx.rectangle(70, 104, W - 140, 2); ctx.fill()
    txt(ctx, typed(line, seg(t, .1, 1.1)), 70, 86, 22, B['ice'], .9*a, 'bold', mono=True)
    txt(ctx, f'DEFENCE · EP {ep}', W - 70, 86, 22, B['cyan'], .9*a, 'bold', 'r', mono=True)
    # corner brackets
    rgba(ctx, B['cyan'], .5*a); ctx.set_line_width(2)
    for (x, y, dx, dy) in ((40, 40, 1, 1), (W - 40, 40, -1, 1), (40, H - 40, 1, -1), (W - 40, H - 40, -1, -1)):
        ctx.move_to(x, y + dy*40); ctx.line_to(x, y); ctx.line_to(x + dx*40, y); ctx.stroke()

def card(ctx, x, y, w, h, a, title=None, col=None, p=1.):
    col = col or B['cyan']
    fill(ctx, lambda: rrect(ctx, x, y, w, h, 10), B['deep'], .78*a)
    stroke_pts(ctx, rect_pts(x, y, w, h), p, col, a, 2.5)
    if title:
        fill(ctx, lambda: ctx.rectangle(x, y, w*ease(p), 54), col, .18*a)
        txt(ctx, title, x + 22, y + 37, 24, col, a*ease(seg(p, .4, 1)), 'bold', mono=True)

def tagb(ctx, x, y, s, col, a, size=24, align='l'):
    if a <= 0: return
    w = tw(ctx, s, size, 'bold', True) + 30; h = size*1.7
    x0 = x - w/2 if align == 'c' else x - w if align == 'r' else x
    fill(ctx, lambda: rrect(ctx, x0, y - h/2, w, h, 6), B['deep'], .85*a)
    ctx.new_path(); rgba(ctx, col, a); ctx.set_line_width(2); rrect(ctx, x0, y - h/2, w, h, 6); ctx.stroke()
    txt(ctx, s, x0 + 15, y + size*.36, size, col, a, 'bold', mono=True)

def counter(v, fmt='{:.0f}'): return fmt.format(v)

def outro(t, D, k=.5): return 1 - ease(seg(t, D - k, D))

def camera(ctx, t, D, zoom=(1.0, 1.035), pan=(0, 0), cx=W/2, cy=H/2):
    p = ease(t/max(D, .01)) if D else 0
    z = lerp(zoom[0], zoom[1], p)
    ctx.translate(cx + pan[0]*p, cy + pan[1]*p); ctx.scale(z, z); ctx.translate(-cx, -cy)

# ---------- official map ----------
_MAP = {}
def india_map(ctx, cx, cy, h, a=1.):
    if a <= 0: return
    if 'img' not in _MAP:
        _MAP['img'] = cairo.ImageSurface.create_from_png(os.path.join(os.path.dirname(__file__), 'data', 'india_official_bp.png'))
    img = _MAP['img']; s = h/img.get_height()
    ctx.save(); ctx.translate(cx - img.get_width()*s/2, cy - h/2); ctx.scale(s, s)
    ctx.set_source_surface(img, 0, 0); ctx.paint_with_alpha(a); ctx.restore()

def map_point(cx, cy, h, px, py, src_w=1392, src_h=1760):
    s = h/src_h
    return cx - src_w*s/2 + px*s, cy - h/2 + py*s

# ---------- finishing layer ----------
_grain = []
def _grains():
    if _grain: return _grain
    rng = np.random.default_rng(11)
    for k in range(6):
        n = (rng.normal(0, 1, (H//2, W//2))*26 + 128).clip(0, 255).astype(np.uint8)
        arr = np.dstack([n, n, n, np.full_like(n, 255)])
        _grain.append(cairo.ImageSurface.create_for_data(bytearray(arr.tobytes()), cairo.FORMAT_ARGB32, W//2, H//2, (W//2)*4))
    return _grain

def sticker(ctx, label, col, t, t0, life=2.8):
    p_in = seg(t, t0, t0 + .4); p_out = seg(t, t0 + life, t0 + life + .3)
    if p_in <= 0 or p_out >= 1: return
    a = ease(p_in*2)*(1 - p_out); s = eob(p_in, 2)*(1 - .2*eoc(p_out))
    face(ctx, 40, 'black'); w = ctx.text_extents(label).x_advance + 60; h = 74
    x, y = W - 90 - w/2, 880
    ctx.save(); ctx.translate(x, y); ctx.scale(max(s, .01), max(s, .01))
    fill(ctx, lambda: rrect(ctx, -w/2, -h/2, w, h, 6), B['deep'], .9*a)
    stroke_pts(ctx, rect_pts(-w/2, -h/2, w, h), 1, col, a, 3)
    # scan line sweep
    sx = -w/2 + w*((t - t0)*1.3 % 1)
    rgba(ctx, col, .25*a); ctx.rectangle(sx, -h/2, 6, h); ctx.fill()
    txt(ctx, label, 0, 14, 40, col, a, 'black', 'c', glow=1)
    ctx.restore()

def marker(ctx, kind, x, y, w, h, p, a=1., seed=0):
    if p <= 0 or a <= 0: return
    if kind == 'circle':
        pts = [(x + w/2*1.04*math.cos(-1.9 + 2*math.pi*1.06*i/60), y + h/2*math.sin(-1.9 + 2*math.pi*1.06*i/60)) for i in range(61)]
    elif kind == 'underline':
        pts = [(x + w*i/20, y + 2*math.sin(i*.9 + seed)) for i in range(21)]
    else:
        pts = bez((x, y), (x + w*.5 + h*.3, y + h*.5 - w*.3), (x + w, y + h))
    stroke_pts(ctx, pts, p, B['amber'] if kind != 'underline' else B['cyan'], a, 6)

def _wipe(ctx, p, out):
    """a blueprint scan: a bright line sweeps across, drawing a grid panel behind it"""
    e = lerp(-100, W + 100, eoc(p) if out else ease(p))
    ctx.save()
    if out: ctx.rectangle(0, 0, e, H)
    else: ctx.rectangle(e, 0, W - e, H)
    rgba(ctx, B['deep']); ctx.fill()
    rgba(ctx, B['cyan'], .9); ctx.rectangle(e - 3, 0, 6, H); ctx.fill()
    g = cairo.LinearGradient(e - 120, 0, e, 0); g.add_color_stop_rgba(0, B['cyan'][0], B['cyan'][1], B['cyan'][2], 0); g.add_color_stop_rgba(1, B['cyan'][0], B['cyan'][1], B['cyan'][2], .3)
    ctx.set_source(g); ctx.rectangle(e - 120, 0, 120, H); ctx.fill()
    ctx.restore()

def make_post(groups, keys, annots=None):
    annots = annots or {}
    def group(k): return groups.get(k, k)
    def post(ctx, b, t, tl):
        core.BEAT = b; D = b['D']; i = b['i']
        for j, (phrase, kind, x, y, w, h) in enumerate(annots.get(b['k'], [])):
            t0 = T(phrase); marker(ctx, kind, x, y, w, h, seg(t, t0, t0 + .55), 1 - ease(seg(t, D - .5, D - .2)), seed=j)
        for phrase, label, col in keys.get(b['k'], []):
            sticker(ctx, label, B[col], t, T(phrase) - .05)
        # slow moving light + vignette
        lx = W*(.3 + .4*math.sin((b['start'] + t)*.05)); ly = H*.2
        g = cairo.RadialGradient(lx, ly, 50, lx, ly, 1100)
        g.add_color_stop_rgba(0, .6, .85, 1, .07); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.save(); ctx.set_operator(cairo.OPERATOR_SCREEN); ctx.set_source(g); ctx.paint(); ctx.restore()
        v = cairo.RadialGradient(W/2, H/2, 500, W/2, H/2, 1250)
        v.add_color_stop_rgba(0, 0, 0, 0, 0); v.add_color_stop_rgba(1, 0, 0, .02, .45)
        ctx.save(); ctx.set_source(v); ctx.paint(); ctx.restore()
        gs = _grains()[int((b['start'] + t)*30) % 6]
        ctx.save(); ctx.scale(2, 2); ctx.set_operator(cairo.OPERATOR_OVERLAY); ctx.set_source_surface(gs, 0, 0); ctx.paint_with_alpha(.08); ctx.restore()
        TD = .34
        if i + 1 < len(tl) and group(tl[i+1]['k']) != group(b['k']) and t > D - TD: _wipe(ctx, seg(t, D - TD, D), True)
        if i > 0 and group(tl[i-1]['k']) != group(b['k']) and t < TD: _wipe(ctx, seg(t, 0, TD), False)
    return post

def scene(f, bgname='bp'):
    f.bg = bgname
    return f

def subscribe_card(ctx, t, t0, a_out=1., x=1540, y=720):
    q = seg(t, t0, t0 + .5)
    if q <= 0: return
    s = eob(q, 1.8); a = ease(q*2)*a_out
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    fill(ctx, lambda: rrect(ctx, -240, -64, 480, 128, 10), B['deep'], .92*a)
    stroke_pts(ctx, rect_pts(-240, -64, 480, 128), 1, B['cyan'], a, 3)
    ctx.save(); ctx.translate(-178, 0); ctx.rotate(.2*math.sin((t - t0)*9)*max(0, 1 - (t - t0)/1.5))
    stroke_pts(ctx, bez((-22, 18), (0, -60), (22, 18)) + [(-22, 18)], 1, B['ice'], a, 3)
    ctx.new_path(); rgba(ctx, B['ice'], a); ctx.arc(0, 26, 6, 0, 2*math.pi); ctx.fill(); ctx.restore()
    txt(ctx, 'SUBSCRIBE', -128, -4, 42, B['ice'], a, 'black')
    txt(ctx, 'GyaanXstudios', -128, 38, 24, B['cyan'], a, 'bold', mono=True)
    ctx.restore()
