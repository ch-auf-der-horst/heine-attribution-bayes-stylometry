# Case 1: The ‘Norderney’ poems in *Der Vagabund* (1848)

*Deutsche Fassung: [README.de.md](README.de.md)*

Texts, scripts, test protocols and results for the article:

> Christoph auf der Horst: Authenticity as probability: the ‘Norderney’ poems in *Der Vagabund* (1848) and attribution practice in Heine scholarship. Submitted to *Digital Scholarship in the Humanities*.

A version archived with a DOI will follow on publication.

## Subject

In 1848 Enno Hektor printed ten poems in his Emden journal *Der Vagabund* (issues IV and V) as songs by Heinrich Heine found on Norderney. Since Franzos (1903) and Elster (1925) they have been regarded as the work of Hektor’s friend Ernst Warnebold. The article tests this attribution with a Bayesian assessment and calibrated stylometry. This folder makes the calculations traceable.

## Structure

| Folder or file | Contents |
|---|---|
| `korpus/` | diplomatic texts of the candidate and of the comparison authors (without Heine); generation scripts; `PROTOKOLL.md` on source texts and editorial interventions; blinding (pool, samples, key) |
| `bayes/` | calibration, blinded application and individual tests E-1 to E-11 (`kal/`), spelling normalisation (`norm/`), imitator texts for the cross-check (`e11/texte/`), overall assessment (`bilanz/`) |
| `textkorrektur_e11/` | correction of the imitator texts against the page images: report, change log, samples, recalculation, data and scripts for the figures |
| `abbildungen/` | Figs 1 and 2 of the article, Tippett plot (note 9) |
| `stilometrie/` | preliminary studies outside the protocol (Section 7.6): scripts, protocols, results in text form |
| `explorativ_ausserhalb_protokoll/` | subdivision of H1 and H3 (note 4) and further imitator runs, with remarks on the limits of interpretation |
| `quellen/` | newspaper search on Warnebold with search logs (note 3) |
| `PROTOKOLLE_II3_II3a.md` | the dated test protocols II.3 and II.3a (E-1 to E-11) and the protocol for the reference class, from the working document (in German, with an English summary) |
| `EINGABEN_NICHT_ENTHALTEN.md`, `eingaben_nicht_enthalten.csv` | inputs that are not published, with target path, source, production and SHA-256 checksum |
| `LITERATUR.md` | full references for the short citations in this folder |
| `pruefe.py` | automatic check of the public state (see below) |

## Installation

Python 3.10 or later. From the root folder of the repository:

```
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # exact tested versions: requirements-getestet.txt
cd vagabund-1848
```

The public state was checked with two environments: Python 3.13.16 with the versions in `requirements-getestet.txt`, and Python 3.10.12 with NumPy 2.2.6, SciPy 1.15.3, Matplotlib 3.10.9, scikit-learn 1.7.2 and Pillow 12.3.0.

## Recomputable without Heine’s texts

Six scripts run with the files in this folder alone. Call them from this folder:

```
python bayes/bilanz/posterior.py                                  # Section 8.2, Table 5
python bayes/bilanz/schwelle.py                                   # Section 8.3, note 12
python textkorrektur_e11/nachrechnung/tab5_warnebold_neutral.py   # Table 5, row ‘Warnebold finding neutral against H3’
python textkorrektur_e11/nachrechnung/abb1_EN.py                  # Fig. 1 (from abb_daten2_korr.json)
python textkorrektur_e11/nachrechnung/abb2_EN.py                  # Fig. 2
python textkorrektur_e11/nachrechnung/tippett_EN.py               # Tippett plot and Cllr, note 9 (from abb_daten2_korr.json)
```

The figure scripts write their files to `textkorrektur_e11/nachrechnung/abb/`. They use the Inter typeface if it is installed and otherwise DejaVu Sans, which ships with Matplotlib; the figures then differ from the published ones in typeface only.

`python pruefe.py` checks the public state in one go: the checksums in `../MANIFEST.sha256`, the structure of all CSV and JSON files, and the six scripts with their expected results (run in a temporary copy). On GitHub the same check runs automatically (`.github/workflows/pruefung.yml`).

All other calculations (stylometry, calibration, blinded application, cross-check with the imitators, tests E-1 to E-11) need Heine’s texts, which cannot be published here. `EINGABEN_NICHT_ENTHALTEN.md` lists what is missing, where the scripts expect it and how it was produced. The results of these calculations are given in the JSON and CSV files and in the reports next to the scripts.

## Historical preparation scripts

The following scripts document how texts and samples were produced. They are not part of the analysis and are not meant to be re-run: they need source files that are not included (page images, OCR pages, Word transcriptions, DHA data), and some would overwrite included files. Several now stop before writing anything if their inputs are missing.

- `korpus/erzeuge_*.py`, `korpus/verblindung/*.py`, `bayes/kal/vb/*.py` (texts and blinding; `verblinden.py` refuses to run because the key already exists)
- `bayes/norm/*.py`, `bayes/e4/prep.py` (normalisation, preparation for E-4)
- `bayes/kal/e11prep.py` (raw OCR of the imitator volumes; would overwrite the corrected texts and stops unless `E11PREP_NEU=1` is set)
- `textkorrektur_e11/werkzeug/*`, `textkorrektur_e11/textqualitaet/*` (page-by-page correction and error rates; the corrected pages are in `seiten_korrigiert.tgz`)
- `explorativ_ausserhalb_protokoll/*/werkzeug/*`
- `quellen/warnebold/zeitungen/*/recherchiere_warnebold_zeitungen.py` (queries an online newspaper portal; the results are logged in the same folder)

## Correspondence with the article

| Article | Files |
|---|---|
| Table 2, Section 5.3 | `bayes/bilanz/referenzklasse.csv` (list of cases with sources; the counts used in the calculation are set in `posterior.py`) |
| Table 3, note 11 (sceptical values) | `bayes/bilanz/befunde.csv` |
| Section 6.4, count of punchlines | `bayes/e10/PROTOKOLL.md` (the coding quotes Heine’s verse and is not included) |
| Table 4, Section 7.2 | `bayes/kal/calib.py`, `kalibrierung.json`; verse features `e3.py`; open-set cross-check `openset.py` |
| Section 7.3, note 6 | `bayes/kal/blind.py`, `blind_ergebnis.json`, `korpus/verblindung/` |
| Section 7.4, Fig. 1 | `bayes/kal/e11.py`, `e11.json`; `textkorrektur_e11/nachrechnung/abb_daten2_korr.py`, `abb1_EN.py` |
| Section 7.5 | individual tests `bayes/kal/e1.py` to `e9c.py` (the header of each script names its protocol) |
| Section 7.6 | `stilometrie/` |
| Section 8.2, Table 5, Fig. 2 | `bayes/bilanz/posterior.py`; `textkorrektur_e11/nachrechnung/abb2_EN.py`, `tab5_warnebold_neutral.py` |
| Section 8.3, note 12 | `bayes/bilanz/schwelle.py` |
| note 8 | `textkorrektur_e11/` |
| note 9 (bootstrap, Cllr, Tippett plot) | `textkorrektur_e11/nachrechnung/abb_daten2_korr.py`, `tippett_EN.py`, `abbildungen/Tippett_Repositorium.*` |
| note 10 (closeness to the *Buch der Lieder*) | `bayes/nf/e8.py` (needs Heine’s texts) |

## Checksums

`../MANIFEST.sha256` covers every file of the published version and is the list to check against. Some folders contain older checksum lists from the working process; they are kept as historical evidence and are not rewritten:

- `bayes/e11/texte/SHA256SUMS.txt` gives the paths with the prefix `texte_neu/`, the folder in which the corrected texts were assembled. Check with `sed 's#texte_neu/##' SHA256SUMS.txt | sha256sum -c` in that folder.
- The `*.sha256` files in `explorativ_ausserhalb_protokoll/` date the protocol drafts and contain a timestamp line after the checksum.
- `explorativ_ausserhalb_protokoll/Explorativ_E11_Klassen/texte/SHA256SUMS.txt` also lists four Heine files (H1b, H1c) that are not included; their checksums are repeated in `eingaben_nicht_enthalten.csv`.

## Prespecification

Each test protocol was dated in the working document before the candidate was opened; the protocols are reproduced in `PROTOKOLLE_II3_II3a.md`. There was no external registration. Retrospective decisions and deviations are reported in Section 5.5 and Table 5 of the article.

## Use of AI tools

AI-assisted tools (Cursor, Claude) were used in developing the code and preparing the data. The author directed their use, checked the code and re-ran the analyses. Details are given in the AI Disclosure Statement of the article.

## Licence

Code: MIT. Own transcriptions, protocols and results: CC BY 4.0. Texts from the Deutsches Textarchiv (*Des Knaben Wunderhorn* 1806, Uhland 1815, the 20 prose excerpts in `korpus/e5/dta_prosa_e5.json`), including their normalised versions and samples derived from them: CC BY-SA 4.0. Details in `../LICENSE` and `../LICENSE-DATA.md`.

## Contact

Christoph auf der Horst, Heinrich-Heine-Universität Düsseldorf  
ORCID: [0000-0002-9372-7537](https://orcid.org/0000-0002-9372-7537)
