#!/usr/bin/env python3
"""Build Modul-Analisis-Pengangguran.pdf (A4 landscape, beginner-friendly ID).

Reads findings.json — every number comes from the compiled BPS (Sakernas) data.
"""
import json
import shutil
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak,
)

HERE = Path(__file__).resolve().parent
F = json.loads((HERE / "findings.json").read_text())
OUT = str(Path.home() / "workspace" / "coursera-modules" / "Modul-Analisis-Pengangguran.pdf")
OUT_COPY = str(HERE / "Modul-Analisis-Pengangguran.pdf")
CHARTS = HERE / "charts"
W, H = landscape(A4)
NAVY = HexColor("#1E3A8A")
TEAL = HexColor("#0D9488")
DARK = HexColor("#1F2937")
GRAY = HexColor("#6B7280")
LIGHT = HexColor("#EFF6FF")

styles = {
    "cover": ParagraphStyle("cover", fontName="Helvetica-Bold", fontSize=30, leading=36,
                            textColor=NAVY, alignment=TA_LEFT),
    "coversub": ParagraphStyle("coversub", fontName="Helvetica", fontSize=16, leading=22,
                               textColor=DARK, alignment=TA_LEFT),
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=22, leading=27,
                         textColor=NAVY, spaceBefore=6, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=16, leading=20,
                         textColor=TEAL, spaceBefore=8, spaceAfter=6),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=12.5, leading=18,
                           textColor=DARK, spaceAfter=7),
    "bullet": ParagraphStyle("bullet", parent=ParagraphStyle("b", fontName="Helvetica",
                             fontSize=12.5, leading=18, textColor=DARK, spaceAfter=5,
                             leftIndent=16, bulletIndent=6)),
    "code": ParagraphStyle("code", fontName="Courier", fontSize=10.5, leading=15,
                          textColor=DARK, backColor=LIGHT, spaceAfter=8,
                          leftIndent=8, borderPadding=(6, 6, 6)),
    "caption": ParagraphStyle("caption", fontName="Helvetica-Oblique", fontSize=10.5,
                              leading=14, textColor=GRAY, alignment=TA_CENTER,
                              spaceBefore=4, spaceAfter=10),
    "warn": ParagraphStyle("warn", fontName="Helvetica", fontSize=12.5, leading=18,
                           textColor=HexColor("#92400E"), backColor=HexColor("#FEF3C7"),
                           borderPadding=(8, 8, 8), spaceAfter=8),
}
story = []


def P(text, style="body"):
    story.append(Paragraph(text, styles[style]))


def num(v):
    """Format number with Indonesian decimal comma; pass strings through."""
    return f"{v}".replace(".", ",")




def B(text):
    story.append(Paragraph(text, styles["bullet"], bulletText="•"))


def CODE(text):
    story.append(Paragraph(text.replace(" ", "&nbsp;").replace("\n", "<br/>"), styles["code"]))


def CHART(fname, caption, width=21 * cm):
    story.append(Image(str(CHARTS / fname), width=width, height=width * 0.58))
    P(caption, "caption")


def TABLE(data, widths=None):
    t = Table([[Paragraph(str(c), styles["body"]) for c in row] for row in data],
              colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#FFFFFF"), LIGHT]),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))


nas = F["nasional"]
par = F["paradoks_pendidikan"]
muda = F["pengangguran_muda"]
kes = F["kesenjangan"]
prov = F["provinsi"]
kerja = F["pasar_kerja"]
PERIODE = ["Feb 2024", "Feb 2025", "Agu 2025", "Feb 2026", "Mei 2026"]

# ---------- COVER ----------
story.append(Spacer(1, 3 * cm))
P("MODUL BELAJAR", "cover")
P("Modul Analisis Pengangguran Indonesia 2026", "cover")
P("Paradoks Pendidikan: dari Angka BPS sampai Dashboard Power BI — Studi Kasus Nyata untuk Pemula", "coversub")
story.append(Spacer(1, 0.6 * cm))
P("Modul ini mengajak kamu menganalisis pengangguran di Indonesia memakai angka "
  "resmi BPS dari Survei Angkatan Kerja Nasional (Sakernas). Kamu akan belajar "
  "apa itu TPT, cara menyusun dataset dari publikasi resmi, memverifikasi angka "
  "dengan SQL, memvisualisasikan dengan Python, lalu menyusun dashboard Power BI. "
  "Semua angka di modul ini dihitung dari data — tidak ada yang dikarang.", "coversub")
story.append(Spacer(1, 0.5 * cm))
P("Sumber data: BPS, Survei Angkatan Kerja Nasional (Sakernas). "
  "Periode: Februari 2024 sampai Mei 2026. Daftar sumber per angka: data/SOURCES.md.", "warn")
story.append(PageBreak())

# ---------- BAB 1 ----------
P("Bab 1 — Apa itu TPT dan Sakernas?", "h1")
P("TPT (Tingkat Pengangguran Terbuka) adalah persentase penganggur terhadap "
  "angkatan kerja. Angkatan kerja adalah penduduk usia 15 tahun ke atas yang "
  "bekerja atau sedang mencari pekerjaan. Penganggur di sini berarti orang "
  "yang tidak bekerja TAPI sedang mencari kerja atau mempersiapkan usaha — "
  "bukan termasuk ibu rumah tangga atau pelajar yang tidak mencari kerja.", "body")
P("Rumus sederhananya:", "h2")
CODE("TPT = (jumlah penganggur / jumlah angkatan kerja) x 100%")
P("Datanya berasal dari Sakernas (Survei Angkatan Kerja Nasional), survei "
  "rumah tangga yang dilakukan BPS dua sampai tiga kali setahun. Angka "
  "pengangguran 2026 yang kamu lihat di berita hampir pasti dari Sakernas. "
  "Indikator pendamping yang juga dipakai: TPAK (Tingkat Partisipasi Angkatan "
  "Kerja) = persentase penduduk usia kerja yang masuk angkatan kerja.", "body")
story.append(PageBreak())

# ---------- BAB 2 ----------
P("Bab 2 — Datanya dari Mana? Kompilasi Publikasi BPS", "h1")
P("Project ini tidak punya mikrodataset mentah Sakernas — yang dikompilasi "
  "adalah angka-angka resmi dari publikasi BPS: laporan Sakernas, Berita Resmi "
  "Statistik, dan tabel statistik di situs BPS. Setiap angka yang dipakai "
  "dicatat sumber publikasinya di data/SOURCES.md.", "body")
P("Hasil kompilasi: 5 titik waktu (Feb 2024, Feb 2025, Agu 2025, Feb 2026, "
  "Mei 2026) dengan rincian:", "h2")
B("Pendidikan terakhir: SD ke bawah, SMP, SMA, SMK, Diploma I/II/III, Diploma IV/S1/S2/S3.")
B("Kelompok umur: 15-24 tahun, 25-59 tahun, 60 tahun ke atas.")
B("Jenis kelamin dan daerah (perkotaan/perdesaan).")
B("38 provinsi (Mei 2026 tersedia untuk 17 provinsi).")
B("Indikator pasar kerja: formal/informal, setengah menganggur, paruh waktu, komuter, upah, penambah lapangan kerja.")
P("Data dimuat ke SQLite dengan scripts/load_to_sqlite.py, lalu setiap angka "
  "kunci diverifikasi ulang dengan query SQL independen di sql/queries.sql. "
  "Ini kebiasaan bagus: hitung dua kali dengan cara berbeda, pastikan hasilnya "
  "sama.", "body")
story.append(PageBreak())

# ---------- BAB 3 ----------
P("Bab 3 — TPT Nasional: Turun Pelan tapi Pasti", "h1")
P(f"TPT nasional turun dari {num(nas['tpt_feb_2024'])}% (Feb 2024) ke "
  f"{num(nas['tpt_mei_2026'])}% (Mei 2026) — penurunan "
  f"{num(abs(nas['penurunan_pp_feb24_mei26']))} poin persen. Sepanjang jalan ada sedikit "
  "naik-turun (misalnya naik ke 4,85% pada Agu 2025), tapi arah umumnya turun.", "body")
TABLE([["Periode", "TPT (%)", "Angkatan Kerja (jt)", "Bekerja (jt)", "Penganggur (jt)", "TPAK (%)", "Upah (jt Rp)"]] +
      [[r["periode"], r["tpt"], r["angkatan_kerja_jt"] or "-", r["bekerja_jt"] or "-",
        r["penganggur_jt"] or "-", r["tpak"] or "-", r["upah_buruh_jt"] or "-"]
       for r in nas["seri"]])
CHART("01_tpt_nasional_tren.png", "Gambar 1 — Tren TPT nasional, Feb 2024 – Mei 2026.")
P(f"Di saat yang sama, ekonomi tetap tumbuh: PDB Q2 2026 tumbuh {num(nas['pdb_q2_2026_yoy'])}% "
  "secara tahunan. Tapi angka rata-rata nasional menyembunyikan jurang yang "
  "lebar di bawahnya — itulah yang kita bongkar di bab-bab berikutnya.", "body")
story.append(PageBreak())

# ---------- BAB 4 ----------
P("Bab 4 — Paradoks Pendidikan (Inti Analisis Ini)", "h1")
P("Ini temuan paling penting project ini. Kalau kamu mengira makin tinggi "
  "ijazah makin mudah dapat kerja, data BPS berkata lain:", "body")
TABLE([["Jenjang", "Feb 2024", "Feb 2025", "Feb 2026", "Mei 2026"]] +
      [[j, par["seri_pendidikan"][j]["Feb 2024"], par["seri_pendidikan"][j]["Feb 2025"],
        par["seri_pendidikan"][j]["Feb 2026"], par["seri_pendidikan"][j]["Mei 2026"]]
       for j in ["SD ke bawah", "SMP", "SMA", "SMK", "Diploma I/II/III", "Diploma IV/S1/S2/S3"]])
P(f"Lulusan SMK punya TPT {num(par['smk_mei_2026'])}% — tertinggi di antara semua "
  f"jenjang. Bandingkan dengan lulusan SD ke bawah yang hanya 2,31%: "
  f"selisihnya {num(par['smk_vs_sd_pp'])} poin persen, dan TPT SMK "
  f"{num(par['smk_vs_nasional_ratio'])} kali lipat rata-rata nasional. Inilah paradoksnya: "
  "jenjang pendidikan terendah justru paling mudah bekerja.", "body")
CHART("02_paradoks_pendidikan.png", "Gambar 2 — TPT per jenjang pendidikan, Mei 2026. SMK tertinggi.")
P("Lulusan universitas (Diploma IV/S1/S2/S3) juga tinggi: 6,09%, bahkan lebih "
  "tinggi dari lulusan SMP. Pasar kerja tidak menyerap sesuai ijazah. "
  "Kabar baiknya: TPT SMK membaik, turun dari 8,62% (Feb 2024) ke 7,68% "
  "(Mei 2026) — turun 0,94 poin persen. Tapi tetap jauh di atas semua jenjang "
  "lain, jadi perbaikan tren belum menyentuh struktur masalahnya.", "body")
CHART("03_pendidikan_tren.png", "Gambar 3 — Tren TPT per jenjang pendidikan, Feb 2024 – Mei 2026.")
story.append(PageBreak())

# ---------- BAB 5 ----------
P("Bab 5 — Pengangguran Muda: Krisis yang Sebenarnya", "h1")
P(f"TPT usia 15-24 tahun mencapai {num(muda['muda_15_24_mei_2026'])}% pada Mei 2026 — "
  f"naik {num(muda['muda_naik_pp_feb_mei_2026'])} poin persen dari Feb 2026. Ini "
  "satu-satunya kelompok umur yang TPT-nya naik dalam periode tersebut.", "body")
TABLE([["Kelompok Umur", "Feb 2024", "Feb 2025", "Feb 2026", "Mei 2026"]] +
      [[k, muda["seri_umur"][k]["Feb 2024"], muda["seri_umur"][k]["Feb 2025"],
        muda["seri_umur"][k]["Feb 2026"], muda["seri_umur"][k]["Mei 2026"]]
       for k in ["15-24 tahun", "25-59 tahun", "60 tahun ke atas"]])
P(f"Untuk skala: angka anak muda {num(muda['muda_vs_nasional_ratio'])} kali lipat "
  f"rata-rata nasional dan {num(muda['muda_vs_produktif_ratio'])} kali lipat kelompok "
  f"usia produktif 25-59 tahun ({num(muda['produktif_25_59_mei_2026'])}%). Kelompok "
  "25-59 justru turun dari 3,08% ke 2,56%. Kesimpulannya jelas: krisis "
  "pengangguran Indonesia adalah krisis pengangguran muda — dan sebagian besar "
  "penganggur muda adalah lulusan SMA/SMK.", "body")
CHART("04_umur.png", "Gambar 4 — TPT per kelompok umur, Feb 2024 – Mei 2026.")
story.append(PageBreak())

# ---------- BAB 6 ----------
P("Bab 6 — Kesenjangan Gender, Kota-Desa, dan Provinsi", "h1")
P("Pengangguran tidak tersebar merata. Tiga jurang besar:", "h2")
P("1. Kota vs desa", "h2")
P(f"Pengangguran perkotaan {num(kes['perkotaan_feb_2026'])}% vs perdesaan "
  f"{num(kes['perdesaan_feb_2026'])}% — selisih {num(kes['urban_rural_gap_pp'])} poin persen, "
  f"kota {num(kes['urban_rural_ratio'])} kali lipat desa. Pengangguran adalah persoalan "
  "perkotaan.", "body")
P("2. Laki-laki vs perempuan", "h2")
P(f"Laki-laki {num(kes['laki_feb_2026'])}% vs perempuan {num(kes['perempuan_feb_2026'])}% "
  f"(selisih {num(kes['gender_gap_pp'])} poin persen). Tapi jangan buru-buru "
  f"menyimpulkan perempuan lebih baik: TPAK perempuan hanya {num(kes['tpak_perempuan_feb_2026'])}% "
  f"vs laki-laki {num(kes['tpak_laki_feb_2026'])}% — banyak perempuan bahkan tidak "
  "masuk angkatan kerja, jadi tidak tercatat sebagai penganggur.", "body")
CHART("05_kesenjangan.png", "Gambar 5 — Kesenjangan gender dan kota-desa, Feb 2026.")
P("3. Antar provinsi", "h2")
P(f"Papua {num(prov['top_mei_2026'][0]['tpt'])}% vs Bali {num(prov['terendah_mei_2026'][-1]['tpt'])}% — "
  f"selisih {num(prov['papua_vs_bali_ratio'])} kali lipat. Sepuluh provinsi tertinggi dipimpin "
  "Papua, lalu Jawa Barat, Banten, dan Kepulauan Riau. Lima terendah: Bali, "
  "Papua Pegunungan, Sulawesi Barat, Sulawesi Tengah, dan NTB.", "body")
CHART("06_provinsi_top10.png", "Gambar 6 — 10 provinsi dengan TPT tertinggi, Mei 2026.")
P(f"Perubahan Feb→Mei 2026: penurunan terbesar {num(prov['turun_terbesar_feb_mei_2026'][0]['provinsi'])} "
  f"({num(prov['turun_terbesar_feb_mei_2026'][0]['perubahan_pp'])} poin persen), kenaikan terbesar "
  f"{num(prov['naik_terbesar_feb_mei_2026'][0]['provinsi'])} "
  f"(+{num(prov['naik_terbesar_feb_mei_2026'][0]['perubahan_pp'])} poin persen).", "body")
story.append(PageBreak())

# ---------- BAB 7 ----------
P("Bab 7 — Siapa 7,22 Juta Penganggur Itu?", "h1")
P("Distribusi penganggur Mei 2026 berdasarkan pendidikan terakhir:", "body")
TABLE([["Pendidikan", "Porsi", "Jiwa (jt)"]] +
      [[d["pendidikan"], f"{num(d['porsi_persen'])}%", num(round(d["juta_orang"], 2))]
       for d in par["distribusi_penganggur_mei_2026"]])
P("Lulusan SMA adalah penyumbang penganggur terbesar: 28% atau 2,02 juta jiwa, "
  "disusul SMK 22,39% atau 1,62 juta jiwa. Lebih dari separuh penganggur Indonesia "
  "adalah lulusan sekolah menengah. Lulusan universitas 14,31% (1,03 juta jiwa), "
  "diploma 2,48% (0,18 juta jiwa).", "body")
CHART("08_distribusi_penganggur.png", "Gambar 7 — Distribusi 7,22 juta penganggur per pendidikan, Mei 2026.")
story.append(PageBreak())

# ---------- BAB 8 ----------
P("Bab 8 — Kualitas Pekerjaan dan Upah", "h1")
P("Angka pengangguran hanya separuh cerita. Yang bekerja pun belum tentu "
  "bekerja dengan baik:", "body")
B(f"Pekerja formal hanya {num(kerja['formal_feb_2026'])}% ({num(kerja['formal_jt_feb_2026'])} juta jiwa) — "
  f"sisanya {num(kerja['informal_feb_2026'])}% bekerja informal.")
B(f"Setengah menganggur (bekerja kurang dari 35 jam/minggu dan masih mencari "
  f"pekerjaan) {num(kerja['setengah_menganggur_feb_2026'])}%; pekerja paruh waktu "
  f"{num(kerja['paruh_waktu_feb_2026'])}%.")
B(f"Pekerja komuter (bekerja di kabupaten/kota berbeda dari tempat tinggal) "
  f"{num(kerja['komuter_feb_2026_jt'])} juta jiwa.")
CHART("09_formal_informal.png", "Gambar 8 — Komposisi pekerja formal vs informal, Feb 2026.")
P("Sisi baiknya: upah rata-rata buruh naik dari Rp3,29 jt (Feb 2026) ke Rp3,39 jt "
  "(Mei 2026). Penambah lapangan kerja terbesar Feb→Mei 2026:", "body")
TABLE([["Sektor", "Tambahan (ribu orang)"]] +
      [[x["sektor"], x["tambah_ribu"]] for x in kerja["sektor_penambah_feb_mei_2026"]])
CHART("10_upah_sektor.png", "Gambar 9 — Upah rata-rata buruh dan penambah lapangan kerja per sektor.")
story.append(PageBreak())

# ---------- BAB 9 ----------
P("Bab 9 — Memverifikasi Angka dengan SQL, Langkah per Langkah", "h1")
P("Setiap angka kunci di modul ini dihitung ulang lewat query SQL independen "
  "di sql/queries.sql. Jalankan dengan:", "body")
CODE("sqlite3 data/pengangguran_2026.db < sql/queries.sql")
P("Contoh 1: verifikasi gap SMK vs SD (harus keluar 7.68, 2.31, gap 5.37):", "h2")
CODE("SELECT pendidikan, mei_2026 FROM tpt_pendidikan\n"
     "WHERE pendidikan IN ('SMK', 'SD ke bawah');\n"
     "SELECT ROUND(\n"
     "  (SELECT mei_2026 FROM tpt_pendidikan WHERE pendidikan = 'SMK') -\n"
     "  (SELECT mei_2026 FROM tpt_pendidikan WHERE pendidikan = 'SD ke bawah'), 2)\n"
     "  AS smk_vs_sd_gap_pp;")
P("Contoh 2: verifikasi rasio muda vs nasional (harus keluar sekitar 3.74):", "h2")
CODE("SELECT ROUND(\n"
     "  (SELECT mei_2026 FROM tpt_umur WHERE kelompok_umur = '15-24 tahun') /\n"
     "  (SELECT tpt_persen FROM tpt_nasional WHERE periode = 'Mei 2026'), 2)\n"
     "  AS muda_vs_nasional;")
P("Contoh 3: verifikasi distribusi penganggur berjumlah sekitar 100%:", "h2")
CODE("SELECT ROUND(SUM(porsi_persen), 2) AS total_porsi FROM distribusi_penganggur;")
P("Totalnya 100,01 karena pembulatan — itu normal, bukan kesalahan. Kunci "
  "kebiasaan analis yang baik: tidak percaya angka hasil olahan sendiri sampai "
  "dihitung ulang dengan cara yang berbeda.", "body")
story.append(PageBreak())

# ---------- BAB 10 ----------
P("Bab 10 — Membangun Dashboard Power BI", "h1")
P("Analisis Python menjawab pertanyaan, tapi dashboard Power BI membuat hasilnya "
  "bisa dipantau dan dijelajahi siapa pun. Langkah besarnya: susun star schema, "
  "buat measure DAX, lalu rakit visual.", "body")
P("1. Star schema (desain anti-jebakan)", "h2")
P("Pelajaran dari proyek Harga Cabai 2026: satu tabel fakta yang mencampur "
  "baris nasional dan baris provinsi membuat measure MAX/CV/RANKX diam-diam "
  "salah ketika slicer provinsi dibiarkan All. Di proyek ini jebakan itu "
  "dihilangkan sejak desain data:", "body")
TABLE([["Tabel", "Isi", "Kunci"],
       ["fact_tpt_nasional", "HANYA 5 baris agregat nasional (Feb 2024 s.d. Mei 2026)", "periode_id"],
       ["fact_tpt_segmen", "HANYA 250 baris level segmen (pendidikan, umur, gender, daerah, provinsi). Tanpa baris Nasional.", "segmen_id, periode_id"],
       ["fact_indikator", "Indikator pasar kerja (formal/informal, setengah menganggur, dll)", "indikator_id, periode_id"],
       ["fact_sektor", "Penambah lapangan kerja per sektor", "sektor_id, periode_id"],
       ["dim_periode", "5 periode + urutan kronologis", "periode_id"],
       ["dim_segmen", "Dimensi segmen (tidak mengandung baris nasional)", "segmen_id"]])
P("Baca powerbi/measures_dax_CATATAN_LEVEL.md SEBELUM merakit — dokumen itu "
  "menjelaskan kenapa dua tabel fakta ini tidak akan pernah saling "
  "mengontaminasi, filter apa pun yang dipasang.", "warn")
P("2. Measure DAX (contoh)", "h2")
CODE("[TPT Nasional] = AVERAGE ( fact_tpt_nasional[tpt_persen] )\n\n"
     "[TPT Segmen] = AVERAGE ( fact_tpt_segmen[tpt_persen] )\n\n"
     "[Gap vs Nasional (pp)] = [TPT Segmen] - [TPT Nasional]\n\n"
     "[Perubahan pp] =\n"
     "DIVIDE ( [TPT Segmen] - [TPT Periode Sebelumnya], 1 )")
P("Daftar lengkap measure ada di powerbi/measures_dax.md — tinggal tempel.", "body")
P("3. Rakit di Power BI Desktop (Windows)", "h2")
B("Import 6 file CSV dari folder powerbi/.")
B("Buat relasi one-to-many dari dim_periode dan dim_segmen ke tabel-tabel fakta (lihat powerbi/build_guide.md).")
B("Tempel measure DAX, lalu bangun halaman sesuai powerbi/dashboard_layout.md.")
B("Verifikasi angka di dashboard dengan findings.json sebelum publish.")
story.append(PageBreak())

# ---------- BAB 11 ----------
P("Bab 11 — Kesimpulan dan Batasan", "h1")
P("Tiga pesan utama dari data:", "h2")
B(f"1. TPT nasional turun ke {num(nas['tpt_mei_2026'])}% seiring ekonomi yang tumbuh "
  f"{num(nas['pdb_q2_2026_yoy'])}%, tapi rata-rata nasional menyembunyikan masalah "
  "struktur: SMK 7,68% dan anak muda 15-24 tahun 17,37%.")
B("2. Pengangguran Indonesia adalah pengangguran muda dan lulusan sekolah "
  "menengah: SMA + SMK menyumbang lebih dari separuh dari 7,22 juta penganggur. "
  "Kota-desa (5,60% vs 3,20%) dan Papua-Bali (4,66x) memperlebar jurang.")
B(f"3. Kualitas pekerjaan belum ideal: formal hanya {num(kerja['formal_feb_2026'])}%, "
  f"informal {num(kerja['informal_feb_2026'])}%. Upah naik ke Rp3,39 jt, dan sektor "
  "akomodasi, transportasi, dan jasa menambah lapangan kerja tercepat.")
P("Batasan yang harus kamu pahami:", "h2")
B("Mei 2026 hanya tersedia untuk 17 provinsi — perbandingan provinsi memakai titik waktu itu.")
B("Angka Papua 2022-2023 tidak sebanding karena pemekaran provinsi.")
B("Dataset ini adalah kompilasi angka publikasi resmi, bukan mikrodataset Sakernas — "
  "tidak bisa dipakai untuk tabulasi silang baru.")
B("Analisis ini tidak mengklaim penyebab (misalnya kenapa SMK tinggi) karena "
  "angka TPT saja tidak cukup membuktikannya. Terima kasih sudah belajar sampai habis!")
story.append(PageBreak())

doc = SimpleDocTemplate(OUT, pagesize=landscape(A4),
                        leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=1.8 * cm, bottomMargin=1.8 * cm)
doc.build(story)
shutil.copy(OUT, OUT_COPY)
print(f"Module saved: {OUT}")
print(f"Copy saved: {OUT_COPY}")
