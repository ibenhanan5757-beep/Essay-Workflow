#!/usr/bin/env python3
"""Ubah naskah Markdown jadi DOCX (dan PDF) sesuai profil format lomba.

Pakai:
    python tools/build_docx.py lomba/<nama>/draf/final.md --profil lomba/<nama> --out lomba/<nama>/kirim/naskah.docx [--pdf]

Markdown yang didukung (sengaja sederhana, sesuai kebutuhan esai):
    # Judul                -> judul esai (ukuran & tebal dari profil)
    ## Subjudul            -> subjudul bagian (opsional; boleh tidak dipakai)
    ### Sub-subjudul       -> sub-subjudul (tebal, ukuran isi)
    paragraf biasa         -> paragraf justify, indent baris pertama dari profil
    **tebal**, *miring*    -> format inline
    - butir / 1. butir     -> daftar berbutir / bernomor
    ## Daftar Pustaka      -> setiap baris/butir jadi satu entri dengan hanging indent (APA)
    ## Lampiran            -> mulai di halaman baru; setiap "**Lampiran N.**" berikutnya juga di halaman baru
    ![keterangan](path)    -> gambar; keterangan dan baris teks sesudahnya (mis. "*Gambar 1. ...*") ikut dicetak
    | tabel | markdown |   -> tabel sederhana (baris pemisah |---|:-:| diabaikan)
    <!-- komentar -->      -> diabaikan

Build ditolak kalau masih ada penanda [PERLU ...], TODO, XXX, atau ?? (pakai --paksa untuk draf uji).
Metadata DOCX (penulis, terakhir diubah oleh) dikosongkan supaya identitas tidak bocor.

Tampilan dibuat seperti naskah terbitan (lihat workflow/06 § Tampilan naskah profesional):
judul bagian memakai gaya Heading Word (hitam, font naskah, tidak terpisah dari paragraf berikutnya),
tabel bergaya tiga garis, keterangan "Tabel N." di atas tabel dan "Gambar N."/"Sumber:" dengan
huruf lebih kecil, kontrol baris janda/yatim, dan lebar gambar seragam (`lebar_gambar_cm`, dengan
tinggi paling banyak `tinggi_gambar_maks_cm`).

Butuh: pip install python-docx. PDF butuh LibreOffice (soffice) atau Microsoft Word (pip install docx2pdf).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):  # Windows: output yang di-pipe jatuh ke cp1252
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
except ImportError:
    sys.exit("python-docx belum terpasang. Jalankan: pip install python-docx")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cek_naskah import penanda_belum_beres  # noqa: E402

PROFIL_DEFAULT = {
    "kertas": "A4",
    "font": "Times New Roman",
    "ukuran_font": 12,
    "spasi": 1.5,
    "margin_cm": {"kiri": 4, "kanan": 3, "atas": 3, "bawah": 3},
    "rata": "justify",
    "indent_paragraf_cm": 1.0,
    "spasi_antar_paragraf_pt": 0,
    "judul": {"ukuran": 14, "tebal": True, "rata": "center"},
    "subjudul": {"ukuran": 12, "tebal": True, "rata": "left"},
    "nomor_halaman": "kanan_bawah",
    "gambar_hanya_di_lampiran": True,
    "judul_bagian_pustaka": ["daftar pustaka", "referensi", "daftar referensi"],
    "judul_bagian_lampiran": ["lampiran"],
    "lebar_gambar_cm": 14,
    "tinggi_gambar_maks_cm": 10,
}

RATA = {
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
}
KERTAS = {
    "a4": (21.0, 29.7),
    "letter": (21.59, 27.94),
    "f4": (21.5, 33.0),      # F4/Folio Indonesia
    "folio": (21.5, 33.0),
    "legal": (21.59, 35.56),
}
NOMOR = {  # posisi nomor halaman -> (header/footer, perataan)
    "kanan_bawah": ("footer", WD_ALIGN_PARAGRAPH.RIGHT),
    "tengah_bawah": ("footer", WD_ALIGN_PARAGRAPH.CENTER),
    "kiri_bawah": ("footer", WD_ALIGN_PARAGRAPH.LEFT),
    "kanan_atas": ("header", WD_ALIGN_PARAGRAPH.RIGHT),
    "tengah_atas": ("header", WD_ALIGN_PARAGRAPH.CENTER),
    "kiri_atas": ("header", WD_ALIGN_PARAGRAPH.LEFT),
}
BUTIR = re.compile(r"^\s*(?:([-*+])|(\d+)[.)])\s+(.*)$")
KETERANGAN = re.compile(r"^[*_]{0,2}(?:(?:Tabel|Gambar|Grafik|Diagram)\s+\d+\s*[.:]|Sumber\s*:|Catatan\s*:)", re.I)


def muat_profil(path):
    """Profil default ditimpa profil lomba. Nilai null berarti 'tidak diatur lomba' -> pakai default."""
    profil = json.loads(json.dumps(PROFIL_DEFAULT))
    if path:
        if Path(path).is_dir():
            path = Path(path) / "profil.json"
        data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
        for k, v in data.items():
            if k.startswith("_") or v is None:
                continue
            if isinstance(v, dict) and isinstance(profil.get(k), dict):
                profil[k].update({kk: vv for kk, vv in v.items() if vv is not None})
            else:
                profil[k] = v
    for k in ("judul_bagian_pustaka", "judul_bagian_lampiran"):
        profil[k] = [s.strip().lower() for s in profil[k]]
    if str(profil["kertas"]).lower() not in KERTAS:
        sys.exit(f"Kertas '{profil['kertas']}' tidak dikenal. Pilihan: {', '.join(KERTAS)}.")
    if profil.get("nomor_halaman") and profil["nomor_halaman"] not in NOMOR:
        sys.exit(f"nomor_halaman '{profil['nomor_halaman']}' tidak dikenal. Pilihan: {', '.join(NOMOR)}, atau null.")
    return profil


def set_font(run, profil, ukuran=None, tebal=None, miring=None):
    run.font.name = profil["font"]
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), profil["font"])
    run.font.size = Pt(ukuran or profil["ukuran_font"])
    if tebal is not None:
        run.bold = tebal
    if miring is not None:
        run.italic = miring


def tambah_inline(par, teks, profil, ukuran=None, tebal_dasar=False, miring_dasar=False):
    # **tebal** dan *miring*
    for bagian in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", teks):
        if not bagian:
            continue
        if bagian.startswith("**") and bagian.endswith("**"):
            set_font(par.add_run(bagian[2:-2]), profil, ukuran, tebal=True, miring=miring_dasar)
        elif bagian.startswith("*") and bagian.endswith("*") and len(bagian) > 2:
            set_font(par.add_run(bagian[1:-1]), profil, ukuran, tebal=tebal_dasar, miring=not miring_dasar)
        else:
            set_font(par.add_run(bagian), profil, ukuran, tebal=tebal_dasar, miring=miring_dasar)


def format_paragraf(par, profil, rata=None, indent=True, hanging=False):
    pf = par.paragraph_format
    pf.alignment = RATA[rata or profil["rata"]]
    pf.line_spacing = profil["spasi"]
    pf.space_before = Pt(0)
    pf.space_after = Pt(profil["spasi_antar_paragraf_pt"])
    if hanging:
        pf.left_indent = Cm(1.27)
        pf.first_line_indent = Cm(-1.27)
    elif indent:
        pf.first_line_indent = Cm(profil["indent_paragraf_cm"])


def siapkan_gaya_heading(doc, profil):
    """Heading 1–3 bawaan Word (supaya muncul di panel navigasi), tapi hitam, font naskah, tanpa warna tema."""
    ukuran = {1: profil["subjudul"]["ukuran"], 2: profil["ukuran_font"], 3: profil["ukuran_font"]}
    for level, uk in ukuran.items():
        g = doc.styles[f"Heading {level}"]
        g.font.name = profil["font"]
        rfonts = g.element.get_or_add_rPr().get_or_add_rFonts()
        for atribut in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            rfonts.set(qn(atribut), profil["font"])
        for atribut in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            rfonts.attrib.pop(qn(atribut), None)
        g.font.size = Pt(uk)
        g.font.bold = profil["subjudul"]["tebal"] if level == 1 else True
        g.font.italic = level == 3
        g.font.color.rgb = RGBColor(0, 0, 0)
        pf = g.paragraph_format
        pf.keep_with_next = True
        pf.space_before = Pt(6)
        pf.space_after = Pt(0)


def tambah_nomor_halaman(section, posisi):
    tempat, rata = NOMOR[posisi]
    wadah = section.header if tempat == "header" else section.footer
    par = wadah.paragraphs[0] if wadah.paragraphs else wadah.add_paragraph()
    par.alignment = rata
    run = par.add_run()
    for tag, teks in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = teks
        run._r.append(el)


def baris_pemisah(sel):
    return all(re.fullmatch(r"\s*:?-+:?\s*", c) for c in sel) and any("-" in c for c in sel)


def garis(elemen, sisi, ada=True):
    """Garis tipis hitam (atau tanpa garis) di satu sisi tabel/sel."""
    el = OxmlElement(f"w:{sisi}")
    el.set(qn("w:val"), "single" if ada else "nil")
    if ada:
        el.set(qn("w:sz"), "6")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
    elemen.append(el)


def tambah_tabel(doc, baris, profil):
    """Tabel gaya tiga garis: garis atas, garis di bawah kepala tabel, garis bawah. Tanpa garis tegak."""
    # pemisah kolom = "|" yang tidak di-escape; "\|" dicetak sebagai "|" (mis. tanda turus)
    sel = [[c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", b.strip().strip("|"))] for b in baris if b.strip().startswith("|")]
    sel = [b for b in sel if not baris_pemisah(b)]
    if not sel:
        return
    kolom = max(len(b) for b in sel)
    tabel = doc.add_table(rows=len(sel), cols=kolom)
    tabel.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblpr = tabel._tbl.tblPr
    batas = OxmlElement("w:tblBorders")
    for sisi, ada in (("top", True), ("left", False), ("bottom", True), ("right", False), ("insideH", False), ("insideV", False)):
        garis(batas, sisi, ada)
    tblpr.append(batas)
    for i, b in enumerate(sel):
        for j in range(kolom):
            sel_tabel = tabel.cell(i, j)
            if i == 0 and len(sel) > 1:
                tcb = OxmlElement("w:tcBorders")
                garis(tcb, "bottom")
                sel_tabel._tc.get_or_add_tcPr().append(tcb)
            par = sel_tabel.paragraphs[0]
            par.paragraph_format.line_spacing = 1.0
            par.paragraph_format.space_before = Pt(2)
            par.paragraph_format.space_after = Pt(2)
            if i == 0:
                par.paragraph_format.keep_with_next = True
            tambah_inline(par, b[j] if j < len(b) else "", profil, ukuran=profil["ukuran_font"] - 1, tebal_dasar=(i == 0))
            if i > 0 and re.fullmatch(r"[\d.,%|\\ -]+|ya|tidak", (b[j] if j < len(b) else "").strip()):
                par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # lebar kolom mengikuti panjang isi (kata terpanjang dan rata-rata teks), supaya kolom nama obat tidak terlipat
    m = profil.get("margin_cm", {})
    lebar_teks = profil.get("lebar_kertas_cm", 21.0) - m.get("kiri", 3) - m.get("kanan", 3)
    bobot = []
    for j in range(kolom):
        isi = [re.sub(r"[*_]", "", b[j]) for b in sel if j < len(b)]
        kata = max((len(w) for t in isi for w in t.split()), default=1)
        panjang = max((len(t) for t in isi[1:]), default=0) if len(isi) > 1 else len(isi[0])
        bobot.append(max(kata, min(panjang, 28), 6))
    total = sum(bobot)
    tabel.autofit = False
    tata = OxmlElement("w:tblLayout")
    tata.set(qn("w:type"), "fixed")
    tblpr.append(tata)
    grid = tabel._tbl.tblGrid.findall(qn("w:gridCol"))
    for j in range(kolom):
        lebar = Cm(lebar_teks * bobot[j] / total)
        tabel.columns[j].width = lebar
        if j < len(grid):
            grid[j].set(qn("w:w"), str(int(lebar.twips)))
        for i in range(len(sel)):
            tabel.cell(i, j).width = lebar
    # jarak sesudah tabel agar teks berikutnya tidak menempel
    jarak = doc.add_paragraph()
    jarak.paragraph_format.space_after = Pt(0)
    jarak.paragraph_format.line_spacing = 1.0
    jarak.add_run().font.size = Pt(6)


def ukuran_gambar(path, lebar_maks, profil):
    """Lebar seragam, tapi gambar tinggi (diagram menurun) dikecilkan supaya tidak memakan satu halaman."""
    try:
        from docx.image.image import Image as GambarDocx
        g = GambarDocx.from_file(str(path))
        rasio = g.px_height / g.px_width
    except Exception:
        return lebar_maks
    tinggi_maks = float(profil.get("tinggi_gambar_maks_cm") or 10)
    return min(lebar_maks, tinggi_maks / rasio) if rasio > 0 else lebar_maks


def tambah_keterangan(doc, teks, profil):
    """Keterangan gambar/tabel/sumber: huruf lebih kecil, tanpa indent, tidak terpisah dari tabel di bawahnya."""
    cap = doc.add_paragraph()
    tambah_inline(cap, " ".join(teks.split()), profil, profil["ukuran_font"] - 2)
    catatan = re.match(r"^[*_]{0,2}Catatan\s*:", teks.strip(), re.I)
    format_paragraf(cap, profil, rata="justify" if catatan else "center", indent=False)
    cap.paragraph_format.line_spacing = 1.0
    cap.paragraph_format.space_after = Pt(6)
    if re.match(r"^\*{0,2}(Tabel|Gambar)\b", teks.strip(), re.I):
        cap.paragraph_format.keep_with_next = True
        cap.paragraph_format.space_after = Pt(2)
    return cap


def entri_pustaka(baris):
    """Satu entri per baris/butir; baris berawalan spasi/tab adalah lanjutan entri sebelumnya."""
    entri = []
    for b in baris:
        if not b.strip():
            continue
        if entri and b[:1] in (" ", "\t") and not BUTIR.match(b):
            entri[-1] += " " + b.strip()
        else:
            m = BUTIR.match(b)
            entri.append((m.group(3) if m else b).strip())
    return entri


def kosongkan_metadata(doc):
    cp = doc.core_properties
    cp.author = ""
    cp.last_modified_by = ""
    cp.comments = ""
    cp.keywords = ""
    cp.subject = ""


def build(md_path, profil, out_path):
    teks = Path(md_path).read_text(encoding="utf-8-sig")
    teks = re.sub(r"<!--.*?-->", "", teks, flags=re.S)
    doc = Document()
    kosongkan_metadata(doc)
    sec = doc.sections[0]
    lebar, tinggi = KERTAS[str(profil["kertas"]).lower()]
    sec.page_width, sec.page_height = Cm(lebar), Cm(tinggi)
    m = profil["margin_cm"]
    sec.left_margin, sec.right_margin = Cm(m["kiri"]), Cm(m["kanan"])
    sec.top_margin, sec.bottom_margin = Cm(m["atas"]), Cm(m["bawah"])
    if profil.get("nomor_halaman"):
        tambah_nomor_halaman(sec, profil["nomor_halaman"])

    gaya = doc.styles["Normal"]
    gaya.font.name = profil["font"]
    gaya.font.size = Pt(profil["ukuran_font"])
    gaya.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), profil["font"])
    gaya.paragraph_format.widow_control = True
    siapkan_gaya_heading(doc, profil)
    lebar_teks = lebar - m["kiri"] - m["kanan"]
    lebar_gambar = min(float(profil.get("lebar_gambar_cm") or 14), lebar_teks)

    mode = "isi"  # isi | pustaka | lampiran
    jumlah_lampiran = 0  # setiap "Lampiran N." sesudah yang pertama mulai di halaman baru
    peringatan = []
    antrean = re.split(r"\n\s*\n", teks.strip())
    i = 0
    while i < len(antrean):
        b = antrean[i]
        i += 1
        baris = [l for l in b.splitlines() if l.strip()]
        if not baris:
            continue
        pertama = baris[0].strip()
        sisa = "\n".join(baris[1:]).strip()

        if pertama.startswith("# "):
            par = doc.add_paragraph()
            tambah_inline(par, pertama[2:].strip(), profil, profil["judul"]["ukuran"], profil["judul"]["tebal"])
            format_paragraf(par, profil, rata=profil["judul"]["rata"], indent=False)
            par.paragraph_format.keep_with_next = True
            if sisa:
                antrean.insert(i, sisa)
            continue
        if pertama.startswith("## "):
            judul = pertama[3:].strip()
            low = judul.rstrip(":").strip().lower()
            if low in profil["judul_bagian_lampiran"]:
                mode = "lampiran"
                doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            elif low in profil["judul_bagian_pustaka"]:
                mode = "pustaka"
            elif mode == "pustaka":
                mode = "isi"
            par = doc.add_paragraph(style="Heading 1")
            tambah_inline(par, judul, profil, profil["subjudul"]["ukuran"], profil["subjudul"]["tebal"])
            format_paragraf(par, profil, rata=profil["subjudul"]["rata"], indent=False)
            par.paragraph_format.keep_with_next = True
            if sisa:
                antrean.insert(i, sisa)
            continue
        if re.match(r"^#{3,6}\s", pertama):
            par = doc.add_paragraph(style="Heading 2")
            tambah_inline(par, re.sub(r"^#{3,6}\s+", "", pertama), profil, profil["ukuran_font"], True)
            format_paragraf(par, profil, rata="left", indent=False)
            par.paragraph_format.keep_with_next = True
            if sisa:
                antrean.insert(i, sisa)
            continue
        if pertama.startswith("|"):
            tabel = [l for l in baris if l.strip().startswith("|")]
            tambah_tabel(doc, tabel, profil)
            if mode == "isi" and profil["gambar_hanya_di_lampiran"]:
                peringatan.append("Tabel ditemukan di luar Lampiran; profil lomba meminta tabel/gambar di lampiran.")
            lain = "\n".join(l for l in baris if not l.strip().startswith("|")).strip()
            if lain:
                antrean.insert(i, lain)
            continue
        gbr = re.fullmatch(r"!\[(.*?)\]\((.*?)\)", pertama)
        if gbr:
            if mode == "isi" and profil["gambar_hanya_di_lampiran"]:
                peringatan.append(f"Gambar '{gbr.group(2)}' ada di luar Lampiran.")
            path = (Path(md_path).parent / gbr.group(2)).resolve()
            if path.exists():
                doc.add_picture(str(path), width=Cm(ukuran_gambar(path, lebar_gambar, profil)))
                doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
                doc.paragraphs[-1].paragraph_format.keep_with_next = True
            else:
                peringatan.append(f"File gambar tidak ditemukan: {path}")
            # keterangan: alt-text kalau tidak ada baris keterangan di bawahnya
            ket = sisa.splitlines() if sisa else []
            alt = gbr.group(1).strip()
            if alt and (not ket or (KETERANGAN.match(alt) and not re.match(r"^[*_]{0,2}(Gambar|Grafik|Diagram)\b", ket[0].strip(), re.I))):
                ket.insert(0, alt)  # alt-text "Gambar N. ..." + baris "Sumber: ..." di bawah gambar
            for baris_ket in ket:
                tambah_keterangan(doc, baris_ket, profil)
            continue
        if mode == "lampiran" and re.match(r"^[*_]{0,2}Lampiran\s+\d+", pertama):
            if jumlah_lampiran:
                doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            jumlah_lampiran += 1
        if KETERANGAN.match(pertama) and mode != "pustaka" and len(pertama) < 300:
            # "Tabel 1. ..." boleh langsung diikuti baris tabel tanpa baris kosong
            tambah_keterangan(doc, pertama, profil)
            if sisa:
                antrean.insert(i, sisa)
            continue
        if mode == "pustaka":
            for e in entri_pustaka(b.splitlines()):
                par = doc.add_paragraph()
                tambah_inline(par, e, profil)
                format_paragraf(par, profil, rata="left", indent=False, hanging=True)
            continue
        if BUTIR.match(baris[0]):
            butir = []
            for l in baris:
                mb = BUTIR.match(l)
                if mb:
                    butir.append([mb.group(1) is None, mb.group(3).strip()])
                elif butir:
                    butir[-1][1] += " " + l.strip()
            for bernomor, isi_butir in butir:
                par = doc.add_paragraph(style="List Number" if bernomor else "List Bullet")
                tambah_inline(par, isi_butir, profil)
                format_paragraf(par, profil, rata="left", indent=False)
            continue
        isi = " ".join(l.strip() for l in baris)
        par = doc.add_paragraph()
        tambah_inline(par, isi, profil)
        format_paragraf(par, profil, indent=(mode == "isi"))

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)
    return peringatan


def cari_soffice():
    ada = shutil.which("soffice") or shutil.which("libreoffice")
    if ada:
        return ada
    for dasar in (os.environ.get("ProgramFiles", r"C:\Program Files"), os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")):
        p = Path(dasar) / "LibreOffice" / "program" / "soffice.exe"
        if p.exists():
            return str(p)
    mac = Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")
    return str(mac) if mac.exists() else None


def ke_pdf(docx_path):
    out_dir = str(Path(docx_path).parent)
    soffice = cari_soffice()
    if soffice:
        try:
            subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", out_dir, str(docx_path)],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
            return Path(docx_path).with_suffix(".pdf")
        except (subprocess.SubprocessError, OSError) as ex:
            print(f"PDF via LibreOffice gagal ({ex}). Mencoba MS Word...", file=sys.stderr)
    try:
        from docx2pdf import convert  # Windows/Mac dengan Microsoft Word
        convert(str(docx_path))
        return Path(docx_path).with_suffix(".pdf")
    except Exception:
        pass
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        in_p = os.path.abspath(docx_path)
        out_p = os.path.abspath(str(Path(docx_path).with_suffix(".pdf")))
        doc = word.Documents.Open(in_p)
        doc.SaveAs(out_p, FileFormat=17)
        doc.Close()
        word.Quit()
        return Path(out_p)
    except Exception as ex:
        print(f"PDF tidak dibuat: MS Word gagal mengonversi ({ex}). Buka DOCX di Word lalu Save As PDF.", file=sys.stderr)
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown")
    ap.add_argument("--profil", help="folder lomba (berisi profil.json) atau file JSON profil")
    ap.add_argument("--out", required=True, help="path .docx keluaran")
    ap.add_argument("--pdf", action="store_true", help="buat PDF juga")
    ap.add_argument("--paksa", action="store_true", help="tetap build walau masih ada penanda [PERLU ...]/TODO (hanya untuk uji)")
    a = ap.parse_args()
    try:
        profil = muat_profil(a.profil)
        teks = Path(a.markdown).read_text(encoding="utf-8-sig")
    except (OSError, ValueError) as ex:
        sys.exit(f"Gagal membaca file: {ex}")
    sisa = penanda_belum_beres(re.sub(r"<!--.*?-->", "", teks, flags=re.S))
    if sisa:
        daftar = ", ".join(f"{'[PERLU ...]' if p.startswith(chr(92) + '[PERLU') else p} {k}x" for p, k in sisa)
        if not a.paksa:
            sys.exit(f"Build ditolak: masih ada penanda belum beres ({daftar}). Bereskan dulu, atau pakai --paksa untuk draf uji.")
        print(f"PERINGATAN: --paksa dipakai, penanda belum beres: {daftar}")
    try:
        peringatan = build(a.markdown, profil, a.out)
    except PermissionError:
        sys.exit(f"Tidak bisa menulis {a.out}. Tutup file itu di Word lalu ulangi.")
    for p in peringatan:
        print("PERINGATAN:", p)
    print("DOCX:", a.out)
    if a.pdf:
        pdf = ke_pdf(a.out)
        if pdf:
            print("PDF:", pdf)


if __name__ == "__main__":
    main()
