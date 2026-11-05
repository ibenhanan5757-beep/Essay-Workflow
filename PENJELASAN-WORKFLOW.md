# Penjelasan Lengkap Workflow Esai Lomba (100% AI)

Dokumen ini menjelaskan, dari awal sampai akhir, apa yang sudah dibangun, bagaimana cara kerjanya, dan kenapa setiap bagian dirancang begitu.

---

## 1. Gambaran besar

Workflow ini tertanam di folder ini:

| Tempat | Isi | Dipakai kapan |
|---|---|---|
| **Folder `D:\Playground\new essay`** | Workflow lengkap: panduan 8 tahap, alat Python, template, folder per lomba | Saat Claude dibuka di folder ini (Claude Desktop/Cowork/Code). Ini versi utama dan paling lengkap. |

> Untuk Arena Ide dengan subagent dan alat Python, buka folder ini di Claude Desktop/Cowork/Code.

Prinsip desainnya:
1. **Satu workflow untuk semua lomba.** Setiap lomba punya folder sendiri di `lomba/<nama>/`.
2. **100% AI menulis, kamu mengarahkan.** Claude meriset, membuat kerangka, menulis, me-review, dan merevisi. Kamu memilih arah dan menyetujui di setiap checkpoint.
3. **Aturan lomba menang atas default.** Semua angka bawaan (panjang, jumlah sumber, alokasi kata) hanya berlaku kalau guidebook tidak mengatur.
4. **Tidak ada sumber atau angka karangan.** Ini pengaman terpenting, karena satu referensi palsu bisa menggugurkan naskah.
5. **Mesin mengecek yang bisa dicek mesin** (format, jumlah kata, sitasi). Tenaga AI dan kamu dipakai untuk hal yang butuh penilaian (ide, argumen, analisis).

---

## 2. Dari mana asalnya

| Sumber | Yang diambil |
|---|---|
| **academic-research-skills** (Imbad0202) | Cek kualitas tulisan, model pendahuluan CARS, rantai Klaim–Bukti–Penalaran, tangga kekuatan klaim, pertanyaan Sokratik, katalog sesat pikir, hierarki kualitas sumber, reviewer devil's advocate |
| **AI-Research-SKILLs** (Orchestra) | Kerangka brainstorming dan berpikir kreatif (ketegangan, "apa yang berubah", tangga abstraksi, rotasi pemangku kepentingan, bisosiasi), serta aturan anti-halusinasi sitasi |
| **hallmark** (Nutlope) | Prinsip desain anti-"desain AI" untuk sampul, poster, dan lampiran visual |
| **Master SOP Juara** (dokumenmu) | Bedah guidebook dan psikologi juri, turnamen ide + pre-mortem, lokus spesifik, dossier riset, loop juri, build DOCX otomatis. Bagian yang bermasalah tidak dipakai (lihat `catatan/kritik-sop-juara.md`). |
| **Skill Antigravity** (daftarmu) | Inspirasi alat pencari jurnal; dibuat ulang sebagai `tools/cari_sumber.py` |
| **naskah-id** (nothinx, MIT) | Kaidah bahasa Indonesia baku: EYD V, kata baku KBBI, kalimat efektif, pola tulisan AI dalam bahasa Indonesia, dan alat `periksa.py` (cek kaidah + bandingkan angka/sitasi antar versi) |
| **advanced-evaluation** (Agent-Skills-for-Context-Engineering, MIT) | Cara merancang juri AI yang adil: alasan sebelum skor, tukar posisi di setiap adu, seri kalau dua urutan tidak sepakat, netral terhadap panjang dan nada yakin |

File asli semua repo ada di `skills/` sebagai rujukan, dikelompokkan per kegunaan: `skills/esai/`, `skills/desain/`, `skills/presentasi/`.

### Aturan: pemakaian skill
Prinsipnya: **isi esai dari folder ini, skill akun hanya untuk mengurus file dan mencari paper.**

- **Skill folder** (`workflow/`, `templates/`, `skills/`, `.claude/agents/`, `tools/`) mengerjakan semua yang menentukan isi esai: ide, riset, argumen, tulisan, juri, visual. Versinya terkunci dan ikut terbawa kalau folder dipindah.
- **Skill akun** hanya boleh dari daftar izin: `pdf`, `docx`, `pptx`, dan connector Consensus/SciSpace (untuk menemukan paper, lalu tetap diverifikasi dengan `cari_sumber.py`). Skill akun lain tidak dipakai walaupun muncul di daftar Skills, termasuk skill penulisan akademik umum dan skill pengakal detektor AI.
- Kalau ada langkah yang tidak tercakup, Claude mencari kandidat, melaporkannya kepadamu, dan baru menyalinnya ke `skills/` setelah kamu setuju.

Aturan lengkapnya ada di `CLAUDE.md` § Pemakaian skill, dan petanya di § Peta Skill per tahap.

Ringkasan peta:

| Tahap | Skill utama |
|---|---|
| 0 Bedah guidebook | `baca_pdf.py`, `pdf` (akun, halaman scan) |
| 1 Arena Ide | `cari_sumber.py` + WebSearch (bekal), brainstorming + creative-thinking (ide), **advanced-evaluation** + agen `juri-ide` (juri), `arena.py` |
| 2 Riset | `cari_sumber.py`, WebFetch, Consensus/SciSpace (akun, menemukan paper), peta klaim |
| 3 Kerangka | argument builder, CARS, pertanyaan Sokratik |
| 4 Draf | **naskah-id**, anti-slop, `buat_visual.py` |
| 5 Loop juri | agen `juri-esai` + `auditor-sitasi`, advanced-evaluation, devil's advocate + serangan tunggal, `cek_naskah.py`, `cek_klaim.py`, `periksa.py` |
| 6 Revisi & build | `periksa.py --banding`, `build_docx.py`, `cek_docx.py`, `pdf` (akun, render halaman) |
| 7 Visual | `skills/desain/` (hallmark, impeccable, design) |
| 7C PPT | `skills/presentasi/slides/`, `cek_pptx.py`, `pptx` (akun) |

Celah yang tersisa: cek plagiarisme resmi (Turnitin) tidak bisa diakses, diganti `cek_naskah.py --sumber`. KBBI daring belum punya skill, diganti daftar kata baku di naskah-id.

---

## 3. Struktur folder

```
CLAUDE.md                 ← "otak" workflow: dibaca Claude pertama kali
README.md                 ← cara pakai singkat untukmu
PENJELASAN-WORKFLOW.md    ← dokumen ini
MULAI-DI-WINDOWS.md       ← pasang Python, paket, PDF; kalau macet
ISTILAH.md                ← daftar istilah
workflow/                 ← panduan detail tahap 0–7 + MODE-KILAT.md
tools/                    ← alat Python + tes_alat.py
templates/                ← log sumber + peta klaim, rubrik, format review, prompt juri/auditor, prompt Arena Ide
.claude/agents/           ← juri buta: juri-ide, juri-esai, auditor-sitasi (tanpa CLAUDE.md, tanpa akses file)
lomba/_template/          ← kerangka folder lomba baru
lomba/<nama-lomba>/       ← satu folder per lomba
    guidebook.pdf
    aturan.md             ← hasil bedah guidebook
    profil.json           ← format lomba dalam bentuk mesin (untuk alat)
    STATUS.md             ← progres, tenggat, keputusan, log prompt
    ide/                  ← hasil Arena Ide (bekal, pasaran, loop-1..3, final; JSON juri di ide/juri/)
    riset/                ← sumber.md (log + peta klaim), teks/ (teks sumber asli), dossier.md
    draf/                 ← kerangka, draf-v1, review-v1, ..., final
    kirim/                ← DOCX, PDF, lampiran administrasi
lomba/ewc-siswa-pharfest-2026/  ← contoh hasil tahap 0
catatan/                  ← kritik SOP juara, audit, catatan perubahan
skills/                   ← file asli repo rujukan + lisensi (esai/, desain/, presentasi/)
arsip/                    ← file struktur lama yang sudah tidak dipakai
```

**Kenapa panduan dipecah per tahap?** `CLAUDE.md` sudah berisi alur lengkap dalam satu halaman. File di `workflow/` hanya dibaca saat tahapnya berjalan, jadi konteks Claude tidak penuh oleh aturan tahap lain, dan satu tahap bisa diubah tanpa menyentuh tahap lain.

---

## 4. Cara memulai dan melanjutkan

**Lomba baru:** buka folder di Claude lalu bilang *"Lomba baru: [nama], guidebook-nya ini"* sambil melampirkan PDF. Claude akan:
1. Menyalin `lomba/_template/` menjadi `lomba/<nama>/` dan menaruh guidebook di sana
2. Menjalankan tahap 0
3. Berhenti di checkpoint dan menunggu persetujuanmu

**Melanjutkan:** bilang *"Lanjutkan lomba [nama]"*. Claude membaca `lomba/<nama>/STATUS.md` dan meneruskan dari tahap terakhir yang belum dicentang.

**Checkpoint:** setiap tahap berakhir dengan Claude menunjukkan hasil. Kamu bisa menyetujui, mengoreksi, atau meminta alternatif. Claude tidak lanjut ke tahap berikutnya tanpa persetujuanmu.

---

## 5. Tahap demi tahap

### Tahap 0 — Bedah guidebook
**Tujuan:** mengubah guidebook menjadi aturan yang bisa dicek dan strategi yang jelas, sebelum satu kata pun ditulis.

Hasilnya:
1. **Matriks kepatuhan**: setiap aturan yang bisa mendiskualifikasi atau mengurangi nilai (batas kata, format halaman, larangan nama/logo, posisi gambar, gaya sitasi, struktur, nama file, lampiran administrasi, boleh kirim ulang atau tidak, tenggat lengkap dengan jam dan zona waktu), masing-masing dengan halaman guidebook dan cara mengeceknya.
2. **`profil.json`**: format lomba dalam bentuk yang dibaca alat (font, ukuran, spasi, margin, indent, posisi nomor halaman, batas kata, gambar hanya di lampiran atau tidak).
3. **Ambiguitas**: aturan yang tidak jelas atau bertentangan dicatat, dan dipilih tafsiran yang paling aman.
4. **Aturan AI**: dicek dan dikutip. Kalau guidebook melarang AI atau mewajibkan pernyataan "karya sendiri", Claude memperingatkanmu.
5. **Peta rubrik**: kriteria mana yang murah dinaikkan (format, bahasa: kerjakan sempurna dengan alat) dan mana yang mahal (orisinalitas, analisis: di sinilah waktu dihabiskan).
6. **Profil juri**: siapa jurinya, apa yang mereka anggap dangkal, apa yang mereka anggap salah, dan jenis esainya (ilmiah populer, LKTI, opini, reflektif).
7. **Garis waktu mundur** dari tenggat, dengan buffer H-1 kalau tidak boleh kirim ulang, plus perkiraan waktu per tahap. Kalau sisa waktu ≤ 5 hari, Claude menawarkan **Mode Kilat** (`workflow/MODE-KILAT.md`), tapi jalur penuh tetap default.

### Tahap 1 — Arena Ide (tahap terpenting)
**Kenapa:** hipotesisnya, banyak lomba punya dua lapis penilaian. Lapis pertama penyaringan (mungkin dengan AI) yang menilai kualitas tulisan, lalu lapis kedua juri manusia yang subjektif dan sangat ditentukan oleh **ide**. Esai yang sempurna dengan ide biasa bisa peringkat 1 di penyaringan lalu jatuh di babak juri. Karena itu ide diadu habis-habisan sebelum menulis. Tahap ini tidak melibatkan kehidupan pribadimu; semuanya dari riset dan brainstorming.

1. **Bekal**: riset cepat per subtema (data terbaru, regulasi, kegagalan solusi yang ada).
2. **Ide pasaran**: utamanya dari **judul/abstrak juara dan finalis sungguhan** 2–3 edisi sebelumnya (dari kamu atau dicari di web, dengan link). Kalau tidak ada, subagent tanpa konteks memprediksi 3–5 ide pasaran per subtema, dengan label "(prediksi)". Daftar ini jadi anti-referensi sekaligus batas bawah: ide yang hanya setara juara tahun lalu belum cukup mengejutkan.
   **Peta subtema**: setiap subtema dinilai keramaiannya, ruang kebaruannya, ketersediaan datanya, dan kecocokannya dengan juri. Kalau lomba tidak punya subtema, tema dipecah jadi 4–6 sudut.
   **Tambang literatur**: 15–30 artikel jurnal terbaru per subtema dibaca untuk mencari benih ide: temuan baru yang belum diterapkan di Indonesia, celah yang ditulis peneliti sendiri, metode dari bidang lain, dan hasil yang melawan anggapan umum. Benih ini masuk ke generator loop 2–3 lewat lensa "jembatan riset ke lokal", dan ide yang lahir darinya sudah membawa DOI. Peserta lain jarang membaca jurnal, jadi jalur ini menghasilkan ide yang tidak pasaran sekaligus mudah dibuktikan.
3. **3 loop**, masing-masing:
   - Generator membuat **12 ide** dengan set lensa berbeda per loop (A: ketegangan, "apa yang berubah", kegagalan solusi, pemangku kepentingan · B: analogi lintas bidang, inversi, tangga abstraksi, komposisi · C: lokal ekstrem, insentif ekonomi, *adjacent possible*, kontra-intuitif). Loop 2–3 wajib menjauh dari ide loop sebelumnya. **Kuota subtema:** loop 1 mencakup semua subtema; loop 2–3 memberi 8 ide untuk 2–3 subtema terkuat dan 4 ide untuk subtema lain atau ide lintas-subtema. Setiap ide tetap berinduk ke satu subtema.
   - Kartu ide **dibersihkan** (kolom lensa dan "kenapa tidak pasaran" dibuang), lalu **diacak dengan skrip** (`tools/arena.py acak`, seed dicatat).
   - **3 juri buta** (agen proyek `juri-ide`: tanpa CLAUDE.md, tanpa akses file; ≥1 juri memakai model berbeda dari generator; persona akademisi / praktisi / "juri yang sudah membaca 100 esai") menilai dengan **rubrik sendiri** (`templates/rubrik-ide.md`), bukan rubrik guidebook. Satu subagent terpisah memberi **kesan 30 detik** dari nama + inti ide saja.
     - Gerbang (gugur kalau gagal): tepat tema · benar secara ilmiah · aman/etis · **layak untuk jenjang**
     - Skor: **Kejutan 25%** · **Reframing/insight 20%** (keduanya = *WOW factor*, 45%) · Bisa dibayangkan 15% · Daya bela di rapat juri 10% · Tahan serangan 10% · Kelayakan 10% · Bisa dibuktikan 10%
     - Jangkar skor 2/5/9 + distribusi wajib supaya tidak semua ide dapat nilai tinggi
     - Pemeriksaan wajib: uji 30 detik (kesan pertama), ide pasaran terdekat, pertanyaan pembunuh, frasa satu baris
     - Pertanyaan pembela: "ide mana yang akan kamu bela di rapat juri?"
     - Juri wajib menulis alasan sebelum angka, dan diminta tidak terpengaruh panjang kartu atau nada yakin (dari advanced-evaluation)
   - Juri mengembalikan JSON. Peringkat dihitung **skrip** (`tools/arena.py rekap`: median, gugur gerbang mayoritas, seri dipecah K1+K2), lalu **Top 3** mendapat kritik dan saran dari juri baru.
   - Semua disimpan ke `ide/loop-N.md`.
4. **Final, 9 finalis**: diperkuat pakai kritik juri → **setiap finalis wajib punya ≥2 data pendukung nyata** (yang tidak mencapainya tidak ikut final) → panel juri final baru → **Top 4 diadu berpasangan, bolak-balik** (12 adu, poin dihitung `arena.py adu`). Kalau kedua urutan memilih ide yang sama, ide itu dapat 1 poin. Kalau tidak sepakat, hasilnya seri (0,5–0,5), karena itu tanda bias posisi. → juara + cadangan. Kalau riset tahap 2 untuk juara gagal, workflow kembali ke cadangan.
5. **Tesis 2 kalimat + 3–5 kandidat judul** dari ide juara.
6. **Checkpoint**: kamu memilih dari Top 9, juara, dan cadangan.

### Tahap 2 — Riset & dossier
Aturan keras:
- Setiap sumber dicari dengan alat, dibuka, dan dibaca. Yang belum terverifikasi ditandai `[PERLU SUMBER]`.
- Angka hanya dari sumber. Kalau tidak ada data, tulis sebagai estimasi dengan asumsi eksplisit, atau buang.
- "Sumber ditemukan" tidak sama dengan "sumber mendukung klaim".
- Paper yang sudah ditarik (retracted) tidak dipakai.

Langkahnya: turunkan 3–5 pertanyaan bukti dari tesis, cari jawabannya dengan `cari_sumber.py`, simpan ke `riset/sumber.md`, simpan teks aslinya ke `riset/teks/` (dengan URL dan tanggal akses), baca, lalu tulis **peta klaim**: setiap klaim faktual diberi ID (K1, K2, ...) beserta **kutipan verbatim ≤40 kata** dari sumber, halaman, dan kekuatan buktinya. Baru setelah itu statusnya ✅. Kumpulkan data lokus, dasar ilmiah solusi sesuai bidang juri, dan **bukti yang bertentangan** dengan tesis. Hasil akhirnya `riset/dossier.md`: ringkasan bukti per pertanyaan beserta kekuatannya. Penanda `[PERLU ...]` diselesaikan dengan prosedur tetap: cari maksimal 3 kali, kalau gagal klaimnya dilemahkan atau dihapus.

Urutan prioritas sumber: data resmi → tinjauan sistematis → jurnal peer-review → regulasi → laporan lembaga → berita (hanya untuk kasus) → preprint/opini. Panduan riset juga punya tabel sumber data Indonesia per bidang (kesehatan, lingkungan, ekonomi, pendidikan, teknologi, pertanian, sosial).

### Tahap 3 — Kerangka argumen
- **Pohon argumen**: tesis → 2–3 argumen (tidak dipaksa jadi 3) → kontra-argumen terkuat beserta bantahannya → solusi (siapa, apa, bagaimana, kenapa realistis).
- **Klaim–Bukti–Penalaran** untuk setiap argumen. Penalaran wajib ada, karena bukti tanpa penalaran hanya tempelan data.
- **Strategi kontra-argumen**: bantah, akui lalu batasi, ubah sudut pandang, atau akui sebagai keterbatasan.
- **Pendahuluan model CARS**: (1) kenapa penting sekarang, pakai data; (2) celah yang didukung riset; (3) tesis tegas yang menjawab celah itu.
- **Alokasi kata** (default kalau guidebook tidak mengatur): pendahuluan 15%, isi 55%, solusi 20%, penutup 10%.
- **Seleksi judul** dengan checklist.

### Tahap 3b — Rencana visual (bersama kerangka)
- Visual diputuskan saat menyusun argumen, bukan ditempel di akhir. Setiap calon visual harus lolos tiga pertanyaan: kalau dihapus, apakah juri kehilangan sesuatu? Apa satu pesannya? Dari mana datanya?
- Menu: grafik data, diagram mekanisme/alur, tabel pembanding, gambar prototipe/konsep (diberi label "ilustrasi konsep"), foto berlisensi jelas, peta lokasi, infografis (hanya kalau dinilai). Patokan 1 visual per 600–800 kata, paling banyak 3–4.
- Grafik dan diagram dibuat `tools/buat_visual.py`: font sama dengan naskah, satu warna aksen + abu-abu, tanpa gradasi, 3D, atau glow, tetap terbaca kalau dicetak hitam-putih. Palet khas AI (gradasi ungu-biru, warna bawaan framework, cyan menyala di latar gelap) dilarang.

### Tahap 4 — Menulis draf
Claude menulis seluruh draf dari kerangka yang sudah disetujui. Kamu memberi arahan, Claude merevisi.

Urutan menulis: isi → solusi → pendahuluan → penutup → judul.

Gaya disesuaikan dengan jenis esai: ilmiah populer (akurat tapi bahasa awam), LKTI (lebih teknis, hanya dengan data nyata), opini (satu posisi tegas), atau reflektif (pengalaman jadi tulang punggung).

**Anti-slop**, yang dihindari:
- Pembuka kosong seperti "Di era digital saat ini", "Tidak dapat dipungkiri", "Dalam rangka", dan seterusnya
- Kata yang terlalu sering dipakai: krusial, holistik, sinergi, transformatif, dan seterusnya
- Pola khas AI: daftar selalu 3 butir, paragraf berstruktur seragam, "bukan sekadar X melainkan Y" berulang, kalimat bijak di akhir setiap paragraf, tanda pisah berlebihan, klaim menggelembung

Penggantinya: detail konkret (tempat, angka, tahun), panjang kalimat yang bervariasi, dan pendapat yang berani tapi dibatasi dengan jujur. Ejaan mengikuti EYD V.

Draf hanya boleh memakai fakta dari peta klaim yang berstatus ✅. Kalimat yang memakai klaim diberi ID (`<!--K3-->`, tidak tercetak). Draf disimpan sebagai `draf/draf-v1.md`, lalu langsung dicek dengan `cek_naskah.py` dan `cek_klaim.py` (setiap angka di draf harus ada di peta klaim).

### Tahap 5 — Loop juri
Ini perbaikan terbesar dari SOP Juara. Desain loopnya:
1. **Cek mesin dulu**: `cek_naskah.py` (format, kata, sitasi, klise), `cek_klaim.py` (angka vs peta klaim), `periksa.py` (kaidah), dan `cari_sumber.py cek-pustaka` (sumbernya ada, penulis/tahun cocok, tidak ditarik).
2. **Auditor sitasi**: subagent baru hanya menerima pasangan (kalimat naskah, kutipan sumber) dan menilai: mendukung / sebagian / tidak mendukung. "Tidak mendukung" = temuan Kritis.
3. **Juri di konteks baru** (agen `juri-esai`, setiap peran panggilan terpisah): skor utama memakai **rubrik resmi lomba dengan bobot resmi**. Lapis kedua memakai rubrik sendiri (`templates/rubrik-esai.md`): **penyaring** (bahasa, alur, bukti, bebas jejak AI) dan **juri manusia** (ide terasa dalam ±100 kata pertama, momen "aha", bisa dibayangkan, tahan serangan, kredibilitas ahli, melekat) untuk mencari perbaikan yang membuat esai menonjol.
4. **Setiap skor dan temuan wajib disertai kutipan bukti** dari naskah. Tanpa kutipan, tidak sah.
5. **Devil's advocate**: juri paling skeptis yang hanya mencari kelemahan, yaitu lompatan logika, keberatan yang belum dijawab, salah istilah bidang, solusi yang tidak realistis, dan kalimat khas AI. Temuan Kritis/Mayor-nya **dikonfirmasi** juri lain di konteks baru. Yang tidak sah diturunkan jadi Minor, supaya loop bisa benar-benar berhenti.
6. **Tangga kekuatan klaim**: mungkin menunjukkan < berkaitan dengan < memprediksi < berkontribusi pada < memengaruhi < menyebabkan/membuktikan. Klaim tidak boleh lebih tinggi dari buktinya.
7. **Tingkat temuan berdasarkan dampak**: Kritis (tesis runtuh, fakta salah, sumber palsu, kalimat tidak didukung sumbernya, melanggar aturan), Mayor (argumen utama melemah, atau satu kriteria resmi turun di bawah 7), Minor (bahasa).
8. **Syarat berhenti**: tidak ada kriteria rubrik resmi < 7, tidak ada temuan Kritis/Mayor yang terkonfirmasi, dan auditor sitasi tidak memberi "tidak mendukung". Maksimal 3 putaran. Tidak ada target "skor >98", karena target angka membuat AI memuaskan juri tiruan, bukan juri asli.
9. **Perbandingan berpasangan**: versi baru dibandingkan dengan versi lama per kriteria. Perubahan yang membuat naskah lebih buruk dibatalkan, dan karena itu setiap perubahan dicatat bersama kriteria yang disasarnya.

### Tahap 6 — Revisi & build file
- Revisi dikerjakan Kritis → Mayor → Minor, dan setiap perubahan dicatat.
- Kekuatan klaim tidak boleh digeser diam-diam (misalnya menghapus batasan atau menaikkan "berkaitan" jadi "menyebabkan").
- Setiap versi disimpan (`draf-v1`, `draf-v2`, ...).
- **Build otomatis**: `build_docx.py` mengubah `final.md` menjadi DOCX dan PDF persis sesuai `profil.json`. Build ditolak kalau masih ada penanda `[PERLU ...]`, dan metadata penulis di DOCX dikosongkan. Tampilannya dibuat seperti artikel jurnal: judul bagian memakai Heading Word berwarna hitam, tabel tiga garis, keterangan gambar/tabel lebih kecil dengan baris sumber, dan gambar berukuran seragam.
- **Cek tampilan**: `cek_docx.py` menangkap tanda "format AI" di file Word (emoji, teks berwarna, tebal berlebihan, poin-poin, Enter berulang, gambar tanpa keterangan atau sumber, metadata), lalu setiap halaman PDF dilihat.
- **Checklist akhir**: cek naskah bersih, pustaka terverifikasi, angka dicocokkan ulang dengan sumber, DOCX/PDF dibuka dan dicek, nama file sesuai aturan, lampiran administrasi siap, dan dikirim sebelum H-1.

### Tahap 7 — Visual, lampiran, presentasi (opsional)
- Cek dulu apakah visual dinilai. Kalau tidak, cukup 1–2 tabel atau grafik yang membantu argumen, dan hanya dari data asli.
- Sampul atau poster (hanya kalau diminta) memakai prinsip Hallmark: tanpa data/logo/kutipan karangan, tanpa gradasi ungu-biru atau ilustrasi AI generik, satu gagasan per halaman, dan satu ciri khas yang ditampilkan besar.

### Tahap 7C — Presentasi/PPT (hanya kalau kamu minta)
- Tidak pernah jalan otomatis. Workflow selesai di file Word/PDF; PPT dibuat hanya kalau kamu meminta PPT, slide, atau pitch deck.
- **Kalau kamu memberi contoh PPT**, contohnya dibaca (`cek_pptx.py gaya` + dilihat per slide) lalu digolongkan: template wajib panitia (dipakai apa adanya, hanya diisi), contoh gaya (ditiru gayanya, bukan isinya), contoh juara (dipelajari alurnya), atau tanpa contoh (gaya bawaan). Kalau contoh gaya punya ciri slide AI, kamu ditanya sekali mau diikuti persis atau tanpa ciri itu.
- Alur slide khusus lomba (bukan pitch investor): pembuka → masalah dengan angka → celah → gagasan → cara kerja → bukti → kelayakan → dampak → penutup, plus slide cadangan untuk tanya-jawab.
- Lantai anti-slop slide: judul berupa kalimat kesimpulan, ≤30 kata dan ≤3 butir per slide, huruf ≥18 pt, maksimal 2 font, satu warna aksen, tanpa gradasi ungu, emoji, ikon tempelan, glow, atau slide "Terima Kasih" kosong. Dicek otomatis dengan `cek_pptx.py cek`.
- Naskah bicara per slide (±130 kata per menit), simulasi 3 juri, dan 5 pertanyaan paling mematikan beserta jawaban dan sumbernya.

---

## 6. Alat (`tools/`)

| Alat | Fungsi | Status uji |
|---|---|---|
| `cari_sumber.py` | **cari**: OpenAlex, arXiv, PubMed, Europe PMC, Semantic Scholar (filter tahun, open access, simpan ke log) · **doi**: verifikasi di Crossref/DataCite + cek retraksi + format APA 7 · **cek-pustaka**: verifikasi seluruh daftar pustaka draf (DOI, judul, penulis pertama, tahun, retraksi; entri tanpa DOI didaftar untuk cek manual) · **fda**: recall & label obat (FDA AS) · **uji-klinis**: ClinicalTrials.gov | Diuji ke API sungguhan ✅. OpenAlex & Semantic Scholar sebaiknya memakai kunci API gratis |
| `cek_naskah.py` | jumlah kata isi vs batas, semua bentuk `[PERLU ...]`/TODO tersisa, nama/sekolah yang terselip (kata utuh), sitasi tanpa pustaka dan sebaliknya (termasuk singkatan lembaga, "dan", et al., [n]), frasa klise, gambar di luar lampiran, paragraf/kalimat terlalu panjang, dan `--sumber`: kalimat ≥8 kata yang tersalin mentah dari `<L>/riset/teks/` | Tes otomatis ✅ |
| `cek_klaim.py` | setiap angka di draf ada di peta klaim; setiap ID `<!--Kn-->` ada dan berstatus ✅ | Tes otomatis ✅ |
| `arena.py` | acak dengan seed, median skor juri, gugur gerbang, poin adu berpasangan | Tes otomatis ✅ |
| `skills/esai/naskah-id/scripts/periksa.py` | kaidah EYD V/KBBI + klise mesin; `--banding` angka/sitasi/kutipan yang berubah antar versi | `--tes` lulus 108/108 ✅ |
| `build_docx.py` | Markdown → DOCX + PDF sesuai profil: kertas (A4/F4/Letter/Legal), font, ukuran, spasi, margin, justify, indent, judul, `###`, daftar, nomor halaman atas/bawah, pustaka satu entri per baris dengan hanging indent, keterangan gambar, lampiran di halaman baru, metadata penulis dikosongkan, menolak build kalau ada `[PERLU ...]` | Tes otomatis ✅ |
| `baca_pdf.py` | teks guidebook per halaman (`=== Halaman N ===`) | — |
| `buat_visual.py` | grafik (batang, garis) dan diagram (alur, siklus) dari JSON, gaya tenang ala jurnal | Tes otomatis ✅ |
| `cek_pptx.py` | cek slide buatan AI + baca gaya PPT contoh | Tes otomatis ✅ |
| `cek_docx.py` | cek tampilan file Word: font, warna, emoji, tebal, keterangan & sumber gambar/tabel, metadata | Tes otomatis ✅ |
| `tes_alat.py` | 43 tes untuk semua alat (termasuk bug yang ditemukan audit) | `python tools/tes_alat.py` |
| `frasa_slop.txt` | daftar frasa klise, bisa kamu tambah sendiri | — |

Instalasi: lihat `MULAI-DI-WINDOWS.md`. Ringkasnya Python 3.8+, `pip install python-docx pypdf matplotlib python-pptx`, dan untuk PDF LibreOffice atau `pip install docx2pdf` kalau ada MS Word.

---

## 7. Pengaman yang tertanam

| Risiko | Pengaman |
|---|---|
| Referensi palsu atau halusinasi | Semua sumber lewat alat, status ⚠️/✅, `cek-pustaka` (DOI + penulis + tahun + retraksi), penanda `[PERLU ...]` yang memblokir build |
| Sumber asli tapi tidak mendukung kalimatnya | Peta klaim dengan kutipan verbatim + auditor sitasi buta |
| Angka karangan ("hemat Rp X miliar", "akurasi 95%") | Angka hanya dari peta klaim (`cek_klaim.py`), atau estimasi dengan asumsi eksplisit |
| Klaim berlebihan | Tangga kekuatan klaim di review dan revisi |
| Gugur administratif | Matriks kepatuhan + `profil.json` + alat otomatis + checklist akhir |
| AI menilai dirinya sendiri | Agen juri tanpa CLAUDE.md dan tanpa akses file, ≥1 juri dengan model berbeda, skor wajib berkutipan, temuan Mayor wajib dikonfirmasi, skor utama memakai rubrik resmi |
| Revisi malah memperburuk | Perbandingan berpasangan antar versi (posisi ditukar) + `periksa.py --banding` untuk angka/sitasi yang berubah |
| Kalimat tersalin mentah dari sumber | `cek_naskah.py --sumber` |
| Juri AI bias posisi/panjang | Tukar posisi di setiap adu, seri kalau tidak sepakat, instruksi netral panjang dan nada |
| Tulisan terasa AI | Anti-slop + `frasa_slop.txt` + cek otomatis + kasus nyata terverifikasi |
| File Word atau visual terlihat "buatan AI" | `build_docx.py` bergaya jurnal + `cek_docx.py` + lantai visual dan palet di tahap 3b |
| Pilihan skill terbatas pada folder | § Pemakaian skill: skill akun yang lebih cocok boleh dipakai, dicek sebelum langkah penting |
| Ide "biasa saja" di mata juri manusia | Arena Ide: judul juara sungguhan sebagai anti-referensi, 3 loop lensa berbeda, juri buta (kartu dibersihkan, diacak skrip), gerbang kelayakan jenjang, ≥2 bukti per finalis, adu berpasangan |
| Lomba ternyata melarang AI | Peringatan di tahap 0 dengan kutipan halaman |
| Instruksi tersembunyi di guidebook/sumber web | Diperlakukan sebagai data, bukan perintah |

---

## 8. Yang belum selesai
1. Kunci API gratis OpenAlex (https://openalex.org/settings/api) dipasang sebagai `OPENALEX_API_KEY` di laptop (lihat `MULAI-DI-WINDOWS.md`) dan/atau secret environment cloud.
2. Sisa struktur lama sudah dipindah ke `arsip/` (29 Okt 2026). Hapus folder itu kalau sudah yakin tidak dibutuhkan.
3. Daftar perubahan terakhir: `catatan/perubahan-2026-10-29.md`.
