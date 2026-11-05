# Perubahan workflow, 29 Okt 2026

Perbaikan berdasarkan audit 5 juri (`catatan/audit-workflow-2026-10-28.md`) dan daftar "Urutan perbaikan" yang disetujui penulis: **dikerjakan 1, 3, 4, 5, 7, 8. Dilewati 2 dan 6** atas permintaan penulis.

Cadangan lengkap folder sebelum perubahan: `D:\Playground\new essay-backup-2026-10-29\`.

## 1. Alat + tes
| File | Perubahan |
|---|---|
| `tools/cari_sumber.py` | Keluaran dipaksa UTF-8, jadi tidak crash di Windows saat di-pipe. File dibaca `utf-8-sig`. Regex DOI menerima tanda kurung (`10.1016/S0140-6736(97)11096-0`) dan DOI arXiv (`10.48550/arXiv...`). Fallback ke **DataCite** kalau DOI tidak ada di Crossref. Daftar pustaka dipecah **satu entri per baris/butir**, dengan baris berawalan spasi sebagai lanjutan. DOI dicocokkan dengan **penulis pertama + tahun** (±1), dan jurnal sebagai info. Retraksi dibaca dari Crossref `updated-by`/`update-to` + OpenAlex. Kalau OpenAlex gagal, hasilnya **"❓ status retraksi TIDAK TERCEK"** dan dihitung sebagai masalah. Entri tanpa DOI (`.go.id`, BPS, WHO, peraturan) dihitung dan didaftar sebagai "cek manual". Preprint `posted-content` ditandai. Kalau offline, alat berhenti dengan pesan satu baris. Header `--simpan` ditambah kolom "Teks disimpan di". |
| `tools/cek_naskah.py` | UTF-8 + `utf-8-sig`. Penanda seragam: semua `[PERLU ...]` (SUMBER/DATA/RUJUKAN, huruf apa pun). `--nama` dan frasa klise dicocokkan **per kata utuh**. Pencocok sitasi ditulis ulang: koma sebelum tahun, `dan`/`&`, `dkk.`/`et al.`, banyak tahun `(Smith, 2020, 2021)`, singkatan lembaga dari `Nama Lengkap [SINGKATAN]`, sitasi naratif lembaga multi-kata, dan `[n]`. `(Maret 2024)` dan `(Rp 1500)` diabaikan. `--sumber <L>/riset` otomatis memakai `riset/teks/` dan melewati `dossier.md`/`sumber.md`/`README.md`. "1.000" dihitung satu kata. Fungsi `penanda_belum_beres()` dipakai bersama build. |
| `tools/build_docx.py` | UTF-8 + `utf-8-sig`. Pesan jelas kalau python-docx belum terpasang. **Build ditolak kalau ada `[PERLU ...]`/TODO** (`--paksa` untuk uji). Keterangan gambar ikut tercetak (baris di bawah gambar, atau alt-text). Mendukung `###`, daftar `-`/`1.`, dan baris pemisah `|:-:|` diabaikan. Kertas **F4/Folio**/Legal. `nomor_halaman` atas/bawah (termasuk `tengah_atas`) atau `null`. Nilai `null` di profil diganti default, bukan crash. "Daftar Pustaka" tidak peka huruf besar dan boleh diakhiri titik dua. Pustaka satu paragraf per entri. **Metadata DOCX (author/lastModifiedBy) dikosongkan**. Bug `blok.index` diganti loop berindeks. LibreOffice dicari di `Program Files`. Kegagalan docx2pdf ditangkap. |
| `tools/tes_alat.py` (baru) | 37 tes `unittest`, semuanya tanpa jaringan kecuali 3 (aktif dengan `ESAI_TES_JARINGAN=1`). Mencakup semua bug di atas, termasuk subprocess dengan `PYTHONIOENCODING=cp1252`. |
| `tools/README.md` | Ditulis ulang: daftar pip (python-docx, pypdf, docx2pdf), tanpa path tetap, perilaku baru setiap alat, alat baru, dan status uji. |

## 3. Peta klaim
| File | Perubahan |
|---|---|
| `templates/sumber.md` | Kolom "Teks disimpan di" + tabel **Peta klaim** (ID, klaim, sumber, kutipan verbatim ≤40 kata, hlm, kekuatan, status). |
| `workflow/02-riset.md` | Peta klaim wajib. Status ✅ hanya setelah kutipan disalin. Teks sumber di `riset/teks/` harus asli dengan baris `Sumber: URL · diakses · bagian`. Prosedur menyelesaikan `[PERLU ...]` (cari ≤3 kali → lemahkan/hapus → catat). Kembali ke ide cadangan kalau 2 dari 3 pertanyaan bukti tidak terjawab. Domain Garuda diseragamkan. |
| `workflow/04-menulis-draf.md` | § Fakta hanya dari peta klaim: hanya klaim ✅, kalimat ditandai `<!--Kn-->`, kekuatan tidak melebihi peta. `cek_klaim.py` ditambah ke checkpoint. |
| `tools/cek_klaim.py` (baru) | Angka di draf (%, Rp, desimal koma, ribuan, tahun data) harus ada di peta klaim. ID `<!--Kn-->` harus ada dan ✅. |
| `templates/prompt-auditor-sitasi.md` (baru), `.claude/agents/auditor-sitasi.md` (baru) | Auditor sitasi buta: hanya menerima pasangan (kalimat, kutipan), lalu menjawab mendukung/sebagian/tidak/tak bisa dinilai. |
| `workflow/05-review.md` | Langkah auditor sitasi. "Tidak mendukung" = Kritis. |
| `workflow/03-kerangka.md` | Kolom bukti di pohon argumen menyebut ID peta klaim. |
| `workflow/06-revisi-final.md` | Sumber/angka baru wajib masuk peta klaim. Cek akhir memakai `cek_klaim.py`, nol `[PERLU ...]`, `--sumber .../teks`, dan metadata penulis kosong. Contoh pustaka lembaga `[SINGKATAN]`. Log perubahan per kriteria. |

## 4. Rubrik resmi sebagai skor utama tahap 5
| File | Perubahan |
|---|---|
| `workflow/05-review.md` | Ditulis ulang. **Rubrik resmi dengan bobot resmi = skor utama dan syarat berhenti** (tidak ada kriteria resmi < 7, tidak ada Kritis/Mayor terkonfirmasi, auditor sitasi bersih, maks 3 putaran). Rubrik sendiri jadi lapis kedua. Skor, devil's advocate, konfirmasi, auditor, dan berpasangan dijalankan sebagai **panggilan terpisah**. Temuan Kritis/Mayor wajib berkutipan dan **dikonfirmasi** juri baru, yang tidak sah turun jadi Minor. |
| `templates/prompt-juri.md` | Ditulis ulang jadi bagian A (rubrik resmi + lapis kedua), B (DA, kutipan wajib, "tidak ada temuan" sah), C (berpasangan), dan D (konfirmasi temuan, baru). |
| `templates/rubrik-esai.md` | Judul jadi "lapis kedua". Kalimat "bobot resmi tidak menggantikan" diganti § Hubungan dengan rubrik resmi. **P4 "Bebas jejak AI" tidak diubah** (bagian dari item 2 yang dilewati). |
| `templates/review.md` | Tabel cek mesin, skor resmi, skor lapis kedua, auditor sitasi, kolom konfirmasi, log perubahan, dan syarat berhenti. |
| `.claude/agents/juri-esai.md` (baru) | Agen juri esai tanpa CLAUDE.md (`omitClaudeMd: true`) dan tanpa alat file/web. |
| `templates/rubrik-ide.md` | Tetap rubrik sendiri, hanya diubah sesuai item 5. |

## 5. Arena Ide (jalur penuh dipertahankan)
| File | Perubahan |
|---|---|
| `.claude/agents/juri-ide.md` (baru) | Juri buta tanpa CLAUDE.md dan tanpa alat Read/Glob/Grep/Bash/PowerShell/Write/Edit/Web/Agent/Skill. Agen proyek baru terbaca setelah sesi Claude Code dibuka ulang. |
| `workflow/01-ide-dan-tesis.md` | Kartu **dibersihkan** (tanpa Lensa dan "Kenapa tidak pasaran") sebelum dinilai. Acak dengan `arena.py acak --seed`. **≥1 juri dengan model berbeda** dari generator. Kesan 30 detik jadi panggilan terpisah. Gerbang **G4 Layak untuk jenjang**. Agregasi oleh `arena.py rekap` (median, gugur mayoritas, seri → K1+K2 → kesan "berhenti"). Aturan "boleh naik satu peringkat" dihapus. **Setiap finalis wajib ≥2 data pendukung nyata**, yang kurang tidak ikut final. Jalur cadangan kalau riset tahap 2 gagal. Ide pasaran utamanya dari **judul/abstrak juara sungguhan**, prediksi model hanya cadangan berlabel. Catatan biaya (±35 panggilan) dan bias diperbarui. Generator tidak dikurangi. |
| `templates/rubrik-ide.md` | G4 ditambah. K6 dinilai setelah G4. |
| `templates/prompt-ide-juri.md` | Langkah pembersihan + acak + agen + keragaman model untuk agen utama. Keluaran **JSON** untuk `arena.py`. Prompt "Kesan 30 detik" terpisah. Kritik Top 3 menerima kartu bersih. |
| `templates/prompt-ide-pasaran.md` | Data juara sungguhan dulu (dengan link, tidak boleh dikarang), lalu prediksi berlabel. |
| `templates/prompt-ide-generator.md` | "Kenapa tidak pasaran" ditandai untuk cek mandiri (dibuang sebelum dinilai). Ditambah pengingat G4. |
| `templates/prompt-ide-adu.md` | Memakai agen `juri-ide` dan kartu bersih + bukti. Baris JSON per adu. `arena.py adu`. |
| `tools/arena.py` (baru) | `acak` (seed tetap + label buta), `rekap` (median, gugur gerbang, urutan), `adu` (poin: sepakat = 1, tidak sepakat/seri = 0,5). |
| `lomba/_template/ide/README.md` | Daftar file baru (`peta-subtema.md`, `adu-final.json`, `juri/`). |

## 7. Mode Kilat, waktu, Windows, istilah
| File | Perubahan |
|---|---|
| `workflow/MODE-KILAT.md` (baru) | Jalur untuk tenggat ≤ 5 hari, **bukan default**, dan dipilih penulis: 1 loop generator + 1 juri dengan model berbeda + penulis memilih dari Top 5, review 1 putaran. Bagian yang tidak boleh dipangkas: kepatuhan, peta klaim, auditor sitasi, alat cek, dan cek akhir. |
| `workflow/00-dekonstruksi-lomba.md` | Tabel perkiraan waktu per tahap dan pemicu tawaran Mode Kilat. Rujukan contoh Pharfest diperbaiki. |
| `MULAI-DI-WINDOWS.md` (baru) | Python (PATH, `py`), pip, LibreOffice/docx2pdf, PowerShell di folder, path berspasi, encoding, email/kunci API, dan tabel "kalau macet". |
| `ISTILAH.md` (baru) | Daftar istilah: CARS, CER, K1–K7, G1–G4, H1–H6, P1–P4, peta klaim, seed, median, dll. |
| `README.md` | Tautan ke Windows/istilah, perkiraan waktu dan Mode Kilat, isi folder baru. |

## 8. Merapikan + aturan skill
| File | Perubahan |
|---|---|
| `arsip/` (baru) + `arsip/README.md` | **Dipindah, tidak dihapus**: root `STATUS.md`, `00-aturan-lomba.md`, `profil/`, `contoh/`, `draf/`, `riset/`, `Guidebook EWC Siswa Pharfest 2026.pdf` (salinan ketiga, isi identik), dan `catatan/MASTER_SOP_WORKFLOW_LKTI_ESAI_CHAMPION.md`. Tidak ada file workflow yang merujuk path lama. `skill-desain.zip` tidak dipindah karena masih dirujuk `skills/`. |
| `CLAUDE.md` § **Pemakaian skill** (baris ±32–43, menggantikan "ATURAN WAJIB: setiap langkah pakai skill spesifik") | Rujukan folder dihitung sebagai skill sah. Boleh memakai skill akun yang lebih cocok (`citation-check`, `paper-critique`, `llm-council`, `stop-slop`/`humanizer`, `docx`, `create-viz`, `canvas-design`), dengan menyebut dan mencatat skill yang dipakai. Skill yang tidak tersedia diganti rujukan folder. **Berhenti hanya kalau tidak ada skill dan tidak ada alternatif.** Bagian ini sengaja dibuat satu judul supaya mudah ditambah. |
| `CLAUDE.md` § Peta Skill | Baris "—" diisi (agen `juri-ide`, `arena.py`, alat folder), ditambah baris ide pasaran, peta klaim, dan auditor sitasi, juri esai memakai rubrik resmi, dan path skill desain diarahkan ke `skills/` (atau `.claude/skills/` setelah dipasang). § Tahapan, § Alat, dan syarat berhenti diperbarui. **Bagian "Mode: esai 100% AI" dan "Pengaman" tidak diubah.** |
| `PENJELASAN-WORKFLOW.md` | Disesuaikan dengan semua perubahan di atas (aturan skill, struktur folder, tahap 1/2/4/5/6, tabel alat, pengaman, "yang belum selesai"). |
| `lomba/contoh-pharfest-2026/` | `dekonstruksi.md` → **`aturan.md`** dengan struktur template dan **kolom Hlm** (nomor halaman dicek dari `baca_pdf.py`), rubrik resmi per butir. **`STATUS.md`** baru. Kontak humas ditulis sebagai rujukan halaman. |
| `catatan/kritik-sop-juara.md` | Catatan lokasi baru SOP asli. |
| `lomba/_template/riset/README.md` | Aturan teks sumber asli + `--sumber <L>/riset/teks`. |

## Yang dilewati
- **Item 2** (gerbang integritas AI): tidak ada gerbang AI baru, P4 "Bebas jejak AI" tidak diganti nama, teks mode AI di CLAUDE.md tidak diubah. Butir checklist lama "Aturan AI dan orisinalitas sudah diputuskan" di `workflow/06` dibiarkan apa adanya.
- **Item 6** (siswa di dalam esai): tidak ada langkah wawancara, penulisan ulang oleh siswa, pembaca manusia, atau latihan tanya-jawab.
- Sesuai catatan koordinator, sengaja tidak dikerjakan: literatur jurnal sebagai sumber ide, rencana visual esai, dan gaya DOCX profesional di luar perbaikan bug.

## Belum dikerjakan / catatan
- Temuan editor bahasa (katalog klise lomba Indonesia, perbaikan aturan EYD di `naskah-id`, `--banding` untuk verba klaim) termasuk item 6 versi audit (klise/ragam), bukan daftar yang disetujui. Belum dikerjakan.
- Agen proyek di `.claude/agents/` baru terbaca setelah sesi Claude Code dibuka ulang di folder ini. Field `omitClaudeMd` dan `disallowedTools` mengikuti dokumentasi Claude Code. Tidak ada cara resmi untuk membuat agen benar-benar tanpa alat, jadi alat file/web/shell ditolak satu per satu.
- PDF tidak bisa diuji di komputer ini (LibreOffice dan docx2pdf tidak terpasang). `build_docx.py --pdf` memberi pesan yang jelas.
- Peta klaim belum diuji pada esai sungguhan. Pola angka di `cek_klaim.py` mungkin perlu ditambah setelah dipakai.

## Hasil uji akhir (29 Okt 2026)
- `python tools/tes_alat.py`: **37 tes, OK (3 tes jaringan dilewati)**. Dengan `ESAI_TES_JARINGAN=1`, ketiga tes jaringan juga lulus (Crossref, DataCite arXiv, retraksi Wakefield).
- `skills/naskah-id/scripts/periksa.py --tes`: 108/108.
- Uji kering pada Markdown placeholder (di folder sementara, bukan esai lomba):
  - `cek_naskah`: hanya melapor kurang kata, sesuai harapan.
  - `cek_klaim`: bersih.
  - `build_docx`: DOCX A4, margin 4/3, `###`, butir, pustaka satu entri per paragraf, tabel tanpa baris pemisah, metadata kosong. PDF dilewati dengan pesan.
  - `cek-pustaka`: 1 entri terverifikasi.
- `python tools/cari_sumber.py doi "10.1016/S0140-6736(97)11096-0"`: DOI terbaca utuh, ⛔ DITARIK.

---

# Tambahan 29 Okt 2026 (thread "skill, ide, visual")

Dikerjakan setelah perbaikan di atas selesai, di atas versi hasil perbaikan itu. Permintaan penulis: aturan skill yang fleksibel, jurnal sebagai sumber ide, file Word yang terlihat profesional, dan rencana visual esai.

| File | Perubahan |
|---|---|
| `CLAUDE.md` § Pemakaian skill | Ditambah (tidak mengganti): dua sumber skill (folder vs akun), lihat daftar skill akun sebelum langkah penting, urutan kekuatan aturan > CLAUDE.md > workflow > skill, tabel skill akun per tahap, dan skill yang tidak dipakai. |
| `CLAUDE.md` § Peta Skill, Tahapan, Alat | Baris baru: tambang literatur (tahap 1), rencana visual (3b), cek tampilan naskah (6); grafik memakai `buat_visual.py`; tahap 3b di tabel tahapan; alat `buat_visual.py` dan `cek_docx.py`. |
| `workflow/01-ide-dan-tesis.md` | **Langkah 0b — Tambang literatur**: 15–30 artikel per subtema, empat jenis benih (temuan belum diterapkan, celah riset, metode lintas bidang, hasil kontra-intuitif), kartu di `ide/tambang-literatur.md`, dipakai generator loop 2–3 lewat lensa "jembatan riset ke lokal". Kartu ke juri tetap bersih (tanpa DOI). |
| `templates/prompt-ide-generator.md` | Blok `<benih>` dan lensa jembatan riset ke lokal. |
| `workflow/03-kerangka.md` | § 7 Rencana visual; checkpoint menyertakan rencana visual. |
| `workflow/03b-rencana-visual.md` (baru) | Cek aturan, uji tiga pertanyaan per visual, menu visual + alat + skill, spesifikasi `buat_visual.py`, lantai visual, palet khas AI yang dihindari, isi `rencana-visual.md`, pemeriksaan. |
| `workflow/06-revisi-final.md` | Contoh Markdown gambar/tabel dengan keterangan dan sumber; § Tampilan naskah profesional (wajib, dilarang, cara cek); cek akhir memakai `cek_docx.py` dan melihat setiap halaman PDF. |
| `workflow/07-sampul-poster.md` | Merujuk tahap 3b dan aturan palet. |
| `tools/build_docx.py` | `##`/`###` memakai gaya Heading 1/2 Word (hitam, font naskah, tanpa warna tema, keep with next); tabel tiga garis (tanpa garis tegak) dan rata tengah; keterangan "Tabel N."/"Gambar N."/"Sumber:" lebih kecil, tanpa indent, "Tabel N." menempel ke tabel; alt-text "Gambar N. ..." dicetak bersama baris "Sumber:" di bawah gambar; kontrol baris janda/yatim; lebar gambar dari `lebar_gambar_cm`, tinggi dibatasi `tinggi_gambar_maks_cm`. Paragraf biasa yang diawali "Gambar 1 menunjukkan" tetap paragraf. |
| `tools/buat_visual.py` (baru) | Grafik `batang`, `batang_h`, `garis` dan diagram `alur`, `siklus` dari JSON. Butuh matplotlib. |
| `tools/cek_docx.py` (baru) | Cek tampilan file Word (lihat `tools/README.md`). |
| `tools/tes_alat.py` | +4 tes: tampilan profesional build_docx, cek_docx (bersih vs kotor), buat_visual (semua jenis, jenis tidak dikenal). |
| `tools/README.md`, `MULAI-DI-WINDOWS.md`, `PENJELASAN-WORKFLOW.md` | Alat baru, `pip install matplotlib`, tahap 3b, tambang literatur, aturan skill dua sumber, pengaman baru. |
| `lomba/_template/profil.json` | `lebar_gambar_cm`, `tinggi_gambar_maks_cm`, `warna_aksen`. |
| `lomba/_template/visual/README.md` (baru), `lomba/_template/ide/README.md` | Folder spesifikasi visual; `tambang-literatur.md` di daftar file Arena Ide. |

Uji (Linux, Python 3.13, python-docx, matplotlib 3.11.2): `tes_alat.py` 41 tes OK (3 tes jaringan dilewati). Contoh naskah dengan grafik, diagram alur, dan tabel dibangun, dicek `cek_docx.py` (bersih), lalu dirender ke PDF lewat LibreOffice dan dilihat per halaman. Belum diuji di Windows: jalankan `python tools/tes_alat.py` sekali.

## Tambahan: tahap 7C Presentasi/PPT (29 Okt 2026)

Permintaan penulis: panduan PPT yang tidak "AI-slop", skenario kalau penulis memberi contoh PPT, dan **PPT hanya dibuat kalau diminta** (tidak otomatis setelah tahap 6).

| File | Perubahan |
|---|---|
| `workflow/07c-presentasi.md` (baru) | Pemicu hanya atas permintaan; aturan presentasi; **skenario PPT contoh** (A template wajib panitia, B contoh gaya, C contoh juara, D tanpa contoh; contoh gaya yang ber-slop ditanyakan sekali); alur slide khusus lomba dengan pola tata letak dan detik; lantai anti-slop slide (isi dan tampilan); naskah bicara; cara membuat file; uji (cek_pptx, render + uji 3 detik, hitung waktu, simulasi juri, 5 pertanyaan mematikan). |
| `templates/naskah-bicara.md`, `templates/prompt-juri-presentasi.md` (baru) | Naskah per slide dengan kata/detik; prompt 3 juri presentasi (kesan 3 detik, skor berkutipan, pertanyaan, tanda slide AI). |
| `tools/cek_pptx.py` (baru) | `cek` (tanda slide buatan AI) dan `gaya` (ringkasan gaya PPT contoh). Butuh python-pptx. |
| `tools/tes_alat.py` | +2 tes cek_pptx (43 tes). |
| `workflow/07-sampul-poster.md` | Judul jadi "Sampul, Poster & Lampiran Visual"; § C dipindah ke 07c. |
| `workflow/06-revisi-final.md` | Di checkpoint, sebutkan sekali bahwa PPT bisa dibuat kalau diminta; jangan dimulai sebelum diminta. |
| `CLAUDE.md`, `PENJELASAN-WORKFLOW.md`, `tools/README.md`, `MULAI-DI-WINDOWS.md` | Baris 7C di Peta Skill dan Tahapan, aturan "tidak pernah otomatis", alat `cek_pptx.py`, `pip install python-pptx`. |
| `lomba/_template/presentasi/README.md` (baru) | Isi folder presentasi. |

Uji: `tes_alat.py` 43 tes OK di Linux (python-pptx 1.0.2). Deck kotor (emoji, gradasi ungu, 6 butir 14 pt, judul label) tertangkap; deck bersih tanpa temuan.
