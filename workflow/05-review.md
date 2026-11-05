# Tahap 5 — Review (Loop Juri)

Sumber: `skills/esai/advanced-evaluation/` (desain juri LLM), `skills/esai/academic-research-skills/devils_advocate_reviewer_agent.md`, `claim_strength_ladder.md`, `logical_fallacies.md`, dan konsep loop juri dari "Master SOP Juara" yang **dikoreksi** (lihat `catatan/kritik-sop-juara.md` § 4).

## Prinsip desain loop
- **Rubrik resmi lomba adalah skor utama.** Juri sungguhan mengisi lembar nilai resmi, jadi skor utama dan syarat berhenti memakai kriteria serta bobot dari `<L>/aturan.md` § Rubrik penilaian. Rubrik sendiri (`templates/rubrik-esai.md`) dipakai sebagai lapis kedua untuk mencari perbaikan yang membuat esai menonjol. Kalau guidebook tidak mengumumkan rubrik, pakai rubrik dugaan di `aturan.md` dengan bobot sama rata dan sebutkan bahwa itu dugaan.
- **Setiap juri di konteks baru dan dipanggil terpisah.** Skor, devil's advocate, auditor sitasi, dan perbandingan berpasangan adalah panggilan subagent yang berbeda. Masing-masing hanya menerima bahan yang disebut di promptnya, tanpa riwayat proses menulis. Kalau tersedia, pakai agen proyek `.claude/agents/juri-esai.md` (tanpa akses file), yang menerima semua bahan lewat prompt. Model yang baru saja menulis cenderung membela tulisannya sendiri. Agen `juri-esai` dan `auditor-sitasi` memakai Sonnet secara bawaan (`model: sonnet`), sehingga juri tidak ikut Opus walaupun draf ditulis di utas Opus (PL25). Auditor sitasi jangan diturunkan ke Haiku, karena hasilnya menentukan temuan Kritis.
- **Skor wajib disertai bukti kutipan.** Skor tanpa kutipan dianggap tidak sah.
- **Temuan Kritis/Mayor harus dikonfirmasi.** Devil's advocate memang diperintah mencari kelemahan, jadi ia hampir selalu menemukan sesuatu. Temuan Kritis/Mayor baru dihitung kalau (1) menyebut lokasi berupa kutipan persis dari naskah, dan (2) dinyatakan "sah" oleh juri konfirmasi di konteks baru (`templates/prompt-juri.md` § D). Temuan yang tidak lolos konfirmasi diturunkan jadi Minor.
- **Berhenti berdasarkan temuan, bukan target skor tinggi.** Loop selesai kalau ketiganya terpenuhi: tidak ada kriteria rubrik resmi bernilai < 7, tidak ada temuan Kritis/Mayor yang terkonfirmasi, dan auditor sitasi tidak memberi "tidak mendukung" untuk satu klaim pun. Maksimal 3 putaran. Kalau setelah 3 putaran syarat belum terpenuhi, laporkan sisanya ke penulis, jangan putar terus. **Putaran ke-4 dan seterusnya hanya dijalankan kalau penulis memintanya** setelah melihat laporan itu, dan permintaannya dicatat di `STATUS.md` (Pharfest berjalan ±5 putaran).
- **Skor mendatar** (PL17). Kalau satu putaran revisi tidak menaikkan skor rubrik resmi berbobot minimal 0,2, dan penahannya ada di isi (bukti, data lapangan, kelayakan), bukan di bahasa, jangan jalankan putaran lagi hanya untuk memoles bahasa. Laporkan penahan isi itu ke penulis dan minta bahan baru. Temuan Kritis/Mayor dan hasil "tidak mendukung" dari auditor tetap wajib dibereskan sebelum cek akhir tahap 6.
- **Bandingkan berpasangan.** Setelah revisi, juri membandingkan versi lama dan baru per kriteria. Perbandingan dijalankan dua kali dengan posisi versi ditukar. Kriteria yang hasilnya tidak sepakat dianggap setara. Kalau versi baru kalah secara konsisten di suatu kriteria, perubahan yang menyentuh kriteria itu dibatalkan. Karena itu setiap revisi dicatat di `review-vN.md` § Log perubahan (perubahan → kriteria yang disasar).
- **Cek mesin dulu, juri belakangan.** Jalankan alat sebelum memanggil juri supaya juri fokus ke isi.

## Langkah per putaran
1. **Cek mesin**, lalu perbaiki semua temuannya:
   ```
   python tools/cek_naskah.py <L>/draf/draf-vN.md --profil <L> --nama "<nama>" --nama "<sekolah>" --sumber <L>/riset/teks
   python tools/cek_klaim.py <L>/draf/draf-vN.md --peta <L>/riset/sumber.md
   python skills/esai/naskah-id/scripts/periksa.py <L>/draf/draf-vN.md
   python tools/cari_sumber.py cek-pustaka <L>/draf/draf-vN.md
   ```
2. **Auditor sitasi** (`templates/prompt-auditor-sitasi.md`). Agen utama menyusun pasangan *(kalimat naskah, kutipan verbatim dari peta klaim)* untuk setiap kalimat bertanda `<!--Kn-->`. Subagent baru hanya menerima pasangan itu, tanpa naskah utuh dan tanpa tesis, lalu menjawab per pasangan: **mendukung / sebagian / tidak mendukung / tidak bisa dinilai**, beserta alasannya. Hasil "tidak mendukung" = temuan Kritis. Hasil "sebagian" = lemahkan kalimatnya sampai sesuai kutipan.
3. **Juri rubrik** (`templates/prompt-juri.md` § A): skor per kriteria **rubrik resmi** dengan bobot resmi, lalu skor lapis kedua dari `templates/rubrik-esai.md`. Persona juri dari `<L>/aturan.md`. Kalau ada beberapa sudut pandang juri (akademisi vs praktisi), jalankan terpisah.
4. **Devil's advocate** (§ B), panggilan terpisah: hanya mencari kelemahan, setiap temuan wajib dengan kutipan lokasi. Bagian pertamanya adalah **serangan tunggal**: satu memo penolakan ≤200 kata dari satu sumbu paling mematikan (diadaptasi dari skill `kill-argument` ARIS). Serangan tunggal memaksa juri menggali kelemahan terdalam, bukan menyebar banyak keluhan kecil.
5. **Konfirmasi** (§ D): setiap temuan Kritis/Mayor dari langkah 3–4 dan memo serangan tunggal dikirim ke subagent baru bersama naskah. Yang dinyatakan tidak sah diturunkan jadi Minor. Serangan tunggal dipecah menjadi 3–7 poin, lalu setiap poin diperiksa kutipannya dan diberi status. Keputusan dihitung agen utama dengan aturan ini, bukan oleh juri:
   - **belum terjawab**: tingkatnya tetap (poin Kritis/Mayor dihitung sebagai temuan Kritis/Mayor terkonfirmasi)
   - **sebagian**: turun satu tingkat
   - **sudah dijawab naskah** atau kutipannya tidak ada di naskah: bukan temuan
6. Tulis hasil gabungan ke `<L>/draf/review-vN.md` (template `templates/review.md`), termasuk keputusan berhenti/lanjut menurut syarat di atas.
7. Revisi (tahap 6). Putaran berikutnya: cek apakah temuan sudah ditangani, lalu perbandingan berpasangan (§ C). Setiap putaran (penilaian lalu revisi) dikerjakan di utas sendiri. Putaran berikutnya dimulai dari `review-vN.md` dan draf terbaru, bukan dari riwayat putaran sebelumnya.

## Kacamata yang harus tercakup
1. **Rubrik resmi** (skor utama) dan **rubrik sendiri** (`templates/rubrik-esai.md`, lapis kedua): skor per kriteria + kutipan bukti + satu perbaikan paling berdampak.
2. **Devil's advocate**: logika terlemah, keberatan terkuat yang belum dijawab, kelayakan solusi (biaya, pelaksana, waktu), dan sesat pikir (dikotomi palsu, generalisasi tergesa-gesa, korelasi dianggap sebab, *appeal to popularity*, *slippery slope*, *strawman*).
3. **Akurasi bidang**: istilah, mekanisme, dan regulasi benar menurut ahli bidang juri.
4. **Tangga kekuatan klaim**:
   ```
   mungkin menunjukkan < berkaitan dengan < memprediksi < berkontribusi pada < memengaruhi < menyebabkan/membuktikan
   ```
   Data korelasi atau survei tidak boleh ditulis "menyebabkan".
5. **Integritas sumber**: dikerjakan auditor sitasi (kutipan vs kalimat) dan `cek_klaim.py` (angka di teks ada di peta klaim), bukan oleh juri rubrik yang tidak melihat sumber.
6. **Bahasa**: EYD V, kalimat efektif, anti-slop (`04-menulis-draf.md`).

## Tingkat temuan (berdasarkan dampak, bukan nada)
- **Kritis:** tesis runtuh, fakta salah, sumber palsu/ditarik, kalimat tidak didukung sumbernya, atau melanggar aturan lomba
- **Mayor:** melemahkan argumen utama, atau membuat satu kriteria rubrik resmi turun di bawah 7; perlu tulis ulang bagian
- **Minor:** kejelasan dan bahasa
