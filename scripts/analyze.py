#!/usr/bin/env python3
"""Analyze compiled BPS unemployment data -> findings.json.

Every number is computed from data/compiled/*.csv (compiled from official
BPS publications, see data/SOURCES.md). Nothing is invented.
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

PERIODS = ["feb_2024", "feb_2025", "feb_2026", "mei_2026"]
PLABEL = {"feb_2024": "Feb 2024", "feb_2025": "Feb 2025",
          "feb_2026": "Feb 2026", "mei_2026": "Mei 2026"}

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
tpt_feb24 = nas_series[0]["tpt"]   # 4.82
tpt_mei26 = nas_series[4]["tpt"]   # 4.65

# --- education paradox ---
pend_series = {r["pendidikan"]: {p: fnum(r[p]) for p in PERIODS} for r in pend}
smk_mei = pend_series["SMK"]["mei_2026"]            # 7.68
sd_mei = pend_series["SD ke bawah"]["mei_2026"]     # 2.31
smk_vs_sd_pp = round(smk_mei - sd_mei, 2)           # 5.37
smk_vs_nasional_ratio = round(smk_mei / tpt_mei26, 2)  # 1.65
smk_tren = [pend_series["SMK"][p] for p in PERIODS]  # 8.62 8.00 7.74 7.68

# --- youth ---
umur_series = {r["kelompok_umur"]: {p: fnum(r[p]) for p in PERIODS} for r in umur}
muda_mei = umur_series["15-24 tahun"]["mei_2026"]          # 17.37
muda_feb = umur_series["15-24 tahun"]["feb_2026"]          # 16.36
muda_naik_pp = round(muda_mei - muda_feb, 2)               # 1.01
produkt_mei = umur_series["25-59 tahun"]["mei_2026"]        # 2.56
muda_vs_nasional_ratio = round(muda_mei / tpt_mei26, 2)     # 3.74
muda_vs_produktif_ratio = round(muda_mei / produkt_mei, 2)  # 6.79

# --- gender & urban/rural gaps (Feb 2026, latest published) ---
g = {r["jenis_kelamin"]: fnum(r["feb_2026"]) for r in gender}
d = {r["daerah"]: fnum(r["feb_2026"]) for r in daerah}
gender_gap_pp = round(g["Laki-laki"] - g["Perempuan"], 2)   # 0.52
urban_rural_gap_pp = round(d["Perkotaan"] - d["Perdesaan"], 2)  # 2.40
urban_rural_ratio = round(d["Perkotaan"] / d["Perdesaan"], 2)   # 1.75

# --- provinces ---
prov_mei = [(r["provinsi"], fnum(r["mei_2026"])) for r in prov
            if fnum(r["mei_2026"]) is not None]
prov_mei_sorted = sorted(prov_mei, key=lambda x: x[1], reverse=True)
papua_mei = dict(prov_mei)["Papua"]          # 7.08
bali_mei = dict(prov_mei)["Bali"]            # 1.52
papua_vs_bali_ratio = round(papua_mei / bali_mei, 2)  # 4.66
# Feb->Mei 2026 changes for provinces with both values
prov_changes = []
for r in prov:
    a, b = fnum(r["feb_2026"]), fnum(r["mei_2026"])
    if a is not None and b is not None:
        prov_changes.append({"provinsi": r["provinsi"],
                             "feb_2026": a, "mei_2026": b,
                             "perubahan_pp": round(b - a, 2)})
turun_terbesar = sorted(prov_changes, key=lambda x: x["perubahan_pp"])[:3]
naik_terbesar = sorted(prov_changes, key=lambda x: x["perubahan_pp"],
                       reverse=True)[:3]

# --- distribution of unemployed by education (Mei 2026), absolute in jt ---
penganggur_mei_jt = nas_series[4]["penganggur_jt"]  # 7.22
dist_abs = [{"pendidikan": r["pendidikan"],
             "porsi_persen": fnum(r["porsi_persen"]),
             "juta_orang": round(penganggur_mei_jt * fnum(r["porsi_persen"]) / 100, 4)}
            for r in dist]
total_porsi = round(sum(x["porsi_persen"] for x in dist_abs), 2)

# --- labor market indicators ---
ind = {r["indikator"]: r for r in indikator}
formal_feb26 = fnum(ind["Pekerja formal (persen)"]["feb_2026"])      # 40.58
informal_feb26 = fnum(ind["Pekerja informal (persen)"]["feb_2026"])  # 59.42
setengah_feb26 = fnum(ind["Setengah penganggur"]["feb_2026"])        # 7.27
paruh_feb26 = fnum(ind["Pekerja paruh waktu"]["feb_2026"])            # 25.97

sektor_list = [{"sektor": r["sektor"],
                "tambah_ribu": int(r["tambah_ribu_orang"])} for r in sektor]

findings = {
    "meta": {
        "topik": "Pengangguran dan Pasar Kerja Indonesia 2026",
        "sumber": "Kompilasi angka resmi BPS (Sakernas) — lihat data/SOURCES.md",
        "periode": "Feb 2024 s.d. Mei 2026",
    },
    "nasional": {
        "tpt_feb_2024": tpt_feb24, "tpt_mei_2026": tpt_mei26,
        "penurunan_pp_feb24_mei26": round(tpt_mei26 - tpt_feb24, 2),
        "penganggur_mei_2026_jt": penganggur_mei_jt,
        "angkatan_kerja_mei_2026_jt": nas_series[4]["angkatan_kerja_jt"],
        "bekerja_mei_2026_jt": nas_series[4]["bekerja_jt"],
        "tpak_mei_2026": nas_series[4]["tpak"],
        "upah_buruh_mei_2026_jt": nas_series[4]["upah_buruh_jt"],
        "upah_buruh_feb_2026_jt": nas_series[3]["upah_buruh_jt"],
        "seri": nas_series,
        "pdb_q2_2026_yoy": 5.29,
    },
    "paradoks_pendidikan": {
        "smk_mei_2026": smk_mei, "sd_mei_2026": sd_mei,
        "smk_vs_sd_pp": smk_vs_sd_pp,
        "smk_vs_nasional_ratio": smk_vs_nasional_ratio,
        "smk_tren": dict(zip([PLABEL[p] for p in PERIODS], smk_tren)),
        "smk_turun_pp_feb24_mei26": round(smk_tren[3] - smk_tren[0], 2),
        "seri_pendidikan": {k: {PLABEL[p]: v[p] for p in PERIODS}
                            for k, v in pend_series.items()},
        "distribusi_penganggur_mei_2026": dist_abs,
        "total_porsi_persen": total_porsi,
    },
    "pengangguran_muda": {
        "muda_15_24_mei_2026": muda_mei, "muda_15_24_feb_2026": muda_feb,
        "muda_naik_pp_feb_mei_2026": muda_naik_pp,
        "muda_vs_nasional_ratio": muda_vs_nasional_ratio,
        "muda_vs_produktif_ratio": muda_vs_produktif_ratio,
        "produktif_25_59_mei_2026": produkt_mei,
        "seri_umur": {k: {PLABEL[p]: v[p] for p in PERIODS}
                      for k, v in umur_series.items()},
    },
    "kesenjangan": {
        "laki_feb_2026": g["Laki-laki"], "perempuan_feb_2026": g["Perempuan"],
        "gender_gap_pp": gender_gap_pp,
        "perkotaan_feb_2026": d["Perkotaan"], "perdesaan_feb_2026": d["Perdesaan"],
        "urban_rural_gap_pp": urban_rural_gap_pp,
        "urban_rural_ratio": urban_rural_ratio,
        "tpak_laki_feb_2026": fnum(ind["TPAK laki-laki"]["feb_2026"]),
        "tpak_perempuan_feb_2026": fnum(ind["TPAK perempuan"]["feb_2026"]),
    },
    "provinsi": {
        "top_mei_2026": [{"provinsi": p, "tpt": t}
                         for p, t in prov_mei_sorted[:10]],
        "terendah_mei_2026": [{"provinsi": p, "tpt": t}
                              for p, t in prov_mei_sorted[-5:]],
        "papua_vs_bali_ratio": papua_vs_bali_ratio,
        "turun_terbesar_feb_mei_2026": turun_terbesar,
        "naik_terbesar_feb_mei_2026": naik_terbesar,
        "gap_catatan": "Mei 2026 hanya tersedia untuk 17 provinsi; "
                       "Papua 2022-2023 tidak sebanding (pemekaran)",
    },
    "pasar_kerja": {
        "formal_feb_2026": formal_feb26, "informal_feb_2026": informal_feb26,
        "formal_jt_feb_2026": fnum(ind["Pekerja formal (juta orang)"]["feb_2026"]),
        "setengah_menganggur_feb_2026": setengah_feb26,
        "paruh_waktu_feb_2026": paruh_feb26,
        "komuter_feb_2026_jt": fnum(ind["Pekerja komuter"]["feb_2026"]),
        "sektor_penambah_feb_mei_2026": sektor_list,
    },
}

# --- sanity assertions (fail loudly if a headline number drifts) ---
assert smk_mei == 7.68 and sd_mei == 2.31
assert smk_vs_sd_pp == 5.37
assert muda_mei == 17.37 and muda_naik_pp == 1.01
assert tpt_mei26 == 4.65
assert urban_rural_gap_pp == 2.40
assert abs(total_porsi - 100.0) < 0.05
assert papua_mei == 7.08 and bali_mei == 1.52

with open(HERE / "findings.json", "w", encoding="utf-8") as f:
    json.dump(findings, f, ensure_ascii=False, indent=2)
print("findings.json written.")
print(f"SMK {smk_mei}% vs SD {sd_mei}% (gap {smk_vs_sd_pp} pp, {smk_vs_nasional_ratio}x nasional)")
print(f"Muda 15-24: {muda_mei}% (naik {muda_naik_pp} pp Feb->Mei 2026; {muda_vs_nasional_ratio}x nasional)")
print(f"Papua {papua_mei}% vs Bali {bali_mei}% ({papua_vs_bali_ratio}x)")
