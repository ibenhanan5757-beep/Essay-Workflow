# Daftar Istilah

Istilah dan singkatan yang dipakai di `workflow/`, `templates/`, dan `tools/`, diurutkan menurut abjad.

| Istilah | Arti | Dipakai di |
|---|---|---|
| **Adu berpasangan** | Dua ide atau dua versi naskah dibandingkan langsung oleh juri. Setiap pasangan dijalankan dua kali dengan posisi ditukar. Kalau hasil kedua urutan tidak sepakat, dianggap seri. | tahap 1 final, tahap 5 |
| **Agen proyek** | Definisi subagent di `.claude/agents/` (`juri-ide`, `juri-esai`, `auditor-sitasi`). Berjalan tanpa CLAUDE.md dan tanpa alat baca file, supaya juri benar-benar buta. | tahap 1, 5 |
| **APA 7** | Gaya sitasi American Psychological Association edisi 7: (Penulis, Tahun) di teks, daftar pustaka urut abjad. | tahap 4, 6 |
| **Arena Ide** | Tahap 1: ide dibuat dan diadu habis-habisan sebelum esai ditulis. | `workflow/01` |
| **Auditor sitasi** | Subagent yang hanya menerima pasangan (kalimat naskah, kutipan sumber), lalu menilai: mendukung / sebagian / tidak mendukung. | tahap 5 |
| **Bekal** | Kumpulan fakta dan data per subtema untuk generator ide (`ide/bekal.md`). | tahap 1 |
| **CARS** | *Create a Research Space*: pola pendahuluan tiga langkah, yaitu bangun wilayah, tunjukkan celah, lalu isi celah dengan tesis. | `workflow/03` |
| **CER** | *Claim–Evidence–Reasoning*: rantai klaim → bukti → penalaran untuk setiap argumen. | `workflow/03` |
| **Checkpoint** | Titik di akhir setiap tahap ketika Claude berhenti, menunjukkan hasil, dan menunggu persetujuan penulis. | semua tahap |
| **Connector** | Sambungan akun Claude ke layanan luar (misalnya Consensus, SciSpace). Yang boleh dipakai ada di daftar izin `CLAUDE.md` § Pemakaian skill. | Peta Skill |
| **Devil's advocate (DA)** | Juri yang tugasnya hanya mencari kelemahan. Temuan Kritis/Mayor-nya harus dikonfirmasi juri lain. | tahap 5 |
| **DOI** | *Digital Object Identifier*, kode unik artikel ilmiah (`10.xxxx/...`), dicek dengan `cari_sumber.py doi`. | tahap 2, 5 |
| **Dossier** | Ringkasan bukti per pertanyaan riset (`riset/dossier.md`). Isinya tulisan sendiri, bukan teks sumber. | tahap 2 |
| **EYD V / KBBI** | Ejaan yang Disempurnakan edisi V dan Kamus Besar Bahasa Indonesia, acuan bahasa baku. | tahap 4 |
| **G1–G4** | Gerbang rubrik ide: tepat tema, benar secara ilmiah, aman/etis, layak untuk jenjang. Gagal satu = gugur. | `templates/rubrik-ide.md` |
| **H1–H6** | Kriteria lapis "juri manusia" di rubrik esai lapis kedua: ide terasa cepat, momen aha, bisa dibayangkan, tahan serangan, kredibilitas ahli, melekat. | `templates/rubrik-esai.md` |
| **Ide pasaran** | Ide yang paling mungkin ditulis banyak peserta, dari judul juara sungguhan atau prediksi berlabel. Dipakai sebagai anti-referensi. | tahap 1 |
| **Juri buta** | Juri yang tidak tahu proses penulisan dan tidak tahu ide mana dari mana. Kartu sudah dibersihkan, urutan diacak, label netral. | tahap 1, 5 |
| **K1–K7** | Kriteria skor rubrik ide: kejutan, reframing, bisa dibayangkan, daya bela, tahan serangan, kelayakan, bisa dibuktikan. | `templates/rubrik-ide.md` |
| **Kesan 30 detik** | Reaksi pertama juri (biasa / lumayan / berhenti) dari nama + inti ide saja, dijalankan sebagai panggilan terpisah. | tahap 1 |
| **Kritis / Mayor / Minor** | Tingkat temuan review menurut dampaknya ke penilaian juri. | tahap 5 |
| **LKTI** | Lomba Karya Tulis Ilmiah: lebih teknis daripada esai, sering menuntut metode dan data. | semua |
| **Median** | Nilai tengah dari skor beberapa juri, dihitung `arena.py`. Lebih tahan terhadap satu juri yang ekstrem dibanding rata-rata. | tahap 1 |
| **Mode Kilat** | Jalur dipangkas untuk tenggat ≤ 5 hari. Bukan default. | `workflow/MODE-KILAT.md` |
| **P1–P4** | Kriteria lapis "penyaring" di rubrik esai lapis kedua: bahasa, struktur, bukti & sitasi, bebas jejak AI. | `templates/rubrik-esai.md` |
| **Peta klaim** | Tabel di `riset/sumber.md`: setiap klaim faktual dengan ID (K1, K2, ...), kutipan verbatim sumber, halaman, dan status. Draf hanya boleh memakai klaim ✅. | tahap 2, 4, 5 |
| **Peta Skill** | Tabel di CLAUDE.md yang memasangkan setiap langkah dengan skill dan rujukan folder. | CLAUDE.md |
| **`[PERLU ...]`** | Penanda klaim yang belum punya sumber/data: `[PERLU SUMBER]`, `[PERLU DATA: ...]`, `[PERLU RUJUKAN: ...]`. Build ditolak selama masih ada. | tahap 2, 4, 6 |
| **Preprint** | Artikel yang belum melewati peer-review (arXiv, bioRxiv, SSRN). Bukti lemah, jadi kutip versi jurnalnya kalau sudah terbit. | tahap 2 |
| **Profil (`profil.json`)** | Aturan format lomba (kertas, font, margin, batas kata) yang dibaca `build_docx.py` dan `cek_naskah.py`. | tahap 0, 6 |
| **Retraksi** | Paper yang ditarik penerbit karena salah atau curang. Dilarang dikutip. | tahap 2, 5 |
| **Rubrik resmi** | Kriteria dan bobot penilaian dari guidebook, dipakai sebagai skor utama dan syarat berhenti tahap 5. | `<L>/aturan.md` |
| **Seed** | Angka yang membuat pengacakan bisa diulang persis (`arena.py acak --seed`). | tahap 1 |
| **Skill** | Paket instruksi untuk satu jenis tugas: skill akun, skill proyek, atau rujukan di `skills/`. | CLAUDE.md § Pemakaian skill |
| **Slop / anti-slop** | Pola tulisan khas AI yang klise atau kosong, dan cara menghindarinya. | `workflow/04`, `tools/frasa_slop.txt` |
| **Subagent** | Claude kedua yang dijalankan di konteks baru oleh Claude utama (alat Agent). | tahap 1, 5 |
| **Tangga klaim** | Urutan kekuatan kata kerja klaim, dari "mungkin menunjukkan" sampai "menyebabkan". Klaim tidak boleh lebih kuat dari buktinya. | `workflow/05` |
| **Uji 30 detik** | Lihat *Kesan 30 detik*. Di tahap 5: juri membaca judul + paragraf pertama dulu sebelum seluruh naskah. | tahap 1, 5 |
