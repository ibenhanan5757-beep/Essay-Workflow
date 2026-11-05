# Tahap 0 — Bedah Guidebook

Diadopsi dari Fase 0 "Master SOP Juara" dan diperketat. Contoh hasil lengkap: `lomba/ewc-siswa-pharfest-2026/aturan.md` + `STATUS.md` + `profil.json`.

Persiapan: salin `lomba/_template/` ke `<L>` dan taruh guidebook di sana. Baca **seluruh** guidebook, termasuk FAQ dan lampiran; aturan penting sering tersembunyi di FAQ.

**Bawa pelajaran lomba sebelumnya**: baca `catatan/buku-pelajaran.md` § Aktif dan `catatan/bank-juara.md` (bidang/jenjang yang sama). Tulis di `STATUS.md` versi workflow (entri terakhir `catatan/riwayat-workflow.md`) dan ID pelajaran yang relevan untuk lomba ini. Contohnya PL03 (surat orisinalitas) dan PL10 (minta penulis mengecek Instagram panitia untuk judul juara edisi lalu). Catat juga **tanggal pengumuman** dari guidebook, karena tanggal ini dipakai untuk tahap 8b.

Ekstrak teksnya dulu dengan nomor halaman: `python tools/baca_pdf.py <L>/guidebook.pdf --out <L>/guidebook.txt`. Halaman yang diberi peringatan "hampir tanpa teks" (poster, tabel gambar) dibaca langsung sebagai gambar, jangan ditebak.

Tujuan: mengubah guidebook menjadi **tiga hal yang bisa dipakai**: (1) matriks kepatuhan, (2) peta rubrik ke alokasi tenaga, (3) profil juri. Jangan menulis apa pun sebelum ketiganya selesai.

## 1. Matriks kepatuhan
Ekstrak setiap aturan yang bisa membuat naskah **didiskualifikasi atau kehilangan nilai**. Setiap baris wajib menyebut halaman guidebook-nya.

| Aturan | Nilai | Hlm | Cara cek | Alat |
|---|---|---|---|---|
| Batas kata | ... | | otomatis | `tools/cek_naskah.py` |
| Font/ukuran/spasi/margin/indent/nomor halaman | ... | | otomatis | `tools/build_docx.py` + `<L>/profil.json` |
| Identitas penulis/logo dilarang | ... | | otomatis (`--nama`) | `cek_naskah.py` |
| Gambar/tabel hanya di lampiran | ... | | otomatis | `cek_naskah.py` |
| Gaya sitasi | ... | | semi | `cari_sumber.py cek-pustaka` |
| Struktur wajib | ... | | manual | |
| Format & nama file | ... | | manual | |
| Lampiran administrasi (surat orisinalitas, dll.) | ... | | manual | |
| Revisi setelah kirim | boleh/tidak | | — | |
| Tenggat (tanggal + jam + zona waktu) | ... | | — | |

Langsung isi `<L>/profil.json` (dari template) supaya format dan batas kata dicek mesin, bukan ingatan.

**Tandai ambiguitas** (contoh: "minimal 1000—1500 kata" itu minimum 1.000 atau rentang 1.000–1.500?) dan pilih tafsiran yang paling aman, yaitu yang memenuhi kedua bacaan.

## 2. Aturan AI (workflow ini untuk esai 100% AI)
- Apakah guidebook menyebut AI? Kalau ya, kutip persis.
- Cek apakah prompt/log harus dilampirkan, model/alat apa yang boleh, dan apakah boleh disunting manual.
- **Peringatan:** kalau guidebook melarang AI atau mewajibkan pernyataan bahwa esai adalah karya peserta sendiri, sampaikan ke penulis dengan kutipan halamannya sebelum lanjut.

## 3. Peta rubrik → alokasi tenaga
Tulis bobot setiap kriteria, lalu tanyakan: *kriteria mana yang paling murah dinaikkan?*
- Kriteria format/bahasa biasanya murah: kerjakan dengan alat dan checklist sampai sempurna.
- Kriteria isi (orisinalitas, ketajaman analisis) mahal: di sinilah waktu ideasi dan riset dihabiskan.
- Komponen yang **tidak ada di rubrik** (misal visual mewah) jangan diberi tenaga besar.

## 4. Profil juri (berbasis bukti, bukan stereotip)
- Siapa penyelenggara (fakultas, himpunan, lembaga)? Siapa juri yang disebut di guidebook?
- Apa yang **dianggap dangkal** oleh juri bidang itu? (Contoh juri farmasi: solusi berupa "sosialisasi" atau "aplikasi" tanpa mekanisme, data, dan regulasi. Contoh juri ekonomi: solusi tanpa hitungan biaya. Contoh juri lingkungan: klaim dampak tanpa data emisi/limbah.)
- Apa yang **dianggap salah** oleh mereka? (Istilah bidang yang keliru, klaim efektivitas tanpa bukti, mengabaikan regulasi yang berlaku.)
- **Jenis esai**: ilmiah populer, ilmiah/LKTI, opini/argumentatif, reflektif/naratif. Ini menentukan nada dan kedalaman teknis di tahap 4.
- Jenjang peserta: juri menilai relatif terhadap jenjang. Esai SMA tidak perlu terdengar seperti tesis, tapi harus akurat.

## 5. Garis waktu mundur
Dari tenggat, hitung mundur: final H-1, review H-2, draf H-3, riset dan kerangka sebelum itu. Kalau lomba tidak mengizinkan kirim ulang, buffer H-1 wajib.

Perkiraan waktu per tahap untuk esai 1.000–2.000 kata. Waktu kerja Claude berjalan sambil penulis mengerjakan hal lain. Waktu checkpoint bergantung pada seberapa cepat penulis membaca dan menyetujui.

| Tahap (utas) | Kerja Claude | Waktu penulis di checkpoint | Catatan |
|---|---|---|---|
| 0 Bedah guidebook | 15–30 menit | 15 menit | lebih lama kalau PDF berupa scan |
| 1A Bekal, pasaran, tambang literatur, peluang | 45–90 menit | 10 menit | riset paling berat di Arena; subagent riset Sonnet, maks. 3 bersamaan |
| 1B Loop 1–3 + kolam | 45–90 menit | 10 menit | ±15 panggilan subagent (generator + juri + kesan); juri berjalan bersamaan |
| 1C Final | 1–2 jam | 30 menit | ±18 panggilan subagent + ±45–60 pencarian bukti dan cek "sudah ada?" untuk 9 finalis |
| 2 Riset & peta klaim | 1–2 jam | 20 menit | lebih cepat kalau teks penuh tersedia (`cari_sumber.py teks`) |
| 3 + 3b Kerangka & rencana visual | 30–60 menit | 15 menit | termasuk cek argumen pasaran dan debat kerangka (2–3 panggilan subagent) |
| 4 Draf v1 + visual | 45–90 menit | 20 menit | termasuk render dan cek setiap gambar |
| 5 ⇄ 6 Loop juri & revisi | 45–90 menit per putaran (biasanya 1–3) | 15 menit per putaran | 4–5 panggilan subagent per putaran |
| 6 Build DOCX/PDF + cek akhir | 15–30 menit | 20 menit | buka file hasil build sendiri |
| 7 / 7C (opsional) | 30–90 menit / 1–2 jam | 15–30 menit | 7C hanya kalau penulis meminta PPT |
| 8a / 8b / 8c | 15–30 menit masing-masing | 10 menit | 8b setelah pengumuman |

Angka di atas adalah **perkiraan, belum diukur**: Arena Ide v2 belum pernah dijalankan utuh (PL12). Ukuran sebenarnya dikumpulkan lewat `STATUS.md` § Log kuota dan tahap 8a, lalu tabel ini diperbarui.

Total jalur penuh (tahap 0–6): kira-kira **7–14 jam kerja Claude**, tersebar dalam **3–5 hari kalender**. Yang paling sering memperlambat bukan kerja Claude, tetapi (1) limit 5 jam yang habis di tengah Arena, sehingga utas berikutnya harus menunggu reset, dan (2) waktu penulis membaca di setiap checkpoint. **Kalau sisa waktu sampai tenggat ≤ 5 hari**, sampaikan ke penulis dan tawarkan **Mode Kilat** (`workflow/MODE-KILAT.md`). Mode Kilat bukan default: penulis yang memutuskan, dan keputusannya dicatat di `STATUS.md`.

## Checkpoint
Matriks kepatuhan, profil JSON, peta rubrik, profil juri, dan aturan AI ditunjukkan ke penulis. Semua ditulis di `<L>/aturan.md`; tenggat di `<L>/STATUS.md`.

**Mode jalan terus** (`CLAUDE.md` § Mode jalan terus, default kalau penulis berkata "kerjakan"): checkpoint ini tidak ditunggu. Isinya tetap ditulis ke `aturan.md` dan `STATUS.md`, lalu disajikan di laporan final Arena Ide. Claude tetap berhenti di sini kalau guidebook melarang AI, tenggat ≤ 5 hari dan jalur belum dipilih penulis, atau ada ambiguitas yang mengubah arah ide.

Setelah checkpoint ini, tahap 1–8 membaca aturan dari `aturan.md`, bukan dari guidebook. Guidebook hanya dibuka lagi untuk mengecek kutipan halaman tertentu (CLAUDE.md § Satu utas pendek per tahap, "Baca seperlunya"). Karena itu `aturan.md` harus lengkap: setiap aturan yang bisa menggugurkan atau mengurangi nilai ditulis beserta halamannya.
