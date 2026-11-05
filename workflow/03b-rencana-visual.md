# Tahap 3b — Rencana Visual Esai

Direncanakan **bersama kerangka (tahap 3)**, sebelum draf ditulis, lalu **dibuat dan dirender di tahap 4** bersama draf v1. Visual yang baik membawa sebagian argumen, jadi tempatnya diputuskan saat argumen disusun, bukan ditempel di akhir. Hasil: `<L>/draf/rencana-visual.md` dan spesifikasi di `<L>/visual/*.json`.

## 1. Cek aturan dulu
Baca `<L>/aturan.md` dan `<L>/profil.json`:
- Apakah gambar/tabel **boleh di badan teks** atau hanya di lampiran (`gambar_hanya_di_lampiran`)?
- Apakah gambar/tabel **dihitung** dalam batas kata atau halaman?
- Apakah rubrik menilai visual atau "kreativitas penyajian"?

Kalau visual hanya boleh di lampiran dan tidak dinilai, cukup 1–2 visual yang paling membantu argumen. Kalau dilarang sama sekali, lewati tahap ini.

## 2. Uji setiap calon visual
Satu visual hanya masuk kalau lolos tiga pertanyaan:
1. **Kalau visual ini dihapus, apakah juri kehilangan sesuatu?** Kalau teks sudah cukup, buang.
2. **Apa satu pesannya?** Tulis dalam satu kalimat. Kalimat itu jadi keterangan gambar, misalnya "Gambar 2. Kasus naik 75% dalam tiga tahun, lebih cepat dari rata-rata ASEAN".
3. **Dari mana isinya?** Setiap angka harus ada di peta klaim (`riset/sumber.md`) berstatus ✅. Gambar konsep diberi label "Ilustrasi konsep (rancangan penulis)".

Patokan jumlah: sekitar 1 visual per 600–800 kata badan teks, paling banyak 3–4 untuk satu esai. Satu visual yang tajam lebih kuat daripada lima yang biasa.

## 3. Menu visual dan alatnya

| Jenis | Kapan dipakai | Cara membuat | Rujukan pendukung |
|---|---|---|---|
| **Grafik data** (batang, garis) | Menunjukkan besarnya masalah, tren, atau perbandingan | `tools/buat_visual.py` jenis `batang`, `batang_h`, `garis` | `skills/desain/hallmark/references/data-viz.md` |
| **Diagram mekanisme/alur** | Menjelaskan cara kerja gagasan: siapa melakukan apa, urutan, alur data | `tools/buat_visual.py` jenis `alur`, `siklus` | `skills/desain/impeccable/` (kritik); diagram yang lebih bebas digambar dengan skrip sendiri bergaya sama (lihat tahap 4) |
| **Tabel pembanding** | Kondisi sekarang vs usulan, solusi lain vs usulan, biaya per komponen | Tabel Markdown di naskah (dibangun `build_docx.py`) | peta klaim (`riset/sumber.md`) untuk isi pembanding dari literatur |
| **Gambar prototipe/konsep** | Gagasan berupa alat, aplikasi, produk, atau tata ruang | Mockup HTML yang dirender jadi PNG, atau ilustrasi bersih | `skills/desain/hallmark/`, `skills/desain/impeccable/`, `skills/desain/ui-ux-pro-max/` |
| **Foto kondisi nyata** | Masalah yang paling kuat ditunjukkan langsung (lokasi, kondisi lapangan) | Hanya foto berlisensi jelas (Wikimedia Commons, rilis resmi instansi) dengan kredit | — |
| **Peta lokasi** | Gagasan menyasar daerah tertentu | Data terbuka (misalnya OpenStreetMap) dengan atribusi | skrip sendiri bergaya sama |
| **Infografis ringkas** | Hanya kalau rubrik menilai penyajian dan aturan membolehkan | HTML yang dirender jadi PNG | `skills/desain/hallmark/`, `skills/desain/banner-design/` |

## 4. Spesifikasi untuk `buat_visual.py`
Simpan satu file JSON per visual di `<L>/visual/`, lalu jalankan:
```
python tools/buat_visual.py <L>/visual/*.json --profil <L>
```
Hasilnya PNG 300 DPI di `<L>/draf/gambar/`, memakai font naskah dan satu warna aksen (bisa diatur lewat `"warna_aksen"` di profil). Data grafik tanpa `"sumber"` diberi peringatan. Contoh:

```json
{"jenis": "batang", "label": ["2020","2021","2022","2023"],
 "seri": [{"nama": "Kasus", "nilai": [120, 95, 143, 210]}],
 "sorot": 3, "sumbu_y": "Jumlah kasus", "sumber": "Kemenkes (2024)"}
```
```json
{"jenis": "alur", "langkah": [
  {"teks": "Warga memindai kemasan obat"},
  {"teks": "Aplikasi mencocokkan nomor izin BPOM", "label_panah": "data"},
  {"teks": "Hasil verifikasi", "utama": true, "catatan": "asli / palsu / tidak terdaftar"}]}
```
```json
{"jenis": "siklus", "langkah": ["Pantau", "Analisis", "Intervensi", "Evaluasi"], "pusat": "Siklus 30 hari"}
```
Jenis `alur` otomatis menurun kalau langkahnya lebih dari 5, atau pakai `"arah": "bawah"`.

## 5. Lantai visual (tidak boleh dilanggar)
- Tidak ada angka, logo, testimoni, atau tangkapan layar karangan. Mockup prototipe boleh, tapi isinya contoh yang wajar dan diberi label konsep.
- Tidak ada foto buatan AI yang tampil seolah foto asli.
- Tidak ada grafik 3D, diagram lingkaran dengan lebih dari 4 irisan, latar gradasi, bayangan, clip-art, atau kumpulan ikon dekoratif.
- Satu font (sama dengan naskah), satu warna aksen plus abu-abu, tetap terbaca kalau dicetak hitam-putih.
- Teks di dalam gambar minimal setara 8 pt saat dicetak. Judul ditulis di keterangan Word, bukan di dalam gambar.
- Setiap visual dirujuk di teks sebelum muncul ("seperti terlihat pada Gambar 1").

## 6. Palet (yang khas AI dan harus dihindari)
Diringkas dari `skills/desain/hallmark/references/craft.md` § Colour dan `gates.md`, serta `skills/desain/impeccable/reference/craft-floor.md`.

**Dihindari**
- Gradasi ungu ke biru, ungu ke pink, atau cyan menyala di latar gelap. Ini tanda "dibuat AI" yang paling umum.
- Warna bawaan framework (indigo, violet, slate gelap dari Tailwind dan sejenisnya): terlihat seperti template.
- Efek cahaya (glow), halo berwarna, sorotan di latar gelap; teks bergradasi; gradasi lebih dari 3 warna.
- Hitam atau putih murni sebagai latar bidang besar; garis tepi berwarna tebal di sisi kiri kotak.
- Merah dan hijau sebagai satu-satunya pembeda (tidak terbaca oleh buta warna dan di cetakan hitam-putih).

**Dipakai**
- Satu warna aksen sebagai sinyal (kurang dari 5% bidang), misalnya hanya untuk batang atau kotak yang paling penting.
- Abu-abu yang sedikit bernada ke arah warna aksen, latar seperti kertas, teks hampir hitam.
- Warna dipilih dari makna topik, bukan asosiasi umum (kesehatan tidak otomatis hijau-biru).
- Kontras teks minimal 4,5:1 (cek dengan panduan kontras di `skills/desain/impeccable/reference/audit.md` kalau ragu).

## 7. Isi `rencana-visual.md`
Untuk setiap visual: nomor, posisi (setelah paragraf mana, atau lampiran), jenis, satu kalimat pesan, sumber data (rujuk dossier), dan file spesifikasinya. Rencana ini ikut ditunjukkan di checkpoint tahap 3.

## 8. Pemeriksaan

### Putaran umpan balik visual (tahap 4, wajib untuk setiap gambar)
Umpan balik dari melihat gambar yang sudah dirender adalah pendorong utama mutu grafik buatan LLM (MatPlotAgent, ACL Findings 2024). Untuk setiap gambar:

1. Render dengan `python tools/buat_visual.py <L>/visual/<nama>.json --profil <L>`. Alat mencetak `PERIKSA` untuk teks bertumpuk, teks keluar kotak, dan huruf yang tercetak lebih kecil dari 8 pt.
2. **Lihat PNG-nya** (buka sebagai gambar), jangan hanya membaca keluaran alat. Cocokkan dengan § 5 (lantai visual) dan § 2 (satu pesan per gambar): apakah pesannya tertangkap dalam 3 detik, apakah angka dan label sesuai peta klaim, apakah tetap terbaca kalau dicetak hitam-putih.
3. Perbaiki spesifikasi JSON, lalu render ulang. **Paling banyak 3 putaran per gambar.** Kalau setelah 3 putaran masih ada masalah, berlaku `CLAUDE.md` § Aturan berhenti.
4. Catat di `rencana-visual.md`:

   | Gambar | Putaran | Temuan (alat + mata) | Perbaikan |
   |---|---|---|---|

   Temuan `PERIKSA` yang sengaja tidak diperbaiki wajib diberi alasan di tabel ini.

### Pemeriksaan di tahap berikutnya
- Tahap 5: juri esai juga menilai apakah setiap visual menambah argumen. Untuk kritik tampilan, pakai `impeccable critique` (`skills/desain/impeccable/`) pada halaman PDF yang sudah dirender.
- Tahap 6: `tools/cek_docx.py` memeriksa keterangan, urutan nomor, sumber, dan larangan gambar di badan teks.
