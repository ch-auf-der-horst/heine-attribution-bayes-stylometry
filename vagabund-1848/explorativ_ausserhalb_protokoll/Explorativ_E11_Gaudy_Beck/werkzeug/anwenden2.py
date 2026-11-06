import re,sys,os,csv
d,von,bis,kf,ziel=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4],sys.argv[5]
os.makedirs(ziel,exist_ok=True)
bl={}; cur=None
for l in open(kf,encoding='utf-8').read().split('\n'):
    m=re.match(r'@@ (\d+)( VOLL)?$',l)
    if m:
        cur=int(m.group(1)); 
        if m.group(2): bl[cur]={'voll':[]}
        else: bl.setdefault(cur,{'ers':[]}).setdefault('ers',[])
        continue
    if cur is None or l.startswith('#'): continue
    if 'voll' in bl[cur]: bl[cur]['voll'].append(l); continue
    if not l.strip(): continue
    a,b=l.split(' => ',1) if ' => ' in l else (l.rstrip(' =>').rstrip(),'')
    if l.endswith(' =>'): a,b=l[:-3],''
    bl[cur]['ers'].append((a,b))
log=[]; fehler=0
for p in range(von,bis+1):
    t=open(f'rein/{d}/{p}.txt',encoding='utf-8').read()
    alt=t
    if p in bl and 'voll' in bl[p]: t='\n'.join(bl[p]['voll']).strip()+'\n'
    elif p in bl:
        for a,b in bl[p]['ers']:
            if a not in t: print('FEHLT',p,repr(a)); fehler+=1; continue
            t=t.replace(a,b,1); log.append((p,a,b))
    t=re.sub(r'\n{3,}','\n\n',t)
    if p in bl and 'voll' in bl[p]: log.append((p,'[Seite neu]',''))
    open(f'{ziel}/{p}.txt','w',encoding='utf-8').write(t.strip()+'\n' if t.strip() else '')
with open(f'{ziel}/aenderungen.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['seite','vorher','nachher']); w.writerows(log)
print('fehler',fehler,'aenderungen',len(log))
