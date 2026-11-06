"""Tippett-Plot (Repositorium, Anm. 9): score-basierte Likelihood-Quotienten aus abb_daten2_korr.json.
Nachträglich, nicht im Protokoll; geht nicht in die Bilanz ein.
Kurven: Anteil der Proben mit log10 LR >= x, getrennt für Heine-Proben (H1) und Nachahmerproben (H3)."""
import json, numpy as np, matplotlib
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Pfade relativ zum Skriptordner
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter
os.makedirs('abb', exist_ok=True)  # Ausgabeordner
# Inter, falls installiert; sonst die mit Matplotlib gelieferte DejaVu Sans
SCHRIFT = 'Inter' if any(f.name == 'Inter' for f in font_manager.fontManager.ttflist) else 'DejaVu Sans'
plt.rcParams.update({'font.family': SCHRIFT, 'font.size': 8.5, 'pdf.fonttype': 42, 'ps.fonttype': 42, 'axes.linewidth': 0.6})
HEINE = '#1f5a8a'; NACH = '#6f6f6f'; INK = '#1a1a1a'; MUTED = '#5f5f5f'

d = json.load(open('abb_daten2_korr.json', encoding='utf-8'))
TITEL = {'w': 'Vocabulary (150 most frequent words)', 'c': 'Character 4-grams'}


def kurve(werte, xs):
    v = np.asarray(werte)
    return np.array([(v >= x).mean() for x in xs])


alle = [x for k in 'wc' for x in d[k]['llr_h1'] + d[k]['llr_h3'] + [d[k]['llr_kandidat']]]
lo, hi = np.floor(min(alle) * 2) / 2 - 0.1, np.ceil(max(alle) * 2) / 2 + 0.1
xs = np.linspace(lo, hi, 2000)

fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.4), sharey=True)
for ax, k in zip(axs, 'wc'):
    m = d[k]
    ax.axvline(0, color='#bdbdbd', linewidth=0.8, zorder=1)
    ax.step(xs, kurve(m['llr_h1'], xs), where='post', color=HEINE, linewidth=1.8, label='Heine samples (H1 true)', zorder=3)
    ax.step(xs, kurve(m['llr_h3'], xs), where='post', color=NACH, linewidth=1.8, linestyle=(0, (4, 2)), label='Imitator samples (H3 true)', zorder=2)
    ax.axvline(m['llr_kandidat'], color=INK, linewidth=1.0, zorder=4)
    ax.text(m['llr_kandidat'], 1.06, 'Candidate', ha='center', va='bottom', color=INK, fontsize=7.5)
    ax.text(0.02, 0.03, f"Cllr = {m['cllr']:.2f}", transform=ax.transAxes, color=MUTED, fontsize=7.5)
    ax.set_title(TITEL[k], loc='left', color=INK, fontsize=8.5, pad=14)
    ax.set_xlim(lo, hi); ax.set_ylim(-0.04, 1.04)
    ax.set_xlabel('log10 likelihood ratio (H1 : H3)', color=INK)
    ax.grid(color='#ececec', linewidth=0.5, zorder=0)
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=7.5)
axs[0].set_ylabel('Proportion of samples with LR ≥ x', color=INK)
axs[0].yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.0%}'))
h, l = axs[0].get_legend_handles_labels()
fig.legend(h, l, loc='upper right', ncol=2, frameon=False, fontsize=7.5)
fig.subplots_adjust(left=0.09, right=0.98, bottom=0.15, top=0.80, wspace=0.12)
for ext, kw in [('pdf', {}), ('png', {'dpi': 200})]:
    fig.savefig(f'abb/Tippett_Repositorium.{ext}', **kw)
print('Cllr', {k: round(d[k]['cllr'], 3) for k in 'wc'}, 'Kandidat log10 LR', {k: round(d[k]['llr_kandidat'], 3) for k in 'wc'})
print('ok')
