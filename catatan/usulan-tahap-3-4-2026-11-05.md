# Riset tahap 3, 4, dan alat visual (5 Nov 2026)

Pencarian di paper 2024–2026, GitHub, X, dan blog praktisi tentang cara yang lebih canggih untuk menyusun kerangka, menulis draf, dan membuat visual.

## Yang sudah diterapkan (riwayat 2026-11-05n)

| Kode | Perubahan | Dasar |
|---|---|---|
| 3-1 | Cek argumen pasaran (`workflow/03-kerangka.md` § 4, `templates/prompt-argumen-pasaran.md`) | "Argument Collapse", arXiv 2606.01736 (2026): 3,4% argumen utama LLM unik vs 65,3% manusia; Claude ikut diuji |
| 3-2 | Debat kerangka pembela–penyerang, "dalam dulu, baru lebar" (§ 2 dan § 6, `templates/prompt-serang-kerangka.md`) | DARE, EMNLP 2025 (https://aclanthology.org/2025.emnlp-main.483); evaluasi sebagian besar otomatis |
| 3-3 | Struktur esai dipilih secara sadar (§ 1) | Argument Collapse: pola "dukungan → usulan" 29% pada LLM vs 12% pada manusia |
| 4-1 | Contoh gaya 1–2 cuplikan + cek tiru (`workflow/04-menulis-draf.md` § Contoh gaya) | arXiv 2509.14543 (2025): satu contoh menaikkan ketepatan gaya, 2→10 contoh hampir tidak menambah, contoh bertopik sama justru menurunkan |
| V-1 | Cek tata letak otomatis di `tools/buat_visual.py` | Masalah paling sering pada gambar; bisa diukur mesin |
| V-2 | Putaran umpan balik visual, maks. 3 putaran (`workflow/03b-rencana-visual.md` § 8) | MatPlotAgent, ACL Findings 2024 (arXiv 2402.11453): umpan balik visual adalah pendorong utama mutu |

## Usulan yang belum diterapkan (PL38–PL44 di `catatan/buku-pelajaran.md`)

| ID | Kode | Usulan | Dasar dan kekuatan bukti | Cara menguji |
|---|---|---|---|---|
| PL38 | 3-4 | Kotak "situasi retorika" di kerangka: kenapa mendesak sekarang, siapa juri yang membaca, apa batasannya, lalu pilih teknik persuasi | DARE (teori Bitzer); sedang | Satu lomba memakai, bandingkan skor kriteria "persuasif/argumentasi" juri AI tahap 5 dengan lomba sebelumnya |
| PL39 | 3-5 | Bedah kerangka esai juara edisi lalu (struktur, bukan isi) kalau teksnya tersedia | Tips praktisi; lemah | Catat di 8b apakah struktur esai juara mirip struktur yang kita pilih |
| PL40 | 4-2 | Judul, pembuka, dan penutup ditulis 3 versi, dipilih juri buta lewat adu dua arah | Usulan sendiri, meniru cara Arena; belum ada sumber luar | Hitung seberapa sering versi pertama yang menang; kalau hampir selalu, langkah ini tidak perlu |
| PL41 | 4-3 | Pembaca baru menandai 5 kalimat paling generik, hanya kalimat itu yang ditulis ulang | Tips praktisi (blog panduan menulis dengan Claude); lemah | Bandingkan jumlah temuan "generik/klise" juri lapis kedua tahap 5 sebelum dan sesudah |
| PL42 | 4-4 | Perencana per bagian (ringkasan rencana setiap bagian sebelum ditulis) untuk LKTI ≥3.000 kata | Agents' Room (arXiv 2410.02603, fiksi) dan LongWriter (arXiv 2408.07055); sedang, bukan esai | Pakai di lomba LKTI berikutnya; catat di 8a apakah ada bagian yang melenceng dari kerangka |
| PL43 | V-3 | Grafik baru: batang berkelompok/bertumpuk, garis dengan penanda peristiwa | Kebutuhan umum esai kebijakan | Tambahkan saat lomba pertama yang membutuhkannya |
| PL44 | V-4 | Diagram rumit (>6 kotak, bercabang, banyak pelaku) lewat Graphviz | Graphviz paling luas dipakai dan bisa dibaca agen; perlu `winget install graphviz` | Tambahkan saat diagram alur/siklus tidak cukup |

## Yang dicek tetapi tidak cocok untuk esai lomba

STORM dan OmniThink (artikel gaya Wikipedia berbasis retrieval; STORM menunjukkan menghapus kerangka menurunkan mutu, yang mendukung tahap 3 kita), WriteHERE (perencana rekursif laporan/narasi), LongWriter (metode data latih untuk teks 20 ribu kata), Agents' Room (fiksi panjang). Tips praktisi di X dan blog (kerangka dulu, draf lalu sunting terpisah, contoh gaya) sudah sejalan dengan workflow.
