#!/usr/bin/env python3
"""Generate analysis.ipynb for the Pengangguran 2026 project."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

cells = []


def md(src):
    cells.append({"cell_type": "markdown", "metadata": {},
                  "source": src.splitlines(True)})


def code(src):
    cells.append({"cell_type": "code", "metadata": {},
                  "execution_count": None, "outputs": [],
                  "source": src.splitlines(True)})


md("# Analisis Pengangguran Indonesia 2026\n"
   "**Paradoks pendidikan: makin tinggi ijazah, makin tinggi pengangguran.**\n\n"
   "> Dataset dikompilasi dari angka resmi BPS (Sakernas). "
   "Lihat `data/SOURCES.md` untuk sumber per angka.")

code("import pandas as pd\nimport matplotlib.pyplot as plt\n"
     "from pathlib import Path\n"
     "D = Path('data/compiled')\n"
     "pd.set_option('display.float_format', '{:.2f}'.format)")

md("## 1. Muat data kompilasi")
code("nas = pd.read_csv(D/'tpt_nasional_series.csv')\n"
     "pend = pd.read_csv(D/'tpt_pendidikan.csv')\n"
     "umur = pd.read_csv(D/'tpt_umur.csv')\n"
     "prov = pd.read_csv(D/'tpt_provinsi.csv')\n"
     "dist = pd.read_csv(D/'distribusi_penganggur_pendidikan.csv')\n"
     "print('nasional:', nas.shape, '| pendidikan:', pend.shape,\n"
     "      '| umur:', umur.shape, '| provinsi:', prov.shape)")

md("## 2. Tren TPT nasional: turun perlahan")
code("nas[['periode','tpt_persen','penganggur_jt','upah_buruh_jt']]")

md("## 3. Paradoks pendidikan (Mei 2026)")
code("p = pend.set_index('pendidikan')[['feb_2026','mei_2026']]\n"
     "p['gap_vs_sd_pp'] = p['mei_2026'] - p.loc['SD ke bawah','mei_2026']\n"
     "p['ratio_vs_nasional'] = p['mei_2026'] / 4.65\n"
     "p.sort_values('mei_2026', ascending=False)")

md("## 4. Pengangguran muda meledak saat nasional turun")
code("umur.set_index('kelompok_umur')\n"
     "muda = umur.set_index('kelompok_umur').loc['15-24 tahun']\n"
     "print('15-24 thn Mei 2026:', muda['mei_2026'], '%')\n"
     "print('Naik Feb->Mei 2026:', round(muda['mei_2026']-muda['feb_2026'],2), 'pp')\n"
     "print('Rasio vs nasional:', round(muda['mei_2026']/4.65,2), 'x')")

md("## 5. Jurang provinsi (Mei 2026)")
code("pm = prov[['provinsi','mei_2026']].dropna().sort_values('mei_2026', ascending=False)\n"
     "pm.head(10)\n"
     "print('Papua vs Bali:', round(7.08/1.52,2), 'x lipat')")

md("## 6. 7,22 juta penganggur: siapa mereka?")
code("dist['juta_orang'] = (7.22 * dist['porsi_persen'] / 100).round(4)\n"
     "dist.sort_values('porsi_persen', ascending=False)\n"
     "print('Total porsi:', dist['porsi_persen'].sum().round(2), '%')")

md("## 7. Chart")
code("from IPython.display import Image, display\n"
     "import glob\n"
     "for f in sorted(glob.glob('charts/*.png')):\n"
     "    print(f)\n"
     "    display(Image(f, width=800))")

nb = {"nbformat": 4, "nbformat_minor": 5,
      "metadata": {"kernelspec": {"display_name": "Python 3",
                                  "language": "python", "name": "python3"},
                   "language_info": {"name": "python", "version": "3.12"}},
      "cells": cells}
(HERE / "analysis.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1),
                                     encoding="utf-8")
print("analysis.ipynb written:", len(cells), "cells")
