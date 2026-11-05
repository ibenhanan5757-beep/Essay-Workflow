# Mulai di Windows

Panduan sekali pasang untuk menjalankan alat di `tools/` dari laptop Windows. Kalau Claude yang menjalankan alat, Claude memakai langkah yang sama. Kamu cukup memastikan Python sudah terpasang.

## 1. Python
1. Unduh Python 3.12 dari https://www.python.org/downloads/windows/ lalu jalankan installer.
2. Di layar pertama installer, **centang "Add python.exe to PATH"**, lalu klik *Install Now*.
3. Buka PowerShell baru (tombol Windows → ketik `PowerShell`), lalu cek:
   ```powershell
   python --version
   ```
   Kalau muncul `Python 3.x.x`, Python siap. Kalau Microsoft Store malah terbuka atau muncul "not recognized", coba `py --version`. Kalau `py` berhasil, ganti `python` dengan `py` di semua perintah, atau ulangi instalasi dengan kotak PATH dicentang.

## 2. Paket tambahan
```powershell
pip install python-docx pypdf matplotlib python-pptx
```
- `python-docx`: untuk `build_docx.py` (Markdown → DOCX).
- `pypdf`: untuk `baca_pdf.py` (teks guidebook per halaman).
- Kalau `pip` tidak dikenal: `python -m pip install python-docx pypdf matplotlib python-pptx`.

Alat lain (`cari_sumber.py`, `cek_naskah.py`, `cek_klaim.py`, `arena.py`, `tes_alat.py`) tidak butuh paket tambahan.

## 3. PDF (pilih satu)
- **LibreOffice** (gratis): pasang dari https://www.libreoffice.org/download/. `build_docx.py --pdf` otomatis mencari `C:\Program Files\LibreOffice\program\soffice.exe`, jadi tidak perlu diatur PATH-nya.
- **Microsoft Word**: kalau Word sudah terpasang, jalankan `pip install docx2pdf`.
- Tanpa keduanya: buka DOCX hasil build di Word atau Google Docs, lalu simpan sebagai PDF. Periksa ulang margin dan nomor halaman.

## 4. Menjalankan alat
Buka PowerShell **di folder workflow** (folder yang berisi `CLAUDE.md`): di File Explorer, buka folder itu, klik kolom alamat, ketik `powershell`, lalu Enter. Uji sekali:
```powershell
python tools/tes_alat.py
```
Hasil yang benar diakhiri `OK` (beberapa tes jaringan memang `skipped`). Kalau ada `FAILED`, kirim keluarannya ke Claude.

Path yang mengandung spasi harus diapit tanda kutip: `"lomba/nama lomba/draf/final.md"`. Supaya aman, nama folder lomba dibuat tanpa spasi (`lomba/olimpiade-esai-2027`).

## 5. Huruf aneh (encoding)
Semua alat memaksa keluaran UTF-8, jadi ✅ ⚠️ ❌ tidak membuat alat crash. Kalau PowerShell lama menampilkan simbol sebagai `?` atau kotak, tampilannya saja yang rusak, hasilnya tetap benar. Untuk memperbaiki tampilan:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```
Atau pakai **Windows Terminal** (bawaan Windows 11).

## 6. Email & kunci API (opsional, supaya pencarian jurnal jarang dibatasi)
```powershell
setx ESAI_EMAIL "emailkamu@contoh.com"
setx OPENALEX_API_KEY "kunci-dari-openalex.org/settings/api"
setx SEMANTIC_SCHOLAR_API_KEY "kunci-dari-semanticscholar.org"
```
Tutup PowerShell, lalu buka lagi supaya nilainya terbaca. Sesi Claude yang sedang terbuka juga belum melihatnya; mulai sesi baru.

Di mana kunci ini disimpan:
- Di **akun pengguna Windows**, bukan di folder proyek dan bukan di akun Claude. Jadi semua aplikasi di laptop ini (Claude akun mana pun, Antigravity, terminal) otomatis memakainya.
- **Sengaja tidak ditulis di folder proyek**, supaya tidak ikut terunggah ke GitHub atau terbawa saat folder dibagikan. Simpan salinan kuncinya di pengelola kata sandi.
- Pindah ke **laptop lain**: jalankan `setx` di atas sekali lagi di laptop itu.
- Cek apakah sudah terpasang (tanpa menampilkan kuncinya): `[Environment]::GetEnvironmentVariable("OPENALEX_API_KEY","User").Length` menampilkan panjangnya, 0 berarti kosong.
- Menghapus: `[Environment]::SetEnvironmentVariable("OPENALEX_API_KEY", $null, "User")`.

## Kalau macet
| Gejala | Coba |
|---|---|
| `python` tidak dikenal | pakai `py`, atau pasang ulang Python dengan "Add to PATH" |
| `No module named docx` | `python -m pip install python-docx` |
| `matplotlib belum terpasang` | `python -m pip install matplotlib` (untuk `buat_visual.py`) |
| `python-pptx belum terpasang` | `python -m pip install python-pptx` (untuk `cek_pptx.py`, hanya kalau membuat PPT) |
| `Tidak bisa menghubungi database` | cek internet. Kalau sering terkena 429, set email/kunci (langkah 6) lalu tunggu beberapa menit |
| `Build ditolak: masih ada penanda` | naskah masih memuat `[PERLU ...]`/`TODO`. Bereskan dulu (lihat `workflow/02-riset.md`) |
| `Tidak bisa menulis ... .docx` | file DOCX masih terbuka di Word. Tutup lalu ulangi |
| PDF tidak dibuat | pasang LibreOffice atau `pip install docx2pdf` (langkah 3) |
| Sesi Claude terputus di tengah tahap | buka lagi folder ini dan bilang "lanjutkan lomba [nama]". Claude membaca `lomba/<nama>/STATUS.md` |
