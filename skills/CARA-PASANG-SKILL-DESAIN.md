# Skill desain: cara memasang

Semua skill desain dikemas dalam **`arsip\skill-desain.zip`** (dipindah dari folder utama ke `arsip\` pada 29 Okt 2026, jadi tidak ikut ke GitHub) (lengkap: SKILL.md, rujukan, skrip). Claude tidak diizinkan menulis langsung ke folder `.claude` dari jarak jauh, jadi pemasangannya kamu lakukan sendiri:

**Untuk Claude Code** (tab Code di Claude desktop, atau `claude` di terminal) yang dibuka di folder `new essay`:
1. Buka folder `arsip`, klik kanan `skill-desain.zip` → **Extract All...**
2. Isi tujuan ekstrak dengan `D:\Playground\new essay\.claude\skills` lalu klik Extract.
3. Buka ulang sesi Claude Code. Kesepuluh skill langsung terbaca otomatis.
4. Setelah itu zip-nya boleh dihapus. **Jangan hapus** `skills\desain\` dan `skills\presentasi\`: panduan workflow membaca file di sana sebagai rujukan.

Cara lain tanpa zip: salin folder skill dari `skills\desain\` atau `skills\presentasi\` ke `.claude\skills\`, sejajar tanpa folder kelompok. Keluarga ui-ux-pro-max (`design`, `design-system`, `brand`, `banner-design`, `ui-styling`, `ui-ux-pro-max`, `slides`) dipasang bersama karena saling memanggil sebagai folder tetangga.

**Untuk chat Claude biasa / Cowork**: unggah folder skill (di-zip) lewat Settings → Capabilities → Skills.

| Skill | Sumber | Lisensi | Catatan |
|---|---|---|---|
| `impeccable` | pbakaus/impeccable @8409a56 (v4.8.0) | Apache 2.0 | Folder `scripts/` (peluncur yang mengunduh program biner) sengaja tidak disertakan; skill memakai jalur cadangan "Launcher unavailable". |
| `hallmark` | Nutlope/hallmark @65b5e40 (v2.0.0) | MIT | Skrip inti disertakan (`theme.mjs`, `sloplint.mjs`, dll., butuh Node.js). `imagegen.mjs` butuh `TOGETHER_API_KEY` milikmu sendiri. |
| `ui-ux-pro-max`, `design`, `design-system`, `brand`, `banner-design`, `slides`, `ui-styling` | nextlevelbuilder/ui-ux-pro-max-skill @28b3b8d | MIT | Skrip Python/Node lokal. Pembuatan logo/ikon AI butuh kunci API milikmu (Gemini, Atlas Cloud, atau MuAPI); tanpa kunci hanya fitur itu yang tidak jalan. |
| `design-md-referensi` | VoltAgent/awesome-design-md @3b60532 | MIT | Kumpulan 84 DESIGN.md (bukan skill aslinya), dibungkus jadi skill supaya bisa dipanggil. |

Di workflow esai, skill-skill ini dipakai di **tahap 3b/4** (kritik dan poles visual esai, data-viz), **tahap 7** (sampul, poster, infografis), dan **tahap 7C** (slide). Letaknya di folder ini: `skills/desain/` dan `skills/presentasi/slides/`.
