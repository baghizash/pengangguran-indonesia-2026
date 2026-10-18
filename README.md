# Analisis Pengangguran Indonesia 2026

**Paradoks pendidikan: makin tinggi ijazah, makin tinggi pengangguran.**

> **Pernyataan data:** dataset ini **dikompilasi dari angka resmi BPS**
> (Survei Angkatan Kerja Nasional / Sakernas, via Berita Resmi Statistik
> dan publikasi yang mengutip BPS secara eksak). Tidak ada file CSV
> mentah Sakernas yang dapat diunduh publik — setiap angka dicatat
> bersama sumbernya di [`data/SOURCES.md`](data/SOURCES.md). Tidak ada
> satu pun angka yang dikarang; gap data ditandai eksplisit, bukan diisi.

## Temuan kunci (Mei 2026, Sakernas BPS)

- **TPT nasional 4,65%** — turun perlahan dari 4,82% (Feb 2024). Di balik
  angka yang tenang ini ada ketimpangan yang tajam.
- **Paradoks pendidikan:** lulusan **SMK 7,68%** — tertinggi dari semua
  jenjang, **1,65x rata-rata nasional** dan selisih **5,37 poin** dari
  lulusan SD ke bawah (2,31%). SMK turun dari 8,62% (Feb 2024) tapi tetap
  nomor satu. Lulusan SMA 6,17% dan Diploma IV/S1/S2/S3 6,09% juga di
  atas rata-rata nasional.
- **Pengangguran muda meledak:** usia **15–24 tahun 17,37%** — naik
  1,01 poin Feb→Mei 2026 *saat TPT nasional justru turun*. 3,74x
  rata-rata nasional, 6,79x kelompok usia produktif (25–59 thn: 2,56%).
- **Kesenjangan wilayah & gender (Feb 2026):** perkotaan 5,60% vs
  perdesaan 3,20% (gap 2,40 pp); laki-laki 4,88% vs perempuan 4,36%.
- **Jurang provinsi:** Papua 7,08% vs Bali 1,52% — **4,66x lipat**.
  Pusat industri pun tertekan: Jawa Barat 6,61%, Banten 6,48%,
  DKI Jakarta 5,79%.
- **7,22 juta penganggur:** porsi terbesar lulusan **SMA 28%**
  (2,02 jt orang), lalu SMK 22,39% (1,62 jt).
- **Kualitas pekerjaan:** hanya **40,58% pekerja formal**; 59,42%
  informal. Setengah menganggur 7,27%, pekerja paruh waktu 25,97%.
- **Upah naik:** rata-rata upah buruh Rp3,39 jt (Mei 2026) dari Rp3,29 jt
  (Feb 2026). Lapangan kerja baru Feb→Mei 2026 datang dari jasa:
  akomodasi & makan minum +195 rb, transportasi & pergudangan +121 rb.

## Struktur proyek

```
pengangguran-2026/
├── analysis.ipynb            # notebook analisis
├── README.md
├── findings.json             # semua angka kunci (dihitung dari data)
├── data/
│   ├── compiled/            # 9 CSV kompilasi + SOURCES.md
│   ├── pengangguran_2026.db # hasil generate (git-ignored, bisa dibuat ulang)
│   └── SOURCES.md           # sumber per angka
├── sql/queries.sql           # 16 query verifikasi
├── scripts/
│   ├── analyze.py           # hitung findings.json (+assertion)
│   ├── load_to_sqlite.py    # CSV -> SQLite
│   ├── make_charts.py       # 10 chart PNG
│   └── build_powerbi.py     # rakit star schema powerbi/
├── charts/                   # 10 chart PNG
├── powerbi/                  # KIT DASHBOARD POWER BI
│   ├── fact_tpt_nasional.csv / fact_tpt_segmen.csv / fact_indikator.csv / fact_sektor.csv
│   ├── dim_periode.csv / dim_segmen.csv
│   ├── measures_dax.md      # measure siap tempel
│   ├── measures_dax_CATATAN_LEVEL.md  # BACA DULU: desain anti-jebakan
│   ├── dashboard_layout.md  # layout 4 halaman
│   └── build_guide.md       # langkah rakit di Power BI Desktop
├── requirements.txt
└── .gitignore
```

## Cara reproduksi

```bash
~/workspace/mienv/bin/python scripts/analyze.py        # findings.json
~/workspace/mienv/bin/python scripts/load_to_sqlite.py # data/pengangguran_2026.db
~/workspace/mienv/bin/python scripts/make_charts.py    # charts/*.png
~/workspace/mienv/bin/python scripts/build_powerbi.py  # powerbi/*.csv
```

## Batasan

- TPT hanya mengukur pengangguran *terbuka*; setengah menganggur dan
  pekerja paruh waktu dicatat terpisah.
- TPT rendah pada lulusan SD bukan berarti pekerjaan lebih baik —
  mereka terserap ke informal karena tak bisa menunggu pekerjaan sesuai.
- Nilai Mei 2026 untuk gender & perkotaan/perdesaan tidak dipublikasikan
  di abstrak BRS (gap, tidak dikarang). Nilai provinsi Mei 2026 hanya
  untuk 17 provinsi.
- Seri Papua 2022–2023 tidak sebanding dengan 2024+ (pemekaran provinsi).
