# Measure DAX — Pengangguran 2026

Cara pakai: di Power BI Desktop, klik kanan tabel yang sesuai >
**New measure**, lalu tempel rumus di bawah ini. Relasi yang dibutuhkan
(lihat `build_guide.md`):
`fact_tpt_nasional[periode_id]` → `dim_periode[periode_id]`,
`fact_tpt_segmen[periode_id]` → `dim_periode[periode_id]`,
`fact_tpt_segmen[segmen]` → `dim_segmen[segmen]`.

> Desain anti-jebakan: angka nasional HANYA ada di
> `fact_tpt_nasional`, angka segmen HANYA ada di `fact_tpt_segmen`.
> Keduanya tidak pernah tercampur (lihat
> `measures_dax_CATATAN_LEVEL.md`), jadi measure di bawah ini aman
> dipakai tanpa filter khusus.

## 1. TPT nasional

```dax
TPT Nasional =
AVERAGE ( fact_tpt_nasional[tpt_persen] )
```

```dax
TPT Periode Lalu =
VAR u = MAX ( dim_periode[urutan_nasional] )
RETURN
    CALCULATE (
        [TPT Nasional],
        FILTER ( ALL ( dim_periode ), dim_periode[urutan_nasional] = u - 1 )
    )
```

```dax
Perubahan TPT (pp) =
[TPT Nasional] - [TPT Periode Lalu]
```

```dax
Angkatan Kerja (jt) =
SUM ( fact_tpt_nasional[angkatan_kerja_jt] )
```

```dax
Penganggur (jt) =
SUM ( fact_tpt_nasional[penganggur_jt] )
```

```dax
Bekerja (jt) =
SUM ( fact_tpt_nasional[bekerja_jt] )
```

```dax
Upah Buruh Rata-rata (jt) =
AVERAGE ( fact_tpt_nasional[upah_buruh_jt] )
```

## 2. TPT segmen (pendidikan / umur / gender / daerah / provinsi)

```dax
TPT Segmen =
AVERAGE ( fact_tpt_segmen[tpt_persen] )
```

```dax
Gap vs Nasional (pp) =
[TPT Segmen] - [TPT Nasional]
```

> `[TPT Nasional]` di sini otomatis mengikuti periode yang dipilih di
> visual, karena kedua tabel fakta terhubung ke `dim_periode` yang sama.
> Tidak ada baris nasional di `fact_tpt_segmen`, jadi tidak ada
> kontaminasi.

```dax
Rasio vs Nasional =
DIVIDE ( [TPT Segmen], [TPT Nasional] )
```

```dax
Peringkat Segmen =
RANKX ( ALL ( dim_segmen[segmen] ), [TPT Segmen],, DESC )
```

## 3. Indikator pasar kerja (dari fact_indikator)

```dax
Pekerja Formal % =
CALCULATE (
    AVERAGE ( fact_indikator[nilai] ),
    fact_indikator[indikator] = "formal_persen"
)
```

```dax
Pekerja Informal % =
CALCULATE (
    AVERAGE ( fact_indikator[nilai] ),
    fact_indikator[indikator] = "informal_persen"
)
```

```dax
Setengah Menganggur % =
CALCULATE (
    AVERAGE ( fact_indikator[nilai] ),
    fact_indikator[indikator] = "setengah_menganggur_persen"
)
```

```dax
Pekerja Paruh Waktu % =
CALCULATE (
    AVERAGE ( fact_indikator[nilai] ),
    fact_indikator[indikator] = "paruh_waktu_persen"
)
```

## 4. Format tampilan yang disarankan

| Measure | Format |
|---|---|
| TPT Nasional, TPT Segmen, Gap vs Nasional (pp), Perubahan TPT (pp) | Decimal / Percentage, 2 desimal, suffix "pp" untuk selisih |
| Rasio vs Nasional, Peringkat Segmen | Decimal 2 desimal / Whole number |
| Angkatan Kerja, Penganggur, Bekerja (jt) | Decimal, 2 desimal |
| Upah Buruh Rata-rata | Currency Rp, 2 desimal (dalam jt) |
| Pekerja Formal %, Informal % | Percentage, 2 desimal |
