#!/usr/bin/env python3
"""Cek draf terhadap peta klaim: setiap angka di naskah harus ada di peta klaim, dan setiap
ID klaim yang dipakai naskah harus ada di peta dan sudah berstatus ✅.

Pakai:
    python tools/cek_klaim.py lomba/<nama>/draf/draf-v1.md --peta lomba/<nama>/riset/sumber.md [--peta lomba/<nama>/riset/dossier.md]

Cara menandai naskah: setelah kalimat yang memakai data, tulis ID klaimnya sebagai komentar HTML,
misalnya  "... naik menjadi 21,6% (Kemenkes, 2023). <!--K3-->"  atau  <!--K3, K4-->.
Komentar tidak ikut tercetak di DOCX dan tidak dihitung sebagai kata.

Peta klaim adalah tabel di riset/sumber.md (lihat templates/sumber.md) dengan kolom pertama ID (K1, K2, ...)
dan kolom terakhir Status (✅ / ⚠️ / ❌).

Angka yang dicek: persen (21,6%), rupiah (Rp1,2 juta), desimal (2,5), ribuan (1.200), dan tahun data
("pada 2023", "tahun 2021"). Tahun di dalam sitasi (Smith, 2020) tidak dicek di sini.
Alat ini tidak menilai apakah sumber mendukung kalimat; itu tugas auditor sitasi di tahap 5.
"""
import argparse
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):  # Windows: output yang di-pipe jatuh ke cp1252
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

POLA_ANGKA = [
    r"Rp\s?\d[\d.,]*(?:\s?(?:ribu|juta|miliar|triliun))?",
    r"\d+(?:[.,]\d+)?\s?(?:%|persen\b)",
    r"\b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b",
    r"\b\d+,\d+\b",
    r"\b(?:tahun|pada|sejak|hingga|sampai|per|periode)\s+((?:19|20)\d{2})\b",
]
POLA_ID = r"<!--\s*(K\d+(?:\s*,\s*K\d+)*)\s*-->"


def norm_angka(s):
    """Bentuk pembanding: '21,6%' == '21.6 %', 'Rp 1.200.000' == 'Rp1.200.000'."""
    s = s.lower().replace(" ", "").replace("persen", "%")
    awalan = "rp" if s.startswith("rp") else ""
    s = s[len(awalan):]
    m = re.match(r"([\d.,]+)(.*)", s)
    if not m:
        return awalan + s
    inti, akhiran = m.groups()
    if "." in inti and "," in inti:          # 1.200,5 (gaya Indonesia)
        inti = inti.replace(".", "").replace(",", ".")
    elif "," in inti:                        # 21,6
        inti = inti.replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", inti):  # 1.200.000
        inti = inti.replace(".", "")
    inti = inti.rstrip(".")
    return awalan + inti + akhiran


def angka_di(teks):
    hasil = []
    for pola in POLA_ANGKA:
        for m in re.finditer(pola, teks, flags=re.I):
            hasil.append(m.group(1) if m.groups() and m.group(1) else m.group(0))
    return hasil


def baca_peta(teks_peta):
    """{ID: status} dari baris tabel yang kolom pertamanya K<nomor>."""
    peta = {}
    for baris in teks_peta.splitlines():
        sel = [c.strip() for c in baris.strip().strip("|").split("|")]
        if baris.strip().startswith("|") and sel and re.fullmatch(r"K\d+", sel[0]):
            peta[sel[0]] = sel[-1]
    return peta


def isi_naskah(teks):
    """Buang Daftar Pustaka/Lampiran dan judul; sisakan isi + komentar ID."""
    teks = re.split(r"^##\s+(?:Daftar Pustaka|Referensi|Daftar Referensi|Lampiran)\s*:?\s*$", teks, flags=re.M | re.I)[0]
    return re.sub(r"^#.*$", "", teks, flags=re.M)


def periksa(naskah, teks_peta):
    peta = baca_peta(teks_peta)
    angka_peta = {norm_angka(x) for x in angka_di(teks_peta)}
    isi = isi_naskah(naskah)
    dipakai = {k.strip() for g in re.findall(POLA_ID, isi) for k in g.split(",")}
    tanpa_komentar = re.sub(r"<!--.*?-->", "", isi, flags=re.S)
    tanpa_sitasi = re.sub(r"\([^()]*\b(?:19|20)\d{2}[a-z]?\)", "", tanpa_komentar)
    angka_tanpa = []
    for kal in re.split(r"(?<=[.!?])\s+", tanpa_sitasi):
        for a in angka_di(kal):
            if norm_angka(a) not in angka_peta:
                angka_tanpa.append((a.strip(), " ".join(kal.split())[:90]))
    return {
        "id_tak_dikenal": sorted(dipakai - set(peta)),
        "id_belum_terverifikasi": sorted(k for k in dipakai & set(peta) if "✅" not in peta[k]),
        "angka_tanpa_klaim": angka_tanpa,
        "jumlah_id": len(dipakai),
        "jumlah_peta": len(peta),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown")
    ap.add_argument("--peta", action="append", required=True, help="file berisi tabel peta klaim (boleh diulang)")
    a = ap.parse_args()
    try:
        naskah = Path(a.markdown).read_text(encoding="utf-8-sig")
        peta = "\n".join(Path(p).read_text(encoding="utf-8-sig") for p in a.peta)
    except OSError as ex:
        sys.exit(f"Gagal membaca file: {ex}")
    h = periksa(naskah, peta)
    print("== CEK KLAIM ==")
    print(f"· ID klaim dipakai di naskah: {h['jumlah_id']} · baris di peta klaim: {h['jumlah_peta']}")
    masalah = []
    for k in h["id_tak_dikenal"]:
        masalah.append(f"ID {k} dipakai di naskah tapi tidak ada di peta klaim")
    for k in h["id_belum_terverifikasi"]:
        masalah.append(f"ID {k} belum berstatus ✅ di peta klaim (sumber belum dibuka/dibaca); jangan dikutip dulu")
    for angka, kal in h["angka_tanpa_klaim"]:
        masalah.append(f"Angka '{angka}' tidak ada di peta klaim: \"{kal}\" (tambahkan klaimnya, atau tandai [PERLU DATA])")
    if masalah:
        print(f"\n{len(masalah)} hal perlu dicek:")
        for m in masalah:
            print("  -", m)
    else:
        print("\nSemua angka dan ID klaim tercatat di peta klaim.")
    sys.exit(1 if masalah else 0)


if __name__ == "__main__":
    main()
