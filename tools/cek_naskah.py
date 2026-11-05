#!/usr/bin/env python3
"""Cek kepatuhan dan kualitas dasar naskah esai (Markdown) sebelum dikirim.

Pakai:
    python tools/cek_naskah.py lomba/<nama>/draf/final.md --profil lomba/<nama> [--nama "Nama Peserta" --nama "Nama Sekolah"] [--sumber lomba/<nama>/riset/teks]

Yang dicek (semuanya deterministik, tanpa AI):
  1. Jumlah kata isi (tanpa judul, Daftar Pustaka, dan Lampiran) vs batas profil
  2. Penanda yang belum beres: [PERLU SUMBER], [PERLU DATA: ...], [PERLU RUJUKAN: ...], TODO, XXX, ??
  3. Nama peserta/sekolah muncul di naskah (lomba penilaian buta), dicocokkan per kata utuh
  4. Sitasi (Penulis, Tahun) atau [n] di teks yang tidak ada di Daftar Pustaka, dan sebaliknya
  5. Frasa klise khas AI (daftar di tools/frasa_slop.txt), dicocokkan per kata utuh
  6. Gambar/tabel di luar Lampiran bila profil melarang
  7. Paragraf sangat panjang dan kalimat sangat panjang
  8. (--sumber) Kemiripan: rangkaian >=8 kata yang sama persis dengan teks sumber
     (.md/.txt di folder sumber; dossier.md, sumber.md, peta-klaim.md, dan README.md dilewati
     karena itu tulisan sendiri, bukan teks sumber)
Hasil adalah laporan; keputusan tetap di tangan penulis/reviewer.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

for _s in (sys.stdout, sys.stderr):  # Windows: output yang di-pipe jatuh ke cp1252
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent

# Semua bentuk penanda "belum ada sumber/data" yang dipakai workflow dan skill naskah-id.
POLA_PERLU = r"\[PERLU[^\]]*\]"
TAHUN = r"(?:19|20)\d{2}[a-z]?"
BUKAN_SUMBER = {"dossier.md", "sumber.md", "peta-klaim.md", "readme.md"}


def baca(path):
    return Path(path).read_text(encoding="utf-8-sig")


def pecah_bagian(teks, profil):
    pustaka_judul = [s.lower() for s in profil.get("judul_bagian_pustaka") or ["daftar pustaka", "referensi"]]
    lampiran_judul = [s.lower() for s in profil.get("judul_bagian_lampiran") or ["lampiran"]]
    bagian = {"isi": [], "pustaka": [], "lampiran": []}
    mode = "isi"
    for baris in teks.splitlines():
        m = re.match(r"^##\s+(.*)", baris)
        if m:
            judul = m.group(1).strip().rstrip(":").lower()
            if judul in pustaka_judul:
                mode = "pustaka"
                continue
            if judul in lampiran_judul:
                mode = "lampiran"
                continue
        bagian[mode].append(baris)
    return {k: "\n".join(v) for k, v in bagian.items()}


def hitung_kata(teks):
    teks = re.sub(r"^#\s+.*$", "", teks, flags=re.M)  # judul
    teks = re.sub(r"^#{2,}\s+", "", teks, flags=re.M)
    teks = re.sub(r"[*_`>#|]", " ", teks)
    # "1.000" dan "2,5" dihitung satu kata
    return len(re.findall(r"[0-9A-Za-zÀ-ÿ]+(?:[-'.,][0-9A-Za-zÀ-ÿ]+)*", teks))


def kunci_nama(s):
    """Nama penulis/lembaga dalam bentuk pembanding: huruf kecil, tanpa aksen dan tanda baca."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split())


def penulis_pertama(teks_penulis):
    """'Smith dkk.' / 'Smith & Lee' / 'Santoso dan Wibowo' / 'World Health Organization' -> nama pertama."""
    t = re.sub(r"\[[^\]]*\]", "", teks_penulis)  # 'World Health Organization [WHO]'
    t = re.sub(r"\b(dkk|et al)\.?", "", t)
    t = re.split(r"\s+(?:&|dan|and)\s+|,", t)[0]
    return kunci_nama(t)


def sitasi_teks(isi):
    """Set (nama, tahun) dari sitasi di teks. Nama berupa tuple kandidat (dari yang terpanjang),
    karena sitasi naratif bisa didahului kata lain ('Menurut World Health Organization (2021)')."""
    hasil = set()
    # Dalam kurung: (Kemenkes, 2023) / (WHO, 2021; BPOM, 2022) / (Smith dkk., 2020) / (Smith, 2020, 2021)
    # Wajib ada koma sebelum tahun, jadi (Maret 2024) dan (Rp 1500) diabaikan.
    for grup in re.findall(r"\(([^()]*\d{4}[^()]*)\)", isi):
        for item in grup.split(";"):
            m = re.match(rf"\s*(?:lihat\s+|misalnya\s+)?([^,\d][^,]*?)\s*,\s*({TAHUN}(?:\s*,\s*{TAHUN})*)\b", item)
            if not m:
                continue
            nama = penulis_pertama(m.group(1))
            if nama:
                for th in re.findall(TAHUN, m.group(2)):
                    hasil.add(((nama,), th))
    # Naratif: Smith (2020) / Santoso dan Wibowo (2021) / Smith dkk. (2020) / World Health Organization (2021)
    pola = (r"((?:[A-Z][\w\-’']*\s+){0,5}[A-Z][\w\-’']*)"
            r"(?:\s+(?:dkk\.|et al\.)|\s+(?:&|dan)\s+[A-Z][\w\-]+)?\s+\(((?:19|20)\d{2}[a-z]?)\)")
    for nama, th in re.findall(pola, isi):
        kata = nama.split()
        kandidat = tuple(kunci_nama(" ".join(kata[i:])) for i in range(len(kata)))
        hasil.add((kandidat, th))
    return hasil


def entri_pustaka(pustaka):
    """Daftar (kunci_nama_set, tahun, teks) per entri. Kunci berisi nama keluarga penulis pertama,
    atau nama lembaga lengkap + singkatannya ('World Health Organization [WHO]')."""
    hasil = []
    for baris in pustaka.splitlines():
        b = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|\[\d+\]\s*)", "", baris).strip()
        th = re.search(rf"\(({TAHUN})", b) or re.search(rf"\b({TAHUN})\b", b)
        if not b or not th:
            continue
        kunci = set()
        orang = re.match(r"^([^,(\[]+?),\s*[A-Z]\.", b)
        if orang:
            kunci.add(kunci_nama(orang.group(1)))
        else:
            lem = re.match(r"^(.+?)\s*(?:\[([^\]]+)\])?\s*\.?\s*\(", b)
            if lem:
                kunci.add(kunci_nama(lem.group(1)))
                if lem.group(2):
                    kunci.add(kunci_nama(lem.group(2)))
        kunci.discard("")
        if kunci:
            hasil.append((kunci, th.group(1), b))
    return hasil


def cocokkan_sitasi(st, ep):
    """Kembalikan (sitasi tanpa entri, entri tanpa sitasi)."""
    dipakai = set()
    yatim = []
    for kandidat, th in st:
        cocok = None
        for j, (kunci, th_e, _) in enumerate(ep):
            if th_e == th and any(k in kunci for k in kandidat):
                cocok = j
                break
        if cocok is None:
            yatim.append((kandidat[0], th))
        else:
            dipakai.add(cocok)
    tak_disitasi = [(sorted(ep[j][0])[0], ep[j][1]) for j in range(len(ep)) if j not in dipakai]
    return sorted(set(yatim)), tak_disitasi


def ada_kata(kata, teks):
    """Cocokkan kata/frasa utuh (tidak di tengah kata lain), abaikan huruf besar-kecil."""
    return re.findall(r"(?<!\w)" + re.escape(kata) + r"(?!\w)", teks, flags=re.I)


def kata_kecil(teks):
    return re.findall(r"[0-9a-zà-ÿ]+", teks.lower())


def cek_kemiripan(isi, jalur_sumber, n=8):
    """Cari rangkaian >= n kata di isi yang sama persis dengan salah satu file sumber."""
    berkas = []
    for j in jalur_sumber:
        p = Path(j)
        if p.is_dir() and (p / "teks").is_dir():
            p = p / "teks"  # <L>/riset -> <L>/riset/teks (teks sumber asli)
        berkas += sorted(x for x in (p.rglob("*") if p.is_dir() else [p])
                         if x.suffix.lower() in (".md", ".txt") and x.name.lower() not in BUKAN_SUMBER)
    indeks = {}
    for b in berkas:
        k = kata_kecil(b.read_text(encoding="utf-8-sig", errors="ignore"))
        for i in range(len(k) - n + 1):
            indeks.setdefault(tuple(k[i:i + n]), b.name)
    k = kata_kecil(isi)
    temuan, i = [], 0
    while i <= len(k) - n:
        asal = indeks.get(tuple(k[i:i + n]))
        if not asal:
            i += 1
            continue
        j = i + 1
        while j <= len(k) - n and tuple(k[j:j + n]) in indeks:
            j += 1
        temuan.append((" ".join(k[i:j + n - 1]), asal))
        i = j + n - 1
    return temuan, len(berkas)


def penanda_belum_beres(teks):
    """Daftar (pola, jumlah) penanda yang belum dibereskan. Dipakai juga oleh build_docx.py."""
    hasil = []
    for pola in [POLA_PERLU, r"\bTODO\b", r"\bXXX\b", r"\?\?"]:
        k = len(re.findall(pola, teks, flags=re.I if pola == POLA_PERLU else 0))
        if k:
            hasil.append((pola, k))
    return hasil


def muat_profil(path):
    if not path:
        return {}
    pp = Path(path)
    return json.loads(baca(pp / "profil.json" if pp.is_dir() else pp))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown")
    ap.add_argument("--profil", help="folder lomba (berisi profil.json) atau file JSON profil")
    ap.add_argument("--nama", action="append", default=[], help="nama yang tidak boleh muncul (boleh diulang)")
    ap.add_argument("--sumber", action="append", default=[], help="folder/file sumber (.md/.txt) untuk cek kemiripan (boleh diulang)")
    a = ap.parse_args()

    try:
        profil = muat_profil(a.profil)
        teks = re.sub(r"<!--.*?-->", "", baca(a.markdown), flags=re.S)
    except (OSError, ValueError) as ex:
        sys.exit(f"Gagal membaca file: {ex}")
    bag = pecah_bagian(teks, profil)
    masalah, info = [], []

    n = hitung_kata(bag["isi"])
    lo, hi = profil.get("kata_min"), profil.get("kata_maks")
    status = "OK"
    if lo and n < lo:
        status, _ = "KURANG", masalah.append(f"Jumlah kata isi {n} < minimum {lo}")
    if hi and n > hi:
        status, _ = "LEBIH", masalah.append(f"Jumlah kata isi {n} > maksimum {hi}")
    info.append(f"Jumlah kata isi (tanpa judul, pustaka, lampiran): {n} [{status}]"
                + (f" (batas {lo}–{hi})" if lo or hi else ""))

    for pola, k in penanda_belum_beres(teks):
        label = "[PERLU ...]" if pola == POLA_PERLU else pola
        masalah.append(f"Penanda belum beres '{label}': {k}x")

    for nama in a.nama:
        if nama and ada_kata(nama, teks):
            masalah.append(f"Nama '{nama}' muncul di naskah (lomba melarang identitas penulis/institusi)")

    if bag["pustaka"].strip():
        st, ep = sitasi_teks(bag["isi"]), entri_pustaka(bag["pustaka"])
        yatim, tak_disitasi = cocokkan_sitasi(st, ep)
        for nama, th in yatim:
            masalah.append(f"Sitasi di teks tanpa entri pustaka: {nama.title()} ({th}) "
                           "(kalau singkatan lembaga, tulis di pustaka: 'Nama Lengkap [SINGKATAN]. (tahun)')")
        for nama, th in tak_disitasi:
            masalah.append(f"Entri pustaka tidak pernah disitasi: {nama.title()} ({th})")
        nomor = [int(x) for g in re.findall(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\]", bag["isi"]) for x in re.findall(r"\d+", g)]
        if nomor:
            jumlah = len([b for b in bag["pustaka"].splitlines() if b.strip()])
            for x in sorted(set(nomor)):
                if x > jumlah:
                    masalah.append(f"Sitasi bernomor [{x}] melebihi jumlah entri pustaka ({jumlah})")
        info.append(f"Sitasi unik di teks: {len(st) + len(set(nomor))} · entri pustaka: {len(ep)}")
    else:
        masalah.append("Bagian Daftar Pustaka tidak ditemukan (pakai judul '## Daftar Pustaka')")

    frasa_file = ROOT / "frasa_slop.txt"
    if frasa_file.exists():
        for f in frasa_file.read_text(encoding="utf-8-sig").splitlines():
            f = f.strip()
            if not f or f.startswith("#"):
                continue
            k = len(ada_kata(f, bag["isi"]))
            if k:
                masalah.append(f"Frasa klise: '{f}' ({k}x)")

    if profil.get("gambar_hanya_di_lampiran", False):
        if re.search(r"!\[.*?\]\(.*?\)", bag["isi"]) or re.search(r"^\|.*\|\s*$", bag["isi"], flags=re.M):
            masalah.append("Gambar/tabel ada di luar Lampiran (profil lomba meminta di lampiran)")

    for i, p in enumerate([p for p in re.split(r"\n\s*\n", bag["isi"]) if p.strip() and not p.lstrip().startswith("#")], 1):
        kp = hitung_kata(p)
        if kp > 180:
            masalah.append(f"Paragraf {i} panjang sekali ({kp} kata)")
        for kal in re.split(r"(?<=[.!?])\s+", p):
            if hitung_kata(kal) > 45:
                masalah.append(f"Kalimat sangat panjang di paragraf {i}: \"{kal[:70]}...\"")

    if a.sumber:
        temuan, nb = cek_kemiripan(bag["isi"], a.sumber)
        info.append(f"Cek kemiripan terhadap {nb} file sumber: {len(temuan)} rangkaian sama persis")
        for frasa, asal in temuan:
            potong = frasa if len(frasa) <= 90 else frasa[:90] + "..."
            masalah.append(f"Sama persis dengan {asal} ({len(frasa.split())} kata): \"{potong}\" (parafrasekan, atau jadikan kutipan langsung bertanda petik + sitasi)")

    print("== CEK NASKAH ==")
    for i in info:
        print("·", i)
    if masalah:
        print(f"\n{len(masalah)} hal perlu dicek:")
        for m in masalah:
            print("  -", m)
    else:
        print("\nTidak ada masalah terdeteksi oleh cek otomatis.")
    print("\nCatatan: cek ini tidak memverifikasi kebenaran sumber. Buka setiap link/DOI secara manual.")
    sys.exit(1 if masalah else 0)


if __name__ == "__main__":
    main()
