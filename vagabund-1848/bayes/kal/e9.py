"""E-9a/b/c nach Protokoll vom 17.10.2026."""
import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py
import re, json, collections, numpy as np, prep, calib
from calib import cdist, auc, wilson, rate
LAYER='ang'; SIZE=548
CAND_H=str(pfade.KANDIDAT)
import sys; sys.path.insert(0,'../norm'); import angleichen as A
# ---------- Normalisierung für Paare (wie E-8)
STOP=set('der die das den dem des ein eine einen einem einer eines und oder aber doch so wie als da dann wenn wo was wer ich du er sie es wir ihr mich dich sich mir dir ihm ihn ihr uns euch mein meine meinen meinem meiner dein deine deinen deinem sein seine seinen seinem seiner ihre ihren ihrem ist bin bist sind war hat habe hab hast haben wird will kann mag in im an am auf aus bei mit nach von vor zu zum zur über unter um durch für nicht nur noch schon auch gar wol wohl ja nein o ach nun dort hier da dies diese dieser jener all alle'.split())
def nz(w):
    w=w.replace('ſ','s').lower().replace('ß','ss').replace("'",'').replace('’','').replace('th','t').replace('ey','ei')
    w=w.replace('ä','ae').replace('ö','oe').replace('ü','ue'); w=re.sub(r'[^a-z]','',w)
    return re.sub(r'(en|em|er|es|e|n|s)$','',w) if len(w)>4 else w
def line_pairs(line):
    toks=line.split(); c=[(i,nz(t)) for i,t in enumerate(toks) if nz(t) and nz(t) not in STOP and len(nz(t))>2 and re.sub(r'\W','',t.lower()) not in STOP]
    return [((c[k][0],c[k+1][0]),c[k][1]+' '+c[k+1][1]) for k in range(len(c)-1)]
def text_pairs(text):
    s=set()
    for l in prep.clean(text).split('\n'):
        for _,p in line_pairs(l): s.add(p)
    return s
# A1 Paare je Gedicht
POEMS=prep.bdl_poems(LAYER)
A1P={f'{s} {n}':text_pairs(t) for s,n,t in POEMS}
ALLA1=set().union(*A1P.values())
def a1_pairs_without(excl):
    return set().union(*[v for k,v in A1P.items() if k not in excl])
def masked_tokens(text,label,pairset):
    """Token-Strom wie prep.toks, mit Maskenflag (Reimwort oder Heine-Formel)."""
    out=[]
    for l in prep.clean(text).split('\n'):
        toks=l.split()
        if not toks: continue
        m=[False]*len(toks)
        if any(re.search(r'[^\W\d_]',t) for t in toks):
            j=max(i for i,t in enumerate(toks) if re.search(r'[^\W\d_]',t)); m[j]=True   # Reimwort
        for (i,k),p in line_pairs(l):
            if p in pairset: m[i]=m[k]=True
        out+=[(t,label,mm) for t,mm in zip(toks,m)]
    return out
mapping=prep.a2_mapping()
pool=set(prep.decoy_pool())
def strip(stream,cls):
    n548=len(stream)//548; keep=[]
    for i in range(n548+1):
        if (cls,i) in pool: continue
        keep+=stream[i*548:(i+1)*548]
    return keep
def blocks(st): return [st[i*SIZE:(i+1)*SIZE] for i in range(len(st)//SIZE)]
# Ströme mit Masken
def cls_stream(cls):
    out=[]
    for n in prep.CLASSES[cls]:
        out+=masked_tokens(open(prep.kf(LAYER,n),encoding='utf-8').read(),n,ALLA1)
    return out
a2=[]
for pid,t in prep.a2_poems(LAYER): a2+=[(w,pid,False) for w in prep.toks(t)]  # Masken für A2 später je Block
D={}
D['A2']=blocks(strip(a2,'A2'))
for c in ['B1','B2','C2','C3']: D[c]=blocks(strip(cls_stream(c),c))
D['A1L']=blocks([(w,f'{s} {n}',False) for s,n,t in POEMS if s in prep.LIED for w in prep.toks(t)])
D['A1N']=blocks([(w,f'{s} {n}',False) for s,n,t in POEMS if s in prep.NORD for w in prep.toks(t)])
# A2-Masken je Block (Formelpaare aus A1 ohne die entsprechenden Gedichte)
a2text={pid:t for pid,t in prep.a2_poems(LAYER)}
def a2_block_masked(b):
    pids=[]; [pids.append(p) for _,p,_ in b if p not in pids]
    ov={mapping.get(p,'') for p in pids}-{''}
    ps=a1_pairs_without(ov)
    full=[]
    for p in pids: full+=masked_tokens(a2text[p],p,ps)
    # an Blockgrenzen ausrichten: gleiche Tokenfolge, Masken übernehmen
    seq=[w for w,_,_ in b]; i=0; out=[]
    flat=full
    # suche Startposition
    for st in range(len(flat)):
        if [x[0] for x in flat[st:st+5]]==seq[:5]: i=st;break
    return flat[i:i+len(b)]
def fe(kind,mask=False):
    """Merkmalsfunktion wie calib.featurize (Vokabular und z aus Trainingsblöcken ohne Maske)."""
    f=calib.words if kind=='w' else calib.chars
    train=[b for c in ['A1L','A1N','A2','B1','B2','C2','C3'] for b in D[c]]
    conv=lambda b:[(w,l) for w,l,mm in b if not (mask and mm)]
    tot=collections.Counter()
    for b in train: tot.update(f([(w,l) for w,l,_ in b]))
    vocab=[k for k,_ in tot.most_common(150)]; idx={k:i for i,k in enumerate(vocab)}
    def vec(bb):
        c=collections.Counter(f(bb)); n=sum(c.values()) or 1; v=np.zeros(len(vocab))
        for k,x in c.items():
            if k in idx: v[idx[k]]=x/n
        return v
    M=np.array([vec([(w,l) for w,l,_ in b]) for b in train]); mu=M.mean(0); sd=M.std(0); sd[sd==0]=1
    Zref=lambda b:(vec([(w,l) for w,l,_ in b])-mu)/sd       # Referenzen ungemasked
    Ztest=lambda b:(vec(conv(b))-mu)/sd                      # geprüfter Text ggf. gemasked
    return Zref,Ztest
def a1_minus(Zref,ov):
    st=[(w,f'{s} {n}',False) for s,n,t in POEMS if s in prep.LIED and f'{s} {n}' not in ov for w in prep.toks(t)]
    return np.array([Zref(b) for b in blocks(st)])
def run(kind,mask,worklevel):
    Zref,Ztest=fe(kind,mask)
    A1=np.array([Zref(b) for b in D['A1L']])
    classes={'H':D['B1']+D['B2'],'G':D['C2'],'M':D['C3']}
    R={k:np.array([Zref(b) for b in v]) for k,v in classes.items()}
    work={k:[b[0][1] for b in v] for k,v in classes.items()}
    def summ(pos,neg):
        p,n=np.array(pos),np.array(neg); h,f=(p>0).sum(),(n>0).sum(); hl,_=wilson(h,len(p)); _,fh=wilson(f,len(n))
        return dict(auc=round(auc(p,n),3),treffer=f'{h}/{len(p)}',fehlalarm=f'{f}/{len(n)}',LR_nah=round(rate(h,len(p))/rate(f,len(n)),2),LR_nah_min95=round(hl/max(fh,1e-9),2),LR_fern=round((1-rate(h,len(p)))/(1-rate(f,len(n))),2))
    pos={'H':[],'G':[]}
    for b in D['A2']:
        pids={p for _,p,_ in b}; ov={mapping.get(p,'') for p in pids}-{''}
        ref=a1_minus(Zref,ov|{o.rstrip('.')+'.' for o in ov})
        bb=a2_block_masked(b) if mask else b
        x=Ztest(bb)
        for c in pos: pos[c].append(float(np.median(cdist(x,R[c]))-np.median(cdist(x,ref))))
    def neg_closed(c):
        out=[]
        for i,b in enumerate(classes[c]):
            if worklevel: keep=[j for j in range(len(classes[c])) if work[c][j]!=work[c][i]]
            else: keep=[j for j in range(len(classes[c])) if abs(j-i)>1]
            if not keep: continue
            x=Ztest(b); out.append(float(np.median(cdist(x,R[c][keep]))-np.median(cdist(x,A1))))
        return out
    res={'H1:H2 geschlossen (Hektor)':summ(pos['H'],neg_closed('H')),
         'H1:H3 geschlossen (Geibel)':summ(pos['G'],neg_closed('G')),
         'H1:H3 offen (Müller/Wh)':summ(pos['G'],[float(np.median(cdist(Ztest(b),R['G']))-np.median(cdist(Ztest(b),A1))) for b in classes['M']])}
    # Kandidat
    K=masked_tokens(open(CAND_H,encoding='utf-8').read() if False else A.angleichen(open(CAND_H,encoding='utf-8').read()),'K',ALLA1)
    x=Ztest(K)
    res['Kandidat']=dict(s_H2=round(float(np.median(cdist(x,R['H']))-np.median(cdist(x,A1))),3), s_H3=round(float(np.median(cdist(x,R['G']))-np.median(cdist(x,A1))),3),
                         maskiert=f"{sum(m for _,_,m in K)}/{len(K)}" if mask else '-')
    return res
OUT={}
for kind in ['w','c']:
    for mask,wl,lab in [(False,False,'Basis (Nachbarausschluss)'),(False,True,'E-9b Werkebene'),(True,True,'E-9a maskiert, Werkebene')]:
        OUT[f'{kind} {lab}']=run(kind,mask,wl); print(kind,lab,json.dumps(OUT[f'{kind} {lab}'],ensure_ascii=False))
json.dump(OUT,open('e9ab.json','w'),ensure_ascii=False,indent=1)
