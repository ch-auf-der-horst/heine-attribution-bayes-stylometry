import numpy as np, matplotlib
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Pfade relativ zum Skriptordner
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib import font_manager
os.makedirs('abb', exist_ok=True)  # Ausgabeordner
# Inter, falls installiert; sonst die mit Matplotlib gelieferte DejaVu Sans
SCHRIFT = 'Inter' if any(f.name == 'Inter' for f in font_manager.fontManager.ttflist) else 'DejaVu Sans'
plt.rcParams.update({'font.family':SCHRIFT,'font.size':8.5,'pdf.fonttype':42,'ps.fonttype':42,'axes.linewidth':0.6})
HEINE='#1f5a8a'; NACH='#6f6f6f'; INK='#1a1a1a'; MUTED='#5f5f5f'
def P(p,a,b,s3=0.5):
    n=(1-p)/p; return 1/(1+n*(1-s3)*10**(-a)+n*s3*10**(-b))
p=np.linspace(0.03,0.5,300)
fig,ax=plt.subplots(figsize=(6.0,3.6))
for lo,hi,lab in [(1/21,1/8,'skeptische Ansätze\n(1 : 20 bis 1 : 7)'),(1/6,1/4,'Referenzklasse\n(1 : 5 bis 1 : 3)')]:
    ax.axvspan(lo,hi,color='#ececec' if 'skept' in lab else '#dfe7ef',zorder=0,linewidth=0)
    ax.text((lo+hi)/2,0.985,lab,ha='center',va='top',fontsize=7,color=MUTED)
ax.plot(p,P(p,1.5,0.53),color=HEINE,linewidth=2.2,label='ausgewogene Wertung der Befunde')
ax.plot(p,P(p,1.5,0.53,1.0),color=HEINE,linewidth=1.3,linestyle=(0,(5,2)),label='ausgewogen, Gegenmasse ganz bei einem Nachahmer')
ax.plot(p,P(p,0.75,-0.07),color=NACH,linewidth=2.2,label='skeptische Wertung der Befunde')
ax.plot(p,p,color='#b0b0b0',linewidth=0.9,linestyle=':',label='ohne Befunde (Posterior = Prior)')
ax.axhline(0.5,color='#c8c8c8',linewidth=0.7)
pct=FuncFormatter(lambda y,_: f'{int(round(y*100))} %')
ax.xaxis.set_major_formatter(pct); ax.yaxis.set_major_formatter(pct)
ax.set_xlim(0.03,0.5); ax.set_ylim(0,1)
ax.set_xlabel('Ausgangswahrscheinlichkeit für Heine (Prior)',color=INK)
ax.set_ylabel('Wahrscheinlichkeit für Heine nach den Befunden',color=INK)
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.tick_params(colors=MUTED,labelsize=7.5); ax.grid(color='#f0f0f0',linewidth=0.5)
ax.legend(frameon=False,fontsize=7.2,loc='lower right')
fig.subplots_adjust(left=0.13,right=0.97,bottom=0.14,top=0.97)
for ext,kw in [('pdf',{}),('eps',{}),('png',{'dpi':200}),('tiff',{'dpi':600,'pil_kwargs':{'compression':'tiff_lzw'}})]:
    fig.savefig(f'abb/Abb2_Prior_Posterior_korr2.{ext}',**kw)
print('ok')
