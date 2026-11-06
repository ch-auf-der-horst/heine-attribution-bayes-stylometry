import re,json,sys
S='arbeit/'
def load(n):
    if n=='K': t=open(S+'e4/Kandidat.txt').read(); t=re.sub(r'(?m)^[IVX]+\.\s*$','',t)
    else: t=open(S+f'kal/vb/pool/hist/{n}.txt').read()
    return t
def toks(t):
    t=t.replace('’',"'")
    raw=re.findall(r"'?[A-Za-zÄÖÜäöüßéè]+(?:'[A-Za-zäöü]*)?",t)
    out=[]
    for w in raw:
        if w.startswith("'"):
            w={"'nen":'einen',"'ne":'eine',"'s":'es',"'n":'ein'}.get(w.lower(),w[1:])
            out.append(w); continue
        if "'" in w:
            a,b=w.split("'",1)
            if b=='s': out+= [a+'e' if a.lower() in('hab','geb') else a,'es']; continue
            if b=='n': out.append(a+'en'); continue
            out.append(a+'e'); continue
        out.append(w)
    return out
D={}
for n in ['K','P03','P04','P10']:
    tk=toks(load(n)); D[n]={'tokens':tk,'types':sorted(set(tk)),
      'grams':sorted(set(' '.join(tk[i:i+4]) for i in range(len(tk)-3)))}
    print(n,len(tk),len(D[n]['types']),len(D[n]['grams']))
json.dump(D,open('e4_input.json','w'),ensure_ascii=False)
