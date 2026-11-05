# Kritik terhadap "Master SOP Workflow LKTI/Esai Champion"

(SOP aslinya sekarang di `arsip/catatan/MASTER_SOP_WORKFLOW_LKTI_ESAI_CHAMPION.md`.)

Dibaca dengan kacamata AI engineer yang skeptis: apa yang benar-benar menaikkan peluang menang, dan apa yang justru membuat AI menghasilkan naskah yang rapuh atau curang tanpa sengaja. Kasus uji: guidebook EWC Siswa Pharfest UI 2026.

## Ringkasan

SOP ini punya kerangka yang bagus (bedah guidebook, turnamen ide, pre-mortem, loop juri, otomasi DOCX), tapi **dibuat dari satu kasus lomba geomatika dan isinya ikut terbawa jadi aturan umum**. Kalau dipakai mentah-mentah untuk Pharfest, hasilnya akan melanggar format lomba di beberapa titik dan mendorong AI mengarang data. Masalah terbesarnya: **tidak ada satu pun langkah verifikasi sumber**, padahal SOP menuntut 10–15 referensi Scopus Q1, "validasi retrospektif", dan angka "miliar rupiah diselamatkan".

## Yang bagus dan saya ambil

| Ide dari SOP | Kenapa bagus | Diadopsi di |
|---|---|---|
| Fase 0: bedah guidebook + bobot rubrik | Rubrik menentukan ke mana tenaga dialokasikan | `workflow/00-dekonstruksi-lomba.md` |
| Profil juri dari penyelenggara | Juri farmasi menilai beda dengan juri geomatika | sama |
| Turnamen ide + pre-mortem | Memaksa membuang ide yang cacat sebelum menulis | `workflow/01-ide-dan-tesis.md` |
| Lokus spesifik (bukan "seluruh Indonesia") | Konkret = orisinal dan bisa diverifikasi | `01`, `02` |
| Dossier riset sebelum menulis | Mencegah menulis dulu, cari bukti belakangan | `02-riset.md` |
| Loop juri dengan rubrik resmi | Review terarah ke apa yang dinilai | `05-review.md` |
| Build DOCX otomatis dari Markdown | Format bernilai besar (Pharfest: bagian dari 30%) dan rawan salah kalau manual | `tools/build_docx.py` |
| Siapkan defense kalau ada babak presentasi | Relevan untuk lomba yang punya final | `07-sampul-poster.md` (opsional) |

## Yang bermasalah

### 1. Overfit ke satu lomba (masalah paling sistemik)
Lyzenga, Landsat, AHP, batimetri, "Traffic Light System", "Zero-Cost GEE" ditulis seolah wajib. Pharfest adalah **esai ilmiah populer untuk SMA**, juri akademisi dan praktisi kesehatan. Memaksakan rumus matematis ke esai farmasi 1.000–1.500 kata membuatnya terasa dibuat-buat dan memakan ruang dari analisis. Prinsip yang benar: *kedalaman ilmiah sesuai bidang juri* (untuk farmasi: mekanisme degradasi obat, mekanisme resistensi, regulasi BPOM/Permenkes, data Kemenkes/WHO), bukan "harus ada fisika".

### 2. Default panjang dan struktur bertabrakan dengan aturan
- SOP: 7–12 halaman / 3.500–5.500 kata, 7 bab, abstrak, roadmap 5 tahun.
- Pharfest: **1.000–1.500 kata**, tiga bagian (pendahuluan, isi, penutup), tanpa cover.
- SOP: TNR 11 pt, spasi 1,15, judul berwarna navy. Pharfest: **12 pt, spasi 1,5, justify, indent 1 cm, nomor halaman kanan bawah**.
- SOP: grafik di dalam naskah. Pharfest: **gambar/tabel hanya di lampiran paling akhir**.

SOP memang bilang "jika tidak tertulis", tapi bagian Fase 3 dan 6 ditulis sebagai baku, dan AI cenderung mengikuti contoh paling konkret. Di workflow baru, aturan lomba selalu jadi parameter dan default hanya dipakai kalau guidebook kosong.

### 3. Tidak ada verifikasi sumber, padahal permintaannya mengundang halusinasi
"Minimal 10–15 referensi Scopus Q1", "validasi retrospektif", "confusion matrix & Kappa", "berapa miliar rupiah diselamatkan". Siswa SMA dan AI tidak punya data lapangan untuk validasi. Tanpa langkah verifikasi, AI akan **mengarang hasil uji dan angka penghematan** agar memenuhi template. Juri akademisi bisa mengecek satu DOI saja, dan satu referensi palsu bisa menggugurkan naskah. Di workflow baru: setiap angka harus punya sumber yang sudah dibuka, dan yang tidak ada data aslinya ditulis sebagai *estimasi dengan asumsi eksplisit* atau dibuang.

### 4. Loop juri "ulangi sampai skor >98" itu cacat secara desain
- **Model menilai tulisannya sendiri**: bias penilaian diri, skor cenderung naik tiap putaran walau kualitas tidak naik.
- **Target angka = Goodhart**: AI belajar memuaskan juri tiruan, bukan juri asli. Skor 98 tidak berarti apa-apa.
- **Revisi berulang menambah slop**: tiap putaran cenderung menambah istilah, klaim, dan kalimat penegas.
- Perbaikan: juri dijalankan di konteks baru (subagent yang tidak melihat proses menulis), memakai rubrik resmi dengan **bukti kutipan wajib** untuk setiap skor, berhenti ketika **tidak ada temuan Kritis/Mayor** (bukan saat skor tembus angka), maksimal 2–3 putaran, dan versi baru dibandingkan berpasangan dengan versi lama ("mana yang lebih baik dan kenapa") supaya revisi tidak membuat naskah mundur.

### 5. "Visual luxury" salah prioritas untuk lomba ini
Di Pharfest, 30% nilai adalah bahasa dan **kepatuhan format**. Visual hanya boleh di lampiran dan tidak ada di rubrik. Dashboard HTML mockup dan 3 grafik 300 DPI menghabiskan waktu untuk komponen yang nyaris tidak dinilai. Waktu lebih baik dipakai untuk EYD V, kalimat efektif, dan analisis.

### 6. Nada hype mendorong klaim berlebihan
"Juara 1 Mutlak", "menghantam pembaca", "titan", "rahasia alam" adalah instruksi gaya yang bocor ke naskah. AI yang disuruh "menghantam" akan menaikkan kekuatan klaim melebihi bukti, dan juri akademisi justru menghukum itu.

### 7. Tidak portabel dan tidak ada cek kepatuhan
- Bergantung pada tool Antigravity (`invoke_subagent`, `.agents/skills/...`).
- Tidak ada cek jumlah kata, penamaan file, larangan nama/logo di naskah, surat orisinalitas, atau tenggat. Padahal pelanggaran administratif = diskualifikasi, dan Pharfest **tidak mengizinkan revisi/kirim ulang**.

### 8. Formula judul satu pola
`[AKRONIM]: [Metode] [Solusi] Melalui [Teknologi] di [Lokus]` akan menghasilkan judul yang mirip dengan ratusan peserta lain yang memakai template serupa. Guidebook Pharfest meminta judul "ekspresif". Pakai formula itu sebagai salah satu kandidat saja.

## Catatan penting soal Pharfest dan AI

Guidebook Pharfest **tidak menyebut AI sama sekali**, tapi mewajibkan "hasil karya orisinil peserta" dan **surat pernyataan orisinalitas yang ditandatangani**. Esai 100% AI di lomba ini berisiko: kalau panitia menganggapnya bukan karya orisinal peserta, sanksinya diskualifikasi dan pembatalan juara. Kalau lomba yang benar-benar diikuti memang lomba esai AI, aman. Kalau targetnya Pharfest, sebaiknya tanya panitia (humas.pharfest@gmail.com) soal kebijakan AI sebelum mengirim, atau pakai mode "AI membantu, peserta menulis".

## Kesimpulan

Pakai SOP itu sebagai **daftar ide**, bukan prosedur. Prinsipnya yang bagus sudah saya masukkan ke workflow. Konten spesifik geomatika, target skor, dan default panjang/format tidak saya pakai.
