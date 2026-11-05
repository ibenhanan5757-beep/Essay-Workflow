# Pindah ke akun Claude lain

Untuk penulis dan untuk Claude di akun baru yang tidak punya ingatan apa pun tentang percakapan sebelumnya. Panduan ini tidak mengubah aturan workflow; semua aturan tetap di `CLAUDE.md`.

## Jawaban singkat

Workflow ini bisa dijalankan penuh oleh akun Claude lain, **asal dibuka di Claude Code di folder ini**. Hampir semua yang dibutuhkan disimpan di folder, bukan di akun: aturan (`CLAUDE.md`, dibaca otomatis), panduan per tahap, agen juri, kunci skill, alat Python, dan posisi kerja setiap lomba (`<L>/STATUS.md` § Serah terima). Pindah akun pada dasarnya sama dengan memulai utas baru, yang memang sudah menjadi cara kerja normal workflow ini (`CLAUDE.md` § Satu utas pendek per tahap).

| Tempat menjalankan | Bisa? | Alasan |
|---|---|---|
| Claude Code (tab Code di Claude desktop, atau `claude` di terminal) di folder ini, di laptop ini | **Ya, penuh** | Semua aturan, agen, alat, dan data lomba ada di folder |
| Claude Code di laptop lain | **Ya**, setelah persiapan | Folder harus disalin **utuh** (termasuk `lomba/`, `catatan/`, `arsip/`), lalu Python dipasang (`MULAI-DI-WINDOWS.md`) |
| Sesi cloud (claude.ai/code) | Tidak untuk lomba yang sedang berjalan | `lomba/`, semua PDF, dan `arsip/` sengaja tidak ikut ke GitHub (`.gitignore`); agen juri pernah tidak termuat di sesi cloud (PL01) |
| Chat biasa claude.ai atau aplikasi HP | **Tidak** | Tidak bisa membuka folder, menjalankan alat Python, atau memanggil juri buta. Hanya untuk tugas lepas, misalnya membaca satu draf yang ditempel |

## Apa yang ikut dan apa yang tidak

| Hal | Disimpan di | Ikut ke akun baru? | Kalau tidak ada |
|---|---|---|---|
| Aturan, panduan, template | `CLAUDE.md`, `workflow/`, `templates/` | Ya | — |
| Agen juri (`juri-ide`, `juri-esai`, `auditor-sitasi`) | `.claude/agents/` | Ya | Cara cadangan di `workflow/01-ide-dan-tesis.md` § Juri buta (prompt juri utuh, dicatat "tidak dijamin buta") |
| Kunci skill akun | `.claude/settings.json` | Ya | — |
| Rujukan skill dan alat | `skills/`, `tools/`, `lomba-ig/` | Ya | — |
| Posisi kerja lomba | `<L>/STATUS.md` § Serah terima, file di `<L>/` | Ya, **asal serah terima diperbarui** | Lihat "Kalau serah terima tertinggal" di bawah |
| Pelajaran dan bank juara | `catatan/` | Ya | — |
| Riwayat percakapan | akun lama | Tidak | Digantikan serah terima. Yang hanya ada di percakapan dianggap hilang |
| Ingatan otomatis Claude | `C:\Users\<nama>\.claude\projects\…` di laptop ini | Mungkin, kalau laptop dan pengguna Windows-nya sama | Tidak dibutuhkan; isinya juga tercatat di `STATUS.md` dan `CLAUDE.md` |
| Kunci API (`OPENALEX_API_KEY`, `ESAI_EMAIL`, `SEMANTIC_SCHOLAR_API_KEY`) | variabel lingkungan Windows | **Ya** di laptop dan pengguna Windows yang sama (tidak terikat akun Claude). Laptop lain: pasang ulang | `MULAI-DI-WINDOWS.md` § 6. Kunci sengaja tidak disimpan di folder |
| Connector Consensus, SciSpace | akun | Tidak, kecuali dipasang lagi | `tools/cari_sumber.py` (OpenAlex, PubMed, arXiv, Europe PMC, Semantic Scholar) sudah cukup |
| Skill akun `pdf`, `docx`, `pptx` | akun (Settings → Capabilities) | Tergantung akun | PDF: alat Read Claude Code bisa membaca halaman PDF langsung, ditambah `tools/baca_pdf.py`. Word: python-docx. Slide (7C saja): python-pptx + `tools/cek_pptx.py` |
| Skill akun lain (bab skripsi, parafrase, dll.) | akun | Tidak | Memang tidak dipakai (`CLAUDE.md` § Pemakaian skill) |
| Kuota dan plan | akun | Berbeda | Lihat "Hemat kuota" di bawah |

## Sebelum pindah (di akun lama, kalau masih sempat)

1. Ketik: **"Perbarui serah terima sekarang."** Claude menyelesaikan langkah yang sedang berjalan sampai hasilnya tersimpan di file, lalu mengisi `<L>/STATUS.md` § Serah terima dan § Log kuota.
2. Kalau limit habis di tengah langkah, tidak apa-apa. Hasil yang sudah tersimpan di file tetap terpakai. Langkah yang setengah jalan diulang dari awal langkah itu. Contoh: di Arena Ide, JSON juri yang sudah tersimpan di `ide/juri/` tidak perlu diulang; juri yang belum tersimpan dipanggil lagi.

## Di akun baru: persiapan sekali

1. Masuk ke akun baru di Claude desktop, buka tab **Code**, lalu pilih folder `D:\Playground\new essay`. (Atau buka terminal di folder itu dan ketik `claude`.)
2. (Opsional) Di Settings → Capabilities akun baru, aktifkan skill `pdf`, `docx`, `pptx`, dan connector Consensus/SciSpace kalau tersedia. Tanpa itu, workflow tetap jalan dengan alat cadangan.
3. Tempel prompt cek kesiapan ini:

```
Cek kesiapan workflow di folder ini tanpa mengubah file apa pun:
1. Apakah agen juri-ide, juri-esai, dan auditor-sitasi tersedia?
2. Jalankan python tools/tes_alat.py.
3. Skill akun pdf/docx/pptx dan connector Consensus/SciSpace mana yang tersedia?
4. Jalankan python tools/evaluasi.py rekap.
Laporkan singkat apa yang siap, apa yang kurang, dan cadangan yang akan dipakai.
```

Kalau tes alat gagal karena paket Python belum ada, ikuti `MULAI-DI-WINDOWS.md` § 2.

## Melanjutkan lomba

Cukup ketik: **"Lanjutkan lomba <nama>, tahap N."** `CLAUDE.md` membuat Claude membaca `<L>/STATUS.md` dulu, lalu berkas yang disebut di § Serah terima.

### Kalau serah terima tertinggal

Kalau akun lama berhenti sebelum sempat memperbarui serah terima, tempel ini:

```
Serah terima di lomba/<nama>/STATUS.md mungkin tertinggal. Jangan melanjutkan pekerjaan dulu.
Periksa file di lomba/<nama>/ (ide/, ide/juri/, riset/, draf/, kirim/) beserta tanggal ubahnya,
tentukan langkah terakhir yang hasilnya sudah tersimpan utuh, lalu laporkan:
tahap dan langkah terakhir yang selesai, langkah yang setengah jalan, dan usulan langkah berikutnya.
Tunggu persetujuan saya sebelum memperbarui serah terima atau melanjutkan.
```

## Hemat kuota di akun dengan limit lebih kecil

- Arena Ide jalur penuh memakai sekitar 35 panggilan subagent. Di akun Pro, jalur penuh bisa butuh lebih dari satu jendela limit 5 jam. Pecah menjadi utas 1A, 1B, 1C, dan cek limit sebelum memulai.
- Kalau tenggat ≤ 5 hari atau kuota tipis, pilih **Mode Kilat** (`workflow/MODE-KILAT.md`).
- Juri memakai model `sonnet` atau `haiku`; subagent riset paralel paling banyak 3–4 (PL11).
- Satu tahap, satu utas. Jangan melanjutkan utas yang diam lebih dari 1 jam; mulai utas baru dari serah terima.

## Catatan untuk Claude di akun baru

- Kamu tidak punya ingatan tentang lomba ini, dan itu sudah diantisipasi. Sumber kebenaran adalah file: `CLAUDE.md`, `<L>/STATUS.md`, dan isi `<L>/`. Jangan menebak keputusan penulis yang tidak tercatat; tanyakan.
- Skill akun mengikuti daftar izin di `CLAUDE.md` § Pemakaian skill. Kalau `pdf`/`docx`/`pptx` tidak ada di akun ini, pakai cadangan di tabel atas dan sebutkan ke penulis.
- Nama skill di `.claude/settings.json` ditulis untuk akun lama. Skill akun di akun ini yang namanya berbeda tidak otomatis terblokir; aturan tertulis di `CLAUDE.md` tetap berlaku untuk semuanya.
- Kalau agen juri tidak termuat, pakai cara cadangan di `workflow/01-ide-dan-tesis.md` § Juri buta dan catat di `STATUS.md` bahwa juri tidak dijamin buta.
- Catat di `STATUS.md` § Catatan keputusan bahwa pekerjaan dilanjutkan dari akun lain, beserta tanggalnya, supaya tahap 8a bisa melihat apakah perpindahan menimbulkan masalah.
