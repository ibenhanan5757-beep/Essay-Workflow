# Sumber skill

File di folder ini disalin apa adanya (bahasa Inggris) dari tiga repo publik sebagai bahan rujukan. Panduan berbahasa Indonesia di `workflow/` adalah adaptasi ringkasnya untuk essay lomba.

| Folder | Repo | Commit | Lisensi | Yang diambil |
|--------|------|--------|---------|--------------|
| `esai/academic-research-skills/` | https://github.com/Imbad0202/academic-research-skills | b8d050f | CC BY-NC 4.0 (© Cheng-I Wu), hanya untuk penggunaan non-komersial dengan atribusi | Pemeriksaan kualitas tulisan, retorika pendahuluan & judul (CARS), penyusun argumen (CER), tangga kekuatan klaim, pertanyaan Sokratik, katalog sesat pikir, hierarki kualitas sumber, reviewer devil's advocate |
| `esai/ai-research-skills/` | https://github.com/Orchestra-Research/AI-Research-SKILLs | 773a529 | MIT | Kerangka brainstorming ide riset dan berpikir kreatif |
| `desain/hallmark/` | https://github.com/Nutlope/hallmark | 6033bab → 65b5e40 | MIT | v2.0.0; salinannya juga ada di `arsip/skill-desain.zip`. Jangan dihapus: panduan membacanya sebagai rujukan. |

Yang sengaja tidak diambil: pipeline jurnal 10 tahap lengkap, skrip Python/Node, alat systematic review, dan skill ML/infrastruktur. Semuanya terlalu berat atau tidak relevan untuk satu essay lomba.

## Tambahan (pemetaan skill per tahap)

| Folder | Repo | Commit | Lisensi | Yang diambil |
|--------|------|--------|---------|--------------|
| `esai/naskah-id/` | https://github.com/nothinx/naskah-id | e18d574 | MIT (© 2026 nothinx) | SKILL.md, kontrak, rujukan EYD V, kata baku KBBI, kalimat efektif, pola AI, istilah, singkatan, `pertahankan.md`, contoh, `scripts/periksa.py` (pemeriksa pola kaidah + klise, hanya pustaka standar Python, tanpa internet) |
| `esai/advanced-evaluation/` | https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering | HEAD 2026-10 (v2.1.0) | MIT | SKILL.md + rujukan desain juri LLM: bukti sebelum skor, tukar posisi pada adu berpasangan, seri bila dua urutan tidak sepakat, bias panjang/otoritas/swa-penilaian |

Catatan `naskah-id`: kontraknya (pasal 10) menolak perjokian skripsi/tugas dan penyamaran dari detektor. Di workflow ini yang dipakai hanya kaidah bahasanya. Esai 100% AI hanya dikirim ke lomba yang tidak melarang AI (lihat peringatan di tahap 0).

## Skill desain (28 Okt 2026)

`desain/impeccable/`, `desain/hallmark/` (v2.0.0 lengkap), tujuh skill ui-ux-pro-max (`desain/ui-ux-pro-max/`, `desain/design/`, `desain/design-system/`, `desain/brand/`, `desain/banner-design/`, `desain/ui-styling/`, `presentasi/slides/`), dan `desain/design-md-referensi/`. Dikemas di `arsip/skill-desain.zip` untuk diekstrak ke `.claude/skills/`. Sumber, commit, lisensi, dan cara memasangnya ada di `CARA-PASANG-SKILL-DESAIN.md`.

## Pengelompokan folder (5 Nov 2026)

Folder dipindah ke kelompok per kegunaan: `esai/`, `desain/`, `presentasi/` (lihat `README.md`). Isi setiap folder tidak diubah. `esai-lomba/` (orkestrator yang ditulis untuk Antigravity, isinya mengulang `CLAUDE.md`) dipindah ke `arsip/skill-lama/esai-lomba-antigravity/`.

## Metode yang diadaptasi (bukan disalin)

| Metode | Repo | Commit | Lisensi | Dipakai di |
|---|---|---|---|---|
| `novelty-check`: ide dipecah jadi unsur inti, pencarian per unsur, tabel karya terdekat, vonis "sama" hanya kalau ada karya spesifik, kalimat posisi | https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep (ARIS) | f76ec8d | MIT | `workflow/01-ide-dan-tesis.md` § Final langkah 4 |
| `kill-argument`: satu serangan terkuat dari satu sumbu, dipecah jadi poin atomik oleh juri baru, status dijawab/sebagian/belum, keputusan dihitung dengan aturan | sama | f76ec8d | MIT | `workflow/05-review.md`, `templates/prompt-juri.md` § B dan § D |

Yang tidak diambil dari ARIS: penilai lintas model lewat Codex MCP (butuh akun di luar Claude), skrip jejak, dan struktur `.aris/`. Tambahan kita yang tidak ada di ARIS: juri konfirmasi juga memeriksa apakah kutipan lokasi serangan benar-benar ada di naskah.

Catatan: versi terbaru `Imbad0202/academic-research-skills` (v3.24.1) memuat skill `deep-research`, `academic-paper` (mode `citation-check`), dan `academic-paper-reviewer`. Nama-nama itu sempat tercantum di Peta Skill sebagai skill akun padahal tidak pernah terpasang. Skill-nya tidak diambil karena berupa pipeline jurnal 10 tahap (terlalu berat untuk satu esai lomba); perannya sudah dipegang `tools/cari_sumber.py`, agen `auditor-sitasi`, dan agen `juri-esai`.

