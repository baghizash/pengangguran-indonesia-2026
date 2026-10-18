# Sumber Data — Analisis Pengangguran Indonesia 2026

## Sifat dataset: KOMPILASI, bukan file mentah resmi

Dataset ini **dikompilasi** dari angka-angka resmi yang dipublikasikan
(BPS melalui Berita Resmi Statistik Sakernas, serta media yang mengutip
BPS secara eksak). Tidak ada file CSV mentah Sakernas yang bisa diunduh
publik pada saat proyek ini dibuat (dicek 18 Oktober 2026). Setiap angka
di bawah ini dicatat bersama sumber dan tanggalnya. Tidak ada satu pun
angka yang dikarang. Angka yang diturunkan dari selisih yang
dipublikasikan ditandai "diturunkan" di kolom catatan CSV.

## Sumber per angka

### Seri nasional (tpt_nasional_series.csv)

| Angka | Nilai | Sumber | Tanggal rilis |
|---|---|---|---|
| TPT Feb 2026 4,68%; AK 154,91 jt; TPAK 70,56%; bekerja 147,67 jt; upah Rp3,29 jt; pertanian 42,49 jt (28,78%); formal 59,93 jt (40,58%) | — | BPS, BRS "Tingkat Pengangguran Terbuka (TPT) sebesar 4,68 persen" | 5 Mei 2026 |
| TPT Mei 2026 4,65%; AK 155,41 jt; TPAK 70,57%; bekerja 148,19 jt; penganggur 7,22 jt; upah Rp3,39 jt; pertanian 42,60 jt (28,75%) | — | BPS, BRS "Tingkat Pengangguran Terbuka (TPT) sebesar 4,65 persen" | 5 Agu 2026 |
| TPT Feb 2024 4,82%; Feb 2025 4,76% | — | BPS BRS No. 49/05/Th. XXIX, dikutip web-api.bps.go.id | 5 Mei 2026 |
| TPT Agu 2025 4,85% | — | Tabel GoodStats "Indikator Pasar Tenaga Kerja Indonesia Februari 2026" yang mengutip BPS | Jun 2026 |
| Penganggur Feb 2026 7,24 jt | 7,24 | BPS via media (pluang/satujabar mengutip BPS); konsisten dengan 154,91 − 147,67 | Mei 2026 |
| PDB triwulan II-2026 tumbuh 5,29% YoY | 5,29 | BPS via beritanasionalupdate mengutip Kepala BPS | 5 Agu 2026 |

### TPT menurut pendidikan (tpt_pendidikan.csv)

| Periode | Sumber |
|---|---|
| Feb 2024, Feb 2025, Feb 2026 (semua jenjang) | BPS BRS No. 49/05/Th. XXIX, tabel "TPT Menurut Pendidikan Tertinggi yang Ditamatkan", dikutip web-api.bps.go.id |
| Mei 2026 (SMK 7,68; SMA 6,17; DIV/S1/S2/S3 6,09; DI/DII/DIII 4,75; SMP 4,16; SD 2,31) | GoodStats "SMK Jadi Kelompok dengan Tingkat Pengangguran Tertinggi Mei 2026" yang mengutip BPS |
| SMK 13,12% dari penduduk bekerja (Mei 2026) | GoodStats, mengutip BPS |

### TPT menurut umur (tpt_umur.csv)

| Periode | Sumber |
|---|---|
| Feb 2024, Feb 2025, Feb 2026 (15–24: 16,42/16,16/16,36; 25–59: 3,08/3,04/2,93; 60+: 1,14/1,67/1,89) | BPS BRS No. 49/05/Th. XXIX, tabel "TPT Menurut Kelompok Umur", dikutip web-api.bps.go.id |
| Mei 2026 (15–24: 17,37; 25–59: 2,56; 60+: 2,35) | investortrust.id "Penganggur Terbuka Mei 2026 Tinggal 7,2 Juta", mengutip BPS |

### TPT menurut gender dan daerah (tpt_gender.csv, tpt_daerah.csv)

BPS BRS No. 49/05/Th. XXIX (Feb 2024/2025/2026), dikutip web-api.bps.go.id
dan bitgetapp/jakarta365 yang mengutip BPS. Nilai Mei 2026 tidak
dipublikasikan di abstrak BRS Mei 2026 — dicatat sebagai gap.

### TPT provinsi (tpt_provinsi.csv)

| Periode | Sumber |
|---|---|
| Agu 2022, Agu 2023, Agu 2024, Agu 2025, Feb 2026 (38 provinsi) | Bappenas SIMREG "Capaian Indikator Utama Pembangunan — Tingkat Pengangguran Terbuka", simreg.bappenas.go.id (data BPS) |
| Mei 2026 top 10 + terbawah + perubahan Feb→Mei | GoodStats "10 Provinsi dengan Tingkat Pengangguran Tertinggi per Mei 2026" dan "…Terendah 2026"; investortrust.id; genvoice.id — semuanya mengutip BPS |

Catatan: Papua 2022–2023 adalah Papua sebelum pemekaran (wilayah jauh
lebih luas); 2024+ adalah Papua hasil pemekaran. Tren 2022→2024 untuk
Papua tidak sebanding langsung — dicatat di kolom catatan CSV dan tidak
dipakai untuk klaim tren.

### Distribusi penganggur menurut pendidikan (distribusi_penganggur_pendidikan.csv)

investortrust.id, mengutip BPS Sakernas Mei 2026: SMA 28%; SMK 22,39%;
SD ke bawah 17,18%; SMP 15,65%; Diploma IV–S3 14,31%; Diploma I–III 2,48%.

### Indikator pasar kerja (pasar_kerja_indikator.csv)

- Formal 40,58% (59,93 jt), turun 0,02 pp vs Feb 2025 — satujabar.com mengutip BPS
- Informal 59,42% — harianbasis.co mengutip BPS
- Setengah penganggur 7,27% (turun 0,74 pp), paruh waktu 25,97% (naik 0,16 pp), komuter 7,19 jt — satujabar.com mengutip BPS
- TPAK laki-laki 84,57%, perempuan 56,41% — harianbasis.co mengutip BPS
- PMI Manufaktur Apr 2026 49,1 (kontraksi) — harianbasis.co mengutip S&P Global

### Sektor penambah pekerja (sektor_penambah_pekerja.csv)

BPS via beritanasionalupdate (5 Agu 2026): akomodasi & makan minum +195
rb; transportasi & pergudangan +121 rb; jasa lainnya +110 rb (Feb→Mei 2026).

## Batasan yang harus dipahami

- TPT mengukur pengangguran terbuka saja; tidak mencakup setengah
  penganggur dan pekerja paruh waktu yang ingin jam kerja lebih.
- TPT rendah pada kelompok berpendidikan dasar bukan berarti pekerjaan
  lebih baik — kelompok ini terserap ke pekerjaan informal berproduktivitas
  rendah karena tidak bisa menunggu pekerjaan yang sesuai.
- Perbandingan antarprovinsi tidak mengontrol struktur ekonomi daerah
  (mis. dominasi sektor informal menekan TPT secara mekanis).
- Nilai Mei 2026 untuk gender dan perkotaan/perdesaan tidak dipublikasikan
  di abstrak BRS — tidak diisi, tidak dikarang.
- Nilai provinsi Mei 2026 hanya tersedia untuk 17 provinsi (top 10,
  terbawah, dan yang perubahannya dilaporkan) — sisanya gap.
- Selisih angka di belakang koma antar sumber berasal dari pembulatan BPS.
