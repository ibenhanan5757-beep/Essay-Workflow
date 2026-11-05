#!/usr/bin/env python3
"""Buat grafik dan diagram untuk esai dari file spesifikasi JSON, dengan gaya yang seragam dan rapi cetak.

Pakai:
    python tools/buat_visual.py <L>/visual/gambar1.json --profil <L>
    python tools/buat_visual.py <L>/visual/*.json --profil <L>        # semua sekaligus

Hasil: PNG 300 DPI di <L>/draf/gambar/<nama spesifikasi>.png, siap dipanggil dari naskah:
    ![Gambar 1. Keterangan](gambar/gambar1.png)

Gaya sengaja tenang: font sama dengan naskah (dari profil.json), abu-abu + satu warna aksen,
tanpa judul di dalam gambar (judul ada di keterangan Word), tanpa 3D, tanpa bayangan, tetap terbaca
kalau dicetak hitam-putih. Butuh `pip install matplotlib`.

Jenis yang didukung (lihat contoh di workflow/03b-rencana-visual.md):
    batang    : perbandingan antar kategori (tegak)
    batang_h  : perbandingan dengan label kategori panjang (mendatar)
    garis     : tren dari waktu ke waktu
    alur      : diagram alur/mekanisme (kotak dan panah), mendatar atau menurun
    siklus    : langkah yang berputar (misalnya siklus pemantauan)

Setelah menggambar, alat memeriksa tata letak dan mencetak PERIKSA kalau ada:
    - teks yang bertumpuk (label, angka, legenda, catatan);
    - teks yang keluar dari kotak diagram;
    - huruf yang saat dicetak di Word lebih kecil dari 8 pt (dihitung dari lebar_gambar_cm dan
      tinggi_gambar_maks_cm di profil, sama seperti build_docx.py).
Peringatan ini bukan pengganti melihat gambarnya; lihat workflow/03b-rencana-visual.md § 8.
"""
import argparse
import json
import math
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):  # Windows: output yang di-pipe jatuh ke cp1252 dan crash pada emoji
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ABU =["#4d4d4d", "#8c8c8c", "#bfbfbf", "#d9d9d9"]
AKSEN_DEFAULT = "#1f5a8a"  # biru tua: tetap jadi abu gelap kalau dicetak hitam-putih
TEKS = "#222222"


def muat_profil(jalur):
    if not jalur:
        return {}
    p = Path(jalur)
    if p.is_dir():
        p = p / "profil.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def siapkan(plt, font):
    from matplotlib import font_manager
    tersedia = {f.name for f in font_manager.fontManager.ttflist}
    pilihan = [font] if font in tersedia else []
    pilihan += ["Times New Roman", "Liberation Serif", "DejaVu Serif"] if (font or "").lower().find("sans") < 0 and font not in ("Arial", "Calibri") else ["Arial", "Liberation Sans", "DejaVu Sans"]
    plt.rcParams.update({
        "font.family": [f for f in pilihan if f in tersedia] or ["serif"],
        "font.size": 10,
        "axes.edgecolor": "#888888",
        "axes.labelcolor": TEKS,
        "xtick.color": TEKS,
        "ytick.color": TEKS,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 10,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.08,
    })


def warna_seri(n, aksen, sorot_semua=False):
    if n == 1:
        return [aksen]
    return [aksen] + ABU[: n - 1] if n <= 4 else [aksen] + [ABU[i % len(ABU)] for i in range(n - 1)]


def label_angka(ax, batang, satuan, mendatar=False):
    for b in batang:
        nilai = b.get_width() if mendatar else b.get_height()
        teks = f"{nilai:,.1f}".rstrip("0").rstrip(".").replace(",", "X").replace(".", ",").replace("X", ".") + (satuan or "")
        if mendatar:
            ax.text(b.get_x() + nilai, b.get_y() + b.get_height() / 2, " " + teks, va="center", fontsize=9, color=TEKS)
        else:
            ax.text(b.get_x() + b.get_width() / 2, nilai, teks, ha="center", va="bottom", fontsize=9, color=TEKS)


def grafik_batang(plt, s, aksen, mendatar=False):
    label = s["label"]
    seri = s["seri"]
    lebar_cm = s.get("lebar_cm", 15)
    tinggi_cm = s.get("tinggi_cm", 7.5 if not mendatar else max(5, 0.9 * len(label) + 1.5))
    fig, ax = plt.subplots(figsize=(lebar_cm / 2.54, tinggi_cm / 2.54))
    n = len(seri)
    tebal = 0.8 / n
    warna = warna_seri(n, aksen)
    sorot = s.get("sorot")  # indeks kategori yang disorot (hanya untuk 1 seri)
    for i, sr in enumerate(seri):
        posisi = [k + (i - (n - 1) / 2) * tebal for k in range(len(label))]
        if n == 1 and sorot is not None:
            w = [aksen if k == sorot else ABU[2] for k in range(len(label))]
        else:
            w = warna[i]
        fungsi = ax.barh if mendatar else ax.bar
        batang = fungsi(posisi, sr["nilai"], tebal * 0.92, color=w, label=sr.get("nama"))
        if s.get("tampilkan_angka", True):
            label_angka(ax, batang, s.get("satuan", ""), mendatar)
    if mendatar:
        ax.set_yticks(range(len(label)), label)
        ax.invert_yaxis()
        ax.set_xlabel(s.get("sumbu_x", ""))
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.xaxis.grid(True, color="#e6e6e6", linewidth=0.6)
    else:
        ax.set_xticks(range(len(label)), label)
        ax.set_ylabel(s.get("sumbu_y", ""))
        ax.set_xlabel(s.get("sumbu_x", ""))
        ax.yaxis.grid(True, color="#e6e6e6", linewidth=0.6)
    ax.set_axisbelow(True)
    if n > 1:
        ax.legend(frameon=False, fontsize=9)
    return fig


def grafik_garis(plt, s, aksen):
    fig, ax = plt.subplots(figsize=(s.get("lebar_cm", 15) / 2.54, s.get("tinggi_cm", 7.5) / 2.54))
    warna = warna_seri(len(s["seri"]), aksen)
    gaya = ["-", "--", ":", "-."]
    for i, sr in enumerate(s["seri"]):
        ax.plot(s["label"], sr["nilai"], gaya[i % 4], color=warna[i], linewidth=1.8 if i == 0 else 1.3,
                marker="o", markersize=3.5, label=sr.get("nama"))
        if s.get("label_ujung", True) and len(s["seri"]) > 1:
            ax.annotate(sr.get("nama", ""), (len(s["label"]) - 1, sr["nilai"][-1]), xytext=(4, 0),
                        textcoords="offset points", va="center", fontsize=9, color=warna[i])
    ax.set_ylabel(s.get("sumbu_y", ""))
    ax.set_xlabel(s.get("sumbu_x", ""))
    ax.yaxis.grid(True, color="#e6e6e6", linewidth=0.6)
    ax.set_axisbelow(True)
    if len(s["seri"]) > 1 and not s.get("label_ujung", True):
        ax.legend(frameon=False, fontsize=9)
    for teks in s.get("catatan", []):  # [{"x": indeks, "y": nilai, "teks": "..."}]
        ax.annotate(teks["teks"], (teks["x"], teks["y"]), xytext=(0, 14), textcoords="offset points",
                    ha="center", fontsize=8.5, color=TEKS, arrowprops={"arrowstyle": "-", "color": "#888888", "lw": 0.6})
    return fig


def kotak(ax, x, y, l, t, teks, utama=False, aksen=AKSEN_DEFAULT, kecil=None):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x - l / 2, y - t / 2), l, t, boxstyle="round,pad=0.02,rounding_size=0.06",
                                facecolor=aksen if utama else "white", edgecolor=aksen if utama else "#555555", linewidth=1))
    ax.text(x, y + (0.08 if kecil else 0), teks, ha="center", va="center", fontsize=9.5,
            color="white" if utama else TEKS, wrap=True, fontweight="bold" if utama else "normal")
    if kecil:
        ax.text(x, y - t / 2 + 0.12, kecil, ha="center", va="bottom", fontsize=7.5,
                color="#eeeeee" if utama else "#555555")


def panah(ax, a, b, label=None):
    ax.annotate("", xy=b, xytext=a, arrowprops={"arrowstyle": "-|>", "color": "#555555", "lw": 1, "shrinkA": 0, "shrinkB": 0})
    if label:
        tegak = abs(a[0] - b[0]) < 1e-6
        x, y = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        ax.text(x + (0.1 if tegak else 0), y + (0 if tegak else 0.1), label, ha="left" if tegak else "center",
                va="center" if tegak else "bottom", fontsize=8, color="#555555")


def bungkus(teks, lebar):
    import textwrap
    return "\n".join(textwrap.wrap(teks, lebar)) or teks


def diagram_alur(plt, s, aksen):
    langkah = s["langkah"]  # ["teks", ...] atau [{"teks": ..., "catatan": ..., "utama": true}, ...]
    langkah = [x if isinstance(x, dict) else {"teks": x} for x in langkah]
    n = len(langkah)
    menurun = s.get("arah", "kanan") == "bawah" or n > 5
    l, t, jarak = (2.8, 0.7, 1.25) if menurun else (2.2, 1.45, 2.75)
    if menurun:
        lebar = s.get("lebar_cm", 8) / 2.54
        fig, ax = plt.subplots(figsize=(lebar, lebar * ((n - 1) * jarak + t + 0.5) / (l + 0.4)))
        pos = [(0, -i * jarak) for i in range(n)]
    else:
        fig, ax = plt.subplots(figsize=(s.get("lebar_cm", 15) / 2.54, s.get("tinggi_cm", 4) / 2.54))
        pos = [(i * jarak, 0) for i in range(n)]
    for i, (lk, (x, y)) in enumerate(zip(langkah, pos)):
        kotak(ax, x, y, l, t, bungkus(lk["teks"], 28 if menurun else 12), lk.get("utama"), aksen, lk.get("catatan"))
        if i < n - 1:
            nx, ny = pos[i + 1]
            a = (x, y - t / 2) if menurun else (x + l / 2, y)
            b = (nx, ny + t / 2) if menurun else (nx - l / 2, ny)
            panah(ax, a, b, lk.get("label_panah"))
    xs = [p[0] for p in pos]
    ys = [p[1] for p in pos]
    ax.set_xlim(min(xs) - l / 2 - 0.2, max(xs) + l / 2 + 0.2)
    ax.set_ylim(min(ys) - t / 2 - 0.2, max(ys) + t / 2 + 0.3)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def diagram_siklus(plt, s, aksen):
    langkah = [x if isinstance(x, dict) else {"teks": x} for x in s["langkah"]]
    n = len(langkah)
    r = 1.9
    fig, ax = plt.subplots(figsize=(s.get("lebar_cm", 11) / 2.54, s.get("lebar_cm", 11) / 2.54))
    pos = [(r * math.cos(math.pi / 2 - 2 * math.pi * i / n), r * math.sin(math.pi / 2 - 2 * math.pi * i / n)) for i in range(n)]
    l, t = 1.7, 0.75
    for i, (lk, (x, y)) in enumerate(zip(langkah, pos)):
        kotak(ax, x, y, l, t, bungkus(lk["teks"], 13), lk.get("utama"), aksen)
    from matplotlib.patches import FancyArrowPatch
    for i in range(n):
        a, b = pos[i], pos[(i + 1) % n]
        ax.add_patch(FancyArrowPatch(a, b, connectionstyle="arc3,rad=-0.25", arrowstyle="-|>", mutation_scale=10,
                                     color="#555555", lw=1, shrinkA=28, shrinkB=28))
    if s.get("pusat"):
        ax.text(0, 0, bungkus(s["pusat"], 14), ha="center", va="center", fontsize=10, color=aksen, fontweight="bold")
    ax.set_xlim(-r - 1.1, r + 1.1)
    ax.set_ylim(-r - 0.7, r + 0.7)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def _pendek(teks, n=30):
    s = " ".join(teks.get_text().split())
    return s if len(s) <= n else s[: n - 1] + "…"


def periksa_tata_letak(fig, profil=None):
    """Daftar temuan tata letak: teks bertumpuk, teks keluar kotak, huruf tercetak < 8 pt."""
    from matplotlib.patches import FancyBboxPatch
    from matplotlib.text import Text
    profil = profil or {}
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    teks = [(t, t.get_window_extent(r)) for t in fig.findobj(Text)
            if t.get_visible() and t.get_text().strip() and t.get_figure() is fig]
    temuan, tumpuk = [], []
    for i in range(len(teks)):
        for j in range(i + 1, len(teks)):
            (ta, a), (tb, b) = teks[i], teks[j]
            lebar = min(a.x1, b.x1) - max(a.x0, b.x0)
            tinggi = min(a.y1, b.y1) - max(a.y0, b.y0)
            kecil = min(a.width * a.height, b.width * b.height)
            if lebar > 1 and tinggi > 1 and kecil > 0 and lebar * tinggi / kecil > 0.15:
                tumpuk.append(f'teks bertumpuk: "{_pendek(ta)}" dan "{_pendek(tb)}"')
    temuan += tumpuk[:2]
    if len(tumpuk) > 2:
        temuan.append(f"… dan {len(tumpuk) - 2} pasangan teks bertumpuk lain. Label kategori yang panjang: pakai jenis "
                      "'batang_h' atau persingkat labelnya")
    for ax in fig.axes:
        for p in ax.patches:
            if not isinstance(p, FancyBboxPatch):
                continue
            k = p.get_window_extent(r)
            for t, bb in teks:
                cx, cy = (bb.x0 + bb.x1) / 2, (bb.y0 + bb.y1) / 2
                if k.x0 < cx < k.x1 and k.y0 < cy < k.y1 and (
                        bb.x0 < k.x0 - 2 or bb.x1 > k.x1 + 2 or bb.y0 < k.y0 - 2 or bb.y1 > k.y1 + 2):
                    temuan.append(f'teks keluar dari kotak: "{_pendek(t)}" (persingkat teks atau perlebar gambar)')
    if teks:
        pad = 2 * 0.08  # savefig.pad_inches di siapkan()
        kotak_ketat = fig.get_tightbbox(r)
        lebar_cm, tinggi_cm = (kotak_ketat.width + pad) * 2.54, (kotak_ketat.height + pad) * 2.54
        lebar_cetak = min(float(profil.get("lebar_gambar_cm") or 14),
                          float(profil.get("tinggi_gambar_maks_cm") or 10) * lebar_cm / tinggi_cm)
        terkecil = min(t.get_fontsize() for t, _ in teks) * lebar_cetak / lebar_cm
        if terkecil < 8:
            temuan.append(f"huruf terkecil tercetak ±{terkecil:.1f} pt (minimal 8 pt): kecilkan 'lebar_cm' di spesifikasi "
                          "supaya gambar diperbesar saat dicetak, atau persingkat teksnya")
    return list(dict.fromkeys(temuan))


def buat(jalur_spek, profil, out_dir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    s = json.loads(Path(jalur_spek).read_text(encoding="utf-8"))
    siapkan(plt, profil.get("font"))
    aksen = s.get("warna_aksen", profil.get("warna_aksen", AKSEN_DEFAULT))
    jenis = s.get("jenis")
    pembuat = {"batang": lambda: grafik_batang(plt, s, aksen), "batang_h": lambda: grafik_batang(plt, s, aksen, True),
               "garis": lambda: grafik_garis(plt, s, aksen), "alur": lambda: diagram_alur(plt, s, aksen),
               "siklus": lambda: diagram_siklus(plt, s, aksen)}
    if jenis not in pembuat:
        sys.exit(f"{jalur_spek}: jenis '{jenis}' tidak dikenal. Pilih: {', '.join(pembuat)}")
    if jenis in ("batang", "batang_h", "garis") and not s.get("sumber"):
        print(f"PERINGATAN {jalur_spek}: grafik data tanpa 'sumber'. Setiap angka harus dari dossier.", file=sys.stderr)
    fig = pembuat[jenis]()
    temuan = periksa_tata_letak(fig, profil)
    out = Path(out_dir) / (Path(jalur_spek).stem + ".png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {out}" + (f"  (sumber untuk keterangan: {s['sumber']})" if s.get("sumber") else ""))
    for t in temuan:
        print(f"  ⚠️ PERIKSA {Path(jalur_spek).name}: {t}")
    return temuan


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spek", nargs="+", help="file JSON spesifikasi")
    ap.add_argument("--profil", help="folder lomba (berisi profil.json) untuk font")
    ap.add_argument("--out", help="folder hasil (default: <folder lomba>/draf/gambar)")
    a = ap.parse_args()
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        sys.exit("matplotlib belum terpasang. Jalankan: pip install matplotlib")
    profil = muat_profil(a.profil)
    out_dir = a.out or (Path(a.profil) / "draf" / "gambar" if a.profil and Path(a.profil).is_dir() else Path("gambar"))
    jumlah = sum(len(buat(spek, profil, out_dir)) for spek in a.spek)
    print(f"\n{jumlah} temuan tata letak." + (" Perbaiki, atau tulis alasannya di draf/rencana-visual.md, lalu tetap lihat setiap PNG."
                                               if jumlah else " Tetap lihat setiap PNG sebelum dipakai."))


if __name__ == "__main__":
    main()
