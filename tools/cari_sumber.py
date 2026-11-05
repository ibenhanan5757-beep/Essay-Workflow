#!/usr/bin/env python3
"""Cari dan verifikasi sumber ilmiah dari database publik. Tanpa instal apa pun (hanya Python 3.8+).

Perintah:
  cari "kata kunci"           Cari paper. Default: OpenAlex. Pilih database dengan --db
        --db openalex|arxiv|pubmed|europepmc|semantic|garuda|semua
                                garuda = jurnal Indonesia (termasuk tanpa DOI), kata kunci bahasa Indonesia
        --dari 2019             hanya terbit sejak tahun ini
        --n 5                   jumlah hasil per database
        --oa                    hanya yang open access (OpenAlex/Europe PMC)
  doi 10.xxxx/yyyy             Verifikasi satu DOI di Crossref + cek status retraksi di OpenAlex,
                               lalu cetak format APA 7
  cek-pustaka <L>/draf/final.md  Verifikasi semua entri di bagian "## Daftar Pustaka":
                               entri ber-DOI dicek langsung, tanpa DOI dicocokkan ke Crossref
  teks 10.xxxx/yyyy            Cari versi akses terbuka (legal) sebuah paper lewat OpenAlex (+ Unpaywall
                               kalau ESAI_EMAIL diisi) dan Europe PMC. Dengan --simpan-teks <L>/riset/teks
                               teks penuhnya diunduh dan disimpan sebagai .md (butuh pypdf untuk PDF).
  teks <link PDF>              Untuk artikel tanpa DOI (misalnya dari Garuda): unduh PDF dari link itu.
                               Dengan --simpan-teks, beri nama file lewat --nama penulis-tahun.
  fda "nama obat"              openFDA: penarikan produk (recall) dan label obat (data AS)
  uji-klinis "kata kunci"      ClinicalTrials.gov: uji klinis terdaftar

Opsi umum:
  --simpan <L>/riset/sumber.md tambahkan hasil sebagai baris tabel log sumber (status ⚠️ sampai dibuka manual)
  --email kamu@contoh.com      disarankan OpenAlex/Crossref/NCBI ("polite pool", lebih jarang dibatasi).
                               Bisa juga lewat variabel lingkungan ESAI_EMAIL.
  OPENALEX_API_KEY (variabel lingkungan, opsional): kunci gratis dari https://openalex.org/settings/api.
                               Tanpa kunci tetap jalan, tapi kuota harian OpenAlex lebih kecil.
                               Windows: setx OPENALEX_API_KEY "<kunci>" lalu buka terminal baru.
  SEMANTIC_SCHOLAR_API_KEY (opsional): kunci gratis dari https://www.semanticscholar.org/product/api.
                               Tanpa kunci, Semantic Scholar sering menolak (HTTP 429).

Catatan jujur:
  - "Ditemukan di database" berarti sumbernya ADA, bukan berarti isinya mendukung klaim esai.
    Tetap baca abstrak/isi sebelum mengutip.
  - Garuda tidak punya API resmi. `--db garuda` membaca halaman pencarian publiknya, jadi bisa berhenti
    bekerja kalau tampilan situsnya berubah (alat lalu melaporkan "tidak ada hasil", bukan hasil yang salah).
    SINTA tidak dicari; banyak jurnal SINTA sudah tertangkap lewat Garuda dan OpenAlex.
"""
import argparse
import difflib
import html
import io
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

for _s in (sys.stdout, sys.stderr):  # Windows: output yang di-pipe jatuh ke cp1252 dan crash pada emoji
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

UA = "esai-lomba-tools/1.0"
EMAIL = os.environ.get("ESAI_EMAIL", "")
OPENALEX_KEY = os.environ.get("OPENALEX_API_KEY", "")
S2_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY") or os.environ.get("S2_API_KEY", "")


# ---------------------------------------------------------------- HTTP
def _header(url, json_out=True):
    """Header permintaan: User-Agent (+ email untuk 'polite pool') dan kunci Semantic Scholar bila ada."""
    h = {"User-Agent": UA + (f" (mailto:{EMAIL})" if EMAIL else ""),
         "Accept": "application/json" if json_out else "*/*"}
    if S2_KEY and url.startswith("https://api.semanticscholar.org"):
        h["x-api-key"] = S2_KEY
    return h


def ambil(url, params=None, json_out=True, coba=3):
    if OPENALEX_KEY and url.startswith("https://api.openalex.org"):
        params = dict(params or {}, api_key=OPENALEX_KEY)
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode({k: v for k, v in params.items() if v not in (None, "")})
    req = urllib.request.Request(url, headers=_header(url, json_out))
    for i in range(coba):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read().decode("utf-8", "replace")
                return json.loads(data) if json_out else data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code in (429, 500, 502, 503) and i < coba - 1:
                time.sleep(2 * (i + 1))
                continue
            raise
        except urllib.error.URLError:
            if i < coba - 1:
                time.sleep(2 * (i + 1))
                continue
            raise


def bersih(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()


def rapikan_ujung(doi):
    """Buang tanda baca di ujung DOI; ')' hanya dibuang kalau tidak berpasangan,
    supaya DOI seperti 10.1016/S0140-6736(97)11096-0 tetap utuh."""
    while doi:
        if doi[-1] in ".,;:]>\"'":
            doi = doi[:-1]
        elif doi[-1] == ")" and doi.count(")") > doi.count("("):
            doi = doi[:-1]
        else:
            break
    return doi


def norm_doi(doi):
    doi = (doi or "").strip()
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", doi, flags=re.I)
    return rapikan_ujung(doi).lower()


def cari_doi(teks):
    """DOI pertama di teks (termasuk DOI berkurung dan DOI arXiv 10.48550/arXiv.xxxx), atau None."""
    m = re.search(r"10\.\d{4,9}/[^\s<>\"]+", teks or "")
    return rapikan_ujung(m.group(0)) if m else None


# Setiap hasil dinormalisasi ke dict:
# {judul, penulis:[...], tahun, sumber(jurnal), doi, url, sitasi, oa, db, retraksi}

# ---------------------------------------------------------------- database
def cari_openalex(q, n, dari=None, oa=False):
    filt = []
    if dari:
        filt.append(f"from_publication_date:{dari}-01-01")
    if oa:
        filt.append("is_oa:true")
    d = ambil("https://api.openalex.org/works", {"search": q, "per-page": n, "filter": ",".join(filt), "mailto": EMAIL})
    hasil = []
    for w in (d or {}).get("results", []):
        loc = (w.get("primary_location") or {})
        hasil.append({
            "judul": bersih(w.get("title") or w.get("display_name")),
            "penulis": [a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author")],
            "tahun": w.get("publication_year"),
            "sumber": ((loc.get("source") or {}).get("display_name")) or "",
            "doi": norm_doi(w.get("doi")),
            "url": (w.get("open_access") or {}).get("oa_url") or loc.get("landing_page_url") or w.get("id"),
            "sitasi": w.get("cited_by_count"),
            "oa": (w.get("open_access") or {}).get("is_oa"),
            "retraksi": w.get("is_retracted"),
            "jenis": w.get("type"),
            "db": "OpenAlex",
        })
    return hasil


def cari_arxiv(q, n, dari=None, oa=False):
    d = ambil("https://export.arxiv.org/api/query",
              {"search_query": f"all:{q}", "start": 0, "max_results": n, "sortBy": "relevance"}, json_out=False)
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    hasil = []
    for e in ET.fromstring(d).findall("a:entry", ns):
        tahun = int((e.findtext("a:published", "", ns) or "0000")[:4] or 0)
        if dari and tahun < int(dari):
            continue
        doi = e.findtext("x:doi", "", ns)
        jref = bersih(e.findtext("x:journal_ref", "", ns))
        hasil.append({
            "judul": bersih(e.findtext("a:title", "", ns)),
            "penulis": [bersih(a.findtext("a:name", "", ns)) for a in e.findall("a:author", ns)],
            "tahun": tahun,
            "sumber": jref or "arXiv (preprint)",
            "doi": norm_doi(doi),
            "url": e.findtext("a:id", "", ns),
            "sitasi": None, "oa": True, "retraksi": None,
            "jenis": "preprint-terbit" if jref else "preprint",
            "db": "arXiv",
        })
    return hasil


def cari_pubmed(q, n, dari=None, oa=False):
    term = q + (f" AND {dari}:3000[dp]" if dari else "")
    s = ambil("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
              {"db": "pubmed", "term": term, "retmode": "json", "retmax": n, "sort": "relevance",
               "email": EMAIL, "tool": "esai-lomba"})
    ids = (s or {}).get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []
    time.sleep(0.4)  # batas NCBI 3 permintaan/detik tanpa API key
    d = ambil("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
              {"db": "pubmed", "id": ",".join(ids), "retmode": "json", "email": EMAIL, "tool": "esai-lomba"})
    hasil = []
    for pid in ids:
        r = d["result"].get(pid, {})
        doi = next((x["value"] for x in r.get("articleids", []) if x.get("idtype") == "doi"), "")
        hasil.append({
            "judul": bersih(r.get("title")),
            "penulis": [a["name"] for a in r.get("authors", [])],
            "tahun": int((r.get("pubdate") or "0")[:4] or 0),
            "sumber": r.get("fulljournalname") or r.get("source", ""),
            "doi": norm_doi(doi),
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pid}/",
            "sitasi": None, "oa": None, "retraksi": "Retracted Publication" in (r.get("pubtype") or []),
            "jenis": ", ".join(r.get("pubtype") or []),
            "db": "PubMed",
        })
    return hasil


def cari_europepmc(q, n, dari=None, oa=False):
    query = q + (f" AND PUB_YEAR:[{dari} TO 3000]" if dari else "") + (" AND OPEN_ACCESS:y" if oa else "")
    d = ambil("https://www.ebi.ac.uk/europepmc/webservices/rest/search",
              {"query": query, "format": "json", "pageSize": n, "resultType": "lite"})
    hasil = []
    for r in (d or {}).get("resultList", {}).get("result", []):
        url = (f"https://europepmc.org/article/{r.get('source')}/{r.get('id')}")
        hasil.append({
            "judul": bersih(r.get("title")),
            "penulis": [p.strip() for p in (r.get("authorString") or "").rstrip(".").split(",") if p.strip()],
            "tahun": int(r.get("pubYear") or 0),
            "sumber": r.get("journalTitle", ""),
            "doi": norm_doi(r.get("doi")),
            "url": url,
            "sitasi": r.get("citedByCount"), "oa": r.get("isOpenAccess") == "Y", "retraksi": None,
            "jenis": r.get("pubType", ""),
            "db": "Europe PMC",
        })
    return hasil


def cari_semantic(q, n, dari=None, oa=False):
    d = ambil("https://api.semanticscholar.org/graph/v1/paper/search",
              {"query": q, "limit": n, "year": f"{dari}-" if dari else None,
               "fields": "title,authors,year,venue,externalIds,citationCount,openAccessPdf,url"})
    hasil = []
    for p in (d or {}).get("data", []):
        hasil.append({
            "judul": bersih(p.get("title")),
            "penulis": [a.get("name") for a in p.get("authors", [])],
            "tahun": p.get("year"),
            "sumber": p.get("venue", ""),
            "doi": norm_doi((p.get("externalIds") or {}).get("DOI")),
            "url": ((p.get("openAccessPdf") or {}).get("url")) or p.get("url"),
            "sitasi": p.get("citationCount"), "oa": bool(p.get("openAccessPdf")), "retraksi": None,
            "jenis": "", "db": "Semantic Scholar",
        })
    return hasil


GARUDA = "https://garuda.kemdiktisaintek.go.id"


def _nama_garuda(s):
    """Garuda menulis "Belakang, Depan"; ubah jadi "Depan Belakang" supaya sama dengan database lain."""
    s = bersih(s)
    if "," in s:
        belakang, depan = s.split(",", 1)
        s = f"{depan.strip()} {belakang.strip()}".strip()
    return s


def parse_garuda(h):
    """Hasil dari satu halaman pencarian Garuda (HTML). Bergantung pada tampilan situs: kalau Garuda
    mengubah tampilannya, fungsi ini mengembalikan daftar kosong, bukan hasil yang salah."""
    hasil = []
    for blok in (h or "").split('<div class="article-item">')[1:]:
        m = re.search(r'class="title-article"\s+href="([^"]+)"[^>]*>\s*<xmp>(.*?)</xmp>', blok, re.S)
        if not m:
            continue
        sub = re.search(r'<xmp class="subtitle-article">(.*?)</xmp>', blok, re.S)
        terbitan = bersih(sub.group(1)) if sub else ""
        th = re.search(r"\((\d{4})\)", terbitan)
        doi = re.search(r'href="https?://(?:dx\.)?doi\.org/([^"]+)"', blok)
        pdf = re.search(r'href="([^"]+)"[^>]*>\s*<i class="download icon">', blok)
        asli = re.search(r'href="([^"]+)"[^>]*>\s*Original Source', blok)
        abstrak = re.search(r'<xmp class="abstract-article">(.*?)</xmp>', blok, re.S)
        hasil.append({
            "judul": bersih(m.group(2)),
            "penulis": [_nama_garuda(x) for x in re.findall(r'class="author-article"[^>]*><xmp>(.*?)</xmp>', blok, re.S)],
            "tahun": int(th.group(1)) if th else None,
            "sumber": re.split(r"\s+Vol\.?\s", terbitan)[0].strip(),
            "doi": norm_doi(html.unescape(doi.group(1))) if doi else "",
            "url": html.unescape(asli.group(1)) if asli else GARUDA + m.group(1),
            "pdf": html.unescape(pdf.group(1)) if pdf else "",
            "abstrak": bersih(abstrak.group(1)) if abstrak else "",
            "sitasi": None, "oa": bool(pdf), "retraksi": None, "jenis": "", "db": "Garuda",
        })
    return hasil


def cari_garuda(q, n, dari=None, oa=False):
    """Garuda (Garba Rujukan Digital, Kemdiktisaintek): jurnal Indonesia, termasuk yang tanpa DOI.
    Tidak ada API resmi; alat membaca halaman pencarian publiknya (10 hasil per halaman, paling banyak 3 halaman)."""
    hasil = []
    for hal in range(1, 4):
        if hal > 1:
            time.sleep(1)  # sopan ke server Garuda
        rows = parse_garuda(ambil(GARUDA + "/documents", {"q": q, "page": hal}, json_out=False))
        if not rows:
            break
        hasil += [r for r in rows if (not dari or (r["tahun"] or 0) >= dari) and (not oa or r["oa"])]
        if len(hasil) >= n:
            break
    return hasil[:n]


DB = {"openalex": cari_openalex, "arxiv": cari_arxiv, "pubmed": cari_pubmed,
      "europepmc": cari_europepmc, "semantic": cari_semantic, "garuda": cari_garuda}


# ---------------------------------------------------------------- teks penuh akses terbuka
URUT_VERSI = {"publishedVersion": 0, "acceptedVersion": 1, "submittedVersion": 2}


def _unik(lokasi):
    lihat, out = set(), []
    for l in lokasi:
        k = l["pdf"] or l["halaman"]
        if k and k not in lihat:
            lihat.add(k)
            out.append(l)
    return out


def lokasi_dari_openalex(w):
    """Lokasi akses terbuka dari satu record OpenAlex (OpenAlex memuat data Unpaywall)."""
    hasil = []
    for loc in [(w or {}).get("best_oa_location")] + list((w or {}).get("locations") or []):
        if not loc or not loc.get("is_oa"):
            continue
        hasil.append({"pdf": loc.get("pdf_url") or "", "halaman": loc.get("landing_page_url") or "",
                      "lisensi": loc.get("license") or "", "versi": loc.get("version") or "",
                      "asal": ((loc.get("source") or {}).get("display_name")) or "OpenAlex"})
    return _unik(hasil)


def lokasi_dari_unpaywall(d):
    hasil = []
    for loc in (d or {}).get("oa_locations") or []:
        hasil.append({"pdf": loc.get("url_for_pdf") or "",
                      "halaman": loc.get("url_for_landing_page") or loc.get("url") or "",
                      "lisensi": loc.get("license") or "", "versi": loc.get("version") or "",
                      "asal": "Unpaywall" + (f" ({loc['host_type']})" if loc.get("host_type") else "")})
    return _unik(hasil)


def urutkan_lokasi(lokasi):
    """Versi terbit dulu, lalu naskah diterima, lalu preprint; yang punya PDF didahulukan."""
    return sorted(lokasi, key=lambda l: (URUT_VERSI.get(l["versi"], 3), 0 if l["pdf"] else 1))


def pmcid_dari(w):
    """PMCID dari record OpenAlex; OpenAlex kadang menulisnya tanpa awalan PMC (.../articles/1182327)."""
    m = re.search(r"(?:PMC)?(\d+)/?$", (((w or {}).get("ids") or {}).get("pmcid") or "").strip())
    return "PMC" + m.group(1) if m else None


def jats_ke_teks(xml):
    """Teks dari artikel JATS XML (format teks penuh Europe PMC): judul, abstrak, lalu isi per bagian."""
    root = ET.fromstring(xml)

    def isi(el):
        return re.sub(r"\s+", " ", "".join(el.itertext())).strip()

    baris = []
    judul = root.find(".//article-meta//article-title")
    if judul is not None:
        baris.append("# " + isi(judul))
    for ab in root.findall(".//article-meta/abstract"):
        baris.append("## Abstrak")
        baris += [isi(p) for p in ab.iter("p") if isi(p)]
    body = root.find(".//body")
    if body is not None:
        for el in body.iter():
            if el.tag == "title" and isi(el):
                baris.append("## " + isi(el))
            elif el.tag == "p" and isi(el):
                baris.append(isi(el))
    return "\n\n".join(baris)


def unduh(url, batas=30_000_000):
    req = urllib.request.Request(url, headers={**_header(url, False), "Accept": "application/pdf,*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read(batas + 1)
    if len(data) > batas:
        raise ValueError("file lebih dari 30 MB")
    return data


def pdf_ke_teks(data):
    """Teks PDF per halaman dengan penanda '=== Halaman N ===' (nomor halaman file, bukan halaman jurnal)."""
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    pdf = PdfReader(io.BytesIO(data))
    teks = "\n\n".join(f"=== Halaman {i} ===\n{(hlm.extract_text() or '').strip()}" for i, hlm in enumerate(pdf.pages, 1))
    return unicodedata.normalize("NFKC", teks)  # ligatur PDF seperti "ﬁ" menjadi "fi"


def nama_file_teks(folder, penulis, tahun):
    """<folder>/<nama-belakang-penulis-pertama>-<tahun>.md; tidak pernah menimpa file yang sudah ada."""
    nama = (nama_dasar(penulis[0]) or ["sumber"])[-1] if penulis else "tanpa-penulis"
    dasar = f"{nama}-{tahun or 'tt'}"
    path, i = os.path.join(folder, dasar + ".md"), 2
    while os.path.exists(path):
        path, i = os.path.join(folder, f"{dasar}-{i}.md"), i + 1
    return path


def path_dengan_nama(folder, nama):
    """<folder>/<nama>.md dari nama pilihan penulis (misalnya rukmana-2024); tidak pernah menimpa."""
    dasar = re.sub(r"[^a-z0-9]+", "-", nama.lower()).strip("-") or "sumber"
    path, i = os.path.join(folder, dasar + ".md"), 2
    while os.path.exists(path):
        path, i = os.path.join(folder, f"{dasar}-{i}.md"), i + 1
    return path


def teks_dari_link(url, folder=None, nama=None):
    """Untuk artikel tanpa DOI: unduh PDF dari link akses terbuka lalu simpan teksnya."""
    print(f"Link: {url}")
    if not folder:
        print("Tambahkan --simpan-teks <L>/riset/teks (dan --nama penulis-tahun) untuk menyimpan teksnya.")
        return 0
    try:
        data = unduh(url)
    except Exception as ex:
        print(f"❌ Gagal mengunduh: {ex}")
        return 1
    if not data.startswith(b"%PDF"):
        print("❌ Link itu bukan file PDF (mungkin halaman artikel, login, atau pemeriksaan bot). "
              "Cari tombol unduh PDF di halamannya, atau pakai link 'Download Original' dari Garuda.")
        return 1
    teks = pdf_ke_teks(data)
    if teks is None:
        print("❌ Paket pypdf belum terpasang: pip install pypdf")
        return 1
    os.makedirs(folder, exist_ok=True)
    path = path_dengan_nama(folder, nama) if nama else nama_file_teks(folder, [], None)
    kepala = (f"Sumber: {url} · diakses {time.strftime('%Y-%m-%d')} · bagian: teks penuh "
              f"(PDF dari {urllib.parse.urlparse(url).netloc}) · versi: tidak disebut · lisensi: tidak disebut\n\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write(kepala + teks + "\n")
    print(f"✅ Teks penuh disimpan: {path} ({len(teks):,} karakter)")
    if len(teks) < 3000:
        print("⚠️ Teksnya pendek; mungkin hanya abstrak atau PDF hasil pindaian. Periksa isinya.")
    print("Artikel tanpa DOI: catat penulis, tahun, judul, dan nama jurnal dari halaman artikelnya di log sumber, "
          "lalu cocokkan kutipan dengan PDF aslinya sebelum memberi ✅.")
    return 0


def teks_penuh(argumen, folder=None, nama=None):
    if not cari_doi(argumen) and argumen.lower().startswith(("http://", "https://")):
        return teks_dari_link(argumen, folder, nama)
    doi = norm_doi(cari_doi(argumen) or argumen)
    w = ambil("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi, safe="/:()"))
    if not w:
        print(f"❌ DOI {doi} tidak ditemukan di OpenAlex. Cek dulu dengan perintah `doi`.")
        return 1
    lokasi = lokasi_dari_openalex(w)
    if EMAIL:
        try:
            lokasi = _unik(lokasi + lokasi_dari_unpaywall(
                ambil("https://api.unpaywall.org/v2/" + doi, {"email": EMAIL})))
        except Exception as ex:
            print(f"[Unpaywall] gagal: {ex}")
    lokasi = urutkan_lokasi(lokasi)
    pmcid = pmcid_dari(w)
    judul = bersih(w.get("title") or w.get("display_name"))
    penulis = [a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author")]
    tahun = w.get("publication_year")
    print(f"{judul} ({tahun})\nhttps://doi.org/{doi}")
    print(f"Status akses terbuka: {(w.get('open_access') or {}).get('oa_status') or 'tidak diketahui'}")
    if w.get("is_retracted"):
        print("⛔ Paper ini sudah ditarik (retracted). Jangan dipakai.")
    if not lokasi and not pmcid:
        print("Tidak ada versi akses terbuka yang tercatat. Teks penuh hanya lewat langganan/perpustakaan; "
              "jangan memakai situs bajakan. Kalau hanya abstrak yang terbaca, status di peta klaim maksimal ⚠️.")
        return 0
    for i, l in enumerate(lokasi, 1):
        print(f"{i}. {l['versi'] or 'versi tidak disebut'} · lisensi: {l['lisensi'] or 'tidak disebut'} · {l['asal']}")
        if l["pdf"]:
            print(f"     PDF: {l['pdf']}")
        if l["halaman"]:
            print(f"     Halaman: {l['halaman']}")
    if pmcid:
        print(f"Europe PMC (teks penuh): https://europepmc.org/article/PMC/{pmcid}")
    if lokasi and all(l["versi"] == "submittedVersion" for l in lokasi):
        print("ℹ️ Hanya ada versi naskah awal (preprint). Isinya bisa berbeda dari versi terbit; kutip versi jurnalnya.")
    if not folder:
        return 0

    teks, asal, versi, lisensi = None, "", "", ""
    if pmcid:
        try:
            xml = ambil(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML", json_out=False)
            if xml:
                teks, asal, versi = jats_ke_teks(xml), f"Europe PMC {pmcid}, XML", "publishedVersion"
                lisensi = next((l["lisensi"] for l in lokasi if "PubMed Central" in l["asal"] and l["lisensi"]), "")
        except Exception as ex:
            print(f"[Europe PMC] gagal: {ex}")
    for l in lokasi:
        if teks or not l["pdf"]:
            continue
        try:
            data = unduh(l["pdf"])
        except Exception as ex:
            print(f"[unduh] gagal dari {l['pdf']}: {ex}")
            continue
        if not data.startswith(b"%PDF"):
            print(f"[unduh] {l['pdf']} bukan file PDF (mungkin halaman login atau pemeriksaan bot), dilewati.")
            continue
        teks = pdf_ke_teks(data)
        if teks is None:
            print("❌ Paket pypdf belum terpasang: pip install pypdf")
            return 1
        asal, versi, lisensi = f"PDF dari {urllib.parse.urlparse(l['pdf']).netloc}", l["versi"], l["lisensi"]
    if not teks:
        print("❌ Teks penuh tidak bisa diunduh otomatis. Buka link di atas secara manual.")
        return 1
    os.makedirs(folder, exist_ok=True)
    path = path_dengan_nama(folder, nama) if nama else nama_file_teks(folder, penulis, tahun)
    kepala = (f"Sumber: https://doi.org/{doi} · diakses {time.strftime('%Y-%m-%d')} · bagian: teks penuh ({asal})"
              f" · versi: {versi or 'tidak disebut'} · lisensi: {lisensi or 'tidak disebut'}\n\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write(kepala + teks + "\n")
    print(f"\n✅ Teks penuh disimpan: {path} ({len(teks):,} karakter)")
    if len(teks) < 3000:
        print("⚠️ Teksnya pendek; mungkin hanya abstrak atau PDF hasil pindaian. Periksa isinya.")
    print("Teks ini hasil ekstraksi mesin. Cocokkan kutipan dengan versi aslinya sebelum memberi ✅ di peta klaim "
          "(nomor halaman PDF belum tentu sama dengan nomor halaman jurnal).")
    return 0


# ---------------------------------------------------------------- Crossref & APA
def crossref_doi(doi):
    d = ambil(f"https://api.crossref.org/works/{urllib.parse.quote(norm_doi(doi))}", {"mailto": EMAIL})
    return (d or {}).get("message")


def crossref_cari(teks):
    d = ambil("https://api.crossref.org/works", {"query.bibliographic": teks, "rows": 1, "mailto": EMAIL})
    items = (d or {}).get("message", {}).get("items", [])
    return items[0] if items else None


def dari_crossref(m):
    tgl = (m.get("issued") or m.get("published") or {}).get("date-parts", [[None]])[0]
    return {
        "judul": bersih((m.get("title") or [""])[0]),
        "penulis": [" ".join(x for x in (a.get("given"), a.get("family")) if x) or a.get("name", "")
                    for a in m.get("author", [])],
        "penulis_raw": m.get("author", []),
        "tahun": tgl[0] if tgl else None,
        "sumber": (m.get("container-title") or [""])[0],
        "volume": m.get("volume"), "terbitan": m.get("issue"), "halaman": m.get("page"),
        "doi": norm_doi(m.get("DOI")),
        "url": f"https://doi.org/{norm_doi(m.get('DOI'))}",
        "sitasi": m.get("is-referenced-by-count"), "oa": None, "retraksi": None,
        "jenis": m.get("type"), "db": "Crossref",
        "update": [u.get("type") for u in m.get("update-to", [])],
        "retraksi_crossref": retraksi_crossref(m),
    }


def datacite_doi(doi):
    """DOI yang tidak terdaftar di Crossref (arXiv 10.48550, Zenodo, banyak repositori) ada di DataCite."""
    d = ambil(f"https://api.datacite.org/dois/{urllib.parse.quote(norm_doi(doi))}")
    a = ((d or {}).get("data") or {}).get("attributes")
    if not a:
        return None
    return {
        "judul": bersih(((a.get("titles") or [{}])[0]).get("title")),
        "penulis": [c.get("name", "") for c in a.get("creators", [])],
        "penulis_raw": [{"family": c.get("familyName"), "given": c.get("givenName", ""), "name": c.get("name")}
                        for c in a.get("creators", [])],
        "tahun": a.get("publicationYear"),
        "sumber": a.get("publisher") or "",
        "doi": norm_doi(a.get("doi")),
        "url": f"https://doi.org/{norm_doi(a.get('doi'))}",
        "sitasi": None, "oa": True, "retraksi": None,
        "jenis": ((a.get("types") or {}).get("resourceTypeGeneral") or "").lower(),
        "db": "DataCite", "update": [], "retraksi_crossref": False,
    }


def cari_metadata_doi(doi):
    """Crossref dulu, lalu DataCite. Mengembalikan dict hasil (format dari_crossref) atau None."""
    m = crossref_doi(doi)
    if m:
        return dari_crossref(m)
    return datacite_doi(doi)


def retraksi_crossref(m):
    """True kalau metadata Crossref menandai paper ini ditarik (updated-by / update-to bertipe retraction/withdrawal)."""
    for kunci in ("updated-by", "update-to"):
        for u in (m or {}).get(kunci, []) or []:
            if re.search(r"retract|withdraw|removal", (u.get("type") or ""), flags=re.I):
                return True
    return False


def status_retraksi(doi):
    """True/False dari OpenAlex, atau None kalau OpenAlex gagal dihubungi (status TIDAK DIKETAHUI, bukan 'aman')."""
    try:
        w = ambil(f"https://api.openalex.org/works/doi:{norm_doi(doi)}", {"mailto": EMAIL})
        return None if w is None else bool(w.get("is_retracted"))
    except Exception:
        return None


def nama_dasar(s):
    """Huruf kecil tanpa aksen dan tanda baca, untuk membandingkan nama penulis/jurnal."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split()


def cocokkan_metadata(entri, r):
    """Bandingkan entri pustaka dengan metadata DOI. Mengembalikan daftar ketidakcocokan (kosong = cocok)."""
    salah = []
    kata_entri = set(nama_dasar(entri))
    raw = r.get("penulis_raw") or []
    pertama = ""
    if raw:
        pertama = raw[0].get("family") or raw[0].get("name") or ""
    elif r.get("penulis"):
        pertama = r["penulis"][0].split()[-1]
    if pertama:
        kp = nama_dasar(pertama)
        if kp and not all(k in kata_entri for k in kp):
            salah.append(f"penulis pertama di DOI '{pertama}' tidak ada di entri")
    if r.get("tahun"):
        tahun_entri = [int(t) for t in re.findall(r"\b(19\d{2}|20\d{2})\b", entri)]
        if tahun_entri and not any(abs(t - int(r["tahun"])) <= 1 for t in tahun_entri):
            salah.append(f"tahun di DOI {r['tahun']} berbeda dengan entri ({', '.join(map(str, tahun_entri))})")
    return salah


def jurnal_cocok(entri, r):
    """None kalau tidak bisa dicek; True/False kalau nama jurnal dari DOI muncul di entri (singkatan bisa membuat False)."""
    js = [k for k in nama_dasar(r.get("sumber")) if len(k) > 3 and k not in ("journal", "jurnal", "the", "and")]
    if not js or r.get("db") != "Crossref":
        return None
    kata_entri = set(nama_dasar(entri))
    return sum(k in kata_entri for k in js) >= max(1, len(js) // 2)


def apa(r):
    """Format APA 7 sederhana untuk artikel jurnal. Selalu cek ulang manual."""
    raw = r.get("penulis_raw")
    if raw:
        nama = []
        for a in raw:
            if a.get("family"):
                inisial = " ".join(f"{p[0]}." for p in re.split(r"[\s\-]+", a.get("given") or "") if p)
                nama.append(f"{a['family']}, {inisial}".strip().rstrip(","))
            elif a.get("name"):
                nama.append(a["name"])
    else:
        nama = r.get("penulis", [])
    if len(nama) == 0:
        pen = ""
    elif len(nama) == 1:
        pen = nama[0]
    elif len(nama) <= 20:
        pen = ", ".join(nama[:-1]) + ", & " + nama[-1]
    else:
        pen = ", ".join(nama[:19]) + ", . . . " + nama[-1]
    bagian = [f"{pen} ({r.get('tahun') or 't.t.'}). {r.get('judul', '').rstrip('.')}."]
    if r.get("sumber"):
        s = f"*{r['sumber']}*"
        if r.get("volume"):
            s += f", *{r['volume']}*"
            if r.get("terbitan"):
                s += f"({r['terbitan']})"
        if r.get("halaman"):
            s += f", {r['halaman'].replace('-', '–')}"
        bagian.append(s + ".")
    if r.get("doi"):
        bagian.append(f"https://doi.org/{r['doi']}")
    elif r.get("url"):
        bagian.append(r["url"])
    return " ".join(bagian)


# ---------------------------------------------------------------- openFDA & ClinicalTrials
def fda(obat, n):
    q = urllib.parse.quote(f'"{obat}"')
    out = {"recall": [], "label": []}
    d = ambil(f"https://api.fda.gov/drug/enforcement.json?search=product_description:{q}&limit={n}")
    for r in (d or {}).get("results", []):
        out["recall"].append(f"{r.get('report_date', '')[:4]} · kelas {r.get('classification', '')} · "
                             f"{bersih(r.get('reason_for_recall'))[:160]} · {r.get('recalling_firm', '')}")
    d = ambil(f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{q}&limit=1")
    for r in (d or {}).get("results", []):
        for k in ("indications_and_usage", "storage_and_handling", "warnings"):
            if r.get(k):
                out["label"].append(f"{k}: {bersih(r[k][0])[:300]}")
    return out


def uji_klinis(q, n):
    d = ambil("https://clinicaltrials.gov/api/v2/studies", {"query.term": q, "pageSize": n})
    hasil = []
    for s in (d or {}).get("studies", []):
        p = s.get("protocolSection", {})
        idm = p.get("identificationModule", {})
        st = p.get("statusModule", {})
        hasil.append(f"{idm.get('nctId')} · {idm.get('briefTitle')} · {st.get('overallStatus')} · "
                     f"mulai {(st.get('startDateStruct') or {}).get('date', '?')} · "
                     f"https://clinicaltrials.gov/study/{idm.get('nctId')}")
    return hasil


# ---------------------------------------------------------------- tampilan
def tampil(r, i=None):
    pen = r["penulis"]
    pen_s = (pen[0] + (" dkk." if len(pen) > 1 else "")) if pen else "(tanpa penulis)"
    flag = []
    if r.get("retraksi"):
        flag.append("⛔ DITARIK (retracted)")
    if r.get("jenis") in ("preprint", "posted-content"):
        flag.append("preprint, belum peer-review")
    if r.get("jenis") == "preprint-terbit":
        flag.append("preprint yang sudah terbit di jurnal (kutip versi jurnalnya)")
    if r.get("oa"):
        flag.append("open access")
    if r.get("sitasi") is not None:
        flag.append(f"{r['sitasi']} sitasi")
    awal = f"{i}. " if i is not None else ""
    print(f"{awal}[{r['db']}] {pen_s} ({r.get('tahun')}). {r['judul']}")
    if r.get("sumber"):
        print(f"     {r['sumber']}")
    print(f"     {('https://doi.org/' + r['doi']) if r.get('doi') else r.get('url', '')}")
    if r.get("pdf") and not r.get("doi"):
        print(f"     PDF: {r['pdf']}")
    if flag:
        print(f"     {' · '.join(flag)}")


def simpan(path, rows):
    baru = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as f:
        if baru:
            f.write("# Log Sumber\n\n| # | Status | Penulis/Lembaga (Tahun) | Judul | Link/DOI | Jenis | Teks disimpan di | "
                    "Temuan/data yang dipakai (+halaman/tabel) | Dipakai untuk argumen |\n"
                    "|---|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            pen = r["penulis"][0] + (" dkk." if len(r["penulis"]) > 1 else "") if r["penulis"] else ""
            link = f"https://doi.org/{r['doi']}" if r.get("doi") else r.get("url", "")
            judul = r["judul"].replace("|", "/")
            f.write(f"| | ⚠️ | {pen} ({r.get('tahun')}) | {judul} | {link} | {r['db']}: {r.get('jenis') or ''} | | | |\n")
    print(f"\n{len(rows)} baris ditambahkan ke {path} (status ⚠️ sampai kamu membuka dan membaca sumbernya).")


def pecah_entri(teks_bagian):
    """Pecah isi bagian Daftar Pustaka jadi entri: satu entri per baris atau per butir daftar.
    Baris yang diawali spasi/tab (lanjutan entri panjang) digabung ke entri sebelumnya."""
    entri = []
    for baris in teks_bagian.splitlines():
        if not baris.strip():
            continue
        butir = re.match(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|\[\d+\]\s*)", baris)
        if entri and not butir and baris[:1] in (" ", "	"):
            entri[-1] += " " + baris.strip()
            continue
        entri.append(re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|\[\d+\]\s*)", "", baris).strip())
    return [e for e in entri if e]


def bagian_pustaka(md):
    with open(md, encoding="utf-8-sig") as f:
        teks = f.read()
    teks = re.sub(r"<!--.*?-->", "", teks, flags=re.S)
    m = re.search(r"^##\s+(Daftar Pustaka|Referensi|Daftar Referensi|Daftar Rujukan)\s*:?\s*$(.*?)(?=^##\s|\Z)",
                  teks, flags=re.M | re.S | re.I)
    if not m:
        sys.exit("Bagian '## Daftar Pustaka' tidak ditemukan.")
    return pecah_entri(m.group(2))


LEMBAGA = r"(kemkes|kemenkes|kementerian|badan |bps\.go|pom\.go|bpom|who\.int|world health|unicef|unesco|worldbank|world bank|peraturan|undang-undang|jdih|\.go\.id|\.gov\b)"


def kemiripan_judul(judul, entri):
    return difflib.SequenceMatcher(None, judul.lower(), entri.lower()).find_longest_match(
        0, len(judul), 0, len(entri)).size / max(len(judul), 1)


def cek_pustaka(md):
    entri = bagian_pustaka(md)
    ok = masalah = 0
    manual, retraksi_tak_tercek = [], []
    for i, e in enumerate(entri, 1):
        e1 = " ".join(e.split())
        pendek = e1[:110] + ("..." if len(e1) > 110 else "")
        print(f"\n{i}. {pendek}")
        doi = cari_doi(e1)
        try:
            if doi:
                r = cari_metadata_doi(doi)
                if not r:
                    print(f"   ❌ DOI {doi} TIDAK DITEMUKAN di Crossref maupun DataCite. Kemungkinan salah ketik atau referensi karangan.")
                    masalah += 1
                    continue
                print(f"   ✅ DOI ada ({r['db']}): {r['judul'][:90]} ({r['tahun']})")
                salah = []
                if r["judul"] and kemiripan_judul(r["judul"], e1) < 0.6:
                    salah.append("judul di metadata DOI tidak cocok dengan entri")
                salah += cocokkan_metadata(e1, r)
                if jurnal_cocok(e1, r) is False:
                    print(f"   ℹ️ Nama jurnal di DOI: '{r['sumber']}'. Tidak ditemukan di entri (abaikan kalau entri memakai singkatan).")
                ret = True if r.get("retraksi_crossref") else status_retraksi(r["doi"])
                if salah:
                    for s_ in salah:
                        print(f"   ⚠️ {s_[0].upper() + s_[1:]}. Cek apakah DOI dan entri menunjuk paper yang sama.")
                    masalah += 1
                elif ret:
                    print("   ⛔ PAPER INI SUDAH DITARIK (retracted). Jangan dipakai.")
                    masalah += 1
                elif ret is None:
                    print("   ❓ PERINGATAN: status retraksi TIDAK TERCEK (OpenAlex gagal dihubungi atau tidak mengenal DOI ini). "
                          "Cek manual di https://retractiondatabase.org atau ulangi nanti.")
                    retraksi_tak_tercek.append(i)
                    masalah += 1
                else:
                    ok += 1
            else:
                web = re.search(r"https?://\S+", e1)
                link = web.group(0).rstrip(".,;)") if web else None
                if re.search(LEMBAGA, e1, flags=re.I):
                    print(f"   ℹ️ Dokumen lembaga/regulasi tanpa DOI. CEK MANUAL: {link or '(tidak ada link!)'}")
                    manual.append((i, link))
                    masalah += 1
                    continue
                m = crossref_cari(e1)
                if m:
                    r = dari_crossref(m)
                    if kemiripan_judul(r["judul"], e1) > 0.8 and not cocokkan_metadata(e1, r):
                        print(f"   ✅ Cocok di Crossref, DOI: https://doi.org/{r['doi']} (tambahkan DOI ke entri)")
                        ok += 1
                        continue
                    print(f"   ⚠️ Tidak ada yang cocok persis. Terdekat: {r['judul'][:80]} ({r['tahun']})")
                else:
                    print("   ⚠️ Tidak ditemukan di Crossref.")
                print(f"   → CEK MANUAL{': ' + link if link else ' (tidak ada link/DOI!)'}")
                manual.append((i, link))
                masalah += 1
        except (urllib.error.URLError, OSError) as ex:
            print(f"   ❓ Gagal mengecek (jaringan/API tidak bisa dihubungi): {getattr(ex, 'reason', ex)}")
            masalah += 1
        time.sleep(0.2)
    print(f"\n== {ok} terverifikasi otomatis · {masalah} perlu dicek · {len(entri)} entri ==")
    if manual:
        print("Cek manual (tanpa DOI): entri " + ", ".join(f"{i}" + (f" ({l})" if l else " (tanpa link)") for i, l in manual))
    if retraksi_tak_tercek:
        print("Status retraksi tidak tercek: entri " + ", ".join(map(str, retraksi_tak_tercek)))
    return 1 if masalah else 0


# ---------------------------------------------------------------- main
def main():
    global EMAIL
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("perintah", choices=["cari", "doi", "teks", "cek-pustaka", "fda", "uji-klinis"])
    ap.add_argument("argumen")
    ap.add_argument("--db", default="openalex")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--dari", type=int)
    ap.add_argument("--oa", action="store_true")
    ap.add_argument("--simpan")
    ap.add_argument("--email")
    ap.add_argument("--simpan-teks", help="folder tujuan teks penuh untuk perintah teks, misalnya <L>/riset/teks")
    ap.add_argument("--nama", help="nama file teks (misalnya rukmana-2024) untuk perintah teks")
    a = ap.parse_args()
    if a.email:
        EMAIL = a.email

    if a.perintah == "cari":
        dbs = list(DB) if a.db == "semua" else a.db.split(",")
        semua, terlihat = [], set()
        for nama in dbs:
            try:
                hasil = DB[nama](a.argumen, a.n, a.dari, a.oa)
            except Exception as ex:
                print(f"[{nama}] gagal: {ex}")
                continue
            for r in hasil:
                kunci = r["doi"] or r["judul"].lower()
                if kunci in terlihat:
                    continue
                terlihat.add(kunci)
                semua.append(r)
        for i, r in enumerate(semua, 1):
            tampil(r, i)
        if not semua:
            print("Tidak ada hasil. Coba kata kunci bahasa Inggris atau lebih umum.")
        if a.simpan and semua:
            simpan(a.simpan, semua)
    elif a.perintah == "doi":
        doi = cari_doi(a.argumen) or a.argumen
        r = cari_metadata_doi(doi)
        if not r:
            sys.exit(f"❌ DOI {doi} tidak ditemukan di Crossref maupun DataCite.")
        r["retraksi"] = True if r.get("retraksi_crossref") else status_retraksi(r["doi"])
        tampil(r)
        if r["retraksi"]:
            print("⛔ Paper ini sudah ditarik (retracted). Jangan dipakai.")
        elif r["retraksi"] is None:
            print("❓ PERINGATAN: status retraksi TIDAK TERCEK (OpenAlex gagal dihubungi). Ulangi nanti atau cek manual.")
        if r.get("jenis") in ("posted-content", "preprint") or r["doi"].startswith("10.48550/"):
            print("ℹ️ Ini preprint (belum peer-review). Cari apakah sudah terbit di jurnal, lalu kutip versi jurnalnya.")
        print("\nAPA 7 (cek ulang huruf kapital & miring):\n" + apa(r))
        if a.simpan:
            simpan(a.simpan, [r])
    elif a.perintah == "teks":
        sys.exit(teks_penuh(a.argumen, a.simpan_teks, a.nama))
    elif a.perintah == "cek-pustaka":
        sys.exit(cek_pustaka(a.argumen))
    elif a.perintah == "fda":
        out = fda(a.argumen, a.n)
        print("Catatan: data FDA berlaku untuk pasar Amerika Serikat, bukan Indonesia (untuk Indonesia: cekbpom.pom.go.id).")
        print("\nRecall:" if out["recall"] else "\nRecall: tidak ada data")
        for x in out["recall"]:
            print(" -", x)
        print("\nLabel:" if out["label"] else "\nLabel: tidak ada data")
        for x in out["label"]:
            print(" -", x)
    elif a.perintah == "uji-klinis":
        for x in uji_klinis(a.argumen, a.n):
            print("-", x)


if __name__ == "__main__":
    try:
        main()
    except (urllib.error.URLError, OSError) as ex:
        sys.exit(f"❌ Tidak bisa menghubungi database ({getattr(ex, 'reason', ex)}). Cek koneksi internet lalu ulangi.")
    except KeyboardInterrupt:
        sys.exit("Dibatalkan.")
