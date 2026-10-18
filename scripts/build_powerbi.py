#!/usr/bin/env python3
"""Build Power BI star-schema kit in powerbi/.

DESIGN (lesson from the cabai project): national-aggregate rows and
segment rows live in SEPARATE fact tables. They are never mixed, so no
DAX guard is needed to keep MAX/RANK/AVERAGE correct. See
measures_dax_CATATAN_LEVEL.md.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
D = HERE / "data" / "compiled"
P = HERE / "powerbi"
P.mkdir(exist_ok=True)


def read(name):
    with open(D / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(name, fieldnames, rows):
    with open(P / name, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"powerbi/{name}: {len(rows)} rows")


def fnum(x):
    x = (x or "").strip()
    return float(x.replace(",", ".")) if x else None


# ---------- dim_periode ----------
periode_def = [
    (1, "Agu 2022", 2022, 8), (2, "Agu 2023", 2023, 8),
    (3, "Feb 2024", 2024, 2), (4, "Agu 2024", 2024, 8),
    (5, "Feb 2025", 2025, 2), (6, "Agu 2025", 2025, 8),
    (7, "Feb 2026", 2026, 2), (8, "Mei 2026", 2026, 5),
]
# contiguous order within the national Sakernas series (for prev-period DAX)
nas_order = {"Feb 2024": 1, "Feb 2025": 2, "Agu 2025": 3,
             "Feb 2026": 4, "Mei 2026": 5}
write("dim_periode.csv",
      ["periode_id", "periode", "tahun", "bulan", "urutan", "urutan_nasional"],
      [{"periode_id": i, "periode": p, "tahun": t, "bulan": b, "urutan": i,
        "urutan_nasional": nas_order.get(p, "")}
       for i, p, t, b in periode_def])
PID = {p: i for i, p, _, _ in periode_def}

# ---------- fact_tpt_nasional (ONLY national aggregates) ----------
nas = read("tpt_nasional_series.csv")
rows = []
for r in nas:
    rows.append({
        "periode_id": PID[r["periode"]],
        "tpt_persen": r["tpt_persen"],
        "angkatan_kerja_jt": r["angkatan_kerja_jt"],
        "tpak_persen": r["tpak_persen"],
        "bekerja_jt": r["bekerja_jt"],
        "penganggur_jt": r["penganggur_jt"],
        "upah_buruh_jt": r["upah_buruh_jt"],
    })
write("fact_tpt_nasional.csv",
      ["periode_id", "tpt_persen", "angkatan_kerja_jt", "tpak_persen",
       "bekerja_jt", "penganggur_jt", "upah_buruh_jt"], rows)

# ---------- fact_tpt_segmen (ONLY segment rows; national NEVER appears here) ----------
seg_rows = []


def add_seg(csv_name, key_col, dimensi, colmap):
    for r in read(csv_name):
        for col, p in colmap.items():
            v = fnum(r[col])
            if v is not None:
                seg_rows.append({"periode_id": PID[p], "dimensi": dimensi,
                                 "segmen": r[key_col], "tpt_persen": v})


COL4 = {"feb_2024": "Feb 2024", "feb_2025": "Feb 2025",
        "feb_2026": "Feb 2026", "mei_2026": "Mei 2026"}
add_seg("tpt_pendidikan.csv", "pendidikan", "pendidikan", COL4)
add_seg("tpt_umur.csv", "kelompok_umur", "umur", COL4)
add_seg("tpt_gender.csv", "jenis_kelamin", "gender",
        {"feb_2024": "Feb 2024", "feb_2025": "Feb 2025", "feb_2026": "Feb 2026"})
add_seg("tpt_daerah.csv", "daerah", "daerah",
        {"feb_2024": "Feb 2024", "feb_2025": "Feb 2025", "feb_2026": "Feb 2026"})
pmap = {"agu_2022": "Agu 2022", "agu_2023": "Agu 2023", "agu_2024": "Agu 2024",
        "agu_2025": "Agu 2025", "feb_2026": "Feb 2026", "mei_2026": "Mei 2026"}
for r in read("tpt_provinsi.csv"):
    for c, p in pmap.items():
        v = fnum(r[c])
        if v is not None:
            seg_rows.append({"periode_id": PID[p], "dimensi": "provinsi",
                             "segmen": r["provinsi"], "tpt_persen": v})
write("fact_tpt_segmen.csv",
      ["periode_id", "dimensi", "segmen", "tpt_persen"], seg_rows)

# ---------- dim_segmen ----------
dim_defs = [
    ("pendidikan", ["SD ke bawah", "SMP", "Diploma I/II/III", "SMA",
                    "Diploma IV/S1/S2/S3", "SMK"]),
    ("umur", ["15-24 tahun", "25-59 tahun", "60 tahun ke atas"]),
    ("gender", ["Laki-laki", "Perempuan"]),
    ("daerah", ["Perkotaan", "Perdesaan"]),
    ("provinsi", sorted({r["segmen"] for r in seg_rows
                         if r["dimensi"] == "provinsi"})),
]
drows = []
for dim, segs in dim_defs:
    for i, s in enumerate(segs, 1):
        drows.append({"segmen": s, "dimensi": dim, "urutan": i})
write("dim_segmen.csv", ["segmen", "dimensi", "urutan"], drows)

# ---------- fact_indikator (supporting indicators, clearly separate) ----------
ind_map = {
    "Pekerja formal (persen)": ("formal_persen", "persen"),
    "Pekerja informal (persen)": ("informal_persen", "persen"),
    "Setengah penganggur": ("setengah_menganggur_persen", "persen"),
    "Pekerja paruh waktu": ("paruh_waktu_persen", "persen"),
    "Pekerja komuter": ("komuter_jt", "juta orang"),
    "TPAK laki-laki": ("tpak_laki_persen", "persen"),
    "TPAK perempuan": ("tpak_perempuan_persen", "persen"),
    "Pekerja formal (juta orang)": ("formal_jt", "juta orang"),
}
irows = []
for r in read("pasar_kerja_indikator.csv"):
    if r["indikator"] not in ind_map:
        continue
    kode, satuan = ind_map[r["indikator"]]
    for c, p in [("feb_2025", "Feb 2025"), ("feb_2026", "Feb 2026"),
                 ("mei_2026", "Mei 2026")]:
        v = fnum(r[c])
        if v is not None:
            irows.append({"periode_id": PID[p], "indikator": kode,
                          "nilai": v, "satuan": satuan})
write("fact_indikator.csv", ["periode_id", "indikator", "nilai", "satuan"], irows)

# ---------- fact_sektor ----------
srows = [{"sektor": r["sektor"], "periode": "Feb-Mei 2026",
          "tambah_ribu_orang": r["tambah_ribu_orang"]}
         for r in read("sektor_penambah_pekerja.csv")]
write("fact_sektor.csv", ["sektor", "periode", "tambah_ribu_orang"], srows)

# ---------- sanity checks ----------
assert all(r["tpt_persen"] for r in
           [x for x in seg_rows])  # no null keys/values
assert not any(r["segmen"].lower() == "nasional" for r in seg_rows)
assert not any(r["segmen"].lower() == "indonesia" for r in seg_rows)
print("OK: fact_tpt_segmen contains no national rows; no nulls in keys.")
