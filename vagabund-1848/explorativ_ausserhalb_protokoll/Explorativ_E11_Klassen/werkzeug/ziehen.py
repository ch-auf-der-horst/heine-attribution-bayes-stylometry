import json,random,csv,re,os
R=os.environ.get('AA', 'AuthorshipAttribution')
def ziehe(items,seed=20261031,ziel=11000):
    idx=list(range(len(items))); r=random.Random(seed); r.shuffle(idx); sel=[];n=0
    for i in idx:
        sel.append(i); n+=len(items[i].split())
        if n>=ziel: break
    sel.sort(); return sel,n
d=json.load(open(R+'/Heine/H1b_H1c_Abgleich_2026-10-31/H1c_Neue_Gedichte_1844/Gedichtmanifest.json',encoding='utf-8'))
for name,secs in [('H1c_Haupt',{'Neuer Frühling','Verschiedene','Romanzen'}),('H1c_mitZeit',{'Neuer Frühling','Verschiedene','Romanzen','Zeitgedichte'})]:
    it=[x for x in d if x['abschnitt'] in secs]
    sel,n=ziehe([x['text'] for x in it])
    open(name+'.txt','w').write('\n\n'.join(it[i]['text'].strip() for i in sel)+'\n')
    json.dump([it[i]['id'] for i in sel],open(name+'_auswahl.json','w')); print(name,len(it),len(sel),n)
# Steinmann
S=R+'/Steinmann/Ausgabe_1861/'
reg=list(csv.DictReader(open(S+'Bereinigung/gedichtregister.csv',encoding='utf-8')))
gedichte=[]
for band in ['1','2']:
    lines=open(S+f'Steinmann_Heine_Dichtungen_1861_Bd{band}_bereinigt.txt',encoding='utf-8').read().split('\n')
    rb=[r for r in reg if r['Band']==band]
    starts=[];pos=0
    for r in rb:
        first=r['Titel'].split(' / ')[0].strip()
        k=next((i for i in range(pos,len(lines)) if lines[i].strip()==first),None)
        if k is None: print('FEHLT',band,first); starts.append(None); continue
        starts.append(k); pos=k+1
    for j,r in enumerate(rb):
        if starts[j] is None: continue
        end=next((s for s in starts[j+1:] if s is not None),len(lines))
        tl=len(r['Titel'].split(' / '))
        body='\n'.join(lines[starts[j]+tl:end]).strip()
        gedichte.append(dict(band=band,abschnitt=r['Abschnitt'],titel=r['Titel'],seiten=(r['Druckseite_von'],r['Druckseite_bis']),text=body))
pool=[g for g in gedichte if not g['abschnitt'].startswith(('IX.','VI.'))]
sel,n=ziehe([g['text'] for g in pool])
open('Steinmann_1861.txt','w').write('\n\n'.join(pool[i]['text'] for i in sel)+'\n')
json.dump([dict(band=pool[i]['band'],titel=pool[i]['titel'],seiten=pool[i]['seiten']) for i in sel],open('Steinmann_1861_auswahl.json','w'),ensure_ascii=False,indent=1)
print('Steinmann',len(gedichte),len(pool),len(sel),n)
