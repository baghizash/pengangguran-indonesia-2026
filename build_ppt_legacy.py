#!/usr/bin/env python3
"""Build Portofolio-Analisis-Pengangguran-2026.pptx (16:9, 10 slides, ID).

Reads findings.json — every number comes from the compiled BPS (Sakernas) data.
"""
import json
import shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
F = json.loads((HERE / "findings.json").read_text())
CHARTS = HERE / "charts"
OUT = Path.home() / "workspace" / "your_files" / "Portofolio-Analisis-Pengangguran-2026.pptx"
OUT_COPY = HERE / "Portofolio-Analisis-Pengangguran-2026.pptx"

NAVY = RGBColor(0x1E, 0x3A, 0x8A)
TEAL = RGBColor(0x0D, 0x94, 0x88)
RED = RGBColor(0xC0, 0x39, 0x2B)
DARK = RGBColor(0x1F, 0x29, 0x37)
GRAY = RGBColor(0x6B, 0x72, 0x80)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]


def jt(v):
    return f"{v} jt".replace(".", ",")


def pct(v):
    return f"{v}%".replace(".", ",")


def num(v):
    """Format number with Indonesian decimal comma; pass strings through."""
    return f"{v}".replace(".", ",")




def solid_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def textbox(slide, l, t, w, h):
    tx = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tx.text_frame
    tf.word_wrap = True
    return tf


def add_par(tf, text, size, color, bold=False, italic=False, first=False, align=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.space_after = Pt(8)
    if align is not None:
        p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return p


def add_bullet(tf, text, size=17, first=False):
    p = add_par(tf, text, size, DARK, first=first)
    pPr = p._p.get_or_add_pPr()
    pPr.append(pPr.makeelement(qn("a:buChar"), {"char": "\u2022"}))
    pPr.set("marL", "171450")
    pPr.set("indent", "-171450")
    p.space_after = Pt(10)
    p.space_before = Pt(2)
    return p


def content_title(slide, text):
    tf = textbox(slide, 0.7, 0.3, 11.9, 0.9)
    add_par(tf, text, 30, NAVY, bold=True, first=True)
    bar = slide.shapes.add_shape(1, Inches(0.7), Inches(1.15), Inches(1.5), Inches(0.06))
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL
    bar.line.fill.background()


def content_slide(title, bullets, chart=None, caption=None, full_width=False):
    s = prs.slides.add_slide(blank)
    solid_bg(s, WHITE)
    content_title(s, title)
    bw = 11.9 if full_width else 5.6
    tf = textbox(s, 0.7, 1.5, bw, 5.2)
    for i, b in enumerate(bullets):
        add_bullet(tf, b, first=(i == 0))
    if chart:
        s.shapes.add_picture(str(CHARTS / f"{chart}.png"), Inches(6.8), Inches(1.5), width=Inches(5.8))
    if caption:
        tf2 = textbox(s, 0.7, 6.7, 11.9, 0.5)
        add_par(tf2, caption, 11, GRAY, italic=True, first=True)
    return s


nas = F["nasional"]
par = F["paradoks_pendidikan"]
muda = F["pengangguran_muda"]
kes = F["kesenjangan"]
prov = F["provinsi"]
kerja = F["pasar_kerja"]

# ---- Slide 1: Title ----
s = prs.slides.add_slide(blank)
solid_bg(s, NAVY)
tf = textbox(s, 0.9, 1.0, 11.5, 1.2)
add_par(tf, "ANALISIS PENGANGGURAN INDONESIA 2026", 40, WHITE, bold=True, first=True)
tf = textbox(s, 0.9, 2.4, 11.5, 1.2)
add_par(tf, "Paradoks Pendidikan: TPT Nasional Turun, tapi Lulusan SMK Paling Sulit Dapat Kerja",
        22, WHITE, first=True)
tf = textbox(s, 0.9, 3.9, 11.5, 1.6)
add_par(tf, "Data resmi BPS (Sakernas) — Februari 2024 sampai Mei 2026, "
            "dapat direproduksi dari script dan query SQL di repo.", 16, WHITE, first=True)
add_par(tf, "Plus: paket dashboard Power BI (star schema anti-jebakan, DAX, panduan rakit)", 16, WHITE)
tf = textbox(s, 0.9, 6.0, 11.5, 0.8)
add_par(tf, "BAGHIZ ASSHIDDIQIE ARASYA", 20, WHITE, bold=True, first=True)

# ---- Slide 2: Latar belakang & sumber data ----
content_slide("Latar Belakang dan Sumber Data", [
    "Tingkat Pengangguran Terbuka (TPT) nasional turun, tapi angka rata-rata "
    "menyembunyikan jurang yang lebar antar jenjang pendidikan, umur, gender, "
    "kota-desa, dan provinsi.",
    "Project ini mengkompilasi angka resmi BPS dari publikasi Sakernas: "
    "5 titik waktu (Feb 2024, Feb 2025, Agu 2025, Feb 2026, Mei 2026), dengan "
    "rincian pendidikan, umur, gender, kota-desa, dan 38 provinsi.",
    "Semua angka diverifikasi dengan query SQL independen (sql/queries.sql) "
    "dan divisualisasikan dalam 10 chart dari data yang sama.",
    "Pertanyaan utama: TPT nasional 4,65% — tapi siapa sebenarnya 7,22 juta "
    "penganggur itu, dan di mana letak masalah terbesarnya?",
], full_width=True, caption="Sumber: BPS, Survei Angkatan Kerja Nasional (Sakernas). Daftar sumber per angka: data/SOURCES.md.")

# ---- Slide 3: TPT nasional ----
content_slide("TPT Nasional Turun, Ekonomi Tetap Tumbuh", [
    f"TPT nasional turun dari {pct(nas['tpt_feb_2024'])} (Feb 2024) ke {pct(nas['tpt_mei_2026'])} "
    f"(Mei 2026) — penurunan {num(abs(nas['penurunan_pp_feb24_mei26']))} poin persen dalam 27 bulan.",
    f"Penganggur Mei 2026: {jt(nas['penganggur_mei_2026_jt'])} orang dari angkatan kerja "
    f"{jt(nas['angkatan_kerja_mei_2026_jt'])}; yang bekerja {jt(nas['bekerja_mei_2026_jt'])}. "
    f"TPAK {pct(nas['tpak_mei_2026'])}.",
    f"Di saat yang sama, ekonomi tumbuh: PDB Q2 2026 tumbuh {pct(nas['pdb_q2_2026_yoy'])} "
    "secara tahunan. Penurunan TPT berjalan seiring pertumbuhan ekonomi.",
    "Tapi tren nasional saja tidak cukup — masalah sesungguhnya ada di rinciannya.",
], chart="01_tpt_nasional_tren")

# ---- Slide 4: Paradoks pendidikan ----
content_slide("Paradoks Pendidikan: Makin Tinggi Ijazah, Makin Sulit?", [
    f"Lulusan SMK punya TPT {pct(par['smk_mei_2026'])} — tertinggi di antara semua "
    "jenjang pendidikan. Lulusan SD ke bawah hanya 2,31%.",
    f"Selisihnya {num(par['smk_vs_sd_pp'])} poin persen; TPT SMK {num(par['smk_vs_nasional_ratio'])} kali "
    "lipat rata-rata nasional. Paradoks: jenjang paling rendah pendidikannya "
    "justru paling mudah mendapat pekerjaan.",
    "Lulusan universitas (Diploma IV/S1/S2/S3) juga tinggi: 6,09% — lebih tinggi "
    "dari lulusan SMP. Pasar kerja tidak menyerap sesuai ijazah.",
    "Inilah fokus utama analisis ini: ketidakcocokan antara pendidikan dan "
    "lapangan kerja yang tersedia.",
], chart="02_paradoks_pendidikan")

# ---- Slide 5: Tren per jenjang ----
content_slide("Tren SMK Membaik, tapi Masih Tertinggi", [
    f"TPT SMK turun dari {pct(par['smk_tren']['Feb 2024'])} (Feb 2024) ke "
    f"{pct(par['smk_mei_2026'])} (Mei 2026) — turun {num(abs(par['smk_turun_pp_feb24_mei26']))} poin persen. "
    "Tren membaik.",
    "Tapi tetap jauh di atas semua jenjang lain: SMA 6,17%, universitas 6,09%, "
    "Diploma I/II/III 4,75%, SMP 4,16%, SD 2,31%.",
    "Lulusan universitas sempat naik dari 5,63% (Feb 2024) ke 6,23% (Feb 2025) "
    "sebelum turun ke 6,09%. Lulusan SD stabil di sekitar 2,3% sepanjang periode.",
    "Perbaikan tren belum menyentuh struktur masalahnya.",
], chart="03_pendidikan_tren")

# ---- Slide 6: Pengangguran muda ----
content_slide("Generasi Muda: 17,37% Menganggur", [
    f"TPT usia 15-24 tahun: {pct(muda['muda_15_24_mei_2026'])} (Mei 2026), naik "
    f"{num(muda['muda_naik_pp_feb_mei_2026'])} poin persen dari Feb 2026 — "
    "satu-satunya kelompok umur yang TPT-nya naik dalam periode itu.",
    f"Angka ini {num(muda['muda_vs_nasional_ratio'])} kali lipat rata-rata nasional dan "
    f"{num(muda['muda_vs_produktif_ratio'])} kali lipat usia produktif 25-59 tahun "
    f"({pct(muda['produktif_25_59_mei_2026'])}).",
    "Kelompok 25-59 tahun justru turun dari 3,08% (Feb 2024) ke 2,56%; kelompok "
    "60 tahun ke atas naik perlahan ke 2,35%.",
    "Krisis pengangguran Indonesia adalah krisis pengangguran muda — dan sebagian "
    "besar penganggur muda adalah lulusan SMA/SMK.",
], chart="04_umur")

# ---- Slide 7: Kesenjangan gender & kota-desa ----
content_slide("Kesenjangan Gender dan Kota-Desa", [
    f"Pengangguran perkotaan {pct(kes['perkotaan_feb_2026'])} vs perdesaan "
    f"{pct(kes['perdesaan_feb_2026'])} — selisih {num(kes['urban_rural_gap_pp'])} poin persen, "
    f"kota {num(kes['urban_rural_ratio'])} kali lipat desa.",
    f"Laki-laki {pct(kes['laki_feb_2026'])} vs perempuan {pct(kes['perempuan_feb_2026'])} "
    f"(selisih {num(kes['gender_gap_pp'])} pp). Tapi TPAK perempuan hanya {pct(kes['tpak_perempuan_feb_2026'])} "
    f"vs laki-laki {pct(kes['tpak_laki_feb_2026'])} — banyak perempuan bahkan "
    "tidak masuk angkatan kerja.",
    "Artinya: pengangguran adalah persoalan perkotaan, dan di balik angka "
    "perempuan yang lebih rendah ada partisipasi yang jauh lebih kecil.",
], chart="05_kesenjangan")

# ---- Slide 8: Jurang provinsi ----
content_slide("Jurang Provinsi: Papua vs Bali 4,66 Kali Lipat", [
    f"TPT tertinggi: Papua {pct(prov['top_mei_2026'][0]['tpt'])}; terendah: Bali "
    f"{pct(prov['terendah_mei_2026'][-1]['tpt'])} — selisih {num(prov['papua_vs_bali_ratio'])} kali lipat.",
    f"Sepuluh provinsi tertinggi: {', '.join(f'{num(p['provinsi'])} {pct(p['tpt'])}' for p in prov['top_mei_2026'][:3])}... "
    "Jawa Barat dan Banten ikut di papan atas meski pusat industri.",
    f"Penurunan terbesar Feb→Mei 2026: {num(prov['turun_terbesar_feb_mei_2026'][0]['provinsi'])} "
    f"({num(prov['turun_terbesar_feb_mei_2026'][0]['perubahan_pp'])} pp). Kenaikan terbesar: "
    f"{num(prov['naik_terbesar_feb_mei_2026'][0]['provinsi'])} "
    f"(+{num(prov['naik_terbesar_feb_mei_2026'][0]['perubahan_pp'])} pp).",
    "Catatan: Mei 2026 tersedia untuk 17 provinsi; Papua 2022-2023 tidak "
    "sebanding karena pemekaran.",
], chart="06_provinsi_top10")

# ---- Slide 9: Kualitas pekerjaan + upah (two charts) ----
s = prs.slides.add_slide(blank)
solid_bg(s, WHITE)
content_title(s, "Bukan Sekadar Jumlah: Kualitas Pekerjaan")
tf = textbox(s, 0.7, 1.5, 11.9, 2.4)
add_bullet(tf, f"Pekerja formal hanya {pct(kerja['formal_feb_2026'])} ({jt(kerja['formal_jt_feb_2026'])}) — "
               f"sisanya {pct(kerja['informal_feb_2026'])} bekerja informal.", first=True, size=15)
add_bullet(tf, f"Setengah menganggur {pct(kerja['setengah_menganggur_feb_2026'])}, pekerja paruh waktu "
               f"{pct(kerja['paruh_waktu_feb_2026'])}, komuter {jt(kerja['komuter_feb_2026_jt'])}.", size=15)
add_bullet(tf, "Upah rata-rata buruh naik dari Rp3,29 jt (Feb 2026) ke Rp3,39 jt (Mei 2026).", size=15)
add_bullet(tf, "Penambah lapangan kerja terbesar Feb→Mei 2026: " +
           ", ".join(f"{x['sektor'].lower()} (+{num(x['tambah_ribu'])} ribu)" for x in kerja['sektor_penambah_feb_mei_2026']) + ".", size=15)
s.shapes.add_picture(str(CHARTS / "09_formal_informal.png"), Inches(0.7), Inches(4.0), width=Inches(5.8))
s.shapes.add_picture(str(CHARTS / "10_upah_sektor.png"), Inches(6.8), Inches(4.0), width=Inches(5.8))

# ---- Slide 10: Penutup ----
content_slide("Penutup", [
    "Kisah dua sisi 2026: TPT nasional turun ke 4,65% seiring ekonomi yang "
    "tumbuh 5,29%, tapi lulusan SMK (7,68%) dan anak muda 15-24 tahun (17,37%) "
    "tetap jadi kelompok paling tertekan.",
    "Isi repo: analysis.ipynb, data/compiled + SOURCES.md, sql/queries.sql "
    "(semua angka diverifikasi ulang lewat SQL), scripts, charts, findings.json.",
    "Plus kit dashboard Power BI: star schema anti-jebakan (fact_tpt_nasional "
    "dan fact_tpt_segmen terpisah agar measure tidak terkontaminasi), measure DAX, "
    "layout dashboard, dan panduan rakit 20-30 menit — lihat powerbi/measures_dax_CATATAN_LEVEL.md dulu.",
    "Keterbatasan: angka Mei 2026 hanya untuk 17 provinsi; dataset ini kompilasi "
    "angka publikasi resmi, bukan mikrodataset Sakernas. Terima kasih.",
], full_width=True)

OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(str(OUT))
shutil.copy(OUT, OUT_COPY)
print(f"PPT saved: {OUT}")
print(f"Copy saved: {OUT_COPY}")
