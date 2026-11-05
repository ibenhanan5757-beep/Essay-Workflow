"""Ubah data/lomba.json menjadi Excel + CSV (+ ZIP berisi poster).

Pemakaian:
  python -I build_sheet.py <lomba.json> <folder_output> [--posters <folder_poster>]

Kolom "Aturan AI" diisi dari field `ai` (salah satu AI_KATEGORI) dan "Bukti Aturan AI" dari `ai_bukti`
(kutipan + asalnya: caption / poster / juknis hal. N). Kalau `ai` kosong, ditulis "Belum dicek".

Butuh: openpyxl
"""
import csv
import json
import os
import sys
import zipfile
from datetime import date

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

POST_URL = "https://www.instagram.com/p/{}/"
HEADERS = ["No", "Nama Lomba", "Lombanya Apa", "Jenjang", "Deadline Daftar", "Status", "Sisa Hari",
           "Aturan AI", "Bukti Aturan AI", "Keterangan Deadline", "Link Juknis", "Link Postingan IG", "Catatan"]
WIDTHS = [5, 42, 38, 24, 14, 13, 9, 20, 46, 34, 48, 40, 48]
COLS = "ABCDEFGHIJKLM"
NAME = "Lomba_Bookmark_IG"

# Urutan dari paling membatasi. Lihat lomba-ig/SKILL.md § Aturan AI.
AI_KATEGORI = [
    "Dilarang",                        # juknis/poster melarang AI (generatif) dalam bentuk apa pun
    "Dibatasi",                        # boleh dengan syarat: batas % deteksi AI, wajib dicantumkan, hanya untuk alat bantu, dll.
    "Wajib pernyataan karya sendiri",  # tidak menyebut AI, tapi minta surat orisinalitas / pernyataan karya sendiri
    "Boleh",                           # tegas membolehkan
    "Tidak disebut",                   # caption, poster, DAN juknis sudah dibaca, tidak ada aturan soal AI
    "Belum dicek",                     # juknis belum dibaca (default)
]
AI_WARNA = {"Dilarang": "F4B6B6", "Dibatasi": "F8CBAD", "Wajib pernyataan karya sendiri": "FFE699",
            "Boleh": "C6EFCE"}


def load(path):
    with open(path, encoding="utf-8") as f:
        items = json.load(f)
    for it in items:
        it["_dl"] = date.fromisoformat(it["deadline"]) if it.get("deadline") else None
    items.sort(key=lambda it: (it["_dl"] is None, it["_dl"] or date(2100, 1, 1)))
    return items


def write_xlsx(items, out):
    wb = Workbook()
    ws = wb.active
    ws.title = "Lomba"
    ws.append(HEADERS)
    link = Font(color="0563C1", underline="single")
    for i, it in enumerate(items, 1):
        r = i + 1
        post = POST_URL.format(it["post"])
        ws.append([i, it["nama"], it["apa"], it["jenjang"], it["_dl"], None, None,
                   it.get("ai") or "Belum dicek", it.get("ai_bukti", ""), it.get("ket", ""),
                   it.get("juknis") or "(tidak ada di postingan)", post, it.get("catatan", "")])
        ws.cell(r, 5).number_format = "dd mmm yyyy"
        ws.cell(r, 6).value = (f'=IF(E{r}="","Cek manual",IF(E{r}<TODAY(),"Sudah tutup",'
                               f'IF(E{r}=TODAY(),"Hari ini!",IF(E{r}-TODAY()<=7,"Segera","Masih buka"))))')
        ws.cell(r, 7).value = f'=IF(E{r}="","",IF(E{r}<TODAY(),"",E{r}-TODAY()))'
        if it.get("juknis"):
            ws.cell(r, 11).hyperlink = it["juknis"]
            ws.cell(r, 11).font = link
        ws.cell(r, 12).hyperlink = post
        ws.cell(r, 12).font = link

    last = len(items) + 1
    for col, w in zip(COLS, WIDTHS):
        ws.column_dimensions[col].width = w
    thin = Side(style="thin", color="D0D0D0")
    for row in ws.iter_rows(min_row=1, max_row=last):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E78")
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:M{last}"

    # Warna kolom Aturan AI ditambahkan lebih dulu supaya menang atas warna baris (deadline)
    for kat, warna in AI_WARNA.items():
        ws.conditional_formatting.add(f"H2:H{last}", FormulaRule(
            formula=[f'$H2="{kat}"'], fill=PatternFill("solid", fgColor=warna), font=Font(bold=kat == "Dilarang")))

    rng = f"A2:M{last}"
    ws.conditional_formatting.add(rng, FormulaRule(formula=['AND($E2<>"",$E2<TODAY())'],
                                  fill=PatternFill("solid", fgColor="E7E6E6"), font=Font(color="808080")))
    ws.conditional_formatting.add(rng, FormulaRule(formula=['AND($E2<>"",$E2>=TODAY(),$E2-TODAY()<=7)'],
                                  fill=PatternFill("solid", fgColor="FFF2CC")))
    ws.conditional_formatting.add(rng, FormulaRule(formula=['$E2=""'], fill=PatternFill("solid", fgColor="FCE4D6")))

    info = wb.create_sheet("Info")
    info.append(["Dibuat", date.today().isoformat()])
    info.append(["Warna", "Kuning = deadline ≤ 7 hari; abu-abu = sudah tutup; oranye muda = deadline perlu dicek manual"])
    info.append(["Link juknis", "Sebagian dari QR poster (me-qr / get-qr / wps). Buka di HP/browser untuk diarahkan ke file juknis."])
    info.append(["Aturan AI", "Dilarang (merah) · Dibatasi: boleh dengan syarat, mis. batas % deteksi AI (oranye) · "
                 "Wajib pernyataan karya sendiri (kuning) · Boleh (hijau) · Tidak disebut: caption, poster & juknis "
                 "sudah dibaca, tidak ada aturan AI · Belum dicek: juknis belum dibaca"])
    info.append(["Penting", "Workflow esai di folder ini 100% AI. Lomba 'Dilarang' jangan dipilih; "
                 "'Dibatasi' dan 'Wajib pernyataan' dibaca dulu aturannya di juknis (tahap 0)."])
    info.append(["Catatan", "Selalu cek ulang deadline & biaya di juknis resmi sebelum mendaftar."])
    info.column_dimensions["A"].width = 14
    info.column_dimensions["B"].width = 110
    wb.save(out)


def write_csv(items, out):
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow([h for h in HEADERS if h not in ("Status", "Sisa Hari")])
        for i, it in enumerate(items, 1):
            w.writerow([i, it["nama"], it["apa"], it["jenjang"], it.get("deadline") or "",
                        it.get("ai") or "Belum dicek", it.get("ai_bukti", ""), it.get("ket", ""),
                        it.get("juknis", ""), POST_URL.format(it["post"]), it.get("catatan", "")])


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return
    src, outdir = argv[0], argv[1]
    posters = argv[argv.index("--posters") + 1] if "--posters" in argv else None
    os.makedirs(outdir, exist_ok=True)
    items = load(src)
    xlsx = os.path.join(outdir, NAME + ".xlsx")
    csvp = os.path.join(outdir, NAME + ".csv")
    write_xlsx(items, xlsx)
    write_csv(items, csvp)
    print("Excel:", xlsx)
    print("CSV  :", csvp)
    if posters:
        zp = os.path.join(outdir, NAME + "_lengkap.zip")
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(xlsx, os.path.basename(xlsx))
            z.write(csvp, os.path.basename(csvp))
            for fn in sorted(os.listdir(posters)):
                if fn.lower().endswith((".jpg", ".png", ".webp")):
                    z.write(os.path.join(posters, fn), "poster/" + fn)
        print("ZIP  :", zp)
    print(len(items), "lomba")


if __name__ == "__main__":
    main(sys.argv[1:])
