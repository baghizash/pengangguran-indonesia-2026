#!/usr/bin/env python3
"""Load compiled CSVs into SQLite (regenerable; the .db is git-ignored)."""
import csv
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
D = HERE / "data" / "compiled"
DB = HERE / "data" / "pengangguran_2026.db"


def load(cur, table, path, numeric_cols):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    cols = rows[0].keys()
    defs = []
    for c in cols:
        if c in numeric_cols:
            defs.append(f'"{c}" REAL')
        else:
            defs.append(f'"{c}" TEXT')
    cur.execute(f'DROP TABLE IF EXISTS "{table}"')
    cur.execute(f'CREATE TABLE "{table}" ({", ".join(defs)})')
    for r in rows:
        vals = []
        for c in cols:
            v = (r[c] or "").strip()
            if c in numeric_cols:
                vals.append(float(v.replace(",", ".")) if v else None)
            else:
                vals.append(v if v else None)
        cur.execute(
            f'INSERT INTO "{table}" VALUES ({",".join("?" * len(cols))})', vals)


def main():
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    cur = con.cursor()
    num = {"tpt_persen", "angkatan_kerja_jt", "tpak_persen", "bekerja_jt",
           "penganggur_jt", "upah_buruh_jt", "feb_2024", "feb_2025",
           "feb_2026", "mei_2026", "agu_2022", "agu_2023", "agu_2024",
           "agu_2025", "porsi_persen", "tambah_ribu_orang"}
    load(cur, "tpt_nasional", D / "tpt_nasional_series.csv", num)
    load(cur, "tpt_pendidikan", D / "tpt_pendidikan.csv", num)
    load(cur, "tpt_umur", D / "tpt_umur.csv", num)
    load(cur, "tpt_gender", D / "tpt_gender.csv", num)
    load(cur, "tpt_daerah", D / "tpt_daerah.csv", num)
    load(cur, "tpt_provinsi", D / "tpt_provinsi.csv", num)
    load(cur, "distribusi_penganggur", D / "distribusi_penganggur_pendidikan.csv", num)
    load(cur, "pasar_kerja", D / "pasar_kerja_indikator.csv", num)
    load(cur, "sektor", D / "sektor_penambah_pekerja.csv", num)
    con.commit()
    tables = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")]
    for t in tables:
        n = cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        print(f"{t}: {n} rows")
    con.close()
    print("DB:", DB)


if __name__ == "__main__":
    main()
