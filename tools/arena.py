#!/usr/bin/env python3
"""Hitung Arena Ide secara deterministik dari keluaran JSON juri (tahap 1).

Agen utama tidak menghitung peringkat sendiri; ia hanya menjalankan perintah ini dan mencatat hasilnya.

Perintah:
  acak --seed N ID1 ID2 ...        urutan acak (tetap untuk seed yang sama) + label buta A, B, C, ...
                                   Catat seed-nya di STATUS.md supaya bisa diulang.
  rekap <juri1.json> <juri2.json> ...  median skor per ide dari juri buta, gugur kalau mayoritas juri
                                   menyatakan tidak lulus gerbang; urut median lalu median K1+K2.
                                   Boleh diberi JSON semua loop sekaligus = satu kolam gabungan.
        [--top N]                  tandai N teratas sebagai finalis, plus maks. 2 KARTU LIAR: ide di luar
                                   N teratas yang jadi nilai tertinggi seorang juri, dipilih "bela",
                                   atau mendapat "berhenti" di kesan 30 detik
        [--kesan k.json]           {"I01": "berhenti", "I02": "biasa", ...}; boleh diulang (satu per loop)
        [--kecuali X01,I07]        keluarkan kartu jangkar dan ide duplikat dari peringkat; boleh diulang.
                                   Catatan: nilai tertinggi/bela per juri tetap dihitung sebelum pengecualian.
        [--seri 0.5]               ide yang terpaut <= nilai ini dari peringkat 1 dilaporkan SERI
  adu <adu.json>                   poin adu berpasangan: dua urutan sepakat = 1 poin pemenang,
                                   tidak sepakat atau seri = 0,5 masing-masing; selisih puncak <= 0,5 = SERI
  mirip <kartu.md> ... [--ambang 0.18]  pasangan kartu ide yang kata-katanya mirip (calon duplikat).
                                   Kartu = judul "### I07. Nama ide" atau "### [I07] Nama" + isinya.
                                   Ambang 0,18 dikalibrasi pada lomba lama: pasangan >= 0,18 di Pharfest
                                   memang satu keluarga ide. Skrip hanya menyaring calon; agen utama
                                   yang memutuskan duplikat atau bukan.

Format JSON juri (rekap) — satu file per juri:
  {"juri": "J1", "model": "sonnet", "nilai": [
     {"id": "A", "lulus_gerbang": true, "gerbang_gagal": [], "skor": {"K1": 8, "K2": 7, ...}, "total": 7.4}, ...]}

Format JSON adu — daftar hasil, setiap pasangan dijalankan dua kali dengan posisi ditukar:
  [{"a": "A", "b": "B", "urutan": 1, "menang": "A"},   # "menang": id, atau "seri"
   {"a": "B", "b": "A", "urutan": 2, "menang": "B"}, ...]
"""
import argparse
import itertools
import json
import random
import re
import statistics
import string
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):  # Windows: output yang di-pipe jatuh ke cp1252
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def acak(ids, seed):
    hasil = list(ids)
    random.Random(seed).shuffle(hasil)
    return hasil


def label_buta(n):
    huruf = string.ascii_uppercase
    return [huruf[i] if i < 26 else huruf[i // 26 - 1] + huruf[i % 26] for i in range(n)]


def rekap(daftar_juri):
    """{id: {median, median_k12, gugur, n_juri, n_gagal_gerbang, alasan_gerbang,
             maks, sebaran, n_teratas, n_bela}}"""
    per_ide = {}
    for j in daftar_juri:
        lolos = [v for v in j.get("nilai", []) if v.get("lulus_gerbang", True)]
        puncak = max((float(v.get("total", 0)) for v in lolos), default=None)
        for v in j.get("nilai", []):
            d = per_ide.setdefault(v["id"], {"total": [], "k12": [], "gagal": 0, "n": 0, "alasan": [],
                                             "teratas": 0, "bela": 0})
            if j.get("bela") == v["id"]:
                d["bela"] += 1
            if v.get("lulus_gerbang", True) and puncak is not None and float(v.get("total", 0)) == puncak:
                d["teratas"] += 1
            d["n"] += 1
            if not v.get("lulus_gerbang", True):
                d["gagal"] += 1
                d["alasan"] += v.get("gerbang_gagal", [])
                continue
            skor = v.get("skor", {})
            d["total"].append(float(v.get("total", 0)))
            d["k12"].append(float(skor.get("K1", 0)) + float(skor.get("K2", 0)))
    hasil = {}
    for i, d in per_ide.items():
        gugur = d["gagal"] * 2 > d["n"]
        hasil[i] = {
            "median": statistics.median(d["total"]) if d["total"] and not gugur else 0.0,
            "median_k12": statistics.median(d["k12"]) if d["k12"] and not gugur else 0.0,
            "gugur": gugur,
            "n_juri": d["n"],
            "n_gagal_gerbang": d["gagal"],
            "alasan_gerbang": sorted(set(d["alasan"])),
            "maks": max(d["total"]) if d["total"] and not gugur else 0.0,
            "sebaran": (max(d["total"]) - min(d["total"])) if d["total"] and not gugur else 0.0,
            "n_teratas": 0 if gugur else d["teratas"],
            "n_bela": 0 if gugur else d["bela"],
        }
    return hasil


def peringkat(hasil):
    return sorted(hasil, key=lambda i: (hasil[i]["gugur"], -hasil[i]["median"], -hasil[i]["median_k12"], i))


def kartu_liar(hasil, urut, top, kesan=None, maks_liar=2):
    """Ide di luar `top` teratas yang punya sinyal kuat dari satu sumber saja.

    Median meredam ide yang memecah pendapat (satu juri terpikat, yang lain biasa saja), padahal
    reaksi "berhenti dan tertarik" adalah sinyal yang paling dicari. Sinyal: nilai tertinggi
    seorang juri, dipilih untuk dibela, atau "berhenti" di kesan 30 detik. Urut: jumlah sinyal,
    lalu nilai maksimum, lalu median.
    """
    kesan = kesan or {}
    calon = []
    for i in urut[top:]:
        d = hasil[i]
        if d["gugur"]:
            continue
        sinyal = []
        if d["n_teratas"]:
            sinyal.append(f"nilai tertinggi {d['n_teratas']} juri")
        if d["n_bela"]:
            sinyal.append(f"dibela {d['n_bela']} juri")
        if str(kesan.get(i, "")).strip().lower() == "berhenti":
            sinyal.append("kesan 30 detik: berhenti")
        if sinyal:
            calon.append((i, sinyal))
    calon.sort(key=lambda c: (-len(c[1]), -hasil[c[0]]["maks"], -hasil[c[0]]["median"], c[0]))
    return calon[:maks_liar]


def seri_puncak(hasil, urut, ambang=0.5):
    """ID yang mediannya terpaut <= ambang dari peringkat 1 (termasuk peringkat 1)."""
    lolos = [i for i in urut if not hasil[i]["gugur"]]
    if not lolos:
        return []
    atas = hasil[lolos[0]]["median"]
    return [i for i in lolos if atas - hasil[i]["median"] <= ambang + 1e-9]


KATA_UMUM = set("""yang dan di ke dari untuk dengan pada ini itu atau dalam oleh sebagai tidak akan bisa
dapat juga lebih karena agar adalah para tiap setiap serta saat sudah belum masih hanya antara secara
bagi tentang melalui menjadi ada mereka kita kami sendiri tanpa sehingga namun bahwa lalu baru satu dua
tiga mana apa siapa bagaimana per hal cara ide inti masalah mekanisme lokus pelaku bukti mungkin risiko
terbesar subtema utama the of and to in a for is on""".split())


def _kata(teks):
    return {k for k in re.findall(r"[a-z0-9]+", teks.lower()) if len(k) > 2 and k not in KATA_UMUM}


def baca_kartu(teks):
    """{id: teks} dari kartu berformat '### I07. Nama' (baris Lensa/Kenapa tidak pasaran dibuang)."""
    kartu, kini = {}, None
    for baris in teks.splitlines():
        m = re.match(r"^#{2,4}\s+\[?([A-Za-z]*\d+)\]?[.):]?\s+(.*)$", baris)
        if m:
            kini = m.group(1)
            kartu[kini] = [m.group(2)]
            continue
        if baris.startswith("#"):
            kini = None
            continue
        if kini and not re.match(r"^\s*-\s*\**(Lensa|Kenapa tidak pasaran)\b", baris, re.I):
            kartu[kini].append(baris)
    return {i: "\n".join(v) for i, v in kartu.items()}


def mirip(kartu, ambang=0.18):
    """Pasangan (a, b, jaccard) dengan kemiripan kata >= ambang, terbesar dulu."""
    kata = {i: _kata(t) for i, t in kartu.items()}
    hasil = []
    for a, b in itertools.combinations(sorted(kata), 2):
        gabung = kata[a] | kata[b]
        if not gabung:
            continue
        j = len(kata[a] & kata[b]) / len(gabung)
        if j >= ambang:
            hasil.append((a, b, j))
    return sorted(hasil, key=lambda x: -x[2])


def poin_adu(adu):
    poin = {}
    pasangan = {}
    for r in adu:
        for x in (r["a"], r["b"]):
            poin.setdefault(x, 0.0)
        pasangan.setdefault(frozenset((r["a"], r["b"])), []).append(r.get("menang", "seri"))
    for pas, menang in pasangan.items():
        a, b = sorted(pas)
        if len(set(menang)) == 1 and menang[0] in pas and len(menang) >= 2:
            poin[menang[0]] += 1
        else:  # tidak sepakat antar urutan, seri, atau hanya dijalankan sekali
            poin[a] += 0.5
            poin[b] += 0.5
    return poin


def baca_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as ex:
        sys.exit(f"Gagal membaca {p}: {ex}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="perintah", required=True)
    a1 = sub.add_parser("acak")
    a1.add_argument("--seed", type=int, required=True)
    a1.add_argument("ids", nargs="+")
    a2 = sub.add_parser("rekap")
    a2.add_argument("files", nargs="+")
    a2.add_argument("--top", type=int, default=0)
    a2.add_argument("--kesan", action="append", default=[])
    a2.add_argument("--kecuali", action="append", default=[])
    a2.add_argument("--seri", type=float, default=0.5)
    a3 = sub.add_parser("adu")
    a3.add_argument("file")
    a4 = sub.add_parser("mirip")
    a4.add_argument("files", nargs="+")
    a4.add_argument("--ambang", type=float, default=0.18)
    a = ap.parse_args()

    if a.perintah == "acak":
        urut = acak(a.ids, a.seed)
        print(f"seed {a.seed}")
        print("| Label buta | ID asli |\n|---|---|")
        for lab, i in zip(label_buta(len(urut)), urut):
            print(f"| {lab} | {i} |")
    elif a.perintah == "rekap":
        juri = [baca_json(f) for f in a.files]
        h = rekap(juri)
        print(f"Juri: {', '.join(j.get('juri', '?') + ('/' + j['model'] if j.get('model') else '') for j in juri)}")
        buang = {x.strip() for k in a.kecuali for x in k.split(",") if x.strip()}
        if buang:
            h = {i: d for i, d in h.items() if i not in buang}
            print(f"Dikecualikan: {', '.join(sorted(buang))}")
        urut = peringkat(h)
        kesan = {}
        for f in a.kesan:
            kesan.update(baca_json(f))
        liar = dict(kartu_liar(h, urut, a.top, kesan)) if a.top else {}
        print("| Peringkat | ID | Median total | Median K1+K2 | Maks | Sebaran | #1 juri | Bela | Gagal gerbang | Status |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for n, i in enumerate(urut, 1):
            d = h[i]
            if d["gugur"]:
                status = "GUGUR: " + "; ".join(d["alasan_gerbang"])
            elif a.top and n <= a.top:
                status = "finalis"
            elif i in liar:
                status = "KARTU LIAR (" + ", ".join(liar[i]) + ")"
            else:
                status = "lolos"
            print(f"| {n} | {i} | {d['median']:.2f} | {d['median_k12']:.2f} | {d['maks']:.2f} | {d['sebaran']:.2f}"
                  f" | {d['n_teratas']} | {d['n_bela']} | {d['n_gagal_gerbang']}/{d['n_juri']} | {status} |")
        seri = seri_puncak(h, urut, a.seri)
        if len(seri) > 1:
            print(f"\nSERI DI PUNCAK: {', '.join(seri)} terpaut <= {a.seri:g} dari peringkat 1. "
                  "Selisih sebesar ini masih dalam derau juri; jangan sebut satu pemenang dari median saja.")
    elif a.perintah == "adu":
        poin = poin_adu(baca_json(a.file))
        print("| ID | Poin adu |\n|---|---|")
        urut = sorted(poin, key=lambda x: (-poin[x], x))
        for i in urut:
            print(f"| {i} | {poin[i]:g} |")
        if len(urut) > 1 and poin[urut[0]] - poin[urut[1]] <= 0.5:
            print(f"\nSERI/TIPIS: {urut[0]} ({poin[urut[0]]:g}) dan {urut[1]} ({poin[urut[1]]:g}) terpaut <= 0,5 poin. "
                  "Sajikan keduanya ke penulis sebagai pilihan setara.")
    elif a.perintah == "mirip":
        kartu = {}
        for f in a.files:
            try:
                kartu.update(baca_kartu(Path(f).read_text(encoding="utf-8-sig")))
            except OSError as ex:
                sys.exit(f"Gagal membaca {f}: {ex}")
        pasang = mirip(kartu, a.ambang)
        print(f"{len(kartu)} kartu dibaca, {len(pasang)} pasangan dengan kemiripan kata >= {a.ambang:g}")
        if pasang:
            print("| Ide A | Ide B | Kemiripan |\n|---|---|---|")
            for x, y, j in pasang:
                print(f"| {x} | {y} | {j:.2f} |")
            print("\nIni calon duplikat, bukan putusan. Baca kedua kartu: kalau inti dan mekanismenya sama, "
                  "simpan yang lebih tajam dan catat yang dibuang di ide/kolam.md.")


if __name__ == "__main__":
    main()
