# Audit alat pencarian sumber (5 November 2026)

Pertanyaan penulis: apakah alat, skill, dan connector untuk pemetaan tema dan pencarian sumber sudah cukup? Semua hasil di bawah diuji langsung dari laptop penulis (Windows) dan dari sesi Claude Code desktop pada tanggal ini.

## Yang sudah ada dan berfungsi

| Alat | Uji | Hasil |
|---|---|---|
| `tools/cari_sumber.py` (OpenAlex) | "penurunan tanah Semarang" | ✅ 5 artikel jurnal Indonesia yang relevan (Undip, BIG, DOAJ). OpenAlex cukup baik menjangkau jurnal Indonesia yang ber-DOI. |
| `cari_sumber.py` (OpenAlex), kueri kedua | "resep tidak terlayani puskesmas kekosongan obat" | ❌ **HTTP 429**: pencarian anonim OpenAlex dibatasi ("use a free API key"). Kunci `OPENALEX_API_KEY` belum dipasang, dan alat tidak mencoba ulang. |
| `cari_sumber.py --db semua` | "drug stockout primary health care Indonesia" | ⚠️ OpenAlex, arXiv, dan Europe PMC jalan. Semantic Scholar 429 (tanpa kunci). PubMed sempat gagal SSL ("self-signed certificate in chain"), tapi berhasil saat dicoba ulang, jadi masalahnya sesekali saja. |
| Connector **Consensus** (tersambung) | "land subsidence Semarang … house floor raising" | ✅ 8 artikel relevan, termasuk Abidin dkk. 2013 dan Bott dkk. 2021. Paket gratis: halaman pertama saja, DOI hanya untuk paket berbayar. |
| Connector **SciSpace** (tersambung) | pertanyaan yang sama | ✅ 10 artikel, **5 di antaranya jurnal berbahasa Indonesia** (Kemijen, Dadapsari/Layur, Tambak Lorok) yang langsung relevan. Ada tautan PDF. **Connector ini belum disebut di Peta Skill CLAUDE.md.** |
| Skill `deep-research` | daftar skill sesi | ❌ **Tidak tersedia di sesi ini**, padahal Peta Skill menyebutnya di 6 langkah. Penggantinya subagent riset + WebSearch. |
| Connector PubMed, alphaXiv, bioRxiv | status connector | ❌ tidak tersambung (Peta Skill menulis "bila terpasang") |

## Sumber khusus Indonesia (cek akses dari laptop ini)

| Sumber | Akses | Catatan |
|---|---|---|
| Garuda (garuda.kemdiktisaintek.go.id) | 200 | tidak ada API resmi; banyak jurnal SINTA tanpa DOI hanya ada di sini |
| SINTA | 403 | menolak akses otomatis |
| BPS WebAPI (webapi.bps.go.id) | 200 | butuh kunci gratis (daftar akun BPS, dilakukan penulis) |
| data.go.id (Satu Data Indonesia) | 200 | API CKAN terbuka |
| JDIH BPK (peraturan.bpk.go.id) | curl 200, **Python 403** | memblokir user-agent bawaan Python |
| peraturan.go.id | 200 | di sesi cloud Pharfest koneksinya ditolak |
| Google Patents / PDKI (DJKI) | 200 / 302 | belum dipakai; relevan untuk cek "sudah ada?" ide inovasi/teknik |

## Celah untuk pemetaan tema (Arena Ide Langkah 0)

1. **Kolom "keramaian" dan "ruang kebaruan" di peta subtema diisi dengan tebakan agen.** Belum ada angka. OpenAlex bisa menghitung jumlah karya per kata kunci per tahun, dan memisahkan karya global dari karya berafiliasi Indonesia. Selisih besar (ramai secara global, sepi di Indonesia) adalah tanda peluang "jembatan riset ke lokal".
2. **Data resmi Indonesia (BPS, Satu Data, regulasi) dicari lewat WebSearch biasa**, sehingga angka di bekal sering berasal dari berita, bukan tabel resmi.
3. **Jurnal Indonesia tanpa DOI** (Garuda) tidak terjangkau `cari_sumber.py`. Pencarian SciSpace menutup sebagian celah ini.
4. **Cek "sudah ada?" belum mencakup paten dan program pemerintah**, padahal untuk lomba inovasi/teknik keduanya sumber tumpang tindih yang paling mungkin.
5. **Judul juara lomba sejenis** (bank juara) masih sangat sedikit (8 baris). Ini bahan kalibrasi juri yang paling berharga.

## Usulan (menunggu persetujuan penulis, lewat tahap 8c)

| # | Usulan | Jenis | Biaya |
|---|---|---|---|
| A1 | **Penulis membuat kunci gratis OpenAlex** (https://openalex.org/settings/api) lalu `setx OPENALEX_API_KEY "<kunci>"`. Claude tidak boleh membuat akun atas nama penulis. | bug | 5 menit penulis |
| A2 | `cari_sumber.py`: coba ulang otomatis saat 429 (mengikuti `retryAfter`), user-agent yang jelas untuk situs pemerintah, pesan jelas kalau kunci belum ada | bug | kecil |
| A3 | Peta Skill: tambahkan **SciSpace** (tersambung, kuat untuk jurnal Indonesia) dan tulis pengganti resmi kalau `deep-research` tidak tersedia | proses | kecil |
| A4 | `cari_sumber.py peta "kw1" "kw2" …`: jumlah karya global vs Indonesia per tahun (OpenAlex `group_by`), untuk mengisi kolom keramaian/ruang kebaruan di peta subtema | proses | sedang |
| A5 | Cek "sudah ada?": tambahkan Google Patents/PDKI dan situs program pemerintah untuk lomba inovasi/teknik | proses | kecil (panduan saja) |
| A6 | `cari_sumber.py --db garuda` (membaca halaman pencarian Garuda) dan `bps` (WebAPI, kunci dari penulis) | proses | sedang; Garuda bisa rusak kalau tampilan situsnya berubah |
| A7 | Opsional: connector **Elicit** (ada di direktori, belum tersambung) untuk pencarian sistematis/laporan | proses | penulis menyambungkan sendiri |

## Agenda riset berikutnya (urut nilai)

| # | Pertanyaan | Kenapa penting | Cara | Biaya |
|---|---|---|---|---|
| R1 | Ide seperti apa yang menang di lomba esai/LKTI pelajar Indonesia 2023–2026? Kumpulkan 50–100 judul juara + bidang + jenjang. | Menguji bobot "wow" 45% (PL09) dan menyediakan kartu jangkar. Hasilnya dibaca **per lomba dan per bidang**, bukan sebagai satu pola umum. Data Toyota TEY 13 (hardware/limbah lokal) hanya berlaku untuk Toyota Eco Youth, dan perbedaannya dengan ide Arena Toyota karena penulis membatasi ide ke software, bukan karena Arena gagal. | 2–3 subagent riset (Sonnet) di berita kampus dan situs panitia → `catatan/bank-juara.md`, setiap baris dengan link. Utamakan edisi lalu dari lomba yang akan diikuti. | ±3 subagent |
| R2 | Seberapa besar bobot orisinalitas/kebaruan di rubrik resmi lomba esai Indonesia? Survei 15–20 guidebook. | Menguji PL08: apakah rubrik ide yang mengutamakan "wow" cocok dengan lembar nilai resmi | subagent + `baca_pdf.py` untuk guidebook yang bisa diunduh | ±2 subagent |
| R3 | Berapa lomba esai pelajar yang kini melarang AI, mewajibkan surat orisinalitas, atau memakai Turnitin/detektor AI? | Risiko terbesar workflow 100% AI (PL03). 3 dari 4 lomba sejauh ini mewajibkan surat orisinalitas. | gabungkan dengan R2 (guidebook yang sama) | 0 tambahan |
| R4 | Apakah juri AI (Claude) bisa membedakan esai juara dari yang tidak juara? | Validitas seluruh Arena dan tahap 5 | hanya bisa diuji lewat 8b (uji balik) setelah hasil lomba keluar; Navigation 12 Nov | 2 subagent per lomba |

