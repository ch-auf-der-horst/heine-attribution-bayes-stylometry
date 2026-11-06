import json, numpy as np, matplotlib
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Pfade relativ zum Skriptordner
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
d=json.load(open('abb_daten2_korr.json'))
rows=[('Heine, first printings to 1824','heine_A2',True),('Th. Storm (1843)','Storm_1843',False),
      ('Th. Mommsen (1843)','ThMommsen_1843',False),('W. Müller v. Königswinter (1841)','Mueller_WvK_1841',False),
      ('J. Scherr (1842)','Scherr_1842',False)]
HEINE='#1f5a8a'; NACH='#6f6f6f'; INK='#1a1a1a'; MUTED='#5f5f5f'; BAND='#d9d9d9'
from matplotlib import font_manager
os.makedirs('abb', exist_ok=True)  # Ausgabeordner
# Inter, falls installiert; sonst die mit Matplotlib gelieferte DejaVu Sans
SCHRIFT = 'Inter' if any(f.name == 'Inter' for f in font_manager.fontManager.ttflist) else 'DejaVu Sans'
plt.rcParams.update({'font.family':SCHRIFT,'pdf.fonttype':42,'ps.fonttype':42,'font.size':8.5,'axes.linewidth':0.6})
fmt=FuncFormatter(lambda x,_: f'{x:.1f}'.replace('-','−'))
def swarm(v, width, step):
    """einfacher Beeswarm: Punkte nach Wert, vertikal versetzt, damit sie sich nicht überlappen"""
    order=np.argsort(v); ys=np.zeros(len(v)); placed=[]
    for i in order:
        k=0
        while True:
            off=((k+1)//2)*step*(1 if k%2 else -1)
            if all(abs(v[i]-pv)>width or abs(off-po)>step*0.9 for pv,po in placed): break
            k+=1
        ys[i]=off; placed.append((v[i],off))
    return ys
fig,axs=plt.subplots(1,2,figsize=(7.2,3.6),sharey=True,gridspec_kw={'wspace':0.28})
for ax,key in zip(axs,['w','c']):
    m=d[key]; k=m['kandidat']; lo,_,hi=m['boot_q']
    alle=np.concatenate([np.array(m[r[1]]) for r in rows]+[[k,lo,hi]]); span=alle.max()-alle.min()
    ax.axvspan(lo,hi,color=BAND,zorder=0,linewidth=0)
    ax.axvline(k,color=INK,linewidth=1.1,zorder=2)
    for i,(lab,key2,isH) in enumerate(rows):
        y=len(rows)-1-i; v=np.array(m[key2]); off=swarm(v,span*0.018,0.09)
        if isH: ax.scatter(v,y+off,s=16,color=HEINE,edgecolor='white',linewidth=0.4,zorder=3)
        else: ax.scatter(v,y+off,s=16,facecolor='white',edgecolor=NACH,linewidth=0.9,zorder=3)
        med=np.median(v); ax.plot([med,med],[y-0.32,y+0.32],color=HEINE if isH else NACH,linewidth=1.6,zorder=4,solid_capstyle='round')
        n_ge=int((v>=k).sum())
        ax.text(1.03,y,f'{n_ge}/{len(v)}',transform=ax.get_yaxis_transform(),ha='left',va='center',color=MUTED,fontsize=7.5,clip_on=False)
    ax.set_title({'Delta Wörter':'Vocabulary (150 most frequent words)','Zeichen-4-Gramme':'Character 4-grams'}[m['name']],fontsize=8.5,color=INK,loc='left',pad=4)
    pad=span*0.06; ax.set_xlim(alle.min()-pad, alle.max()+pad)
    ax.text(k,len(rows)-0.42,'Candidate ',ha='right',va='bottom',color=INK,fontsize=7.5)
    ax.text(1.03,len(rows)-0.42,'≥ cand.',transform=ax.get_yaxis_transform(),ha='left',va='bottom',color=MUTED,fontsize=7,clip_on=False)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,_: f'{x:.2f}'.replace('-','−')))
    for s in ['top','right','left']: ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color('#9a9a9a'); ax.tick_params(axis='y',length=0); ax.tick_params(axis='x',colors=MUTED,labelsize=7.5)
    ax.grid(axis='x',color='#ececec',linewidth=0.5,zorder=0)
    ax.set_xlabel('Heine-likeness s',color=INK)
axs[0].set_yticks(range(len(rows))); axs[0].set_yticklabels([r[0] for r in rows][::-1],color=INK)
axs[0].set_ylim(-0.6,len(rows)-0.05)
fig.subplots_adjust(left=0.26 if SCHRIFT == 'Inter' else 0.30,right=0.93,bottom=0.14,top=0.92)
for ext,kw in [('pdf',{}),('eps',{}),('png',{'dpi':200}),('tiff',{'dpi':600,'pil_kwargs':{'compression':'tiff_lzw'}})]:
    fig.savefig(f'abb/Fig1_Heine-likeness_imitators_EN.{ext}',**kw)
print('ok')
