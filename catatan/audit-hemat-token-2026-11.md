# Audit hemat token dan kuota (5 November 2026)

Tujuan: menjalankan workflow esai lomba di Claude Code desktop (paket Team) tanpa menghabiskan limit 5 jam dan limit mingguan, **tanpa melonggarkan pengaman** (sumber dan angka, peta klaim, checkpoint, rubrik resmi, peringatan aturan AI).

Status: **U1, U2, dan U11 diterapkan** setelah disetujui penulis pada 5 Nov 2026 (versi workflow `2026-11-05f`, cadangan di `arsip/versi-2026-11-05f/`). **U4, U5, dan U10 diterapkan** di hari yang sama, bersama aturan **peringatan boros** yang diminta penulis (versi `2026-11-05h`, cadangan di `arsip/versi-2026-11-05h/`). Keduanya dicatat di `catatan/riwayat-workflow.md`. Satu bagian U10 sengaja tidak diterapkan: banding berpasangan tetap menilai semua kriteria, karena revisi bisa merusak kriteria yang tidak disentuh. Usulan lain di § 8 masih **usulan** dan harus disetujui penulis lewat tahap 8c (`workflow/08-evaluasi.md`). Ukuran berkas di § 3.2 diukur sebelum perubahan `2026-11-05d` sampai `2026-11-05f`, sehingga CLAUDE.md, `01-ide-dan-tesis.md`, dan `05-review.md` sekarang sedikit berbeda. Pelajaran yang diturunkan dari audit ini dicatat di `catatan/buku-pelajaran.md` sebagai PL24–PL31.

---

## 1. Ringkasan

1. **Pemborosan terbesar adalah utas panjang, bukan jumlah juri.** Claude Code mengirim ulang seluruh isi utas di setiap permintaan, termasuk setiap pemanggilan alat. Pada 29 Okt, ±170 juta dari 180 juta token proyek adalah *cache read*, dan utas Arena Ide sendiri mencapai 74 juta token. Model sekarang punya jendela konteks 1 juta token dengan auto-compact di ±967 ribu, jadi utas bisa terus membesar tanpa pernah dipadatkan.
2. **Bahan yang ditempel ulang ke subagent relatif kecil.** Seluruh rubrik, pasaran, kartu, dan bekal yang dikirim ke ±33 subagent Arena jumlahnya kira-kira 110–150 ribu token. Itu kurang dari 1% dari 74 juta. Menghemat di sini tidak salah, tapi dampaknya kecil.
3. **Ada satu celah konfigurasi yang mahal.** Tiga agen proyek (`juri-ide`, `juri-esai`, `auditor-sitasi`) tidak punya baris `model:`, jadi semuanya **mewarisi model utas utama**. Panduan tahap 1 hanya mewajibkan "paling tidak satu dari tiga juri" memakai model lain. Kalau utas utama berjalan di Opus, dua dari tiga juri loop, semua adu, dan semua juri tahap 5 ikut berjalan di Opus. Menurut Anthropic, Opus "costs several times more per turn than Sonnet".
4. **Setiap permintaan sudah membawa ±86 ribu token beban tetap** sebelum pesan pertama, misalnya alat sistem, alat MCP, daftar skill, dan CLAUDE.md. Dua server MCP yang tidak ada hubungannya dengan esai (Roblox_Studio, godot-ai) tersambung di tingkat pengguna, jadi ikut termuat di setiap proyek.
5. **Kuota tidak dicatat per tahap**, sehingga evaluasi (8a) tidak bisa menunjuk tahap termahal. Toyota dan Civil menulis "tidak tercatat".

Tiga tuas dengan dampak terbesar (rinciannya di § 8):
- **U1:** satu utas pendek per tahap, dengan serah terima lewat `STATUS.md`. Arena dipecah menjadi 3 utas.
- **U2:** `model: sonnet` di ketiga agen proyek, ditambah tabel model per peran.
- **U4/U5:** hasil besar (pencarian, riset, keluaran juri) ditulis ke file, dan utas utama hanya menerima ringkasan.

---

## 2. Apa yang menghabiskan limit: temuan dari dokumen resmi

Diambil 5 Nov 2026. Kutipan bertanda petik adalah kutipan persis; selebihnya parafrase. "COSTS" = https://code.claude.com/docs/en/costs.md, "CACHE" = https://code.claude.com/docs/en/prompt-caching.md.

| Faktor | Yang dikatakan dokumen resmi | Sumber |
|---|---|---|
| Limit paket Team | Pemakaian Claude Code mengambil jatah per kursi yang direset tiap 5 jam (bergulir) dan mingguan. Jatah ini dibagi dengan Claude chat dan Cowork, dan besarnya tergantung tingkat kursi (Standard/Premium). Angka pastinya **tidak dipublikasikan**. | COSTS § Claude for Teams and Enterprise; https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan |
| Limit dibagi antarmodel | Limit sesi dan mingguan berlaku untuk semua model, jadi berganti model dengan `/model` tidak memulihkan akses. Pengecualian: setelah pesan khusus "Opus limit"/"Sonnet limit", pindah ke keluarga model lain tetap bisa dipakai. | COSTS § When a developer asks about a limit |
| Biaya per model | "Opus costs several times more per turn than Sonnet, and Sonnet more than Haiku." Opus "uses meaningfully more of your quota". Pengali pastinya **tidak disebut**. | https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code |
| Utas dibaca ulang | Setiap permintaan, Claude Code "re-sends the full context: the system prompt, your project context, every prior message and tool result". Akibatnya "a one-line question in a session that has been open all day still draws usage for the whole conversation." | CACHE § How the cache is organized; COSTS § Why usage climbs |
| Bobot cache read terhadap limit paket | Hanya disebut ditagih pada "cached token rate … below the standard input rate". Bobotnya terhadap limit paket **tidak disebut**. | CACHE § Check cache performance |
| Umur cache (TTL) | Paket langganan dalam jatah: **utas utama 1 jam**. Subagent, workflow, dan pemadatan (compaction) **5 menit**. Jeda yang lebih lama dari TTL membuat seluruh konteks diproses ulang tanpa cache. | CACHE § Which TTL each request gets; COSTS § Why usage climbs |
| Yang merusak cache | Ganti model ("each model has its own cache"), fast mode, menyambung atau melepas server MCP saat alat tidak ditunda, menolak satu alat utuh, pemadatan, dan menumpuk banyak gambar. Mengganti effort di Opus 5.5, Sonnet 5.5, Haiku 5.5, dan Fable 5.1 **tidak** merusak cache. | CACHE § Actions that invalidate the cache |
| Auto-compact | Model dengan jendela 1 juta memadatkan "at about 967K tokens by default". Ambang bisa diubah dengan `/autocompact`, `autoCompactWindow`, atau `CLAUDE_CODE_AUTO_COMPACT_WINDOW` (100 ribu–1 juta). | https://code.claude.com/docs/en/model-config.md |
| `/clear` dan `/compact` | "/clear costs nothing". `/compact` membaca seluruh utas yang dipadatkan, jadi ia sendiri permintaan besar, dan paling mahal pada utas lama yang cache-nya sudah kedaluwarsa. `/compact` bisa diberi instruksi, dan CLAUDE.md boleh punya bagian `# Compact instructions`. | COSTS § Manage context proactively, § Why usage climbs; CACHE § Compacting |
| Subagent | Punya jendela konteks sendiri, dan hanya ringkasannya yang kembali. Permintaannya "count toward the same usage limits as your main conversation". Subagent tidak membaca cache induk. Kalau `model` tidak diisi, subagent memakai model utas utama. Field `tools` bersifat daftar izin; kalau dikosongkan, subagent mewarisi semua alat. `omitClaudeMd: true` membuang CLAUDE.md dari konteks awal. | https://code.claude.com/docs/en/sub-agents.md; CACHE § Subagents and the cache |
| Saran memakai subagent | "Delegate verbose operations to subagents … only a summary returns". Untuk tugas sederhana pakai `model: haiku`. | COSTS § Delegate verbose operations, § Choose the right model |
| Thinking dan effort | "Thinking tokens are billed as output tokens, and the default budget can be tens of thousands of tokens per request." Thinking tidak bisa dimatikan di Opus/Sonnet/Haiku 5.5. Effort bawaan Opus 5.5, Sonnet 5.5, dan Haiku 5.5 adalah `medium`; `max` "is prone to overthinking". | COSTS § Adjust extended thinking; model-config.md |
| MCP | "MCP tool definitions are deferred by default, so only tool names and server instructions enter context". Saran: "Disable unused servers: Run /mcp". | COSTS § Reduce MCP server overhead; https://code.claude.com/docs/en/mcp.md |
| Skill | Deskripsi skill selalu dimuat; isi skill baru dimuat saat dipanggil, lalu tetap ada di konteks pada setiap giliran sesudahnya. `disable-model-invocation: true` mengeluarkan deskripsinya dari konteks. | https://code.claude.com/docs/en/skills.md |
| CLAUDE.md dan memori | Dimuat di setiap sesi. "Aim to keep CLAUDE.md under 200 lines". `@import` tidak mengurangi biaya konteks. Suntingan di tengah sesi baru berlaku setelah `/clear`, `/compact`, atau mulai ulang. | COSTS § Move instructions from CLAUDE.md to skills; https://code.claude.com/docs/en/memory.md; CACHE |
| Membaca file dan PDF | Satu Read maksimal 25.000 token secara bawaan. PDF lebih dari 10 halaman dibaca per rentang (`pages`, maksimal 20). Jumlah token per halaman PDF **tidak disebut**. Gambar dan PDF lama dibuang per batch saat batas permintaan tercapai, dan itu memicu pemrosesan ulang. | https://code.claude.com/docs/en/tools-reference.md; CACHE § Accumulating many images |
| WebFetch dan WebSearch | WebFetch menjalankan prompt atas halaman di panggilan model terpisah, dan Claude hanya menerima hasilnya (bukan halaman mentah). WebSearch hanya mengembalikan judul dan URL. | tools-reference.md |
| Pemakaian saat diam | Scheduled task, pesan dari sesi lain, dan goal check-in masing-masing memulai giliran baru yang mengirim seluruh konteks. Ringkasan sesi (recap) dan pemadatan saat diam juga memakai token. Pesan masuk dari sesi lain bisa ditahan dengan `crossSessionInbound: hold`. | COSTS § Background token usage, § Why usage climbs |
| Agent teams | Sekitar 7× token sesi biasa saat rekan tim berjalan di plan mode. Fitur ini tidak dipakai workflow ini. | COSTS § Manage agent team costs |
| Alat ukur | `/usage` (rincian per skill, subagent, dan server MCP, plus rekomendasi), `/context`, cincin pemakaian di aplikasi desktop, dan alat `get_usage`. | COSTS § Track your costs; https://code.claude.com/docs/en/desktop.md |

**Batas yang perlu diingat:** Anthropic tidak menerbitkan rumus resmi tentang berapa bagian limit paket yang dipakai oleh *cache read*. Data proyek ini (170 juta dari 180 juta adalah *cache read*) dan pernyataan COSTS bahwa utas panjang "still draws usage for the whole conversation" sama-sama menunjuk panjang utas sebagai tuas utama. Besaran pastinya tetap tidak diketahui.

---

## 3. Mengukur beban token workflow ini

Semua angka token di bagian ini adalah **perkiraan kasar ukuran byte ÷ 4**. Teks bahasa Indonesia bisa memakai lebih banyak token per karakter daripada teks bahasa Inggris, jadi angka sebenarnya mungkin sedikit lebih tinggi. Angka di § 3.1 adalah **hasil ukur** dari alat `get_usage`, bukan perkiraan.

### 3.1 Beban tetap per permintaan (diukur, sesi ini, 5 Nov 2026)

| Kategori | Token |
|---|---|
| Alat sistem (System tools) | 37.279 |
| Alat MCP (browser bawaan, alat aplikasi, konektor) | 20.362 |
| Prompt sistem | 11.100 |
| Daftar skill | 9.956 |
| Berkas memori (CLAUDE.md + memori otomatis) | 7.333 |
| **Jumlah sebelum pesan apa pun** | **±86.000** |

Jendela konteks 1.000.000 token, auto-compact di 97%. Angka ±86 ribu ini ikut terbaca di **setiap** permintaan. Utas dengan 300 permintaan membaca beban tetap ini ±26 juta kali-token, meskipun sebagian besar masuk lewat cache.

Daftar skill memuat banyak skill yang tidak terpakai untuk esai. Contohnya, 10 skill `hyperframes`/`media-use` di `~/.claude/skills/` saja punya deskripsi sepanjang ±6.000 karakter (±1.500 token), belum termasuk skill akun untuk skripsi, disertasi, dan sejenisnya.

### 3.2 Berkas workflow

| Berkas | Byte (baris "di dalamnya": karakter) | ± token | Kapan dimuat |
|---|---|---|---|
| `CLAUDE.md` | 21.973 | 5.500 | setiap permintaan, setiap utas |
| … di dalamnya: § Pemakaian skill + § Peta Skill | 9.397 | 2.350 | setiap permintaan |
| … di dalamnya: § Alat | 3.247 | 810 | setiap permintaan |
| `workflow/00-dekonstruksi-lomba.md` | 5.524 | 1.380 | tahap 0 |
| `workflow/01-ide-dan-tesis.md` | 27.586 | 6.900 | tahap 1, sering dibaca ulang per langkah |
| `workflow/02-riset.md` | 7.278 | 1.820 | tahap 2 |
| `workflow/03-kerangka.md` + `03b-rencana-visual.md` | 8.889 | 2.220 | tahap 3 |
| `workflow/04-menulis-draf.md` | 5.889 | 1.470 | tahap 4 |
| `workflow/05-review.md` | 5.758 | 1.440 | tahap 5 |
| `workflow/06-revisi-final.md` | 5.177 | 1.290 | tahap 6 |
| `workflow/07-sampul-poster.md` / `07c-presentasi.md` | 2.081 / 8.666 | 520 / 2.170 | bila diminta |
| `workflow/08-evaluasi.md` | 9.441 | 2.360 | tahap 8 |
| `workflow/MODE-KILAT.md` | 2.440 | 610 | tahap 0 bila tenggat ≤ 5 hari |
| `templates/prompt-ide-juri.md` | 5.863 | 1.470 | per juri Arena (±4.000 karakter yang dikirim) |
| `templates/prompt-ide-generator.md` / `-adu.md` / `-pasaran.md` | 3.867 / 3.769 / 3.272 | 970 / 940 / 820 | per panggilan |
| `templates/rubrik-ide.md` | 6.217 | 1.550 | per juri Arena |
| `templates/prompt-juri.md` / `rubrik-esai.md` / `prompt-auditor-sitasi.md` | 4.105 / 2.969 / 1.907 | 1.030 / 740 / 480 | per juri tahap 5 |
| `.claude/agents/*.md` (3 berkas) | 3.318 | 830 | prompt sistem setiap subagent juri |
| `catatan/buku-pelajaran.md` + `bank-juara.md` | 12.836 | 3.210 | tahap 0 |

Membaca seluruh berkas workflow sekali tidak mahal (±30 ribu token). Yang mahal adalah **berapa lama berkas itu tinggal di utas** setelah dibaca. Contohnya `01-ide-dan-tesis.md` (±6.900 token): kalau dibaca di awal utas Arena dan utas itu berjalan 250 permintaan, berkas ini saja terbaca ulang ±1,7 juta token.

### 3.3 Bahan yang ditempel ulang ke subagent

**Tahap 1, jalur penuh** (ukuran contoh dari Navigation dan Pharfest):

| Bahan | ± token sekali kirim | Dikirim ke | Kali | ± total |
|---|---|---|---|---|
| Teks prompt juri yang dikirim | 1.000 | juri loop (9), panel final (3), kritik (1) | 13 | 13.000 |
| Rubrik ide bagian 1–4 | 1.550 | sama | 13 | 20.000 |
| Daftar pasaran | 600 (Navigation, 2.446 B) – 1.300 (Pharfest, 5.168 B) | juri (13) + generator (3) | 16 | 10.000–21.000 |
| 12 kartu bersih | 2.000–2.500 (perkiraan: `loop-N.md` 16,5 KB juga memuat daftar satu baris dan rekap) | juri loop | 9 | 18.000–23.000 |
| Bekal | 12.000 (Navigation, 49 KB) – 17.800 (Pharfest, 71 KB) | generator | 3 | 36.000–53.000 |
| Paket 2 ide per adu | 1.000–1.500 (perkiraan, tidak ada berkas paket untuk diukur) | adu | 12 | 12.000–18.000 |
| **Jumlah bahan** | | | | **±110.000–150.000** |

**Tahap 5, per putaran** (naskah Pharfest 12,9–15,2 KB ≈ 3.200–3.800 token):

| Panggilan | Bahan | ± token |
|---|---|---|
| Juri rubrik | naskah + rubrik resmi + `rubrik-esai.md` + prompt | 6.000 |
| Devil's advocate | naskah + prompt | 5.000 |
| Konfirmasi | naskah + temuan | 5.000 |
| Banding berpasangan × 2 | 2 versi naskah + prompt, dua kali | 17.000 |
| Auditor sitasi | pasangan kalimat dan kutipan saja | 2.000–4.000 |
| **Per putaran** | | **±35.000–40.000** |

Pharfest menjalankan ±5 putaran, jadi totalnya ±175–200 ribu token bahan.

**Yang tidak bisa diukur dari sini:** beban tetap tiap subagent (prompt sistem dan alat miliknya sendiri). Agen juri mewarisi semua alat kecuali yang dilarang, termasuk nama alat MCP. Kalaupun beban tetap per subagent mendekati utas utama (±80 ribu tanpa CLAUDE.md), 33 panggilan Arena hanya menambah ±2,5 juta token. Itu tetap jauh di bawah 74 juta token utas Arena. Sebagai pembanding, subagent riset dokumen untuk audit ini (Sonnet, 29 pemanggilan alat, kebanyakan WebFetch) dilaporkan memakai ±138 ribu token.

### 3.4 Hasil yang kembali ke utas utama (bagian yang benar-benar mahal)

Setiap keluaran subagent dan setiap hasil alat masuk ke utas utama, lalu ikut terbaca di **setiap permintaan berikutnya**.

| Lomba | Bahan | Ukuran | ± token |
|---|---|---|---|
| Navigation | keluaran juri dan adu yang disimpan (`ide/juri/out-*.md`, 30 berkas) | 135.116 B | 34.000 |
| Navigation | catatan riset bekal (`ide/_riset/`, 4 berkas) + `bekal.md` | 100.975 B | 25.000 |
| Pharfest | `ide/bekal.md` + `tambang-literatur.md` | 98.871 B | 25.000 |
| Pharfest | teks sumber `riset/teks/` (14 berkas) | ±214 KB | ±54.000 |
| Pharfest | 6 versi draf (`draf-v1..v6.md`) | 85.162 B | 21.000 |
| Pharfest | `guidebook.txt` | 26.662 B | 6.700 |

Ilustrasi (asumsi, bukan ukuran): 34 ribu token keluaran juri yang masuk di tengah utas Arena, lalu diikuti 150 permintaan lagi, terbaca ulang ±5 juta token. Kalau keluaran itu langsung disimpan ke file dan utas berikutnya hanya membaca tabel `arena.py rekap` (±1 ribu token), angkanya turun ke ±150 ribu.

**Rumus kasar** yang dipakai di seluruh audit ini: *token yang dibaca dalam satu utas ≈ jumlah permintaan × rata-rata ukuran konteks.* Satu pemanggilan alat sama dengan satu permintaan. Misalnya, 74 juta token setara dengan ±250 permintaan pada konteks rata-rata ±300 ribu. Itu hanya ilustrasi, karena jumlah permintaan utas Arena tidak tercatat.

---

## 4. Data nyata dari empat lomba

| Lomba | Subagent per tahap | Model | Kejadian kuota | Sumber |
|---|---|---|---|---|
| Pharfest (29–30 Okt) | Bekal: **6 subagent riset Opus paralel**. Arena "Versi Sedang": 2 loop × 2 juri + 1 juri panel + 6 adu. Tahap 2–4 tanpa subagent. Tahap 5: ±5 putaran × 4–5 subagent. | Riset Opus; juri Sonnet/Haiku; tahap 5 Sonnet | **Limit 5 jam habis dalam ±15 menit**, limit mingguan 68% setelah riset. Arena dipangkas, tahap 6 tidak dicentang, versi darurat dibuat. | `ewc-siswa-pharfest-2026/STATUS.md`, `evaluasi.md` |
| Navigation (30 Okt) | Bekal: 4 peneliti + 1 penulis laporan (`deep-research`). Arena penuh: ±30 subagent. Tahap 2 tanpa subagent. | Sonnet/Haiku | Bentrok tenggat dengan Pharfest di kuota Pro yang sama, sehingga tahap 5–6 dipangkas dan cadangan kirim dibuat dari v3. Subagent kesan 30 detik membuat scheduled task tanpa diminta (PL07). | `essay-navigation-2026/STATUS.md`, `evaluasi.md` |
| Toyota (5 Nov) | Arena 1 loop atas permintaan penulis ("hemat kuota"): generator oleh agen utama, kesan 30 detik digabung ke juri, 3 juri subagent umum. | "model berbeda dari generator" | Kuota tidak tercatat | `toyota-eco-youth-14/STATUS.md` |
| Civil (31 Okt) | 1 loop, 3 juri, 6 adu | keluarga model non-Claude (pro/flash) | Kuota tidak tercatat (dikerjakan di alat lain) | `essay-civil-comp/evaluasi.md` |
| Sesi lintas lomba | Utas evaluasi workflow mencapai 439 ribu token konteks. Limit 5 jam naik dari 5% ke 47% dalam satu sesi kerja. Saat audit ini diukur, limit 5 jam 49% dan limit mingguan 21%. | — | — | brief sesi induk; `get_usage` 5 Nov |

Pola yang terlihat: setiap kali kuota menipis, yang dipangkas adalah **tahap mutu** (Arena, tahap 5–6), padahal sumber borosnya ada di **cara utas dijalankan** (riset Opus paralel, utas panjang). Penghematan yang benar harus terjadi di cara kerja, supaya tahap mutu tidak perlu dikorbankan.

---

## 5. Audit per tahap

Kolom **Dampak**: T = tinggi, S = sedang, K = kecil. Ini perkiraan arah, bukan hasil ukur. Kolom **Hemat berisiko** sengaja dipisah: isinya **tidak** diusulkan sebagai default, hanya sebagai pilihan yang diputuskan penulis.

### Lintas tahap

| Pemborosan utama | Hemat aman untuk mutu | Hemat berisiko untuk mutu | Dampak |
|---|---|---|---|
| Satu utas dipakai lintas tahap atau sepanjang Arena, sehingga konteks tumbuh sampai ratusan ribu token dan terbaca ulang di setiap permintaan. | Satu utas pendek per tahap. Utas berikutnya mulai dari `STATUS.md` § Serah terima (U1). Pakai `/clear` (gratis) di antara tahap, bukan `/compact` pada utas besar. | Menyetel auto-compact lebih rendah (misalnya 300 ribu): pemadatan bisa menghilangkan detail yang belum ditulis ke file. | **T** |
| Melanjutkan utas lama setelah jeda lebih dari 1 jam, sehingga seluruh konteks diproses ulang tanpa cache. | Jangan melanjutkan utas yang sudah diam lebih dari 1 jam; mulai utas baru dari serah terima. | — | S |
| Ganti model di tengah utas (cache per model). | Pilih model dan effort di awal utas (U3). Effort boleh diubah di model 5.5 tanpa merusak cache. | — | S |
| Beban tetap ±86 ribu per permintaan: MCP tak relevan, deskripsi skill tak relevan, CLAUDE.md dengan tabel besar. | Matikan Roblox_Studio dan godot-ai untuk proyek ini (U7). Pindahkan tabel Peta Skill dan Alat dari CLAUDE.md (U8). Tambahkan `# Compact instructions`. | — | K–S, tapi berlaku di **setiap** permintaan |
| Pemicu saat diam: scheduled task, laporan sesi samping ke utas induk yang besar, goal check-in. | Jangan membuat scheduled task dari subagent (PL07). Sesi samping melapor ke utas yang pendek, atau pesan masuk ditahan (`crossSessionInbound: hold`, keputusan penulis). | — | S |
| Kuota tidak tercatat. | `get_usage` di setiap checkpoint, dicatat di `STATUS.md` (U11). | — | tidak langsung, tapi dibutuhkan untuk 8a |

### Pra-0 · Rekap bookmark Instagram

| Pemborosan utama | Hemat aman | Hemat berisiko | Dampak |
|---|---|---|---|
| Tangkapan layar dan gambar poster menumpuk di utas. Gambar lama dibuang per batch saat batas tercapai, dan itu memicu pemrosesan ulang. Utas panjang untuk ±30 postingan. | Pakai `qr.py` (unduh dan pindai QR di skrip) dan `og:description`. Lihat poster sebagai gambar hanya kalau caption dan QR tidak memuat nama, jenjang, atau tenggat. Satu utas per batch ≤30 postingan, dan `lomba.json` diperbarui per postingan (sudah begitu). Model Sonnet. | Tidak membuka poster sama sekali: tenggat dan jenjang bisa salah baca. | S |

### Tahap 0 · Bedah guidebook

| Pemborosan utama | Hemat aman | Hemat berisiko | Dampak |
|---|---|---|---|
| Membaca PDF guidebook sebagai gambar per halaman (Navigation: 8 halaman semua dicek sebagai gambar; PDF Pharfest 14 MB). Guidebook dibaca ulang di tahap-tahap berikutnya. | `baca_pdf.py` dulu (sudah di panduan). Halaman dilihat sebagai gambar **hanya** kalau diberi peringatan "hampir tanpa teks". Setelah `aturan.md` jadi, tahap 1–8 membaca `aturan.md` (±2 ribu token), bukan `guidebook.txt` (Pharfest ±6.700) atau PDF. Model Sonnet, kecuali guidebook rumit. | Tidak membaca FAQ atau lampiran: aturan diskualifikasi sering ada di sana. **Jangan.** | K–S |
| Membaca seluruh `buku-pelajaran.md` dan `bank-juara.md` yang terus membesar. | Baca § Aktif saja, dan untuk bank juara cukup baris bidang/jenjang yang sama (Grep). | — | K |

### Tahap 1 · Arena Ide (tahap termahal)

| Pemborosan utama | Hemat aman | Hemat berisiko | Dampak |
|---|---|---|---|
| **Satu utas untuk seluruh Arena** (satu utas Arena mencapai 74 juta token; layar pemakaian 29 Okt). | Pecah menjadi 3 utas: **1A** bekal, pasaran, tambang literatur, peluang · **1B** loop 1–3 dan kolam · **1C** final (kritik, bukti, cek "sudah ada?", panel, evolusi, paket, adu). Setiap utas mulai dari file. | — | **T** |
| Juri mewarisi model utas utama. Kalau utas Opus, 2/3 juri loop, 12 adu, kritik, dan prediksi pasaran ikut Opus. | `model: sonnet` sebagai bawaan agen `juri-ide` (U2). Haiku hanya untuk kesan 30 detik, jawaban chatbot, dan satu persona yang diputar (PL06). Panel final boleh 1 Opus + 2 Sonnet (diputar). | Semua juri Haiku: Haiku paling sering berbeda pendapat (PL06). **Jangan.** | **T** bila utas utama Opus |
| Riset bekal oleh subagent Opus paralel (Pharfest: limit habis dalam 15 menit). | Sonnet, maksimal 3 paralel, cek `get_usage` dulu (PL11). Setiap peneliti menulis catatannya ke `ide/_riset/` dan mengembalikan ringkasan ≤200 kata + path (U4). | Riset bekal hanya dari WebSearch tanpa membuka sumber: bekal jadi dangkal. | **T** |
| Pencarian bukti finalis (18–27×) dan cek "sudah ada?" (±27×) berjalan di utas utama, sehingga setiap hasil WebSearch/WebFetch menumpuk. | Delegasikan ke 1–3 subagent Sonnet (masing-masing 3 finalis). Hasil ditulis ke `ide/final.md` dengan link dan kata kunci, dan utas utama memeriksa sampel link. Syarat ≥2 bukti dan ≥3 pencarian tetap. | Mengurangi jumlah pencarian: kebaruan palsu lolos (PL13). **Jangan.** | S–T |
| Keluaran juri lengkap (alasan per kriteria) kembali ke utas utama (Navigation ±34 ribu token). | Agen utama langsung menyimpan JSON dan keluaran ke `ide/juri/`, lalu di utas yang sama hanya membaca tabel `arena.py rekap`. Karena utas dipecah (1B → 1C), keluaran ini tidak terbawa ke utas final. | Menghapus "alasan dulu, angka kemudian": mutu penilaian turun (desain `advanced-evaluation`). **Jangan.** Memendekkan alasan menjadi ≤15 kata per kriteria: risiko kecil, perlu diuji. | S |
| Bekal penuh (49–71 KB) dikirim ke 3 generator. | Loop 2–3 sudah menerima "wilayah yang sudah diambil" dan benih jurnal. Kirim bekal penuh di loop 1 saja. | Ringkasan bekal ≤1.500 kata untuk semua generator (U13, hipotesis): ide bisa kurang berpijak pada data. | K–S |
| Persona ditulis di awal prompt juri, sehingga awalan (prefix) setiap juri berbeda dan tidak ada cache bersama. | Susun ulang: aturan, rubrik, pasaran, dan cara kerja di depan; persona dan kartu acak di belakang (U9). Juri yang dipanggil dalam 5 menit bisa berbagi cache awalan. | — | K (tidak terukur) |
| Memanggil ulang `01-ide-dan-tesis.md` utuh di setiap langkah. | Baca bagian yang dibutuhkan saja (Grep/rentang baris) di setiap utas 1A/1B/1C. | — | K |
| Ukuran Arena tetap besar saat kuota tinggal sedikit. | Penulis memilih ukuran Arena S/M/L (PL02) dengan melihat sisa kuota (`get_usage`) di checkpoint tahap 0. | Memakai ukuran S/Kilat saat tenggat masih longgar: keyakinan pada ide juara lebih rendah. | T bila dipilih |

### Tahap 2 · Riset, peta klaim, dossier

| Pemborosan utama | Hemat aman | Hemat berisiko | Dampak |
|---|---|---|---|
| Teks sumber dibaca utuh ke utas utama (Pharfest `riset/teks/` ±54 ribu token). | Simpan teks sumber ke `riset/teks/` lewat skrip atau WebFetch, lalu cari kutipan dengan **Grep** atau baca per rentang. Jangan memuat seluruh file. | Tidak menyimpan teks asli: auditor sitasi dan `cek_naskah --sumber` jadi tidak bisa jalan. **Jangan** (pengaman). | S |
| WebFetch dengan prompt umum ("ringkas halaman ini") mengembalikan ringkasan panjang. | Prompt WebFetch yang sempit: "kutip persis kalimat yang memuat angka X dan nomor halamannya". Hasilnya pendek dan langsung bisa dipakai di peta klaim. | — | K–S |
| Pertanyaan bukti dikerjakan berurutan di utas utama yang terus membesar. | Opsional: 1 subagent Sonnet per pertanyaan bukti (maksimal 3 paralel) yang menulis ke `riset/teks/` dan mengembalikan baris peta klaim berstatus ⚠️. Utas utama yang memverifikasi dan memberi ✅. | Status ✅ diberikan langsung oleh subagent tanpa diverifikasi: melonggarkan peta klaim. **Jangan.** | S |
| PDF regulasi besar dibaca sebagai gambar. | Ekstrak teksnya (`baca_pdf.py`) dan baca halaman yang dikutip saja. | — | S |

### Tahap 3 · Kerangka dan 3b · rencana visual

| Pemborosan utama | Hemat aman | Hemat berisiko | Dampak |
|---|---|---|---|
| Membawa konteks Arena dan riset ke tahap ini. | Utas baru dari `STATUS.md` + `riset/dossier.md` + `riset/sumber.md` (peta klaim). Jangan membaca ulang `ide/loop-*.md`. Opus effort tinggi: kerangka menentukan mutu. | `llm-council` untuk menguji kontra-argumen menambah beberapa panggilan. Opsional, bukan default. | S |
| Mengulang render grafik dan melihat PNG berkali-kali. | `buat_visual.py` dari JSON; lihat gambar sekali per versi akhir. | — | K |

### Tahap 4 · Menulis draf

| Pemborosan utama | Hemat aman | Hemat berisiko | Dampak |
|---|---|---|---|
| Menulis ulang draf utuh berkali-kali di utas (6 versi Pharfest ≈ 21 ribu token). | Draf v1 ditulis sekali ke file. Revisi berikutnya memakai Edit (perubahan saja), bukan menulis ulang dan mencetak seluruh naskah. Cek dengan skrip (`cek_naskah`, `cek_klaim`, `periksa.py`) yang hanya mencetak temuan. | — | S |
| Isi skill gaya (`humanizer`, `stop-slop`, `parafrase-akademik`) tetap ada di konteks setelah dipanggil. | Panggil skill gaya sekali, di akhir tahap 4, di utas yang lalu ditutup. | — | K–S |
| Model penulis. | Opus, effort tinggi. **Jangan dihemat di sini**: kualitas tulisan menentukan lolos penyaringan. | Menulis draf dengan Sonnet: hemat, tapi mutu belum diuji di workflow ini. | — |

### Tahap 5 · Loop juri

| Pemborosan utama | Hemat aman | Hemat berisiko | Dampak |
|---|---|---|---|
| `juri-esai` dan `auditor-sitasi` mewarisi model utas utama. | `model: sonnet` di kedua agen (U2). Pharfest sudah memakai Sonnet di semua juri tahap 5. Auditor sitasi **tetap Sonnet**, bukan Haiku, karena hasilnya menentukan temuan Kritis. | Auditor dengan Haiku: salah baca dukungan kutipan. **Jangan.** | T bila utas Opus |
| Putaran berlanjut walau skor mendatar (Pharfest ±5 putaran, skor mentok 7,7–7,8). | Aturan berhenti saat skor mendatar (PL17). Batas 3 putaran ditegakkan, dan penahan isi dilaporkan ke penulis. | — | **T** di tahap ini |
| Banding berpasangan × 2 dengan dua naskah utuh di setiap putaran (±17 ribu token bahan). | Banding hanya untuk kriteria yang disentuh revisi (sudah tercatat di Log perubahan). Kirim seluruh naskah, tapi minta penilaian kriteria yang relevan saja. | Banding satu arah saja: bias posisi tidak terhapus. **Jangan.** | K–S |
| Keluaran juri dan DA kembali ke utas yang juga dipakai merevisi. | Tahap 5 dan 6 per putaran di utas sendiri: putaran N menilai, menulis `review-vN.md`, lalu selesai. Revisi di utas baru yang membaca `review-vN.md` + draf. | Menggabungkan juri rubrik dan DA dalam satu panggilan: independensi hilang. **Jangan.** | S |

### Tahap 6 · Revisi dan build

| Pemborosan utama | Hemat aman | Hemat berisiko | Dampak |
|---|---|---|---|
| Render PDF dan melihat semua halaman di setiap versi antara. | `cek_docx.py` dulu. Versi antara: lihat halaman yang berubah saja. **Cek akhir tetap melihat setiap halaman sekali** (pengaman `06-revisi-final.md`). | Melewati cek halaman akhir. **Jangan.** | S |
| Utas revisi membawa seluruh riwayat tahap 5. | Utas build terpisah dan pendek, dengan Sonnet (perintah, cek, render). | — | S |

### Tahap 7 dan 7C · Visual terpisah dan presentasi

| Pemborosan utama | Hemat aman | Hemat berisiko | Dampak |
|---|---|---|---|
| Iterasi desain berbasis gambar (render, lihat, ubah, ulangi). | Hanya kalau diminta (sudah begitu). Batasi 2–3 iterasi, lihat pratinjau beresolusi rendah, satu utas per artefak. | — | S bila dipakai |

### Tahap 8 · Evaluasi

| Pemborosan utama | Hemat aman | Hemat berisiko | Dampak |
|---|---|---|---|
| Data kuota tidak ada, sehingga 8a harus menebak. | Catat `get_usage` di setiap checkpoint (U11). 8b dan 8c di utas baru (sudah di panduan). | — | K (biaya), T (nilai data) |

### Mode Kilat

| Pemborosan utama | Hemat aman | Hemat berisiko | Dampak |
|---|---|---|---|
| Mode Kilat hanya ditawarkan berdasarkan tenggat, padahal di Pharfest dan Navigation yang habis duluan adalah **kuota**. | Di checkpoint tahap 0, tampilkan `get_usage` di samping garis waktu, dan biarkan penulis memilih jalur penuh, ukuran Arena M (PL02), atau Kilat. Semua pengaman Kilat tetap. | Memakai Kilat otomatis saat kuota tinggi. **Jangan**: penulis yang memutuskan. | T bila dipilih |

---

## 6. Model per peran (usulan U3)

Prinsip: Opus dipakai di tempat ide dan tulisan ditentukan. Sonnet untuk penilaian, riset, dan orkestrasi. Haiku untuk reaksi cepat dan peniruan peserta biasa. Model dipilih **di awal utas**, tidak diganti di tengah utas.

| Peran | Model | Effort utas | Alasan |
|---|---|---|---|
| Utas pra-0, tahap 0, tahap 2, tahap 6 (build), tahap 8 | Sonnet | medium | Ekstraksi, verifikasi, dan perintah alat. Pengaman ada di alat dan auditor. |
| Utas 1A (bekal, peluang) dan 1C (kolam/final, hibrida, paket) | Opus | high | Rumusan peluang dan paket menentukan mutu ide. |
| Utas 1B (loop: membersihkan kartu, mengacak, menyimpan JSON) | Sonnet | medium | Pekerjaan mekanis. Generator dipanggil dengan `model: opus` secara eksplisit. |
| Generator ide (3) | Opus | — | Ide adalah prioritas utama, dan panggilannya hanya 3. |
| Peneliti bekal / tambang literatur | Sonnet, ≤3 paralel | — | PL11 |
| Prediksi pasaran | Sonnet | — | |
| Jawaban chatbot | Haiku | — | Meniru jawaban yang didapat peserta biasa. |
| Juri loop (9) | Sonnet ×2 + Haiku ×1, diputar per persona | — | PL06. Sudah dipakai di Navigation. |
| Kesan 30 detik | Haiku | — | Reaksi singkat |
| Kritik finalis | Sonnet | — | |
| Panel final (3) | Opus ×1 + Sonnet ×2, diputar | — | Keputusan penting, hanya 3 panggilan. |
| Adu berpasangan (12) | Sonnet | — | Banyak panggilan, keputusan biner. Sudah dipakai di Pharfest. |
| Pencari bukti / cek "sudah ada?" | Sonnet | — | |
| Utas tahap 3 (kerangka) dan tahap 4 (draf) | Opus | high | Mutu tulisan |
| Utas revisi tahap 6 (isi) | Opus | medium–high | |
| Juri rubrik, DA, konfirmasi, banding (tahap 5) | Sonnet | — | Sudah dipakai di Pharfest. |
| Auditor sitasi | Sonnet | — | Menentukan temuan Kritis, jadi bukan Haiku. |
| Visual (tahap 7) | Sonnet | medium | |

Effort `max` tidak dipakai di mana pun. Dokumen resmi menyebutnya "prone to overthinking", dan thinking ditagih sebagai token keluaran.

---

## 7. Subagent atau utas utama?

**Subagent lebih hemat** kalau:
- pekerjaannya menghasilkan banyak keluaran yang tidak perlu dibaca utuh, misalnya pencarian web, membaca sumber panjang, riset bekal, dan cek "sudah ada?";
- utas utama sudah besar, karena setiap token hasil yang masuk ke sana terbaca ulang di setiap permintaan berikutnya;
- butuh konteks bersih demi mutu, misalnya juri buta, DA, dan auditor. Untuk peran ini subagent memang wajib, bukan pilihan hemat.

**Utas utama lebih hemat** kalau:
- tugasnya kecil (1–3 pemanggilan alat): subagent membawa prompt sistem dan alatnya sendiri, mulai tanpa cache induk, dan cache-nya hanya 5 menit;
- tugasnya butuh konteks yang memang sudah ada di utas, misalnya menulis draf dari kerangka dan peta klaim yang baru dibaca;
- utasnya masih kecil (awal utas).

**Ilustrasi** (asumsi, bukan ukuran): 20 hasil WebSearch/WebFetch × ±2 ribu token = ±40 ribu token yang masuk ke utas utama. Kalau utas berlanjut 150 permintaan lagi, itu terbaca ulang ±6 juta token. Subagent yang mengembalikan ringkasan 500 token hanya menambah ±75 ribu token baca ulang, ditambah biaya subagent itu sendiri.

### Pola "satu utas pendek per tahap"

Usulan bagian baru di `lomba/_template/STATUS.md` (U1):

```markdown
## Serah terima (diperbarui di setiap checkpoint)
- Tahap selesai / berikutnya:
- Baca dulu (maks. 5 berkas): STATUS.md, aturan.md, …
- Jangan dibaca ulang: guidebook.pdf/.txt (pakai aturan.md), ide/loop-*.md (pakai ide/final.md), riset/teks/* (Grep saja)
- Keputusan penulis yang mengikat:
- Pertanyaan terbuka:
- Kuota saat serah terima: 5 jam __% · mingguan __% (get_usage)
- Utas berikutnya: model __ · effort __
```

Urutan utas untuk jalur penuh: 0 → 1A → 1B → 1C → 2 → 3+3b → 4 → 5/6 per putaran → 6 build → (7) → 8a. Totalnya ±10–12 utas pendek, bukan 2–3 utas panjang.

---

## 8. Daftar usulan

Jenis mengikuti `workflow/08-evaluasi.md` § 8c: **bug** dan **proses** boleh diterapkan setelah 1 lomba. **Hipotesis** (strategi) baru boleh diubah setelah ≥3 lomba dengan hasil diketahui. Tidak ada usulan yang melonggarkan pengaman.

| No | Usulan | Jenis | File terkait | Dampak | Risiko mutu | PL |
|---|---|---|---|---|---|---|
| U1 | Satu utas pendek per tahap. Arena dipecah menjadi 1A/1B/1C. Tambah § Serah terima di template STATUS. Pakai `/clear` di antara tahap. Jangan melanjutkan utas yang diam lebih dari 1 jam. | proses | `CLAUDE.md` § Memulai/Melanjutkan, `lomba/_template/STATUS.md`, `workflow/01-ide-dan-tesis.md` § Catatan teknis | **T** | rendah: semua hasil sudah di file | PL24 |
| U2 | Tambah `model: sonnet` di frontmatter `juri-ide`, `juri-esai`, dan `auditor-sitasi`. Panggilan yang butuh model lain (Haiku untuk kesan, Opus untuk 1 juri panel final) tetap memakai parameter `model` di alat Agent. Ubah kalimat "paling tidak satu juri berbeda" menjadi tabel model per peran. | bug | `.claude/agents/*.md`, `workflow/01-ide-dan-tesis.md` § Juri buta, `templates/prompt-ide-juri.md` langkah 3 | **T** bila utas Opus | rendah: Sonnet/Haiku sudah dipakai di Navigation dan Pharfest | PL25 |
| U3 | Tabel model dan effort per peran/utas (§ 6). Model dipilih di awal utas dan tidak diganti di tengah. | proses | `CLAUDE.md` (atau berkas peta skill, U8), `workflow/00-…` § garis waktu | S–T | rendah | PL29 |
| U4 | Subagent riset dan pencarian (bekal, tambang literatur, bukti finalis, cek "sudah ada?", pertanyaan bukti tahap 2): Sonnet, ≤3 paralel, `get_usage` dulu, hasil ditulis ke file, mengembalikan ringkasan ≤200 kata + path. Utas utama tetap memverifikasi dan memberi ✅. | proses | `workflow/01-…` § Langkah 0/0b, § Final 3–4; `workflow/02-riset.md` | **T** | rendah, selama verifikasi tetap di utas utama | PL11, PL26 |
| U5 | Membaca seperlunya: sesudah tahap 0 baca `aturan.md`, bukan guidebook; `riset/teks/` lewat Grep/rentang; berkas workflow per bagian; draf direvisi dengan Edit, bukan ditulis ulang utuh. | proses | `workflow/00`, `02`, `04`, `06` | S | tidak ada | PL26 |
| U6 | Batasi alat agen juri dengan daftar izin `tools:`. Dokumen resmi: tanpa `tools`, agen mewarisi semua alat, termasuk scheduled task dan MCP. Daftar kosong biasanya gagal diluncurkan, jadi uji dulu formatnya (misalnya satu alat yang tidak berbahaya, atau `disallowedTools` dengan pola `mcp__*`) memakai `/agents`. Ini juga menutup PL07. | bug | `.claude/agents/*.md` | K (token), T (keamanan) | tidak ada | PL25, PL07 |
| U7 | Matikan Roblox_Studio dan godot-ai untuk proyek esai. Keduanya terdaftar di tingkat pengguna (`~/.claude.json`), sehingga muncul di semua proyek. Lakukan **sebelum** membuka utas, karena mengubah server di tengah utas bisa merusak cache. Ini pengaturan akun penulis, bukan file workflow. | proses | pengaturan MCP (`/mcp` atau konektor aplikasi) | K per permintaan, tapi berlaku di semua permintaan | tidak ada | PL27 |
| U8 | Rampingkan CLAUDE.md: pindahkan § Peta Skill, tabel skill akun, dan § Alat (±3 ribu token) ke `workflow/PETA-SKILL.md` dan `tools/README.md`, yang dibaca di awal setiap tahap. Di CLAUDE.md tinggal satu baris rujukan. Tambahkan `# Compact instructions` (pertahankan tahap aktif, ID klaim, keputusan penulis, path file; buang hasil pencarian dan juri yang sudah tersimpan). | proses | `CLAUDE.md` | K–S | rendah: risiko Peta Skill terlewat, ditutup dengan baris rujukan wajib | PL27 |
| U9 | Susun ulang prompt juri dan adu supaya bagian yang sama untuk semua juri (aturan, rubrik, pasaran, cara kerja) ada di depan, dan persona serta kartu acak di belakang. Tujuannya cache awalan bersama (TTL subagent 5 menit). | proses | `templates/prompt-ide-juri.md`, `prompt-ide-adu.md`, `prompt-juri.md` | K (tidak terukur) | rendah: perlu dicek bahwa persona tetap jelas | PL30 |
| U10 | Tahap 5: tegakkan batas 3 putaran, berhenti saat skor mendatar (PL17), dan jalankan banding hanya untuk kriteria yang disentuh revisi. Setiap putaran (nilai, lalu revisi) di utas sendiri. | proses | `workflow/05-review.md`, `06-revisi-final.md` | **T** di tahap 5 | rendah | PL17, PL24 |
| U11 | Catat `get_usage` (5 jam %, mingguan %) di setiap checkpoint di `STATUS.md` § Serah terima, dan tambah kolom kuota per tahap di template `evaluasi.md`. | proses | `lomba/_template/STATUS.md`, `lomba/_template/evaluasi.md`, `workflow/08-evaluasi.md` § 8a | tidak langsung | tidak ada | PL28 |
| U12 | Checkpoint tahap 0 menampilkan sisa kuota di samping garis waktu. Penulis memilih jalur penuh, Arena M (PL02), atau Kilat. Tidak ada pemangkasan otomatis. | proses | `workflow/00-…`, `workflow/MODE-KILAT.md` | T bila dipilih | **ada** (ukuran Arena lebih kecil), diputuskan penulis | PL02, PL28 |
| U13 | Bekal ringkas (≤1.500 kata) untuk generator; bekal penuh hanya untuk agen utama dan loop 1. | **hipotesis** | `workflow/01-…` § Generator, `templates/prompt-ide-generator.md` | K–S | **ada**: ide bisa kurang berpijak pada data; uji dulu ≥3 lomba | PL31 |
| U14 | Cegah pemicu saat diam: subagent tidak membuat scheduled task (PL07, U6); sesi samping melapor ke utas pendek; pertimbangkan `crossSessionInbound: hold` di utas tahap yang panjang. Pengaturan ini milik penulis. | proses | `CLAUDE.md` (catatan), pengaturan penulis | S | tidak ada | PL24 |
| U15 | Gambar dan PDF: tahap 0 hanya halaman scan yang dilihat sebagai gambar. Pra-0 tanpa tangkapan layar berulang. Tahap 6 versi antara hanya melihat halaman yang berubah, dan cek akhir tetap melihat semua halaman sekali. | proses | `workflow/00`, `06`, `lomba-ig/SKILL.md` | S | tidak ada, karena pengaman cek akhir tetap | PL26 |
| U16 | Skill: panggil skill berat (`humanizer`, `docx`, `pdf`, `deep-research`) di utas yang membutuhkannya saja, karena isinya tetap di konteks sampai utas ditutup. Opsional untuk penulis: matikan skill akun/pengguna yang tidak pernah dipakai untuk esai (misalnya `hyperframes`), atau beri `disable-model-invocation: true`. Daftar skill sesi ini ±10 ribu token. | proses | `CLAUDE.md` § Pemakaian skill; pengaturan skill penulis | K–S | tidak ada | PL27 |

### Perkiraan dampak gabungan (ilustrasi, bukan janji)

Dengan rumus *permintaan × rata-rata konteks*: kalau Arena memakai ±250 permintaan dengan rata-rata ±300 ribu token dalam satu utas (±75 juta), lalu dipecah menjadi 3 utas yang masing-masing mulai di ±90 ribu dan berhenti di ±200 ribu (rata-rata ±145 ribu), jumlah yang dibaca turun ke ±36 juta untuk pekerjaan yang sama. Itu kira-kira separuhnya. Hasil sebenarnya baru diketahui setelah U11 dijalankan di lomba berikutnya.

---

## 9. Batas audit ini

- Bobot *cache read* terhadap limit paket Team tidak dipublikasikan, jadi semua "dampak" di sini adalah arah, bukan persentase limit.
- Jumlah permintaan per utas dan token per subagent di lomba lama tidak tercatat. Angka 74 juta dan 170/180 juta berasal dari memori proyek (layar pemakaian 29 Okt), bukan dari ekspor log.
- Perkiraan token berkas memakai byte ÷ 4.
- Belum diuji apakah daftar izin `tools:` dengan alat minimal benar-benar membuat agen juri tanpa alat berbahaya (U6), dan apakah susunan ulang prompt (U9) benar-benar memberi cache bersama.
- Model Fable punya limit mingguan terpisah (0% terpakai saat audit). Audit ini tidak menilai apakah Fable cocok untuk peran tertentu.

## 10. Sumber

- COSTS — https://code.claude.com/docs/en/costs.md
- CACHE — https://code.claude.com/docs/en/prompt-caching.md
- Subagent — https://code.claude.com/docs/en/sub-agents.md
- Model, effort, auto-compact — https://code.claude.com/docs/en/model-config.md
- Jendela konteks dan `/compact` — https://code.claude.com/docs/en/context-window.md
- MCP dan tool search — https://code.claude.com/docs/en/mcp.md
- Skill — https://code.claude.com/docs/en/skills.md
- Memori dan CLAUDE.md — https://code.claude.com/docs/en/memory.md
- Read, WebFetch, WebSearch — https://code.claude.com/docs/en/tools-reference.md
- Aplikasi desktop — https://code.claude.com/docs/en/desktop.md
- Model dan limit — https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code
- Limit Pro/Max — https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan
- Team/Enterprise — https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan
- Cara kerja limit — https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work
- Data proyek: `get_usage` (5 Nov 2026), `lomba/*/STATUS.md`, `lomba/*/evaluasi.md`, memori proyek `kuota-pemakaian`
