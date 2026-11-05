# Evaluasi Workflow dan Arena Ide (5 November 2026)

Bahan penilaian ada tiga. Pertama, workflow (`CLAUDE.md`, `workflow/`, `templates/rubrik-ide.md`, prompt generator dan juri). Kedua, data nyata dari 4 lomba yang sudah memakai workflow ini: Navigation, Pharfest, Civil, dan Toyota, termasuk 261 penilaian juri di `ide/juri/*.json`. Ketiga, riset web dari 3 subagent (laporan lengkap di `catatan/riset-arena-ide/`).

Skill `deep-research` tidak tersedia di sesi ini. Penggantinya adalah 3 subagent riset Sonnet yang bekerja paralel. Kebanyakan sumber hanya mereka lihat dari abstrak atau cuplikan hasil pencarian, jadi sebelum dikutip di esai, sumber perlu dibuka sendiri. Sitasi yang tidak bisa diverifikasi subagent tidak dipakai di sini.

---

## 1. Kesimpulan singkat

- **Workflow secara umum kuat di sisi integritas**: tidak ada sumber karangan, ada peta klaim, auditor sitasi, matriks kepatuhan, dan checkpoint. Kelemahan terbesarnya tidak ada di dalam tahap mana pun. Kelemahannya, workflow **tidak pernah diuji terhadap hasil lomba sungguhan**, dan **praktiknya hampir selalu menyimpang dari desain** karena kuota dan tenggat.
- **Fondasi Arena Ide sudah sejalan dengan riset.** Ide dibuat banyak lalu diseleksi, juri dipanggil terpisah dan buta, urutan diacak, adu dibalik dua arah dengan aturan seri, ada bukti ≥2, dan manusia yang memutuskan. Ini sudah di atas rata-rata pipeline yang dipublikasikan.
- Tetapi ada **enam celah** yang ditunjukkan oleh data lomba sendiri maupun oleh literatur:
  1. tidak ada deduplikasi ide;
  2. seleksi dilakukan per loop, bukan dari satu kolam gabungan;
  3. median membuang suara juri yang paling "terpikat";
  4. tidak ada cek "apakah ide ini sudah pernah ada";
  5. tidak ada langkah menggabungkan atau mengembangkan ide (evolusi);
  6. peringkat di puncak sebenarnya seri statistik, tetapi dilaporkan sebagai satu juara.

---

## 2. Kekurangan workflow secara keseluruhan

| # | Kekurangan | Bukti | Usulan |
|---|---|---|---|
| W1 | **Tidak ada umpan balik dari hasil lomba.** Tidak ada satu pun `STATUS.md` yang mencatat hasil (juara, finalis, atau gugur) maupun komentar juri. Jadi bobot rubrik ide (Kejutan + Reframing = 45%) masih hipotesis dan belum pernah dicek. | `STATUS.md` keempat lomba | Tambah **Tahap 8 Pasca-lomba**: catat hasil, judul para juara, dan komentar juri bila ada. Bandingkan dengan peringkat Arena. Masukkan judul juara ke bank "ide pasaran" bidang itu. Setelah 5–10 lomba, baru ada dasar untuk mengubah bobot. |
| W2 | **Desain dan praktik tidak cocok.** Jalur penuh (±35 subagent) hanya dijalankan 1 kali dari 4 lomba. Pharfest memakai "Versi Sedang" yang diimprovisasi agen, Toyota dan Civil hanya 1 loop, dan Mode Kilat cuma memakai 1 juri. Setiap lomba akhirnya punya versi Arena yang berbeda. | `STATUS.md` § Catatan keputusan | Resmikan **3 ukuran Arena (S/M/L)** lengkap dengan jumlah panggilan dan perkiraan kuota, lalu jadikan **M sebagai default**. Versi improvisasi tidak lagi diperlukan. |
| W3 | **Kebutaan juri tidak terjamin.** Agen `juri-ide` tidak termuat di sesi cloud (Navigation, Toyota), sehingga juri diganti subagent umum yang hanya "diminta" membaca satu file. | Catatan keputusan Navigation dan Toyota | Siapkan satu file prompt juri yang sudah utuh untuk fallback, lalu catat di `loop-N.md` apakah juri benar-benar buta. |
| W4 | **Risiko diskualifikasi karena surat orisinalitas berulang.** 3 dari 4 lomba (Pharfest, Navigation, Civil) mewajibkan pernyataan orisinalitas atau karya asli peserta, sementara workflow ini 100% AI. Toyota tidak menyebut keduanya. Tahap 0 memang memperingatkan, tetapi setelah itu workflow tetap berjalan normal. (Dikoreksi 5 Nov; versi awal laporan ini menulis "keempat lomba".) | `aturan.md` Pharfest, Navigation, Civil | Jadikan ini **keputusan wajib di tahap 0**, dengan pilihan yang jelas: (a) penulis menulis ulang memakai bahan dari Claude, (b) tanya panitia, (c) lanjut dengan risiko yang dicatat. Ini risiko terbesar di seluruh workflow, lebih besar daripada kualitas ide. |
| W5 | **Rubrik ide terputus dari rubrik resmi.** Rubrik ide sengaja tidak mengikuti guidebook. Padahal di lomba esai Indonesia, orisinalitas biasanya hanya berbobot 10–30%, dan argumen, dampak, serta penulisan sering lebih besar (riset 2). Akibatnya, ide yang menang di Arena bisa kurang cocok dengan lembar nilai resmi. | `templates/rubrik-ide.md` § Penyesuaian | Pertahankan bobot "wow", tetapi tambahkan satu cek di panel final: *"seberapa besar ide ini membantu skor di kriteria resmi X, Y, Z?"* Cek ini tidak dimasukkan ke skor, cukup jadi informasi untuk penulis. |

Tahap 2–6 tidak saya temukan bercelah besar. Pengamannya (peta klaim, `cek_klaim.py`, auditor sitasi, syarat berhenti berdasarkan temuan) justru bagian terkuat workflow ini.

---

## 3. Arena Ide: apa kata data dari 4 lomba

Angka berikut dihitung dari `ide/juri/*.json` dengan skrip (korelasi peringkat Spearman antarjuri).

| Temuan | Angka | Artinya |
|---|---|---|
| **Gerbang hampir tidak pernah menggugurkan** | 6 dari 261 penilaian (2,3%) | G2 "benar secara ilmiah" dinilai juri tanpa membuka sumber. Gerbang ini memberi rasa aman yang semu. |
| **Juri "lelah" sering tidak sepakat dengan dua juri lain** | ρ = 0,08 dan 0,14 (Navigation loop 1); 0,22 vs praktisi (Toyota). Di Navigation final selisihnya kecil (0,49 dan 0,68), sedangkan akademisi–praktisi 0,70–0,90. (Dikoreksi 5 Nov dengan `tools/evaluasi.py`, yang merata-rata nilai kembar. Hitungan kasar sebelumnya 0,06/0,12/0,32/0,21.) | Persona "lelah" selalu memakai Haiku, jadi persona dan model tercampur. Tidak bisa diketahui apakah ia berbeda karena persona atau karena model yang lebih lemah. Median lalu membuang suaranya, padahal workflow sendiri menyebut reaksi "berhenti dan tertarik" sebagai sinyal terpenting. |
| **Panel final dan adu berpasangan tidak sepakat** di kedua lomba yang menjalankan keduanya | Navigation: peringkat 1 panel = I25, juara adu = I13 (peringkat 4 panel). Pharfest: peringkat 1 panel = I01, juara adu = I20. | Top 4 Navigation hanya terpaut 7,10–7,70. Di puncak, peringkat sebagian besar acak. Menyebut satu "juara" memberi keyakinan palsu. |
| **Skor menumpuk** | Total umumnya 4–8. Top 4 hanya terpaut ~0,6. | Skala 1–10 berbobot tidak cukup membedakan ide-ide teratas, dan ini cocok dengan temuan riset bahwa skor Likert dari LLM kurang andal. |
| **Seleksi per loop** | Top 3 diambil dari setiap loop | Loop yang kuat dan loop yang lemah sama-sama mendapat 3 kursi. Ide ke-4 dari loop kuat bisa lebih baik daripada ide ke-1 dari loop lemah. |
| **Penggabungan ide terjadi tanpa sengaja** | `final.md` Navigation: "I25 bisa digabung sebagai satu bagian di esai juara" | Rekombinasi terbukti berguna, tetapi workflow melarangnya ("tidak boleh mengganti inti ide"). |

---

## 4. Temuan riset dan artinya untuk Arena Ide

### A. Sains tentang menghasilkan dan memilih ide

| Temuan | Sumber | Implikasi |
|---|---|---|
| Kualitas sebuah proses ide ditentukan oleh **ide terbaiknya**, bukan rata-ratanya. Ide yang dibuat sendiri-sendiri lalu digabung lebih baik daripada brainstorming bersama. | Girotra, Terwiesch & Ulrich 2010, https://repository.upenn.edu/oid_papers/191 | Loop yang terpisah sudah benar. Tetapi penggabungan seharusnya terjadi sebelum seleksi (satu kolam), bukan setelah Top 3 per loop. |
| Membuat ide dengan LLM itu murah, sedangkan **seleksi adalah titik sempitnya**. | Girotra, Meincke, Terwiesch & Ulrich 2023 ("Ideas are dimes a dozen") | Tenaga lebih baik dipindah dari menghasilkan 36 ide ke seleksi yang lebih tajam. |
| Ide dari satu model dan satu prompt cenderung **seragam**. Chain-of-thought dan persona menaikkan keragaman sampai mendekati kelompok manusia. | Meincke, Mollick & Terwiesch 2024, https://arxiv.org/abs/2402.01727 | Generator perlu CoT (buat banyak dulu, lalu pilih yang paling berbeda) dan pengukuran duplikasi. |
| Saat jumlah ide diperbesar, **hanya sekitar 5% yang unik**. Ide LLM dinilai pakar lebih baru tetapi sedikit kurang layak. Juri LLM tidak andal. | Si, Yang & Hashimoto 2024, https://arxiv.org/abs/2409.04109 | Wajib dedup sebelum juri. Jangan percaya penuh pada skor kebaruan dari LLM. |
| Ide LLM **turun nilainya lebih tajam setelah dieksekusi** dibanding ide manusia. | Si dkk. 2025 ("ideation–execution gap"), https://arxiv.org/abs/2506.20803 | Uji "bisa jadi esai yang kuat" sebelum memilih juara, bukan hanya menilai kartu ide. |
| AI membuat karya individu lebih kreatif tetapi **karya kolektif lebih seragam**. | Doshi & Hauser 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11244532 | Peserta lain juga memakai AI. Daftar pasaran perlu memuat "ide yang akan ditulis ChatGPT/Gemini untuk tema ini". |
| Penyeleksi manusia **memilih ide yang aman** daripada yang orisinal. Ada bias terhadap kreativitas saat situasi tidak pasti. | Rietzschel, Nijstad & Stroebe 2010; Mueller dkk. 2012 | Median dan rapat juri cenderung konservatif. Perlu jalur "kartu liar" untuk ide yang memecah pendapat. |
| Kreator lebih jago menilai ide **orang lain** daripada manajer, tetapi buruk menilai ide sendiri. | Berg 2016 (ASQ) | Persona juri "penulis yang menilai karya sesama" layak dicoba. Generator jangan pernah ikut menilai idenya sendiri. |
| Juri LLM punya bias posisi, bias panjang, dan **bias memilih tulisan sendiri**. | Zheng dkk. 2023, https://arxiv.org/abs/2306.05685; Panickssery dkk. 2024, https://arxiv.org/abs/2404.13076 | "Model berbeda" di Arena masih satu keluarga (Sonnet/Haiku/Opus = Claude), jadi bias swa-preferensi belum teredam. |
| Efek urutan tampil terjadi di juri sungguhan (skor naik untuk yang tampil belakangan). | Bruine de Bruin 2005 | Pengacakan per juri sudah benar. |

### B. Pipeline AI penghasil ide yang dipublikasikan

| Elemen | Ada di | Di Arena Ide |
|---|---|---|
| Deduplikasi/klaster ide | Google AI co-scientist (agen Proximity), Si 2024 | **Tidak ada** |
| Benih dari literatur | SciMON, Chain of Ideas, Scideator | Ada (Langkah 0b, loop 2–3) ✅ |
| Cek kebaruan = mencari **tumpang tindih** dengan karya yang sudah ada | Scideator (Novelty Checker), SciMON, RAG-Novelty | **Tidak ada.** Yang ada hanya ≥2 bukti *pendukung*, dan daftar pasaran berupa prediksi LLM kalau juara asli tidak ditemukan (Navigation), sehingga penilaiannya melingkar. |
| Peringkat dengan adu/Elo sebagai mesin utama | Co-scientist (turnamen Elo + debat), Chain of Ideas (round-robin dua urutan) | Hanya untuk Top 4. 36 ide dinilai per ide (pointwise). |
| Evolusi: menggabung atau memutasi ide teratas | Co-scientist (agen Evolution) | **Dilarang** ("tidak boleh mengganti inti ide") |
| Manusia sebagai pemutus akhir | Hampir semua | Ada ✅ |

Sumber: https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/, https://arxiv.org/abs/2410.13185 (Chain of Ideas), https://arxiv.org/abs/2409.14634 (Scideator), https://arxiv.org/abs/2409.16605 (RAG-Novelty).

### C. Praktik di ideathon, hackathon, dan lomba ide

| Temuan | Sumber | Implikasi |
|---|---|---|
| **Rumuskan masalah dulu, baru cari solusi** (Define sebelum Ideate). Double Diamond dan d.school memisahkan keduanya. | https://web.stanford.edu/class/me113/d_thinking.html | Arena langsung bergerak dari subtema ke solusi. Reframing hanya muncul sebagai salah satu lensa. |
| **Opportunity Solution Tree**: satu tujuan, beberapa peluang, baru kemudian solusi. | https://askable.com/blog/opportunity-solution-trees | Ide yang dikelompokkan per peluang menjaga keragaman secara terstruktur. |
| Kriteria yang berulang di banyak lomba: dampak/urgensi, kebaruan, kelayakan, kesesuaian tema, bukti, komunikasi. Di Indonesia, orisinalitas sering berbobot 10–30%. | ISEF https://www.societyforscience.org/isef/grand-award/criteria/; contoh panduan esai kampus | Bobot kejutan 25% + reframing 20% di Arena lebih tinggi daripada di lomba nyata. Ini sah sebagai strategi, tetapi perlu diuji lewat W1. |
| Kesalahan umum: **cakupan terlalu luas** dan esai **deskriptif, bukan analitis**. | Juri hackathon (DEV.to); panduan John Locke (Polygence, sekunder) | Perlu uji: "Ada satu klaim inti yang bisa dibuktikan dalam batas kata?" dan "Ada tesis yang bisa dibantah?" |
| Kesan pertama dan penyajian sangat menentukan. | Tsay 2021 (lomba pitch), UCL | Untuk esai, judul dan paragraf pembuka sebaiknya ikut diuji di final, bukan hanya kartu ide. |
| **Tidak ada studi peer-review** tentang faktor penentu juara esai/LKTI. | Riset 2 | Rubrik Arena mana pun tetap hipotesis. Hanya data pasca-lomba (W1) yang bisa mengujinya. |
| Klaim "aplikasi/sosialisasi itu klise" tidak bersumber. Ide berbasis platform pernah juara 3 nasional. | https://unair.ac.id/mahasiswa-fib-raih-juara-3-lomba-esai-tingkat-nasional/ | Larangan di generator sebaiknya dibaca sebagai "tanpa mekanisme yang jelas", bukan larangan mutlak (dan memang sudah ditulis begitu). |

---

## 5. Usulan perbaikan Arena Ide (urut prioritas)

### P1: murah, dampaknya besar
1. **Satu kolam + dedup.** Ide dari semua loop digabung, ide kembar atau sangat mirip dihapus (agen utama atau skrip kemiripan sederhana di `arena.py`), lalu 9 finalis dipilih dari kolam gabungan. Keseimbangan subtema dijaga dengan batas maksimum per subtema, bukan dengan kursi per loop.
2. **Jalur kartu liar.** Maksimal 2 kursi finalis untuk ide yang (a) mendapat skor tertinggi dari satu juri, atau (b) mendapat reaksi "berhenti" di kesan 30 detik, walaupun mediannya rendah. Tukar model antarpersona di setiap loop (misalnya juri "lelah" sesekali memakai Sonnet) supaya ketahuan apakah perbedaan datang dari persona atau dari model.
3. **Cek "sudah ada?" untuk 9 finalis**, terpisah dari bukti pendukung. Cari judul atau inti ide di web, Google Scholar, dan pengumuman juara lomba sejenis. Kalau tumpang tindihnya tinggi, beri sudut baru atau turunkan K1. Ini mengganti penilaian kebaruan yang melingkar.
4. **Laporkan ketidakpastian.** Kalau panel dan adu tidak sepakat, atau selisih median < ±0,5, sebut hasilnya "seri". Sajikan 2–3 ide teratas ke penulis dengan pro dan kontra masing-masing, bukan satu juara.
5. **Jangkar kalibrasi.** Kalau judul juara edisi lalu ditemukan, selipkan 1–2 judul itu diam-diam (ditulis sebagai kartu yang sama) ke tumpukan juri. Kalau juri menaruh juara asli di bawah, rubrik atau juri sedang miskalibrasi. Biayanya nol panggilan tambahan.

### P2: sedang
6. **Langkah 0c, Rumusan masalah.** Dari bekal, buat 4–6 rumusan peluang ("Bagaimana kita bisa …", lengkap dengan bukti bahwa masalahnya nyata). Generator lalu membuat ide per peluang. Ini menggantikan lensa reframing yang sekarang hanya kebetulan muncul.
7. **Uji "bisa jadi esai" di Top 4.** Untuk setiap ide: tesis 2 kalimat, 3 poin argumen beserta bukti yang tersedia, dan paragraf pembuka ±100 kata. Adu berpasangan dilakukan pada paket ini, bukan pada kartu. Ini menjawab celah ideasi–eksekusi sekaligus menguji kesan pertama.
8. **Satu putaran evolusi.** Setelah panel final, agen utama membuat 1–2 ide hibrida dari finalis teratas (gabungan atau mutasi pada kelemahan terbesar), lalu hibrida itu ikut adu. Contoh nyatanya I13 + I25 di Navigation.
9. **Generator: buat banyak, lalu pilih yang paling berbeda.** Generator menulis 25–30 ide satu baris dengan CoT, lalu memilih 12 yang paling jauh satu sama lain dan dari daftar pasaran. Tambahkan juga ke daftar pasaran prediksi "ide yang akan dihasilkan chatbot umum untuk tema ini".

### P3: opsional atau jangka panjang
10. **Tahap 8 Pasca-lomba** (W1). Ini satu-satunya cara tahu apakah rubrik ide benar.
11. **Juri lintas vendor secara manual** untuk 4 finalis teratas: penulis menempel kartu ke ChatGPT atau Gemini. Ini satu-satunya cara meredam bias swa-preferensi dalam keluarga Claude.
12. **Ukuran Arena resmi S/M/L** (W2). Usulan M: 2 loop × 12 ide → dedup → 2 juri per loop dari model berbeda → kolam gabungan → 6 finalis + kartu liar → cek "sudah ada?" → 1 putaran evolusi → adu dua arah Top 4 dengan paket "bisa jadi esai". Kira-kira 20 panggilan subagent.

### Yang sebaiknya tidak diubah
Juri buta tanpa CLAUDE.md, label yang diacak skrip, adu dua arah dengan aturan seri, alasan sebelum skor, syarat ≥2 bukti untuk finalis, tambang literatur, daftar pasaran, dan checkpoint penulis. Semua ini didukung riset.

---

## 6. Status penerapan (5 Nov 2026)

P1 dan P2 sudah diterapkan atas permintaan penulis. P3 belum.

| Usulan | Di mana |
|---|---|
| Kolam gabungan + dedup | `workflow/01-ide-dan-tesis.md` § Kolam; `arena.py mirip` |
| Kartu liar | § Kolam langkah 3; `arena.py rekap --top --kesan` |
| Model diputar antarpersona | § Juri buta |
| Cek "sudah ada?" | § Final langkah 4 |
| Laporan seri (Pilihan A/B) | § Final langkah 10; `rekap` mencetak `SERI DI PUNCAK`, `adu` mencetak `SERI/TIPIS` |
| Kartu jangkar juara lama | § Kartu jangkar; `templates/prompt-ide-pasaran.md`; `rekap --kecuali` |
| Rumusan peluang | Langkah 0c; `templates/prompt-ide-generator.md` |
| Paket "bisa jadi esai" untuk adu | § Final langkah 8; `templates/prompt-ide-adu.md` |
| Evolusi (≤2 hibrida) | § Final langkah 6–7 |
| Generator: buat banyak lalu pilih 12 yang paling berbeda; pasaran versi chatbot | `templates/prompt-ide-generator.md`, `templates/prompt-ide-pasaran.md` § 3 |

Juga disesuaikan: `MODE-KILAT.md`, `CLAUDE.md` (Peta Skill, Tahapan, Alat), `tools/README.md`, `.claude/agents/juri-ide.md` (deskripsi + instruksi "berani memberi nilai tinggi untuk ide orisinal"), dan `lomba/_template/ide/README.md`. Kritik per loop (3 panggilan) diganti satu kritik untuk semua finalis, jadi total panggilan subagent tetap sekitar 33.

**Uji pada data lama.**
- `arena.py mirip` dengan ambang 0,18 tidak menemukan duplikat di 36 ide Navigation (kemiripan tertinggi 0,21 hanya pada ambang yang lebih rendah). Di Pharfest, skrip menandai pasangan yang memang satu keluarga ide: "Apotek yang Bangga Menolak" dan "Tunda, Bukan Tolak", serta karagenan dan porang sebagai bahan obat lokal. Jadi dedup lebih berguna sebagai pengaman murah daripada sumber perbaikan besar.
- Rekap kolam Navigation (`--top 7`) menandai I25, I13, dan I02 sebagai seri di puncak, serta I11 dan I30 sebagai kartu liar. Kedua kartu liar itu tidak masuk finalis lama.
- `python tools/tes_alat.py`: 47 tes lolos (4 tes baru untuk kartu liar, seri, dan dedup).
