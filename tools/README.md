# Alat

Jalankan dari folder utama workflow (folder yang berisi `CLAUDE.md`). Butuh Python 3.8+. Cara memasang Python dan menjalankan perintah di Windows: [`MULAI-DI-WINDOWS.md`](../MULAI-DI-WINDOWS.md).

```
pip install python-docx        # build_docx.py
pip install pypdf              # baca_pdf.py (atau pdfplumber)
pip install docx2pdf           # opsional: PDF lewat MS Word kalau tidak ada LibreOffice
pip install matplotlib         # buat_visual.py (grafik & diagram)
pip install python-pptx        # cek_pptx.py (hanya kalau membuat PPT, tahap 7C)
```
Alat lain (`cari_sumber.py`, `cek_naskah.py`, `cek_klaim.py`, `arena.py`, `evaluasi.py`, `tes_alat.py`) hanya memakai pustaka standar Python.

Semua alat memaksa keluaran UTF-8, jadi aman dijalankan dari PowerShell atau oleh Claude (keluaran yang di-pipe). Kalau internet mati, alat yang butuh API berhenti dengan satu baris pesan, bukan traceback.

## tes_alat.py — tes otomatis
```
python tools/tes_alat.py              # semua tes tanpa internet
python tools/tes_alat.py -v
```
Untuk ikut menguji API sungguhan (Crossref, DataCite, OpenAlex), set dulu `ESAI_TES_JARINGAN=1` (PowerShell: `$env:ESAI_TES_JARINGAN="1"`). Jalankan tes ini setiap kali alat diubah.

## buat_visual.py — grafik & diagram untuk esai
```
python tools/buat_visual.py lomba/<nama>/visual/*.json --profil lomba/<nama>
```
Satu file JSON per visual (contoh di `workflow/03b-rencana-visual.md`). Jenis: `batang`, `batang_h`, `garis`, `alur`, `siklus`. Hasil PNG 300 DPI di `<L>/draf/gambar/`, dengan font naskah dari profil, satu warna aksen (`warna_aksen` di profil) + abu-abu, tanpa judul di dalam gambar (judul ada di keterangan Word). Grafik data tanpa `"sumber"` diberi peringatan.

Setelah menggambar, alat memeriksa tata letak dan mencetak `⚠️ PERIKSA` untuk: teks yang bertumpuk (pasangan pertama disebut, sisanya diringkas dengan saran memakai `batang_h` untuk label panjang), teks yang keluar dari kotak diagram, dan huruf yang saat dicetak di Word lebih kecil dari 8 pt. Ukuran cetak dihitung dari `lebar_gambar_cm` dan `tinggi_gambar_maks_cm` di profil, sama seperti `build_docx.py`, jadi diagram kecil yang diperbesar saat dicetak tidak dianggap bermasalah. Temuan dipakai di putaran umpan balik visual (`workflow/03b-rencana-visual.md` § 8); melihat PNG-nya tetap wajib.

## cek_docx.py — cek tampilan file Word
```
python tools/cek_docx.py "lomba/<nama>/kirim/<nama file>.docx" --profil lomba/<nama>
```
Melapor KRITIS/MAYOR/MINOR/INFO: font atau ukuran di luar profil (termasuk tabel), teks berwarna/stabilo/bergaris bawah, emoji, huruf tebal di badan teks > 3%, tanda pisah panjang berulang, paragraf kosong berturut-turut, huruf kapital semua, gambar tanpa "Gambar N.", tabel tanpa "Tabel N." di atasnya, keterangan gambar tanpa sumber, nomor tidak urut, gambar di badan teks padahal profil melarang, dan metadata yang terisi. Keluar dengan kode 1 kalau ada KRITIS/MAYOR.

## cek_pptx.py — cek slide & baca gaya PPT contoh
```
python tools/cek_pptx.py cek  "lomba/<nama>/presentasi/slide.pptx" --durasi 7 --maks-slide 10
python tools/cek_pptx.py gaya "lomba/<nama>/presentasi/contoh/contoh.pptx" --out lomba/<nama>/presentasi/gaya-contoh.md
```
`cek` melapor KRITIS/MAYOR/MINOR/INFO: emoji, gradasi (KRITIS kalau bernada ungu), glow, bayangan berlebihan, lebih dari 2 keluarga huruf, huruf isi < 18 pt (baris "Sumber:" boleh 12 pt), > 35/50 kata atau > 4 butir per slide, kapital semua yang panjang, judul berupa label, slide tanpa judul, warna ungu/violet, terlalu banyak warna aksen, jumlah slide melebihi batas atau terlalu banyak untuk durasi, dan slide tanpa catatan pembicara. Ukuran huruf yang hanya diwarisi dari master tidak terbaca, jadi tetap lihat gambar slidenya. `gaya` meringkas ukuran slide, font tema dan yang dipakai, warna, ukuran huruf, kata per slide, tata letak, gambar, dan gradasi.

## baca_pdf.py — teks guidebook per halaman
```
python tools/baca_pdf.py lomba/<nama>/guidebook.pdf --out lomba/<nama>/guidebook.txt
```
Hasilnya dipisah `=== Halaman N ===` supaya setiap aturan bisa dikutip dengan nomor halaman. Halaman yang hampir tanpa teks (poster, scan) diberi peringatan dan harus dibaca sebagai gambar.

## cari_sumber.py — cari & verifikasi jurnal
```
python tools/cari_sumber.py cari "kata kunci bahasa inggris" --dari 2019
python tools/cari_sumber.py cari "..." --db pubmed,europepmc --n 5 --simpan lomba/<nama>/riset/sumber.md
python tools/cari_sumber.py cari "..." --db semua --oa
python tools/cari_sumber.py doi 10.1016/j.scitotenv.2020.140111
python tools/cari_sumber.py teks 10.1371/journal.pmed.0020124 --simpan-teks lomba/<nama>/riset/teks
python tools/cari_sumber.py cari "bank sampah desa" --db garuda --n 10
python tools/cari_sumber.py teks "https://jurnal.ac.id/article/download/539/787" --simpan-teks lomba/<nama>/riset/teks --nama syafruddin-2019
python tools/cari_sumber.py cek-pustaka lomba/<nama>/draf/draf-v1.md
python tools/cari_sumber.py fda "amoxicillin"
python tools/cari_sumber.py uji-klinis "antibiotic stewardship"
```
Database: OpenAlex (paling luas, termasuk status retraksi), arXiv (preprint), PubMed & Europe PMC (biomedis/farmasi), Semantic Scholar, Crossref (verifikasi DOI dan format APA), DataCite (DOI arXiv/Zenodo/repositori yang tidak ada di Crossref), openFDA (recall & label obat AS), ClinicalTrials.gov.

Yang dicek `cek-pustaka` untuk setiap entri di `## Daftar Pustaka` (satu entri per baris atau per butir `-`; baris berawalan spasi dianggap lanjutan entri sebelumnya):
- DOI ada di Crossref atau DataCite. DOI berkurung seperti `10.1016/S0140-6736(97)11096-0` dibaca utuh.
- Judul, **penulis pertama, dan tahun** di metadata DOI cocok dengan entri (tahun boleh selisih 1). Nama jurnal yang tidak cocok dilaporkan sebagai info, karena entri sering memakai singkatan.
- Status retraksi dari Crossref (`updated-by`/`update-to`) dan OpenAlex. Kalau OpenAlex gagal dihubungi, entri ditandai **❓ status retraksi TIDAK TERCEK** dan dihitung sebagai masalah, bukan dianggap aman.
- Entri tanpa DOI (dokumen lembaga `.go.id`, BPS, WHO, peraturan) dihitung dan didaftar di akhir sebagai **cek manual**.
- Format APA entri tidak dicek. Perintah `doi` mencetak format APA 7 dari metadata untuk disalin.

Set email supaya tidak cepat dibatasi: `--email kamu@mail.com`, atau di PowerShell `$env:ESAI_EMAIL="kamu@mail.com"`.
OpenAlex: kunci gratis dari https://openalex.org/settings/api. Di Windows: `setx OPENALEX_API_KEY "<kunci>"`, lalu buka terminal baru. Kode mengirimnya sebagai parameter `api_key`.
Semantic Scholar: kunci gratis lewat https://www.semanticscholar.org/product/api, lalu `setx SEMANTIC_SCHOLAR_API_KEY "<kunci>"`. Kode mengirimnya sebagai header `x-api-key`, hanya ke api.semanticscholar.org.

Perintah `teks` (teks penuh akses terbuka): mencari lokasi legal sebuah DOI di OpenAlex (yang memuat data Unpaywall), di Unpaywall langsung kalau `ESAI_EMAIL` diisi, dan di Europe PMC. Urutannya versi terbit, naskah diterima, lalu preprint. Dengan `--simpan-teks <folder>`, teks diambil dari XML Europe PMC kalau ada (paling bersih), kalau tidak dari PDF (butuh `pypdf`, ligatur dinormalkan, penanda `=== Halaman N ===`). Nama file `<nama-belakang>-<tahun>.md` dan tidak pernah menimpa file lama. Teks hasil ekstraksi mesin tetap dicocokkan dengan aslinya sebelum ✅.

Batasan: kata kunci satu bahasa, jadi pakai bahasa Inggris untuk hasil internasional dan bahasa Indonesia untuk `--db garuda`. Garuda tidak punya API resmi: `--db garuda` membaca halaman pencarian publiknya (10 hasil per halaman, paling banyak 3 halaman, jeda 1 detik). Kalau tampilan situs Garuda berubah, alat melaporkan "tidak ada hasil", bukan hasil yang salah; tes jaringan `TesJaringan.test_garuda` akan gagal sebagai tanda. SINTA dan Google Scholar tidak dicari otomatis.

## cek_naskah.py — cek kepatuhan
```
python tools/cek_naskah.py lomba/<nama>/draf/final.md --profil lomba/<nama> --nama "Nama Kamu" --nama "Nama Sekolah" --sumber lomba/<nama>/riset/teks
```
- Penanda belum beres: semua bentuk `[PERLU ...]` (`[PERLU SUMBER]`, `[PERLU DATA: ...]`, `[PERLU RUJUKAN: ...]`), `TODO`, `XXX`, `??`.
- `--nama` dan frasa klise dicocokkan per kata utuh, jadi "Ani" tidak menandai "organik", dan "sinergi" tidak menandai "sinergis".
- Sitasi dicocokkan dengan pustaka: `(Smith, 2020)`, `(Smith, 2020, 2021)`, `(Smith dkk., 2020)`, `(Smith & Lee, 2019)`, `Santoso dan Wibowo (2021)`, `(Park et al., 2019)`, sitasi bernomor `[1]`, dan singkatan lembaga. Agar `(WHO, 2021)` cocok, tulis entri pustakanya `World Health Organization [WHO]. (2021). ...`. `(Maret 2024)` dan `(Rp 1500)` tidak dianggap sitasi.
- `--sumber` (boleh diulang) membandingkan isi naskah dengan file `.md`/`.txt` teks sumber dan melaporkan rangkaian ≥8 kata yang sama persis. Kalau diberi `<L>/riset`, yang dipakai otomatis `<L>/riset/teks`. `dossier.md`, `sumber.md`, dan `README.md` selalu dilewati karena itu tulisan sendiri. Ini pengganti sederhana cek plagiarisme: hanya terhadap sumber yang kamu simpan, dan tidak menangkap terjemahan.

## cek_klaim.py — angka dan ID klaim vs peta klaim
```
python tools/cek_klaim.py lomba/<nama>/draf/draf-v1.md --peta lomba/<nama>/riset/sumber.md
```
Melaporkan angka di naskah (persen, rupiah, desimal, ribuan, tahun data) yang tidak ada di peta klaim, ID klaim `<!--K3-->` yang tidak ada di peta, dan ID yang statusnya belum ✅. Lihat `workflow/02-riset.md` § Peta klaim.

## evaluasi.py — tahap 8 (evaluasi pasca-lomba)
```
python tools/evaluasi.py juri lomba/<nama>
python tools/evaluasi.py rekap
```
- `juri` membaca `<L>/ide/juri/*.json` (file kesan dan adu otomatis dilewati), mengelompokkan per `loop-N` dan `final`, lalu melaporkan korelasi Spearman antarjuri (nilai kembar dirata-rata), pasangan juri yang paling tidak sepakat, persentase gugur gerbang, persentil kartu jangkar (ID berawalan `X`), dan apakah peringkat 1 panel final sama dengan juara di `adu-final.json`. Keluarannya Markdown yang tinggal ditempel ke `<L>/evaluasi.md`.
- `rekap` menggabungkan semua `lomba/*/hasil.json` (folder `_template` dan `contoh*` dilewati): tabel per lomba, sebaran hasil, rata-rata persentil jangkar, tingkat setuju uji balik, daftar lomba yang belum menjalankan 8a/8b, dan peringatan kalau hasil yang diketahui masih < 3 lomba (belum cukup untuk mengubah hipotesis strategi).

## arena.py — hitungan Arena Ide
```
python tools/arena.py acak --seed 20261029 I01 I02 I03 ...
python tools/arena.py rekap lomba/<nama>/ide/juri/loop-1-*.json
python tools/arena.py mirip lomba/<nama>/ide/loop-1.md lomba/<nama>/ide/loop-2.md lomba/<nama>/ide/loop-3.md
python tools/arena.py rekap lomba/<nama>/ide/juri/loop-*.json --top 7 --kesan <kesan-loop-1.json> --kecuali X01,I07
python tools/arena.py adu lomba/<nama>/ide/adu-final.json
```
Pengacakan dengan seed tetap, median skor, gugur gerbang, dan poin adu berpasangan dihitung skrip dari JSON juri, bukan oleh model. Format JSON ada di docstring alat dan di `templates/prompt-ide-juri.md`.

- `mirip` menandai pasangan kartu yang kata-katanya mirip (kemiripan Jaccard ≥ 0,18, kata umum dibuang; baris `Lensa` dan `Kenapa tidak pasaran` diabaikan). Ambang ini dikalibrasi pada lomba lama. Hasilnya calon duplikat, dan agen utama yang memutuskan.
- `rekap --top N` menandai N finalis dan maksimal 2 **kartu liar**: ide di luar N teratas yang menjadi nilai tertinggi seorang juri, dipilih `bela`, atau mendapat "berhenti" di file `--kesan`. Kolom `Maks`, `Sebaran`, `#1 juri`, dan `Bela` menunjukkan ide yang memecah pendapat juri.
- `rekap` mencetak `SERI DI PUNCAK` kalau ide-ide teratas terpaut ≤ 0,5 (`--seri`). `adu` mencetak `SERI/TIPIS` kalau selisih poin dua teratas ≤ 0,5.
- `--kecuali` mengeluarkan kartu jangkar (`X01`) dan duplikat dari peringkat.

## naskah-id/periksa.py — kaidah bahasa Indonesia
```
python skills/esai/naskah-id/scripts/periksa.py lomba/<nama>/draf/final.md
python skills/esai/naskah-id/scripts/periksa.py --banding lomba/<nama>/draf/draf-v1.md lomba/<nama>/draf/draf-v2.md
python skills/esai/naskah-id/scripts/periksa.py --tes
```
Dari repo nothinx/naskah-id (MIT). Menyaring pola kaidah EYD V/KBBI dan klise mesin. `--banding` melaporkan angka, sitasi, dan kutipan yang berubah antar versi.

## build_docx.py — Markdown → DOCX/PDF sesuai format lomba
```
python tools/build_docx.py lomba/<nama>/draf/final.md --profil lomba/<nama> --out "lomba/<nama>/kirim/naskah.docx" --pdf
```
- Profil format ada di `lomba/<nama>/profil.json` (dibuat dari `lomba/_template/profil.json` di tahap 0). Nilai `null` berarti "tidak diatur lomba" dan diganti default.
- Kertas: `A4`, `F4`/`Folio` (21,5 × 33 cm), `Letter`, `Legal`. Nomor halaman: `kanan_bawah`, `tengah_bawah`, `kiri_bawah`, `kanan_atas`, `tengah_atas`, `kiri_atas`, atau `null`.
- Didukung: `#`, `##`, `###`, paragraf, `**tebal**`/`*miring*`, daftar `-`/`1.`, tabel (baris `|---|:-:|` diabaikan), gambar beserta baris keterangan di bawahnya, Daftar Pustaka satu entri per baris dengan hanging indent, dan Lampiran di halaman baru.
- Build **ditolak** kalau masih ada penanda `[PERLU ...]`/`TODO`/`XXX`/`??`. Pakai `--paksa` hanya untuk draf uji.
- Metadata DOCX (penulis, terakhir diubah oleh) dikosongkan. Kalau file dibuka lalu disimpan ulang di Word, Word bisa mengisinya lagi. Cek di File → Info → Inspect Document.
- PDF: LibreOffice dicari di PATH dan di `C:\Program Files\LibreOffice`. Kalau tidak ada, dipakai MS Word lewat `docx2pdf`.

## Status pengujian (29 Okt 2026)
- `tes_alat.py`: 43 tes (2 tes `cek_pptx.py` ditambahkan untuk tahap 7C; 4 tes baru untuk tampilan `build_docx.py`, `cek_docx.py`, dan `buat_visual.py`, ditambahkan 29 Okt 2026 dan diuji di Linux dengan python-docx + matplotlib 3.11). Yang offline lulus di Windows (Python 3.12, python-docx 1.2.0) untuk 37 tes awal. Tes jaringan (Crossref, DataCite arXiv, retraksi Wakefield) juga lulus.
- `skills/esai/naskah-id/scripts/periksa.py --tes` lulus 108/108.
- `cari_sumber.py` diuji ke API sungguhan (28 Okt 2026): arXiv, PubMed, Europe PMC, Crossref + APA, openFDA, dan ClinicalTrials.gov berjalan. OpenAlex dan Semantic Scholar kadang menolak dengan 429 kalau tanpa kunci.
