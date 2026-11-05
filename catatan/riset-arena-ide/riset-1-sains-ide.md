# Riset 1: Sains generasi dan seleksi ide (untuk audit pipeline Arena Ide)

Catatan metode: semua tautan di bawah muncul di hasil pencarian sesi ini. Sebagian besar isi diambil dari abstrak/ringkasan di hasil pencarian, bukan dari membaca teks penuh. Angka rinci hanya dikutip bila muncul di hasil. Yang tidak terverifikasi ditandai **[UNVERIFIED]**.

## 1. Generasi ide dan kualitas ide terbaik

**1.1 Girotra, Terwiesch & Ulrich (2010), Management Science 56(4):591-605.** Kinerja kelompok didefinisikan sebagai kualitas ide TERBAIK, bukan rata-rata atau jumlah. Struktur "hybrid" (individu bekerja sendiri dulu, baru berkumpul) menghasilkan lebih banyak ide, ide lebih baik, dan lebih mampu memilah kualitas dibanding "team" (brainstorming bersama). Membangun di atas ide orang lain tidak membuat ide lebih banyak atau lebih baik.
Tautan: https://repository.upenn.edu/oid_papers/191 ; https://pubsonline.informs.org/doi/pdf/10.1287/mnsc.1100.1172
Implikasi: tahap generasi sebaiknya independen (beberapa proses terpisah yang tidak saling melihat), baru digabung di tahap seleksi. Loop 1-3 yang saling melihat hasil sebelumnya berisiko "anchoring" ke ide awal.

**1.2 Kornish & Ulrich (2014), J. Marketing Research 51(1):14-26.** Data Quirky: ide mentah penting (ide 1 SD lebih baik ~ +50% laju penjualan); panel konsumen online (sampel sekecil 20) lebih baik memprediksi ide bagus daripada rating pakar.
Tautan: https://mackinstitute.wharton.upenn.edu/2014/the-importance-of-the-raw-idea-in-innovation-testing-the-sow-s-ear-hypothesis/ (juga https://www.ama.org/2017/07/19/does-the-raw-idea-in-innovation-really-matter/)
Implikasi: ide mentah memang penentu; untuk esai, "pembaca awam terwakili" (juri persona audiens umum) layak ditambahkan di samping juri pakar. Catatan: topik "duplikat ide" Kornish-Ulrich tidak saya temukan di sumber ini **[UNVERIFIED]**.

**1.3 Kuantitas melahirkan kualitas dan logika nilai ekstrem.** Argumen bahwa hanya ide teratas yang penting (sehingga variansi dan jumlah sampel lebih penting daripada rata-rata) adalah dasar kerangka Girotra dkk. (kinerja = kualitas ide terbaik). Pernyataan "ide kuat sering muncul belakangan" (Rietzschel dkk.) **[UNVERIFIED]**: pencarian hanya memberi daftar publikasi, bukan temuan.
Implikasi: tujuan pipeline adalah memaksimalkan max, bukan mean. Perbanyak kandidat yang BENAR-BENAR berbeda; jangan optimasi skor rata-rata.

## 2. Ideasi LLM

**2.1 Girotra, Meincke, Terwiesch, Ulrich (2023), "Ideas Are Dimes a Dozen".** (Catatan: hasil pencarian menunjukkan penulisnya bukan Mollick.) ChatGPT-4 menghasilkan ide jauh lebih cepat/murah; kualitas rata-rata (purchase intent) lebih tinggi dari ide mahasiswa, dengan variansi kualitas lebih tinggi. Penulis menyatakan hambatan bergeser dari generasi ke evaluasi/seleksi, yang LLM belum cocok kerjakan.
Tautan: https://mackinstitute-wharton.relayto.com/e/ideas-are-dimes-a-dozen-large-language-models-for-idea-generation-in-innovation-je5os6xrtbnsj
Implikasi: generasi murah, jadi pipeline harus menaruh anggaran di seleksi, bukan di generasi.

**2.2 Meincke, Mollick, Terwiesch (2024), "Prompting Diverse Ideas: Increasing AI Idea Variance", arXiv 2402.01727.** GPT-4 tanpa prompt khusus menghasilkan kumpulan ide kurang beragam daripada kelompok manusia. Prompt chain-of-thought memberi skor keragaman tertinggi atau mendekati tingkat manusia; prompt persona ("pikir seperti Steve Jobs") juga membantu; perangkat kreativitas HBR kurang membantu.
Tautan: https://arxiv.org/pdf/2402.01727 ; https://mackinstitute.wharton.upenn.edu/2024/new-paper-on-prompting-diverse-ideas-increasing-ai-idea-variance/
Implikasi: gunakan prompt CoT, persona/kendala heterogen, dan ukur duplikasi (kemiripan kosinus) sebelum juri menilai. Satu prompt diulang = kumpulan ide homogen.

**2.3 Makalah lanjutan (2026, arXiv, penulis Terwiesch, Meincke, Girotra, Mollick, Nave, Ulrich).** Ringkasan pencarian: menggabungkan ide lintas vendor LLM, rekayasa prompt, dan menyuntik persona/kendala menaikkan keragaman hampir ke level manusia. Hanya dilihat lewat entri IDEAS/RePEc: https://ideas.repec.org/p/arx/papers/2607.27553.html **[sebagian UNVERIFIED: tidak dibuka]**.
Implikasi: pakai beberapa model/vendor sebagai generator, bukan satu.

**2.4 Si, Yang & Hashimoto (2024), arXiv 2409.04109.** 79 pakar mengulas buta ide pakar vs ide AI vs ide AI yang di-rerank manusia. Ide AI dinilai lebih NOVEL secara signifikan (p<0.05) dan sedikit kurang layak; penulis mencatat kegagalan evaluasi-diri LLM dan kurangnya keragaman generasi (duplikasi saat diskala) sebagai masalah terbuka.
Tautan: https://arxiv.org/abs/2409.04109v1 ; https://arxiv.org/html/2409.04109v1
Implikasi: jangan percaya LLM menilai ide LLM; dedup wajib; novelty LLM nyata tetapi kelayakan perlu diperiksa.

**2.5 Si, Hashimoto, Yang (2025), "The Ideation-Execution Gap", arXiv 2506.20803 (juga poster ICLR 2026).** 43 peneliti mengeksekusi ide (>100 jam). Sebelum eksekusi ide LLM dinilai lebih tinggi di semua metrik; setelah eksekusi skor ide LLM turun lebih tajam, peringkat terbalik (manusia lebih tinggi pada banyak metrik, pembalikan itu sendiri tidak signifikan; N kecil).
Tautan: https://arxiv.org/abs/2506.20803 ; https://arxiv.org/html/2506.20803v1
Implikasi: ide yang tampak bagus di kartu ide belum tentu bagus saat ditulis. Tambahkan uji "bisa dieksekusi jadi esai" (outline cepat atau paragraf pembuka) sebelum final.

**2.6 Doshi & Hauser (2024), Science Advances 10(28):eadn5290.** Cerita dengan ide dari GPT-4 dinilai lebih kreatif, lebih baik, lebih enak dibaca (terutama untuk penulis kurang kreatif), tetapi cerita dengan bantuan AI lebih mirip satu sama lain.
Tautan: https://pmc.ncbi.nlm.nih.gov/articles/PMC11244532
Implikasi: kalau banyak peserta lomba memakai AI, ide "bagus-rata-rata" akan menumpuk; ide juara harus menyimpang dari mode distribusi AI. Tambahkan juri/filter "apakah ini ide yang akan dipilih kebanyakan peserta ber-AI?" (lihat templates/prompt-ide-pasaran.md).

## 3. Seleksi ide oleh manusia

**3.1 Rietzschel, Nijstad & Stroebe (2010), British J. Psychology 101:47-68** (bukan 2006; makalah 2006 berbeda, J. Exp. Soc. Psych. 42:244-251). Peserta buruk memilih ide kreatif; mereka condong ke ide layak dan diinginkan dengan mengorbankan orisinalitas; instruksi "pilih yang kreatif" memperbaiki orisinalitas pilihan tetapi menurunkan kepuasan/efektivitas yang dinilai. Menambah ide tidak banyak membantu memilih ide kreatif.
Tautan: https://dspace.library.uu.nl/bitstream/handle/1874/7404/full.pdf
Implikasi: rubrik juri yang menghargai "layak/jelas" akan menggeser ke ide aman. Pisahkan dimensi orisinalitas dan kelayakan, jangan dijumlah dulu.

**3.2 Mueller, Melwani & Goncalo (2012), Psychological Science.** Bias implisit terhadap kreativitas muncul saat ada kebutuhan mengurangi ketidakpastian; mengganggu pengenalan ide kreatif.
Tautan: https://repository.upenn.edu/mgmt_papers/66
Implikasi: juri LLM yang diminta "berhati-hati/kritis" mungkin meniru bias ini. Instruksi eksplisit "cari ide paling berani" perlu dipasang.

**3.3 Berg (2016), Administrative Science Quarterly 61(3):433-468** (DOI 10.1177/0001839216642211). Studi 339 profesional sirkus: kreator lebih akurat memprediksi sukses ide orang lain dibanding manajer, tetapi tidak untuk ide sendiri; lab menunjuk pada peran berpikir divergen+konvergen.
Tautan: https://mackinstitute.wharton.upenn.edu/2016/balancing-on-the-creative-high-wire/ ; https://www.gsb.stanford.edu/faculty-research/publications/balancing-creative-high-wire-forecasting-success-novel-ideas
Implikasi: juri sebaiknya diberi peran "kreator menilai ide orang lain" (penulis/juri esai berpengalaman), bukan "manajer pemilih"; jangan biarkan generator menilai idenya sendiri.

**3.4 Consensual Assessment Technique (Amabile).** Reliabilitas antar-rater biasanya >.70 dan sering ~.90, naik dengan jumlah juri (sekitar 7-10 praktis); pakar lebih konsisten daripada non-pakar; kritik "scattered CAT" ada.
Tautan: https://www.rider.edu/sites/default/files/2024-05/baerkkaufmangentile.pdf ; https://knowledge.lancashire.ac.uk/id/eprint/28402/1/28402%20CsehJeffries_A%20scattered%20CAT%20A%20critical%20evaluation%20of%20the%20Consensual%20Assessment%20Technique%20for%20creativity%20research.pdf
Implikasi: konsistensi juri tinggi tidak membuktikan validitas (mereka bisa sama-sama bias). Hitung reliabilitas antar juri sebagai pemeriksaan kesehatan, bukan bukti kebenaran.

**3.5 Median/rata-rata menekan ide polarisasi?** Tidak ada sumber empiris langsung yang ditemukan di pencarian ini **[UNVERIFIED]**. Argumennya logis (agregasi rata-rata/median dari juri yang bias konservatif membuang ide "cinta atau benci"), konsisten dengan 3.1-3.2. Berg/Rietzschel mendukung arah bias, tetapi bukan klaim median itu sendiri.
Implikasi: tambahkan jalur seleksi berbasis kuantil atas/maks (mis. ide dengan skor orisinalitas tertinggi oleh SATU juri atau persentil 80) sebagai "jalur liar" ke final di samping median.

## 4. LLM sebagai juri

**4.1 Zheng dkk. (2023), MT-Bench/Chatbot Arena, arXiv 2306.05685.** Juri LLM kuat (GPT-4) sepakat dengan preferensi manusia >80%, setara antar-manusia; ada bias posisi, verbositas, dan self-enhancement, sebagian dapat dimitigasi. (Rincian bias dari ringkasan pihak ketiga, cek PDF sebelum mengutip angka.)
Tautan: https://arxiv.org/abs/2306.05685 ; https://arxiv.org/html/2306.05685v4
Implikasi: acak/tukar urutan kartu ide, netralkan panjang kartu, jalankan tiap pasangan dua arah.

**4.2 Panickssery, Bowman & Feng (2024), NeurIPS 2024, arXiv 2404.13076.** LLM mengenali tulisannya sendiri dan menyukainya; self-recognition berkorelasi linear dengan self-preference setelah fine-tuning.
Tautan: https://arxiv.org/abs/2404.13076v1 ; https://papers.nips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.html
Implikasi: juri sebaiknya dari model/versi berbeda dari generator (atau campur vendor), dan kartu ide dinormalisasi gayanya agar sulit dikenali.

**4.3 Organisciak dkk. (2023), Thinking Skills and Creativity 49:101356 (DOI 10.1016/j.tsc.2023.101356).** LLM yang di-fine-tune pada skor manusia untuk AUT mencapai korelasi hingga r=.81 dengan rater manusia; hanya jarak semantik lebih lemah.
Tautan: https://openscoring.du.edu/research
Implikasi: korelasi tinggi tercapai setelah fine-tuning dengan data manusia. Juri zero-shot belum tentu setara; catat bahwa untuk esai tidak ada data kalibrasi, jadi kalibrasi dengan ide juara nyata (pasaran).

**4.4 Pairwise vs pointwise.** CrEval (arXiv 2505.19236): evaluator kreativitas berpasangan dilatih pada label 30 juri manusia melampaui GPT-4o 18,7% dalam kesepakatan dengan manusia. Studi iklan menemukan korelasi lemah/tidak konsisten antara juri LLM dan manusia (Kendall tau ~0,50). Perbandingan langsung pairwise vs pointwise yang ketat tidak ditemukan; klaim "pairwise lebih konsisten" bersumber glosarium informal.
Tautan: https://arxiv.org/pdf/2505.19236 ; https://arxiv.org/pdf/2509.09702v1 ; https://aclanthology.org/anthology-files/pdf/emnlp/2025.emnlp-main.1009.pdf (EMNLP 2025, skor orisinalitas berbasis frekuensi; tidak dibaca rinci)
Implikasi: pakai pairwise untuk finalis (sudah ada di desain), pointwise hanya untuk penyaringan kasar; jangan klaim keunggulan pairwise sebagai fakta kuat.

**4.5 Elo/turnamen.** Tesis master (Kennesaw) memakai forced-choice + Elo; disagreement manusia membatasi ceiling terutama di ujung atas: https://digitalcommons.kennesaw.edu/masterstheses/100 (sumber lemah).
Implikasi: di ujung atas, juri berbeda pendapat; jangan terlalu percaya urutan 1 vs 2.

## 5. Perilaku juri di kompetisi nyata

**5.1 Bruine de Bruin (2005), Acta Psychologica 118(3):245-260, DOI 10.1016/j.actpsy.2004.08.005.** Di Eurovision dan figure skating, skor naik seiring urutan tampil (efek posisi serial), baik skor akhir maupun langkah-demi-langkah; penjelasan: kesan awal dibentuk satu per satu. Saran: acak urutan ronde pertama, balik di ronde kedua.
Tautan: https://research.tue.nl/en/publications/save-the-last-dance-for-me-unwanted-serial-position-effects-in-ju/ ; https://www.cbsnews.com/news/perform-last-finish-first
Implikasi: urutan kartu ke juri harus diacak per juri dan sebagian dibalik; berlaku juga untuk juri LLM (konteks panjang) dan juri esai manusia.

**5.2 Kelelahan juri/efek kesan pertama.** Tidak ada sumber yang saya temukan di sesi ini **[UNVERIFIED]**. Pakai mitigasi: batas jumlah esai/kartu per juri, rotasi urutan.

## Daftar sitasi yang tidak terverifikasi
- Kornish & Ulrich tentang duplikasi ide (hanya "Sow's Ear" 2014 terverifikasi, dan tidak membahas duplikasi).
- Rietzschel dkk. 2007 (J. Exp. Soc. Psych.) kuantitas-kualitas: hanya judul/bibliografi terlihat, temuan tidak.
- Bukti empiris bahwa median/rata-rata menekan ide polarisasi (tidak ada sumber langsung).
- Kelelahan juri dan efek kesan pertama selain Bruine de Bruin.
- Angka bias posisi/verbositas Zheng dkk. (dari ringkasan pihak ketiga).
- Makalah 2026 tentang keragaman ide lintas vendor (hanya entri RePEc dilihat, tidak dibuka).
- Studi iklan (tau ~0,50) dan CrEval: hanya dari ringkasan hasil pencarian.
