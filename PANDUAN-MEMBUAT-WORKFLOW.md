# Panduan Membuat Workflow Baru (untuk diberikan ke Claude)

Disarikan dari pembuatan dan revisi workflow esai lomba di folder ini (28 Okt – 5 Nov 2026): audit, 4 lomba nyata, riset cara kerja juri dan pipeline ide, dan perbaikan hemat kuota. Isinya prinsip yang **terbukti berguna atau terbukti dibutuhkan setelah ada yang gagal**, ditambah langkah untuk menyusun workflow baru: lomba poster/infografis, video AI, hackathon, pitch, atau pekerjaan berulang lain.

**Cara pakai.** Salin file ini ke folder kosong untuk proyek baru, lalu kirim ke Claude:
> Baca `PANDUAN-MEMBUAT-WORKFLOW.md`, lalu bantu aku membuat workflow untuk **[tujuan]**. Mulai dari Langkah 1, dan berhenti di setiap checkpoint.

---

## Bagian 1 — Prinsip (berlaku untuk workflow apa pun)

| # | Prinsip | Kenapa (dari pengalaman) |
|---|---|---|
| 1 | **Aturan pemberi tugas menang atas default workflow.** Tahap pertama selalu "bedah aturan": matriks kepatuhan dengan nomor halaman, rubrik resmi, profil juri, tenggat, aturan AI. | Aturan penting sering tersembunyi di FAQ dan lampiran. Satu pelanggaran format bisa menggugurkan karya sebagus apa pun. |
| 2 | **Keputusan mahal ditaruh di depan.** Pilih konsep atau ide sebelum produksi, dan beri tahap itu tenaga terbesar. | Mengganti ide setelah draf atau video jadi jauh lebih mahal daripada menyeleksi ide di awal. |
| 3 | **Pisahkan pembuat dan penilai.** Penilai adalah subagent tanpa konteks yang tidak melihat proses pembuatan. Kartu dibersihkan dari pembelaan diri pembuat, urutan diacak dengan skrip, alasan ditulis sebelum skor, dan perbandingan berpasangan dijalankan dua arah (tidak sepakat = seri). | Model yang baru membuat sesuatu cenderung membelanya. Juri LLM punya bias posisi, bias panjang, dan bias memilih tulisan sendiri. |
| 4 | **Penilai AI hanya proksi.** Laporkan ketidakpastian ("seri" kalau selisihnya kecil), lalu biarkan manusia memilih. | Panel dan adu memilih juara berbeda di 2 dari 2 lomba. Selisih skor di puncak sering masih dalam derau. |
| 5 | **Hitungan oleh skrip, bukan oleh model.** Ini mencakup acak dengan seed, median, poin adu, jumlah kata, ukuran file, dan durasi. | Model salah menghitung dan tidak bisa diulang. Skrip bisa diuji dan hasilnya sama setiap kali. |
| 6 | **Jangan mengarang.** Setiap fakta, angka, dan kutipan punya sumber yang bisa dicek. Yang belum terverifikasi diberi penanda (`[PERLU SUMBER]`), dan build ditolak selama penanda masih ada. | Sumber palsu lebih merusak daripada karya yang terlambat. |
| 7 | **Cek mesin dulu, juri belakangan.** Pemeriksaan murah dan pasti (format, angka, ejaan, ukuran) dijalankan sebelum penilaian yang mahal. | Juri jadi fokus ke isi, dan putaran juri tidak terbuang untuk salah ketik. |
| 8 | **Berhenti berdasarkan temuan, bukan target skor.** Batasi jumlah putaran (misalnya 3). Kalau skor mendatar dua putaran, berhenti memoles dan cari bahan baru. | Lima putaran juri di Pharfest mentok di 7,7–7,8. Yang menahan skornya isi, bukan bahasa. |
| 9 | **Untuk ide: buat banyak, buang yang kembar, cek "sudah ada?".** Siapkan anti-referensi (karya juara lalu, ide pasaran, jawaban chatbot untuk prompt polos), lalu cari tumpang tindih di web, literatur, paten, dan lomba lain. | Ide LLM dari satu prompt cenderung seragam. Peserta lain juga memakai AI. Satu ide "juara" ternyata sudah ada di jurnal. |
| 10 | **Manusia memegang checkpoint.** Setiap tahap berakhir dengan hasil yang ditunjukkan, lalu menunggu persetujuan. Pilihan penting (ide, konsep, kirim) milik manusia. | Mencegah kerja panjang ke arah yang salah. |
| 11 | **Keadaan disimpan di file, bukan di percakapan.** Satu `STATUS.md` per proyek berisi progres, catatan keputusan, serah terima ke utas berikutnya, dan log kuota. | Satu lomba kehilangan hampir semua data evaluasi karena STATUS tidak diperbarui. |
| 12 | **Satu tahap, satu utas pendek.** Keluaran besar ditulis ke file, file dibaca seperlunya (Grep/rentang baris), dan pindah tahap dengan utas baru, bukan `/compact`. | Biaya terbesar adalah utas panjang yang dibaca ulang tiap pesan: ±170 juta dari 180 juta token adalah baca ulang cache. |
| 13 | **Subagent hemat kalau dipakai dengan benar.** Gunakan model kecil (Sonnet/Haiku) untuk juri dan riset, maksimal 3–4 berjalan paralel, dan cek kuota dulu. | 6 subagent Opus paralel menghabiskan limit 5 jam dalam ±15 menit. |
| 14 | **Isi dari folder, skill akun hanya untuk urusan file dan pencarian.** Rujukan yang menentukan isi disimpan di folder proyek (versinya terkunci). Skill akun dibatasi dengan daftar izin. | Skill akun bisa berubah sewaktu-waktu dan diam-diam mengubah gaya atau isi. |
| 15 | **Workflow memperbaiki diri lewat evaluasi.** Ada retro proses setelah kirim, retro hasil setelah pengumuman, dan buku pelajaran lintas proyek. Perubahan hanya dibuat dengan persetujuan, disertai hipotesis dan cara mengujinya. Bug boleh diperbaiki setelah 1 kasus; strategi baru diubah setelah ≥3 hasil. | Tanpa umpan balik, semua desain tetap tebakan. Satu kasus bisa menyesatkan, karena pola juara satu lomba hanya berlaku untuk lomba itu. |
| 16 | **Jujur soal risiko aturan.** Kalau aturan melarang AI atau mewajibkan pernyataan karya sendiri, sebutkan dengan kutipan halaman sebelum mulai. Jangan pernah membuat langkah untuk mengakali detektor. | 3 dari 4 lomba esai mewajibkan surat orisinalitas. Ini risiko terbesar, lebih besar daripada mutu karya. |

---

## Bagian 2 — Langkah menyusun workflow baru

### Langkah 1 · Wawancara singkat (Claude bertanya, maksimal 8 pertanyaan sekaligus)
1. Hasil akhirnya apa, dan dalam format apa (file, ukuran, durasi)?
2. Siapa yang menilai, dan apa kriterianya? Apakah ada rubrik resmi atau contoh karya juara?
3. Apa batasnya: tenggat, kuota/paket Claude, alat berbayar yang dimiliki, aturan AI?
4. Pembagian peran: apa yang dikerjakan AI dan apa yang diputuskan manusia?
5. Apa yang dianggap gagal (gugur, didiskualifikasi, jelek)?
6. Sumber data atau bahan apa yang tersedia?
7. Seberapa sering workflow ini akan dipakai: sekali, atau berulang untuk banyak lomba?
8. Ada workflow lama di folder lain yang bisa dijadikan contoh?

**Checkpoint:** ringkasan jawaban dalam 10 baris.

### Langkah 2 · Riset kecil (paling banyak 2–3 subagent Sonnet)
- Kriteria penilaian nyata dari 2–3 lomba sejenis, dan apa kata juri atau pemenang tentang hal yang membuat menang. Pola dari satu lomba **tidak** digeneralisasi.
- Metode yang dipakai praktisi bidang itu (misalnya design thinking untuk hackathon, storyboard untuk video).
- Alat, skill, dan connector yang tersedia di sesi ini, beserta celahnya. Uji langsung, jangan berasumsi.
- Risiko aturan: kebijakan AI, hak cipta, lisensi musik/gambar, privasi.

**Checkpoint:** laporan riset singkat dengan link. Simpan di `catatan/`.

### Langkah 3 · Rancang tahapan
Isi tabel ini dulu, sebelum menulis panduan apa pun:

| # | Tahap | Tujuan | Masukan | Keluaran (file) | Penilai/cek | Alat/skrip | Checkpoint |
|---|---|---|---|---|---|---|---|
| 0 | Bedah aturan | matriks kepatuhan | guidebook | `aturan.md`, `profil.json` | — | ekstrak PDF per halaman | ya |
| 1 | Arena konsep | pilih ide/konsep | aturan, riset | `ide/final.md` | juri buta + adu | skrip agregasi | ya |
| … | … | … | … | … | … | … | … |
| N | Evaluasi | pelajaran | semua | `evaluasi.md` | — | skrip rekap | ya |

Aturan rancangan:
- Setiap tahap menghasilkan **file**, dan tahap berikutnya hanya membaca file itu.
- Ada tahap "bedah aturan" di awal dan "evaluasi" di akhir.
- Setiap penilaian punya pemeriksaan mesin sebelumnya, dan setiap loop punya batas putaran.
- Siapkan **mode cepat** untuk tenggat sempit, dengan daftar yang tidak boleh dipangkas (kepatuhan dan kejujuran sumber), dan **ukuran resmi** (S/M/L). Tanpa itu, agen akan mengimprovisasi versinya sendiri setiap kali.
- Tulis perkiraan biaya per tahap (jumlah subagent, model).

**Checkpoint:** tabel tahapan disetujui.

### Langkah 4 · Struktur folder
```
CLAUDE.md                  peta singkat: tahapan, aturan dasar, peta skill, alat (≤ ±12 ribu karakter)
workflow/00-…md … NN-…md   satu panduan per tahap, dibaca per bagian
templates/                 prompt juri/generator, rubrik, template STATUS/evaluasi
.claude/agents/            agen penilai tanpa konteks (omitClaudeMd: true, alat dibatasi)
tools/                     skrip Python + tes_alat.py
skills/                    rujukan metode (lisensi dicatat di SUMBER.md)
proyek/_template/          STATUS.md (progres, keputusan, serah terima, log kuota), evaluasi.md, hasil.json
proyek/<nama>/             satu folder per lomba/tugas
catatan/                   buku-pelajaran.md, riwayat-workflow.md, audit, riset
```

### Langkah 5 · Bangun, mulai dari yang paling sering gagal
1. `CLAUDE.md` dan template `STATUS.md`.
2. Panduan tahap 0 dan alat cek kepatuhan.
3. Tahap seleksi ide/konsep beserta agen juri dan skrip agregasinya.
4. Tahap produksi, cek mesin, dan loop juri.
5. Tahap evaluasi.

Setiap skrip punya tes. Jalankan tesnya setiap kali skrip diubah.

### Langkah 6 · Uji coba pada satu kasus nyata
Jalankan seluruh workflow pada satu lomba sungguhan atau lomba lama, lalu catat setiap langkah yang dilewati, diubah, atau macet. Penyimpangan yang berulang adalah tanda workflow tidak cocok dengan kenyataan, bukan tanda agennya salah. Perbaiki, lalu tulis entri pertama di `catatan/riwayat-workflow.md`.

### Langkah 7 · Pemeliharaan
Setiap proyek selesai: retro proses → buku pelajaran → usulan → persetujuan → cadangkan file lama → ubah → catat versi dan hipotesisnya.

---

## Bagian 3 — Titik awal untuk jenis lomba lain

Ini titik awal untuk diuji, bukan aturan. Sesuaikan dengan rubrik dan aturan lomba yang sebenarnya (Langkah 2).

| Jenis | "Arena" (keputusan mahal di depan) | Cek mesin khusus | Persona juri | Risiko khusus |
|---|---|---|---|---|
| **Poster / infografis** | 3–5 arah konsep (pesan utama satu kalimat + gaya visual), dinilai juri buta dari **thumbnail kecil** ("terbaca dari jauh dalam 3 detik?") | ukuran px/cm dan DPI, format file, kontras warna (WCAG), jumlah kata, jumlah font, logo/identitas yang dilarang, setiap angka punya sumber | desainer, ahli bidang tema, orang awam yang lewat | gambar/ikon berhak cipta; teks di gambar AI salah eja; aturan pemakaian AI gambar |
| **Video dengan AI generatif** | logline + struktur cerita 3 babak, adu berpasangan; lalu storyboard per shot sebelum generate apa pun | durasi, rasio, resolusi, fps, kenyaringan audio (LUFS), subtitle, kredit/lisensi musik, label "dibuat dengan AI" kalau diwajibkan | sutradara/editor, juri tema, penonton yang menilai 5 detik pertama | konsistensi karakter antar-shot (catat prompt + seed per shot di file); kuota alat generate berbayar; wajah/suara orang nyata; musik tanpa lisensi |
| **Hackathon** | penemuan masalah (data/wawancara) → ide dinilai dengan bobot **kelayakan dalam 24–48 jam** yang besar → cakupan MVP satu alur demo | demo selalu jalan (tes otomatis tiap checkpoint jam), README, lisensi dependensi, aturan "kode dibuat selama acara" | juri teknis, juri bisnis/dampak, juri yang hanya melihat demo 3 menit | cakupan terlalu luas (kesalahan paling umum menurut juri); demo gagal saat live (siapkan video cadangan); kunci API terekspos |
| **Pitch / business plan** | masalah + segmen pengguna + bukti permintaan, lalu model bisnis; adu dua arah | angka keuangan konsisten antar-slide/lampiran, sumber setiap asumsi pasar, durasi pitch | investor, pakar industri, calon pengguna | angka pasar tanpa sumber; klaim traksi yang tidak bisa dibuktikan |
| **Lainnya** | tanyakan: keputusan apa yang paling mahal kalau salah? Itu yang diadu di depan | tanyakan: apa saja yang bisa dicek pasti oleh skrip? | ambil dari profil juri di aturan | tanyakan: apa yang membuat karya gugur? |

---

## Bagian 4 — Kesalahan yang pernah terjadi (cek sebelum workflow dipakai)

- [ ] Agen penilai tidak termuat di lingkungan tertentu (sesi cloud). Siapkan prompt juri utuh sebagai cadangan, dan catat kalau juri tidak dijamin buta.
- [ ] Subagent menjalankan alat yang tidak diminta (membuat scheduled task). Batasi alat agen penilai dan tulis "jangan memanggil alat apa pun" di prompt.
- [ ] Skor dari keluarga model berbeda tidak sebanding. Bandingkan dengan peringkat/persentil, dan catat model setiap juri.
- [ ] Gerbang lulus/gugur hampir tidak pernah menggugurkan. Jangan menganggap "lolos gerbang" sebagai bukti kebenaran.
- [ ] Median membuang ide yang memecah pendapat juri. Sediakan jalur "kartu liar".
- [ ] File proyek lain tercampur di folder kirim. Cek isi folder kirim sebelum mengirim.
- [ ] Satu karya tersimpan atas nama dua peserta. Satu karya untuk satu peserta.
- [ ] Alat pencarian kena batas (429) tanpa kunci API. Uji alat di awal, dan siapkan kunci atau jalur cadangan.
- [ ] Pola juara dari satu lomba diperlakukan sebagai pola umum. Pola juara hanya berlaku untuk lomba itu sendiri.
- [ ] Utas dibiarkan memanjang sampai ratusan ribu token. Ikuti prinsip 12, dan peringatkan manusia sebelum langkah boros.

---

## Bagian 5 — Kerangka `CLAUDE.md` awal

```markdown
# Workflow [nama] (umum, untuk [jenis tugas] apa pun)
Setiap proyek punya folder `proyek/<nama>/`. `<P>` = folder proyek yang sedang dikerjakan.

## Memulai proyek baru
1. Salin `proyek/_template/` → `proyek/<nama>/`, taruh aturan/guidebook di sana.
2. Baca `catatan/buku-pelajaran.md` § Aktif.
3. Tahap 0 → … → N. Setiap tahap: checkpoint, perbarui STATUS § Serah terima + § Log kuota.
4. Setelah kirim: evaluasi (retro proses), setelah pengumuman: retro hasil.

## Satu utas pendek per tahap
[aturan utas, baca seperlunya, peringatan boros + ambangnya]

## Aturan dasar
1. Aturan pemberi tugas > default workflow.
2. Jangan mengarang sumber/angka; penanda [PERLU SUMBER].
3. [aturan mutu khas bidang ini]

## Tahapan
| # | Tahap | Panduan | Hasil di `<P>/` |

## Peta skill per tahap
| Tahap · langkah | Skill & alat |

## Alat (`tools/`)
| Alat | Fungsi |

## Workflow yang memperbaiki diri
[evaluasi → buku pelajaran → usulan → persetujuan → riwayat; bug 1 kasus, strategi ≥3 hasil; pengaman tidak pernah dilonggarkan]
```

Contoh lengkap yang bisa dibaca Claude: folder workflow esai ini (`CLAUDE.md`, `workflow/`, `tools/arena.py`, `tools/evaluasi.py`, `catatan/buku-pelajaran.md`).
