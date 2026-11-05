# Evaluasi — [nama lomba]

Panduan: `workflow/08-evaluasi.md`. Angka mesin juga diisi di `hasil.json`.

## 8a Retro proses (segera setelah kirim)
- **Dikirim:** [tanggal, jam] / tidak dikirim (alasan)
- **Mode & ukuran Arena:** [penuh / Kilat / lainnya + rincian] · **versi workflow:** [tanggal di catatan/riwayat-workflow.md]
- **Kuota/waktu:** ringkasan dari `STATUS.md` § Log kuota. Baris tanpa catatan ditulis "tidak tercatat".

| Tahap / utas | Kenaikan limit 5 jam (poin %) | Konteks utas terbesar (token) | Subagent (jumlah × model) | Limit habis? |
|---|---|---|---|---|

- **Tahap termahal:** [tahap dengan kenaikan limit 5 jam terbesar] · **limit 5 jam / mingguan pernah habis:** [ya/tidak, kapan]

### Statistik juri
[tempel keluaran `python tools/evaluasi.py juri <L>`]

### Penyimpangan dari workflow
| Langkah | Yang dilakukan | Alasan | Akibat |
|---|---|---|---|

### Hambatan
| Hambatan | Tahap | Dampak (waktu / kuota / mutu) | Dugaan sebab |
|---|---|---|---|

### Pilihan penulis
- Rekomendasi Arena: [juara/cadangan atau Pilihan A/B]
- Dipilih penulis: [ID + judul] · alasan kalau berbeda:
- Jalur cadangan tahap 2 dipakai? [ya/tidak]

### Pelajaran kandidat
| # | Kejadian | Dugaan sebab | Usulan | Jenis (bug / proses / hipotesis / risiko) | ID di buku pelajaran |
|---|---|---|---|---|---|

## 8b Retro hasil (setelah pengumuman)
- **Hasil:** [juara / finalis / tidak lolos] · peringkat: · jumlah peserta: · sumber pengumuman (link):
- **Skor/komentar juri** (kutip persis + sumber):

### Juara lomba ini (juga disalin ke `catatan/bank-juara.md`)
Tulis setiap juara sebagai kartu supaya bisa dicek dengan `python tools/arena.py mirip <L>/evaluasi.md <L>/ide/loop-*.md`.

### W01. [judul juara 1]
- Inti ide: [≤2 kalimat, dari abstrak/pengumuman]
- Sumber: [link]

### Kemiripan dengan ide kita
| Juara | Ide kita yang paling mirip | Kemiripan | Nasib ide itu di Arena (peringkat/skor/gugur) | Bacaan |
|---|---|---|---|---|

### Uji balik
- Ide kita vs [juara]: urutan 1 → [pemenang], urutan 2 → [pemenang] · kesimpulan: juri AI memilih juara asli? [ya / tidak / seri]

### Rubrik resmi
- Kriteria yang kemungkinan menentukan hasil:
- Skor juri AI terakhir (`draf/review-vN.md`) dibandingkan dengan skor resmi:

### Pelajaran tambahan
| # | Kejadian | Dugaan sebab | Usulan | Jenis | ID di buku pelajaran |
|---|---|---|---|---|---|
