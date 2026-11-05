---
name: esai-lomba
description: Menjalankan atau melanjutkan workflow esai lomba di folder ini (tahap 0 bedah guidebook, 1 Arena Ide dengan juri buta subagent, 2 riset dan peta klaim, 3 kerangka, 4 draf, 5 loop juri, 6 build DOCX/PDF, 7 visual/PPT, 8 evaluasi). Pakai setiap kali penulis memberi guidebook/juknis lomba esai, meminta "lanjutkan lomba <nama>", atau menyebut tahap workflow ini.
---

# Workflow esai lomba (pintu masuk untuk Antigravity)

Skill ini hanya penunjuk. Isi workflow ada di file proyek; jangan meringkas atau mengganti isinya dari ingatan.

1. Baca `AGENTS.md` (terjemahan bagian khusus Claude Code) dan `CLAUDE.md` (aturan lengkap). **Aturan berhenti** (`AGENTS.md` § 0) berlaku di setiap langkah: kerjakan persis seperti panduan, atau berhenti dan lapor dengan format `⛔ BERHENTI`. Jangan pernah mengganti langkah dengan cara lain tanpa persetujuan penulis.
2. Lomba baru: ikuti `CLAUDE.md` § Memulai lomba baru. Lomba lama: baca `lomba/<nama>/STATUS.md` § Serah terima, lalu hanya berkas yang disebut di sana.
3. Buka panduan tahap yang sedang dikerjakan:

| Tahap | Panduan |
|---|---|
| 0 | `workflow/00-dekonstruksi-lomba.md` (+ `workflow/MODE-KILAT.md` kalau tenggat ≤ 5 hari) |
| 1 | `workflow/01-ide-dan-tesis.md` (percakapan 1A, 1B, 1C) |
| 2 | `workflow/02-riset.md` |
| 3, 3b | `workflow/03-kerangka.md`, `workflow/03b-rencana-visual.md` |
| 4 | `workflow/04-menulis-draf.md` |
| 5 | `workflow/05-review.md` + `templates/prompt-juri.md` |
| 6 | `workflow/06-revisi-final.md` |
| 7, 7C | `workflow/07-sampul-poster.md`, `workflow/07c-presentasi.md` (7C hanya atas permintaan) |
| 8 | `workflow/08-evaluasi.md` |

4. Juri selalu subagent terpisah, dibuat dengan `define_subagent` lalu dipanggil dengan `invoke_subagent` (lihat `AGENTS.md` § 2). Satu juri = satu panggilan.
5. Akhiri setiap tahap di checkpoint: tunjukkan hasil beserta daftar periksa langkah (setiap langkah dengan path file buktinya), tunggu persetujuan, lalu perbarui `STATUS.md` § Serah terima.
