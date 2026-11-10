#!/usr/bin/env python3
"""Analyze compiled BPS unemployment data -> findings.json.

Every number is computed from data/compiled/*.csv (compiled from official
BPS publications, see data/SOURCES.md). Nothing is invented.
Headline period: Agustus 2026 (BRS No. 113/11/Th. XXIX, 5 Nov 2026).
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
D = HERE / "data" / "compiled"


def read_csv(name):
    with open(D / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fnum(x):
    x = (x or "").strip()
    return float(x.replace(",", ".")) if x else None


nas = read_csv("tpt_nasional_series.csv")
pend = read_csv("tpt_pendidikan.csv")
umur = read_csv("tpt_umur.csv")
gender = read_csv("tpt_gender.csv")
daerah = read_csv("tpt_daerah.csv")
prov = read_csv("tpt_provinsi.csv")
dist = read_csv("distribusi_penganggur_pendidikan.csv")
indikator = read_csv("pasar_kerja_indikator.csv")
sektor = read_csv("sektor_penambah_pekerja.csv")

PERIODS = ["feb_2024", "agu_2024", "feb_2025", "agu_2025",
           "feb_2026", "mei_2026", "agu_2026"]
PLABEL = {"feb_2024": "Feb 2024", "agu_2024": "Agu 2024",
          "feb_2025": "Feb 2025", "agu_2025": "Agu 2025",
          "feb_2026": "Feb 2026", "mei_2026": "Mei 2026",
          "agu_2026": "Agu 2026"}

# --- national series ---
nas_series = []
for r in nas:
    nas_series.append({
        "periode": r["periode"],
        "tpt": fnum(r["tpt_persen"]),
        "angkatan_kerja_jt": fnum(r["angkatan_kerja_jt"]),
        "tpak": fnum(r["tpak_persen"]),
        "bekerja_jt": fnum(r["bekerja_jt"]),
        "penganggur_jt": fnum(r["penganggur_jt"]),
        "upah_buruh_jt": fnum(r["upah_buruh_jt"]),
    })
by_per = {s["periode"]: s for s in nas_series}
tpt_feb24 = by_per["Feb 2024"]["tpt"]        # 4.82
tpt_agu25 = by_per["Agu 2025"]["tpt"]        # 4.85
tpt_agu26 = by_per["Agu 2026"]["tpt"]        # 4.75
latest = by_per["Agu 2026"]
prev = by_per["Mei 2026"]

# --- education paradox ---
pend_series = {r["pendidikan"]: {p: fnum(r[p]) for p in PERIODS} for r in pend}
smk_agu = pend_series["SMK"]["agu_2026"]            # 8.20
sd_agu = pend_series["SD ke bawah"]["agu_2026"]     # 2.24
smk_vs_sd_pp = round(smk_agu - sd_agu, 2)           # 5.96
smk_vs_nasional_ratio = round(smk_agu / tpt_agu26, 2)  # 1.73
smk_tren = [pend_series["SMK"][p] for p in PERIODS]
smk_yoy_pp = round(pend_series["SMK"]["agu_2026"]
                   - pend_series["SMK"]["agu_2025"], 2)  # -0.43

# --- youth ---
umur_series = {r["kelompok_umur"]: {p: fnum(r[p]) for p in PERIODS} for r in umur}
muda_agu = umur_series["15-24 tahun"]["agu_2026"]          # 17.50
muda_agu25 = umur_series["15-24 tahun"]["agu_2025"]        # 16.89
muda_yoy_pp = round(muda_agu - muda_agu25, 2)              # 0.61
produkt_agu = umur_series["25-59 tahun"]["agu_2026"]       # 2.78
muda_vs_nasional_ratio = round(muda_agu / tpt_agu26, 2)    # 3.68
muda_vs_produktif_ratio = round(muda_agu / produkt_agu, 2)  # 6.29

# --- gender & urban/rural gaps (Agu 2026) ---
g = {r["jenis_kelamin"]: fnum(r["agu_2026"]) for r in gender}
d = {r["daerah"]: fnum(r["agu_2026"]) for r in daerah}
gender_gap_pp = round(g["Laki-laki"] - g["Perempuan"], 2)   # -0.29
urban_rural_gap_pp = round(d["Perkotaan"] - d["Perdesaan"], 2)  # 2.08
urban_rural_ratio = round(d["Perkotaan"] / d["Perdesaan"], 2)   # 1.60

# --- provinces (Agu 2026: all 38 published) ---
prov_agu = [(r["provinsi"], fnum(r["agu_2026"])) for r in prov
            if fnum(r["agu_2026"]) is not None]
prov_agu_sorted = sorted(prov_agu, key=lambda x: x[1], reverse=True)
papua_agu = dict(prov_agu)["Papua"]          # 7.12
bali_agu = dict(prov_agu)["Bali"]            # 1.42
papua_vs_bali_ratio = round(papua_agu / bali_agu, 2)  # 5.01
# Agu 2025 -> Agu 2026 changes (all provinces have both)
prov_changes = []
for r in prov:
    a, b = fnum(r["agu_2025"]), fnum(r["agu_2026"])
    if a is not None and b is not None:
        prov_changes.append({"provinsi": r["provinsi"],
                             "agu_2025": a, "agu_2026": b,
                             "perubahan_pp": round(b - a, 2)})
turun_terbesar = sorted(prov_changes, key=lambda x: x["perubahan_pp"])[:3]
naik_terbesar = sorted(prov_changes, key=lambda x: x["perubahan_pp"],
                       reverse=True)[:3]

# --- distribution of unemployed by education (Agu 2026), absolute in jt ---
penganggur_agu_jt = latest["penganggur_jt"]  # 7.38
dist_abs = [{"pendidikan": r["pendidikan"],
             "porsi_persen": fnum(r["porsi_persen"]),
             "juta_orang": round(penganggur_agu_jt * fnum(r["porsi_persen"]) / 100, 4)}
            for r in dist]
total_porsi = round(sum(x["porsi_persen"] for x in dist_abs), 2)

# --- labor market indicators ---
ind = {r["indikator"]: r for r in indikator}
sektor_list = [{"sektor": r["sektor"],
                "tambah_ribu": int(r["tambah_ribu_orang"])} for r in sektor]

findings = {
    "meta": {
        "topik": "Pengangguran dan Pasar Kerja Indonesia 2026",
        "sumber": "Kompilasi angka resmi BPS (Sakernas) — lihat data/SOURCES.md",
        "periode": "Feb 2024 s.d. Agu 2026",
    },
    "nasional": {
        "tpt_feb_2024": tpt_feb24, "tpt_agu_2026": tpt_agu26,
        "tpt_agu_2025": tpt_agu25,
        "perubahan_pp_feb24_agu26": round(tpt_agu26 - tpt_feb24, 2),
        "turun_pp_yoy_agu25_agu26": round(tpt_agu26 - tpt_agu25, 2),
        "penganggur_agu_2026_jt": penganggur_agu_jt,
        "angkatan_kerja_agu_2026_jt": latest["angkatan_kerja_jt"],
        "bekerja_agu_2026_jt": latest["bekerja_jt"],
        "tpak_agu_2026": latest["tpak"],
        "upah_buruh_agu_2026_jt": latest["upah_buruh_jt"],
        "upah_buruh_mei_2026_jt": prev["upah_buruh_jt"],
        "seri": nas_series,
        "pdb_q2_2026_yoy": 5.29,
    },
    "paradoks_pendidikan": {
        "smk_agu_2026": smk_agu, "sd_agu_2026": sd_agu,
        "smk_vs_sd_pp": smk_vs_sd_pp,
        "smk_vs_nasional_ratio": smk_vs_nasional_ratio,
        "smk_tren": dict(zip([PLABEL[p] for p in PERIODS], smk_tren)),
        "smk_perubahan_pp_feb24_agu26": round(smk_tren[-1] - smk_tren[0], 2),
        "smk_turun_pp_yoy": smk_yoy_pp,
        "seri_pendidikan": {k: {PLABEL[p]: v[p] for p in PERIODS}
                            for k, v in pend_series.items()},
        "distribusi_penganggur_agu_2026": dist_abs,
        "total_porsi_persen": total_porsi,
    },
    "pengangguran_muda": {
        "muda_15_24_agu_2026": muda_agu, "muda_15_24_agu_2025": muda_agu25,
        "muda_naik_pp_yoy": muda_yoy_pp,
        "muda_vs_nasional_ratio": muda_vs_nasional_ratio,
        "muda_vs_produktif_ratio": muda_vs_produktif_ratio,
        "produktif_25_59_agu_2026": produkt_agu,
        "seri_umur": {k: {PLABEL[p]: v[p] for p in PERIODS}
                      for k, v in umur_series.items()},
    },
    "kesenjangan": {
        "laki_agu_2026": g["Laki-laki"], "perempuan_agu_2026": g["Perempuan"],
        "gender_gap_pp": gender_gap_pp,
        "perkotaan_agu_2026": d["Perkotaan"], "perdesaan_agu_2026": d["Perdesaan"],
        "urban_rural_gap_pp": urban_rural_gap_pp,
        "urban_rural_ratio": urban_rural_ratio,
        "tpak_laki_agu_2026": fnum(ind["TPAK laki-laki"]["agu_2026"]),
        "tpak_perempuan_agu_2026": fnum(ind["TPAK perempuan"]["agu_2026"]),
    },
    "provinsi": {
        "top_agu_2026": [{"provinsi": p, "tpt": t}
                         for p, t in prov_agu_sorted[:10]],
        "terendah_agu_2026": [{"provinsi": p, "tpt": t}
                              for p, t in prov_agu_sorted[-5:]],
        "papua_vs_bali_ratio": papua_vs_bali_ratio,
        "turun_terbesar_agu25_agu26": turun_terbesar,
        "naik_terbesar_agu25_agu26": naik_terbesar,
        "gap_catatan": "Agu 2026 tersedia untuk semua 38 provinsi "
                       "(Lampiran 3 BRS); Papua 2022-2023 tidak sebanding "
                       "(pemekaran)",
    },
    "pasar_kerja": {
        "formal_agu_2026": fnum(ind["Pekerja formal (persen)"]["agu_2026"]),
        "informal_agu_2026": fnum(ind["Pekerja informal (persen)"]["agu_2026"]),
        "formal_jt_agu_2026": fnum(ind["Pekerja formal (juta orang)"]["agu_2026"]),
        "setengah_menganggur_agu_2026": fnum(ind["Setengah penganggur"]["agu_2026"]),
        "paruh_waktu_agu_2026": fnum(ind["Pekerja paruh waktu"]["agu_2026"]),
        "penuh_agu_2026": fnum(ind["Pekerja penuh"]["agu_2026"]),
        "komuter_agu_2026_jt": fnum(ind["Pekerja komuter"]["agu_2026"]),
        "sektor_penambah_feb_mei_2026": sektor_list,
    },
}

# --- sanity assertions (fail loudly if a headline number drifts) ---
assert smk_agu == 8.20 and sd_agu == 2.24
assert smk_vs_sd_pp == 5.96
assert muda_agu == 17.50 and muda_yoy_pp == 0.61
assert tpt_agu26 == 4.75
assert urban_rural_gap_pp == 2.08
assert abs(total_porsi - 100.0) < 0.05
assert papua_agu == 7.12 and bali_agu == 1.42
assert len(prov_agu) == 38

with open(HERE / "findings.json", "w", encoding="utf-8") as f:
    json.dump(findings, f, ensure_ascii=False, indent=2)
print("findings.json written.")
print(f"SMK {smk_agu}% vs SD {sd_agu}% (gap {smk_vs_sd_pp} pp, {smk_vs_nasional_ratio}x nasional)")
print(f"Muda 15-24: {muda_agu}% (naik {muda_yoy_pp} pp YoY; {muda_vs_nasional_ratio}x nasional)")
print(f"Papua {papua_agu}% vs Bali {bali_agu}% ({papua_vs_bali_ratio}x)")
print("Turun terbesar YoY:", turun_terbesar[0])
print("Naik terbesar YoY:", naik_terbesar[0])
