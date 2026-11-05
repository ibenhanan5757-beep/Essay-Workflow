# Tahap 8 — Evaluasi & Perbaikan Workflow

Setiap lomba punya foldernya sendiri, tapi workflow-nya dipakai bersama. Tahap ini menghubungkan keduanya: **apa yang terjadi di satu lomba menjadi bahan perbaikan untuk lomba berikutnya.** Tanpa tahap ini, semua desain Arena Ide (bobot "wow" 45%, persona juri, kartu liar, paket esai) tetap hipotesis yang tidak pernah diuji.

Lingkarannya:

```
lomba N selesai ─► 8a retro proses ─► 8b retro hasil (setelah pengumuman)
                         │                    │
                         ▼                    ▼
                 catatan/buku-pelajaran.md ◄──┘   catatan/bank-juara.md
                         │
                         ▼
                 8c tinjauan workflow ─► usulan ─► penulis setuju ─► file workflow diubah
                         │                                          └► catatan/riwayat-workflow.md
                         ▼
lomba N+1: tahap 0 membaca pelajaran aktif + bank juara ─► ... ─► 8a ...
```

| Langkah | Kapan | Hasil |
|---|---|---|
| **8a Retro proses** | segera setelah naskah dikirim, atau setelah memutuskan tidak mengirim | `<L>/evaluasi.md` § 8a, `<L>/hasil.json` (sebagian), pelajaran kandidat |
| **8b Retro hasil** | setelah pengumuman pemenang | `<L>/evaluasi.md` § 8b, `hasil.json` lengkap, `catatan/bank-juara.md` |
| **8c Tinjauan workflow** | setelah 8a atau 8b; tinjauan besar setiap ada 3 lomba baru dengan hasil diketahui | `catatan/buku-pelajaran.md`, usulan perubahan, `catatan/riwayat-workflow.md` |

Hemat kuota: 8a dikerjakan di ujung utas terakhir lomba itu, sedangkan 8b dan 8c di utas baru yang pendek dan dimulai dari `<L>/evaluasi.md`. Tidak ada subagent di 8a. Di 8b hanya ada 2 panggilan (uji balik).

---

## 8a — Retro proses (segera setelah kirim)

Salin `lomba/_template/evaluasi.md` dan `lomba/_template/hasil.json` ke `<L>/` kalau belum ada.

1. **Statistik juri**: jalankan `python tools/evaluasi.py juri <L>` dan tempel hasilnya ke § 8a. Angka ini mencakup kesepakatan antarjuri, persentase gugur gerbang, posisi kartu jangkar, dan apakah panel final sama dengan juara adu.
2. **Penyimpangan dari workflow**: setiap langkah yang dilewati, dipangkas, atau diganti, lengkap dengan alasan dan akibatnya. Sumbernya `STATUS.md` § Catatan keputusan, `ide/`, dan `draf/review-vN.md`. Penyimpangan bukan kesalahan, tapi pola penyimpangan yang berulang adalah tanda workflow tidak cocok dengan kenyataan.
3. **Hambatan**: alat yang error, prompt yang membuat subagent berbuat aneh, aturan guidebook yang ambigu, dan langkah yang paling banyak memakan waktu atau kuota. Sumber kuota adalah `STATUS.md` § Log kuota, yang diisi dari `get_usage` di setiap checkpoint (CLAUDE.md § Satu utas pendek per tahap). Ringkas di tabel kuota § 8a: kenaikan limit 5 jam per tahap, utas terbesar, subagent per tahap, dan apakah limit pernah habis.
4. **Pilihan penulis**: rekomendasi Arena dibandingkan dengan ide yang dipilih penulis, beserta alasan penulis kalau ia memilih lain. Kalau penulis sering memilih di luar rekomendasi, juri AI atau rubriknya yang perlu dicek, bukan penulisnya.
5. **Isi `hasil.json`**: semua kolom yang sudah diketahui. Kolom yang belum diketahui dibiarkan `null`.
6. **Pelajaran kandidat** (1–5 baris): *Kejadian → Dugaan sebab → Usulan → Jenis* (bug / proses / hipotesis / risiko).
7. **Tanggal pengumuman**: salin dari `aturan.md` ke `STATUS.md`. Kalau penulis mau, tawarkan pengingat terjadwal di tanggal itu untuk menjalankan 8b.

Jangan mengarang. Yang tidak tercatat ditulis "tidak tercatat".

## 8b — Retro hasil (setelah pengumuman)

Penulis memberi tahu hasilnya, atau Claude mencari pengumumannya di web/Instagram panitia kalau penulis meminta.

1. **Hasil sendiri**: status (`juara` / `finalis` / `tidak lolos` / `tidak dikirim`), peringkat, jumlah peserta kalau diketahui, skor atau komentar juri kalau ada (dikutip persis, dengan sumbernya).
2. **Juara lomba ini**: judul, inti ide, dan abstrak kalau ada, beserta link pengumuman. Salin ke `catatan/bank-juara.md`. Judul juara tidak boleh dikarang. Kalau tidak bisa diverifikasi, tulis "tidak ditemukan".
3. **Apakah juara mirip ide kita?** Tulis setiap juara sebagai kartu `### W01. Judul` di `<L>/evaluasi.md`, lalu jalankan `python tools/arena.py mirip <L>/evaluasi.md <L>/ide/loop-*.md`. Dari sini muncul tiga kemungkinan:
   - Juara mirip ide kita yang **gugur atau berperingkat rendah**: ini bukti terkuat bahwa juri AI salah menilai. Catat skornya.
   - Juara mirip **ide pasaran atau prediksi** kita: berarti juri manusia lomba ini menghargai ide yang aman, dan bobot K1 Kejutan mungkin terlalu tinggi untuk lomba sejenis.
   - Juara **tidak mirip apa pun**: catat sudutnya, karena ini sudut yang tidak dijangkau generator.
4. **Uji balik** (2 panggilan subagent `juri-ide`, kalau abstrak juara tersedia dan esai kita tidak juara 1): ide kita dan ide juara 1, keduanya ditulis sebagai kartu bersih dengan format dan panjang sama, diadu dua arah dengan `templates/prompt-ide-adu.md` (versi kartu). Isi `uji_balik.juri_ai_pilih_juara_asli`: `true` kalau kedua urutan memilih juara asli, `false` kalau kedua urutan memilih ide kita, dan `null` kalau hasilnya seri. Kalau esai kita juara 1, adu melawan juara 2. Setelah beberapa lomba, angka ini menunjukkan seberapa jauh juri AI bisa dipercaya.
5. **Rubrik resmi**: dari komentar atau skor juri, kriteria mana yang kemungkinan menentukan hasil. Bandingkan dengan skor juri AI di `draf/review-vN.md` terakhir.
6. Tambahkan pelajaran kandidat baru.

Satu hasil tidak membuktikan apa pun. Kalah atau menang di satu lomba bisa karena faktor yang tidak terlihat (jumlah peserta, selera satu juri, presentasi). Karena itu 8b mengumpulkan data, sedangkan keputusan mengubah strategi baru dibuat di 8c.

## 8c — Tinjauan workflow

### Masukkan pelajaran ke buku
Setiap pelajaran kandidat dari 8a/8b dimasukkan ke `catatan/buku-pelajaran.md`:
- Kalau pelajaran yang sama sudah ada, **jangan buat baris baru**. Tambahkan nama lomba ke kolom bukti dan naikkan hitungan lombanya.
- Kalau belum ada, buat baris baru dengan ID berikutnya (`PL12`, ...) dan status `usulan`.

### Kapan pelajaran boleh mengubah workflow

| Jenis | Contoh | Bukti minimal |
|---|---|---|
| **Bug** | alat crash, aturan saling bertabrakan, langkah tidak bisa dijalankan di lingkungan tertentu | 1 lomba |
| **Proses** | langkah terlalu mahal, urutan membingungkan, template kurang kolom | 1 lomba kalau sebabnya jelas, 2 lomba kalau tidak |
| **Risiko** | aturan orisinalitas, diskualifikasi, kebocoran identitas | 1 lomba (pengaman boleh diperketat kapan saja) |
| **Hipotesis strategi** | bobot rubrik ide, persona juri, panjang Arena, apa yang membuat menang | **≥3 lomba dengan hasil diketahui** yang mengarah sama, atau uji balik yang konsisten. `evaluasi.py rekap` memberi peringatan kalau datanya belum cukup. |

Alasan aturan ini: SOP yang menyesuaikan diri dengan satu lomba menjadi *overfit* (`catatan/kritik-sop-juara.md` § 1). Satu kemenangan bisa membuat strategi buruk terlihat benar, dan satu kekalahan bisa membuat strategi baik terlihat salah.

**Yang tidak pernah dilonggarkan oleh evaluasi**: larangan mengarang sumber/angka, peta klaim, auditor sitasi, checkpoint penulis, rubrik resmi sebagai skor utama, dan peringatan aturan AI/orisinalitas di tahap 0. Evaluasi boleh memperketat pengaman, tidak boleh melonggarkannya.

### Cara mengubah workflow
1. Claude menulis usulan ke penulis, berisi: file yang diubah, isi perubahannya, pelajaran yang mendasarinya (ID), **hipotesis** (apa yang diharapkan membaik), dan **cara mengujinya** di lomba berikutnya (kolom `hasil.json` atau angka `evaluasi.py` mana yang akan dilihat).
2. Penulis menyetujui, mengubah, atau menolak. Usulan yang ditolak tetap dicatat (status `ditolak`, beserta alasannya), supaya tidak diusulkan ulang tanpa bukti baru.
3. **Cadangkan dulu**: salin file yang akan diubah ke `arsip/versi-<tanggal>/` dengan struktur folder yang sama. Kalau folder ini sudah menjadi repo git, commit sudah cukup.
4. Ubah file. Kalau ada alat yang diubah, jalankan `python tools/tes_alat.py`.
5. Catat di `catatan/riwayat-workflow.md` (tanggal, ringkasan, file, pelajaran, hipotesis, cara uji). Untuk perubahan besar, tulis rinciannya di `catatan/perubahan-<tanggal>.md`.
6. Ubah status pelajaran menjadi `diterapkan (<tanggal>)`, lalu isi `versi_workflow` di `hasil.json` lomba berikutnya dengan tanggal itu.

### Tinjauan besar (setiap 3 lomba baru dengan hasil diketahui)
1. Jalankan `python tools/evaluasi.py rekap`.
2. Untuk setiap hipotesis di `riwayat-workflow.md` yang berstatus `menunggu uji`, tentukan apakah hipotesis itu **terbukti**, **tidak terbukti**, atau **belum cukup data**. Hipotesis yang tidak terbukti dikembalikan dari cadangan atau diganti, setelah penulis setuju.
3. Pelajaran berstatus `usulan` yang buktinya sudah cukup diajukan ke penulis.
4. Pelajaran yang tidak muncul lagi di 3 lomba terakhir dan tidak lagi relevan diberi status `arsip`.
5. Tulis ringkasan tinjauan di `catatan/riwayat-workflow.md`.

## Di awal lomba baru
Tahap 0 membaca `catatan/buku-pelajaran.md` § Aktif (status `diterapkan` atau `usulan` dengan jenis risiko/proses), lalu `catatan/bank-juara.md` untuk bidang dan jenjang yang sama. Bank juara dipakai sebagai bahan `ide/pasaran.md` dan kartu jangkar, tetap dengan link sumbernya.

## Checkpoint
- **8a**: tunjukkan ke penulis penyimpangan, hambatan, dan pelajaran kandidat.
- **8b**: tunjukkan hasil, juara, hasil cek kemiripan, dan uji balik.
- **8c**: tunjukkan usulan perubahan. **Tidak ada file workflow yang diubah tanpa persetujuan penulis.**
