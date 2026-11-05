# Cara draf Markdown dan Word dibuat (30 Okt 2026)

Ringkasnya: naskah ditulis sebagai **Markdown** (teks biasa dengan tanda sederhana), lalu diubah menjadi **Word** oleh skrip Python `tools/build_docx.py` yang membaca aturan format dari `lomba/<nama>/profil.json`. Gambar dibuat oleh `tools/buat_visual.py`. Setiap langkah dicek mesin sebelum dan sesudah.

## 1. Menulis naskah Markdown (`draf/draf-vN.md`)

Tanda yang dipakai:

| Di Markdown | Jadi apa di Word |
|---|---|
| `# Judul` | judul esai (14 pt, tebal, rata tengah) |
| `## Pendahuluan` | subjudul bagian (gaya Heading 1, tebal) |
| paragraf biasa | paragraf rata kiri-kanan, menjorok 1 cm di baris pertama |
| `**tebal**`, `*miring*` | tebal / miring |
| `1. ...` | daftar bernomor |
| `## Daftar Pustaka` | setiap baris jadi entri APA dengan indentasi gantung (hanging indent 1,27 cm) |
| `## Lampiran` | pindah ke halaman baru; setiap `**Lampiran N.**` berikutnya juga di halaman baru |
| `Tabel 1. ...` lalu `\| a \| b \|` | keterangan tabel kecil di atas, tabel gaya tiga garis |
| `Catatan: ...` | catatan tabel, huruf lebih kecil |
| `![Gambar 1. ...](gambar/x.png)` | gambar selebar 14 cm + keterangan di bawahnya |
| `<!--K3-->` | **tidak dicetak**; ini ID klaim yang menghubungkan kalimat ke sumbernya |

Komentar `<!--Kn-->` adalah kunci keamanan data: setiap angka atau fakta di naskah menunjuk satu baris di `riset/sumber.md` (peta klaim) yang berisi kutipan asli sumber. Juri tidak melihat komentar ini, tetapi alat cek dan auditor sitasi memakainya.

## 2. Aturan format dari guidebook (`profil.json`)

Tahap 0 menyalin aturan guidebook hlm 10 ke file ini: A4, Times New Roman 12, spasi 1,5, margin kiri 4 / kanan 3 / atas 3 / bawah 3 cm, rata kiri-kanan, judul 14 pt, nomor halaman kanan bawah, gambar hanya di lampiran, 1.000–1.500 kata. Skrip build membaca angka-angka ini, jadi format tidak diatur tangan.

## 3. Membangun Word (`tools/build_docx.py`)

Perintah:
```
python tools/build_docx.py lomba/<L>/draf/draf-v6.md --profil lomba/<L> --out lomba/<L>/draf/draf-v6.docx
```
Yang dilakukan skrip (pakai pustaka Python `python-docx`):
1. Membuat dokumen kosong, mengatur ukuran kertas, margin, font dasar, spasi, dan nomor halaman (field PAGE di footer kanan).
2. Membaca Markdown per blok (dipisah baris kosong) dan memutuskan jenisnya: judul, subjudul, paragraf, daftar, tabel, gambar, keterangan, pustaka, atau lampiran.
3. Untuk judul bagian dipakai gaya **Heading** bawaan Word (hitam, font naskah), dengan "keep with next" supaya judul tidak tertinggal sendirian di bawah halaman.
4. **Tabel** dibuat bergaya tiga garis (garis atas, di bawah kepala tabel, dan bawah; tanpa garis tegak), seperti tabel di jurnal. Sejak 30 Okt: lebar kolom dihitung dari panjang isi (kata terpanjang dan teks terpanjang tiap kolom), tata letak dikunci "fixed" supaya Word dan LibreOffice menghormatinya, angka dan "ya/tidak" ditengahkan, dan ada jarak kecil sesudah tabel. Tanda `\|` dicetak sebagai garis turus.
5. **Gambar** disisipkan dengan lebar seragam dari profil (14 cm, tinggi maksimal 10 cm), lalu keterangan "Gambar N." dan "Sumber:" dengan huruf lebih kecil.
6. **Daftar pustaka**: tiap entri jadi paragraf dengan indentasi gantung, rata kiri.
7. Metadata file (penulis, terakhir diubah oleh) **dikosongkan** supaya identitas tidak bocor ke juri.
8. Build ditolak kalau masih ada penanda belum beres seperti `[PERLU DATA: ...]`, `TODO`, atau `??`.

## 4. Membuat gambar (`tools/buat_visual.py`)

Gambar ditulis sebagai spesifikasi JSON di `visual/` (misalnya `lingkaran-nol.json`: jenis "siklus", lima langkah, satu langkah utama berwarna, teks di tengah). Skrip memakai `matplotlib` untuk menggambar kotak dan panah dengan font naskah, abu-abu dan satu warna aksen (#1f5a8a, tetap terbaca kalau dicetak hitam-putih), tanpa judul di dalam gambar (judul ada di keterangan Word), lalu menyimpan PNG 300 DPI ke `draf/gambar/`. Sejak 30 Okt, gambar dirender saat draf dibuat, jadi setiap .docx sudah lengkap.

## 5. Pengecekan otomatis setiap versi

| Alat | Yang dicek |
|---|---|
| `tools/cek_naskah.py` | jumlah kata isi (tanpa judul, pustaka, lampiran) vs batas; sitasi di teks ↔ entri pustaka; frasa klise AI; tabel/gambar di luar lampiran; kalimat terlalu panjang; kemiripan ≥8 kata berturut-turut dengan teks sumber |
| `tools/cek_klaim.py` | setiap `<!--Kn-->` ada di peta klaim dan berstatus ✅ |
| `skills/naskah-id/scripts/periksa.py` | EYD V (mis. koma sebelum "sehingga"), singkatan belum dijelaskan, kalimat >35 kata, pola AI bahasa Indonesia |
| `tools/cek_docx.py` | membuka .docx hasil build dan mencocokkan kertas, margin, font, spasi, rata, keterangan tabel dengan profil |
| render PDF (LibreOffice) | dilihat sebagai gambar untuk memeriksa tampilan lampiran |

## 6. Kenapa hasilnya rapi

- Format tidak pernah diatur tangan; semuanya dari satu sumber aturan (`profil.json`), jadi konsisten di setiap versi.
- Gaya meniru naskah terbitan: tabel tiga garis, keterangan kecil, heading bawaan Word, kontrol baris janda/yatim.
- Markdown tetap teks biasa, jadi mudah dibandingkan antarversi dan dibaca juri AI tanpa gangguan format.

## 7. Mengulang di komputer sendiri

```
pip install python-docx matplotlib
python tools/buat_visual.py lomba/<L>/visual/*.json --profil lomba/<L>
python tools/build_docx.py lomba/<L>/draf/draf-vN.md --profil lomba/<L> --out lomba/<L>/draf/draf-vN.docx
python tools/cek_docx.py lomba/<L>/draf/draf-vN.docx --profil lomba/<L>
```
PDF terbaik dibuat dengan membuka .docx di Microsoft Word lalu Save As PDF (font Times New Roman asli).
