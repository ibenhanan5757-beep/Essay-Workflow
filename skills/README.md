# Folder `skills/`

Rujukan dari repo luar yang dipakai workflow esai, **dikelompokkan per kegunaan**. Semua isi folder ini adalah skill folder yang sah (lihat `CLAUDE.md` § Pemakaian skill). Sumber, commit, dan lisensi setiap folder ada di `SUMBER.md`.

```
skills/
├── esai/          isi esai: ide, riset, argumen, bahasa, desain juri (tahap 1–6)
│   ├── academic-research-skills/   kualitas tulisan, CARS, CER, tangga klaim, Sokratik, sesat pikir, hierarki sumber, devil's advocate
│   ├── ai-research-skills/         brainstorming ide riset, berpikir kreatif (lensa Arena Ide)
│   ├── advanced-evaluation/        desain juri LLM: alasan dulu, tukar posisi, seri, bias panjang
│   └── naskah-id/                  EYD V, KBBI, kalimat efektif, pola AI + scripts/periksa.py
├── desain/        visual: grafik, diagram, sampul, poster, gaya slide (tahap 3b, 4, 7, 7C)
│   ├── hallmark/                   anti-"desain AI", palet, data-viz, lantai visual
│   ├── impeccable/                 critique, polish, typeset, layout, audit (termasuk kontras)
│   ├── design-md-referensi/        84 contoh DESIGN.md
│   └── design/, design-system/, brand/, banner-design/, ui-styling/, ui-ux-pro-max/   (satu keluarga, lihat catatan)
└── presentasi/    slide (tahap 7C, hanya kalau penulis meminta PPT)
    └── slides/
```

## Cara pakai

- **Sebagai rujukan (default).** Panduan di `workflow/` menyebut file di sini dengan path lengkap, misalnya `skills/esai/naskah-id/references/kata-baku.md`. Claude membacanya saat langkah itu dikerjakan. Tidak perlu pemasangan.
- **Sebagai skill yang bisa dipanggil langsung** (hanya untuk skill desain dan slide): pasang ke `.claude/skills/` mengikuti `CARA-PASANG-SKILL-DESAIN.md`. Di `.claude/skills/`, folder skill harus **sejajar tanpa folder kelompok** (`.claude/skills/hallmark/`, bukan `.claude/skills/desain/hallmark/`).

**Catatan keluarga ui-ux-pro-max.** `design`, `design-system`, `brand`, `banner-design`, `ui-styling`, `ui-ux-pro-max` (di `desain/`) dan `slides` (di `presentasi/`) berasal dari satu repo dan saling memanggil sebagai folder tetangga (misalnya `slides` menjalankan `../design-system/scripts/search-slides.py`). Pengelompokan di sini hanya untuk penyimpanan. Kalau dipasang ke `.claude/skills/`, pasang ketujuhnya bersama dan sejajar.

## Menambah skill baru

Ikuti `CLAUDE.md` § Pemakaian skill langkah 4: laporkan kandidat ke penulis, dan setelah disetujui salin ke kelompok yang sesuai (`esai/`, `desain/`, atau `presentasi/`), catat di `SUMBER.md`, lalu tambahkan ke Peta Skill. Kalau tidak cocok dengan tiga kelompok itu, buat kelompok baru dengan nama kegunaannya dan tambahkan ke bagan di atas.

Skill lain di luar folder ini: `lomba-ig/SKILL.md` (pra-tahap 0, rekap lomba dari bookmark Instagram) dan agen juri di `.claude/agents/`.
