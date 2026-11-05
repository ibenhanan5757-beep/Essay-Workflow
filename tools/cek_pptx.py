#!/usr/bin/env python3
"""Periksa slide presentasi (.pptx): tanda "slide buatan AI", dan baca gaya dari PPT contoh.

Pakai:
    python tools/cek_pptx.py cek  "<L>/presentasi/slide.pptx" [--durasi 7] [--maks-slide 10]
    python tools/cek_pptx.py gaya "<L>/presentasi/contoh/contoh.pptx" [--out "<L>/presentasi/gaya-contoh.md"]

cek  : per slide dan seluruh deck. Melapor KRITIS/MAYOR/MINOR/INFO:
       - emoji/simbol dekoratif, gradasi (terutama ungu-biru/ungu-pink), efek glow/bayangan
       - lebih dari 2 keluarga huruf, huruf isi lebih kecil dari 18 pt (baris "Sumber:" boleh 12 pt)
       - terlalu banyak kata atau butir per slide, judul berupa label ("Latar Belakang") bukan kalimat
       - warna ungu/violet, terlalu banyak warna aksen, kapital semua yang panjang
       - jumlah slide terlalu banyak untuk durasi, slide tanpa catatan pembicara
gaya : ringkasan gaya PPT contoh (ukuran slide, font tema dan yang dipakai, warna, ukuran judul/isi,
       kata per slide, tata letak, gambar, gradasi) untuk ditiru gayanya, bukan isinya.
Butuh `pip install python-pptx`.
"""
import argparse
import colorsys
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅❌✔✖➡⬅-⬇]")
JUDUL_LABEL = {
    "latar belakang", "pendahuluan", "rumusan masalah", "tujuan", "manfaat", "metode", "metodologi",
    "pembahasan", "hasil", "solusi", "gagasan", "kesimpulan", "penutup", "saran", "daftar pustaka",
    "referensi", "agenda", "outline", "overview", "introduction", "background", "conclusion", "problem",
    "solution", "analisis", "implementasi", "dampak", "terima kasih", "thank you", "tim", "team",
}
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}


def hex_ke_hsv(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return colorsys.rgb_to_hsv(r, g, b)


def ungu(h):
    hue, sat, val = hex_ke_hsv(h)
    return 0.70 <= hue <= 0.87 and sat >= 0.35 and val >= 0.25


def berwarna(h):
    _, sat, val = hex_ke_hsv(h)
    return sat >= 0.25 and 0.15 <= val


def font_tema(path):
    """Font judul (major) dan isi (minor) dari theme1.xml."""
    hasil = {}
    try:
        with zipfile.ZipFile(path) as z:
            nama = next((n for n in z.namelist() if re.match(r"ppt/theme/theme\d+\.xml", n)), None)
            if nama:
                xml = z.read(nama).decode("utf-8", "replace")
                for jenis in ("major", "minor"):
                    m = re.search(rf"<a:{jenis}Font>\s*<a:latin typeface=\"([^\"]*)\"", xml)
                    if m:
                        hasil[jenis] = m.group(1)
    except (OSError, zipfile.BadZipFile):
        pass
    return hasil


def teks_shape(shape):
    if not shape.has_text_frame:
        return []
    return [p for p in shape.text_frame.paragraphs]


def info_slide(slide, tema):
    """Kumpulkan data satu slide dari objek python-pptx dan XML mentahnya."""
    xml = slide._element.xml
    judul = ""
    if slide.shapes.title is not None and slide.shapes.title.has_text_frame:
        judul = slide.shapes.title.text_frame.text.strip()
    kata, butir, kecil, kapital, emoji = 0, 0, [], [], set()
    ukuran = Counter()
    for shape in slide.shapes:
        if shape.has_table if hasattr(shape, "has_table") else False:
            for baris in shape.table.rows:
                for sel in baris.cells:
                    kata += len(sel.text.split())
            continue
        adalah_judul = slide.shapes.title is not None and shape.shape_id == slide.shapes.title.shape_id
        # placeholder isi (Title and Content) memberi butir dari tata letak, tanpa buChar di slide
        isi_placeholder = shape.is_placeholder and not adalah_judul and shape.placeholder_format.type in (2, 7)
        for p in teks_shape(shape):
            t = p.text.strip()
            if not t:
                continue
            emoji |= set(EMOJI.findall(t))
            if not adalah_judul:
                kata += len(t.split())
                tanpa_butir = p._p.find(".//a:buNone", NS) is not None
                if not tanpa_butir and (isi_placeholder or p.level > 0 or p._p.find(".//a:buChar", NS) is not None
                                        or p._p.find(".//a:buAutoNum", NS) is not None):
                    butir += 1
            if len(t) > 25 and t.isupper():
                kapital.append(t[:40])
            for r in p.runs:
                if r.font.size is not None:
                    pt = r.font.size.pt
                    ukuran[pt] += 1
                    batas = 12 if re.match(r"^\s*(sumber|source)\s*:", t, re.I) else 18
                    if pt < batas and r.text.strip():
                        kecil.append((pt, t[:40]))
    fonts = Counter()
    for m in re.finditer(r'<a:latin typeface="([^"]+)"', xml):
        f = m.group(1)
        f = tema.get("major", f) if f == "+mj-lt" else tema.get("minor", f) if f == "+mn-lt" else f
        fonts[f] += 1
    warna = Counter(m.group(1).upper() for m in re.finditer(r'<a:srgbClr val="([0-9A-Fa-f]{6})"', xml))
    grad = re.findall(r"<a:gradFill.*?</a:gradFill>", xml, re.S)
    warna_grad = [c.upper() for g in grad for c in re.findall(r'<a:srgbClr val="([0-9A-Fa-f]{6})"', g)]
    return {
        "judul": judul, "kata": kata, "butir": butir, "kecil": kecil, "kapital": kapital, "emoji": emoji,
        "fonts": fonts, "warna": warna, "grad": len(grad), "warna_grad": warna_grad, "ukuran": ukuran,
        "glow": xml.count("<a:glow"), "bayangan": xml.count("<a:outerShdw"),
        "gambar": sum(1 for s in slide.shapes if s.shape_type == 13),
        "catatan": slide.has_notes_slide and bool(slide.notes_slide.notes_text_frame.text.strip()),
        "tata_letak": slide.slide_layout.name,
    }


def judul_label(judul):
    j = judul.strip().rstrip(":").lower()
    return j in JUDUL_LABEL or (len(j.split()) <= 2 and not re.search(r"\d", j))


def cek(path, durasi=None, maks_slide=None):
    from pptx import Presentation
    prs = Presentation(str(path))
    tema = font_tema(path)
    temuan = []
    semua_font, semua_warna = Counter(), Counter()
    slides = list(prs.slides)

    def catat(t, m):
        temuan.append((t, m))

    for i, slide in enumerate(slides, 1):
        s = info_slide(slide, tema)
        semua_font.update(s["fonts"])
        semua_warna.update(s["warna"])
        label = f"Slide {i}" + (f" (\"{s['judul'][:30]}\")" if s["judul"] else "")
        if s["emoji"]:
            catat("KRITIS", f"{label}: emoji/simbol dekoratif {' '.join(sorted(s['emoji']))}")
        if s["grad"]:
            if any(ungu(c) for c in s["warna_grad"]):
                catat("KRITIS", f"{label}: gradasi bernada ungu. Ini ciri paling umum slide buatan AI.")
            else:
                catat("MAYOR", f"{label}: {s['grad']} isian gradasi. Pakai warna rata.")
        if s["glow"]:
            catat("MAYOR", f"{label}: efek glow.")
        if s["bayangan"] > 2:
            catat("MINOR", f"{label}: {s['bayangan']} bayangan. Kedalaman cukup dari ukuran dan jarak.")
        if s["kata"] > 50:
            catat("MAYOR", f"{label}: {s['kata']} kata. Slide dibaca sekilas; pindahkan ke naskah bicara (target ≤ 30).")
        elif s["kata"] > 35:
            catat("MINOR", f"{label}: {s['kata']} kata (target ≤ 30).")
        if s["butir"] > 4:
            catat("MAYOR", f"{label}: {s['butir']} butir. Pecah, atau ganti dengan satu kalimat + visual.")
        if s["kecil"]:
            pt, contoh = min(s["kecil"])
            catat("MAYOR", f"{label}: huruf {pt:g} pt (\"{contoh}\"). Minimal 18 pt untuk isi, 12 pt untuk sumber.")
        if s["kapital"]:
            catat("MINOR", f"{label}: kapital semua yang panjang (\"{s['kapital'][0]}\").")
        if s["judul"] and judul_label(s["judul"]) and 1 < i < len(slides):
            catat("MINOR", f"{label}: judul berupa label. Tulis kesimpulannya, misalnya \"Kasus naik 75% dalam 3 tahun\".")
        if not s["judul"] and 1 < i < len(slides):
            catat("MINOR", f"Slide {i}: tanpa judul.")
        if not s["catatan"]:
            catat("INFO", f"Slide {i}: belum ada catatan pembicara.")

    fonts = [f for f in semua_font if f]
    if len(fonts) > 2:
        catat("MAYOR", f"{len(fonts)} keluarga huruf: {', '.join(fonts)}. Maksimal 2.")
    aksen = sorted({c for c in semua_warna if berwarna(c)})
    if len(aksen) > 3:
        catat("MINOR", f"{len(aksen)} warna berwarna dipakai ({', '.join('#' + c for c in aksen[:8])}). Cukup 1 aksen, maksimal 3.")
    if any(ungu(c) for c in aksen):
        catat("MAYOR", "Ada warna ungu/violet (" + ", ".join("#" + c for c in aksen if ungu(c)) + "). Palet khas AI; ganti kecuali memang identitas yang diminta.")
    if maks_slide and len(slides) > maks_slide:
        catat("KRITIS", f"{len(slides)} slide, melebihi batas lomba {maks_slide}.")
    if durasi and len(slides) > durasi * 1.6 + 1:
        catat("MAYOR", f"{len(slides)} slide untuk {durasi} menit. Patokan sekitar 1,2–1,5 slide per menit.")
    return temuan


def gaya(path):
    from pptx import Presentation
    from pptx.util import Emu
    prs = Presentation(str(path))
    tema = font_tema(path)
    slides = list(prs.slides)
    data = [info_slide(s, tema) for s in slides]
    fonts, warna, ukuran, tata = Counter(), Counter(), Counter(), Counter()
    for d in data:
        fonts.update(d["fonts"])
        warna.update(d["warna"])
        ukuran.update(d["ukuran"])
        tata[d["tata_letak"]] += 1
    lebar, tinggi = Emu(prs.slide_width).cm, Emu(prs.slide_height).cm
    rasio = "16:9" if abs(lebar / tinggi - 16 / 9) < 0.05 else "4:3" if abs(lebar / tinggi - 4 / 3) < 0.05 else f"{lebar:.1f}×{tinggi:.1f} cm"
    kata = [d["kata"] for d in data] or [0]
    baris = [
        f"# Gaya PPT contoh: {Path(path).name}",
        "",
        "Ringkasan otomatis dari `tools/cek_pptx.py gaya`. Yang ditiru gayanya, bukan isi, logo, atau identitasnya.",
        "",
        f"- Ukuran slide: {rasio}; jumlah slide: {len(slides)}",
        f"- Font tema: judul {tema.get('major', '?')}, isi {tema.get('minor', '?')}",
        "- Font yang dipakai: " + (", ".join(f"{f} ({n})" for f, n in fonts.most_common(5)) or "mengikuti tema"),
        "- Warna yang dipakai: " + (", ".join(f"#{c} ({n})" for c, n in warna.most_common(8)) or "mengikuti tema"),
        "- Ukuran huruf yang ditulis eksplisit: " + (", ".join(f"{u:g} pt ({n})" for u, n in sorted(ukuran.items(), reverse=True)[:8]) or "mengikuti tema"),
        f"- Kata per slide: rata-rata {sum(kata) / len(kata):.0f}, terbanyak {max(kata)}",
        f"- Slide bergambar: {sum(1 for d in data if d['gambar'])} dari {len(slides)}; slide bergradasi: {sum(1 for d in data if d['grad'])}",
        "- Tata letak: " + ", ".join(f"{t} ({n})" for t, n in tata.most_common()),
        "",
        "## Per slide",
        "| # | Judul | Kata | Butir | Gambar | Tata letak |",
        "|---|---|---|---|---|---|",
    ]
    for i, d in enumerate(data, 1):
        baris.append(f"| {i} | {d['judul'][:50].replace('|', '/')} | {d['kata']} | {d['butir']} | {d['gambar']} | {d['tata_letak']} |")
    return "\n".join(baris) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="perintah", required=True)
    a1 = sub.add_parser("cek")
    a1.add_argument("pptx")
    a1.add_argument("--durasi", type=float, help="durasi presentasi (menit)")
    a1.add_argument("--maks-slide", type=int, help="batas jumlah slide dari aturan lomba")
    a2 = sub.add_parser("gaya")
    a2.add_argument("pptx")
    a2.add_argument("--out", help="simpan ringkasan ke file .md")
    a = ap.parse_args()
    try:
        import pptx  # noqa: F401
    except ImportError:
        sys.exit("python-pptx belum terpasang. Jalankan: pip install python-pptx")
    if not Path(a.pptx).exists():
        sys.exit(f"File tidak ditemukan: {a.pptx}")
    if a.perintah == "gaya":
        hasil = gaya(a.pptx)
        if a.out:
            Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            Path(a.out).write_text(hasil, encoding="utf-8")
            print(f"Tersimpan: {a.out}")
        else:
            print(hasil)
        return
    temuan = cek(a.pptx, a.durasi, a.maks_slide)
    urutan = {"KRITIS": 0, "MAYOR": 1, "MINOR": 2, "INFO": 3}
    if not [t for t in temuan if t[0] != "INFO"]:
        print("✅ Tidak ada tanda slide buatan AI.")
    for tingkat, pesan in sorted(temuan, key=lambda x: urutan[x[0]]):
        print(f"[{tingkat}] {pesan}")
    if any(t in ("KRITIS", "MAYOR") for t, _ in temuan):
        sys.exit(1)


if __name__ == "__main__":
    main()
