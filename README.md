# Heine Attribution Studies

Data, scripts and test protocols for assessing the authenticity of texts that have been attributed to, or denied to, Heinrich Heine. The tests combine philological findings with calibrated stylometry in a Bayesian assessment: each finding is weighted as a likelihood ratio, the prior probability is estimated from a reference class of comparable cases, and the uncertainty is reported in sensitivity analyses.

*Deutsche Fassung: [README.de.md](README.de.md)*

## Cases

| Folder | Subject | Article |
|---|---|---|
| `vagabund-1848/` | ten poems that Enno Hektor printed in 1848 in *Der Vagabund* as poems by Heine found on Norderney | auf der Horst, ‘Authenticity as probability’, submitted to *Digital Scholarship in the Humanities* |

Each folder has its own README describing its structure, how to reproduce the results, and which scripts produce which tables and figures.

## Quick check

```
pip install -r requirements.txt
python vagabund-1848/pruefe.py
```

This checks the checksums, the CSV and JSON files and the six scripts that run without Heine’s texts. Installation, tested versions and details are in the README of each case.

## Language

The READMEs are available in English and German. Test protocols, reports, code comments and file names are in German, as are the texts under study.

## Use of AI tools

AI-assisted tools (Cursor, Claude) were used in developing the code and preparing the data; the author checked the code and re-ran the analyses. See the AI Disclosure Statement of the article.

## Citation

Please cite the article and this repository (version 1.0.0). A version archived with a DOI will follow on publication. Details in `CITATION.cff`.

## Licence

Code: MIT (`LICENSE`). Own transcriptions, protocols, results, figures and documentation: CC BY 4.0. Texts from the Deutsches Textarchiv: CC BY-SA 4.0. Texts from modern scholarly editions and data from the Heine-Portal are not included. Details in `LICENSE-DATA.md` (German: `LICENSE-DATEN.md`).

## Contact

Christoph auf der Horst, Heinrich-Heine-Universität Düsseldorf  
ORCID: [0000-0002-9372-7537](https://orcid.org/0000-0002-9372-7537)  
GitHub: [ch-auf-der-horst](https://github.com/ch-auf-der-horst)
