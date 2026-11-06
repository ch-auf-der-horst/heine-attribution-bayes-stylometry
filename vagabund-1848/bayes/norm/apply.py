import sys,glob,os,csv,collections,shutil
sys.path.insert(0,'.'); import angleichen as A
S='arbeit/out'
jobs=[(f,'out/korpus/'+os.path.basename(f)[:-4]+'_ang.txt') for f in sorted(glob.glob('AuthorshipAttribution/corpus_diplomatisch/*.txt')) if 'Kandidat' not in f]
jobs.append((S+'/Heine_Buch_der_Lieder_1827_restituiert.txt','out/korpus/Heine_Buch_der_Lieder_1827_restituiert_ang.txt'))
for f in sorted(glob.glob(S+'/A2/Gedichte/*.txt')): jobs.append((f,'out/A2/Gedichte/'+os.path.basename(f)))
for f in sorted(glob.glob(S+'/A2/Bloecke_548/*.txt')): jobs.append((f,'out/A2/Bloecke_548/'+os.path.basename(f)))
rows=[]; total=collections.Counter(); R=['R1 th','R2 ey','R3 Ae','R3 e-Überstrich','R4 Apostroph','R5 Anführung','R6 Strich']
for src,dst in jobs:
    A.log.clear(); t=open(src,encoding='utf-8').read(); u=A.angleichen(t)
    assert t.count('\n')==u.count('\n') and len(t.split())==len(u.split())
    open(dst,'w',encoding='utf-8').write(u)
    by=collections.Counter()
    for (r,a,b),n in A.log.items():
        by[r]+=n
        if '/A2/Bloecke' not in src: total[(r,a,b)]+=n
    rows.append([os.path.basename(src)]+[by[r] for r in R]+[len(t.split())])
with open('out/Angleichung_je_Datei.csv','w',newline='') as f:
    w=csv.writer(f,delimiter=';'); w.writerow(['Datei','R1 th','R2 ey','R3 Ae/Oe/Ue','R3 e-Überstrich','R4 Apostroph','R5 Anführung','R6 Strich','Wörter'])
    for r in rows:
        if not r[0].startswith('A2_'): w.writerow(r)
    a2=[r for r in rows if r[0].startswith('A2_') and not r[0].startswith('A2_Block')]
    w.writerow(['A2 (178 Gedichte zusammen)']+[sum(r[i] for r in a2) for i in range(1,9)])
with open('out/Angleichung_Ersetzungen.csv','w',newline='') as f:
    w=csv.writer(f,delimiter=';'); w.writerow(['Regel','vorher','nachher','Anzahl (alle Korpora, ohne A2-Blöcke)'])
    for (r,a,b),n in sorted(total.items()): w.writerow([r,a,b,n])
shutil.copy('angleichen.py','out/angleichen.py')
# rate per 1000 words of R1+R2 per file for report
for r in rows:
    if not r[0].startswith('A2_B') and not r[0].startswith('A2_'):
        print(f"{r[0][:40]:40} th/1000={1000*r[1]/r[-1]:5.1f} ey/1000={1000*r[2]/r[-1]:5.1f}")
print('A2', 1000*sum(r[1] for r in a2)/sum(r[-1] for r in a2), 1000*sum(r[2] for r in a2)/sum(r[-1] for r in a2))
