import importlib.util, os, sys, cairo
ROOT='/home/claude/defence-videos'; sys.path.insert(0, ROOT)
spec=importlib.util.spec_from_file_location('ep','ep.py'); ep=importlib.util.module_from_spec(spec); spec.loader.exec_module(ep)
from engine import core
core.TOTAL=float(ep.TOTAL)
from engine.core import W,H
from engine.runner import Episode
beats=[(k,n) for k,n,_ in ep.BEATS]; scenes={k:f for k,_,f in ep.BEATS}; bg={k:f.bg for k,_,f in ep.BEATS}
extra=dict(hook=1.5,tip=3.0,end=3.5); extra.update(getattr(ep,'EXTRA',{}))
import importlib as _il; mp=_il.import_module(ep.POST).make_post
post=mp(ep.GROUPS, ep.KEYS, ep.ANNOT)
E=Episode(ep.EP,os.getcwd(),beats,{},scenes,bg,extra,nocap=tuple(scenes),chunk_caps=True,post=post)
tl=E.timeline()
os.makedirs('scan',exist_ok=True)
STEP=11.0
t=2.0; n=0
while t < core.TOTAL-1:
    b=[x for x in tl if x['start']<=t<x['start']+x['D']]
    if b:
        b=b[0]; lt=t-b['start']
        surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); ctx=cairo.Context(surf)
        E.frame(ctx,b,lt,bg[b['k']],bg[b['k']])
        surf.write_to_png(f'scan/{n:03d}_{b["k"]}_{int(t)}.png'); n+=1
    t+=STEP
print(n)
