# Folder persiapan untuk Antigravity

**Status (5 Nov 2026): dikerjakan.** Hasilnya `AGENTS.md` (ditulis ulang untuk workflow terbaru), `.agents/skills/esai-lomba/SKILL.md` (pintu masuk tipis, bukan 8 skill per tahap), dan `PINDAH-KE-ANTIGRAVITY.md`. Catatan di bawah adalah riset 28 Okt yang menjadi dasarnya; tabel skill akun di bawah sudah usang (lihat `CLAUDE.md` § Pemakaian skill).

Permintaan 28 Okt 2026: siapkan folder supaya Antigravity bisa menjalankan workflow ini. Ditunda atas permintaan penulis. Hasil riset yang sudah didapat:

## Cara Antigravity membaca instruksi
- **Rules** (dibaca otomatis): `AGENTS.md` atau `GEMINI.md` di akar folder, atau file di `.agents/rules/`. Batas **12.000 karakter per file**. (`CLAUDE.md` tidak dibaca otomatis; ukurannya sekarang ±9.600 karakter, jadi muat kalau disalin jadi `AGENTS.md`.)
- **Skills**: `.agents/skills/<nama>/SKILL.md` (per proyek) atau `~/.gemini/config/skills/` (global). Format sama dengan skill Claude: frontmatter `name` + `description`, boleh punya `scripts/`, `references/`, `assets/`.
- **Subagent**: ada di Antigravity CLI (agen kustom dengan `subagent: true`). Kalau tidak dipakai, juri Arena Ide dijalankan di percakapan baru.
- Sumber: https://codelabs.developers.google.com/getting-started-with-antigravity-skills dan https://thepromptshelf.dev/blog/google-antigravity-agents-md-rules-guide-2026

## Skill mana yang bisa dibawa
| Skill | Asal | Bisa disalin ke Antigravity? |
|---|---|---|
| docx, pdf, pptx, xlsx | Anthropic, lisensi proprietary (dilarang disalin/dipakai di luar layanan Anthropic) | **Tidak.** Pengganti: `tools/build_docx.py` (DOCX/PDF), `tools/baca_pdf.py` (baca PDF), python-pptx bila perlu slide |
| deep-research, docs, skill-creator, dll. | Bawaan Anthropic | Tidak; pakai `workflow/02-riset.md` + `tools/cari_sumber.py` |
| essay-lomba, review-essay-lomba, desain-sampul-essay, parafrase-akademik | Buatan penulis | Ya |
| stop-slop | Hardik Pandya, MIT | Ya, dengan LICENSE |
| naskah-id, advanced-evaluation, hallmark, impeccable | MIT / Apache 2.0, sudah di `skills/` | Ya (impeccable bahkan sudah menyediakan versi `.agents/skills/`) |
| Connector alphaXiv, Consensus, bioRxiv | Akun Claude | Tidak ikut; pakai `cari_sumber.py` |

## Rencana saat dilanjutkan
1. `AGENTS.md` = salinan `CLAUDE.md` yang disesuaikan (nama skill Antigravity, juri lewat percakapan baru/agen CLI).
2. `.agents/skills/` berisi 8 skill per tahap (pembungkus tipis yang menunjuk ke `workflow/0X-*.md`) + salinan skill yang boleh disalin.
3. `PINDAH-KE-ANTIGRAVITY.md`: panduan singkat untuk penulis.
4. Saran pemakaian: Arena Ide dan draf tetap di model terkuat; Antigravity/Gemini cocok sebagai juri kedua (beda model mengurangi bias swa-penilaian).
