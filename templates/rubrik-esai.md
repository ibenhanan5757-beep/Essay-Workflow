# Rubrik Juri Esai (Tahap 5) — lapis kedua

**Skor utama dan syarat berhenti memakai rubrik resmi lomba** (`<L>/aturan.md` § Rubrik penilaian, dengan bobot resmi). Lihat `workflow/05-review.md`. Rubrik di bawah ini lapis kedua: dipakai untuk mencari perbaikan yang membuat esai **lolos penyaringan di peringkat atas, lalu menang di rapat juri manusia**. Skornya tidak menentukan kapan loop berhenti.

## Gerbang (harus lulus semua; dicek mesin dan checklist)
- Patuh aturan: jumlah kata, format, larangan identitas, posisi gambar, gaya sitasi (`tools/cek_naskah.py`, `tools/build_docx.py`)
- Semua sumber nyata dan tidak ditarik (`tools/cari_sumber.py cek-pustaka`)
- Tidak ada fakta yang salah atau angka tanpa sumber

## Lapis 1 — Penyaring (40%)
Hal yang dinilai pembaca cepat atau AI penyaring.

| # | Kriteria | Bobot | 9 = |
|---|---|---|---|
| P1 | Bahasa | 10% | EYD V bersih, kalimat efektif, diksi tepat |
| P2 | Struktur & alur | 10% | Pendahuluan–isi–penutup runtut; setiap paragraf satu gagasan dengan transisi logis |
| P3 | Bukti & sitasi | 10% | Setiap klaim penting didukung data terbaru dari sumber kuat |
| P4 | Bebas jejak AI | 10% | Nol frasa klise, pola paragraf bervariasi, detail konkret |

## Lapis 2 — Juri manusia (60%)
Hal yang membuat juri memilih esai ini di rapat juri.

| # | Kriteria | Bobot | 9 = |
|---|---|---|---|
| H1 | Ide terasa cepat | 15% | Dalam ±100 kata pertama, juri sudah tahu idenya dan merasa "ini beda" |
| H2 | Momen "aha" | 15% | Ada bagian yang membuat juri melihat masalah dengan cara baru, dinyatakan jelas dan tidak terkubur |
| H3 | Bisa dibayangkan | 10% | Ada skenario/contoh konkret: siapa melakukan apa, di mana, langkah pertama |
| H4 | Tahan serangan | 10% | Keberatan terkuat dijawab di dalam esai sebelum juri sempat menanyakannya |
| H5 | Kredibilitas ahli | 5% | Tidak ada satu pun "alarm" bagi juri ahli bidang (istilah, mekanisme, regulasi) |
| H6 | Melekat | 5% | Nama/frasa ide konsisten dan judul serta penutup membuat esai diingat |

Gunakan jangkar: 2 = lemah, 5 = rata-rata esai lomba, 9 = yang terbaik di tumpukan. Skor ≥8 wajib disertai kutipan yang membuktikannya.

## Pemeriksaan wajib juri
1. **Uji 30 detik:** baca judul + paragraf pertama saja, lalu catat kesan (biasa / lumayan / berhenti dan tertarik) sebelum membaca sisanya.
2. **Ringkasan satu kalimat:** kalau juri tidak bisa meringkas ide esai dalam satu kalimat setelah membacanya, H1 maksimal 4.
3. **Pertanyaan pembela:** "Kalimat apa yang akan kamu ucapkan untuk membela esai ini di rapat juri?" Kalau jawabannya generik ("bahasanya bagus"), lapis 2 bermasalah.

## Hubungan dengan rubrik resmi
Rubrik resmi lomba dinilai lebih dulu, dengan bobot resmi. Bobot resmi itulah yang dipakai untuk skor total dan syarat berhenti (tidak ada kriteria resmi < 7). Bobot di atas hanya untuk mengurutkan perbaikan lapis kedua. Kalau perbaikan lapis kedua menurunkan skor salah satu kriteria resmi, utamakan kriteria resmi.
