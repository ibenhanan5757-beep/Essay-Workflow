# Menjalankan workflow di Antigravity

Untuk penulis. Antigravity (aplikasi agen dari Google) bisa membuka folder ini dan menjalankan alat Python yang sama, tapi tidak membaca `CLAUDE.md` dan tidak punya fitur khusus Claude Code. File ini menjelaskan apa yang sudah disiapkan dan apa yang berbeda.

## Jawaban singkat

Sebagian besar workflow bisa jalan di Antigravity, **tapi tidak persis 100% sama** dengan di Claude Code:

| Bagian | Di Antigravity |
|---|---|
| Aturan workflow | Jalan. `AGENTS.md` dibaca otomatis dan menyuruh agen membaca `CLAUDE.md` |
| Panduan tahap, template, rujukan `skills/` | Jalan, dibaca dari folder yang sama |
| Alat Python (`tools/`) | Jalan, asal Python dan paketnya terpasang |
| Posisi kerja lomba (`STATUS.md` § Serah terima) | Jalan, sama persis |
| Juri buta | Jalan, tapi **tidak sepenuhnya buta**: subagent Antigravity selalu bisa membaca file dan ikut melihat `AGENTS.md` (diuji 5 Nov). Juri dibuat lewat `define_subagent` tanpa alat tulis dan dilarang membuka file lewat instruksinya, lalu dicatat sekali per lomba |
| Agen `.claude/agents/`, kunci `.claude/settings.json`, skill akun Claude (`pdf`, `docx`, `pptx`), connector Consensus/SciSpace | **Tidak ada.** Diganti alat folder (lihat `AGENTS.md` § 2) |
| Mutu tulisan dan ide | Bergantung model. Workflow ini disetel dan diuji dengan Claude; dengan model lain hasilnya belum pernah diukur |

## Yang sudah disiapkan di folder

| File | Fungsi |
|---|---|
| `AGENTS.md` | Aturan yang dibaca otomatis Antigravity: menunjuk ke `CLAUDE.md`, menerjemahkan bagian khusus Claude Code, dan memuat aturan keras (juri subagent, peta klaim, checkpoint) |
| `.agents/skills/esai-lomba/SKILL.md` | Skill pintu masuk: muncul saat kamu memberi juknis atau meminta "lanjutkan lomba …", lalu menunjuk ke panduan tahap |

Folder `.agent/skills/` (tanpa huruf *s*) yang kosong tidak dipakai; lokasi skill proyek Antigravity adalah `.agents/skills/`.

## Persiapan sekali

1. Buka Antigravity, lalu buka folder `D:\Playground\new essay` sebagai workspace.
2. Pastikan Python siap (di laptop ini sudah). Di laptop lain, ikuti `MULAI-DI-WINDOWS.md`.
3. Tempel prompt cek ini:

```
Baca AGENTS.md dan CLAUDE.md. Lalu, tanpa mengubah file apa pun:
1. Jalankan python tools/tes_alat.py.
2. Apakah kamu bisa memanggil subagent terpisah untuk juri? Model apa saja yang tersedia untuk subagent?
3. Apakah skill esai-lomba di .agents/skills/ terbaca?
Laporkan singkat.
```

## Memakai

- **Lomba baru:** taruh juknis di folder, lalu ketik: "Mulai lomba baru: <nama lomba>, juknisnya di <lokasi file>."
- **Melanjutkan lomba** yang dikerjakan di Claude: "Lanjutkan lomba <nama>, tahap N." Agen membaca `lomba/<nama>/STATUS.md` § Serah terima. Pastikan serah terima sudah diperbarui sebelum pindah (lihat `PINDAH-AKUN-CLAUDE.md` § Sebelum pindah).
- **Satu tahap, satu percakapan**, sama seperti di Claude Code.

## Saran pemakaian

- **Paling aman:** kerjakan Arena Ide, draf, dan revisi di Claude, karena workflow ini disetel dengan Claude.
- **Paling bermanfaat dari Antigravity: juri kedua dari keluarga model lain.** Semua juri di workflow ini memakai Claude, jadi bias menilai tulisan sendiri hanya teredam sebagian. Model Gemini di Antigravity bisa menjadi juri rubrik atau devil's advocate tambahan untuk draf tahap 5, dengan prompt dari `templates/prompt-juri.md`. Simpan hasilnya di `draf/review-vN.md` dan tandai juri mana yang dari Antigravity.
- Kalau seluruh lomba dikerjakan di Antigravity, catat di `STATUS.md` dan di tahap 8a, supaya hasilnya bisa dibandingkan dengan lomba yang dikerjakan di Claude.

## Hasil cek 5 Nov 2026

Laporan lengkapnya ada di `catatan/cek-antigravity.md`. Yang dipakai di `AGENTS.md`:

- **Subagent:** `invoke_subagent` dengan `Model` = `pro` / `flash` / `flash_lite` / `inherit`, dan `define_subagent` untuk membuat tipe juri tanpa alat tulis, tanpa MCP, dan tanpa subagent. Subagent tetap bisa membaca file dan melihat `AGENTS.md`, jadi juri di Antigravity tidak sepenuhnya buta.
- **File aturan:** `AGENTS.md` terbaca utuh (batas 24 KB per file; sekarang ±9 KB). `CLAUDE.md` tidak dimuat otomatis, jadi `AGENTS.md` menyuruh agen membacanya.
- **Aturan global plugin sains** (`~/.gemini/config/plugins/science/rules/AGENTS.md`) ikut termuat. `AGENTS.md` proyek menyatakan aturan itu tidak berlaku untuk workflow ini.
- **48 skill sains** (termasuk `literature-search-openalex`, `pubmed-database`) terpasang global. Skill-skill itu tidak dipakai; pencarian tetap lewat `tools/cari_sumber.py`.
- **Tidak ada alat membuka halaman web** (hanya `search_web`), jadi halaman dibuka lewat skrip Python. **Tidak ada alat cek kuota**; kalau muncul `RESOURCE_EXHAUSTED (429)`, agen wajib berhenti.
- **Model percakapan utama** bisa Gemini 3.8 Flash atau Claude Opus 4.6. Untuk menulis ide dan draf, pilih model terkuat yang tersedia.

## Supaya agen tidak menerobos

Pengalamanmu dengan Gemini (menerobos dengan cara lain dan mengarang) sudah dijawab dengan aturan berhenti di `CLAUDE.md` dan `AGENTS.md` § 0: setiap langkah dikerjakan persis seperti panduannya, atau agen berhenti dan melapor dengan format `⛔ BERHENTI`. Dua hal yang bisa kamu lakukan sendiri supaya lebih ketat:

1. Di pengaturan Antigravity, set **Chat Approval Policy** ke `request-review`, supaya setiap perintah terminal menunggu persetujuanmu.
2. Di setiap checkpoint, cek **daftar periksa langkah** yang wajib disertakan agen. Setiap langkah harus punya path file sebagai bukti. Kalau ada langkah tanpa bukti, minta agen membuktikannya atau mengulang langkah itu.

Kalau agen tetap menerobos, catat kejadiannya di `STATUS.md` § Catatan keputusan supaya masuk evaluasi tahap 8a.
