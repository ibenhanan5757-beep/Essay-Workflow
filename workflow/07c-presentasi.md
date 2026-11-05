# Tahap 7C — Presentasi / PPT (opsional)

**Hanya dikerjakan kalau penulis meminta PPT, slide, atau pitch deck.** Workflow utama selesai di tahap 6 (file Word/PDF). Jangan lanjut ke tahap ini otomatis, walaupun lomba punya babak presentasi. Cukup ingatkan sekali di checkpoint tahap 6 bahwa babak presentasi ada dan PPT bisa dibuat kalau diminta.

Bahan: `<L>/draf/final.md` (atau file Word final yang diberikan penulis, dibaca dengan skill `docx`), `<L>/aturan.md`, peta klaim `<L>/riset/sumber.md`, dan gambar di `<L>/draf/gambar/`. Semua hasil disimpan di `<L>/presentasi/`.

## 1. Aturan presentasi
Dari guidebook atau pengumuman finalis, isi `<L>/presentasi/aturan-presentasi.md` dengan nomor halamannya:
- durasi presentasi dan durasi tanya-jawab
- batas jumlah slide, rasio (16:9 / 4:3), format kirim (PPTX, PDF, atau tampil langsung), nama file
- template wajib dari panitia, logo yang boleh/harus dipakai, larangan identitas sekolah
- dikirim sebelum hari H atau dibawa saat tampil

## 2. Kalau penulis memberi contoh PPT
Taruh file contoh di `<L>/presentasi/contoh/`. Lihat dulu contohnya dengan dua cara: `python tools/cek_pptx.py gaya <file> --out <L>/presentasi/gaya-contoh.md` untuk angka-angkanya, lalu render setiap slide jadi gambar (PDF lewat LibreOffice/PowerPoint, lalu per halaman) dan lihat langsung. Contoh berbentuk PDF dibaca dengan `tools/baca_pdf.py` dan dilihat sebagai gambar. Lalu tentukan contohnya termasuk yang mana:

| Jenis contoh | Yang dilakukan | Yang tidak boleh |
|---|---|---|
| **A. Template wajib panitia** | Pakai file itu sebagai dasar: master slide, tata letak, logo panitia, dan warnanya dipertahankan. Isi dengan skill `pptx`. Lantai di § 4 tetap berlaku untuk **isi** (kata, butir, judul, ukuran huruf). | Mengganti warna atau font template, menghapus logo panitia. Kalau template sendiri memakai gradasi atau warna ungu, itu milik panitia; catat di laporan, jangan dianggap kesalahan. |
| **B. Contoh gaya** ("buat seperti ini") | Tiru gayanya: rasio, pasangan font, palet, kepadatan kata, pola tata letak, perlakuan gambar, posisi judul. Tulis ringkasan gaya yang diambil di `gaya-contoh.md`. | Menyalin isi, teks, logo, nama, foto milik orang lain, atau identitas merek. |
| **C. Contoh juara/peserta lain** | Pelajari alur cerita, jumlah slide, cara membuka dan menutup, dan apa yang membuatnya kuat. Catat pelajarannya di `gaya-contoh.md`. | Meniru struktur kalimat, desain, atau gagasannya. |
| **D. Tidak ada contoh** | Pakai gaya bawaan: font naskah (atau satu sans-serif untuk judul + font naskah untuk isi), palet yang sama dengan visual esai (satu aksen + abu-abu), latar terang seperti kertas. | — |

Kalau contoh jenis B memiliki ciri slide AI (gradasi ungu-biru, emoji, ikon tempelan, 6+ butir per slide, glow), sebutkan ke penulis dan tanya **sekali**: ikuti persis, atau ambil gayanya tanpa ciri itu. Rekomendasi: tanpa ciri itu. Kalau penulis tidak menjawab, kerjakan versi tanpa ciri itu dan sebutkan bedanya.

Kalau jenisnya tidak jelas (misalnya penulis hanya mengirim file tanpa keterangan), anggap B dan sebutkan anggapan itu.

## 3. Alur slide (strategi presentasi lomba)
Pola pitch investor (YC, Kawasaki) di `skills/desain/design-system/` tidak dipakai, karena juri lomba menilai gagasan, bukti, dan kelayakan, bukan peluang investasi. Pakai alur ini dan sesuaikan dengan durasi. Patokan: 5 menit → 7–8 slide, 7 menit → 9–10 slide, 10 menit → sekitar 12 slide.

| # | Tujuan slide | Pola tata letak | Isi | Waktu |
|---|---|---|---|---|
| 1 | Pembuka | Judul + satu gambar atau angka ciri khas | Judul esai (atau versi kalimatnya), nama tim hanya kalau dibolehkan | 20 dtk |
| 2 | Masalah | Angka besar | Satu angka terkuat dari peta klaim + sumber kecil | 40 dtk |
| 3 | Celah | Sebelum-sesudah atau tabel pembanding | Kenapa solusi yang ada belum berhasil | 40 dtk |
| 4 | Gagasan | Satu kalimat besar + satu visual | Tesis dalam satu kalimat | 30 dtk |
| 5 | Cara kerja | Diagram alur | Siapa melakukan apa, urutannya (gambar dari `buat_visual.py`) | 60 dtk |
| 6 | Bukti | Grafik fokus atau dua kolom | Dasar ilmiah dan data pendukung | 50 dtk |
| 7 | Kelayakan | Garis waktu atau tabel | Pelaksana, biaya, tahapan, risiko utama | 50 dtk |
| 8 | Dampak | Dua atau tiga indikator | Ukuran keberhasilan yang bisa dicek | 40 dtk |
| 9 | Penutup | Satu kalimat besar | Pesan yang ingin diingat juri | 20 dtk |
| + | Slide cadangan (setelah penutup, tidak ditampilkan) | Bebas | Jawaban pertanyaan sulit: data tambahan, perhitungan biaya, perbandingan | — |

Simpan rencana di `<L>/presentasi/alur-slide.md`: nomor, judul-kalimat, pola, visual, angka (ID peta klaim), dan detik.

## 4. Lantai slide (anti "slide buatan AI")
Tidak boleh dilanggar, kecuali bagian yang ditentukan template wajib panitia.

**Isi**
- Judul slide = kalimat kesimpulan, paling banyak 12 kata ("Kasus obat ilegal naik 75% dalam tiga tahun"). Judul label seperti "Latar Belakang", "Solusi", "Pembahasan" tidak dipakai.
- Paling banyak 30 kata per slide (slide tabel boleh lebih), paling banyak 3 butir, tanpa sub-butir. Penjelasan pindah ke naskah bicara.
- Satu pesan dan satu visual dominan per slide.
- Angka hanya dari peta klaim, dengan sumber kecil di slide yang sama.
- Tidak ada slide "Agenda/Daftar Isi" untuk presentasi 10 menit atau kurang, dan tidak ada slide "Terima Kasih" kosong. Slide terakhir berisi pesan penutup.
- Tidak ada istilah yang tidak dijelaskan, singkatan tanpa kepanjangan, atau kutipan tokoh sebagai hiasan.

**Tampilan**
- Huruf isi minimal 18 pt (idealnya 24 pt), judul minimal 28 pt, sumber minimal 12 pt.
- Paling banyak 2 keluarga huruf. Satu warna aksen ditambah abu-abu; latar terang seperti kertas, atau satu latar gelap yang konsisten.
- Dilarang: gradasi ungu-biru/ungu-pink, cyan menyala di latar gelap, glow, bayangan tebal, emoji, ikon tempelan, clip-art, ilustrasi atau foto stok AI generik, kartu di dalam kartu, label kapital yang direnggangkan, bingkai dekoratif, tanda air.
- Posisi judul, margin, dan grid sama di semua slide. Rata kiri lebih tenang daripada semua rata tengah.
- Animasi: tidak ada, atau muncul sederhana untuk membuka langkah satu per satu. Tanpa transisi berputar atau memantul.
- Gambar: dari esai (`buat_visual.py`), foto berlisensi dengan kredit, atau tangkapan layar/mockup prototipe berlabel "ilustrasi konsep". Untuk slide, buat ulang grafik dengan `"lebar_cm": 12` lalu tempatkan selebar sekitar 24 cm, supaya teks di dalam grafik setara sekitar 20 pt.

Rujukan desain: `skills/presentasi/slides/references/layout-patterns.md` (pola tata letak), `skills/desain/hallmark/` (lantai dan palet), `workflow/03b-rencana-visual.md` § Palet.

## 5. Naskah bicara
Isi `templates/naskah-bicara.md` untuk setiap slide, dan salin ke catatan pembicara (speaker notes) di PPTX. Patokan kecepatan bicara sekitar 130 kata per menit. Total naskah harus selesai 20–30 detik sebelum batas waktu. Kalimat pembuka tidak dimulai dengan "Assalamualaikum ... baiklah ... pada kesempatan kali ini" yang panjang; salam singkat lalu langsung masalah.

## 6. Membuat file
| Kebutuhan | Cara | Skill |
|---|---|---|
| PPTX yang bisa diedit (default) | dibangun dari alur slide dengan python-pptx | `pptx` (akun) |
| Template wajib panitia | isi file template, jangan membuat dari nol | `pptx` (akun) |
| Presentasi dari browser | HTML 16:9 | `skills/presentasi/slides/`, `skills/desain/hallmark/` |
| Canva diminta penulis | penulis mengerjakannya di Canva dari alur slide dan naskah bicara | — |

Simpan `<L>/presentasi/slide.pptx` dan versi PDF-nya, dengan nama file sesuai aturan.

## 7. Uji
1. `python tools/cek_pptx.py cek <L>/presentasi/slide.pptx --durasi <menit> --maks-slide <batas>`. Semua KRITIS dan MAYOR harus beres (kecuali yang berasal dari template wajib panitia, dicatat).
2. Render setiap slide jadi gambar dan lihat satu per satu. **Uji 3 detik**: apakah pesan slide tertangkap dalam 3 detik? Kritik tampilan dengan `impeccable critique` (`skills/desain/impeccable/`).
3. Hitung kata naskah bicara: total kata ÷ 130 ≤ durasi − 0,5 menit.
4. **Simulasi juri** (`templates/prompt-juri-presentasi.md`): tiga juri di konteks baru melihat gambar slide dan naskah bicara, memberi skor, lalu mengajukan pertanyaan. Dari semua pertanyaan, pilih 5 yang paling mematikan (gabungkan dengan temuan devil's advocate di tahap 5). Siapkan untuk masing-masing: jawaban yang bisa diucapkan dalam 30 detik, sumbernya (ID peta klaim), dan slide cadangan kalau perlu. Simpan di `<L>/presentasi/tanya-jawab.md`.

## Checkpoint
Tunjukkan gambar semua slide, naskah bicara, dan daftar tanya-jawab. Penulis menyetujui sebelum file final dibuat atau dikirim.
