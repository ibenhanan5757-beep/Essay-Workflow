# Survei pipeline AI untuk generate dan ranking ide, sebagai tolok ukur Arena Ide

Status verifikasi: [V] = halaman arXiv/blog dibuka langsung; [S] = hanya dari ringkasan hasil pencarian (judul, snippet, atau sumber sekunder); [?] = tidak terverifikasi. ID arXiv berawalan 26xx yang muncul di hasil pencarian (mis. 2608.29696, 2609.15938, 2607.14118) tidak saya buka dan tidak boleh dikutip tanpa dicek.

## 1. Google AI co-scientist [V]
- Gottweis et al., "Accelerating scientific discovery with Co-Scientist", arXiv 2502.18864 (v1 Feb 2025; v2 Jun 2026; tercatat terbit di Nature 2026). https://arxiv.org/abs/2502.18864
- Blog resmi: https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/
- Enam agen di bawah Supervisor: Generation, Reflection, Ranking, Evolution, Proximity, Meta-review. Blog menyebut "self-play scientific debate" sebagai langkah penalaran, dan menurut blog pula Ranking memakai turnamen Elo. Detail Proximity (klaster/dedup) dan Meta-review hanya tersirat di blog; detailnya ada di makalah penuh, yang tidak saya baca [?].
- Elo hanya metrik otomatis internal ("tidak berbasis ground truth independen"). Pada soal GPQA diamond, Elo lebih tinggi berkorelasi positif dengan peluang benar. Skala waktu komputasi: kualitas (Elo top-1 dan rata-rata top-10) naik terus pada 15 tujuan riset terbuka. Pada 11 tujuan, ahli menilai novelty dan impact lebih tinggi; sampel kecil.
- Peran manusia: memberi tujuan, ide benih, dan umpan balik bahasa alami; validasi laboratorium dengan "expert-in-the-loop".

## 2. Pipeline ide lain
- **AI Scientist v1**, Lu et al., arXiv 2408.06292 [V abstrak]: ide, kode, eksperimen, makalah, dan peninjau otomatis. Cek novelty lewat pencarian literatur ada di isi makalah, tidak terverifikasi dari abstrak [?]. https://arxiv.org/abs/2408.06292
- **AI Scientist v2**, Yamada et al., arXiv 2504.08066 [V]: pohon pencarian agentik, tanpa templat kode; satu dari tiga naskah otonom melewati ambang rata-rata penerimaan workshop ICLR. https://arxiv.org/abs/2504.08066
- **SciMON**, Wang et al., arXiv 2305.14259 [S]: generate dari konteks masalah dengan retrieval, lalu loop novelty: bandingkan dengan literatur terambil dan revisi. Hasil dilaporkan cenderung inkremental dan kurang detail. https://arxiv.org/pdf/2305.14259
- **ResearchAgent**, Baek et al., arXiv 2404.07738 [?]: tidak ditemukan sumber primer; deskripsi sekunder (generasi iteratif + agen peninjau LLM + memori entitas).
- **Nova**, arXiv 2410.14255 [S]: perencanaan dan pencarian iteratif, benih berbasis teori inovasi, retrieval multi-ronde, menargetkan novelty dan diversity. https://arxiv.org/pdf/2410.14255
- **Chain of Ideas (CoI)**, Li et al., arXiv 2410.13185 [V]: paper disusun sebagai rantai perkembangan bidang; protokol **Idea Arena** (turnamen round-robin pairwise, Elo per metode, kedua urutan dinilai) [S untuk detail Elo/urutan]. Biaya ~US$0,50 per ide. https://arxiv.org/abs/2410.13185
- **Scideator**, Radensky et al., arXiv 2409.14634 [S]: ekstraksi facet (tujuan, mekanisme, evaluasi) dari paper, rekombinasi, dan **Idea Novelty Checker** (retrieve-then-rerank, label novel/tidak plus saran mengganti facet). Studi pengguna 19 lalu 22 peserta. https://arxiv.org/abs/2409.14634
- **LiveIdeaBench**, Ruan et al., arXiv 2412.17596 [S]: prompt satu kata kunci, juri LLM menilai originality/feasibility/clarity; kecerdasan umum model tidak selalu sejalan dengan kreativitas ilmiah. https://arxiv.org/html/2412.17596v3
- **IdeaBench** (~Okt 2024) [?]: hanya muncul di daftar; halaman tidak dibuka.
- **Si, Yang, Hashimoto 2024**, arXiv 2409.04109 [V abstrak]: 100+ peneliti NLP; ide LLM dinilai lebih novel (p<0,05) tapi sedikit kurang feasible; kegagalan self-evaluation LLM dan kurangnya diversity disebut masalah terbuka. https://arxiv.org/abs/2409.04109 Detail dari sumber sekunder [S]: 4000 ide benih per topik, dedup embedding ambang 0,8, tersisa ~5% unik; judul ide sebelumnya ditempel di prompt agar tidak mengulang; kondisi AI+rerank oleh manusia mendapat novelty 5,81 (lebih tinggi). https://arxiv.org/pdf/2409.04109
- **Ideation-Execution Gap**, Si et al., arXiv 2506.20803 [V]: 43 peneliti mengeksekusi ide (100+ jam). Skor ide LLM turun lebih tajam daripada ide pakar (novelty, excitement, effectiveness, overall); peringkat banyak yang terbalik. Menilai ide tanpa hasil eksekusi sulit. https://arxiv.org/abs/2506.20803

## 3. Bukti per pertanyaan
**(a) Keruntuhan diversity dan perbaikannya**
- Meincke, Mollick, Terwiesch, arXiv 2402.01727 [V]: pool ide GPT-4 kurang beragam dibanding kelompok manusia; rekayasa prompt memperbaiki; chain-of-thought paling beragam dan paling banyak ide unik. https://arxiv.org/abs/2402.01727
- Studi Columbia, arXiv 2602.20408 [S]: dua mekanisme: fiksasi (output awal membatasi yang berikut) dan kolaps ke satu distribusi. CoT mengurangi fiksasi; persona biasa lebih baik dari persona selebritas; gabungan keduanya terbaik. https://www.emergentmind.com/papers/2602.20408
- arXiv 2604.18005 [S]: kolaps multi-agen terutama dari struktur interaksi; jaga independensi dan perbedaan pendapat. https://arxiv.org/pdf/2604.18005.pdf
- Desain dialog multi-agen untuk ideasi, SIGDIAL 2025, arXiv 2507.08350 [S]: trade-off diversity agen, paralelisme, kedalaman interaksi. https://arxiv.org/html/2507.08350v1
- Tidak ditemukan uji langsung campuran beberapa keluarga model untuk diversity [?].
- Teknik lain terverifikasi sebagian: seeding dengan literatur (SciMON, CoI, Nova), daftar judul sebelumnya di prompt (Si 2024).

**(b) Evolusi vs satu kali pilih** [S, lemah]: satu makalah eksekusi menyatakan evolutionary search mengalahkan best-of-N pada anggaran sama; SciDER (arXiv 2603.01421) memakai operator improve (tulis ulang pada dimensi terlemah) dan combine (dua induk); ada peringatan bahwa tekanan seleksi menyebabkan diversity collapse (huggingface.co/papers/2606.10587). Co-scientist memakai Evolution agent tetapi ablasi spesifik tidak saya verifikasi [?].

**(c) Elo/pairwise vs rubrik pointwise** [S]: Si 2024 menemukan skor Likert LLM selaras buruk dengan preferensi manusia dan LLM lebih baik meranking (dikutip CoI). CoI memakai round-robin Elo dengan kedua urutan. Studi novelty pada pasangan paper (SchNovel, arXiv 2409.16605 [V abstrak]) memperkenalkan RAG-Novelty (retrieve paper mirip lalu nilai) yang mengungguli baseline; perbandingan pairwise vs pointwise tidak ada di abstrak [?] (sumber sekunder bilang pairwise jauh lebih baik). https://arxiv.org/abs/2409.16605

**(d) Bias juri dan novelty vs feasibility** [S]: Ideation Arena (arXiv 2608.29696 [?], ID perlu dicek): kesepakatan juri LLM dengan pakar sekitar 54,4% novelty, 53,8% feasibility, 56,8% overall; juri LLM belum bisa mereproduksi preferensi pakar. Self-preference: Wataoka et al., arXiv 2404.13076 (terkait perplexity); studi 2026 menyebut sebagian efek artefak ketidakpastian evaluator. Bias posisi dan panjang: Zheng et al. MT-Bench (tidak diverifikasi langsung [?]). Panel juri idealnya beda model dari generator.

**(e) Cek novelty otomatis**: retrieve-then-compare ada di SciMON, Scideator (novelty checker), RAG-Novelty, AI Scientist v1 (tidak terverifikasi detail), dan InnoEval arXiv 2602.14367 [S] (evaluasi berbasis pengetahuan multi-perspektif).

## 4. Kompetisi/hackathon/pitch
- Falk, Chen et al., arXiv 2503.04290 [S]: 193.353 proyek Devpost, 30 proyek dibandingkan antara juri LLM dan manusia; LLM sebagai juri pendamping (hibrid), perlu dipaksa lebih kritis (LLM terlalu afirmatif). https://arxiv.org/pdf/2503.04290
- PBIG-DATA, arXiv 2604.22517 [S]: ~3000 skor pakar atas 300 ide produk; disagreement pakar besar; juri yang dipersonalisasi lebih cocok daripada juri agregat. https://arxiv.org/html/2604.22517v1
- Ideasi untuk lomba esai secara khusus: tidak ditemukan [?].

## 5. Tabel perbandingan
| Pipeline | Generasi | Dedup | Cek novelty | Ranking | Refinement/evolusi | Peran manusia |
|---|---|---|---|---|---|---|
| Arena Ide (existing) | 3 loop x 12, 3 lensa kreativitas, 1 prompt | Tidak eksplisit | ≥2 sumber pendukung per finalis (mencari dukungan, bukan overlap) | Rubrik berbobot, 3 juri buta, median, gerbang; adu pairwise 2 urutan di top 4 | Tidak ada | Memilih juara akhir |
| Co-scientist | Agen Generation (+ debat self-play) | Agen Proximity (klaster) | Reflection (kritik, termasuk literatur) | Turnamen Elo + debat | Agen Evolution, loop berulang, Meta-review | Tujuan, benih, umpan balik |
| SciMON | Dari konteks + retrieval | n/a | Loop novelty terhadap literatur | n/a | Revisi iteratif | n/a |
| CoI | Rantai paper | n/a | Lewat Idea Arena | Round-robin Elo (2 urutan) | Iterasi dalam rantai | n/a |
| Scideator | Rekombinasi facet | n/a | Novelty Checker (retrieve-rerank) + ganti facet | Pengguna | Iterasi novelty | Interaktif |
| Nova | Retrieval multi-ronde + benih teori | Target diversity | Via retrieval | n/a | Iteratif | n/a |
| Si 2024 | Overgenerate 4000 + judul sebelumnya di prompt | Embedding 0,8 | Cek LLM | LLM ranker (lemah) / pakar | n/a | Re-rank manusia terbaik |

## 6. Kesimpulan tolok ukur
Arena Ide sudah punya: juri buta berpersona, gerbang, median, adu pairwise dua urutan, bukti sumber, dan manusia memutuskan. Yang tidak ada: dedup eksplisit, cek novelty terhadap tumpang tindih (bukan dukungan), evolusi, panel multi-model, ranking Elo/turnamen lebih luas, benih retrieval, dan validasi juri vs manusia. Tidak ada bukti bahwa juri LLM menilai novelty/feasibility dengan baik (agreement ~54%); jangan memberi bobot tinggi pada skor LLM tanpa kalibrasi.
