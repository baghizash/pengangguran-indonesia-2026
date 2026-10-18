-- Verification queries: every headline number recomputed independently
-- from the compiled tables. Run: sqlite3 data/pengangguran_2026.db < sql/queries.sql

-- 1. National TPT series
SELECT periode, tpt_persen FROM tpt_nasional;

-- 2. Education paradox: SMK vs SD, Mei 2026 (expect 7.68, 2.31, gap 5.37)
SELECT pendidikan, mei_2026 FROM tpt_pendidikan
WHERE pendidikan IN ('SMK', 'SD ke bawah');
SELECT ROUND(
  (SELECT mei_2026 FROM tpt_pendidikan WHERE pendidikan = 'SMK') -
  (SELECT mei_2026 FROM tpt_pendidikan WHERE pendidikan = 'SD ke bawah'), 2)
  AS smk_vs_sd_gap_pp;

-- 3. SMK trend Feb 2024 -> Mei 2026 (expect 8.62, 8.00, 7.74, 7.68)
SELECT feb_2024, feb_2025, feb_2026, mei_2026 FROM tpt_pendidikan
WHERE pendidikan = 'SMK';

-- 4. Youth 15-24: Feb 2026 vs Mei 2026 (expect 16.36 -> 17.37, +1.01 pp)
SELECT feb_2026, mei_2026,
       ROUND(mei_2026 - feb_2026, 2) AS naik_pp
FROM tpt_umur WHERE kelompok_umur = '15-24 tahun';

-- 5. Youth vs national ratio Mei 2026 (expect ~3.74)
SELECT ROUND(
  (SELECT mei_2026 FROM tpt_umur WHERE kelompok_umur = '15-24 tahun') /
  (SELECT tpt_persen FROM tpt_nasional WHERE periode = 'Mei 2026'), 2)
  AS muda_vs_nasional;

-- 6. Urban vs rural gap Feb 2026 (expect 5.60 vs 3.20, gap 2.40)
SELECT daerah, feb_2026 FROM tpt_daerah;
SELECT ROUND(
  (SELECT feb_2026 FROM tpt_daerah WHERE daerah = 'Perkotaan') -
  (SELECT feb_2026 FROM tpt_daerah WHERE daerah = 'Perdesaan'), 2)
  AS urban_rural_gap_pp;

-- 7. Gender gap Feb 2026 (expect 4.88 vs 4.36, gap 0.52)
SELECT jenis_kelamin, feb_2026 FROM tpt_gender;

-- 8. Top-10 provinces Mei 2026
SELECT provinsi, mei_2026 FROM tpt_provinsi
WHERE mei_2026 IS NOT NULL
ORDER BY mei_2026 DESC LIMIT 10;

-- 9. Papua vs Bali ratio Mei 2026 (expect 7.08 / 1.52 = 4.66)
SELECT ROUND(
  (SELECT mei_2026 FROM tpt_provinsi WHERE provinsi = 'Papua') /
  (SELECT mei_2026 FROM tpt_provinsi WHERE provinsi = 'Bali'), 2)
  AS papua_vs_bali;

-- 10. Distribution of unemployed sums to ~100
SELECT ROUND(SUM(porsi_persen), 2) AS total_porsi FROM distribusi_penganggur;

-- 11. Unemployed by education in jt (Mei 2026: 7.22 jt * porsi)
SELECT pendidikan, porsi_persen,
       ROUND(7.22 * porsi_persen / 100, 4) AS juta_orang
FROM distribusi_penganggur ORDER BY porsi_persen DESC;

-- 12. Formal vs informal Feb 2026 (expect 40.58 vs 59.42)
SELECT indikator, feb_2026 FROM pasar_kerja
WHERE indikator LIKE 'Pekerja formal (persen)' OR indikator LIKE 'Pekerja informal (persen)';

-- 13. Sector job additions Feb-May 2026
SELECT sektor, tambah_ribu_orang FROM sektor ORDER BY tambah_ribu_orang DESC;

-- 14. Wage Feb 2026 -> Mei 2026 (expect 3.29 -> 3.39)
SELECT periode, upah_buruh_jt FROM tpt_nasional
WHERE periode IN ('Feb 2026', 'Mei 2026');
