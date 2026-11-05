# Tahap 4 — Menulis Draf

Sumber: `skills/esai/academic-research-skills/writing_quality_check.md`, `writing_judgment_framework.md`, dan **`skills/esai/naskah-id/`** untuk bahasa Indonesia baku (EYD V, KBBI, kalimat efektif, pola AI). Skill akun penulisan tidak dipakai (lihat `CLAUDE.md` § Pemakaian skill).

Dari `naskah-id`, yang dipakai: `references/ejaan-eyd-v.md`, `kata-baku.md`, `kalimat-efektif.md`, `pola-ai.md`, `istilah.md`, `singkatan.md`. Baca juga `references/pertahankan.md` supaya tidak mengoreksi berlebihan (misalnya pasif yang sah, hedging yang memang perlu).

## Siapa yang menulis
**Claude menulis seluruh draf** dari kerangka yang sudah disetujui. Penulis membaca dan memberi arahan ("lebih tajam di argumen 2", "nada lebih formal"), lalu Claude merevisi. Kalau lomba meminta log prompt, simpan di `<L>/STATUS.md`.

## Fakta hanya dari peta klaim
- Setiap angka, temuan, dan kutipan di draf diambil dari tabel **Peta klaim** di `<L>/riset/sumber.md`, dan hanya dari baris berstatus ✅. Klaim ⚠️ belum boleh dikutip sebagai fakta.
- Setelah kalimat yang memakai klaim, tulis ID-nya sebagai komentar HTML: `... naik menjadi 21,6% (Kemenkes, 2023). <!--K3-->`. Lebih dari satu: `<!--K3, K4-->`. Komentar tidak tercetak di DOCX dan tidak dihitung sebagai kata.
- Kekuatan kalimat tidak boleh melebihi kolom "Kekuatan" dan kutipan di peta klaim (tangga klaim di `workflow/05-review.md`).
- Butuh fakta yang belum ada di peta? Tulis `[PERLU DATA: ...]`, lalu selesaikan lewat prosedur di `workflow/02-riset.md`. Jangan mengisi angka dari ingatan.

## Contoh gaya (sebelum menulis)
Satu contoh tulisan manusia di prompt sangat menaikkan ketepatan gaya hasil tulisan model, sedangkan lebih dari dua contoh hampir tidak menambah (arXiv 2509.14543, 2025). Tujuannya tulisan yang enak dibaca juri, bukan mengakali detektor AI (itu dilarang).

1. Pilih **1–2 cuplikan ±150–250 kata** dari tulisan Indonesia berkualitas yang **gayanya** cocok dengan jenis esai lomba. Pilih karena gayanya, bukan karena topiknya sama: contoh bertopik sama justru menurunkan ketepatan gaya dan berisiko ikut tersalin isinya. Sumber yang dianjurkan:
   - esai juara lomba sebidang dan sejenjang yang teksnya tersedia (`catatan/bank-juara.md`);
   - The Conversation Indonesia (lisensi CC BY-ND), atau opini media nasional kredibel.
2. Simpan di `<L>/draf/teladan-gaya.md`: cuplikan, link, penulis, tanggal, lalu **3–5 ciri gaya** yang akan ditiru, misalnya cara membuka paragraf, panjang kalimat yang bervariasi, cara memasukkan angka, tingkat formal, dan cara menutup paragraf tanpa kalimat bijak.
3. Tulis draf mengikuti **ciri gaya** itu, bukan meniru kalimat atau isinya. Cuplikan tidak pernah masuk naskah.
4. **Cek tiru:** salin cuplikan juga ke `<L>/riset/teks/teladan-1.md` (dan seterusnya) dengan baris pertama `Sumber: <link> · diakses <tanggal> · bagian: teladan gaya, BUKAN sumber klaim`. Dengan begitu `cek_naskah.py --sumber` menangkap rangkaian ≥8 kata yang tersalin. Peta klaim tidak boleh mengutip file teladan.

## Urutan menulis
1. Isi/argumen dulu (bagian paling berat dan paling banyak bukti).
2. Solusi.
3. Pendahuluan (lebih mudah setelah isi jelas).
4. Penutup: tegaskan tesis dengan cara baru, implikasi, ajakan. Jangan sekadar ringkasan ulang.
5. Judul final.

## Anti-slop: pola yang harus dihindari

### Frasa pembuka kosong (Bahasa Indonesia)
| Hindari | Gantinya |
|---------|----------|
| "Di era globalisasi/digital saat ini..." | Mulai langsung dengan fakta atau kasus |
| "Tidak dapat dipungkiri bahwa..." | Hapus, langsung nyatakan |
| "Perlu diketahui bahwa..." / "Penting untuk dicatat bahwa..." | Hapus |
| "Dalam rangka..." | "Untuk..." |
| "Seiring dengan perkembangan zaman..." | Sebut perkembangan yang spesifik |
| "Hal ini menjadi bukti nyata bahwa..." | "Ini menunjukkan..." atau langsung data |
| "Bagaikan pisau bermata dua" | Jelaskan dua dampaknya secara konkret |
| "Sudah menjadi rahasia umum..." | Kalau umum, beri sumbernya |
| "Bab ini akan membahas..." | Langsung bahas |

### Kata yang sering dipakai berlebihan
`krusial, signifikan (tanpa angka), holistik, komprehensif, sinergi, optimal, inovatif, transformatif, multidimensi, esensial, fundamental, menggali lebih dalam, lanskap, ekosistem (di luar arti harfiah)`. Tidak dilarang, tapi tanya: apakah ini kata paling tepat?

### Pola struktur
- **Paksaan tiga:** setiap daftar selalu 3 butir. Pakai sebanyak yang didukung bukti.
- **Struktur cermin:** setiap paragraf persis berpola kalimat topik → 3 bukti → simpulan. Variasikan sesuai isi.
- **Kontras biner berulang:** "bukan sekadar X, melainkan Y" di setiap bagian.
- **Ganti-ganti istilah:** pakai istilah yang konsisten untuk konsep yang sama.
- **Tanda pisah (—) dan titik koma berlebihan.**
- **Kalimat penutup bijak** di setiap paragraf ("Pada akhirnya, semua kembali pada kita.").
- **Klaim menggelembung:** "revolusioner", "satu-satunya solusi", tanpa bukti.

### Yang membuat tulisan terasa manusia
- Detail konkret: nama tempat, angka, tahun, kasus nyata
- Kasus nyata yang terverifikasi dari sumber (nama program, daerah, tahun)
- Kalimat yang panjangnya bervariasi mengikuti makna
- Pendapat yang berani tapi dibatasi dengan jujur

## Bahasa
- Ikuti EYD V / KBBI untuk Bahasa Indonesia (huruf kapital, kata depan "di" dipisah, istilah asing dimiringkan).
- Satu paragraf = satu gagasan.

## Sesuaikan dengan jenis esai
- **Ilmiah populer**: mekanisme dan data dijelaskan dengan bahasa awam yang tetap akurat. Istilah teknis dijelaskan saat pertama muncul. Tidak perlu rumus.
- **Ilmiah/LKTI**: boleh lebih teknis, dengan metode dan perhitungan, tapi tetap hanya kalau didukung data nyata.
- **Opini/argumentatif**: satu posisi tegas, kontra-argumen dijawab, data secukupnya untuk menopang posisi.
- **Reflektif/naratif**: kalau lomba mewajibkan pengalaman pribadi, tanyakan ke penulis. Pengalaman tidak boleh dikarang.

## Visual dibuat di tahap ini
Semua visual esai (grafik, diagram, tabel, ilustrasi, baik di badan teks maupun lampiran) dibuat dan dirender **di tahap 4, bersama draf v1**, bukan di tahap 6 atau 7 (permintaan penulis, 30 Okt 2026). Ilustrasi yang tidak bisa dibuat `buat_visual.py` digambar dengan skrip sendiri bergaya sama (font naskah, satu warna aksen + abu-abu, tanpa gradasi), lalu diberi label "ilustrasi". Setelah render, jalankan **putaran umpan balik visual** di `workflow/03b-rencana-visual.md` § 8: baca temuan `PERIKSA` dari `buat_visual.py`, lihat setiap PNG, cocokkan dengan daftar lantai visual, perbaiki, ulangi paling banyak 3 putaran. Jangan menyalin gambar dari jurnal; gambar ulang sendiri dan tulis "diadaptasi dari ..." bila mengikuti figur sumber.

## Checkpoint
Kalau `draf/rencana-visual.md` memuat gambar, render sekarang (jangan tunggu tahap 6) supaya setiap versi DOCX sudah lengkap: `python tools/buat_visual.py <L>/visual/*.json --profil <L>` (PNG ke `<L>/draf/gambar/`), lalu rujuk dengan `![Gambar N. ...](gambar/<nama>.png)`. Setiap versi draf juga di-build ke DOCX: `python tools/build_docx.py <L>/draf/draf-vN.md --profil <L> --out <L>/draf/draf-vN.docx`.

Simpan sebagai `<L>/draf/draf-v1.md`, lalu jalankan dan perbaiki temuannya sebelum masuk loop juri:
```
python tools/cek_naskah.py <L>/draf/draf-v1.md --profil <L> --sumber <L>/riset/teks
python tools/cek_klaim.py <L>/draf/draf-v1.md --peta <L>/riset/sumber.md
python skills/esai/naskah-id/scripts/periksa.py <L>/draf/draf-v1.md
```
Hasil `periksa.py` adalah petunjuk, bukan putusan: setiap temuan dibaca dalam konteksnya.

Di checkpoint, sebutkan juga contoh gaya yang dipakai (`draf/teladan-gaya.md`), hasil cek tiru dari `cek_naskah.py --sumber`, dan tabel putaran visual di `draf/rencana-visual.md`.
