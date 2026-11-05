#!/usr/bin/env python3
"""Periksa file Word hasil build: apakah formatnya terlihat seperti naskah lomba yang rapi, bukan "format AI".

Pakai:
    python tools/cek_docx.py "<L>/kirim/<nama file>.docx" --profil <L>

Yang diperiksa (semua dari isi file, tidak ada yang dikirim ke internet):
    - font dan ukuran yang tidak sesuai profil lomba (termasuk di tabel)
    - teks berwarna, stabilo, garis bawah, huruf kapital semua yang panjang
    - emoji dan simbol dekoratif, tanda pisah panjang (—) yang berlebihan
    - huruf tebal yang terlalu banyak di badan teks
    - paragraf kosong berturut-turut (jarak dibuat dengan Enter, bukan pengaturan spasi)
    - gambar dan tabel tanpa keterangan "Gambar N." / "Tabel N.", nomor yang loncat, keterangan tanpa sumber
    - gambar/tabel di badan teks padahal profil bilang hanya boleh di lampiran
    - metadata dokumen (penulis, judul) yang bisa membocorkan identitas
Butuh `pip install python-docx`.
"""
import argparse
import json
import re
import sys
from pathlib import Path

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⬆↔-⇿✅❌✔✖]")
KETERANGAN = re.compile(r"^(Gambar|Tabel|Grafik|Diagram)\s+(\d+)[\.\:]", re.I)


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


def font_run(run, gaya_default):
    nama = run.font.name or (run.style.font.name if run.style is not None else None) or gaya_default
    rpr = run._element.rPr
    if rpr is not None and rpr.rFonts is not None:
        from docx.oxml.ns import qn
        nama = rpr.rFonts.get(qn("w:ascii")) or nama
    return nama


def semua_paragraf(doc):
    for p in doc.paragraphs:
        yield p, False
    for t in doc.tables:
        for baris in t.rows:
            for sel in baris.cells:
                for p in sel.paragraphs:
                    yield p, True


def seperti_judul(p):
    """Judul/subjudul/keterangan tidak dihitung sebagai badan teks: gaya Heading, atau baris pendek yang seluruhnya tebal."""
    if p.style.name.lower().startswith(("heading", "title", "judul", "caption")) or KETERANGAN.match(p.text.strip()):
        return True
    isi = [r for r in p.runs if r.text.strip()]
    return len(p.text.strip()) <= 120 and bool(isi) and all(r.bold for r in isi)


def punya_gambar(p):
    return bool(p._element.xpath(".//*[local-name()='drawing' or local-name()='pict']"))


def periksa(jalur, profil):
    from docx import Document
    from docx.shared import Pt
    doc = Document(jalur)
    temuan = []

    def catat(tingkat, pesan):
        temuan.append((tingkat, pesan))

    normal = doc.styles["Normal"].font
    font_profil = profil.get("font") or normal.name
    ukuran_ok = {profil.get("ukuran_font", 12)}
    for kunci, bawaan in (("judul", 14), ("subjudul", 12)):  # bawaan sama dengan build_docx.py
        isi = profil.get(kunci) if isinstance(profil.get(kunci), dict) else {}
        ukuran_ok.add(isi.get("ukuran") or bawaan)
    ukuran_ok |= {9, 10, 11}  # keterangan gambar, isi tabel, catatan kaki

    font_lain, ukuran_lain, berwarna, stabilo, garis_bawah, emoji = {}, {}, 0, 0, 0, set()
    tebal_huruf = total_huruf = 0
    pisah_panjang = 0
    for p, di_tabel in semua_paragraf(doc):
        for r in p.runs:
            t = r.text
            if not t.strip():
                continue
            f = font_run(r, normal.name)
            if f and font_profil and f != font_profil:
                font_lain[f] = font_lain.get(f, 0) + 1
            uk = r.font.size.pt if r.font.size else None
            if uk and uk not in ukuran_ok:
                ukuran_lain[uk] = ukuran_lain.get(uk, 0) + 1
            if r.font.color is not None and r.font.color.type is not None and r.font.color.rgb not in (None, "000000"):
                berwarna += 1
            if r.font.highlight_color:
                stabilo += 1
            if r.font.underline:
                garis_bawah += 1
            emoji |= set(EMOJI.findall(t))
            pisah_panjang += t.count("—")
            if not di_tabel and not seperti_judul(p):
                total_huruf += len(t)
                if r.bold:
                    tebal_huruf += len(t)

    if font_lain:
        catat("MAYOR", f"Font selain {font_profil}: " + ", ".join(f"{k} ({v} potong teks)" for k, v in font_lain.items()))
    if ukuran_lain:
        catat("MINOR", "Ukuran huruf di luar yang wajar untuk profil ini: " + ", ".join(f"{k:g} pt ({v}x)" for k, v in ukuran_lain.items()))
    if berwarna:
        catat("MAYOR", f"{berwarna} potong teks berwarna. Naskah lomba memakai teks hitam saja.")
    if stabilo:
        catat("MAYOR", f"{stabilo} potong teks distabilo.")
    if garis_bawah:
        catat("MINOR", f"{garis_bawah} potong teks bergaris bawah. Untuk penekanan pakai miring, atau tidak sama sekali.")
    if emoji:
        catat("KRITIS", "Emoji/simbol dekoratif ditemukan: " + " ".join(sorted(emoji)))
    if total_huruf and tebal_huruf / total_huruf > 0.03:
        catat("MAYOR", f"{tebal_huruf / total_huruf:.0%} huruf badan teks dicetak tebal. Esai profesional hampir tidak memakai tebal di paragraf.")
    if pisah_panjang > 2:
        catat("MINOR", f"Tanda pisah panjang (—) muncul {pisah_panjang} kali. Ini salah satu ciri tulisan AI; ganti dengan koma, titik dua, atau kalimat baru.")

    # Paragraf kosong berturut-turut dan huruf kapital semua
    kosong = maks_kosong = 0
    for p in doc.paragraphs:
        if not p.text.strip() and not punya_gambar(p) and not p._element.xpath(".//*[local-name()='br'][@*[local-name()='type']='page']"):
            kosong += 1
            maks_kosong = max(maks_kosong, kosong)
        else:
            kosong = 0
        teks = p.text.strip()
        if len(teks) > 40 and teks.isupper():
            catat("MINOR", f"Paragraf huruf kapital semua: \"{teks[:50]}...\"")
    if maks_kosong >= 2:
        catat("MINOR", f"Ada {maks_kosong} paragraf kosong berturut-turut. Jarak sebaiknya dari spasi paragraf, bukan Enter berulang.")

    # Gambar, tabel, keterangan
    paragraf = doc.paragraphs
    teks_semua = [p.text.strip() for p in paragraf]
    lampiran_mulai = next((i for i, t in enumerate(teks_semua) if t.lower() in [x.lower() for x in profil.get("judul_bagian_lampiran", ["lampiran"])]), None)
    nomor = {"gambar": [], "tabel": []}
    for i, t in enumerate(teks_semua):
        m = KETERANGAN.match(t)
        if m:
            jenis = "tabel" if m.group(1).lower() == "tabel" else "gambar"
            nomor[jenis].append(int(m.group(2)))
            if jenis == "gambar" and not re.search(r"sumber|dok\.|diolah|ilustrasi|rancangan penulis|desain penulis", t + " " + (teks_semua[i + 1] if i + 1 < len(teks_semua) else ""), re.I):
                catat("MINOR", f"Keterangan \"{t[:40]}\" tanpa sumber. Tulis \"Sumber: ...\" atau \"Ilustrasi konsep (rancangan penulis)\".")
    for i, p in enumerate(paragraf):
        if punya_gambar(p):
            dekat = teks_semua[max(0, i - 1): i + 3]
            if not any(KETERANGAN.match(x) for x in dekat):
                catat("MAYOR", f"Gambar di paragraf ke-{i + 1} tanpa keterangan \"Gambar N. ...\".")
            if profil.get("gambar_hanya_di_lampiran") and (lampiran_mulai is None or i < lampiran_mulai):
                catat("KRITIS", f"Gambar di badan teks (paragraf ke-{i + 1}), padahal aturan lomba: gambar hanya di lampiran.")
    body = doc.element.body
    for idx, el in enumerate(body.iterchildren()):
        if el.tag.endswith("}tbl"):
            sebelum = el.getprevious()
            teks_sebelum = "".join(sebelum.itertext()).strip() if sebelum is not None else ""
            if not KETERANGAN.match(teks_sebelum):
                catat("MINOR", f"Tabel tanpa keterangan \"Tabel N. ...\" tepat di atasnya (sebelumnya: \"{teks_sebelum[:30]}\").")
    for jenis, daftar in nomor.items():
        if daftar and daftar != list(range(1, len(daftar) + 1)):
            catat("MAYOR", f"Nomor {jenis} tidak urut: {daftar}")

    # Metadata
    cp = doc.core_properties
    for kolom in ("author", "last_modified_by", "title", "subject", "keywords", "comments"):
        nilai = getattr(cp, kolom, None)
        if nilai and str(nilai).strip() and str(nilai).strip().lower() not in ("python-docx", ""):
            catat("INFO", f"Metadata {kolom} = \"{nilai}\". Kosongkan kalau lomba meminta naskah anonim.")
    return temuan


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx")
    ap.add_argument("--profil", help="folder lomba (berisi profil.json) atau file JSON profil")
    a = ap.parse_args()
    try:
        import docx  # noqa: F401
    except ImportError:
        sys.exit("python-docx belum terpasang. Jalankan: pip install python-docx")
    temuan = periksa(a.docx, muat_profil(a.profil))
    urutan = {"KRITIS": 0, "MAYOR": 1, "MINOR": 2, "INFO": 3}
    if not temuan:
        print("✅ Format bersih: tidak ada temuan.")
        return
    for tingkat, pesan in sorted(temuan, key=lambda x: urutan[x[0]]):
        print(f"[{tingkat}] {pesan}")
    if any(t in ("KRITIS", "MAYOR") for t, _ in temuan):
        sys.exit(1)


if __name__ == "__main__":
    main()
