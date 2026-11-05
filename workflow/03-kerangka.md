# Tahap 3 — Kerangka Argumen

Sumber: `skills/esai/academic-research-skills/argument_builder_agent.md`, `intro_title_rhetoric_guide.md`. Langkah 1, 4, dan 6 ditambahkan 5 Nov 2026 dari riset:
- "Argument Collapse" (arXiv 2606.01736, 2026): dari 23 ribu esai lima model termasuk Claude, hanya 3,4% argumen utama LLM yang unik, dibanding 65,3% pada esai manusia, dan strukturnya seragam.
- DARE (EMNLP 2025): kerangka yang dikembangkan "dalam dulu, baru lebar" dan diuji lewat debat pembela–penyerang menghasilkan argumen yang lebih logis dan beragam.

Urutan kerja: struktur → pohon argumen → CER → cek argumen pasaran → kontra-argumen → debat kerangka → pendahuluan → alokasi kata → judul → rencana visual. Hasil di `<L>/draf/kerangka.md`.

## 1. Pilih struktur esai secara sadar
Esai buatan LLM paling sering memakai pola "dukungan → usulan" (29% vs 12% pada esai manusia). Pilih struktur yang paling menguatkan tesis, lalu tulis pilihan dan alasannya (1 kalimat) di awal `kerangka.md`.

| Struktur | Cocok kalau |
|---|---|
| Masalah → sebab → solusi | Sebabnya sendiri adalah temuan baru. Kalau memilih ini, tulis kenapa lebih kuat daripada minimal satu pilihan lain |
| Kasus dulu | Ada satu kasus nyata terverifikasi yang langsung memperlihatkan masalahnya |
| Mitos lawan fakta | Anggapan umum (termasuk ide pasaran) bisa dibantah dengan data |
| Kontra-argumen dulu | Pandangan populer kuat dan esai ini menawarkan koreksi |
| Perbandingan | Kondisi sekarang vs usulan, atau daerah/negara yang sudah berhasil vs yang belum |
| Apa yang berubah | Teknologi, regulasi, atau data 2–3 tahun terakhir membuka jalan yang dulu tidak ada |

Kalau guidebook mewajibkan susunan bab (misalnya LKTI), ikuti guidebook. Pilihan struktur lalu berlaku untuk urutan argumen di dalam bab isi.

## 2. Pohon argumen
```
Tesis: [klaim utama]
├── A1: [argumen utama, yang paling menentukan tesis]
│   ├── A1.1: [sub-klaim]
│   │   ├── Bukti: [sumber + temuan + ID peta klaim, mis. K3]
│   │   └── Penalaran: [kenapa bukti ini mendukung sub-klaim]
│   └── A1.2: ...
├── A2: ...
├── (A3 hanya kalau memang ada; 2 argumen kuat lebih baik dari 3 yang dipaksakan)
├── Kontra-argumen terkuat + bantahan
└── Solusi / rekomendasi: siapa melakukan apa, bagaimana, kenapa realistis
```
**Dalam dulu, baru lebar.** Kembangkan A1 sampai dua tingkat (argumen → sub-klaim → bukti) sebelum menambah A2. Setiap simpul diberi nomor (A1, A1.1, …) supaya bisa dirujuk di langkah 4 dan 6.

## 3. Rantai Klaim–Bukti–Penalaran (CER)
Untuk tiap argumen isi tabel:

| Klaim | Bukti | Penalaran |
|-------|-------|-----------|
| | | |

Penalaran adalah bagian yang paling sering hilang di essay pelajar. Bukti tanpa penalaran = tempelan data.

## 4. Cek argumen pasaran
Ide yang baru pun bisa ditopang argumen yang sama dengan esai lain. Langkah ini memastikan argumennya juga tidak pasaran.

1. Panggil satu subagent lewat agen `juri-esai` dengan `templates/prompt-argumen-pasaran.md`. Kirim **hanya** tema, jenjang, dan tesis 2 kalimat; jangan kirim dossier atau kerangka.
2. Simpan jawabannya di `<L>/draf/argumen-pasaran.md`: daftar argumen, struktur, dan jenis data yang paling umum untuk tesis ini.
3. Tandai setiap argumen dan sub-klaim di pohon dengan **[pasaran]** (sama atau sangat mirip dengan daftar) atau **[khas]**.
4. **Syarat:** minimal satu argumen utama atau sub-klaim kunci berstatus [khas] dan bersandar pada bukti dossier (ID peta klaim). Argumen [pasaran] boleh tetap ada kalau buktinya lokal dan spesifik, tetapi jangan jadi tulang punggung esai. Kalau tidak ada argumen [khas] yang berbukti, berlaku `CLAUDE.md` § Aturan berhenti: laporkan, jangan memaksakan.

## 5. Kontra-argumen
| Argumen | Keberatan terkuat | Strategi |
|---------|-------------------|----------|
| | | Bantah / Akui lalu batasi / Ubah sudut pandang / Akui sebagai keterbatasan |

## 6. Debat kerangka (pembela lawan penyerang)
Kelemahan logika paling murah diperbaiki sekarang, sebelum ada satu kalimat naskah. Devil's advocate di tahap 5 tetap berjalan; langkah ini tidak menggantikannya.

1. **Putaran 1.** Panggil subagent penyerang lewat agen `juri-esai` dengan `templates/prompt-serang-kerangka.md`. Kirim kerangka ringkas: struktur, pohon bernomor, CER, kontra-argumen yang direncanakan, dan solusi. Jangan kirim dossier atau proses Arena Ide.
2. **Pembelaan.** Agen utama menjawab setiap poin serangan di `<L>/draf/debat-kerangka.md`:

   | Poin serangan | Simpul | Jawaban: dijawab dengan bukti (ID) / kerangka diubah / diakui sebagai keterbatasan | Perubahan di kerangka |
   |---|---|---|---|

   Jawaban "dijawab dengan bukti" wajib menyebut ID peta klaim. Kalau buktinya tidak ada, pilih "kerangka diubah" atau "diakui".
3. **Putaran 2** hanya kalau putaran 1 mengubah argumen utama (A1) atau tesis: serang kerangka yang sudah diubah dengan prompt yang sama. Paling banyak 2 putaran.
4. Serangan terkuat yang tidak bisa dibantah tuntas menjadi kontra-argumen di esai ("akui lalu batasi"), bukan disembunyikan.

## 7. Struktur pendahuluan (model CARS, 3 langkah)
1. **Bangun wilayah:** kenapa topik ini penting *sekarang* (pakai data, bukan "di era globalisasi ini").
2. **Tunjukkan celah:** apa yang belum terjawab / salah kaprah / belum berhasil. Celah harus didukung riset; jangan klaim "belum ada yang meneliti" tanpa bukti. Bahannya: kalimat posisi dan tabel karya terdekat dari cek "sudah ada?" di `<L>/ide/final.md`.
3. **Isi celah:** satu kalimat tujuan/tesis yang tegas, menjawab celah tadi persis.

Hindari: pembuka terlalu lebar ("Sejak zaman dahulu..."), daftar sumber tanpa sintesis, tesis yang tersembunyi di tengah paragraf.

## 8. Alokasi kata
Contoh untuk batas 1.500 kata (sesuaikan dengan aturan lomba):
- Pendahuluan 15% · Isi/argumen 55% · Solusi 20% · Penutup 10%

## 9. Judul
Buat 3–5 kandidat. Cek:
- Kata kunci tema ada di 3–4 kata pertama
- Spesifik (tidak cocok untuk 50 essay lain)
- Tidak memakai pembuka kosong ("Sebuah Kajian tentang...", "Menuju...")
- Klaim di judul tidak lebih kuat dari isi
- Judul berbentuk "frasa menarik: subjudul jelas" boleh, asal frasa depannya tetap informatif

## 10. Rencana visual
Putuskan grafik, diagram, tabel, atau gambar prototipe **bersama kerangka**, karena visual yang baik membawa sebagian argumen. Ikuti `workflow/03b-rencana-visual.md`, hasilnya `<L>/draf/rencana-visual.md`. Di pohon argumen, tandai argumen mana yang dibantu visual (misalnya "Bukti: K3 → Gambar 1").

## Checkpoint
Tunjukkan kerangka lengkap (struktur yang dipilih dan alasannya, pohon bernomor dengan tanda [pasaran]/[khas]), ringkasan `argumen-pasaran.md`, tabel `debat-kerangka.md` beserta perubahan yang dibuat, kandidat judul, dan rencana visual. Penulis menyetujui sebelum menulis draf.
