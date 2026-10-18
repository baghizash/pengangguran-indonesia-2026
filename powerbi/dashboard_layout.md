# Layout Dashboard Power BI — Pengangguran Indonesia 2026

Dashboard 4 halaman. Tabel: `fact_tpt_nasional`, `fact_tpt_segmen`,
`fact_indikator`, `fact_sektor`, `dim_periode`, `dim_segmen`.
Measure dari `measures_dax.md`.

## Slicer global (semua halaman)

| Slicer | Sumber |
|---|---|
| Periode | `dim_periode[periode]` |
| Dimensi segmen | `dim_segmen[dimensi]` (pendidikan/umur/gender/daerah/provinsi) |

## Halaman 1 — Overview

Judul: **Pengangguran Indonesia 2026 — Sekilas**

| Visual | Isi |
|---|---|
| 4 kartu KPI | `[TPT Nasional]`, `[Penganggur (jt)]`, `[Angkatan Kerja (jt)]`, `[Upah Buruh Rata-rata (jt)]` — periode Mei 2026 |
| Line chart | `[TPT Nasional]` per `dim_periode[periode]` (Feb 2024 → Mei 2026) |
| Bar chart | `[TPT Segmen]` per pendidikan, periode Mei 2026 (sorot SMK) |
| Tabel | Top 5 provinsi TPT tertinggi + 5 terendah (Mei 2026) |

**Insight:** TPT nasional turun ke 4,65%, tapi SMK 7,68% dan muda 17,37%.

## Halaman 2 — Paradoks Pendidikan

Judul: **Paradoks Pendidikan — Ijazah Tinggi, Pengangguran Tinggi**

| Visual | Isi |
|---|---|
| Bar chart | `[TPT Segmen]` per jenjang pendidikan (Mei 2026), urut menurun |
| Line chart | Tren SMK vs SMA vs Diploma IV/S1+ (Feb 2024 → Mei 2026) |
| Bar chart | `[Gap vs Nasional (pp)]` per jenjang pendidikan |
| Tabel | Distribusi penganggur: porsi % + juta orang per pendidikan |

**Insight:** SMK 7,68% = 1,65x rata-rata nasional; gap SMK vs SD 5,37 pp.

## Halaman 3 — Pengangguran Muda & Wilayah

Judul: **Anak Muda & Ketimpangan Wilayah**

| Visual | Isi |
|---|---|
| Bar chart | `[TPT Segmen]` per kelompok umur (Mei 2026) |
| Line chart | Tren 15-24 thn vs 25-59 thn (Feb 2024 → Mei 2026) — sorot kenaikan muda saat nasional turun |
| Bar chart horizontal | TPT per provinsi (Mei 2026), top 15 |
| Bar chart | Gender gap + gap perkotaan vs perdesaan (Feb 2026) |

**Insight:** muda 17,37% naik 1,01 pp saat TPT nasional turun; Papua 7,08% = 4,66x Bali.

## Halaman 4 — Upah & Formalitas

Judul: **Upah Naik, Tapi 6 dari 10 Pekerja Informal**

| Visual | Isi |
|---|---|
| Line chart | `[Upah Buruh Rata-rata (jt)]` per periode (Feb 2026 → Mei 2026) |
| Donut chart | `[Pekerja Formal %]` vs `[Pekerja Informal %]` (Feb 2026) |
| Bar chart | `[Setengah Menganggur %]`, `[Pekerja Paruh Waktu %]` |
| Bar chart | `fact_sektor[tambah_ribu_orang]` per sektor (Feb-Mei 2026) |

**Insight:** upah Rp3,39 jt tapi 59,42% pekerja informal; lapangan kerja baru dari jasa.

## Tips format

- Skema warna: navy `#1E3A8A` untuk nasional, merah `#C0392B` untuk sorotan masalah (SMK, muda, Papua), teal `#0D9488` untuk pembanding.
- Semua TPT: 2 desimal + tanda %.
- Judul tiap visual: kalimat insight, bukan nama kolom.
