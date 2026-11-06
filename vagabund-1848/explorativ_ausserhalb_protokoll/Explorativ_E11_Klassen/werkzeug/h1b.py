import json,html,re,collections
R='/'.join(__import__('os').environ.get('AA', 'AuthorshipAttribution').split('/'))
A=json.load(open(R+'/A_Administration/DHA01_hhp_raw.json',encoding='utf-8'))
pages=collections.defaultdict(list)
for p,n,tag,style,t in A:
    if tag in ['linebreak','emptyline']: pages[p].append('\n')
    if t and tag not in ['faksimile','invfaksimile','pageheader']: pages[p].append(html.unescape(re.sub('<[^>]*>','',t)))
DA={p:''.join(t) for p,t in pages.items()}
HEAD=re.compile(r"^\s*(<.*>|[IVXLC]+\.|\d+\.|Lieder von.*|Kleine Gedichte.*|\(Geschrieben.*|Drey und dreyßig.*|Lied\.|Burleskes Sonett\.|Etwas für.*|H\. Heine\.|\d\. Zu ›.*|\(Aus Göttingen.*\))\s*$")
def poem(pages_,incipit,maxlines=200):
    lines=[]
    for p in pages_: lines+=DA[p].split('\n')
    key=re.sub(r'\W','',incipit.lower())[:20]
    for i,l in enumerate(lines):
        if re.sub(r'\W','',l.lower()).startswith(key):
            out=[]
            for m in lines[i:i+maxlines]:
                if out and (HEAD.match(m) or m.strip().startswith('<')): break
                out.append(m)
            t='\n'.join(out).strip()
            return re.sub(r'\n{3,}','\n\n',t)
    raise SystemExit('nicht gefunden: '+incipit)
MAIN=[ # (gruppe,nr,incipit,pages)
('Agrippina','1','Die Wälder und Felder grünen',[482]),
('Agrippina','3','Man glaubt daß ich mich gräme',[242]),
('Agrippina','5','Lieben und Hassen, Hassen und Lieben',[482]),
('Agrippina','6','Daß ich dich liebe, o Möpschen',[483]),
('Agrippina','7',"Tag und Nacht hab' ich gedichtet",[483]),
('Agrippina','8','Die Jahre kommen und gehen',[234]),
('Agrippina','10','Es faßt mich wieder der alte Muth',[483]),
('Agrippina','11','Auf den Wällen Salamankas',[292,294]),
('Rheinblüthen','I','Den König Wiswamitra',[258]),
('Rheinblüthen','II','Nun ist es Zeit, daß ich mit Verstand',[256,258]),
('Rheinblüthen','III','Du Lilje meiner Liebe',[481]),
('Rheinblüthen','IV','Ich rief den Teufel, und er kam',[246]),
('Rheinblüthen','V','Mensch! verspotte nicht den Teufel',[246]),
('Rheinblüthen','VI','Und als ich Euch meine Schmerzen geklagt',[244]),
('Biene','I','In mein gar zu dunkles Leben',[206]),
('Biene','II','Du hast Diamanten und Perlen',[274]),
('Biene','III','Sie haben heut Abend Gesellschaft',[272]),
('Biene','IV','Hat sie sich denn nicht geäußert',[244]),
('Biene','V','Sie liebten sich Beide, doch Keiner',[244]),
('Biene','VI','Theurer Freund! Was soll es nützen',[256]),
('Biene','VII','Werdet nur nicht ungeduldig',[256]),
]
out=[];man=[]
for g,nr,inc,ps in MAIN:
    t=poem(ps,inc); out.append(t); man.append(dict(gruppe=g,nr=nr,incipit=inc,dha=ps,woerter=len(t.split()),text=t))
open('H1b_Haupt.txt','w').write('\n\n'.join(out)+'\n')
# Gegenprobe: + Agrippina 2, 9 aus Datei; <25>-<32>; Wenn junge Herzen brechen
ag=open(R+'/Heine/Heine_Agrippina.txt',encoding='utf-8-sig').read()
def ausdatei(inc,stop):
    i=ag.index(inc); j=ag.index(stop,i); return ag[i:j].strip()
extra=[ausdatei('Er steht so starr','Altes Kaminstück'), ausdatei('Draußen ziehen weiße Flocken','Du bist gestorben')]
unpr={};cur=None
for p in range(512,531):
    for line in DA[p].split('\n'):
        if line.strip()=='LE MESSAGE.': cur=None; break
        m=re.fullmatch(r'<(\d+)\.>',line.strip())
        if m: cur=int(m[1]); unpr[cur]=[]; continue
        if cur: unpr[cur].append(line)
for k in range(25,33):
    t='\n'.join(l for l in unpr[k] if not HEAD.match(l)).strip(); extra.append(re.sub(r'\n{3,}','\n\n',t))
extra.append(poem([484],'Wenn junge Herzen brechen'))
open('H1b_plus.txt','w').write('\n\n'.join(out+extra)+'\n')
json.dump(man,open('H1b_manifest.json','w'),ensure_ascii=False,indent=1)
print('Haupt',sum(m['woerter'] for m in man),'plus',len(open('H1b_plus.txt').read().split()))
for k in range(25,33): print(k, ' '.join(unpr[k])[:90])
