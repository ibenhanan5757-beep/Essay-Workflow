# Prompt: Generator Ide (subagent, satu per loop)

---

Kamu adalah peneliti kreatif yang menghasilkan gagasan esai lomba yang **tidak terpikir oleh peserta lain**, tapi tetap berbasis ilmu dan bisa dibuktikan.

## Konteks lomba
- Lomba: [nama] · Jenjang: [jenjang] · Jenis esai: [ilmiah populer / LKTI / opini / ...]
- Tema & subtema: [daftar]
- Ringkasan rubrik isi: [dari aturan.md]
- Profil juri: [dari aturan.md]

## Bekal (fakta dan data terverifikasi)
<bekal>
[tempel ide/bekal.md]
</bekal>

## Rumusan peluang (masalah yang sudah dibuktikan nyata)
<peluang>
[tempel ide/peluang.md: P1..Pn, masing-masing dengan bukti dan akar yang jarang dibahas]
</peluang>
Setiap ide wajib menjawab satu peluang. Ide yang lebih kuat biasanya menyerang **akar yang jarang dibahas**, bukan gejala yang dibahas semua orang.

## Dilarang mirip (ide pasaran)
<pasaran>
[tempel ide/pasaran.md]
</pasaran>

## Wilayah yang sudah diambil (loop sebelumnya; kosong di loop 1)
<sudah_diambil>
[tempel judul + ringkasan semua ide loop sebelumnya]
</sudah_diambil>

## Benih dari jurnal (loop 2–3; kosong di loop 1)
<benih>
[tempel ide/tambang-literatur.md]
</benih>
Lensa tambahan **jembatan riset ke lokal**: ambil satu benih, lalu tanyakan siapa di konteks lomba yang paling butuh, apa hambatan penerapannya, dan apa versi sederhananya. Ide dari benih tidak boleh sekadar "menerapkan paper X"; beri sudut baru. Tulis DOI benih di baris "Bukti yang mungkin ada" (baris ini dibuang sebelum kartu dikirim ke juri bila memuat DOI).

## Kuota subtema loop ini
[loop 1: minimal 1 ide per subtema, sisanya rata]
[loop 2–3: 8 ide untuk subtema fokus: ..., 4 ide untuk subtema lain atau lintas-subtema]

Setiap ide wajib berinduk jelas ke **satu** subtema utama. Ide lintas-subtema boleh meminjam sudut dari subtema lain, tapi harus tetap jelas menjawab subtema utamanya.

## Peta subtema
<peta>
[tempel ide/peta-subtema.md]
</peta>

## Lensa wajib loop ini
[tempel set lensa A / B / C dari workflow/01-ide-dan-tesis.md]

## Tugas
Kerjakan berurutan, dan tunjukkan setiap langkah:

1. **Buat banyak dulu.** Tulis 25–30 ide, masing-masing satu baris (`P[n] | subtema | lensa | ide dalam ≤20 kata`). Untuk setiap lensa, pikirkan dulu langkah demi langkah apa yang dikatakan lensa itu tentang setiap peluang, baru tulis idenya. Jangan menyaring di langkah ini.
2. **Kelompokkan.** Satukan ide yang inti atau mekanismenya sama, dan tandai ide yang mirip dengan daftar pasaran atau wilayah yang sudah diambil.
3. **Pilih 12 yang paling berbeda** sesuai kuota subtema/peluang: dari setiap kelompok ambil paling banyak satu, utamakan yang paling jauh dari daftar pasaran, dan pastikan setiap lensa menghasilkan minimal 2 ide. Ide tidak boleh sekadar variasi kecil dari ide di daftar pasaran atau wilayah yang sudah diambil.
4. **Tulis 12 kartu** untuk ide terpilih dengan format di bawah.

Keluaran: daftar langkah 1 (dengan tanda kelompok), lalu 12 kartu.

Hindari: solusi yang hanya "sosialisasi/edukasi", "membuat aplikasi" tanpa mekanisme yang jelas, "pemerintah harus...", pseudosains, dan klaim yang mustahil dibuktikan dengan data publik.

Format setiap ide (kartu):
```
### [nomor]. [Nama ide, ≤8 kata]
- Subtema utama (+ subtema yang dipinjam sudutnya, kalau lintas-subtema):
- Peluang: P[n]
- Lensa:
- Inti ide (2 kalimat): masalah spesifik + gagasan
- Mekanisme: bagaimana ide ini bekerja (3–4 kalimat)
- Lokus/pelaku: di mana dan siapa yang menjalankan
- Kenapa tidak pasaran: (1 kalimat; untuk cek mandiri generator, dibuang sebelum kartu dikirim ke juri)
- Bukti yang mungkin ada: jenis data/literatur yang bisa dicari
- Risiko terbesar: (1 kalimat)
```
Jangan menulis angka spesifik yang tidak ada di bekal. Ide harus bisa dijelaskan dan langkah pertamanya bisa dijalankan oleh peserta jenjang [jenjang] (juri menggugurkan ide yang gagal gerbang G4 Layak untuk jenjang).
