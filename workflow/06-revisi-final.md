# Tahap 6 — Revisi & Finalisasi

## Revisi
- Kerjakan temuan Kritis → Mayor → Minor. Catat setiap perubahan dan kriteria yang disasarnya di `review-vN.md` § Log perubahan, supaya perubahan yang kalah di perbandingan berpasangan bisa dibatalkan.
- **Jangan menggeser kekuatan klaim diam-diam**: jangan menghapus batasan ("di wilayah ini", "data awal") atau menaikkan "berkaitan" jadi "menyebabkan" tanpa bukti baru.
- Sumber atau angka baru harus lewat `cari_sumber.py`, dibaca, dan masuk peta klaim (`<L>/riset/sumber.md`) dengan status ✅ sebelum ditulis di naskah.
- Simpan setiap versi di `<L>/draf/` (`draf-v1.md`, `draf-v2.md`, ...) supaya juri bisa membandingkan berpasangan. Versi baru dibuat dengan menyalin versi lama lalu mengubah bagian yang perlu dengan Edit, bukan menulis ulang seluruh naskah ke percakapan. Cara ini hemat konteks, dan `--banding` tetap bisa membandingkan kedua versi.
- Setelah revisi, jalankan `python skills/esai/naskah-id/scripts/periksa.py --banding <L>/draf/draf-vN.md <L>/draf/draf-vN+1.md`. Laporan ini menunjukkan angka, sitasi, dan kutipan yang hilang atau bertambah. Setiap baris harus bisa dijelaskan.

## Build file kirim (otomatis)
```
python tools/build_docx.py <L>/draf/final.md --profil <L> --out "<L>/kirim/<nama file sesuai aturan>.docx" --pdf
```
Format halaman (kertas, font, ukuran, spasi, margin, rata, indent, judul, nomor halaman) diambil dari profil, jadi tidak perlu diatur manual di Word. PDF dibuat lewat LibreOffice atau MS Word (`pip install docx2pdf`).

Format Markdown untuk naskah final:
```
# Judul Esai

Paragraf pendahuluan... (Penulis, 2023)

Paragraf isi...

## Daftar Pustaka

Penulis, A. (2023). Judul. *Jurnal*, *1*(2), 3–4. https://doi.org/...
Lembaga Lengkap [SINGKATAN]. (2024). *Judul laporan*. https://...

## Lampiran

![Gambar 1. Keterangan](gambar/grafik1.png)
```
Daftar Pustaka: satu entri per baris (atau per butir `-`). Baris yang diawali spasi dianggap lanjutan entri sebelumnya. Komentar `<!--Kn-->` boleh tetap ada di final.md karena tidak tercetak. Subjudul di dalam isi opsional. Kalau lomba tidak meminta subjudul eksplisit, cukup paragraf.

Gambar dan tabel di Markdown:
```
![Gambar 1. Kasus naik 75% dalam tiga tahun](gambar/gambar1.png)
Sumber: Kemenkes (2024), diolah.

Tabel 1. Perbandingan cara sekarang dan usulan
| Aspek | Sekarang | Usulan |
|---|---|---|
| Waktu | 5–10 menit | < 1 menit |
Sumber: rancangan penulis.
```
Keterangan gambar ada di bawah gambar, keterangan tabel di atas tabel, dan baris "Sumber:" di bawahnya. Gambar dibuat dengan `tools/buat_visual.py` (lihat `workflow/03b-rencana-visual.md`).

## Tampilan naskah profesional (bukan "format AI")
Juri membuka file sebelum membaca isinya. Naskah yang terlihat seperti artikel jurnal memberi kesan serius sejak halaman pertama; naskah yang penuh tebal, warna, emoji, dan poin-poin langsung terlihat seperti salinan chatbot. `build_docx.py` sudah mengatur sebagian besar ini otomatis. Tugas penulisan:

- **Wajib:** satu font, teks hitam; judul bagian lewat `##`/`###` (jadi Heading Word); paragraf utuh, bukan poin-poin; setiap gambar dan tabel dirujuk di teks sebelum muncul, nomornya urut, dan ada sumbernya; daftar pustaka satu gaya (APA 7 kalau aturan tidak menentukan), urut abjad.
- **Dilarang di badan esai:** emoji, teks berwarna, stabilo, kotak berbayang, garis hiasan, poin-poin (bullet) sebagai pengganti paragraf, huruf tebal di tengah kalimat, huruf kapital semua untuk penekanan, tanda pisah panjang (—) berulang, judul bagian bergaya ("Pendahuluan: Sebuah Awal Perjalanan"). Daftar bernomor hanya untuk isi yang memang berupa daftar paralel dan jenis esainya membolehkan (misalnya langkah implementasi di LKTI).
- **Periksa:**
  ```
  python tools/cek_docx.py "<L>/kirim/<nama file>.docx" --profil <L>
  ```
  Semua temuan KRITIS dan MAYOR harus beres. Setelah itu render PDF per halaman dan lihat setiap halamannya (skill `pdf`): halaman pertama, perpindahan halaman, posisi gambar dan tabel, dan daftar pustaka.

## Cek akhir (semua harus ✅)
- [ ] `python tools/cek_naskah.py <L>/draf/final.md --profil <L> --nama "<nama>" --nama "<sekolah>" --sumber <L>/riset/teks` tanpa masalah
- [ ] `python skills/esai/naskah-id/scripts/periksa.py <L>/draf/final.md` tanpa temuan K (kaidah) yang tersisa
- [ ] `python tools/cari_sumber.py cek-pustaka <L>/draf/final.md` sudah dicek, dan sisa ⚠️ diverifikasi manual
- [ ] `python tools/cek_klaim.py <L>/draf/final.md --peta <L>/riset/sumber.md` tanpa masalah, dan auditor sitasi putaran terakhir tidak memberi "tidak mendukung"
- [ ] Tidak ada penanda `[PERLU ...]` (build otomatis ditolak kalau masih ada)
- [ ] `python tools/cek_docx.py "<L>/kirim/<nama file>.docx" --profil <L>` tanpa temuan KRITIS/MAYOR, dan setiap halaman PDF sudah dilihat
- [ ] Buka DOCX dan PDF hasil build: halaman pertama, nomor halaman, lampiran di halaman baru, File → Info: kolom penulis kosong
- [ ] Struktur wajib lengkap; judul konsisten dengan isi
- [ ] Nama file persis sesuai aturan
- [ ] Lampiran administrasi (surat orisinalitas, kartu pelajar, dll.) siap
- [ ] Aturan AI dan orisinalitas sudah diputuskan (lihat `<L>/STATUS.md`)
- [ ] Kirim sebelum H-1 kalau lomba tidak mengizinkan kirim ulang

Kalau lomba punya babak presentasi, sebutkan sekali di checkpoint bahwa PPT bisa dibuat lewat tahap 7C kalau penulis meminta. Jangan mulai membuatnya sebelum diminta.
