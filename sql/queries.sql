-- Verification queries: every headline number recomputed independently
-- from the compiled tables. Run: sqlite3 data/pengangguran_2026.db < sql/queries.sql

-- 1. National TPT series
SELECT periode, tpt_persen FROM tpt_nasional;

-- 2. Education paradox: SMK vs SD, Agu 2026 (expect 8.20, 2.24, gap 5.96)
SELECT pendidikan, agu_2026 FROM tpt_pendidikan
WHERE pendidikan IN ('SMK', 'SD ke bawah');
SELECT ROUND(
  (SELECT agu_2026 FROM tpt_pendidikan WHERE pendidikan = 'SMK') -
  (SELECT agu_2026 FROM tpt_pendidikan WHERE pendidikan = 'SD ke bawah'), 2)
  AS smk_vs_sd_gap_pp;

-- 3. SMK trend Feb 2024 -> Agu 2026 (expect 8.62, 9.01, 8.00, 8.63, 7.74, 7.68, 8.20)
SELECT feb_2024, agu_2024, feb_2025, agu_2025, feb_2026, mei_2026, agu_2026
FROM tpt_pendidikan
WHERE pendidikan = 'SMK';

-- 4. Youth 15-24: Agu 2025 vs Agu 2026 (expect 16.89 -> 17.50, +0.61 pp)
SELECT agu_2025, agu_2026,
       ROUND(agu_2026 - agu_2025, 2) AS naik_pp
FROM tpt_umur WHERE kelompok_umur = '15-24 tahun';

-- 5. Youth vs national ratio Agu 2026 (expect ~3.68)
SELECT ROUND(
  (SELECT agu_2026 FROM tpt_umur WHERE kelompok_umur = '15-24 tahun') /
  (SELECT tpt_persen FROM tpt_nasional WHERE periode = 'Agu 2026'), 2)
  AS muda_vs_nasional;

-- 6. Urban vs rural gap Agu 2026 (expect 5.53 vs 3.45, gap 2.08)
SELECT daerah, agu_2026 FROM tpt_daerah;
SELECT ROUND(
  (SELECT agu_2026 FROM tpt_daerah WHERE daerah = 'Perkotaan') -
  (SELECT agu_2026 FROM tpt_daerah WHERE daerah = 'Perdesaan'), 2)
  AS urban_rural_gap_pp;

-- 7. Gender Agu 2026 (expect laki-laki 4.64 vs perempuan 4.93; perempuan lebih tinggi)
SELECT jenis_kelamin, agu_2026 FROM tpt_gender;

-- 8. Top-10 provinces Agu 2026
SELECT provinsi, agu_2026 FROM tpt_provinsi
WHERE agu_2026 IS NOT NULL
ORDER BY agu_2026 DESC LIMIT 10;

-- 9. Papua vs Bali ratio Agu 2026 (expect 7.12 / 1.42 = 5.01)
SELECT ROUND(
  (SELECT agu_2026 FROM tpt_provinsi WHERE provinsi = 'Papua') /
  (SELECT agu_2026 FROM tpt_provinsi WHERE provinsi = 'Bali'), 2)
  AS papua_vs_bali;

-- 10. Distribution of unemployed sums to ~100 (expect 100.01, rounding)
SELECT ROUND(SUM(porsi_persen), 2) AS total_porsi FROM distribusi_penganggur;

-- 11. Unemployed by education in jt (Agu 2026: 7.38 jt * porsi)
SELECT pendidikan, porsi_persen,
       ROUND(7.38 * porsi_persen / 100, 4) AS juta_orang
FROM distribusi_penganggur ORDER BY porsi_persen DESC;

-- 12. Formal vs informal Agu 2026 (expect 42.07 vs 57.93)
SELECT indikator, agu_2026 FROM pasar_kerja
WHERE indikator LIKE 'Pekerja formal (persen)' OR indikator LIKE 'Pekerja informal (persen)';

-- 13. Sector job additions Feb-May 2026 (latest sector-change period BPS published)
SELECT sektor, tambah_ribu_orang FROM sektor ORDER BY tambah_ribu_orang DESC;

-- 14. Wage Mei 2026 -> Agu 2026 (expect 3.39 -> 3.42)
SELECT periode, upah_buruh_jt FROM tpt_nasional
WHERE periode IN ('Mei 2026', 'Agu 2026');
