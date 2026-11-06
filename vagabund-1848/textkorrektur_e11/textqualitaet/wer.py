import re,glob,os,difflib,json,math,collections
def tok(t):
    t=t.replace('ſ','s')
    w=re.findall(r"[^\W\d_]+(?:'[^\W\d_]*)?|\S*\d\S*",t)
    w=[x.replace("'","") for x in w]
    return [x.lower() for x in w if not re.fullmatch(r"[ivxlc]+",x.lower())]
res=collections.defaultdict(lambda:[0,0,[]])
for f in sorted(glob.glob('ref/*.txt')):
    n=os.path.basename(f)[:-4]; text=n.rsplit('_',1)[0]
    r=tok(open(f).read()); o=tok(open('ocrseiten/'+n+'.txt').read())
    sm=difflib.SequenceMatcher(None,r,o,autojunk=False); err=0; bsp=[]
    for op,a1,a2,b1,b2 in sm.get_opcodes():
        if op!='equal':
            err+=max(a2-a1,b2-b1); bsp.append((' '.join(r[a1:a2]),' '.join(o[b1:b2])))
    res[text][0]+=err; res[text][1]+=len(r); res[text][2]+=bsp
    print(f"{n:24s} Wörter {len(r):4d} Fehler {err:2d}  {bsp}")
print()
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return (c-h)/d,(c+h)/d
K=N=0
for t,(e,n,_) in res.items():
    lo,hi=wilson(e,n); K+=e;N+=n
    print(f"{t:18s} {e:3d}/{n:4d} = {100*e/n:4.1f} %  (95 %-Bereich {100*lo:.1f}–{100*hi:.1f} %)")
lo,hi=wilson(K,N); print(f"{'gesamt':18s} {K:3d}/{N:4d} = {100*K/N:4.1f} %  ({100*lo:.1f}–{100*hi:.1f} %)")
json.dump({t:{'fehler':v[0],'woerter':v[1],'beispiele':v[2]} for t,v in res.items()},open('wer_e11.json','w'),ensure_ascii=False,indent=1)
