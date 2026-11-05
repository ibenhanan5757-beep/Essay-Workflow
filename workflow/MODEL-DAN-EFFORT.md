# Manual model dan effort per tahap

Manual ini menjawab dua pertanyaan di awal setiap utas: **model apa** (Opus 5.5 atau Sonnet 5.5) dan **effort berpikir berapa** (medium, high, atau xhigh). Dasarnya `catatan/audit-hemat-token-2026-11.md` § 6 (usulan U3, PL29) dan tabel subagent di `workflow/01-ide-dan-tesis.md` § Juri buta. Aturan lomba dan pengaman di CLAUDE.md tetap lebih kuat dari manual ini.

## Prinsip

1. **Mutu esai didahulukan.** Setiap langkah yang menentukan isi esai (aturan lomba, ide, bukti, kerangka, tulisan, revisi) memakai Opus. Sonnet hanya dipakai di langkah yang tidak mengubah isi esai, atau yang memang lebih baik dikerjakan model lain (juri; lihat § Kenapa juri tetap Sonnet).
2. **Hemat di langkah mekanis justru menjaga mutu.** Di Pharfest, kuota habis di tengah lomba sehingga Arena dipangkas dan tahap 6 tidak selesai. Kerusakan mutu terbesar datang dari tahap mutu yang terpaksa dilewati, bukan dari model yang lebih kecil di langkah mekanis.
3. **Effort xhigh untuk langkah yang membuat isi** (1C, 3, 4). Effort `max` tidak dipakai; dokumentasi resmi menyebutnya "prone to overthinking".
4. **Model dipilih di awal utas dan tidak diganti di tengah utas.** Setiap model punya cache sendiri, jadi ganti model di tengah utas membuat seluruh utas diproses ulang. **Effort boleh diubah kapan saja** di model 5.5 tanpa merusak cache.
5. **Subagent tidak mengikuti utas utama.** Agen `juri-ide`, `juri-esai`, dan `auditor-sitasi` dikunci ke Sonnet lewat frontmatter. Model lain untuk subagent ditulis eksplisit per panggilan (parameter `model`).

## Tabel utas utama

| Utas | Isi pekerjaan | Model | Effort | Dampak ke mutu esai |
|---|---|---|---|---|
| Pra-0 | Rekap bookmark IG (`lomba-ig/`) | Sonnet | medium | Tidak ada; belum menyentuh esai |
| 0 | Bedah guidebook → `aturan.md`, `profil.json`, `STATUS.md` | **Opus** | high | Salah baca aturan berarti diskualifikasi. Profil juri dan rubrik yang keliru membuat Arena membidik sasaran yang salah. Utasnya pendek |
| 1A | Bekal, pasaran, tambang literatur, rumusan peluang | Opus | high | Rumusan peluang menentukan arah semua ide |
| 1B | Loop 1–3: bersihkan kartu, acak, panggil juri, simpan JSON, kolam dan dedup | Sonnet | **high** | Utas ini tidak membuat ide; ide dibuat subagent generator Opus. Effort high untuk keputusan dedup dan kolam |
| 1C | Finalis, cek "sudah ada?", evolusi/hibrida, paket esai, adu | Opus | **xhigh** | Titik keputusan terbesar: ide adalah penentu utama di babak juri manusia |
| 2 | Riset, peta klaim, dossier | **Opus** | high | Memilih bukti terkuat dan memberi ✅ menentukan nilai "data/bukti" dan akurasi. Pencarian dilempar ke subagent Sonnet (≤3 paralel) supaya utas tetap pendek; verifikasi tetap di utas ini |
| 3 + 3b | Kerangka argumen, kontra-argumen, judul, rencana visual | Opus | **xhigh** | Logika esai dikunci di sini |
| 4 | Menulis draf + semua visual esai | Opus | **xhigh** | Ini produknya. Giliran yang hanya menjalankan alat otomatis memakai sedikit thinking, jadi xhigh tidak boros di sana |
| 5 ⇄ 6 (per putaran) | Panggil juri, rekap temuan, revisi isi | Opus | high | Revisi mengikuti temuan juri yang sudah spesifik (kutipan + lokasi). Naikkan ke xhigh kalau revisi menyentuh struktur argumen atau tesis |
| 6 build | `build_docx.py`, `cek_docx.py`, render dan cek halaman PDF | Sonnet | medium | Tidak mengubah kata; format dijaga alat dan cek visual per halaman |
| 7 | Sampul, poster, infografis terpisah | Sonnet, medium; **Opus, high** kalau karya itu ikut dinilai rubrik | | Desain yang dinilai juri diperlakukan seperti isi |
| 7C | Slide dan naskah bicara (hanya kalau penulis meminta) | Opus | high | Alur presentasi dan jawaban tanya-jawab adalah isi argumen |
| 8a / 8b | Retro proses dan retro hasil | Sonnet | medium | Esai sudah dikirim |
| 8c | Tinjauan workflow dan usulan perubahan | Opus | high | Menentukan mutu semua lomba berikutnya |

**Mode Kilat** (`workflow/MODE-KILAT.md`) memakai tabel yang sama. Effort xhigh tidak diturunkan, karena yang dipangkas Mode Kilat adalah jumlah langkah, bukan kedalaman berpikir.

**Kalau kuota sudah ≥ 70%** (limit 5 jam atau mingguan): jangan turunkan model atau effort di utas 0, 1C, 2, 3, 4, dan 5 ⇄ 6. Pilihannya, diputuskan penulis: (a) tunggu limit 5 jam pulih, lalu lanjut dengan utas baru dari § Serah terima; (b) kerjakan dulu utas mekanis (1B, 6 build, 7) yang memang Sonnet; (c) kalau tenggat memaksa, penulis sendiri yang memilih langkah mana yang dikurangi, dan pilihannya dicatat di `STATUS.md`.

Dalam **mode jalan terus** (`CLAUDE.md` § Mode jalan terus), tahap 0–1C dikerjakan di satu utas, jadi model utas utama tidak berganti di 1B. Pilih Opus untuk utas itu (0, 1A, dan 1C memakai Opus). Model subagent tetap mengikuti tabel di bawah.

## Tabel subagent

Effort subagent hanya ditulis kalau tercantum di sini. Selebihnya biarkan bawaan.

| Peran subagent | Tahap | Model | Effort |
|---|---|---|---|
| Peneliti bekal, tambang literatur | 1A | `sonnet`, maksimal 3 paralel | bawaan |
| Prediksi pasaran | 1A | Sonnet (bawaan agen) | bawaan |
| Jawaban chatbot | 1A | `haiku` (sengaja: meniru jawaban yang didapat peserta biasa) | bawaan |
| Generator ide (3) | 1B | `opus` | high |
| Juri loop (3 per loop) | 1B | 2 × Sonnet + 1 × `haiku`, persona yang mendapat Haiku diputar | bawaan |
| Kesan 30 detik | 1B | `haiku` (sengaja: reaksi pembaca sekilas) | bawaan |
| Kritik finalis | 1C | Sonnet | bawaan |
| Pencari bukti, cek "sudah ada?" | 1C | `sonnet`, maksimal 3 paralel | bawaan |
| Panel final (3) | 1C | 1 × `opus` + 2 × Sonnet, diputar | Opus: high |
| Adu berpasangan | 1C | Sonnet | bawaan |
| Pencari bukti per pertanyaan | 2 | `sonnet`, maksimal 3 paralel | bawaan |
| Juri rubrik, devil's advocate, serangan tunggal, konfirmasi, banding berpasangan | 5 | Sonnet (bawaan `juri-esai`) | bawaan |
| Auditor sitasi | 5 | Sonnet (bawaan `auditor-sitasi`) | bawaan |
| Argumen pasaran, serang kerangka | 3 | Sonnet (bawaan `juri-esai`) | bawaan |
| Juri presentasi | 7C | Sonnet | bawaan |

**Jangan:** auditor sitasi atau juri esai dengan Haiku (salah baca dukungan kutipan menghasilkan temuan Kritis yang keliru); semua juri loop Haiku (PL06); peneliti Opus paralel (Pharfest: limit 5 jam habis dalam ±15 menit). Subagent Opus di luar tabel ini memicu peringatan boros (CLAUDE.md).

## Kenapa juri tetap Sonnet

Ini bukan sekadar hemat. Ada tiga alasan mutu:

1. **Juri sebaiknya berbeda model dari penulis.** Juri LLM cenderung lebih menyukai tulisan buatan dirinya sendiri (Panickssery dkk. 2024, https://arxiv.org/abs/2404.13076; lihat `catatan/evaluasi-arena-ide-2026-11.md`). Draf dan ide ditulis Opus, jadi juri Sonnet lebih keras menilainya daripada juri Opus. Masih satu keluarga (Claude), jadi bias ini hanya teredam sebagian.
2. **Pencari bukti tidak memutuskan.** Subagent riset Sonnet hanya membawa calon sumber dan kutipan. Yang memilih bukti dan memberi ✅ adalah utas utama Opus (tahap 2), setelah mencocokkan dengan teks di `riset/teks/`.
3. **Keputusan juri berlapis.** Skor wajib disertai kutipan, temuan Kritis/Mayor dikonfirmasi juri kedua, perbandingan dijalankan dua kali dengan posisi ditukar, dan keputusan akhir ide ada di tangan penulis.

**Haiku di juri loop** sengaja dipertahankan. Juri manusia sungguhan juga ada yang membaca sekilas, mediannya membuang suara yang menyimpang, dan ide yang hanya disukai satu juri tetap bisa masuk lewat jalur kartu liar. Model juri adalah hipotesis strategi (PL06), jadi baru boleh diubah setelah ≥3 lomba dengan hasil diketahui (CLAUDE.md § Workflow yang memperbaiki diri).

**Risiko yang masih ada:** juri Sonnet bisa melewatkan kelemahan halus yang akan dilihat juri manusia ahli. Penangkalnya sudah ada di tahap 5 (devil's advocate, serangan tunggal, konfirmasi). Pengecekan tambahan yang bisa dilakukan secara manual: penulis menempel draf ke ChatGPT atau Gemini sebagai juri dari keluarga model lain (CLAUDE.md § Celah yang sudah diketahui).

## Cara memakai

1. **Sebelum pesan pertama di utas baru**, pilih model dan effort sesuai tabel utas utama: lewat pemilih model di kotak pesan aplikasi desktop, atau `/model` di terminal. Kalau lupa, tulis di pesan pertama, misalnya "pakai Opus, effort xhigh", dan Claude menggantinya di awal utas, saat cache utas masih kecil.
2. **Di setiap checkpoint**, isi baris "Utas berikutnya: model … · effort …" di `STATUS.md` § Serah terima, diambil dari tabel ini.
3. **Di § Log kuota**, kolom subagent ditulis "jumlah × model" (misalnya "3 × opus, 9 × sonnet, 3 × haiku"), supaya tahap 8c bisa menilai apakah tabel ini perlu diubah.
4. **Kalau di tengah utas ternyata butuh model lain** (misalnya utas Sonnet harus menulis ulang bagian esai), simpan hasil ke file, tutup checkpoint, dan buka utas baru dengan model yang tepat. Jangan ganti model di utas yang sudah panjang.

## Status tabel ini

Tabel ini adalah **aturan proses**, yang boleh diubah setelah 1 lomba lewat 8c. Dibanding usulan U3 di audit, versi ini menaikkan utas 0 dan 2 ke Opus, utas 1B ke effort high, 1C/3/4 ke xhigh, 8c ke Opus, dan menghapus penurunan effort saat kuota tinggi. Semua kenaikan ini **belum diuji** dan menambah pemakaian kuota (pengali pastinya tidak dipublikasikan). Uji di lomba berikutnya: catat § Log kuota per utas, dan di 8a nilai apakah ada tahap mutu yang terpangkas karena kuota. Kalau ada, langkah pertama yang dikembalikan ke Sonnet adalah utas 0, karena paling mekanis di antara kenaikan itu.
