# Audit workflow esai lomba: 5 juri tanpa konteks (28 Okt 2026)

Lima subagent dijalankan dari nol, tanpa riwayat percakapan. Masing-masing memakai satu peran, membaca folder ini tanpa mengubah apa pun, dan sebagian menguji alatnya langsung (output uji ditulis di folder sementara). Catatan: subagent tetap ikut membaca `CLAUDE.md`, jadi mereka tahu folder ini adalah workflow 100% AI.

| Peran | Skor | Inti putusan |
|---|---|---|
| Juri kepala lomba esai/LKTI | 6,5 | Cukup kuat untuk masuk 10 besar, tapi belum cukup untuk juara: rubrik menyimpang dari lembar nilai resmi, dan penulis tidak siap di babak presentasi |
| Peneliti integritas sumber | 6 | Bisa memastikan sumber *ada*, tapi tidak memastikan sumber *mendukung kalimatnya* |
| Senior AI engineer | 6 | Konsep juri LLM bagus, eksekusinya bocor: alat crash di Windows, juri tidak benar-benar buta |
| Editor bahasa Indonesia | 6,5 | Kaidah KBBI/EYD akurat, tapi pengecek buta terhadap klise khas esai lomba Indonesia |
| Auditor kepatuhan + siswa pemula | 6 | Matriks kepatuhan bagus, tapi tidak ada gerbang etika yang mengikat dan tidak ada mode cepat |

**Rata-rata ±6,2/10.** Semua sepakat desainnya di atas rata-rata SOP lomba. Lubangnya ada di eksekusi alat, pemeriksaan klaim terhadap sumber, etika, dan kecepatan.

---

## A. Temuan yang muncul di 2 juri atau lebih (paling bisa dipercaya)

1. **`cari_sumber.py` crash di Windows** (AI engineer, auditor). Kedua juri menguji langsung. Saat output ditangkap agen, encoding jatuh ke cp1252 sehingga emoji ✅❌⛔❓ memicu `UnicodeEncodeError`. Akibatnya `cek-pustaka` dan `doi` mati.
   → Tambahkan `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` di semua alat, seperti di `periksa.py`.
2. **Bobot rubrik internal mengalahkan bobot guidebook** (juri kepala, AI engineer). `templates/rubrik-esai.md:40` menyebut bobot sendiri "tidak berubah". Ini bertentangan dengan Aturan dasar 1. Contoh: di Pharfest, bahasa+format bernilai 30%, sedangkan rubrik internal hanya memberi bahasa 10%.
   → Syarat berhenti memakai skor dengan bobot guidebook. Rubrik H1–H6 dipakai sebagai lapis pembeda juara.
3. **Gerbang AI dan orisinalitas tidak mengikat** (juri kepala, auditor). Workflow hanya "menyebut" risikonya, tanpa keputusan wajib. Tidak ada larangan menandatangani surat "karya sendiri" untuk naskah 100% AI. Kriteria "Bebas jejak AI" (`rubrik-esai.md:18`) bisa terbaca sebagai upaya menyamarkan pemakaian AI.
   → Tambahkan gerbang wajib di akhir tahap 0: ungkapkan / minta konfirmasi tertulis panitia / pindah ke mode bantu-AI / STOP, lalu catat keputusannya di STATUS. Ganti kriteria itu menjadi "kualitas prosa".
4. **Tidak ada mode cepat** (juri kepala, auditor, AI engineer). Arena Ide butuh ±31 panggilan subagent, ditambah 8 checkpoint dan loop review sampai 3 putaran. Contoh Pharfest sendiri tenggatnya 4 hari.
   → Buat "Mode Kilat": 1 loop ide, juri lebih sedikit, checkpoint digabung, jadwal per hari, dan otomatis aktif bila tenggat < H-7.
5. **Aturan "wajib skill, kalau tidak BERHENTI" akan sering macet** (AI engineer, auditor). Ada baris "—" di Peta Skill, skill yang bersyarat, langkah yang tidak tercantum sama sekali, dan skill akun yang tidak ada di akun orang lain.
   → Rujukan di folder dianggap skill yang sah. Tetapkan fallback per langkah. Berhenti hanya kalau tidak ada skill *dan* tidak ada fallback.
6. **Penanda `[PERLU …]` tidak seragam** (peneliti, editor). Workflow memakai `[PERLU SUMBER]`, sedangkan `naskah-id` memakai `[PERLU DATA: …]`/`[PERLU RUJUKAN: …]`. Padahal `cek_naskah.py:136` hanya menangkap `[PERLU SUMBER]` persis, sehingga dua penanda lain lolos ke build.
   → Pakai satu format, ubah regex menjadi `\[PERLU (SUMBER|DATA|RUJUKAN)[^\]]*\]`, dan wajibkan hasilnya nol sebelum build.
7. **Retraksi gagal tanpa pesan** (peneliti, AI engineer). Kalau OpenAlex membalas 429, hasilnya None dan diperlakukan sebagai "tidak ditarik". Field `update-to` dari Crossref sudah diambil tapi tidak dipakai.
   → Tampilkan "retraksi TIDAK TERCEK" sebagai masalah, dan pakai `update-to`.
8. **Pencocokan sitasi salah untuk nama lembaga dan "dan"** (peneliti, AI engineer, editor). Contohnya "Badan Pusat Statistik" terbaca "Statistik", "Kemenkes" tidak cocok dengan "Kementerian Kesehatan", "Santoso dan Wibowo" terbaca "Wibowo", dan "(Rp, 1500)" dianggap sitasi. Dalam satu uji, 10 dari 12 temuan adalah alarm palsu.
9. **`--sumber <L>/riset` ikut membandingkan dossier tulisan Claude sendiri** (AI engineer). Cek 8-gram juga tidak bisa menangkap terjemahan dari sumber berbahasa Inggris (peneliti).
10. **Sisa struktur lama di root membingungkan** (semua juri). Contohnya `STATUS.md`, `00-aturan-lomba.md` yang sudah terisi "100% AI", `profil/`, `draf/`, `riset/`, `contoh/`, `MASTER_SOP_*`, dan PDF guidebook 3 salinan. Contoh Pharfest juga tidak punya `aturan.md`/`STATUS.md` walau disebut "contoh tahap 0 lengkap".

## B. Kritis, temuan satu juri tapi berat

- **Klaim tidak dicocokkan dengan sumbernya** (peneliti). Tidak ada artefak yang menautkan kalimat ke kutipan verbatim + halaman. Juri tahap 5 tidak pernah melihat sumber, sehingga lensa "angka di teks = angka di sumber" mustahil dikerjakan.
  → Buat `riset/peta-klaim.md` (kalimat | sumber | kutipan ≤40 kata | halaman | kekuatan klaim), ditambah subagent auditor sitasi yang hanya menerima peta itu dan teks sumbernya.
- **Metadata salah lolos sebagai ✅** (peneliti). Penulis dan tahun salah tetapi DOI benar tetap dihitung "terverifikasi", dan DOI arXiv/DataCite dicap "karangan".
  → Cocokkan tahun dan penulis pertama, tambahkan fallback DataCite, atau wajibkan `openalex.py daftar` sebagai lapis kedua.
- **Bug parser** (AI engineer). DOI yang berisi tanda kurung (Lancet/Elsevier) terpotong lalu dicap karangan. Daftar pustaka satu entri per baris terbaca sebagai 1 entri, jadi sisanya tidak dicek. `build_docx.py` juga menggabungkan seluruh pustaka jadi satu paragraf, menampilkan bullet `-` dan `###` apa adanya, dan crash pada kertas F4 atau nilai null.
- **Juri tidak buta** (AI engineer). Subagent ikut memuat CLAUDE.md dan bisa membuka file `ide/`. Kartu ide juga memuat "kenapa tidak pasaran", yang berarti pembelaan diri ikut dibaca juri.
  → Buat agen `.claude/agents/juri-*.md` tanpa alat, hapus field pembelaan sebelum penjurian, minta output JSON, dan siapkan `tools/arena.py` untuk acak dengan seed dan menghitung median/poin.
- **Loop review tidak akan pernah berhenti** (AI engineer). Devil's advocate diperintah untuk selalu mencari masalah, jadi selalu ada temuan Mayor dan loop selalu jalan 3 putaran.
  → Temuan Mayor sah hanya kalau dikonfirmasi juri kedua, dan skor, DA, serta adu berpasangan dijalankan sebagai panggilan terpisah.
- **Penulis tidak siap presentasi/wawancara** (juri kepala). Satu pertanyaan juri seperti "kenapa data ini?" bisa membongkar bahwa penulis tidak menguasai isinya.
  → Tambahkan tahap wajib "Pembekalan penulis": ringkasan 1 halaman, 15–20 pertanyaan beserta jawaban, simulasi tanya-jawab dengan juri penyerang, dan kuis sumber.
- **Klise esai lomba Indonesia tidak tertangkap** (editor). Contohnya "Indonesia Emas 2045", "garda terdepan", "angin segar", "sinergi pentahelix", "Melalui program ini, diharapkan dapat…", "Kedepannya", "di sosialisasikan", "Rp 5 milyar". Dari ±22 klise yang diuji, periksa.py hanya menangkap 2.
  → Tambahkan katalog "klise esai lomba Indonesia" di `pola-ai.md`, `periksa.py`, dan `frasa_slop.txt` dengan batas kata `\b` supaya "sinergis" atau "arsitek lanskap" tidak ikut kena.

## C. Mayor lainnya

- Daftar ide pasaran ditebak LLM. Belum ada korpus judul juara edisi sebelumnya, dan juri memakai model yang sama dengan generator (juri kepala).
- Bobot WOW 45% vs kelayakan 10% berisiko mendorong ide aneh. Kelayakan menurut jenjang sebaiknya jadi gerbang (juri kepala).
- Bukti ide baru dicek di final dengan 1–2 pencarian, tanpa aturan kembali ke cadangan kalau tahap 2 tidak menemukan data (juri kepala).
- Register suara tidak disesuaikan jenjang, padahal esai SMA yang berbunyi seperti tulisan doktoral adalah tanda joki/AI paling jelas (juri kepala). Panduan ragam per jenis esai hanya 4 baris dan cenderung bergaya jurnal (editor).
- LKTI yang menuntut data primer (survei, wawancara) belum ditangani (juri kepala).
- Kontrak `naskah-id` ("angka hanya dari pengguna, tolak menulis tugas utuh") bertentangan dengan mode 100% AI (editor).
- `--banding` tidak menangkap pergeseran kekuatan klaim, misalnya "berkorelasi" → "menyebabkan" (editor).
- Pola judul klise LKTI ("Optimalisasi … Sebagai Upaya … Mewujudkan Indonesia Emas 2045") dan kapitalisasi judul belum dicek (editor).
- Gerbang "tidak ada angka tanpa sumber" diklaim dicek mesin, padahal belum diimplementasikan. Sitasi bernomor `[1]` juga tidak terbaca (peneliti).
- Matriks kepatuhan belum punya baris untuk batas plagiasi, batas halaman, langkah pengiriman, dan aturan tim (auditor).
- PDF di Windows rapuh: LibreOffice di Program Files tidak terdeteksi, dan docx2pdf butuh MS Word (auditor, AI engineer).
- Konteks dan biaya: transkrip semua juri kembali ke agen utama (AI engineer).

## D. Urutan perbaikan yang disarankan

1. **Perbaikan alat (cepat, berdampak besar):** UTF-8 di semua alat, regex DOI berkurung, pemecahan entri pustaka (cari_sumber + build_docx), retraksi "TIDAK TERCEK" + `update-to`, cek tahun/penulis, fallback DataCite, regex `[PERLU …]` yang seragam, `--sumber …/teks`, pencocokan sitasi lembaga dan "dan", F4/null di profil. Tambahkan `tools/tes_alat.py` berisi kasus-kasus uji di atas.
2. **Gerbang etika + Mode Kilat + pembekalan penulis.**
3. **Bobot guidebook sebagai syarat berhenti, dan Mayor wajib dikonfirmasi silang.**
4. **Peta klaim + auditor sitasi buta.**
5. **Juri benar-benar terisolasi** (`.claude/agents/`, tanpa alat, JSON, `tools/arena.py`).
6. **Katalog klise Indonesia + matriks ragam per jenis esai + pola judul.**
7. **Longgarkan aturan skill-wajib** (fallback per langkah).
8. **Bersihkan struktur lama di root dan lengkapi contoh Pharfest.**

Catatan: semua temuan berasal dari laporan subagent. Temuan alat (UTF-8, DOI, retraksi) diuji langsung oleh dua juri secara terpisah. Sebelum memperbaiki temuan lain, cek dulu baris yang dirujuk.
