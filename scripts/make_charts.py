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
    "figure.dpi": 150, "axes.grid": True, "grid.alpha": 0.3,
    "grid.linestyle": "--",
})
NAVY = "#1E3A8A"; TEAL = "#0D9488"; RED = "#C0392B"; ORANGE = "#E67E22"
GREEN = "#27AE60"; GRAY = "#6B7280"; DARK = "#1F2937"; LIGHT = "#DBEAFE"

PERIODS = ["Feb 2024", "Feb 2025", "Feb 2026", "Mei 2026"]
X = np.arange(len(PERIODS))


def save(fig, name):
    fig.tight_layout()
    fig.savefig(CH / f"{name}.png", bbox_inches="tight")
    plt.close(fig)
    print("chart:", name)


# ---------- 01: national TPT trend ----------
fig, ax = plt.subplots(figsize=(10, 5.5))
tpt = [4.82, 4.76, 4.85, 4.68, 4.65]
xp = ["Feb 2024", "Feb 2025", "Agu 2025", "Feb 2026", "Mei 2026"]
ax.plot(xp, tpt, marker="o", color=NAVY, linewidth=2.5, markersize=8)
for x, y in zip(xp, tpt):
    ax.annotate(f"{y:.2f}%", (x, y), textcoords="offset points",
                xytext=(0, 12), ha="center", fontsize=10, color=NAVY,
                fontweight="bold")
ax.set_ylim(4.4, 5.0)
ax.set_title("TPT Nasional Turun Perlahan: 4,82% (Feb 2024) ke 4,65% (Mei 2026)")
ax.set_ylabel("TPT (%)")
ax.annotate("Pengangguran muda 15-24 th justru NAIK\nke 17,37% pada periode yang sama",
            xy=(4, 4.65), xytext=(2.2, 4.88),
            arrowprops=dict(arrowstyle="->", color=RED),
            fontsize=10, color=RED, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc="#FDEDEC", ec=RED))
save(fig, "01_tpt_nasional_tren")

# ---------- 02: education paradox ----------
fig, ax = plt.subplots(figsize=(10, 5.5))
edu = ["SD ke\nbawah", "SMP", "Diploma\nI/II/III", "SMA",
       "Diploma IV/\nS1/S2/S3", "SMK"]
feb26 = [2.32, 4.19, 4.80, 6.23, 6.13, 7.74]
mei26 = [2.31, 4.16, 4.75, 6.17, 6.09, 7.68]
x = np.arange(len(edu)); w = 0.38
b1 = ax.bar(x - w / 2, feb26, w, label="Feb 2026", color=LIGHT, edgecolor=NAVY)
b2 = ax.bar(x + w / 2, mei26, w, label="Mei 2026", color=NAVY)
for b in list(b1) + list(b2):
    ax.annotate(f"{b.get_height():.2f}%", (b.get_x() + b.get_width() / 2, b.get_height()),
                textcoords="offset points", xytext=(0, 4), ha="center", fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(edu)
ax.set_title("Paradoks Pendidikan: Makin Tinggi Ijazah, Makin Tinggi Pengangguran")
ax.set_ylabel("TPT (%)")
ax.legend()
ax.annotate("SMK 7,68% = 3,3x lipat\nlulusan SD (2,31%)",
            xy=(5, 7.68), xytext=(3.2, 8.6),
            arrowprops=dict(arrowstyle="->", color=RED),
            fontsize=10, color=RED, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc="#FDEDEC", ec=RED))
save(fig, "02_paradoks_pendidikan")

# ---------- 03: education trend ----------
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(PERIODS, [8.62, 8.00, 7.74, 7.68], marker="o", label="SMK",
        color=RED, linewidth=2.5)
ax.plot(PERIODS, [6.73, 6.35, 6.23, 6.17], marker="s", label="SMA",
        color=ORANGE, linewidth=2.5)
ax.plot(PERIODS, [5.63, 6.23, 6.13, 6.09], marker="^",
        label="Diploma IV / S1 / S2 / S3", color=NAVY, linewidth=2.5)
ax.plot(PERIODS, [2.38, 2.32, 2.32, 2.31], marker="d", label="SD ke bawah",
        color=GREEN, linewidth=2.5)
ax.set_title("Tren TPT per Jenjang: SMK Turun tapi Tetap Tertinggi")
ax.set_ylabel("TPT (%)"); ax.legend(); ax.set_ylim(1.5, 9.5)
save(fig, "03_pendidikan_tren")

# ---------- 04: age groups ----------
fig, ax = plt.subplots(figsize=(10, 5.5))
umur = ["15-24 thn", "25-59 thn", "60+ thn"]
vals = [[16.42, 16.16, 16.36, 17.37], [3.08, 3.04, 2.93, 2.56],
        [1.14, 1.67, 1.89, 2.35]]
x = np.arange(len(umur)); w = 0.2
colors = [LIGHT, "#93C5FD", "#3B82F6", NAVY]
for i, p in enumerate(PERIODS):
    b = ax.bar(x + (i - 1.5) * w, [v[i] for v in vals], w, label=p,
               color=colors[i], edgecolor=NAVY)
    for bar in b:
        ax.annotate(f"{bar.get_height():.2f}%", (bar.get_x() + bar.get_width() / 2,
                    bar.get_height()), textcoords="offset points", xytext=(0, 4),
                    ha="center", fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(umur)
ax.set_title("Pengangguran Muda 15-24 Tahun: 17,37% (3,7x Rata-rata Nasional)")
ax.set_ylabel("TPT (%)"); ax.legend()
save(fig, "04_umur")

# ---------- 05: gender + urban/rural gaps ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
ax = axes[0]
b = ax.bar(["Laki-laki", "Perempuan"], [4.88, 4.36], color=[NAVY, TEAL], width=0.6)
for bar in b:
    ax.annotate(f"{bar.get_height():.2f}%", (bar.get_x() + bar.get_width() / 2,
                bar.get_height()), textcoords="offset points", xytext=(0, 6),
                ha="center", fontsize=11, fontweight="bold")
ax.set_title("Gender (Feb 2026)"); ax.set_ylabel("TPT (%)"); ax.set_ylim(0, 6)
ax.annotate("gap 0,52 pp", xy=(0.5, 5.2), ha="center", fontsize=10, color=GRAY)
ax = axes[1]
b = ax.bar(["Perkotaan", "Perdesaan"], [5.60, 3.20], color=[ORANGE, GREEN], width=0.6)
for bar in b:
    ax.annotate(f"{bar.get_height():.2f}%", (bar.get_x() + bar.get_width() / 2,
                bar.get_height()), textcoords="offset points", xytext=(0, 6),
                ha="center", fontsize=11, fontweight="bold")
ax.set_title("Perkotaan vs Perdesaan (Feb 2026)"); ax.set_ylim(0, 6.5)
ax.annotate("gap 2,40 pp (1,75x)", xy=(0.5, 6.0), ha="center", fontsize=10,
            color=RED, fontweight="bold")
fig.suptitle("Kesenjangan: Kota 1,75x Desa; Laki-laki di Atas Perempuan",
             fontsize=14, fontweight="bold")
save(fig, "05_kesenjangan")

# ---------- 06: top-10 provinces ----------
fig, ax = plt.subplots(figsize=(10, 6))
prov = ["Papua", "Jawa Barat", "Banten", "Kep. Riau", "Papua Barat Daya",
        "Aceh", "Sulawesi Utara", "DKI Jakarta", "Maluku", "Sumatera Barat"]
val = [7.08, 6.61, 6.48, 6.45, 6.38, 5.89, 5.85, 5.79, 5.75, 5.53]
colors = [RED if v >= 6.4 else ORANGE if v >= 5.7 else TEAL for v in val]
y = np.arange(len(prov))
b = ax.barh(y, val, color=colors, edgecolor=DARK)
ax.set_yticks(y); ax.set_yticklabels(prov); ax.invert_yaxis()
for bar, v in zip(b, val):
    ax.annotate(f"{v:.2f}%", (v, bar.get_y() + bar.get_height() / 2),
                textcoords="offset points", xytext=(6, 0), va="center",
                fontsize=10, fontweight="bold")
ax.axvline(4.65, color=NAVY, linestyle="--", linewidth=1.5)
ax.annotate("Nasional 4,65%", xy=(4.65, 9.2), xytext=(4.0, 8.6),
            fontsize=10, color=NAVY, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=NAVY))
ax.set_title("10 Provinsi dengan TPT Tertinggi, Mei 2026 (Bali Terendah: 1,52%)")
ax.set_xlabel("TPT (%)")
save(fig, "06_provinsi_top10")

# ---------- 07: provincial trend ----------
fig, ax = plt.subplots(figsize=(11, 5.5))
xp = ["Agu 2022", "Agu 2023", "Agu 2024", "Agu 2025", "Feb 2026", "Mei 2026"]
series = {
    "Jawa Barat": [8.31, 7.44, 6.75, 6.77, 6.64, 6.61],
    "Banten": [8.09, 7.52, 6.68, 6.69, 6.59, 6.48],
    "DKI Jakarta": [7.18, 6.53, 6.21, 6.05, 6.03, 5.79],
    "Kep. Riau": [8.23, 6.80, 6.39, 6.45, 6.87, 6.45],
    "Papua": [None, None, 6.48, 6.96, 7.02, 7.08],
    "Bali": [4.80, 2.69, 1.79, 1.49, 1.59, 1.52],
}
for name, vals in series.items():
    xs = [x for x, v in zip(xp, vals) if v is not None]
    ys = [v for v in vals if v is not None]
    ax.plot(xs, ys, marker="o", label=name, linewidth=2.2)
ax.set_title("Tren TPT Provinsi 2022-2026: Jawa Barat & Banten Turun Jauh, Papua Naik")
ax.set_ylabel("TPT (%)"); ax.legend(ncol=3, fontsize=9)
ax.annotate("Papua 2022-2023\nsebelum pemekaran", xy=(1, 5.5), fontsize=8,
            color=GRAY, style="italic")
save(fig, "07_provinsi_tren")

# ---------- 08: distribution of unemployed ----------
fig, ax = plt.subplots(figsize=(10, 5.5))
edu = ["SMA", "SMK", "SD ke bawah", "SMP", "Diploma IV-S3", "Diploma I-III"]
porsi = [28.00, 22.39, 17.18, 15.65, 14.31, 2.48]
jt = [2.0216, 1.6166, 1.2404, 1.1299, 1.0332, 0.1791]
y = np.arange(len(edu))
b = ax.barh(y, porsi, color=[RED, ORANGE, GRAY, TEAL, NAVY, LIGHT], edgecolor=DARK)
ax.set_yticks(y); ax.set_yticklabels(edu); ax.invert_yaxis()
for bar, p, j in zip(b, porsi, jt):
    ax.annotate(f"{p:.2f}%  ({j:.2f} jt orang)",
                (p, bar.get_y() + bar.get_height() / 2),
                textcoords="offset points", xytext=(6, 0), va="center", fontsize=10)
ax.set_title("7,22 Juta Penganggur (Mei 2026): SMA Paling Banyak, 2,02 Jt Orang")
ax.set_xlabel("Porsi dari total penganggur (%)")
save(fig, "08_distribusi_penganggur")

# ---------- 09: formal vs informal ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
ax = axes[0]
w = ax.pie([40.58, 59.42], labels=["Formal\n40,58%", "Informal\n59,42%"],
           colors=[NAVY, ORANGE], autopct="", startangle=90,
           textprops={"fontsize": 12, "fontweight": "bold"},
           wedgeprops={"edgecolor": "white", "linewidth": 2})
ax.set_title("Status Pekerjaan (Feb 2026)")
ax = axes[1]
ind = ["Setengah\nmenganggur", "Pekerja\nparuh waktu"]
vv = [7.27, 25.97]
b = ax.bar(ind, vv, color=[TEAL, GRAY], width=0.55)
for bar, v in zip(b, vv):
    ax.annotate(f"{v:.2f}%", (bar.get_x() + bar.get_width() / 2, v),
                textcoords="offset points", xytext=(0, 6), ha="center",
                fontsize=11, fontweight="bold")
ax.set_title("Kualitas Pekerjaan (Feb 2026)"); ax.set_ylim(0, 30)
ax.set_ylabel("% dari pekerja")
fig.suptitle("6 dari 10 Pekerja Informal; 1 dari 4 Pekerja Paruh Waktu",
             fontsize=14, fontweight="bold")
save(fig, "09_formal_informal")

# ---------- 10: wages + sectors ----------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
ax = axes[0]
ax.plot(["Feb 2025", "Feb 2026", "Mei 2026"], [None, 3.29, 3.39], marker="o",
        color=GREEN, linewidth=2.5, markersize=8)
ax.set_title("Rata-rata Upah Buruh Naik"); ax.set_ylabel("Rp juta")
ax.annotate("Rp3,39 jt", xy=(2, 3.39), xytext=(1.2, 3.5),
            arrowprops=dict(arrowstyle="->", color=GREEN),
            fontsize=11, fontweight="bold", color=GREEN)
ax = axes[1]
sek = ["Akomodasi &\nmakan minum", "Transportasi &\npergudangan", "Jasa\nlainnya"]
tb = [195, 121, 110]
b = ax.bar(sek, tb, color=[TEAL, NAVY, ORANGE], width=0.6)
for bar, v in zip(b, tb):
    ax.annotate(f"+{v} rb", (bar.get_x() + bar.get_width() / 2, v),
                textcoords="offset points", xytext=(0, 6), ha="center",
                fontsize=11, fontweight="bold")
ax.set_title("Penambah Pekerja Terbanyak (Feb-Mei 2026)")
ax.set_ylabel("Ribu orang")
fig.suptitle("Upah Naik; Lapangan Kerja Baru dari Jasa & Akomodasi",
             fontsize=14, fontweight="bold")
save(fig, "10_upah_sektor")

print("done: 10 charts")
