# Status: [nama lomba]

- **Tenggat:** [tanggal, jam, zona waktu] · kirim ulang boleh? [ya/tidak] · **pengumuman:** [tanggal]
- **Versi workflow:** [tanggal terakhir di catatan/riwayat-workflow.md] · pelajaran aktif yang relevan: [ID dari catatan/buku-pelajaran.md]
- **Aturan AI di guidebook:** [kutipan + halaman; atau "tidak disebut"] · log prompt wajib? [ya/tidak]
- **Mode kerja:** jalan terus sampai final ide (default) / berhenti di setiap tahap · jalur: penuh / Kilat
- **Subtema & tesis:**
- **Judul:**

## Progres
- [ ] 0. Guidebook dibedah (aturan.md, profil.json)
- [ ] 1. Arena Ide selesai (ide/final.md) & tesis disetujui
- [ ] 2. Sumber terkumpul & terverifikasi (riset/)
- [ ] 3. Kerangka disetujui
- [ ] 4. Draf v1 selesai
- [ ] 5. Loop juri selesai (tidak ada temuan Kritis/Mayor)
- [ ] 6. Final + file kirim siap (kirim/)
- [ ] 7. Visual/lampiran/presentasi (kalau diminta)
- [ ] 8a. Retro proses (evaluasi.md, hasil.json) — segera setelah kirim
- [ ] 8b. Retro hasil + bank juara — setelah pengumuman ([tanggal pengumuman])
- [ ] 8c. Pelajaran masuk catatan/buku-pelajaran.md; usulan perubahan diputuskan penulis

## Serah terima
Diperbarui di setiap checkpoint. Utas baru mulai dari sini (CLAUDE.md § Satu utas pendek per tahap).
- **Tahap selesai → berikutnya:**
- **Utas berikutnya: model … · effort …** (dari `workflow/MODEL-DAN-EFFORT.md`)
- **Baca dulu (maks. 5 berkas):** `STATUS.md`, `aturan.md`, …
- **Tidak perlu dibaca ulang:** `guidebook.pdf`/`guidebook.txt` (pakai `aturan.md`), `ide/loop-*.md` dan `ide/juri/` (pakai `ide/kolam.md` atau `ide/final.md`), `riset/teks/*` (cari dengan Grep)
- **Keputusan penulis yang mengikat:**
- **Pertanyaan terbuka:**

## Log kuota
Satu baris per checkpoint, dari `get_usage`. Dipakai di tahap 8a untuk menemukan tahap termahal.

| Tanggal, jam | Tahap / utas | Limit 5 jam % | Mingguan % | Konteks utas (token) | Subagent di utas ini (jumlah × model) |
|---|---|---|---|---|---|

## Catatan keputusan
(tanggal: keputusan)

## Log prompt (kalau lomba meminta)
