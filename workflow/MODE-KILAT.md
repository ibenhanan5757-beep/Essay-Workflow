# Mode Kilat (bukan default)

Jalur yang dipangkas untuk tenggat **≤ 5 hari**. Jalur penuh (tahap 0–6 apa adanya) tetap default karena menghasilkan ide dan naskah yang lebih kuat, terutama Arena Ide 3 loop. Mode ini hanya dipakai kalau penulis memilihnya setelah melihat garis waktu di tahap 0. Catat di `<L>/STATUS.md`: `Mode: Kilat (alasan: tenggat <tanggal>, sisa <n> hari)`.

**Yang tidak dipangkas sama sekali**: matriks kepatuhan tahap 0, aturan sumber dan peta klaim tahap 2, auditor sitasi, `cek_klaim.py`, `cek-pustaka`, `cek_naskah.py`, dan cek akhir tahap 6. Esai yang cepat tapi memuat sumber palsu atau melanggar format lebih buruk daripada tidak dikirim.

| Tahap | Jalur penuh | Mode Kilat |
|---|---|---|
| 0 | lengkap | lengkap (tidak dipangkas) |
| 1 Arena Ide | rumusan peluang, 3 loop × 12 ide, 3 juri buta per loop, kolam + dedup + kartu liar, cek "sudah ada?", panel final, evolusi, adu Top 4 pakai paket esai | **3–4 rumusan peluang singkat** (tanpa tambang literatur) → **1 loop generator** (buat 25–30 ide satu baris → pilih 12 paling berbeda, kuota subtema loop 1, lensa A + B digabung) → **1 juri** lewat agen `juri-ide` dengan model berbeda dari generator, pakai rubrik ide lengkap (gerbang G1–G4 tetap) → `arena.py mirip` (dedup) → `arena.py rekap --top 5` (Top 5 + kartu liar dari `bela`) → **cek "sudah ada?"** (1 pencarian web per ide; aturan vonis sama dengan jalur penuh: *sama* hanya kalau bisa menyebut karya spesifik) → **penulis memilih** dari Top 5. Tanpa panel final, evolusi, dan adu. Bukti pendukung ≥2 tetap wajib untuk ide yang dipilih. |
| 2 Riset | 3–5 pertanyaan bukti | 2–3 pertanyaan bukti, peta klaim tetap wajib |
| 3 Kerangka | lengkap | kerangka ringkas: struktur yang dipilih + tesis + pohon argumen + **cek argumen pasaran** (1 panggilan) + 1 kontra-argumen; debat kerangka dilewati (devil's advocate tahap 5 tetap jalan); checkpoint digabung dengan tahap 4 |
| 4 Draf | lengkap | lengkap (contoh gaya cukup 1 cuplikan; putaran umpan balik visual tetap) |
| 5 Loop juri | maks 3 putaran: juri rubrik + devil's advocate + konfirmasi + auditor sitasi + berpasangan | **1 putaran**: cek mesin + auditor sitasi + 1 juri rubrik resmi + devil's advocate (temuan Kritis/Mayor tetap dikonfirmasi). Putaran kedua hanya kalau masih ada temuan Kritis. |
| 6 Revisi & build | lengkap | lengkap (cek akhir tidak dipangkas) |
| 7 Visual | opsional | hanya yang diwajibkan guidebook |

Perkiraan: ±2–4 jam kerja Claude, ±6–8 panggilan subagent (bandingkan ±35 di jalur penuh).

Saat menyajikan hasil Arena Ide Mode Kilat, sebutkan ke penulis bahwa ide dipilih dari satu putaran dan satu juri, jadi keyakinannya lebih rendah dari jalur penuh.
