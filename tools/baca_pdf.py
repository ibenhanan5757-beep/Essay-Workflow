#!/usr/bin/env python3
"""Ekstrak teks guidebook PDF per halaman, supaya aturan bisa dikutip dengan nomor halaman.

Pakai:
    python tools/baca_pdf.py lomba/<nama>/guidebook.pdf                  # cetak ke layar
    python tools/baca_pdf.py lomba/<nama>/guidebook.pdf --out lomba/<nama>/guidebook.txt
    python tools/baca_pdf.py lomba/<nama>/guidebook.pdf --halaman 3-5

Mesin yang dicoba berurutan: pypdf (`pip install pypdf`), pdfplumber, lalu perintah `pdftotext`.
PDF hasil scan (gambar) tidak punya teks: alat ini akan memberi tahu, dan halaman itu perlu dibaca
langsung oleh model yang bisa melihat gambar, atau di-OCR dulu.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def pakai_pypdf(jalur):
    from pypdf import PdfReader
    return [(h.extract_text() or "") for h in PdfReader(str(jalur)).pages]


def pakai_pdfplumber(jalur):
    import pdfplumber
    with pdfplumber.open(str(jalur)) as pdf:
        return [(h.extract_text() or "") for h in pdf.pages]


def pakai_pdftotext(jalur):
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext tidak ada")
    teks = subprocess.run(["pdftotext", "-layout", str(jalur), "-"], capture_output=True,
                          text=True, encoding="utf-8", errors="replace", check=True).stdout
    return teks.split("\f")[:-1] if teks.endswith("\f") else teks.split("\f")


def ekstrak(jalur):
    gagal = []
    for nama, fungsi in [("pypdf", pakai_pypdf), ("pdfplumber", pakai_pdfplumber), ("pdftotext", pakai_pdftotext)]:
        try:
            return nama, fungsi(jalur)
        except Exception as e:  # mesin tidak terpasang atau gagal membaca
            gagal.append(f"{nama}: {e.__class__.__name__}")
    sys.exit("Tidak ada mesin PDF yang berhasil (" + "; ".join(gagal) + "). Jalankan: pip install pypdf")


def rentang(teks, total):
    a, _, b = teks.partition("-")
    return max(1, int(a)), min(total, int(b or a))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--out", help="simpan hasil ke file teks")
    ap.add_argument("--halaman", help="misalnya 3 atau 3-5")
    a = ap.parse_args()

    mesin, halaman = ekstrak(Path(a.pdf))
    awal, akhir = rentang(a.halaman, len(halaman)) if a.halaman else (1, len(halaman))
    bagian, kosong = [], []
    for i in range(awal, akhir + 1):
        isi = halaman[i - 1].strip()
        if len(isi) < 20:
            kosong.append(i)
        bagian.append(f"=== Halaman {i} ===\n{isi}\n")
    hasil = "\n".join(bagian)

    if a.out:
        Path(a.out).write_text(hasil, encoding="utf-8")
        print(f"Tersimpan: {a.out} ({akhir - awal + 1} halaman, mesin {mesin})")
    else:
        print(hasil)
    if kosong:
        print(f"\nPERINGATAN: halaman {', '.join(map(str, kosong))} hampir tanpa teks (mungkin gambar/scan). "
              "Baca halaman itu langsung sebagai gambar, jangan ditebak.", file=sys.stderr)


if __name__ == "__main__":
    main()
