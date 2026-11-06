import json,re,glob,collections,random
S='arbeit/'
U8='AuthorshipAttribution/corpus_diplomatisch/'
pages=json.load(open('pages.json')); pages={int(k):v for k,v in pages.items()}
SIG=r'(?:D\d(?:h\d?)?(?:-\d)?(?:,\d)*|J{1,2}I{0,3}\d?|JI{1,3}|GH|G|H\d?(?:-\d)?|h|RI{1,2}\d?H?(?:-\d)?|RII\d|I|E\d?|Text|dSt|St|Shs)'
GRP=re.compile(rf'(?<![A-Za-zäöüß]){SIG}(?:\s*\(Korr\.\))?(?:\s*,\s*{SIG}(?:\s*\(Korr\.\))?)*(?=\s|$|\n)')
GENH=re.compile(r'(?<![A-Za-z])(H\d?(?:-\d)?|h)(?![A-Za-z(])')
def genuine(g):
    g2=g.replace('RI1H','').replace('GH',''); g2=re.sub(r'D\dh\d?','',g2); g2=re.sub(r'H\d?(?:-\d)?\s*\(Korr\.\)','',g2)
    return bool(GENH.search(g2))
def split_app(text):
    U,P=[],[]; pos=0
    for g in GRP.finditer(text):
        seg=text[pos:g.start()]; pos=g.end()
        seg=seg.split(']')[-1]
        seg=re.sub(r'\(\d\)|\([a-z]\d?\)|/:|:/|°','',seg)
        (U if genuine(g.group(0)) else P).append(seg)
    return U,P
# DHA I apparatus
L1=open(S+'dha/lesarten.txt').read()
U1,P1=split_app(L1)
# DHA II: only Lesarten parts
app=''
for p in range(300,387):
    app+=pages.get(p,'')+'\n'
app+='\n'.join(pages.get(p,'') for p in range(854,858))
les=[]
for m in re.finditer(r'Lesarten\s*\n(.*?)(?=\n\s*Erläuterungen|\n\s*Entstehung|\Z)',app,re.S): les.append(m.group(1))
U2,P2=split_app('\n'.join(les))
# unpublished poem texts p.178 (zeitgen. nicht gedruckt) -> U ; NF text 11-30 -> P
U3=[pages.get(178,'')]
P3=[pages[p] for p in range(11,31)]
P4=[open(S+'out/Heine_Buch_der_Lieder_1827_restituiert.txt').read()]+[open(f).read() for f in glob.glob(S+'out/A2/Gedichte/*.txt')]+[open(U8+f).read() for f in ['Heine_Heimkehr.txt','Heine_Almanach.txt','Heine_Aurora.txt','Heine_Ballade.txt','Heine_Biene.txt','Heine_DonnaClara.txt','Heine_Kevlaar.txt','Heine_Ratcliff.txt','Heine_Agrippina.txt']]
STOP=set('der die das den dem des ein eine einen einem einer eines und oder aber doch so wie als da dann wenn wo was wer ich du er sie es wir ihr mich dich sich mir dir ihm ihn ihr uns euch mein meine meinen meinem meiner dein deine deinen deinem sein seine seinen seinem seiner ihre ihren ihrem ist bin bist sind war hat habe hab hast haben wird will kann mag in im an am auf aus bei mit nach von vor zu zum zur über unter um durch für nicht nur noch schon auch gar wol wohl ja nein o ach nun dort hier da dies diese dieser jener all alle'.split())
def norm(t):
    t=t.replace('ſ','s').lower().replace('ß','ss').replace("'",'').replace('’','').replace('th','t')
    t=re.sub(r'ey','ei',t); t=t.replace('ä','ae').replace('ö','oe').replace('ü','ue')
    return t
def stem(w): return re.sub(r'(en|em|er|es|e|n|s)$','',w) if len(w)>4 else w
def lines_units(text):
    pairs,tris=set(),set()
    for line in re.split(r'[\n.;:!?]',text):
        tok=re.findall(r'[a-z]+',norm(line))
        st=[stem(w) for w in tok]
        for i in range(len(st)-2): tris.add(' '.join(st[i:i+3]))
        c=[stem(w) for w in tok if w not in STOP and len(w)>2]
        for i in range(len(c)-1): pairs.add(c[i]+' '+c[i+1])
    return pairs,tris
def setof(texts):
    P,T=set(),set()
    for t in texts:
        p,tr=lines_units(t); P|=p; T|=tr
    return P,T
UP,UT=setof(U1+U2+U3); PP,PT=setof(P1+P2+P3+P4)
print('U-Segmente',len(U1),len(U2),'U-Einheiten',len(UP),len(UT),'P-Einheiten',len(PP),len(PT))
def hits(text):
    p,t=lines_units(text)
    hp=sorted(x for x in p if x in UP and x not in PP); ht=sorted(x for x in t if x in UT and x not in PT)
    return hp,ht,len(p),len(t)
K=open(U8+'Kandidat_Vagabund.txt').read()
hp,ht,np_,nt=hits(K)
print('KANDIDAT pairs',len(hp),hp,'tris',len(ht),ht,'(von',np_,nt,')')
# also hits in P (descriptive)
p,t=lines_units(K); print('Kandidat-Paare auch in gedruckten Heine-Texten:',len([x for x in p if x in PP]),'von',len(p))
# controls: blocks of ~len(K words)
nw=len(K.split())
ctrl=[]
for f in ['Steinmann_Lieder','Geibel_Lieder','Geibel_Junius','Geibel_Buecher','Hektor_Vagabund','Hektor_Schilda','Mueller_1','Mueller_2','Wunderhorn_1806','Uhland_Lieder']:
    t=open(U8+f+'.txt').read(); lines=t.split('\n'); cur=[];n=0;k=0
    for l in lines:
        cur.append(l); n+=len(l.split())
        if n>=nw:
            r=hits('\n'.join(cur)); ctrl.append((f,len(r[0])+len(r[1]),r[0][:4]+r[1][:4])); cur=[];n=0;k+=1
            if k>=8: break
vals=sorted(c[1] for c in ctrl)
print('Kontrollen',len(ctrl),'Treffer je Probe: Mittel %.2f'%(sum(vals)/len(vals)),'95%-Quantil',vals[int(0.95*len(vals))-1],'max',vals[-1])
print('Kandidat gesamt',len(hp)+len(ht),' Anteil Kontrollen >= Kandidat: %.2f'%(sum(1 for v in vals if v>=len(hp)+len(ht))/len(vals)))
for c in sorted(ctrl,key=lambda x:-x[1])[:12]: print(c)

NFP,NFT=setof(P3); BP,BT=setof(P4+P1)
def share(text):
    p,t=lines_units(text); return (len([x for x in p if x in BP])/max(1,len(p)), len([x for x in p if x in NFP])/max(1,len(p)), sorted(x for x in p if x in NFP))
k=share(K); print('Kandidat: Anteil Paare in BdL-Texten %.3f, in NF %.3f'%k[:2], k[2])
rows=[]
for f in ['Steinmann_Lieder','Geibel_Lieder','Geibel_Junius','Hektor_Vagabund','Hektor_Schilda','Mueller_1','Mueller_2','Wunderhorn_1806','Uhland_Lieder']:
    t=open(U8+f+'.txt').read(); w=t.split(); bl=[' '.join(w[i:i+nw]) for i in range(0,min(len(w),nw*8),nw)]
    # use line structure: approximate by splitting on original lines instead
    lines=t.split('\n'); cur=[];n=0;res=[]
    for l in lines:
        cur.append(l); n+=len(l.split())
        if n>=nw: res.append(share('\n'.join(cur))[:2]); cur=[];n=0
        if len(res)>=8: break
    if not res: continue
    rows.append((f,round(sum(r[0] for r in res)/len(res),3),round(sum(r[1] for r in res)/len(res),3),len(res)))
for r in rows: print(r)
for f in ['Steinmann_Lieder','Steinmann_Sonette']:
    t=open(U8+f+'.txt').read(); s=share(t); print(f,len(t.split()),'BdL %.3f NF %.3f'%s[:2])
t=open(S+'out/Steinmann_Lieder_bereinigt.txt').read(); s=share(t); print('Steinmann bereinigt',len(t.split()),'BdL %.3f'%s[0])
pK=lines_units(K)[0]; print('Kandidat Paare in BdL:',sorted(x for x in pK if x in BP))
import re as _re
nft='\n'.join(P3)
# NF text: strip witness labels lines
nft=_re.sub(r'J{1,2}I{0,2}:|H\d?:[^\n]*','',nft)
w=nft.split(); res=[]
lines=nft.split('\n'); cur=[];n=0
for l in lines:
    cur.append(l); n+=len(l.split())
    if n>=nw: res.append(share('\n'.join(cur))[0]); cur=[];n=0
print('Heines Neuer Frühling (echt, nicht BdL): Anteil Paare in BdL je Probe',[round(x,3) for x in res])
