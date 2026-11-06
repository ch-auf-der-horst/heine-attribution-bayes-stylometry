import json,re,collections,numpy as np,random
D=json.load(open('AuthorshipAttribution/corpus_diplomatisch/e5/dta_prosa_e5.json'))
D={k:v for k,v in D.items() if not v.startswith('ERR')}
EY=r'\b(b|s|fr|dr|zw|dab|vorb|herb|einerl|allerl)ey(n|d|ns)?\b'
def norm(t):
    t=t.replace('ſ','s').replace('¬ ','').replace('¬','').lower().replace('ß','ss')
    t=re.sub(EY,lambda m:m.group(1)+'ei'+(m.group(2) or ''),t)
    return re.findall(r"[a-zäöüé]+",t)
H=norm(open('H.txt').read()); F=norm(open('F.txt').read())
A={k:norm(v) for k,v in D.items()}
NP=len(H); NC=len(F)
def mfw(texts,n):
    c=collections.Counter(); [c.update(t) for t in texts]; return [w for w,_ in c.most_common(n)]
def chars(tok): s=' '.join(tok); return [s[i:i+4] for i in range(len(s)-3)]
def vec(tok,feat,mode):
    units=tok if mode=='w' else chars(tok)
    c=collections.Counter(units); n=max(1,len(units)); return np.array([c[f]/n for f in feat])
def run(mode,nfeat,seed=0):
    rng=random.Random(seed)
    # profiles: first NP words; chunks from rest
    prof={k:v[:NP] for k,v in A.items()}
    chunks={k:[v[NP+i*NC:NP+(i+1)*NC] for i in range(5) if len(v)>=NP+(i+1)*NC] for k,v in A.items()}
    pool=list(prof.values())+[H]
    feat=mfw(pool,nfeat) if mode=='w' else mfw([chars(t) for t in pool],nfeat)
    def zstack(profiles):
        M=np.array([vec(p,feat,mode) for p in profiles]); mu=M.mean(0); sd=M.std(0)+1e-9; return mu,sd
    def cos(a,b): return 1-np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-12)
    def score(unknown,hprof,others):
        profs=[hprof]+others; mu,sd=zstack(profs)
        u=(vec(unknown,feat,mode)-mu)/sd
        d=[cos(u,(vec(p,feat,mode)-mu)/sd) for p in profs]
        return np.mean([d[0]<x for x in d[1:]])
    pos=[]
    hch=[H[i*NC:(i+1)*NC] for i in range(NP//NC)]
    for i,ch in enumerate(hch):
        rest=[w for j,c in enumerate(hch) if j!=i for w in c]+H[(NP//NC)*NC:]
        pos.append(score(ch,rest,[v[:len(rest)] for v in prof.values()]))
    neg=[]
    for k,chs in chunks.items():
        others=[v for kk,v in prof.items() if kk!=k]
        for ch in chs: neg.append(score(ch,H,others))
    pos=np.array(pos);neg=np.array(neg)
    auc=np.mean([(p>n)+0.5*(p==n) for p in pos for n in neg])
    f=score(F,H,list(prof.values()))
    return auc,pos,neg,f
for mode,n in [('w',100),('c',200)]:
    auc,pos,neg,f=run(mode,n)
    thr=sorted(set(list(pos)+list(neg)))
    print(mode,n,'AUC=%.2f'%auc,'pos',np.round(pos,2),'neg mean %.2f'%neg.mean(),'neg>=0.9: %d/%d'%((neg>=0.9).sum(),len(neg)),'F score=%.2f'%f)
    # where does F rank: fraction of negatives with score>=f, positives with score>=f
    print('   P(neg>=F)=%.2f  P(pos>=F)=%.2f'%((neg>=f).mean(),(pos>=f).mean()))
print(len(H),len(F),sorted(A))

def nearest(mode,n):
    prof={k:v[:NP] for k,v in A.items()}; prof['HEKTOR']=H
    pool=list(prof.values()); feat=mfw(pool,n) if mode=='w' else mfw([chars(t) for t in pool],n)
    M={k:vec(p,feat,mode) for k,p in prof.items()}; X=np.array(list(M.values())); mu=X.mean(0); sd=X.std(0)+1e-9
    u=(vec(F,feat,mode)-mu)/sd
    d={k:1-np.dot(u,(v-mu)/sd)/(np.linalg.norm(u)*np.linalg.norm((v-mu)/sd)) for k,v in M.items()}
    return sorted(d.items(),key=lambda x:x[1])
for mode,n in [('w',100),('c',200)]:
    r=nearest(mode,n); print(mode,[ (k[:22],round(v,2)) for k,v in r])
