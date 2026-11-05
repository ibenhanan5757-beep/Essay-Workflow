# Laporan Lingkungan Antigravity: Workflow Esai Lomba
**Tanggal:** 2026-11-05

Laporan ini memverifikasi kesiapan lingkungan Google Antigravity untuk menjalankan workflow penulisan esai lomba (`new essay`). Setiap poin ditandai sumber validasinya: `[DIUJI]` (diuji langsung pada sesi ini), `[DOKUMENTASI]` (tercantum dalam panduan/dokumentasi resmi Antigravity), atau `[TIDAK TAHU]` (tidak dapat dipastikan).

---

## A. Model dan Versi

### 1. Versi Antigravity dan Model Aktif
* **Model Aktif:** `Gemini 3.8 Flash (High)` `[DIUJI]`. (Sebelumnya pada sesi ini sempat menggunakan `Claude Opus 4.6 (Thinking)` berdasarkan riwayat pengaturan pengguna).
* **Versi Antigravity:** Antigravity 2.0 Desktop Application (Google DeepMind / Google AI platform) `[DOKUMENTASI]`. 
* **CLI `agy`:** Perintah `agy` tidak terdaftar pada PATH Windows sistem saat ini (`ObjectNotFound: CommandNotFoundException`), sehingga nomor versi build CLI internal tidak dapat ditarik via terminal `[DIUJI]`.

### 2. Daftar Model yang Dapat Dipilih
* **Percakapan Utama (Chat UI):** Dapat diganti sewaktu-waktu oleh pengguna melalui menu pemilih model (*Model Selection dropdown*) di UI Antigravity. Pilihan model yang terkonfirmasi aktif meliputi `Gemini 3.8 Flash (High)` dan `Claude Opus 4.6 (Thinking)` `[DIUJI]`.
* **Subagent (`invoke_subagent`):** Model subagent dipilih secara presisi melalui parameter `Model` dengan opsi enum persis:
  1. `"inherit"` (mengikuti model percakapan utama)
  2. `"flash_lite"` (model teringan dan tercepat)
  3. `"flash"` (model menengah)
  4. `"pro"` (model penalaran terkuat/terbesar) `[DIUJI]`.

---

## B. File Instruksi

### 3. File Instruksi yang Dimuat Otomatis
* **File yang dimuat otomatis ke sistem:**
  1. `d:\Playground\new essay\AGENTS.md` `[DIUJI]`
  2. `C:\Users\Asus\.gemini\config\plugins\science\rules\AGENTS.md` (aturan visualisasi dari plugin global) `[DIUJI]`
* **Catatan penting:** File `CLAUDE.md` **TIDAK** dimuat secara otomatis ke dalam konteks aturan prompt Antigravity. Antigravity hanya memindai `AGENTS.md`, `GEMINI.md`, dan `.agents/rules/*.md` `[DIUJI]`.
* **Kutipan bukti kalimat pertama `AGENTS.md` yang diterima sistem:**
  > `File ini dibaca otomatis oleh Antigravity. Workflow di folder ini ditulis untuk Claude Code, jadi aturan lengkapnya ada di CLAUDE.md: baca file itu di awal setiap tugas workflow dan ikuti, kecuali bagian yang diterjemahkan di § 2.` `[DIUJI]`

### 4. Batas Panjang File Instruksi dan Status `AGENTS.md`
* **Batas per file instruksi:** Maksimal **24 KB (24.000 bytes)**. File instruksi yang melebihi 24.000 bytes akan dipotong (*truncated*) pada batas baris `[DOKUMENTASI]`.
* **Batas agregat (*aggregate rules budget*):** **20.000 tokens** (`defaultRulesBudget`). Aturan yang melebihi anggaran total akan diturunkan (*demoted*) menjadi penunjuk lokasi file (*file path pointer*) agar dibaca sesuai kebutuhan `[DOKUMENTASI]`.
* **Status `AGENTS.md` saat ini:** **TIDAK TERPOTONG** `[DIUJI]`. Ukuran file `AGENTS.md` adalah 8.131 bytes (jauh di bawah batas 24.000 bytes). Seluruh isi teks diterima utuh hingga baris terakhir (`pip install python-docx pypdf matplotlib python-pptx (MULAI-DI-WINDOWS.md).`).

---

## C. Skill

### 5. Status Skill "esai-lomba" dan Daftar Seluruh Skill
* **Status `esai-lomba`:** **TERBACA DAN AKTIF** di lokasi `d:\Playground\new essay\.agents\skills\esai-lomba\SKILL.md` `[DIUJI]`.
* **Total skill yang terdeteksi:** 60 skill (1 skill lokal proyek + 59 skill global/bawaan) `[DIUJI]`.
* **Daftar lengkap skill:**
  * **Skill Proyek (1):**
    * `esai-lomba`: `d:\Playground\new essay\.agents\skills\esai-lomba\SKILL.md`
  * **Skill Bawaan Antigravity (7):**
    * `agy-customizations`: `C:\Users\Asus\.gemini\antigravity\builtin\skills\agy-customizations\SKILL.md`
    * `antigravity-guide`: `C:\Users\Asus\.gemini\antigravity\builtin\skills\antigravity_guide\SKILL.md`
    * `automation`: `C:\Users\Asus\.gemini\antigravity\builtin\skills\automation\SKILL.md`
    * `generative_ui`: `C:\Users\Asus\.gemini\antigravity\builtin\skills\generative_ui\SKILL.md`
    * `migrate-workflows`: `C:\Users\Asus\.gemini\antigravity\builtin\skills\migrate-workflows\SKILL.md`
    * `plugin`: `C:\Users\Asus\.gemini\antigravity\builtin\skills\plugin\SKILL.md`
    * `ui-plugin-navigation`: `C:\Users\Asus\.gemini\antigravity\builtin\skills\ui-plugin-navigation\SKILL.md`
  * **Skill Global Plugin Sains (`~/.gemini/config/plugins/science/`) (48):**
    * `alphafold-database-fetch-and-analyze`, `alphagenome-atlas-website-links`, `alphagenome-single-variant-analysis`, `alphagenome-variant-impact-score`, `biomolecular-structure-viewer`, `chembl-database`, `cheminformatics-cofolding`, `cheminformatics-core`, `cheminformatics-doc2mol`, `cheminformatics-ml`, `cheminformatics-physics`, `cheminformatics-reactions`, `clinical-trials-database`, `clinvar-database`, `credentials`, `dbsnp-database`, `embl-ebi-ols`, `encode-ccres-database`, `ensembl-database`, `foldseek-structural-search`, `gnomad-database`, `gtex-database`, `human-protein-atlas-database`, `interpro-database`, `jaspar-database`, `literature-search-arxiv`, `literature-search-biorxiv`, `literature-search-europepmc`, `literature-search-openalex`, `ncbi-sequence-fetch`, `openfda-database`, `opentargets-database`, `pdb-database`, `predictingthepast`, `protein_sequence_msa`, `protein-sequence-similarity-search`, `pubchem-database`, `pubmed-database`, `pymol`, `quickgo-database`, `rdkit-general`, `reactome-database`, `string-database`, `ucsc-conservation-and-tfbs`, `unibind-database`, `uniprot-database`, `uv`, `workflow-skill-creator`.
  * **Skill Global Plugin Gemini API & SDK (4):**
    * `gemini-api-dev`, `gemini-live-api-dev`, `gemini-omni-flash-api` (`~/.gemini/config/plugins/gemini-api/`)
    * `google-antigravity-sdk` (`~/.gemini/config/plugins/google-antigravity-sdk/`)

---

## D. Subagent

### 6. Nama Alat dan Parameter Pemanggilan Subagent
* **Nama Alat:** `invoke_subagent` `[DIUJI]`.
* **Parameter:**
  * `TypeName` (*string, wajib*): Tipe subagent (`"self"`, `"research"`, `"image-generator"`, atau nama custom yang dibuat lewat `define_subagent`).
  * `Role` (*string, wajib*): Judul/peran singkat 2–5 kata (misal: `'Juri Buta Putaran 1'`).
  * `Prompt` (*string, wajib*): Instruksi kerja detail.
  * `Model` (*enum, opsional*): Pilihan model: `"inherit"`, `"flash_lite"`, `"flash"`, `"pro"`.
  * `Workspace` (*enum, opsional*): Mode workspace: `"inherit"` (default), `"branch"` (workspace terisolasi/kloning), atau `"share"`.
* **Alat Pendukung:**
  * `define_subagent`: Mendefinisikan tipe agen baru beserta switch izin: `EnableWriteTools`, `EnableMCPTools`, `EnableSubagentTools`, dan `SystemPrompt`.
  * `manage_subagents`: Mengelola status (`list`, `kill`, `kill_all`).
  * `send_message`: Berkomunikasi antar-agen via `ConversationId`.

### 7. Hasil Uji Langsung Subagent (`Model: flash_lite`)
* **Eksekusi:** Subagent diuji menggunakan `Model="flash_lite"` dan `TypeName="research"` dengan ID `fa22f53f-8301-4b7b-a57f-5702624860e4` `[DIUJI]`.
* **Jawaban Subagent Apa Adanya:**
  > `(1) Ya, saya bisa membaca file di workspace. (2) Ya, saya melihat isi AGENTS.md beserta aturan dan konteks yang diberikan. (3) Saya memiliki akses ke alat bawaan (seperti run_command, view_file, search_web, dll.) serta semua alat MCP yang terdaftar di sistem.` `[DIUJI]`

### 8. Larangan Akses File/Alat dan Konkurensi Paralel
* **Apakah subagent bisa dilarang membaca file dan memanggil alat?**
  * Secara arsitektur, Antigravity menetapkan bahwa subagent selalu mewarisi alat riset pembacaan file: *"Subagents always have tools to research the codebase and to communicate with other agents"* `[DOKUMENTASI]`.
  * Parameter `define_subagent` hanya dapat menonaktifkan alat tulis (`EnableWriteTools: false`) dan MCP (`EnableMCPTools: false`).
  * **Solusi Juri Buta:** Agar subagent benar-benar bertindak sebagai juri buta tanpa membaca workspace atau memanggil alat, pembatasan **wajib** dikunci melalui `SystemPrompt` atau `Prompt` eksplisit: *"DILARANG membuka file apa pun, DILARANG memanggil tool apa pun, evaluasi HANYA berdasarkan teks yang disediakan dalam prompt ini."* `[DIUJI]`.
* **Berapa subagent boleh berjalan paralel?**
  * Antigravity mendukung peluncuran banyak subagent di latar belakang secara asinkron (reactive wakeup tanpa polling) `[DOKUMENTASI]`.
  * Batas konkurensi tidak dibatasi angka baku di antarmuka, tetapi dibatasi oleh kuota token / rate-limit API `[DOKUMENTASI]`. Saat kuota habis, pemanggilan subagent akan ditolak dengan galat `RESOURCE_EXHAUSTED (code 429)` `[DIUJI]`.

---

## E. Alat

### 9. Ketersediaan Alat
* **Terminal / Eksekusi Python:** Tersedia via `run_command` (lingkungan Windows PowerShell/cmd) `[DIUJI]`.
* **Baca-Tulis File:** Tersedia via `read_file`, `write_file`, dan `edit_file` `[DIUJI]`.
* **Pencarian Web:** Tersedia via `search_web` `[DIUJI]`.
* **Membuka Halaman Web:** Tidak ada alat native mandiri `fetch_url` untuk membaca HTML mentah secara langsung di core tools Antigravity, tetapi dapat dieksekusi melalui skrip Python (`httpx`/`requests`/`curl`) di terminal `[DIUJI]`.
* **Browser Otomatis:** Tidak ada browser interaktif visual bawaan aktif secara native (kecuali modul luar seperti `Browser Use` atau Playwright yang dijalankan mandiri via Python) `[DIUJI]`.
* **Melihat Gambar / Halaman PDF sebagai Gambar:** `read_file` secara native mendukung format teks, gambar, audio, video, dan PDF (multimodal) `[DOKUMENTASI]`. Selain itu, konversi halaman PDF menjadi gambar dapat diproses secara lokal melalui pustaka Python `pypdf` / `pdf2image` `[DIUJI]`.

### 10. Uji `python tools/tes_alat.py`
* **Status:** Berhasil dijalankan tanpa kegagalan `[DIUJI]`.
* **Baris Terakhir Hasil Eksekusi:**
  ```text
  Ran 50 tests in 2.707s

  OK (skipped=3)
  ```

### 11. Uji `python tools/cari_sumber.py`
* **Perintah:** `python tools/cari_sumber.py cari "stunting posyandu Indonesia" --n 2`
* **Status:** Berhasil 100% `[DIUJI]`.
* **Hasil:** Menghasilkan 2 literatur terverifikasi dari OpenAlex:
  1. *Irma Afifa dkk. (2023). PEMBERDAYAAN KADER POSYANDU TERHADAP KEJADIAN STUNTING PADA BALITA DI INDONESIA : SYSTEMATIC LITERATURE REVIEW* (Jurnal Kesehatan Tambusai).
  2. *Iman Permana dkk. (2026). Increasing The Capacity of Posyandu Cadres to Reduce Stunting in Sarwodadi Village, Indonesia* (Proceeding International Conference of Community Service).

---

## F. Alur Kerja

### 12. Fitur Meminta Persetujuan Penulis di Checkpoint
1. **Artifacts dengan `RequestFeedback: true`:**
   Saat membuat atau mengedit artefak (rencana kerja, matriks, draf) di folder artefak (`<appDataDir>\brain\<conversation-id>`), menyetel `RequestFeedback: true` memunculkan tombol **"Proceed"** di antarmuka agar penulis menyetujui langkah sebelum dieksekusi `[DOKUMENTASI]`.
2. **`ask_question`:**
   Alat bawaan untuk menyajikan pertanyaan interaktif atau opsi multiple-choice di antarmuka chat dan menunggu respons penulis sebelum agen melangkah `[DOKUMENTASI]`.
3. **Chat Approval Policy:**
   Pengaturan izin eksekusi tool di UI Antigravity (`request-review` atau `strict`) secara otomatis menahan eksekusi perintah terminal hingga disetujui secara manual oleh penulis `[DOKUMENTASI]`.

### 13. Ingatan Antarpercakapan dan Struktur Folder
* **Ingatan Antarpercakapan:** Setiap sesi percakapan baru dimulai dengan konteks bersih (*fresh state*). Percakapan sebelumnya diarsipkan dalam file log `transcript.jsonl` dan basis data `conversation_summaries.db`, serta dapat direferensikan manual oleh pengguna lewat `@ mentions` (previous conversations) di UI `[DOKUMENTASI]`. Tidak ada transfer memori diam-diam yang terjadi tanpa dimuat ke dalam file.
* **Folder Standar Antigravity:**
  * **Aturan:** `AGENTS.md` di root proyek atau direktori `.agents/rules/*.md`.
  * **Skill:** Direktori `.agents/skills/<nama>/SKILL.md` adalah lokasi standar untuk penambahan kemampuan berbasis repositori `[DOKUMENTASI]`.

### 14. Pengecekan Kuota dan Penanganan Batas Limit
* **Melihat Sisa Kuota:** Agen tidak memiliki alat bawaan untuk membaca kuota secara kuantitatif. Pengguna harus memantau sisa kuota melalui panel profil/pengaturan aplikasi Antigravity `[DIUJI]`.
* **Jika Kuota Habis:** Sistem memicu galat sistem `RESOURCE_EXHAUSTED (code 429)` yang menginformasikan reset waktu (misal: *"Individual quota reached. Resets in 8h29m43s"*). Saat galat ini terjadi, subagent atau giliran percakapan model akan dihentikan paksa oleh sistem `[DIUJI]`.
