# Tahap 1 — Arena Ide

**Ini tahap terpenting di seluruh workflow.**

Hipotesis desainnya: banyak lomba menilai dalam dua lapis. Lapis pertama adalah penyaringan (bisa dengan AI atau panitia) yang menilai kerapian, kepatuhan, dan kualitas tulisan. Lapis kedua adalah juri manusia yang menilai secara subjektif, dan yang paling menentukan di sana adalah **apakah idenya terasa baru, tajam, dan berkesan**. Esai yang ditulis sempurna dengan ide "biasa saja" bisa lolos lapis pertama di peringkat atas lalu jatuh di lapis kedua. Karena itu ide diadu habis-habisan **sebelum** satu kalimat esai ditulis.

Sumber lensa: `skills/esai/ai-research-skills/brainstorming-research-ideas.md`, `creative-thinking-for-research.md`. Prompt: `templates/prompt-ide-*.md`. Semua hasil disimpan di `<L>/ide/`. Dasar riset untuk desain versi ini (kolam gabungan, kartu liar, cek "sudah ada?", evolusi, paket esai): `catatan/evaluasi-arena-ide-2026-11.md`.

Tahap ini **tidak melibatkan kehidupan pribadi penulis**. Semua ide berasal dari riset dan brainstorming.

---

## Ringkasan alur

```
Langkah 0  Bekal riset per subtema + ide pasaran (juara sungguhan, prediksi, jawaban chatbot) + peta subtema
Langkah 0b Tambang literatur: benih ide dari jurnal
Langkah 0c Rumusan peluang: 4–8 "Bagaimana kita bisa ...", masing-masing dengan bukti masalahnya nyata
             │
Loop 1     Generator (buat 25–30 ide satu baris → pilih 12 paling berbeda; lensa A; semua peluang tercakup)
             → kartu dibersihkan + diacak (+1–2 kartu jangkar juara lama, kalau ada)
             → 3 juri buta (agen juri-ide, model diputar antarpersona) + 1 kesan 30 detik → JSON
Loop 2     Generator (lensa B + benih jurnal, fokus peluang terkuat + lintas-subtema, menjauh dari loop 1) → juri buta
Loop 3     Generator (lensa C, menjauh dari loop 1–2) → juri buta
             │
Kolam      semua kartu digabung → dedup (arena.py mirip) → rekap semua loop sekaligus
             → 7 finalis + ≤2 kartu liar (arena.py rekap --top 7 --kesan)
             │
Final      kritik finalis → penguatan → ≥2 bukti pendukung + cek "sudah ada?"
             → panel juri final → 1 putaran evolusi (≤2 ide hibrida)
             → Top 4 dibuat jadi paket "bisa jadi esai" → adu berpasangan bolak-balik
             → juara + cadangan, atau "seri" kalau data tidak bisa memisahkan → tesis + kandidat judul
             │
Checkpoint penulis memilih (boleh juara, cadangan, atau finalis lain)
```

---

## Langkah 0 — Bekal (dikerjakan agen utama)

1. **Peta tema** (`<L>/ide/bekal.md`): untuk setiap subtema, 5–10 fakta/data terbaru dari riset cepat (`tools/cari_sumber.py` + sumber resmi), regulasi atau program yang sedang berjalan, dan kegagalan solusi yang sudah ada. Bekal ini supaya ide berangkat dari masalah nyata, bukan khayalan.
   **Kalau riset bekal dibagi ke subagent** (PL11, PL26): pakai model Sonnet (`model: sonnet` ditulis eksplisit, supaya tidak mewarisi Opus), **maksimal 3 berjalan bersamaan**, dan cek `get_usage` dulu. Setiap subagent menulis catatannya ke `<L>/ide/_riset/<subtema>.md`, lalu hanya mengembalikan ringkasan ≤200 kata dan path berkasnya. Agen utama menyusun `bekal.md` dari berkas-berkas itu. Di Pharfest, 6 subagent riset Opus yang berjalan bersamaan menghabiskan limit 5 jam dalam ±15 menit.
2. **Ide pasaran** (`<L>/ide/pasaran.md`, cara lengkap di `templates/prompt-ide-pasaran.md`):
   - **Utama: data sungguhan.** Mulai dari `catatan/bank-juara.md` (juara lomba sebidang yang sudah dikumpulkan di lomba-lomba sebelumnya). Lalu minta penulis, atau cari di web, judul dan abstrak karya juara/finalis 2–3 edisi sebelumnya dari lomba yang sama dan lomba sebidang di jenjang yang sama. Setiap baris diberi link sumbernya, dan judul juara tidak boleh dikarang. **Sisihkan 1–2 juara** sebagai kartu jangkar (lihat "Kartu jangkar" di bawah); juara yang disisihkan tidak ditulis di `pasaran.md` yang dikirim ke juri.
   - **Cadangan: prediksi.** Subagent tanpa konteks memprediksi ide yang paling mungkin ditulis peserta lain (3–5 per subtema) dan subtema mana yang paling ramai. Setiap baris diberi label "(prediksi)".
   - **Jawaban chatbot.** Banyak peserta lain juga memakai AI, dan AI membuat karya kolektif makin seragam (Doshi & Hauser 2024). Subagent baru (sebaiknya model kecil) diberi prompt polos seperti yang akan diketik peserta biasa, lalu jawabannya dicatat dengan label "(chatbot)". Kalau penulis mau, tempel prompt yang sama ke ChatGPT/Gemini dan tambahkan jawabannya.
   Daftar ini jadi **anti-referensi**: generator dilarang menghasilkan yang mirip, dan juri memberi penalti untuk kemiripan. Juara tahun lalu juga jadi batas bawah: ide yang hanya setara dengannya belum cukup mengejutkan.
3. **Peta subtema** (`<L>/ide/peta-subtema.md`): agen utama menilai setiap subtema dengan tabel berikut.

   | Subtema | Keramaian (berapa banyak peserta kemungkinan memilih) | Ruang kebaruan (seberapa banyak sudut yang belum digarap) | Ketersediaan data | Kecocokan dengan keahlian juri |
   |---|---|---|---|---|

   Subtema yang ramai belum tentu buruk: ide yang benar-benar baru di subtema ramai justru paling mencolok, karena juri membandingkannya langsung dengan banyak esai yang mirip. Tapi subtema ramai menuntut kejutan yang lebih tinggi. Peta ini dipakai untuk membagi kuota ide di loop 2–3.

Kalau lomba **tidak punya subtema** (hanya tema besar), agen utama memecah tema menjadi 4–6 "sudut" sendiri (misalnya per sektor, pelaku, atau jenis masalah), lalu sudut-sudut itu diperlakukan seperti subtema.

## Langkah 0b — Tambang literatur (benih ide dari jurnal)

Banyak ide juara lahir dari temuan riset yang **sudah ada tapi belum sampai ke konteks lokal**, atau dari celah yang ditulis sendiri oleh peneliti. Peserta lain jarang membaca jurnal, jadi benih dari sini cenderung tidak pasaran dan sekaligus mudah dibuktikan.

**Cara:**
1. Untuk setiap subtema, cari 15–30 artikel 3 tahun terakhir: `python tools/cari_sumber.py cari "<kata kunci bahasa Inggris>" --dari <tahun>` (OpenAlex, arXiv, PubMed, Europe PMC), WebSearch, dan connector Consensus/SciSpace (akun, hanya untuk menemukan paper). Utamakan artikel tinjauan (review), meta-analisis, dan laporan lembaga. Pencarian per subtema boleh dibagi ke subagent dengan aturan yang sama seperti bekal: Sonnet, maksimal 3 bersamaan, hasil ditulis ke `<L>/ide/_riset/`, dan yang kembali hanya ringkasan.
2. Baca abstraknya. Untuk yang menjanjikan, baca juga bagian diskusi, keterbatasan, dan saran penelitian lanjutan.
3. Ambil empat jenis benih:
   - **Temuan baru yang belum diterapkan** di Indonesia atau di kelompok sasaran lomba
   - **Celah dan keterbatasan** yang ditulis peneliti sendiri ("penelitian lanjutan perlu ...")
   - **Metode dari bidang lain** yang bisa dipinjam untuk masalah di tema
   - **Hasil yang berlawanan dengan anggapan umum** (bahan ide kontra-intuitif)
4. Tulis setiap benih sebagai kartu di `<L>/ide/tambang-literatur.md`:

   | Benih (1 kalimat) | Jenis | Sumber (penulis, tahun, DOI) | Bagian yang dibaca | Kenapa relevan untuk subtema | Risiko (terlalu teknis, mahal, data lokal tidak ada) |
   |---|---|---|---|---|---|

   Targetnya 3–6 benih per subtema. Hanya tulis yang benar-benar dibaca; benih dari judul saja tidak boleh.

**Dipakai di mana:**
- Rumusan peluang (Langkah 0c): celah riset dan hasil kontra-intuitif sering menjadi akar masalah yang jarang dibahas.
- Generator Loop 2 dan Loop 3 menerima kartu benih, dengan lensa tambahan **"jembatan riset ke lokal"**: ambil satu temuan, lalu tanyakan siapa di konteks lomba yang paling butuh, apa hambatan penerapannya, dan apa versi sederhananya.
- Ide yang lahir dari benih membawa DOI-nya. Ini menaikkan K7 (bisa dibuktikan) dan membantu syarat ≥2 data pendukung untuk finalis.

**Pengaman:**
- Ide boleh melampaui paper, tapi klaim tidak. Yang belum dibuktikan ditulis sebagai usulan atau hipotesis.
- Ide yang hanya "menerapkan paper X apa adanya" kurang orisinal di mata juri. Benih harus diberi sudut baru: konteks, sasaran, mekanisme, atau gabungan dengan benih lain.
- Sesuaikan dengan jenjang (gerbang G4). Untuk lomba SMA, temuan teknis diterjemahkan ke bahasa yang dipahami juri umum.
- Preprint (arXiv, bioRxiv) ditandai belum ditelaah sejawat.
- Kartu yang dikirim ke juri loop tetap kartu bersih (tanpa DOI dan tanpa asal benih), supaya juri tidak menilai dari "sudah ada jurnalnya".

**Skill:** `tools/cari_sumber.py`, WebSearch/WebFetch, dan connector Consensus/SciSpace (akun, hanya untuk menemukan paper). Dua temuan yang saling bertentangan ditulis berdampingan di kartu benih; risiko benih diisi di kolom Risiko.

## Langkah 0c — Rumusan peluang (masalah dulu, baru solusi)

Lomba ide yang matang (Double Diamond, d.school) memisahkan **merumuskan masalah** dari **mencari solusi**. Reframing (K2, bobot 20%) paling sering lahir di sini, bukan dari lensa yang kebetulan dipakai. Agen utama menulis `<L>/ide/peluang.md` dari bekal dan tambang literatur, tanpa subagent.

1. Untuk setiap subtema, tulis 1–2 peluang dengan pola:
   > **P[n]. Bagaimana kita bisa** [hasil yang diinginkan] **bagi** [kelompok spesifik] **padahal** [hambatan nyata]?
2. Setiap peluang wajib punya:
   - **Bukti masalahnya nyata**: 1–2 data dari bekal atau benih, dengan sumber. Peluang tanpa bukti dibuang.
   - **Akar yang jarang dibahas**: satu kalimat tentang penyebab yang tidak disebut di ide pasaran. Kalau akarnya sama dengan yang dibahas semua orang, tulis ulang peluangnya.
   - **Subtema induk.**
3. Totalnya 4–8 peluang, membentuk pohon: tujuan lomba → peluang → (nanti) ide. Ide yang dikelompokkan per peluang menjaga keragaman secara terstruktur.

Generator menulis nomor peluang di setiap kartu. Di loop 1, setiap peluang mendapat minimal 1 ide.

## Loop 1–3 — Generate → Nilai → Simpan

### Generator (subagent, `templates/prompt-ide-generator.md`)
- Menerima: tema/subtema, ringkasan aturan dan rubrik, bekal, **rumusan peluang**, daftar ide pasaran, **set lensa untuk loop ini**, dan (loop 2–3) daftar semua ide dari loop sebelumnya sebagai "wilayah yang sudah diambil" serta **kartu benih dari tambang literatur** dengan lensa tambahan "jembatan riset ke lokal".
- **Buat banyak, lalu pilih yang paling berbeda.** Generator menulis 25–30 ide satu baris dulu, mengelompokkan yang mirip, lalu memilih 12 yang paling jauh satu sama lain dan dari daftar pasaran. Ide dari satu model dengan satu prompt cenderung seragam, sedangkan menalar langkah demi langkah dan memakai persona menaikkan keragaman (Meincke, Mollick & Terwiesch 2024). Daftar satu baris disimpan di `ide/loop-N.md` sebagai bahan kombinasi.
- Menghasilkan **12 kartu** dalam format yang sama (lihat prompt). Setiap ide wajib menyebut **satu subtema utama** (aturan lomba biasanya hanya membolehkan satu) dan **nomor peluangnya**.
- **Kuota subtema per loop:**
  - **Loop 1 (eksplorasi):** setiap peluang mendapat minimal 1 ide, setiap subtema minimal 1 ide, dan sisanya dibagi rata.
  - **Loop 2–3 (pendalaman):** 8 ide untuk 2–3 subtema/peluang paling menjanjikan (dari peta subtema + rekap loop sebelumnya), dan 4 ide untuk subtema lain atau ide **lintas-subtema** (memakai sudut dari subtema lain, tapi tetap berinduk jelas ke satu subtema). Slot lintas-subtema ini sering melahirkan ide paling mengejutkan.
  - Tidak boleh ada satu subtema yang mengambil lebih dari setengah ide dalam satu loop, kecuali lomba hanya punya 1–2 subtema.
- Set lensa dibagi supaya ketiga loop tidak berputar di wilayah yang sama:

| Set | Lensa |
|---|---|
| **A** (loop 1) | ketegangan/kontradiksi · "apa yang berubah" (teknologi/regulasi/data 2–3 tahun terakhir) · kegagalan solusi yang ada (*failure analysis*) · rotasi pemangku kepentingan |
| **B** (loop 2) | bisosiasi/analogi lintas bidang · inversi/negasi (balik asumsi umum) · tangga abstraksi (naik ke prinsip, turun ke kasus ekstrem) · komposisi/dekomposisi |
| **C** (loop 3) | lokal ekstrem (satu daerah/komunitas spesifik) · ekonomi & insentif (siapa yang mau bayar/bergerak) · *adjacent possible* (apa yang baru bisa dilakukan sekarang) · ide "kontra-intuitif tapi berbukti" |

### Kartu jangkar (kalibrasi juri, hanya loop 1)
Kalau Langkah 0 menemukan judul dan abstrak juara sungguhan, agen utama menulis 1–2 juara yang disisihkan itu sebagai kartu dengan format dan panjang yang sama, lalu memberi ID `X01`, `X02`. Kartu ini diselipkan ke tumpukan loop 1 dan diacak bersama ide lain. Biayanya nol panggilan tambahan.
- Kartu jangkar **tidak pernah** ikut kolam atau finalis. Keluarkan ID `X..` dari daftar sebelum memilih finalis.
- Bacaan: kalau juri menaruh juara sungguhan di **separuh bawah** tumpukan, juri atau rubrik sedang tidak menangkap apa yang dihargai juri manusia lomba ini. Catat di `ide/loop-1.md`, sampaikan ke penulis di checkpoint, dan turunkan keyakinan rekomendasi akhir.
- Kalau tidak ada data juara sungguhan, langkah ini dilewati (jangan pakai prediksi sebagai jangkar).

### Juri buta (3 subagent terpisah, `templates/prompt-ide-juri.md`)
- **Benar-benar buta**: juri dipanggil lewat agen proyek `.claude/agents/juri-ide.md`, yang berjalan tanpa CLAUDE.md dan tanpa alat baca file. Semua bahan (persona, rubrik, pasaran, kartu) dikirim lewat prompt. Kalau agen proyek tidak tersedia (misalnya di sesi cloud), kirim prompt juri yang sudah utuh langsung di pesan ke subagent biasa, perintahkan untuk tidak membuka file apa pun, lalu catat di `ide/loop-N.md` bahwa juri itu tidak dijamin buta.
- **Kartu dibersihkan dulu**: kolom `Lensa`, `Peluang`, dan `Kenapa tidak pasaran` (pembelaan diri generator), nomor asli, dan kata "AI/generator" dibuang. Juri menilai ide, bukan argumen generator tentang idenya sendiri.
- **Urutan ide diacak dengan skrip** untuk setiap juri: `python tools/arena.py acak --seed <angka> I01 ... I12 [X01]`, dengan seed yang dicatat di `ide/loop-N.md`. Labelnya buta (A, B, C, ...).
- **Model per peran, diputar antarpersona.** Agen `juri-ide` memakai **Sonnet** secara bawaan (`model: sonnet` di frontmatter). Tanpa baris itu agen mewarisi model utas utama, sehingga di utas Opus hampir semua juri ikut Opus, padahal Opus memakan kuota beberapa kali lipat Sonnet (PL25). Model lain dipilih per panggilan lewat parameter `model` alat Agent, yang mengalahkan frontmatter:

  | Peran subagent | Model |
  |---|---|
  | Generator (3) | `opus`, ditulis eksplisit (ide adalah prioritas, dan panggilannya hanya 3) |
  | Juri loop (3 per loop) | 2 × Sonnet + 1 × `haiku`; persona yang mendapat Haiku diputar setiap loop |
  | Kesan 30 detik, jawaban chatbot | `haiku` |
  | Prediksi pasaran, kritik finalis, adu berpasangan | Sonnet (bawaan) |
  | Panel final (3) | 1 × `opus` + 2 × Sonnet; catat persona mana yang mendapat Opus |

  Semua juri berbeda model dari generator. **Persona dan model tidak boleh selalu berpasangan sama**: putar di setiap loop (contoh: loop 1 juri "lelah" = Haiku, loop 2 juri "lelah" = Sonnet dan akademisi = Haiku). Di Navigation, juri "lelah" selalu Haiku dan paling sering berbeda pendapat, sehingga tidak bisa diketahui apakah bedanya datang dari persona atau dari model. Model setiap juri dicatat. Semua model ini masih satu keluarga (Claude), jadi bias swa-penilaian hanya teredam sebagian.
- **Kesan 30 detik dipisah**: satu subagent tambahan hanya menerima nama + inti 2 kalimat setiap ide dan memberi reaksi biasa / lumayan / berhenti. Simpan sebagai JSON `ide/juri/kesan-loop-N.json` (`{"I01": "berhenti", ...}`). Juri skor tidak diminta "pura-pura belum membaca detail".
- **Tiga persona**, sesuai profil juri di `<L>/aturan.md`:
  1. Akademisi bidang lomba (ketepatan ilmiah, kedalaman)
  2. Praktisi/pengambil kebijakan (kelayakan, dampak nyata)
  3. Juri "pembaca lelah" yang sudah membaca 100 esai hari ini (mana yang membuatnya berhenti dan berkata "oh, menarik")
- Setiap juri menjalankan gerbang G1–G4 (termasuk **G4 Layak untuk jenjang**, gugur kalau peserta jenjang ini tidak mungkin menjalankan langkah pertamanya), pemeriksaan wajib, dan skor berbobot sesuai `templates/rubrik-ide.md`, lalu mengakhiri jawabannya dengan blok JSON (termasuk `bela`).
- Juri menilai ide **lintas subtema dalam satu tumpukan**, karena pada akhirnya hanya satu esai yang dikirim. Gerbang G1 memastikan setiap ide jelas menjawab subtema yang dipilihnya.
- **Simpan, jangan pilih dulu.** Simpan JSON setiap juri ke `ide/juri/loop-N-J1.json` dst. (label buta dikembalikan ke ID asli). Jalankan `python tools/arena.py rekap ide/juri/loop-N-*.json` hanya sebagai **informasi** untuk memilih subtema/peluang fokus di loop berikutnya. Finalis tidak dipilih per loop, karena dengan cara itu loop yang lemah tetap mendapat kursi sebanyak loop yang kuat.

### Rubrik juri ide (`templates/rubrik-ide.md`)
Rubrik ini **dibuat khusus untuk tujuan menang di babak juri manusia** dan tidak mengikuti rubrik guidebook. Guidebook hanya dipakai untuk gerbang tema, persona juri, dan jenjang.

- **Gerbang (gugur kalau gagal):** G1 tepat tema · G2 benar secara ilmiah, tidak terdengar pseudosains · G3 aman/etis · G4 layak untuk jenjang
- **Skor berbobot:** K1 Kejutan 25% · K2 Reframing/insight 20% · K3 Bisa dibayangkan 15% · K4 Daya bela di rapat juri 10% · K5 Tahan serangan 10% · K6 Kelayakan 10% · K7 Bisa dibuktikan 10%
- **Jangkar skor 2/5/9** per kriteria, plus **distribusi wajib** (maksimal sepertiga ide boleh mendapat K1 ≥8) supaya juri tidak memberi nilai tinggi ke semua ide
- **Pemeriksaan wajib:** uji 30 detik (kesan pertama dicatat sebelum membaca detail), ide pasaran terdekat, pertanyaan pembunuh, dan frasa satu baris
- **Pertanyaan pembela** (panel final & adu): "ide mana yang akan kamu bela di rapat juri?"

Catatan dari data 4 lomba: gerbang hanya menggugurkan 6 dari 261 penilaian. G2 dinilai juri tanpa membuka sumber, jadi jangan menganggap ide yang lolos G2 sudah benar secara ilmiah. Kebenaran ilmiahnya baru diuji di bukti pendukung (Final langkah 3) dan tahap 2.

### Simpan per loop
`<L>/ide/loop-N.md` berisi: daftar 25–30 ide satu baris dari generator, 12 kartu lengkap (dengan subtema dan peluangnya), seed acak, model setiap juri, tabel `arena.py rekap` loop itu, kesan 30 detik, dan (loop 1) posisi kartu jangkar. JSON mentah juri disimpan di `<L>/ide/juri/`. Semua ide disimpan, karena ide peringkat bawah bisa jadi bahan kombinasi.

## Kolam — gabungkan, buang duplikat, pilih finalis

Kualitas proses ide ditentukan oleh **ide terbaiknya**, dan ide yang dibuat terpisah lalu digabung sebelum seleksi lebih baik daripada seleksi per kelompok (Girotra, Terwiesch & Ulrich 2010). Agen utama menulis hasil langkah ini di `<L>/ide/kolam.md`.

1. **Dedup.** `python tools/arena.py mirip ide/loop-1.md ide/loop-2.md ide/loop-3.md`. Skrip hanya menandai pasangan yang kata-katanya mirip (ambang 0,18). Agen utama membaca setiap pasangan: kalau inti dan mekanismenya sama, ide yang mediannya lebih rendah ditandai **duplikat** dan dikeluarkan dari kolam. Kalau sudutnya berbeda, keduanya tetap. Catat setiap keputusan. Duplikat juga bisa lolos dari skrip (kata berbeda, ide sama), jadi baca juga daftar nama ide sekali dari atas ke bawah.
2. **Rekap kolam.** Jalankan rekap atas semua JSON loop sekaligus (tanpa kartu jangkar dan tanpa duplikat):
   ```
   python tools/arena.py rekap ide/juri/loop-*.json --top 7 --kesan ide/juri/kesan-loop-1.json --kesan ide/juri/kesan-loop-2.json --kesan ide/juri/kesan-loop-3.json --kecuali X01,X02,<ID duplikat>
   ```
   `--kecuali` mengeluarkan kartu jangkar dan duplikat dari peringkat.
3. **Finalis = 7 teratas + ≤2 kartu liar.** Median meredam ide yang memecah pendapat (satu juri terpikat, dua lainnya biasa saja), padahal penyeleksi cenderung memilih ide yang aman daripada yang orisinal (Rietzschel, Nijstad & Stroebe 2010). Skrip menandai **KARTU LIAR**: ide di luar 7 teratas yang mendapat nilai tertinggi dari seorang juri, dipilih untuk dibela, atau mendapat "berhenti" di kesan 30 detik. Kartu liar ikut final dengan syarat yang sama (bukti ≥2, cek "sudah ada?").
4. **Batas per subtema.** Kalau satu subtema mengambil lebih dari 6 dari 9 kursi, ganti finalis terbawah subtema itu dengan ide terbaik dari subtema lain yang belum terwakili. Catat penggantiannya.
5. Tabel keluaran skrip, keputusan dedup, dan daftar finalis ditempel ke `ide/kolam.md`.

## Final — finalis menjadi juara

1. **Kritik finalis** (1 subagent juri baru, konteks kosong, `templates/prompt-ide-juri.md` § Kritik & Saran): untuk setiap finalis, kelemahan terbesar, pertanyaan juri manusia yang paling mematikan, dan **satu saran konkret yang membuat ide itu lebih tajam**.
2. **Penguatan**: agen utama merevisi finalis memakai kritik itu. Revisi hanya boleh mempertajam ide, tidak boleh mengganti inti idenya. Penggabungan ide dikerjakan nanti di langkah 5.
3. **Bukti pendukung (wajib)**: setiap finalis harus punya **minimal 2 data pendukung nyata** sebelum masuk panel final. Data dicari dengan `cari_sumber.py` atau sumber resmi, lalu dibuka, dan dicatat dengan link/DOI + satu kalimat temuannya di bawah kartu. Finalis yang tidak mencapai 2 setelah 3 kali pencarian **tidak ikut panel final**. Catat di `ide/final.md` beserta kata kunci yang sudah dicoba.
   **Hemat konteks:** pencarian bukti (langkah 3) dan pencarian untuk cek "sudah ada?" (langkah 4) boleh dibagi ke 1–3 subagent Sonnet, masing-masing ±3 finalis. Setiap subagent menulis hasilnya ke `ide/_riset/finalis-<ID>.md`: link/DOI, satu kalimat temuan, kata kunci yang dicoba, dan tabel karya terdekat. Yang kembali ke utas utama hanya ringkasan. Agen utama tetap **membuka sendiri minimal 1 link bukti per finalis**, dan **vonis cek "sudah ada?" tetap diputuskan agen utama** dari tabel itu. Jumlah minimal bukti dan pencarian tidak berubah.
4. **Cek "sudah ada?" (wajib, terpisah dari bukti pendukung)**. Bukti pendukung menjawab "apakah ide ini benar"; cek ini menjawab "apakah ide ini baru". Pipeline ide yang kuat mencari **tumpang tindih**, bukan hanya dukungan (Scideator, SciMON). Metodenya diadaptasi dari skill `novelty-check` ARIS (lihat `skills/SUMBER.md`). Untuk setiap finalis, agen utama:
   1. **Memecah ide jadi 2–4 unsur inti**: sasaran (siapa yang dibantu), mekanisme (bagaimana gagasan bekerja), konteks/lokus (di mana), dan pembeda dari solusi yang sudah umum. Ide yang dicari sebagai satu kalimat utuh sering lolos dari tumpang tindih sebagian.
   2. **Mencari minimal 3 kali, dengan setiap unsur inti tercakup minimal satu pencarian**:
      - web, dengan inti ide dalam bahasa Indonesia ("<inti ide> program", "<inti ide> desa/sekolah/puskesmas ...");
      - literatur, dengan `cari_sumber.py cari "<inti ide bahasa Inggris>"`;
      - lomba, dengan "lomba esai / LKTI / PKM <kata kunci inti>" (karya atau juara lomba lain dengan ide yang sama).
      Hasil yang paling mirip dibuka (abstrak atau halaman programnya), tidak dinilai dari judul saja.
   3. **Menulis tabel karya terdekat** di bawah kartu, paling banyak 3 baris. Setiap baris wajib punya link yang benar-benar dibuka:

      | Karya / program / juara | Tahun | Link | Unsur yang sama | Bedanya (1 kalimat) |
      |---|---|---|---|---|

   4. **Memberi vonis**, dengan aturan supaya ide bagus tidak digugurkan sembarangan:
      - *tidak ditemukan*: tidak ada karya yang sama di unsur sasaran maupun mekanisme.
      - *sebagian*: ada karya yang sama di sebagian unsur, tapi bedanya bisa ditulis dalam satu kalimat yang jelas. **Kemiripan saja bukan alasan gugur**: wilayah yang ramai tetap boleh dilanjutkan kalau bedanya jelas.
      - *sama*: hanya boleh kalau bisa menyebut **satu karya spesifik** (dengan link) yang sasaran **dan** mekanismenya sama. Vonis *sama* tanpa karya spesifik tidak sah dan diturunkan menjadi *sebagian*.
      Kalau hasilnya *sama*, finalis itu boleh diberi satu kali sudut baru yang jelas berbeda (konteks, sasaran, mekanisme). Kalau tidak bisa, finalis keluar.
   5. **Menulis kalimat posisi** (1 kalimat): "Berbeda dengan [karya terdekat], gagasan ini [pembeda]." Kalimat ini ikut ke paket "bisa jadi esai" dan nanti dipakai di pendahuluan (langkah "tunjukkan celah" di tahap 3).
   Catat kata kunci yang dipakai. Vonis, tabel karya terdekat, dan kalimat posisi ikut dikirim ke juri final dengan judul **Karya serupa yang sudah ada**, supaya K1 dinilai terhadap kenyataan, bukan hanya terhadap daftar pasaran yang sering berupa prediksi.
5. **Panel final** (3 juri baru lewat agen `juri-ide`, model diputar antarpersona, urutan diacak skrip, rubrik sama + **pertanyaan pembela**): menilai finalis yang lolos langkah 3–4, lalu peringkat dihitung dengan `arena.py rekap ide/juri/final-*.json`. Ide yang paling sering dipilih untuk dibela (kolom `Bela`) dicatat sebagai sinyal tambahan.
6. **Evolusi (satu putaran).** Pipeline ide yang kuat tidak berhenti di seleksi; mereka menggabungkan dan memutasi ide terbaik (agen Evolution di Google AI co-scientist). Agen utama membuat **paling banyak 2 ide hibrida** dari 5 teratas panel final:
   - **Gabungan**: dua finalis yang saling melengkapi menjadi satu ide (contoh nyata: di Navigation, I25 "jalan ditinggikan, rumah jadi kolam" cocok menjadi satu lapisan dari I13 "lantai rumah sebagai lingkar pohon").
   - **Mutasi**: satu finalis diubah tepat di kelemahan terbesarnya menurut panel.
   Hibrida wajib memenuhi syarat yang sama (≥2 bukti, cek "sudah ada?"), ditandai `H01`, `H02`, dan **tidak boleh** lebih panjang atau lebih rinci daripada kartu finalis lain. Kalau tidak ada gabungan atau mutasi yang masuk akal, lewati langkah ini dan catat alasannya.
7. **Top 4 untuk adu.** Ambil 4 teratas panel final. Kalau ada hibrida, hibrida terbaik menggantikan peringkat 4, kecuali hibrida itu berasal dari peringkat 1 dan 2 sendiri (adu ide melawan gabungannya sendiri tidak berguna; dalam hal ini hibrida menggantikan salah satu induknya, yaitu yang peringkatnya lebih rendah).
8. **Paket "bisa jadi esai".** Ide LLM cenderung tampak lebih baru di atas kertas tetapi nilainya turun lebih tajam setelah dikerjakan (Si dkk. 2024, 2025). Karena itu adu tidak membandingkan kartu, tetapi paket yang menguji apakah ide bisa menjadi esai yang kuat. Agen utama membuat paket untuk setiap ide Top 4, dengan **format dan panjang yang sama** untuk semua:
   - judul kerja (1 baris);
   - tesis 2 kalimat (pola di bagian "Dari juara ke tesis");
   - 3 poin argumen, masing-masing dengan bukti yang **sudah ditemukan** (link) atau tanda `[belum ada bukti]`;
   - paragraf pembuka ±100 kata, seperti yang akan dibaca juri dalam 30 detik pertama;
   - kontra-argumen terkuat + jawabannya (2 kalimat).
   - kalimat posisi dari cek "sudah ada?" (1 kalimat).
   Paket disimpan di `ide/paket-final.md`. Paket ditulis dengan usaha yang sama untuk semua ide; jangan memoles calon favorit.
9. **Adu berpasangan Top 4** (`templates/prompt-ide-adu.md`): setiap pasangan diadu dua kali dengan urutan dibalik (A vs B, lalu B vs A) untuk menghapus bias posisi. 6 pasangan × 2 = 12 adu. Kalau kedua urutan memilih ide yang sama, ide itu mendapat 1 poin. Kalau tidak sepakat, pasangan itu seri (0,5 poin masing-masing), karena ketidaksepakatan berarti bias posisi. Poin dihitung dengan `python tools/arena.py adu ide/adu-final.json`.
10. **Juara, cadangan, atau seri.** Juara adalah ide dengan poin adu terbanyak, kalau **semua** ini terpenuhi:
    - `arena.py adu` tidak mencetak `SERI/TIPIS` (selisih poin dengan peringkat 2 > 0,5), dan
    - juara adu tidak kalah langsung dari peringkat 2 adu di kedua urutan.
    Kalau tidak terpenuhi, atau kalau peringkat 1 panel final dan juara adu berbeda, hasilnya **seri**: sajikan 2 ide teratas sebagai **Pilihan A** dan **Pilihan B** yang setara, masing-masing dengan kelebihan, kelemahan, dan risiko buktinya, lalu biarkan penulis memilih. Di Navigation dan Pharfest, panel final dan adu memilih ide berbeda, dan Top 4 Navigation hanya terpaut 7,10–7,70. Selisih sebesar itu masih dalam derau juri, jadi menyebut satu juara di situasi seperti ini memberi keyakinan palsu.
11. Hasil disimpan di `<L>/ide/final.md`: tabel kolam dan kartu liar, ranking panel final, hibrida (kalau ada), paket Top 4, matriks adu, juara + cadangan **atau** Pilihan A/B, alasannya, bukti pendukung dan hasil cek "sudah ada?" masing-masing, posisi kartu jangkar di loop 1, dan **ide terbaik per subtema** (supaya terlihat kalau satu subtema mendominasi).
12. **Jalur cadangan**: kalau di tahap 2 dua dari tiga pertanyaan bukti utama juara tidak terjawab, kembali ke cadangan (lalu finalis berikutnya), bukan memaksakan juara dengan bukti tipis.

## Dari juara ke tesis
- **Tesis 2 kalimat** (sudah dibuat di paket; perbaiki kalau perlu):
  > Masalah: "[Konteks/lokus] masih menghadapi [masalah spesifik], yang berdampak pada [akibat konkret]."
  > Gagasan: "Esai ini berargumen bahwa [klaim utama], karena [alasan 1] dan [alasan 2]."
- **3–5 kandidat judul** dengan pola berbeda (deskriptif, deklaratif, frasa ekspresif + subjudul, opsional akronim). Jangan semua kandidat memakai akronim.

## Checkpoint
Dalam **mode jalan terus** (`CLAUDE.md` § Mode jalan terus), inilah satu-satunya titik berhenti sejak tahap 0. Laporan di sini juga memuat isi checkpoint tahap 0, ringkasan 1A dan 1B, tafsiran yang diambil Claude sendiri, dan daftar periksa langkah tahap 0–1C dengan bukti file.

Tunjukkan ke penulis:
- Top 9 dengan subtema dan ringkasan satu kalimat, dengan kartu liar ditandai;
- hasil cek "sudah ada?";
- juara dan cadangan beserta alasannya, **atau** Pilihan A/B kalau hasilnya seri;
- posisi kartu jangkar (kalau ada) sebagai ukuran seberapa bisa dipercaya juri AI;
- tesis dan kandidat judul.

Penulis memilih. Catat di `<L>/STATUS.md`.

---

## Catatan teknis
- **Subagent** tersedia di Claude Code/Cowork (alat Agent). Kalau tidak tersedia (misalnya chat biasa), jalankan setiap prompt juri di **chat baru** dan tempel hasilnya kembali. Prinsipnya sama: juri tidak boleh melihat proses brainstorming.
- **Tiga utas** (hemat kuota, CLAUDE.md § Satu utas pendek per tahap). Setiap utas dimulai dari `STATUS.md` § Serah terima, dan diakhiri dengan memperbarui serah terima serta § Log kuota.

  | Utas | Langkah | Hasil di file | Yang dibaca di awal utas |
  |---|---|---|---|
  | **1A** | Langkah 0, 0b, 0c | `ide/bekal.md`, `pasaran.md`, `peta-subtema.md`, `tambang-literatur.md`, `peluang.md` | `STATUS.md`, `aturan.md`, `catatan/bank-juara.md` |
  | **1B** | Loop 1–3, Kolam | `ide/loop-N.md`, `ide/juri/*.json`, `ide/juri/kesan-loop-N.json`, `ide/kolam.md` | `STATUS.md`, `aturan.md` (ringkasan aturan, rubrik, profil juri), `ide/peluang.md`, `pasaran.md`, `peta-subtema.md`; `bekal.md` dan `tambang-literatur.md` hanya untuk dikirim ke generator |
  | **1C** | Final langkah 1–12, tesis, judul, checkpoint | `ide/final.md`, `ide/paket-final.md`, `ide/adu-final.json`, tesis + judul di `STATUS.md` | `STATUS.md`, `aturan.md`, `ide/kolam.md`, kartu finalis di `ide/loop-N.md` (Grep atau rentang baris, bukan berkas utuh), `pasaran.md` |

  Keluaran juri yang panjang tinggal di utas 1B dan tidak dibawa ke 1C. Yang dibawa hanya tabel `arena.py rekap` dan daftar finalis di `ide/kolam.md`.
- **Perkiraan biaya:**
  - Panggilan subagent: 3 generator + 9 juri loop + 3 kesan 30 detik + 1 prediksi pasaran + 1 jawaban chatbot + 1 kritik finalis + 3 juri final + 12 adu ≈ **33 panggilan**.
  - Pekerjaan agen utama: ±18–27 pencarian bukti dan ±27–36 pencarian cek "sudah ada?" untuk 9 finalis (minimal 3 per finalis, ditambah unsur inti yang belum tercakup), ditambah rumusan peluang, dedup, hibrida, dan paket.
  - Model per panggilan mengikuti tabel di § Juri buta: hanya generator dan satu juri panel final yang memakai Opus. Hasil juri ditulis ke JSON dan dihitung skrip, jadi transkrip juri tidak perlu dibaca ulang utuh oleh agen utama.
  - Kalau tenggat sangat sempit, lihat Mode Kilat di `workflow/MODE-KILAT.md` (bukan default).
- Juri AI hanya **proksi** juri manusia. Belum ada studi peer-review tentang faktor penentu juara lomba esai, jadi bobot rubrik ide tetap hipotesis. Kartu jangkar dan catatan hasil lomba sungguhan adalah satu-satunya cara mengujinya. Rekomendasi akhir tetap disajikan ke penulis, bukan diputuskan sepihak.
- **Desain juri mengikuti `skills/esai/advanced-evaluation/`**: alasan sebelum skor, tukar posisi di setiap adu (tidak sepakat = seri), netral terhadap panjang dan nada yakin, keyakinan dicatat. Bias swa-penilaian (generator dan juri dari keluarga model yang sama) tidak bisa dihapus sepenuhnya. Peredamnya adalah agen tanpa CLAUDE.md, kartu yang dibersihkan dari pembelaan diri, label buta yang diacak skrip, model yang diputar antarpersona, kartu jangkar dari juara sungguhan, dan checkpoint penulis di akhir. Opsional: penulis menempel paket Top 4 ke ChatGPT/Gemini sebagai juri dari keluarga model lain.
