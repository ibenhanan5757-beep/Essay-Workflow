# Workflow Esai Lomba — Cara Pakai

Satu workflow untuk semua lomba esai. Setiap lomba punya folder sendiri.

**Pertama kali di Windows?** Pasang Python dan paketnya dulu: [`MULAI-DI-WINDOWS.md`](MULAI-DI-WINDOWS.md). Istilah yang asing (CARS, K1–K7, peta klaim, dll.) dijelaskan di [`ISTILAH.md`](ISTILAH.md).

## Lomba baru
1. Buka folder ini di Claude (Desktop/Code/Cowork) dan bilang, misalnya: *"Lomba baru: [nama lomba], guidebook-nya ini"* sambil melampirkan PDF-nya.
2. Claude membuat `lomba/<nama-lomba>/` dari `lomba/_template/` lalu menjalankan **tahap 0**: membedah guidebook dan membuat profil format. Workflow ini untuk esai 100% AI: Claude yang menulis, kamu yang mengarahkan dan menyetujui.
3. Lanjutkan dengan *"lanjut tahap berikutnya"*. Setiap tahap berhenti di checkpoint untuk kamu setujui.

## Berapa lama?
Jalur penuh: sekitar 5–10 jam kerja Claude, tersebar dalam 2–4 hari kalender, ditambah waktumu membaca di setiap checkpoint. Rincian per tahap ada di `workflow/00-dekonstruksi-lomba.md` § Garis waktu. Kalau tenggat tinggal ≤ 5 hari, Claude menawarkan **Mode Kilat** (`workflow/MODE-KILAT.md`). Mode ini lebih cepat, tapi ide dipilih dari satu putaran saja. Jalur penuh tetap default.

## Melanjutkan
*"Lanjutkan lomba [nama]"*: Claude membaca `lomba/<nama>/STATUS.md` dan meneruskan dari tahap terakhir.

## Isi folder
```
CLAUDE.md            aturan & alur utama (dibaca Claude)
README.md            file ini
MULAI-DI-WINDOWS.md  pasang Python, paket, PDF; kalau macet
ISTILAH.md           daftar istilah
PENJELASAN-WORKFLOW.md  penjelasan lengkap untuk manusia
workflow/            panduan tahap 0–8 + MODE-KILAT.md
tools/               cari & verifikasi jurnal, cek naskah, cek klaim, hitung arena, build DOCX/PDF, tes
templates/           log sumber + peta klaim, rubrik, format review, prompt juri & auditor
.claude/agents/      juri buta (tanpa CLAUDE.md, tanpa akses file)
lomba/_template/     kerangka folder untuk lomba baru
lomba/<nama>/        satu folder per lomba: guidebook, aturan, profil, status, ide, riset, draf, kirim
lomba/ewc-siswa-pharfest-2026/  contoh hasil tahap 0 (tidak ikut di GitHub)
catatan/             kritik SOP juara, audit, catatan perubahan
skills/              rujukan dari repo luar per kegunaan: esai/, desain/, presentasi/ (+ SUMBER.md)
arsip/               file lama yang sudah tidak dipakai (lihat arsip/README.md)
```

Folder `arsip/` (termasuk `skill-desain.zip`), semua PDF (termasuk guidebook), dan folder lomba selain `_template` tidak ikut di GitHub (lihat `.gitignore`). Cara memasang skill desain ada di `skills/CARA-PASANG-SKILL-DESAIN.md`; sumber dan lisensinya ada di `skills/SUMBER.md` dan `skills/CARA-PASANG-SKILL-DESAIN.md`.
