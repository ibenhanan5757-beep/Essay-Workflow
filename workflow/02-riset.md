# Tahap 2 — Riset Sumber (Dossier)

Sumber: `skills/esai/academic-research-skills/source_quality_hierarchy.md`, aturan sitasi `ml-paper-writing` (AI-Research-SKILLs), dan konsep *literature dossier* dari "Master SOP Juara".

Hasil: `<L>/riset/sumber.md` (log sumber + **peta klaim**) + `<L>/riset/teks/` (teks sumber yang dibaca) + `<L>/riset/dossier.md` (ringkasan bukti per pertanyaan). **Tidak ada kalimat naskah sebelum dossier dan peta klaim selesai.**

## Aturan keras
1. **Jangan mengarang sitasi.** Setiap sumber dicari dengan alat, dibuka, dan dibaca bagian yang relevan. Yang belum bisa diverifikasi ditandai `[PERLU SUMBER]`.
2. **Angka hanya dari sumber.** Setiap angka dicatat di peta klaim dengan tahun data, halaman/tabel, dan kutipan verbatim asalnya. Kalau tidak ada data, tulis sebagai *estimasi dengan asumsi eksplisit* ("jika 30% ... maka ...") atau buang. Jangan mengarang "hasil uji", "validasi", atau "penghematan Rp X miliar".
3. **Sumber ditemukan ≠ sumber mendukung.** Baca abstrak/isi sebelum mengaitkannya ke klaim. Status ✅ hanya diberikan setelah kutipan verbatim yang mendukung klaim disalin ke peta klaim.
4. Jangan pakai paper yang sudah ditarik (retracted). Alat menandainya. Kalau alat mencetak "status retraksi TIDAK TERCEK", ulangi nanti atau cek manual sebelum memberi ✅.
5. **Teks sumber harus asli.** Isi `<L>/riset/teks/*.md` hanya teks yang benar-benar diambil dari sumber (hasil WebFetch, abstrak dari alat, salinan dari PDF), bukan ringkasan tulisan sendiri. Baris pertama setiap file: `Sumber: <URL/DOI> · diakses <tanggal> · bagian: <abstrak/hlm 4–6/...>`.

## Hemat konteks
Aturan keras di atas tidak berubah. Bagian ini hanya mengatur cara kerjanya supaya utas tidak membengkak (PL11, PL26).
- Teks sumber disimpan dulu ke `riset/teks/`, lalu kutipan dicari dengan Grep atau dibaca per rentang baris. File teks sumber tidak dimuat utuh ke percakapan.
- Prompt WebFetch dibuat sempit, misalnya "kutip persis kalimat yang memuat angka X beserta halamannya". WebFetch menjalankan prompt itu di panggilan model terpisah dan hanya mengembalikan hasilnya, jadi prompt yang sempit memberi hasil pendek yang bisa langsung dipakai.
- **Kalau pertanyaan bukti dibagi ke subagent:** pakai Sonnet, maksimal 3 bersamaan, dan cek `get_usage` dulu. Subagent menyimpan teks sumber asli ke `riset/teks/`, lalu mengembalikan calon baris peta klaim berstatus ⚠️ beserta path berkasnya. **Status ✅ hanya diberikan agen utama** setelah mencocokkan kutipan dengan berkas di `riset/teks/` (aturan keras 3).
- PDF regulasi atau laporan yang panjang diekstrak dulu dengan `tools/baca_pdf.py`. Yang dibaca hanya halaman yang dikutip.

## Peta klaim (wajib)
Tabel "Peta klaim" di `<L>/riset/sumber.md` (format di `templates/sumber.md`) adalah satu-satunya tempat draf boleh mengambil fakta.
- Satu baris per klaim faktual: ID (`K1`, `K2`, ...), klaim seperti yang akan ditulis di naskah, nomor sumber di log, **kutipan verbatim ≤40 kata** dari teks sumber, halaman/tabel, kekuatan bukti, dan status.
- Kutipan diambil dari file di `riset/teks/`, bukan dari ingatan. Kalau teksnya tidak bisa dibuka (paywall), status maksimal ⚠️ dan klaim itu tidak boleh dikutip sebagai fakta.
- Klaim di naskah tidak boleh lebih kuat dari kutipannya. Kalau sumber bilang "berkorelasi", klaim tidak boleh berbunyi "menyebabkan".
- Angka yang akan ditulis dalam bentuk lain (misalnya "Rp1,2 juta" dari "Rp1.200.000") ditulis dalam bentuk naskah di kolom "Klaim di naskah", supaya `tools/cek_klaim.py` bisa mencocokkannya.

## Menyelesaikan `[PERLU ...]`
Semua penanda memakai satu bentuk: `[PERLU SUMBER]`, `[PERLU DATA: apa yang dicari]`, atau `[PERLU RUJUKAN: apa yang dicari]`. `cek_naskah.py` menangkap ketiganya, dan `build_docx.py` menolak build selama masih ada.
1. Cari maksimal tiga kali dengan kata kunci berbeda (alat + satu sumber Indonesia yang relevan).
2. Kalau ketemu: buka, salin kutipan ke peta klaim, beri ID, ganti penanda dengan sitasi + `<!--Kn-->`.
3. Kalau tidak ketemu: lemahkan klaim jadi pernyataan tanpa angka atau estimasi berasumsi eksplisit, atau hapus kalimatnya.
4. Catat keputusannya di `STATUS.md` § Catatan keputusan (klaim apa, dicari di mana, hasilnya).

## Alat (`tools/cari_sumber.py`, tanpa instal tambahan)

| Kebutuhan | Perintah |
|---|---|
| Cari paper umum (250 juta+ karya) | `python tools/cari_sumber.py cari "kata kunci bahasa inggris" --dari 2019` |
| Biomedis/kesehatan | `... cari "..." --db pubmed,europepmc` |
| Preprint sains/teknologi | `... cari "..." --db arxiv` (preprint belum peer-review, jadi pakai seperlunya) |
| Jurnal Indonesia, termasuk yang tanpa DOI | `... cari "kata kunci bahasa Indonesia" --db garuda` (membaca halaman pencarian Garuda; abstrak ikut terambil). Hasil tanpa DOI menampilkan link PDF |
| Semua database sekaligus | `... cari "..." --db semua --n 3` |
| Hanya open access | tambah `--oa` |
| Simpan ke log | tambah `--simpan <L>/riset/sumber.md` |
| Simpan teks sumber yang dibaca | tempel abstrak/kutipan penting ke `<L>/riset/teks/<penulis-tahun>.md`. Folder ini dipakai `cek_naskah.py --sumber` untuk mendeteksi kalimat yang tersalin mentah. |
| Verifikasi DOI + cek retraksi + format APA 7 | `... doi 10.xxxx/xxxxx` |
| Teks penuh artikel tanpa DOI (misalnya dari Garuda) | `... teks "<link PDF>" --simpan-teks <L>/riset/teks --nama penulis-tahun`. Penulis, tahun, judul, dan jurnal dicatat manual dari halaman artikelnya |
| Cari versi akses terbuka (legal) dan simpan teks penuhnya | `... teks 10.xxxx/xxxxx --simpan-teks <L>/riset/teks` (OpenAlex, Unpaywall kalau `ESAI_EMAIL` diisi, Europe PMC). File langsung diberi baris `Sumber: … · diakses … · bagian: teks penuh`. Paper tanpa versi terbuka: alat menyebutnya; status peta klaim maksimal ⚠️ kalau hanya abstrak yang terbaca |
| Cek seluruh daftar pustaka draf | `... cek-pustaka <L>/draf/draf-v1.md` |
| Recall & label obat (FDA, data AS) | `... fda "amoxicillin"` |
| Uji klinis terdaftar | `... uji-klinis "antibiotic resistance"` |

Connector akun yang boleh dipakai (daftar izin di `CLAUDE.md` § Pemakaian skill): **Consensus** dan **SciSpace**, hanya untuk menemukan paper. Setiap temuan tetap dibuka teksnya dan diverifikasi dengan `doi` sebelum masuk peta klaim.

Tips: kata kunci bahasa Inggris memberi hasil jauh lebih banyak. Supaya tidak cepat dibatasi API (HTTP 429), isi variabel lingkungan `ESAI_EMAIL`, `OPENALEX_API_KEY`, dan (opsional) `SEMANTIC_SCHOLAR_API_KEY` (`MULAI-DI-WINDOWS.md` § 6).

**Sumber Indonesia** (tidak punya API yang stabil, cari manual lalu catat link-nya). Pilih sesuai bidang lomba:

| Bidang | Data & regulasi | Database paper (alat) |
|---|---|---|
| Umum | BPS (bps.go.id), Satu Data Indonesia, peraturan.go.id / JDIH kementerian terkait | OpenAlex, Semantic Scholar |
| Kesehatan/farmasi | Kemenkes (profil kesehatan, SKI/Riskesdas), BPOM (cekbpom.pom.go.id), Fornas/DOEN, WHO | PubMed, Europe PMC; `fda`, `uji-klinis` |
| Lingkungan/energi | KLHK (SIPSN untuk sampah), ESDM, BMKG, BRIN | OpenAlex |
| Ekonomi/bisnis | BI, OJK, Kemenkeu, Kemenkop UKM, World Bank | OpenAlex (filter ekonomi) |
| Pendidikan | Kemendikbudristek (Dapodik, Rapor Pendidikan), PISA/OECD | OpenAlex, Europe PMC (psikologi) |
| Teknologi/AI | Komdigi, laporan industri kredibel | arXiv, Semantic Scholar |
| Pertanian/pangan | Kementan, Bapanas, FAO | OpenAlex |
| Sosial/hukum/budaya | Komnas HAM, BPS sosial, putusan MA, jurnal SINTA | OpenAlex |

Jurnal Indonesia: `cari_sumber.py cari "…" --db garuda` lebih dulu, lalu OpenAlex (banyak jurnal SINTA terindeks di sana). Google Scholar hanya dibuka manual (memblokir otomatisasi). Kalau artikelnya punya DOI, verifikasi dengan perintah `doi`.

## Prioritas sumber
1. Data resmi (BPS, Kemenkes, BPOM, WHO, World Bank)
2. Tinjauan sistematis / meta-analisis
3. Artikel jurnal peer-review (internasional atau SINTA)
4. Regulasi & pedoman resmi
5. Laporan lembaga riset kredibel
6. Berita media kredibel (hanya untuk kasus/peristiwa)
7. Preprint dan opini pakar (paling lemah)

Target jumlah referensi mengikuti panjang esai, bukan angka tetap. Sebagai patokan (kalau guidebook tidak mengatur): esai 1.000–1.500 kata cukup 8–15 sumber; LKTI 3.000+ kata 15–30 sumber. yang benar-benar dipakai jauh lebih baik dari 25 sumber tempelan.

## Langkah
1. Dari tesis, turunkan 3–5 pertanyaan bukti.
2. Untuk setiap pertanyaan: cari dengan alat, simpan, buka, simpan teksnya ke `riset/teks/`, baca, isi kolom "temuan", lalu tulis baris peta klaim (kutipan verbatim + halaman). Baru setelah itu ubah status jadi ✅.
3. **Lokus:** kumpulkan data spesifik lokus (angka daerah/sekolah/program).
4. **Mekanisme:** cari dasar ilmiah solusi sesuai bidang juri (lihat tabel di atas). Jangan memaksakan rumus kalau esainya ilmiah populer.
5. **Bukti yang bertentangan:** catat di tabel terpisah, untuk bahan kontra-argumen.
6. Tulis `<L>/riset/dossier.md`: per pertanyaan, 3–5 butir temuan + sumber + seberapa kuat buktinya.

## Checkpoint
Tunjukkan dossier, peta klaim (berapa ✅ / ⚠️), dan celah bukti. Klaim tanpa bukti dilemahkan atau dibuang sebelum masuk kerangka. Kalau dua dari tiga pertanyaan bukti utama tidak terjawab, laporkan ke penulis dan usulkan kembali ke ide cadangan dari Arena Ide (`ide/final.md`).
