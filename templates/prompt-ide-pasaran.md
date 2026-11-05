# Ide Pasaran (Langkah 0 Arena Ide)

`ide/pasaran.md` adalah anti-referensi. Generator dilarang menghasilkan ide yang mirip, dan juri memberi penalti K1 untuk kemiripan. Isinya diambil dari tiga sumber, **berurutan**: data juara sungguhan, prediksi, dan jawaban chatbot.

## 1. Data sungguhan (utama)
Minta penulis (atau cari di web) **judul dan, kalau ada, abstrak karya juara/finalis 2–3 edisi sebelumnya** dari lomba yang sama, ditambah lomba sebidang di jenjang yang sama. Sumber yang biasa ada: pengumuman pemenang di Instagram/web panitia, buku kumpulan esai, berita kampus.

Tulis di bagian atas `ide/pasaran.md`:
```
## Juara/finalis sungguhan
| Lomba & tahun | Judul | Inti ide (≤20 kata) | Sumber (link) |
```
Daftar ini berfungsi ganda:
- **Batas bawah kejutan**: ide yang hanya setara juara tahun lalu belum cukup mengejutkan.
- **Jangkar juri**: juri ditanya, "apakah ide ini lebih tajam dari juara tahun lalu?"

Jangan mengarang judul juara. Kalau tidak ada data yang bisa diverifikasi, tulis "tidak ditemukan" dan lanjut ke bagian 2.

**Kartu jangkar.** Kalau ditemukan ≥3 juara sungguhan, sisihkan 1–2 di antaranya (pilih yang abstraknya paling jelas). Tulis keduanya di `ide/jangkar.md`, bukan di `pasaran.md`, karena juara itu akan diselipkan diam-diam sebagai kartu `X01`/`X02` di loop 1 untuk menguji juri (`workflow/01-ide-dan-tesis.md` § Kartu jangkar). Kalau juara yang ditemukan kurang dari 3, semuanya masuk ke `pasaran.md` dan kartu jangkar dilewati.

## 2. Prediksi (cadangan, selalu diberi label)
Jalankan prompt di bawah di subagent tanpa konteks (agen `juri-ide`). Tulis hasilnya di bawah judul `## Prediksi (bukan data)`, dan beri tanda "(prediksi)" di setiap baris supaya juri tahu daftar ini tebakan model.

---

Kamu adalah panitia berpengalaman yang sudah membaca ribuan esai lomba di Indonesia.

Lomba: [nama lomba] · Jenjang peserta: [jenjang] · Tema: [tema]
Subtema:
[daftar subtema]

Tugas:
1. Untuk **setiap subtema**, tuliskan **3–5 ide yang paling mungkin ditulis oleh kebanyakan peserta**, yaitu ide yang pertama terpikir, paling sering muncul di internet, atau paling "aman".
2. Perkirakan urutan subtema dari yang **paling banyak** sampai **paling sedikit** dipilih peserta, beserta alasan singkatnya.

Format per ide, satu baris: `subtema | ringkasan ide (≤20 kata) | kenapa ide ini pasaran`

Jangan menilai bagus atau buruk. Tugasmu hanya memetakan apa yang umum.

---

## 3. Jawaban chatbot (selalu dijalankan, diberi label)
Banyak peserta lain memakai ChatGPT, Gemini, atau Claude untuk mencari ide, dan AI membuat hasil kolektif makin seragam. Jadi ide yang paling mungkin muncul di meja juri adalah **jawaban pertama chatbot untuk prompt polos**. Jalankan prompt di bawah apa adanya di subagent baru (sebaiknya model kecil, misalnya `haiku`), tanpa bekal dan tanpa daftar pasaran. Kalau penulis mau, tempel prompt yang sama ke ChatGPT/Gemini dan tambahkan jawabannya. Tulis hasilnya di bawah judul `## Jawaban chatbot (bukan data)`, dengan tanda "(chatbot)" dan nama modelnya di setiap baris.

---

Saya mau ikut lomba esai [nama lomba] untuk [jenjang] dengan tema "[tema]". Subtemanya: [daftar subtema]. Beri saya 10 ide esai yang bagus dan bisa menang, masing-masing dengan judul dan penjelasan singkat.
