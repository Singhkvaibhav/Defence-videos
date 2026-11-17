import re, io
t = open('../../scripts/ep04_air_defence.md', encoding='utf-8').read()
en_tbl = re.search(r'### Long video(.*?)#### Hindi', t, re.S).group(1)
hi_tbl = re.search(r'#### Hindi narration \(हिंदी\)(.*?)### Sources', t, re.S).group(1)
def rows(tbl, col):
    out = []
    for r in tbl.split('\n'):
        if not r.strip().startswith('|'): continue
        c = [x.strip() for x in r.strip().strip('|').split('|')]
        if not c or c[0].startswith('---') or c[0] == 'Time': continue
        out.append(c[col])
    return out
EN_ROWS = rows(en_tbl, 3); HI_ROWS = rows(hi_tbl, 1)
assert len(EN_ROWS) == len(HI_ROWS) == 14, (len(EN_ROWS), len(HI_ROWS))

SPLIT = [['cold1','cold2','cold3'], ['job1','job2','job3'], ['qs1'], ['have1','have2','have3'],
         ['s4001','s4002','s4003'], ['buy1','buy2'], ['kus1','kus2','kus3','kus4'],
         ['bmd1','bmd2'], ['net1','net2','net3'], ['mis1','mis2'],
         ['deb1','deb2','deb3'], ['st1','st2'], ['three1'], ['end1']]
assert len(SPLIT) == 14

def partition(parts, n):
    """split `parts` into exactly n non-empty contiguous groups, balanced by length"""
    assert len(parts) >= n, (len(parts), n)
    cum = []; a = 0
    for p in parts: a += len(p); cum.append(a)
    total = a
    cuts = []           # index of last part in each of the first n-1 groups
    for i in range(1, n):
        target = total*i/n
        lo = i - 1                       # leave i-1 parts behind
        hi = len(parts) - (n - i) - 1    # leave n-i parts ahead
        lo = max(lo, (cuts[-1] + 1) if cuts else 0)
        best = min(range(lo, hi + 1), key=lambda j: abs(cum[j] - target))
        cuts.append(best)
    groups = []; start = 0
    for c in cuts + [len(parts) - 1]:
        groups.append(parts[start:c + 1]); start = c + 1
    assert len(groups) == n and all(groups), [len(g) for g in groups]
    return groups

EN = []; HI = []
for keys, e, h in zip(SPLIT, EN_ROWS, HI_ROWS):
    n = len(keys)
    if n == 1:
        EN.append((keys[0], e)); HI.append((keys[0], h)); continue
    ep = re.split(r'(?<=[.!?]) +', e); hp = re.split(r'(?<=[।!?]) +', h)
    for k, g in zip(keys, partition(ep, n)): EN.append((k, ' '.join(g)))
    for k, g in zip(keys, partition(hp, n)): HI.append((k, ' '.join(g)))

# word-for-word check against the approved script
assert ' '.join(x[1] for x in EN) == ' '.join(EN_ROWS), 'EN text changed'
assert ' '.join(x[1] for x in HI) == ' '.join(HI_ROWS), 'HI text changed'
assert [k for k, _ in EN] == [k for k, _ in HI]

with io.open('text.py', 'w', encoding='utf-8') as f:
    f.write('# generated from scripts/ep04_air_defence.md — approved narration, word for word\n')
    f.write('EN = [\n')
    for k, v in EN: f.write(f' ({k!r}, {v!r}),\n')
    f.write(']\n\nHI = {\n')
    for k, v in HI: f.write(f' {k!r}: {v!r},\n')
    f.write('}\n')
print(len(EN), 'beats; longest EN', max(len(v.split()) for _, v in EN), 'words')
for k, v in EN: print(' ', k, len(v.split()))
