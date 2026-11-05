# Panduan untuk agen/model lain: menulis draf esai lomba dan membuat Word-nya

> **Aturan berhenti berlaku untuk semua agen** (`CLAUDE.md` § Aturan berhenti): kerjakan setiap langkah persis seperti panduannya. Kalau tidak bisa, berhenti dan lapor dengan format `⛔ BERHENTI`, jangan mengganti dengan cara lain atau mengarang hasil. Antigravity: lihat juga `AGENTS.md` § 0.

Panduan umum untuk lomba esai apa pun di folder ini. `<L>` = folder lomba, misalnya `lomba/ewc-siswa-pharfest-2026`. Jalankan semua perintah dari folder akar proyek (`D:\Playground\new essay`). Sebelum mulai, baca `CLAUDE.md` di akar proyek dan `<L>/STATUS.md` untuk posisi kerja.

Catatan jujur: panduan ini soal mutu tulisan dan format. Panduan ini tidak mengubah aturan lomba. Kalau lomba atau surat orisinalitas melarang karya yang ditulis AI, aturan itu tetap berlaku dan harus dipatuhi.

---

## A. Menulis isi draf Markdown dari nol

### A0. Bahan wajib sebelum menulis
1. `<L>/aturan.md` dan `<L>/profil.json`: batas kata, gaya sitasi, aturan gambar/tabel, format kertas. Semuanya disalin dari guidebook di tahap 0.
2. `<L>/draf/kerangka.md` yang **sudah disetujui penulis**: tesis, pohon argumen, kontra-argumen, alokasi kata per bagian.
3. `<L>/riset/sumber.md` § Peta klaim: satu-satunya sumber angka dan fakta. Pakai hanya baris berstatus ✅.
4. `<L>/draf/rencana-visual.md`: gambar/tabel yang direncanakan dan posisinya.

Fakta yang tidak ada di peta klaim tidak boleh ditulis. Tulis `[PERLU DATA: ...]` lalu cari sumbernya (`workflow/02-riset.md`). Jangan mengisi angka dari ingatan.

### A1. Urutan menulis
1. Isi argumen (bagian dengan bukti terbanyak), lalu solusi, lalu keterbatasan/kontra-argumen.
2. Pendahuluan setelah isi jelas.
3. Penutup terakhir.
4. Hitung kata dengan `cek_naskah.py` tiap selesai satu bagian.

### A2. Kerangka Markdown
```
# Judul

## Pendahuluan
## <Argumen 1 sebagai frasa isi>
## <Argumen 2 sebagai frasa isi>
## <Argumen 3 / dampak>
## <Nama solusi>
## Keterbatasan
## Penutup
## Daftar Pustaka
## Lampiran            (kalau ada)
```
- Subjudul berupa frasa isi, misalnya "Perencanaan yang Hanya Melihat Obat Keluar", bukan label kosong seperti "Pembahasan". Juri bisa membaca argumen dari daftar subjudul saja.
- Kalau guidebook mewajibkan struktur atau subjudul tertentu, ikuti guidebook.

### A3. Aturan paragraf
- Satu paragraf = satu gagasan, 3–6 kalimat.
- Kalimat pertama langsung membawa isi (fakta, angka, atau klaim), bukan "Pada bagian ini akan dibahas...".
- Angka selalu dengan konteks: tahun, jumlah sampel, cakupan.
- Sitasi sesuai gaya lomba (misalnya APA: `(Penulis dkk., 2024)`) di akhir kalimat bersumber, lalu komentar ID klaim `<!--K1-->` (tidak tercetak).
- Jangan menutup paragraf dengan kalimat bijak atau ringkasan ulang.
- Variasikan panjang kalimat. Pecah kalimat di atas ±35 kata.

### A4. Pola yang terbaca seperti tulisan mesin (hapus)
Disusun dari temuan juri di loop review esai EWC Pharfest 2026.

| Hindari | Contoh | Tulis begini |
|---|---|---|
| Kontras "bukan X, melainkan Y" | "berasal dari penilaian petugas, bukan dari catatan permintaan" | nyatakan Y langsung |
| Kalimat meta | "Tesis esai ini:", "Esai ini berpendapat", "Bagian berikut membahas" | langsung nyatakan klaimnya |
| Penutup slogan | "Celah inilah yang diisi...", "Sistem yang berkelanjutan membutuhkan..." | kalimat berisi data atau langkah konkret |
| Penilaian diri | "Usulan ini sederhana", "Pembagian tugasnya tegas" | tunjukkan lewat isi |
| Pembuka retoris | "Bagaimana sebuah X bisa...?" | buka dengan fakta terkuat |
| Paksaan tiga | tiga butir padahal buktinya dua | sebut sebanyak yang ada |
| Frasa gaya | "melangkah lebih jauh", "di atas kertas", "yang jelas" | kata kerja biasa |
| Klaim absolut | "tidak ada mekanisme", "tidak dikerjakan siapa pun" | "sejauh penelusuran penulis, belum ada..." |
| Tebal di tengah prosa | "**58% dari 60 obat**" | tanpa tebal |
| Hedging berulang | "penulis menduga" berkali-kali | sekali di tempat yang paling perlu |
| Pembuka kosmik / penegas kosong | "Di era digital ini", "Tidak dapat dipungkiri" | hapus |
| Kalke Inggris | "memainkan peran", "di mana" sebagai penghubung | "berperan", "yang/tempat/saat" |

Dicek juga oleh mesin: `tools/frasa_slop.txt` (lewat `cek_naskah.py`) dan `skills/esai/naskah-id/references/pola-ai.md` (lewat `periksa.py`).

### A5. Kekuatan klaim = kekuatan bukti
Tangga: mungkin menunjukkan < berkaitan dengan < memprediksi < berkontribusi < memengaruhi < menyebabkan.
- Survei atau dugaan peneliti → "menduga", "dapat berasal dari", bukan "menyebabkan".
- Mekanisme yang belum diukur → tulis terang bahwa belum diukur.
- Angka asumsi → sebut asumsinya, lalu **hitung dengan benar**. Juri menangkap salah hitung.
- Usulan sendiri → tulis sebagai rancangan atau usulan, jangan diberi ID klaim seolah fakta dari sumber.

### A6. Membuat esai "bisa dibayangkan"
- Pelaku nyata (siapa melakukan apa), benda nyata (formulir, laporan, rapat), tempat nyata.
- Contoh konkret di lampiran, diberi label "ilustrasi, bukan data".
- Skenario angka (kecil dan besar) dan rencana uji coba dengan ukuran keberhasilan.
- Jawab keberatan terkuat di dalam esai sebelum juri sempat menanyakannya.
- Kalau ada bahan nyata dari penulis (wawancara, pengamatan), pakai dan sitasi. Jangan mengarangnya.

### A7. Markdown yang membuat Word terlihat profesional
- Daftar bernomor hanya untuk langkah berurutan. Bagian lain berupa prosa.
- Ikuti aturan lomba soal tabel/gambar. Kalau hanya boleh di lampiran, badan teks cukup merujuk: "Rancangannya ada di Lampiran 1."
- Lampiran: tiap blok diawali `**Lampiran N.** keterangan`, lalu `Tabel N. ...` tepat di atas tabel, dan `Catatan: ...` di bawahnya.
- Tabel ≤5 kolom dengan kepala kolom pendek.
- Gambar dari spesifikasi JSON (`tools/buat_visual.py`), bukan tangkapan layar. Keterangannya "Gambar N. ..." dan "Sumber: ...".
- Daftar pustaka sesuai gaya lomba, lengkap dengan DOI. Penulis yang sama diurutkan menurut tahun.

### A8. Setelah menulis
1. Jalankan cek di bagian B sampai bersih.
2. Build .docx, buka atau render ke PDF, lalu periksa tiap halaman (terutama lampiran).
3. Loop juri (`workflow/05-review.md`): juri rubrik resmi guidebook, devil's advocate, auditor sitasi, banding berpasangan, masing-masing di konteks terpisah.

---

## B. Membuat Word yang sama persis

Word dibuat oleh skrip Python di `tools/`, bukan oleh model. Agen mana pun menghasilkan file identik **asal menjalankan skrip yang sama**.

### B1. Aturan keras
1. JANGAN membuat skrip baru atau menulis ulang `tools/build_docx.py`. JANGAN mengatur format Word dengan tangan.
2. JANGAN mengubah `<L>/profil.json` kecuali sedang mengerjakan tahap 0 (menyalin aturan guidebook).
3. Ubah isi hanya di `<L>/draf/draf-vN.md`, lalu build ulang.
4. Pertahankan komentar `<!--Kn-->`.
5. Versi baru = file baru (`draf-vN+1.md`). Setiap versi dibuat .md **dan** .docx.

### B2. Persiapan (sekali)
```
pip install python-docx matplotlib
```

### B3. Build setiap versi
```
python tools/buat_visual.py <L>/visual/*.json --profil <L>
python tools/build_docx.py <L>/draf/draf-vN.md --profil <L> --out <L>/draf/draf-vN.docx
```
Di Windows, kalau `*.json` tidak dikenali, sebutkan file JSON satu per satu. Gambar tersimpan di `<L>/draf/gambar/` dan dirujuk dari Markdown sebagai `gambar/<nama>.png`, jadi file .md harus berada di `<L>/draf/`.

### B4. Cek wajib
```
python tools/cek_naskah.py <L>/draf/draf-vN.md --profil <L> --sumber <L>/riset/teks
python tools/cek_klaim.py <L>/draf/draf-vN.md --peta <L>/riset/sumber.md
python skills/esai/naskah-id/scripts/periksa.py <L>/draf/draf-vN.md
python tools/cek_docx.py <L>/draf/draf-vN.docx --profil <L>
```
Kriteria lulus:
- `cek_naskah.py`: jumlah kata dalam batas profil dan "Tidak ada masalah terdeteksi".
- `cek_klaim.py`: semua ID berstatus ✅. Kalau masih ada ⚠️, catat di STATUS.
- `periksa.py`: tidak ada temuan berlabel K. Temuan G dibaca sesuai konteks.
- `cek_docx.py`: "✅ Format bersih".

### B5. Sintaks Markdown yang dikenali `build_docx.py`
Hanya tanda ini yang didukung. Tanda lain tercetak apa adanya.
- `# Judul` (sekali, baris pertama) · `## Subjudul` · `### Sub-subjudul`
- paragraf dipisah satu baris kosong · `**tebal**`, `*miring*` · daftar `1. ...` / `- ...`
- `## Daftar Pustaka`: satu entri per paragraf, dengan indentasi gantung
- `## Lampiran`: mulai halaman baru; tiap blok `**Lampiran N.**` juga mulai di halaman baru
- tabel: `Tabel N. keterangan` tepat di atasnya, tabel pipa `| a | b |` dengan `|---|---|`; garis turus ditulis `\|`; lebar kolom diatur otomatis
- `Catatan: ...` di bawah tabel = catatan tabel berhuruf kecil
- gambar: `![Gambar N. keterangan](gambar/nama.png)` lalu `*Sumber: ...*`
- `<!-- ... -->` tidak dicetak
- Build ditolak kalau masih ada `[PERLU ...]`, `TODO`, `XXX`, atau `??`.

### B6. PDF
Buka .docx di **Microsoft Word**, lalu File > Save As > PDF, supaya font tetap asli. Beri nama file sesuai format penamaan di guidebook (lihat `<L>/aturan.md`).

### B7. Kalau hasil berbeda
- Pastikan `tools/build_docx.py` versi 30 Okt 2026 atau lebih baru.
- Jalankan dari folder akar proyek.
- Pastikan `<L>/profil.json` sudah diisi dari guidebook lomba yang bersangkutan.
