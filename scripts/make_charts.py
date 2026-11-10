#!/usr/bin/env python3
"""Build 10 clean charts for the Pengangguran 2026 project."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CH = HERE / "charts"
CH.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.size": 11, "axes.titlesize": 14, "axes.titleweight": "bold",
    "figure.dpi": 150, "axes.grid": True, "grid.alpha": 0.55,
    "grid.linestyle": "-", "grid.linewidth": 0.7, "grid.color": "#CFC8B8",
    "font.family": "Noto Sans",
    "figure.facecolor": "#F7F1E5", "axes.facecolor": "#F7F1E5",
    "savefig.facecolor": "#F7F1E5",
    "text.color": "#2E3138", "axes.labelcolor": "#2E3138",
    "xtick.color": "#2E3138", "ytick.color": "#2E3138",
    "axes.edgecolor": "#B9B2A2",
    "axes.prop_cycle": plt.cycler(color=["#4E7FA6", "#C75B7F", "#8FB0C9",
                                         "#2E3138", "#D98CA6", "#6E97B5"]),
})
# Tema T2 OAT/BLUE/PINK: primary blue, aksen pink, pink lembut, ink
NAVY = "#4E7FA6"; TEAL = "#8FB0C9"; RED = "#C75B7F"; ORANGE = "#D98CA6"
GREEN = "#2F5A7E"; GRAY = "#8A8578"; DARK = "#2E3138"; LIGHT = "#DCE9F2"

PERIODS = ["Feb 2024", "Feb 2025", "Feb 2026", "Mei 2026"]
X = np.arange(len(PERIODS))


def save(fig, name):
    fig.tight_layout()
    fig.savefig(CH / f"{name}.png", bbox_inches="tight")
    plt.close(fig)
    print("chart:", name)


# ---------- 01: national TPT trend ----------
fig, ax = plt.subplots(figsize=(10, 5.5))
tpt = [4.82, 4.76, 4.85, 4.68, 4.65, 4.75]
xp = ["Feb 2024", "Feb 2025", "Agu 2025", "Feb 2026", "Mei 2026", "Agu 2026"]
ax.plot(xp, tpt, marker="o", color=NAVY, linewidth=2.5, markersize=8)
for x, y in zip(xp, tpt):
    ax.annotate(f"{y:.2f}%", (x, y), textcoords="offset points",
                xytext=(0, 12), ha="center", fontsize=10, color=NAVY,
                fontweight="bold")
ax.set_ylim(4.4, 5.0)
ax.set_title("TPT Nasional: 4,75% (Agu 2026), Turun dari 4,85% Setahun Lalu")
ax.set_ylabel("TPT (%)")
ax.annotate("Pengangguran muda 15-24 th justru NAIK\nke 17,50% pada Agu 2026",
            xy=(5, 4.75), xytext=(2.4, 4.9),
            arrowprops=dict(arrowstyle="->", color=RED),
            fontsize=10, color=RED, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc="#F6E3EA", ec=RED))
save(fig, "01_tpt_nasional_tren")

# ---------- 02: education paradox ----------
fig, ax = plt.subplots(figsize=(10, 5.5))
edu = ["SD ke\nbawah", "SMP", "Diploma\nI/II/III", "SMA",
       "Diploma IV/\nS1/S2/S3", "SMK"]
feb26 = [2.32, 4.19, 4.80, 6.23, 6.13, 7.74]
agu26 = [2.24, 3.78, 4.18, 6.87, 5.09, 8.20]
x = np.arange(len(edu)); w = 0.38
b1 = ax.bar(x - w / 2, feb26, w, label="Feb 2026", color=LIGHT, edgecolor=NAVY)
b2 = ax.bar(x + w / 2, agu26, w, label="Agu 2026", color=NAVY)
for b in list(b1) + list(b2):
    ax.annotate(f"{b.get_height():.2f}%", (b.get_x() + b.get_width() / 2, b.get_height()),
                textcoords="offset points", xytext=(0, 4), ha="center", fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(edu)
ax.set_title("Paradoks Pendidikan: Makin Tinggi Ijazah, Makin Tinggi Pengangguran")
ax.set_ylabel("TPT (%)")
ax.legend()
ax.annotate("SMK 8,20% = 3,7x lipat\nlulusan SD (2,24%)",
            xy=(5, 8.20), xytext=(3.2, 9.2),
            arrowprops=dict(arrowstyle="->", color=RED),
            fontsize=10, color=RED, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc="#F6E3EA", ec=RED))
save(fig, "02_paradoks_pendidikan")

# ---------- 03: education trend ----------
fig, ax = plt.subplots(figsize=(10, 5.5))
P7 = ["Feb 2024", "Agu 2024", "Feb 2025", "Agu 2025", "Feb 2026", "Mei 2026", "Agu 2026"]
ax.plot(P7, [8.62, 9.01, 8.00, 8.63, 7.74, 7.68, 8.20], marker="o", label="SMK",
        color=RED, linewidth=2.5)
ax.plot(P7, [6.73, 7.05, 6.35, 6.88, 6.23, 6.17, 6.87], marker="s", label="SMA",
        color=ORANGE, linewidth=2.5)
ax.plot(P7, [5.63, 5.25, 6.23, 5.39, 6.13, 6.09, 5.09], marker="^",
        label="Diploma IV / S1 / S2 / S3", color=NAVY, linewidth=2.5)
ax.plot(P7, [2.38, 2.32, 2.32, 2.30, 2.32, 2.31, 2.24], marker="d", label="SD ke bawah",
        color=GREEN, linewidth=2.5)
ax.set_title("Tren TPT per Jenjang: SMK Naik Lagi Setiap Agustus, Tetap Tertinggi")
ax.set_ylabel("TPT (%)"); ax.legend(); ax.set_ylim(1.5, 10)
save(fig, "03_pendidikan_tren")

# ---------- 04: age groups ----------
fig, ax = plt.subplots(figsize=(10, 5.5))
umur = ["15-24 thn", "25-59 thn", "60+ thn"]
vals = [[16.42, 16.16, 16.36, 17.50], [3.08, 3.04, 2.93, 2.78],
        [1.14, 1.67, 1.89, 1.44]]
x = np.arange(len(umur)); w = 0.2
P4 = ["Feb 2024", "Feb 2025", "Feb 2026", "Agu 2026"]
colors = [LIGHT, "#A9C6DA", "#7FA8C4", NAVY]
for i, p in enumerate(P4):
    b = ax.bar(x + (i - 1.5) * w, [v[i] for v in vals], w, label=p,
               color=colors[i], edgecolor=NAVY)
    for bar in b:
        ax.annotate(f"{bar.get_height():.2f}%", (bar.get_x() + bar.get_width() / 2,
                    bar.get_height()), textcoords="offset points", xytext=(0, 4),
                    ha="center", fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(umur)
ax.set_title("Pengangguran Muda 15-24 Tahun: 17,50% (3,7x Rata-rata Nasional)")
ax.set_ylabel("TPT (%)"); ax.legend()
save(fig, "04_umur")

# ---------- 05: gender + urban/rural gaps ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
ax = axes[0]
b = ax.bar(["Laki-laki", "Perempuan"], [4.64, 4.93], color=[NAVY, TEAL], width=0.6)
for bar in b:
    ax.annotate(f"{bar.get_height():.2f}%", (bar.get_x() + bar.get_width() / 2,
                bar.get_height()), textcoords="offset points", xytext=(0, 6),
                ha="center", fontsize=11, fontweight="bold")
ax.set_title("Gender (Agu 2026)"); ax.set_ylabel("TPT (%)"); ax.set_ylim(0, 6)
ax.annotate("perempuan kini lebih tinggi, gap 0,29 pp", xy=(0.5, 5.4), ha="center", fontsize=10, color=GRAY)
ax = axes[1]
b = ax.bar(["Perkotaan", "Perdesaan"], [5.53, 3.45], color=[ORANGE, GREEN], width=0.6)
for bar in b:
    ax.annotate(f"{bar.get_height():.2f}%", (bar.get_x() + bar.get_width() / 2,
                bar.get_height()), textcoords="offset points", xytext=(0, 6),
                ha="center", fontsize=11, fontweight="bold")
ax.set_title("Perkotaan vs Perdesaan (Agu 2026)"); ax.set_ylim(0, 6.5)
ax.annotate("gap 2,08 pp (1,60x)", xy=(0.5, 6.0), ha="center", fontsize=10,
            color=RED, fontweight="bold")
fig.suptitle("Kesenjangan: Kota 1,6x Desa; Perempuan Melampaui Laki-laki",
             fontsize=14, fontweight="bold")
save(fig, "05_kesenjangan")

# ---------- 06: top-10 provinces ----------
fig, ax = plt.subplots(figsize=(10, 6))
prov = ["Papua", "Jawa Barat", "Banten", "Papua Barat Daya", "Kep. Riau",
        "Maluku", "Sulawesi Utara", "DKI Jakarta", "Aceh", "Sumatera Barat"]
val = [7.12, 6.67, 6.61, 6.56, 6.37, 6.23, 5.90, 5.75, 5.70, 5.57]
colors = [RED if v >= 6.4 else ORANGE if v >= 5.7 else TEAL for v in val]
y = np.arange(len(prov))
b = ax.barh(y, val, color=colors, edgecolor=DARK)
ax.set_yticks(y); ax.set_yticklabels(prov); ax.invert_yaxis()
for bar, v in zip(b, val):
    ax.annotate(f"{v:.2f}%", (v, bar.get_y() + bar.get_height() / 2),
                textcoords="offset points", xytext=(6, 0), va="center",
                fontsize=10, fontweight="bold")
ax.axvline(4.75, color=NAVY, linestyle="--", linewidth=1.5)
ax.annotate("Nasional 4,75%", xy=(4.75, 9.2), xytext=(4.0, 8.6),
            fontsize=10, color=NAVY, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=NAVY))
ax.set_title("10 Provinsi dengan TPT Tertinggi, Agu 2026 (Bali Terendah: 1,42%)")
ax.set_xlabel("TPT (%)")
save(fig, "06_provinsi_top10")

# ---------- 07: provincial trend ----------
fig, ax = plt.subplots(figsize=(11, 5.5))
xp = ["Agu 2022", "Agu 2023", "Agu 2024", "Agu 2025", "Feb 2026", "Mei 2026", "Agu 2026"]
series = {
    "Jawa Barat": [8.31, 7.44, 6.75, 6.77, 6.64, 6.61, 6.67],
    "Banten": [8.09, 7.52, 6.68, 6.69, 6.59, 6.48, 6.61],
    "DKI Jakarta": [7.18, 6.53, 6.21, 6.05, 6.03, 5.79, 5.75],
    "Kep. Riau": [8.23, 6.80, 6.39, 6.45, 6.87, 6.45, 6.37],
    "Papua": [None, None, 6.48, 6.96, 7.02, 7.08, 7.12],
    "Bali": [4.80, 2.69, 1.79, 1.49, 1.59, 1.52, 1.42],
}
for name, vals in series.items():
    xs = [x for x, v in zip(xp, vals) if v is not None]
    ys = [v for v in vals if v is not None]
    ax.plot(xs, ys, marker="o", label=name, linewidth=2.2)
ax.set_title("Tren TPT Provinsi 2022-2026: Jawa Barat & Banten Turun Jauh, Papua Tetap Naik")
ax.set_ylabel("TPT (%)"); ax.legend(ncol=3, fontsize=9)
ax.annotate("Papua 2022-2023\nsebelum pemekaran", xy=(1, 5.5), fontsize=8,
            color=GRAY, style="italic")
save(fig, "07_provinsi_tren")

# ---------- 08: distribution of unemployed ----------
fig, ax = plt.subplots(figsize=(10, 5.5))
edu = ["SMA", "SMK", "SD ke bawah", "SMP", "Diploma IV-S3", "Diploma I-III"]
porsi = [32.31, 24.85, 15.55, 13.38, 11.93, 1.99]
jt = [2.3848, 1.8340, 1.1476, 0.9875, 0.8804, 0.1469]
y = np.arange(len(edu))
b = ax.barh(y, porsi, color=[RED, ORANGE, GRAY, TEAL, NAVY, LIGHT], edgecolor=DARK)
ax.set_yticks(y); ax.set_yticklabels(edu); ax.invert_yaxis()
for bar, p, j in zip(b, porsi, jt):
    ax.annotate(f"{p:.2f}%  ({j:.2f} jt orang)",
                (p, bar.get_y() + bar.get_height() / 2),
                textcoords="offset points", xytext=(6, 0), va="center", fontsize=10)
ax.set_title("7,38 Juta Penganggur (Agu 2026): SMA Paling Banyak, 2,38 Jt Orang")
ax.set_xlabel("Porsi dari total penganggur (%)")
save(fig, "08_distribusi_penganggur")

# ---------- 09: formal vs informal ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
ax = axes[0]
w = ax.pie([42.07, 57.93], labels=["Formal\n42,07%", "Informal\n57,93%"],
           colors=[NAVY, ORANGE], autopct="", startangle=90,
           textprops={"fontsize": 12, "fontweight": "bold"},
           wedgeprops={"edgecolor": "white", "linewidth": 2})
ax.set_title("Status Pekerjaan (Agu 2026)")
ax = axes[1]
ind = ["Setengah\nmenganggur", "Pekerja\nparuh waktu"]
vv = [8.68, 23.85]
b = ax.bar(ind, vv, color=[TEAL, GRAY], width=0.55)
for bar, v in zip(b, vv):
    ax.annotate(f"{v:.2f}%", (bar.get_x() + bar.get_width() / 2, v),
                textcoords="offset points", xytext=(0, 6), ha="center",
                fontsize=11, fontweight="bold")
ax.set_title("Kualitas Pekerjaan (Agu 2026)"); ax.set_ylim(0, 30)
ax.set_ylabel("% dari pekerja")
fig.suptitle("Hampir 6 dari 10 Pekerja Informal; Setengah Penganggur Naik",
             fontsize=14, fontweight="bold")
save(fig, "09_formal_informal")

# ---------- 10: wages + sectors ----------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
ax = axes[0]
ax.plot(["Feb 2026", "Mei 2026", "Agu 2026"], [3.29, 3.39, 3.42], marker="o",
        color=GREEN, linewidth=2.5, markersize=8)
ax.set_title("Rata-rata Upah Buruh Naik Tipis"); ax.set_ylabel("Rp juta")
ax.set_ylim(3.24, 3.48)
ax.annotate("Rp3,42 jt", xy=(2, 3.42), xytext=(-80, 16),
            textcoords="offset points",
            arrowprops=dict(arrowstyle="->", color=GREEN),
            fontsize=11, fontweight="bold", color=GREEN)
ax = axes[1]
sek = ["Pertanian", "Perdagangan", "Industri"]
tb = [41.73, 26.42, 20.35]
b = ax.bar(sek, tb, color=[TEAL, NAVY, ORANGE], width=0.6)
for bar, v in zip(b, tb):
    ax.annotate(f"{v:.2f} jt", (bar.get_x() + bar.get_width() / 2, v),
                textcoords="offset points", xytext=(0, 6), ha="center",
                fontsize=11, fontweight="bold")
ax.set_title("Penyerap Pekerja Terbanyak (Agu 2026)")
ax.set_ylabel("Juta orang")
fig.suptitle("Upah Naik Tipis; Pertanian Tetap Penyerap Pekerja Terbesar",
             fontsize=14, fontweight="bold")
save(fig, "10_upah_sektor")

print("done: 10 charts")
