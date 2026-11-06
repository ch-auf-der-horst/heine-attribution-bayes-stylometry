import re,os
K='arbeit/korr/korr/'
def lies(d,p):
    f=f'{K}{d}/{p}.txt'
    if not os.path.exists(f): return ''
    return '\n'.join(l for l in open(f).read().split('\n') if not l.startswith('#')).strip()
St=[14, 15, 16, 17, 18, 26, 27, 28, 29, 35, 39, 46, 52, 70, 71, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 108, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 140]
Th=[1,5,6,7,8,9,10,11,12,13,22,23,24,25,30,31,32,33,34,36,40,41,44,45,53,54,55,56,57,58,59,60,61,62,63,64,65,66,68,72,73,75,76,77,78,97,98,99,102,103,105,106,107,109,110,111,112,113,114,115,116,117,118,119,135,136,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,157,158,159,160,161,162,164,165,166,167,168,169,170]
PLAN={'Scherr_1842':('sc',list(range(9,117))),'Mueller_WvK_1841':('mu',list(range(15,137))),'Storm_1843':('lb',St),'ThMommsen_1843':('lb',Th)}
if __name__=='__main__':
    # Eingabeprüfung (nachträglich ergänzt, 6.11.2026): Die korrigierten Seiten liegen in seiten_korrigiert.tgz
    # (Ordner korr/); zum Neulauf nach arbeit/korr/ entpacken. Ohne sie entstünden leere Texte.
    if not all(os.path.isdir(K+d) for d in ('sc','mu','lb')):
        raise SystemExit('Abbruch: korrigierte Seiten fehlen in '+K+' (seiten_korrigiert.tgz nach arbeit/korr/ entpacken).')
    os.makedirs('texte_neu',exist_ok=True)
    for n,(d,ps) in PLAN.items():
        txt='\n\n'.join(t for t in (lies(d,p) for p in ps) if t)
        open(f'texte_neu/{n}.txt','w').write(re.sub(r'\n{3,}','\n\n',txt)+'\n')
        print(n,len(txt.split()))
