# Panduan Rakit Dashboard — Power BI Desktop (Windows)

Waktu: sekitar 20–30 menit. File CSV ada di folder `powerbi/` proyek ini.

## Langkah 1 — Import data

1. Buka Power BI Desktop > **Get Data > Text/CSV**.
2. Import 6 file: `fact_tpt_nasional.csv`, `fact_tpt_segmen.csv`,
   `fact_indikator.csv`, `fact_sektor.csv`, `dim_periode.csv`,
   `dim_segmen.csv`.
3. Pastikan tipe kolom numerik terdeteksi sebagai Decimal Number,
   `periode_id`/`urutan` sebagai Whole Number.

## Langkah 2 — Relasi (Model view)

Buat relasi one-to-many (single direction, dari dimensi ke fakta):

| Dari | Ke |
|---|---|
| `dim_periode[periode_id]` | `fact_tpt_nasional[periode_id]` |
| `dim_periode[periode_id]` | `fact_tpt_segmen[periode_id]` |
| `dim_periode[periode_id]` | `fact_indikator[periode_id]` |
| `dim_segmen[segmen]` | `fact_tpt_segmen[segmen]` |

`fact_sektor` tidak perlu relasi (satu periode saja).

## Langkah 3 — Urutan kategori

1. Pilih kolom `dim_periode[periode]`, lalu **Sort by Column >
   `urutan`**.
2. Pilih kolom `dim_segmen[segmen]`, lalu **Sort by Column >
   `urutan`**.

## Langkah 4 — Measure DAX

1. Baca dulu `measures_dax_CATATAN_LEVEL.md` (2 menit, penting).
2. Klik kanan `fact_tpt_nasional` > **New measure**, tempel measure
   bagian 1 dari `measures_dax.md`.
3. Klik kanan `fact_tpt_segmen` > **New measure**, tempel measure
   bagian 2.
4. Klik kanan `fact_indikator` > **New measure**, tempel measure
   bagian 3.

## Langkah 5 — Bangun 4 halaman

Ikuti `dashboard_layout.md` halaman per halaman. Pasang slicer
`dim_periode[periode]` di tiap halaman. Untuk halaman 2, filter visual
ke `dim_segmen[dimensi] = "pendidikan"`; halaman 3 ke
`"umur"`/`"provinsi"`/`"gender"`/`"daerah"` sesuai visual.

## Langkah 6 — Cek akhir

Samakan dengan tabel di `measures_dax_CATATAN_LEVEL.md`:
TPT nasional Mei 2026 = 4,65%; SMK = 7,68%; SD = 2,31%;
15-24 thn = 17,37%; Papua = 7,08%; Bali = 1,52%.
Kalau beda, cek relasi dan filter halaman dulu.

## Langkah 7 — Publish (opsional)

**File > Publish > Publish to Power BI** (butuh akun Power BI)
untuk dibagikan via link.
