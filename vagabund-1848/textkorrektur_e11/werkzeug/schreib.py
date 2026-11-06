import sys,re,os
d=sys.argv[1]; t=sys.stdin.read()
for teil in re.split(r'(?m)^@@ ',t)[1:]:
    kopf,_,rest=teil.partition('\n'); p=int(kopf.split()[0])
    os.makedirs(f'korr/{d}',exist_ok=True)
    open(f'korr/{d}/{p}.txt','w').write(rest.strip()+'\n'); print(d,p,len(rest.split()),'Wörter')
