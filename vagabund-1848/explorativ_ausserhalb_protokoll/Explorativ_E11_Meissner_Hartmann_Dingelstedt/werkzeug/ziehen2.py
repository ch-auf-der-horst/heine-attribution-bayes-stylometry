import random,sys,json,subprocess,os
name=sys.argv[1]; pools=json.loads(sys.argv[2])  # [[dir,pdf,von,bis],...]
U='AuthorshipAttribution/Heine_Nachahmer_Gedichtbaende/'
pages=[(d,f,p) for d,f,a,b in pools for p in range(a,b+1)]
r=random.Random(20261031); r.shuffle(pages)
sel=[];n=0
for d,f,p in pages:
    os.makedirs(f'neu/{d}',exist_ok=True); os.makedirs(f'img/{d}',exist_ok=True); os.makedirs(f'rein/{d}',exist_ok=True)
    if not os.path.exists(f'neu/{d}/{p}.txt'):
        subprocess.run(f'pdftoppm -f {p} -l {p} -scale-to-x -1 -scale-to-y 2200 -gray -png -singlefile {U}{f}.pdf img/{d}/{p}',shell=True,check=True)
        from PIL import Image
        Image.open(f'img/{d}/{p}.png').point(lambda v: 255 if v>150 else 0).save(f'img/{d}/{p}_b.png')
        subprocess.run(f'OMP_THREAD_LIMIT=1 TESSDATA_PREFIX=arbeit/korr/tessdata tesseract img/{d}/{p}_b.png neu/{d}/{p} -l deu_latf --psm 4',shell=True,check=True,stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
    subprocess.run(f'python3 sk/reinigen.py {d} {p} {p} rein/{d}_tmp && cp rein/{d}_tmp/{p}.txt rein/{d}/{p}.txt',shell=True,check=True,stdout=subprocess.DEVNULL)
    k=len(open(f'rein/{d}/{p}.txt').read().split())
    if k==0: continue
    sel.append((d,p)); n+=k
    print(d,p,k,n,flush=True)
    if n>=11000: break
sel.sort()
json.dump(sel,open(f'auswahl_{name}.json','w')); print('FERTIG',len(sel),n)
