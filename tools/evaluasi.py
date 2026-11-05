#!/usr/bin/env python3
"""Tahap 8: angka untuk evaluasi pasca-lomba dan tinjauan workflow (lihat workflow/08-evaluasi.md).

Perintah:
  juri <L>          statistik juri Arena Ide dari <L>/ide/juri/*.json:
                    - kesepakatan peringkat antarjuri per kelompok (loop-1, loop-2, final, ...)
                      dengan korelasi Spearman (ties dirata-rata);
                    - persentase ide yang gugur gerbang;
                    - posisi kartu jangkar (ID berawalan X) sebagai persentil;
                    - apakah peringkat 1 panel final sama dengan juara adu (kalau ada adu-final.json).
                    Keluaran Markdown, tinggal ditempel ke <L>/evaluasi.md.
  rekap [folder]    gabungan semua <folder>/*/hasil.json (default: lomba/): tabel per lomba, hitungan
                    hasil, rata-rata persentil jangkar, tingkat setuju uji balik, dan daftar lomba yang
                    belum dievaluasi. Memberi peringatan kalau data belum cukup untuk mengubah
                    hipotesis strategi (< 3 lomba dengan hasil diketahui).

Hanya pustaka standar. Folder yang namanya diawali "_" atau "contoh" dilewati di rekap.
"""
import argparse
import itertools
import json
import re
import statistics
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):  # Windows: output yang di-pipe jatuh ke cp1252
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arena  # noqa: E402

HASIL_DIKETAHUI = {"juara", "finalis", "tidak lolos"}
MIN_LOMBA_STRATEGI = 3


# ---------------------------------------------------------------- statistik dasar
def peringkat_rata(nilai):
    """Peringkat 1..n (kecil = nilai kecil); nilai yang sama mendapat peringkat rata-rata."""
    urut = sorted(range(len(nilai)), key=lambda i: nilai[i])
    pr = [0.0] * len(nilai)
    i = 0
    while i < len(urut):
        j = i
        while j + 1 < len(urut) and nilai[urut[j + 1]] == nilai[urut[i]]:
            j += 1
        for k in range(i, j + 1):
            pr[urut[k]] = (i + j) / 2 + 1
        i = j + 1
    return pr


def spearman(a, b):
    """Korelasi Spearman (Pearson atas peringkat). None kalau < 3 data atau tanpa variasi."""
    if len(a) != len(b) or len(a) < 3:
        return None
    ra, rb = peringkat_rata(a), peringkat_rata(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    sab = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    saa = sum((x - ma) ** 2 for x in ra)
    sbb = sum((y - mb) ** 2 for y in rb)
    if not saa or not sbb:
        return None
    return sab / (saa * sbb) ** 0.5


# ---------------------------------------------------------------- juri
def kelompok_juri(folder_juri):
    """{'loop-1': [(nama_file, json), ...], 'final': [...]} dari file juri berformat arena."""
    grup = {}
    for p in sorted(Path(folder_juri).glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        if not isinstance(d, dict) or "nilai" not in d:
            continue  # file kesan 30 detik, adu, dsb.
        m = re.match(r"^(.*?)-J[^-]*$", p.stem)
        grup.setdefault(m.group(1) if m else p.stem, []).append((p.name, d))
    return grup


def statistik_kelompok(daftar):
    """Kesepakatan dan gerbang untuk satu kelompok juri."""
    skor = []
    for nama, d in daftar:
        s = {v["id"]: float(v.get("total", 0)) for v in d.get("nilai", []) if v.get("lulus_gerbang", True)}
        label = d.get("juri", nama) + ("/" + d["model"] if d.get("model") else "")
        skor.append((label, s))
    pasangan = []
    for (la, sa), (lb, sb) in itertools.combinations(skor, 2):
        ids = sorted(set(sa) & set(sb))
        r = spearman([sa[i] for i in ids], [sb[i] for i in ids])
        pasangan.append((la, lb, len(ids), r))
    n_nilai = sum(len(d.get("nilai", [])) for _, d in daftar)
    n_gugur = sum(1 for _, d in daftar for v in d.get("nilai", []) if not v.get("lulus_gerbang", True))
    hasil = arena.rekap([d for _, d in daftar])
    urut = arena.peringkat(hasil)
    jangkar = {}
    for i in urut:
        if i.upper().startswith("X") and not hasil[i]["gugur"]:
            lain = [x for x in urut if x != i]
            di_bawah = sum(1 for x in lain if urut.index(x) > urut.index(i))
            jangkar[i] = round(100 * di_bawah / len(lain)) if lain else None
    return {"pasangan": pasangan, "n_nilai": n_nilai, "n_gugur": n_gugur,
            "puncak": urut[0] if urut else None, "jangkar": jangkar}


def laporan_juri(folder_lomba):
    folder_lomba = Path(folder_lomba)
    grup = kelompok_juri(folder_lomba / "ide" / "juri")
    if not grup:
        return f"Tidak ada JSON juri di {folder_lomba / 'ide' / 'juri'}."
    baris = [f"### Statistik juri Arena Ide ({folder_lomba.name})", "",
             "| Kelompok | Juri | Ide | Spearman antarjuri (min–maks) | Pasangan paling tidak sepakat | Gugur gerbang | Peringkat 1 |",
             "|---|---|---|---|---|---|---|"]
    total_n = total_g = 0
    semua_r = []
    jangkar_semua = {}
    for nama in sorted(grup, key=lambda g: (not g.startswith("loop"), g)):
        st = statistik_kelompok(grup[nama])
        total_n += st["n_nilai"]
        total_g += st["n_gugur"]
        rs = [p for p in st["pasangan"] if p[3] is not None]
        semua_r += [p[3] for p in rs]
        if rs:
            rentang = f"{min(p[3] for p in rs):.2f} – {max(p[3] for p in rs):.2f}"
            lemah = min(rs, key=lambda p: p[3])
            lemah_s = f"{lemah[0]} vs {lemah[1]} ({lemah[3]:.2f})"
        else:
            rentang, lemah_s = "– (1 juri)", "–"
        n_ide = len({v["id"] for _, d in grup[nama] for v in d.get("nilai", [])})
        baris.append(f"| {nama} | {len(grup[nama])} | {n_ide} | {rentang} | {lemah_s} | "
                     f"{st['n_gugur']}/{st['n_nilai']} | {st['puncak']} |")
        for k, v in st["jangkar"].items():
            jangkar_semua[f"{nama}:{k}"] = v
    baris.append("")
    baris.append(f"- Gugur gerbang seluruhnya: {total_g} dari {total_n} penilaian "
                 f"({(100 * total_g / total_n if total_n else 0):.1f}%).")
    if semua_r:
        baris.append(f"- Median Spearman antarjuri: {statistics.median(semua_r):.2f} "
                     f"(n pasangan = {len(semua_r)}). Di bawah ±0,3 berarti juri hampir tidak sepakat.")
    if jangkar_semua:
        for k, v in jangkar_semua.items():
            baris.append(f"- Kartu jangkar {k}: persentil {v} (lebih tinggi dari {v}% ide lain). "
                         "Di bawah 50 = juri AI tidak menangkap apa yang dihargai juri manusia.")
    else:
        baris.append("- Kartu jangkar: tidak dipakai.")
    adu = folder_lomba / "ide" / "adu-final.json"
    if "final" in grup and adu.exists():
        try:
            poin = arena.poin_adu(json.loads(adu.read_text(encoding="utf-8-sig")))
            juara_adu = sorted(poin, key=lambda x: (-poin[x], x))[0] if poin else None
            puncak_panel = statistik_kelompok(grup["final"])["puncak"]
            sama = "sama" if juara_adu == puncak_panel else "BERBEDA"
            baris.append(f"- Peringkat 1 panel final = {puncak_panel}, juara adu = {juara_adu}: {sama}.")
        except (OSError, ValueError, KeyError) as ex:
            baris.append(f"- adu-final.json tidak terbaca: {ex}")
    return "\n".join(baris)


# ---------------------------------------------------------------- rekap lintas lomba
def baca_hasil(folder):
    hasil = []
    for p in sorted(Path(folder).glob("*/hasil.json")):
        if p.parent.name.startswith(("_", "contoh")):
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError) as ex:
            print(f"Peringatan: {p} tidak terbaca ({ex})", file=sys.stderr)
            continue
        d["_folder"] = p.parent.name
        hasil.append(d)
    return hasil


def _ambil(d, *kunci):
    for k in kunci:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def ringkas_hasil(daftar):
    """Angka agregat dari daftar hasil.json."""
    diketahui = [d for d in daftar if _ambil(d, "hasil", "status") in HASIL_DIKETAHUI]
    jangkar = [float(x) for d in daftar if (x := _ambil(d, "arena", "jangkar_persentil")) is not None]
    uji = [d for d in daftar if _ambil(d, "uji_balik", "dijalankan")]
    setuju = [d for d in uji if _ambil(d, "uji_balik", "juri_ai_pilih_juara_asli") is True]
    hitung = {}
    for d in daftar:
        s = _ambil(d, "hasil", "status") or "?"
        hitung[s] = hitung.get(s, 0) + 1
    return {
        "n": len(daftar),
        "n_diketahui": len(diketahui),
        "hitung": hitung,
        "jangkar_rata": statistics.mean(jangkar) if jangkar else None,
        "n_jangkar": len(jangkar),
        "n_uji": len(uji),
        "n_setuju": len(setuju),
        "cukup_untuk_strategi": len(diketahui) >= MIN_LOMBA_STRATEGI,
    }


def laporan_rekap(folder):
    folder = Path(folder)
    daftar = baca_hasil(folder)
    baris = ["| Lomba | Bidang | Jenjang | Mode | Versi workflow | Dikirim | Hasil | Pilih juara Arena? | Jangkar | Uji balik setuju? |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for d in daftar:
        def f(*k):
            v = _ambil(d, *k)
            return "–" if v is None or v == "" else ("ya" if v is True else "tidak" if v is False else str(v))
        baris.append(f"| {d['_folder']} | {f('bidang')} | {f('jenjang')} | {f('mode')} | {f('versi_workflow')} | "
                     f"{f('dikirim')} | {f('hasil', 'status')} | {f('arena', 'sama_dengan_juara_arena')} | "
                     f"{f('arena', 'jangkar_persentil')} | {f('uji_balik', 'juri_ai_pilih_juara_asli')} |")
    r = ringkas_hasil(daftar)
    baris += ["", f"- Lomba dengan hasil.json: {r['n']}; hasil sudah diketahui: {r['n_diketahui']}.",
              "- Sebaran status: " + (", ".join(f"{k} {v}" for k, v in sorted(r["hitung"].items())) or "–") + "."]
    if r["n_jangkar"]:
        baris.append(f"- Rata-rata persentil kartu jangkar: {r['jangkar_rata']:.0f} (n = {r['n_jangkar']}).")
    if r["n_uji"]:
        baris.append(f"- Uji balik: juri AI memilih juara asli di {r['n_setuju']} dari {r['n_uji']} lomba.")
    if not r["cukup_untuk_strategi"]:
        baris.append(f"- ⚠️ Hasil diketahui baru {r['n_diketahui']} lomba (< {MIN_LOMBA_STRATEGI}). "
                     "Belum cukup untuk mengubah hipotesis strategi (bobot rubrik, persona juri). "
                     "Perbaikan bug dan proses tetap boleh.")
    belum = []
    for p in sorted(folder.iterdir()) if folder.exists() else []:
        if not p.is_dir() or p.name.startswith(("_", "contoh")) or not (p / "STATUS.md").exists():
            continue
        h = p / "hasil.json"
        if not h.exists():
            belum.append(f"{p.name} (8a belum: hasil.json tidak ada)")
            continue
        d = next((x for x in daftar if x["_folder"] == p.name), {})
        dikirim = _ambil(d, "dikirim")
        if dikirim is None:
            belum.append(f"{p.name} (sedang berjalan, atau kolom 'dikirim' belum diisi)")
        elif dikirim is True and _ambil(d, "hasil", "status") not in HASIL_DIKETAHUI:
            tgl = _ambil(d, "tanggal_pengumuman")
            belum.append(f"{p.name} (8b belum: menunggu hasil" + (f", pengumuman {tgl}" if tgl else "") + ")")
    if belum:
        baris.append("- Belum dievaluasi: " + "; ".join(belum) + ".")
    return "\n".join(baris)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="perintah", required=True)
    a1 = sub.add_parser("juri")
    a1.add_argument("lomba")
    a2 = sub.add_parser("rekap")
    a2.add_argument("folder", nargs="?", default=str(Path(__file__).resolve().parent.parent / "lomba"))
    a = ap.parse_args()
    if a.perintah == "juri":
        print(laporan_juri(a.lomba))
    else:
        print(laporan_rekap(a.folder))


if __name__ == "__main__":
    main()
