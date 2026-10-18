# CATATAN LEVEL — Kenapa Ada Dua Tabel Fakta

Baca ini SEBELUM merakit dashboard. Ini pelajaran dari proyek Harga
Cabai 2026: di sana satu tabel fakta mencampur baris Nasional dan baris
provinsi, sehingga measure `MAX`/`CV`/`RANKX` diam-diam salah kalau
slicer provinsi dibiarkan "All".

Di proyek ini jebakan itu **dihilangkan sejak desain data**:

- `fact_tpt_nasional` — HANYA 5 baris agregat nasional
  (Feb 2024, Feb 2025, Agu 2025, Feb 2026, Mei 2026).
- `fact_tpt_segmen` — HANYA 250 baris level segmen
  (pendidikan, umur, gender, daerah, provinsi). Tidak ada satu pun
  baris "Nasional"/"Indonesia" di sini (diverifikasi oleh
  `scripts/build_powerbi.py`).
- `fact_indikator` dan `fact_sektor` — tabel pendukung yang jelas
  terpisah (indikator pasar kerja & penambah lapangan kerja).

Konsekuensinya untuk DAX:

1. Measure nasional (`[TPT Nasional]`) dan measure segmen
   (`[TPT Segmen]`) tidak akan pernah saling mengontaminasi, filter
   apapun yang dipasang.
2. `[Gap vs Nasional (pp)] = [TPT Segmen] - [TPT Nasional]` aman:
   `[TPT Nasional]` mengikuti periode visual lewat relasi
   `dim_periode` yang sama, tanpa perlu `ALL()` atau filter khusus.
3. `RANKX` per segmen aman karena dimensi segmen tidak mengandung
   baris nasional.

Satu-satunya yang perlu diingat: jangan membuat measure yang
menjumlahkan/menghitung lintas kedua tabel fakta sekaligus (mis.
`COUNTROWS` gabungan) — tidak ada visual di layout yang membutuhkannya.

## Angka yang harus muncul (cek akhir sebelum publish)

| Visual | Angka benar |
|---|---|
| KPI TPT Nasional (Mei 2026) | 4,65% |
| Bar SMK (Mei 2026) | 7,68% |
| Bar SD ke bawah (Mei 2026) | 2,31% |
| Gap SMK vs SD | 5,37 pp |
| Bar 15-24 thn (Mei 2026) | 17,37% |
| Bar Papua (Mei 2026) | 7,08% |
| Bar Bali (Mei 2026) | 1,52% |

Kalau ada yang beda, cek relasi `periode_id`/`segmen` dulu sebelum
mengira datanya salah.
