#!/usr/bin/env python3
"""Tes otomatis untuk alat di tools/ (pustaka standar Python, sebagian besar tanpa internet).

Pakai:
    python tools/tes_alat.py              # semua tes offline
    python tools/tes_alat.py -v           # tampilkan nama setiap tes
Tes yang butuh internet (Crossref/DataCite/OpenAlex) hanya jalan kalau variabel lingkungan
ESAI_TES_JARINGAN=1 (PowerShell: $env:ESAI_TES_JARINGAN="1").
Tes build_docx dan cek_docx dilewati kalau python-docx belum terpasang; tes buat_visual dilewati
kalau matplotlib belum terpasang; tes cek_pptx dilewati kalau python-pptx belum terpasang.

Setiap tes di sini mewakili bug yang pernah ditemukan saat audit (28–29 Okt 2026).
"""
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import cari_sumber as cs  # noqa: E402
import cek_naskah as cn  # noqa: E402
import cek_klaim as ck  # noqa: E402
import arena  # noqa: E402
import evaluasi as ev  # noqa: E402

try:
    import build_docx as bd
    import docx
    ADA_DOCX = True
except SystemExit:
    ADA_DOCX = False

JARINGAN = os.environ.get("ESAI_TES_JARINGAN") == "1"


def tulis(folder, nama, isi):
    p = Path(folder) / nama
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(isi, encoding="utf-8")
    return p


# ---------------------------------------------------------------- cari_sumber
class TesDoi(unittest.TestCase):
    def test_doi_berkurung_utuh(self):
        self.assertEqual(cs.cari_doi("Wakefield (1998). Lancet. https://doi.org/10.1016/S0140-6736(97)11096-0."),
                         "10.1016/S0140-6736(97)11096-0")
        self.assertEqual(cs.cari_doi("doi:10.1016/S0140-6736(20)30183-5"), "10.1016/S0140-6736(20)30183-5")

    def test_kurung_penutup_luar_dibuang(self):
        self.assertEqual(cs.cari_doi("(lihat https://doi.org/10.1038/nature14539)"), "10.1038/nature14539")

    def test_doi_arxiv(self):
        self.assertEqual(cs.cari_doi("https://doi.org/10.48550/arXiv.1706.03762"), "10.48550/arXiv.1706.03762")
        self.assertEqual(cs.norm_doi("https://doi.org/10.48550/arXiv.1706.03762"), "10.48550/arxiv.1706.03762")

    def test_tanpa_doi(self):
        self.assertIsNone(cs.cari_doi("Badan Pusat Statistik. (2023). Statistik Indonesia."))


class TesEntriPustaka(unittest.TestCase):
    def test_satu_entri_per_baris(self):
        teks = ("LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature. https://doi.org/10.1038/nature14539\n"
                "Badan Pusat Statistik. (2023). Statistik Indonesia 2023. https://www.bps.go.id\n"
                "Vaswani, A. dkk. (2017). Attention is all you need. https://doi.org/10.48550/arXiv.1706.03762\n")
        self.assertEqual(len(cs.pecah_entri(teks)), 3)

    def test_butir_dan_lanjutan(self):
        teks = "- Smith, J. (2020). Judul panjang\n  yang bersambung. Jurnal A.\n- Lee, K. (2021). Lain.\n1. Park, S. (2019). X.\n"
        e = cs.pecah_entri(teks)
        self.assertEqual(len(e), 3)
        self.assertIn("yang bersambung", e[0])
        self.assertTrue(e[2].startswith("Park"))


class TesMetadata(unittest.TestCase):
    R = {"judul": "Deep learning", "penulis_raw": [{"family": "LeCun", "given": "Yann"}], "tahun": 2015,
         "sumber": "Nature", "db": "Crossref"}

    def test_cocok(self):
        self.assertEqual(cs.cocokkan_metadata("LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature.", self.R), [])

    def test_penulis_dan_tahun_salah(self):
        salah = cs.cocokkan_metadata("Smith, J., & Hinton, G. (2019). Deep learning. Nature.", self.R)
        self.assertEqual(len(salah), 2)

    def test_tahun_selisih_satu_boleh(self):
        self.assertEqual(cs.cocokkan_metadata("LeCun, Y. (2016). Deep learning.", self.R), [])

    def test_jurnal(self):
        self.assertTrue(cs.jurnal_cocok("LeCun, Y. (2015). Deep learning. Nature, 521.", self.R))
        self.assertFalse(cs.jurnal_cocok("LeCun, Y. (2015). Deep learning. Science, 521.", self.R))


class TesRetraksi(unittest.TestCase):
    def test_crossref_updated_by(self):
        m = {"updated-by": [{"type": "retraction", "DOI": "10.1/x"}]}
        self.assertTrue(cs.retraksi_crossref(m))

    def test_crossref_update_to(self):
        self.assertTrue(cs.retraksi_crossref({"update-to": [{"type": "Withdrawal"}]}))
        self.assertFalse(cs.retraksi_crossref({"update-to": [{"type": "correction"}]}))

    def test_openalex_gagal_bukan_aman(self):
        asli = cs.ambil
        try:
            def gagal(*a, **k):
                raise cs.urllib.error.URLError("offline")
            cs.ambil = gagal
            self.assertIsNone(cs.status_retraksi("10.1038/nature14539"))
        finally:
            cs.ambil = asli


class TesCekPustakaOffline(unittest.TestCase):
    """cek-pustaka dengan API tiruan: retraksi tak tercek = peringatan, entri .go.id = cek manual."""

    def jalankan(self, isi):
        asli = (cs.cari_metadata_doi, cs.status_retraksi, cs.crossref_cari)
        cs.cari_metadata_doi = lambda doi: {"judul": "Deep learning", "tahun": 2015, "db": "Crossref", "sumber": "Nature",
                                            "penulis_raw": [{"family": "LeCun", "given": "Y"}], "doi": doi,
                                            "retraksi_crossref": False}
        cs.status_retraksi = lambda doi: None
        cs.crossref_cari = lambda t: None
        try:
            with tempfile.TemporaryDirectory() as d:
                p = tulis(d, "x.md", isi)
                keluar = io.StringIO()
                lama, sys.stdout = sys.stdout, keluar
                try:
                    kode = cs.cek_pustaka(str(p))
                finally:
                    sys.stdout = lama
                return kode, keluar.getvalue()
        finally:
            cs.cari_metadata_doi, cs.status_retraksi, cs.crossref_cari = asli

    def test_peringatan_dan_manual(self):
        kode, out = self.jalankan("# J\n\nIsi.\n\n## daftar pustaka\n"
                                  "LeCun, Y. (2015). Deep learning. Nature. https://doi.org/10.1038/nature14539\n"
                                  "Badan Pusat Statistik. (2023). Statistik. https://www.bps.go.id\n")
        self.assertEqual(kode, 1)
        self.assertIn("TIDAK TERCEK", out)
        self.assertIn("Cek manual (tanpa DOI): entri 2", out)
        self.assertIn("2 entri", out)


@unittest.skipUnless(JARINGAN, "set ESAI_TES_JARINGAN=1 untuk tes internet")
class TesJaringan(unittest.TestCase):
    def test_crossref(self):
        r = cs.cari_metadata_doi("10.1038/nature14539")
        self.assertEqual(r["tahun"], 2015)

    def test_datacite_arxiv(self):
        r = cs.cari_metadata_doi("10.48550/arXiv.1706.03762")
        self.assertIsNotNone(r)
        self.assertIn("Attention", r["judul"])

    def test_retraksi_wakefield(self):
        r = cs.cari_metadata_doi("10.1016/S0140-6736(97)11096-0")
        self.assertTrue(r["retraksi_crossref"] or cs.status_retraksi(r["doi"]))

    def test_teks_penuh_pmc(self):
        with tempfile.TemporaryDirectory() as d:
            kode = cs.teks_penuh("10.1371/journal.pmed.0020124", d)
            self.assertEqual(kode, 0)
            berkas = list(Path(d).glob("*.md"))
            self.assertEqual(len(berkas), 1)
            isi = berkas[0].read_text(encoding="utf-8")
            self.assertTrue(isi.startswith("Sumber: https://doi.org/10.1371/journal.pmed.0020124"))
            self.assertIn("Why Most Published Research Findings Are False", isi)

    def test_garuda(self):
        hasil = cs.cari_garuda("stunting posyandu", 3)
        self.assertTrue(hasil, "Garuda tidak memberi hasil; mungkin tampilan situsnya berubah")
        self.assertTrue(all(r["judul"] and r["db"] == "Garuda" for r in hasil))


class TesKunciSemantic(unittest.TestCase):
    def setUp(self):
        self.lama = cs.S2_KEY

    def tearDown(self):
        cs.S2_KEY = self.lama

    def test_kunci_hanya_ke_semantic_scholar(self):
        cs.S2_KEY = "kunci-uji"
        self.assertEqual(cs._header("https://api.semanticscholar.org/graph/v1/paper/search")["x-api-key"], "kunci-uji")
        self.assertNotIn("x-api-key", cs._header("https://api.openalex.org/works"))

    def test_tanpa_kunci(self):
        cs.S2_KEY = ""
        self.assertNotIn("x-api-key", cs._header("https://api.semanticscholar.org/graph/v1/paper/search"))


class TesTeksPenuh(unittest.TestCase):
    W = {
        "best_oa_location": {"is_oa": True, "pdf_url": "https://jurnal.id/a.pdf", "landing_page_url": "https://jurnal.id/a",
                             "license": "cc-by", "version": "publishedVersion", "source": {"display_name": "Jurnal A"}},
        "locations": [
            {"is_oa": True, "pdf_url": "https://jurnal.id/a.pdf", "version": "publishedVersion"},  # duplikat best
            {"is_oa": True, "pdf_url": "https://arxiv.org/pdf/1", "version": "submittedVersion",
             "source": {"display_name": "arXiv"}},
            {"is_oa": False, "pdf_url": "https://berbayar.com/a.pdf", "version": "publishedVersion"},
        ],
        "ids": {"pmcid": "https://www.ncbi.nlm.nih.gov/pmc/articles/1182327"},
    }

    def test_lokasi_openalex_buang_duplikat_dan_tertutup(self):
        lok = cs.lokasi_dari_openalex(self.W)
        self.assertEqual([l["pdf"] for l in lok], ["https://jurnal.id/a.pdf", "https://arxiv.org/pdf/1"])

    def test_urutan_versi_terbit_dulu(self):
        lok = cs.urutkan_lokasi(list(reversed(cs.lokasi_dari_openalex(self.W))))
        self.assertEqual(lok[0]["versi"], "publishedVersion")

    def test_unpaywall(self):
        d = {"oa_locations": [{"url_for_pdf": "https://repo.ac.id/x.pdf", "url": "https://repo.ac.id/x",
                               "license": "cc-by", "version": "acceptedVersion", "host_type": "repository"}]}
        lok = cs.lokasi_dari_unpaywall(d)
        self.assertEqual(lok[0]["asal"], "Unpaywall (repository)")
        self.assertEqual(cs.lokasi_dari_unpaywall(None), [])

    def test_pmcid_tanpa_awalan(self):
        self.assertEqual(cs.pmcid_dari(self.W), "PMC1182327")
        self.assertEqual(cs.pmcid_dari({"ids": {"pmcid": "PMC99"}}), "PMC99")
        self.assertIsNone(cs.pmcid_dari({"ids": {}}))

    def test_jats_ke_teks(self):
        xml = ("<article><front><article-meta><title-group><article-title>Judul Uji</article-title></title-group>"
               "<abstract><p>Ringkasan <italic>singkat</italic>.</p></abstract></article-meta></front>"
               "<body><sec><title>Metode</title><p>Paragraf  satu.</p></sec></body></article>")
        teks = cs.jats_ke_teks(xml)
        self.assertEqual(teks.split("\n\n"), ["# Judul Uji", "## Abstrak", "Ringkasan singkat.", "## Metode", "Paragraf satu."])

    def test_nama_file_tidak_menimpa(self):
        with tempfile.TemporaryDirectory() as d:
            p1 = cs.nama_file_teks(d, ["Yasinta Indah Widyaningsih"], 2026)
            self.assertTrue(p1.endswith("widyaningsih-2026.md"))
            Path(p1).write_text("x", encoding="utf-8")
            self.assertTrue(cs.nama_file_teks(d, ["Yasinta Indah Widyaningsih"], 2026).endswith("widyaningsih-2026-2.md"))
            self.assertTrue(cs.nama_file_teks(d, [], None).endswith("tanpa-penulis-tt.md"))

    def test_nama_pilihan_penulis(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(cs.path_dengan_nama(d, "Syafruddin 2019").endswith("syafruddin-2019.md"))

    def test_link_tanpa_folder_tidak_mengunduh(self):
        self.assertEqual(cs.teks_penuh("https://contoh.ac.id/artikel/download/1/2"), 0)


class TesGaruda(unittest.TestCase):
    HTML = '''<div class="ui"><div class="article-item">
        <a class="title-article" href="/documents/detail/111"><xmp>Bank Sampah &amp; Ekonomi Desa</xmp></a>
        <a class="author-article" href="/author/view/1"><xmp>Syafruddin, S</xmp></a>; <a class="author-article" href="/author/view/2"><xmp>Pamungkas, Binar Dwiyanto</xmp></a>
        <br><xmp class="subtitle-article"> Jurnal Ekonomi &amp; Bisnis Vol 7 No 3 (2019): Desember </xmp>
        <p class="action-article"><a class="title-citation" href="https://j.ac.id/article/download/539/787" target="_blank">
            <i class="download icon"></i> Download Original</a>
        | <i><a class="title-citation" href="https://j.ac.id/article/view/539/787" target="_blank">
            Original Source</a></i></p>
        <div class="abstract-article"><xmp class="abstract-article">Penelitian ini menghitung nilai sampah.</xmp></div>
    </div><div class="article-item">
        <a class="title-article" href="/documents/detail/222"><xmp>Kader Posyandu dan Stunting</xmp></a>
        <xmp class="subtitle-article"> Amerta Nutrition Vol. 8 No. 3SP (2024): Edisi Khusus </xmp>
        <a class="title-citation" target="_blank" href="https://doi.org/10.20473/amnt.v8i3SP.2024.61-70">DOI</a>
    </div></div>'''

    def test_parse(self):
        r1, r2 = cs.parse_garuda(self.HTML)
        self.assertEqual(r1["judul"], "Bank Sampah & Ekonomi Desa")
        self.assertEqual(r1["penulis"], ["S Syafruddin", "Binar Dwiyanto Pamungkas"])
        self.assertEqual((r1["tahun"], r1["sumber"]), (2019, "Jurnal Ekonomi & Bisnis"))
        self.assertEqual(r1["doi"], "")
        self.assertEqual(r1["pdf"], "https://j.ac.id/article/download/539/787")
        self.assertEqual(r1["url"], "https://j.ac.id/article/view/539/787")
        self.assertEqual(r1["abstrak"], "Penelitian ini menghitung nilai sampah.")
        self.assertTrue(r1["oa"])
        self.assertEqual(r2["doi"], "10.20473/amnt.v8i3sp.2024.61-70")
        self.assertEqual(r2["url"], cs.GARUDA + "/documents/detail/222")
        self.assertFalse(r2["oa"])

    def test_tampilan_berubah_hasil_kosong(self):
        self.assertEqual(cs.parse_garuda("<html><body>Maintenance</body></html>"), [])
        self.assertEqual(cs.parse_garuda(None), [])

    def test_terdaftar_di_db(self):
        self.assertIs(cs.DB["garuda"], cs.cari_garuda)


class TesUtf8(unittest.TestCase):
    def test_output_dipipe_tidak_crash(self):
        """Di Windows stdout yang di-pipe memakai cp1252; emoji dulu membuat cari_sumber crash."""
        env = dict(os.environ, PYTHONIOENCODING="cp1252")
        r = subprocess.run([sys.executable, str(TOOLS / "cari_sumber.py"), "--help"], capture_output=True, env=env)
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
        kode = "import sys; sys.argv=['x']; sys.path.insert(0, r'%s'); import cari_sumber as c; print('✅⚠️❌⛔❓')" % TOOLS
        r = subprocess.run([sys.executable, "-c", kode], capture_output=True, env=env)
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))


# ---------------------------------------------------------------- cek_naskah
PUSTAKA = """
LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature.
Santoso, B., & Wibowo, A. (2021). Judul. Jurnal.
World Health Organization [WHO]. (2021). Report.
Kementerian Kesehatan Republik Indonesia [Kemenkes]. (2023). Profil Kesehatan.
Badan Pusat Statistik. (2022). Statistik.
Smith, J. (2020). A. Jurnal.
Smith, J. (2021). B. Jurnal.
Park, S. dkk. (2019). C.
"""


class TesSitasi(unittest.TestCase):
    def cek(self, isi):
        return cn.cocokkan_sitasi(cn.sitasi_teks(isi), cn.entri_pustaka(PUSTAKA))

    def test_semua_cocok(self):
        isi = ("Menurut LeCun dkk. (2015) dan Santoso dan Wibowo (2021), datanya kuat (World Health Organization [WHO], 2021). "
               "Lalu (WHO, 2021; Kemenkes, 2023). Badan Pusat Statistik (2022) mencatat. "
               "Temuan serupa (Smith, 2020, 2021) dan (Park et al., 2019).")
        yatim, tak = self.cek(isi)
        self.assertEqual(yatim, [])
        self.assertEqual(tak, [])

    def test_abaikan_bukan_sitasi(self):
        st = cn.sitasi_teks("Survei (Maret 2024) dengan biaya (Rp 1500) dan (n = 30).")
        self.assertEqual(st, set())

    def test_sitasi_yatim(self):
        yatim, _ = self.cek("Data baru (Unicef, 2020).")
        self.assertEqual(yatim, [("unicef", "2020")])

    def test_singkatan_tanpa_alias(self):
        ep = cn.entri_pustaka("Kementerian Kesehatan. (2023). Profil.\n")
        yatim, _ = cn.cocokkan_sitasi(cn.sitasi_teks("(Kemenkes, 2023)"), ep)
        self.assertEqual(len(yatim), 1)


class TesCekNaskah(unittest.TestCase):
    def test_penanda_perlu_seragam(self):
        t = "a [PERLU SUMBER] b [PERLU DATA: biaya] c [PERLU RUJUKAN: survei] d [perlu sumber]"
        self.assertEqual(dict(cn.penanda_belum_beres(t))[cn.POLA_PERLU], 4)

    def test_nama_kata_utuh(self):
        self.assertTrue(cn.ada_kata("Ani", "Ditulis oleh Ani."))
        self.assertFalse(cn.ada_kata("Ani", "Organik dan manisan."))

    def test_frasa_kata_utuh(self):
        self.assertFalse(cn.ada_kata("sinergi", "Kerja sinergis."))
        self.assertTrue(cn.ada_kata("dewasa ini", "Dewasa ini, banyak."))

    def test_hitung_angka_ribuan(self):
        self.assertEqual(cn.hitung_kata("Ada 1.000 siswa dan 2,5 persen."), 6)

    def test_kemiripan_lewati_dossier(self):
        with tempfile.TemporaryDirectory() as d:
            kalimat = "satu dua tiga empat lima enam tujuh delapan sembilan"
            tulis(d, "riset/dossier.md", kalimat)
            temuan, nb = cn.cek_kemiripan(kalimat, [str(Path(d) / "riset")])
            self.assertEqual((temuan, nb), ([], 0))
            tulis(d, "riset/teks/paper.md", kalimat)
            temuan, nb = cn.cek_kemiripan(kalimat, [str(Path(d) / "riset")])
            self.assertEqual(nb, 1)
            self.assertEqual(len(temuan), 1)

    def test_bom_dan_pipe(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.md"
            p.write_text("﻿# Judul\n\nIsi – dengan tanda · [PERLU DATA: x].\n\n## Daftar Pustaka\n", encoding="utf-8")
            env = dict(os.environ, PYTHONIOENCODING="cp1252")
            r = subprocess.run([sys.executable, str(TOOLS / "cek_naskah.py"), str(p)], capture_output=True, env=env)
            self.assertEqual(r.returncode, 1)
            self.assertIn("[PERLU ...]", r.stdout.decode("utf-8"))


# ---------------------------------------------------------------- cek_klaim
class TesCekKlaim(unittest.TestCase):
    PETA = """| ID | Klaim di naskah | Sumber (# di sumber.md) | Kutipan verbatim (≤40 kata) | Hlm/Tabel | Status |
|---|---|---|---|---|---|
| K1 | Prevalensi 21,6% | 3 | "prevalence was 21.6%" | Tabel 2 | ✅ |
| K2 | Biaya Rp1,2 juta | 4 | "Rp1.200.000 per bulan" | hlm 5 | ⚠️ |
"""

    def test_angka_dan_id(self):
        naskah = ("Prevalensinya 21,6% pada 2023 <!--K1-->. Biayanya Rp1,2 juta <!--K2-->. "
                  "Sekitar 45% siswa <!--K9-->. Ada 3 kelompok.")
        hasil = ck.periksa(naskah, self.PETA)
        self.assertIn("K9", hasil["id_tak_dikenal"])
        self.assertIn("K2", hasil["id_belum_terverifikasi"])
        self.assertIn("45%", [a for a, _ in hasil["angka_tanpa_klaim"]])
        self.assertNotIn("21,6%", [a for a, _ in hasil["angka_tanpa_klaim"]])

    def test_normalisasi_angka(self):
        self.assertEqual(ck.norm_angka("21,6%"), ck.norm_angka("21.6 %"))
        self.assertEqual(ck.norm_angka("Rp1.200.000"), ck.norm_angka("Rp 1.200.000"))


# ---------------------------------------------------------------- arena
class TesArena(unittest.TestCase):
    def test_acak_tetap_dengan_seed(self):
        self.assertEqual(arena.acak(list("abcdef"), 7), arena.acak(list("abcdef"), 7))

    def test_median_dan_gerbang(self):
        juri = [
            {"juri": "J1", "nilai": [{"id": "A", "lulus_gerbang": True, "skor": {"K1": 8, "K2": 7}, "total": 7.5},
                                     {"id": "B", "lulus_gerbang": False, "skor": {}, "total": 0}]},
            {"juri": "J2", "nilai": [{"id": "A", "lulus_gerbang": True, "skor": {"K1": 6, "K2": 7}, "total": 6.5},
                                     {"id": "B", "lulus_gerbang": True, "skor": {"K1": 9}, "total": 9}]},
            {"juri": "J3", "nilai": [{"id": "A", "lulus_gerbang": True, "skor": {"K1": 7, "K2": 8}, "total": 7.0},
                                     {"id": "B", "lulus_gerbang": False, "skor": {}, "total": 0}]},
        ]
        rek = arena.rekap(juri)
        self.assertEqual(rek["A"]["median"], 7.0)
        self.assertTrue(rek["B"]["gugur"])  # mayoritas juri menggugurkan di gerbang

    def test_poin_adu_seri_kalau_tidak_sepakat(self):
        adu = [{"a": "A", "b": "B", "urutan": 1, "menang": "A"},
               {"a": "B", "b": "A", "urutan": 2, "menang": "B"},
               {"a": "A", "b": "C", "urutan": 1, "menang": "A"},
               {"a": "C", "b": "A", "urutan": 2, "menang": "A"}]
        poin = arena.poin_adu(adu)
        self.assertEqual(poin["A"], 1.5)
        self.assertEqual(poin["B"], 0.5)
        self.assertEqual(poin["C"], 0)

    def _juri_terbelah(self):
        # D disukai satu juri saja (nilai tertinggi J3 + dibela J3), median rendah
        def j(nama, nilai, bela):
            return {"juri": nama, "bela": bela, "nilai": [
                {"id": i, "lulus_gerbang": True, "skor": {"K1": 5, "K2": 5}, "total": t} for i, t in nilai.items()]}
        return [j("J1", {"A": 8.0, "B": 7.8, "C": 7.0, "D": 4.0, "E": 5.0}, "A"),
                j("J2", {"A": 7.9, "B": 7.7, "C": 6.5, "D": 4.5, "E": 5.5}, "A"),
                j("J3", {"A": 6.0, "B": 6.0, "C": 6.0, "D": 9.0, "E": 5.0}, "D")]

    def test_kartu_liar_menyelamatkan_ide_yang_memecah_juri(self):
        h = arena.rekap(self._juri_terbelah())
        urut = arena.peringkat(h)
        self.assertNotIn("D", urut[:3])
        liar = dict(arena.kartu_liar(h, urut, 3))
        self.assertIn("D", liar)
        self.assertNotIn("E", liar)  # tanpa sinyal apa pun
        self.assertEqual(h["D"]["n_bela"], 1)
        self.assertEqual(h["D"]["n_teratas"], 1)

    def test_kartu_liar_dari_kesan_30_detik(self):
        h = arena.rekap(self._juri_terbelah())
        liar = dict(arena.kartu_liar(h, arena.peringkat(h), 3, {"E": "berhenti"}))
        self.assertIn("E", liar)

    def test_seri_di_puncak(self):
        h = arena.rekap(self._juri_terbelah())
        self.assertEqual(arena.seri_puncak(h, arena.peringkat(h), 0.5), ["A", "B"])

    def test_mirip_menandai_kartu_kembar_saja(self):
        teks = """### I01. Apotek Menolak Antibiotik Tanpa Resep
- Lensa: inversi
- Inti ide: apoteker menolak penjualan antibiotik tanpa resep dengan skrip penolakan ramah
### [I02] Skrip Tunda Antibiotik
- Kenapa tidak pasaran: berbeda
- Inti ide: apoteker menunda penjualan antibiotik tanpa resep dengan skrip penolakan ramah
### I03. Kapsul Karagenan Lokal
- Inti ide: rumput laut lokal diolah jadi cangkang kapsul pengganti gelatin impor
"""
        kartu = arena.baca_kartu(teks)
        self.assertEqual(sorted(kartu), ["I01", "I02", "I03"])
        self.assertNotIn("inversi", kartu["I01"])  # baris Lensa dibuang
        pas = [(a, b) for a, b, _ in arena.mirip(kartu)]
        self.assertIn(("I01", "I02"), pas)
        self.assertNotIn(("I01", "I03"), pas)


# ---------------------------------------------------------------- evaluasi (tahap 8)
class TesEvaluasi(unittest.TestCase):
    def test_spearman_dengan_nilai_kembar(self):
        self.assertAlmostEqual(ev.spearman([1, 2, 3, 4], [10, 20, 30, 40]), 1.0)
        self.assertAlmostEqual(ev.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)
        self.assertEqual(ev.peringkat_rata([5, 5, 1]), [2.5, 2.5, 1.0])
        self.assertIsNone(ev.spearman([1, 2], [1, 2]))  # terlalu sedikit data
        self.assertIsNone(ev.spearman([3, 3, 3], [1, 2, 3]))  # tanpa variasi

    def _tulis(self, folder, nama, isi):
        p = Path(folder) / nama
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(isi), encoding="utf-8")

    def test_juri_kelompok_jangkar_dan_panel_vs_adu(self):
        with tempfile.TemporaryDirectory() as d:
            def juri(nama, nilai):
                return {"juri": nama, "nilai": [{"id": i, "lulus_gerbang": True, "skor": {"K1": 5, "K2": 5},
                                                 "total": t} for i, t in nilai.items()]}
            self._tulis(d, "ide/juri/loop-1-J1.json", juri("J1", {"I01": 8, "I02": 6, "I03": 5, "X01": 7}))
            self._tulis(d, "ide/juri/loop-1-J2.json", juri("J2", {"I01": 7, "I02": 6, "I03": 4, "X01": 8}))
            self._tulis(d, "ide/juri/kesan-loop-1.json", {"I01": "berhenti"})  # bukan file juri
            self._tulis(d, "ide/juri/final-J1.json", juri("F1", {"I01": 8, "I02": 7}))
            self._tulis(d, "ide/adu-final.json", [{"a": "I01", "b": "I02", "urutan": 1, "menang": "I02"},
                                                   {"a": "I02", "b": "I01", "urutan": 2, "menang": "I02"}])
            grup = ev.kelompok_juri(Path(d) / "ide" / "juri")
            self.assertEqual(sorted(grup), ["final", "loop-1"])
            st = ev.statistik_kelompok(grup["loop-1"])
            self.assertEqual(st["jangkar"]["X01"], 67)  # di atas 2 dari 3 ide lain
            lap = ev.laporan_juri(d)
            self.assertIn("BERBEDA", lap)  # panel memilih I01, adu memilih I02

    def test_rekap_hasil_dan_peringatan_data_kurang(self):
        with tempfile.TemporaryDirectory() as d:
            for nama, status in (("lomba-a", "juara"), ("lomba-b", "tidak lolos"), ("_template", "juara")):
                (Path(d) / nama).mkdir()
                (Path(d) / nama / "STATUS.md").write_text("x", encoding="utf-8")
                self._tulis(Path(d) / nama, "hasil.json", {"dikirim": True, "hasil": {"status": status},
                                                           "arena": {"jangkar_persentil": 80},
                                                           "uji_balik": {"dijalankan": True,
                                                                         "juri_ai_pilih_juara_asli": status == "juara"}})
            (Path(d) / "lomba-c").mkdir()
            (Path(d) / "lomba-c" / "STATUS.md").write_text("x", encoding="utf-8")
            r = ev.ringkas_hasil(ev.baca_hasil(d))
            self.assertEqual(r["n"], 2)  # _template dilewati
            self.assertEqual(r["n_diketahui"], 2)
            self.assertFalse(r["cukup_untuk_strategi"])
            self.assertEqual((r["n_uji"], r["n_setuju"]), (2, 1))
            lap = ev.laporan_rekap(d)
            self.assertIn("lomba-c (8a belum", lap)
            self.assertIn("Belum cukup", lap)


# ---------------------------------------------------------------- build_docx
@unittest.skipUnless(ADA_DOCX, "python-docx belum terpasang")
class TesBuildDocx(unittest.TestCase):
    MD = """# Judul Uji

Paragraf pertama dengan **tebal** dan *miring*.

### Sub-subjudul

- butir satu
- butir dua

1. nomor satu
2. nomor dua

| A | B |
|:-:|---|
| 1 | 2 |

## daftar pustaka
LeCun, Y. (2015). Deep learning. Nature.
Smith, J. (2020). Lain. Jurnal.
- Park, S. (2019). Butir.

## Lampiran

![Alt teks](tidak-ada.png)
*Gambar 1. Keterangan asli*
"""

    def bangun(self, profil, md=None):
        with tempfile.TemporaryDirectory() as d:
            tulis(d, "p.json", json.dumps(profil))
            md_p = tulis(d, "x.md", md or self.MD)
            out = Path(d) / "out.docx"
            peringatan = bd.build(str(md_p), bd.muat_profil(str(Path(d) / "p.json")), str(out))
            doc = docx.Document(str(out))
            with zipfile.ZipFile(out) as z:
                header = "".join(z.read(n).decode("utf-8") for n in z.namelist() if n.startswith("word/header"))
            return doc, peringatan, header

    def test_lengkap(self):
        doc, _, _ = self.bangun({"kertas": "F4", "gambar_hanya_di_lampiran": False})
        teks = [p.text for p in doc.paragraphs]
        self.assertAlmostEqual(doc.sections[0].page_height.cm, 33.0, places=1)
        self.assertIn("Sub-subjudul", teks)
        self.assertNotIn("### Sub-subjudul", teks)
        self.assertIn("butir satu", teks)
        self.assertIn("nomor dua", teks)
        for e in ("LeCun, Y. (2015). Deep learning. Nature.", "Smith, J. (2020). Lain. Jurnal.", "Park, S. (2019). Butir."):
            self.assertIn(e, teks)  # satu entri = satu paragraf
        self.assertIn("Gambar 1. Keterangan asli", teks)
        self.assertEqual(len(doc.tables[0].rows), 2)  # baris |:-:| dibuang
        self.assertEqual(doc.core_properties.author, "")
        self.assertEqual(doc.core_properties.last_modified_by, "")

    def test_profil_null_dan_tengah_atas(self):
        doc, _, header = self.bangun({"kertas": None, "margin_cm": None, "nomor_halaman": "tengah_atas"})
        self.assertAlmostEqual(doc.sections[0].page_height.cm, 29.7, places=1)
        self.assertIn("PAGE", header)

    def test_kertas_tidak_dikenal(self):
        with self.assertRaises(SystemExit):
            self.bangun({"kertas": "B5"})

    def test_build_ditolak_kalau_ada_penanda(self):
        with tempfile.TemporaryDirectory() as d:
            md_p = tulis(d, "x.md", "# J\n\nAngka [PERLU DATA: survei].\n")
            r = subprocess.run([sys.executable, str(TOOLS / "build_docx.py"), str(md_p), "--out", str(Path(d) / "o.docx")],
                               capture_output=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertFalse((Path(d) / "o.docx").exists())


    def test_tampilan_profesional(self):
        md = """# Judul

## Bagian Satu

Paragraf isi yang merujuk Gambar 1 menunjukkan sesuatu.

Tabel 1. Perbandingan
| A | B |
|---|---|
| 1 | 2 |
Sumber: data uji.
"""
        doc, _, _ = self.bangun({"gambar_hanya_di_lampiran": False}, md)
        par = {p.text: p for p in doc.paragraphs}
        self.assertEqual(par["Bagian Satu"].style.name, "Heading 1")
        self.assertTrue(par["Bagian Satu"].paragraph_format.keep_with_next)
        self.assertEqual(doc.styles["Heading 1"].font.color.rgb, docx.shared.RGBColor(0, 0, 0))
        self.assertTrue(par["Tabel 1. Perbandingan"].paragraph_format.keep_with_next)
        self.assertIn("Sumber: data uji.", par)
        # paragraf biasa yang diawali "Gambar 1 menunjukkan" bukan keterangan
        self.assertAlmostEqual(par["Paragraf isi yang merujuk Gambar 1 menunjukkan sesuatu."].paragraph_format.first_line_indent.cm, 1.0, places=2)
        xml = doc.tables[0]._tbl.xml
        self.assertIn('w:insideV w:val="nil"', xml)  # tiga garis: tanpa garis tegak
        self.assertNotIn("TableGrid", xml)


# ---------------------------------------------------------------- cek_docx
@unittest.skipUnless(ADA_DOCX, "python-docx belum terpasang")
class TesCekDocx(unittest.TestCase):
    def test_bersih_dan_kotor(self):
        import cek_docx
        from docx.shared import RGBColor
        with tempfile.TemporaryDirectory() as d:
            md_p = tulis(d, "x.md", "# Judul\n\nParagraf biasa (Penulis, 2023).\n\n## Daftar Pustaka\n\nPenulis, A. (2023). Judul.\n")
            bersih = Path(d) / "bersih.docx"
            bd.build(str(md_p), bd.muat_profil(None), str(bersih))
            self.assertEqual([t for t, _ in cek_docx.periksa(str(bersih), bd.muat_profil(None)) if t != "INFO"], [])
            kotor = docx.Document()
            kotor.add_paragraph("Judul \U0001F680")
            r = kotor.add_paragraph().add_run("Kalimat panjang sekali yang sengaja dibuat tebal dan berwarna supaya terdeteksi alat, "
                                            "lebih dari 120 huruf supaya tidak dikira judul bagian — ya — ya — ya.")
            r.bold = True
            r.font.color.rgb = RGBColor(0x80, 0, 0x80)
            r.font.name = "Arial"
            for _ in range(3):
                kotor.add_paragraph("")
            kotor.core_properties.author = "Nama Asli"
            p_kotor = Path(d) / "kotor.docx"
            kotor.save(str(p_kotor))
            temuan = cek_docx.periksa(str(p_kotor), {"font": "Times New Roman"})
            teks = " ".join(m for _, m in temuan)
            for kata in ("Emoji", "Arial", "berwarna", "tebal", "paragraf kosong", "Nama Asli"):
                self.assertIn(kata, teks)


# ---------------------------------------------------------------- buat_visual
try:
    import matplotlib  # noqa: F401
    ADA_MPL = True
except ImportError:
    ADA_MPL = False


@unittest.skipUnless(ADA_MPL, "matplotlib belum terpasang")
class TesBuatVisual(unittest.TestCase):
    def test_semua_jenis(self):
        import buat_visual
        spek = {
            "batang": {"jenis": "batang", "label": ["a", "b"], "seri": [{"nama": "x", "nilai": [1, 2.5]}], "sorot": 1, "sumber": "Uji (2026)"},
            "garis": {"jenis": "garis", "label": ["2020", "2021"], "seri": [{"nama": "x", "nilai": [1, 2]}, {"nama": "y", "nilai": [2, 1]}], "sumber": "Uji"},
            "alur": {"jenis": "alur", "langkah": ["satu", {"teks": "dua", "utama": True}]},
            "siklus": {"jenis": "siklus", "langkah": ["a", "b", "c"]},
        }
        with tempfile.TemporaryDirectory() as d:
            for nama, isi in spek.items():
                p = tulis(d, f"{nama}.json", json.dumps(isi))
                buat_visual.buat(str(p), {}, str(Path(d) / "gambar"))
                self.assertGreater((Path(d) / "gambar" / f"{nama}.png").stat().st_size, 1000)

    def test_jenis_tidak_dikenal(self):
        import buat_visual
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "x.json", json.dumps({"jenis": "pai"}))
            with self.assertRaises(SystemExit):
                buat_visual.buat(str(p), {}, d)

    def _temuan(self, spek, profil=None):
        import buat_visual
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "v.json", json.dumps(spek))
            return buat_visual.buat(str(p), profil or {}, d)

    def test_grafik_normal_tanpa_temuan(self):
        self.assertEqual(self._temuan({"jenis": "batang", "label": ["2020", "2021", "2022"],
                                       "seri": [{"nama": "x", "nilai": [3, 5, 4]}], "sumber": "Uji"}), [])
        self.assertEqual(self._temuan({"jenis": "siklus", "langkah": ["Pantau", "Analisis", "Intervensi", "Evaluasi"]}), [])

    def test_label_panjang_bertumpuk(self):
        label = ["Kabupaten Kepulauan Seribu Utara", "Kabupaten Kepulauan Seribu Selatan",
                 "Kota Administrasi Jakarta Pusat", "Kota Administrasi Jakarta Timur"]
        temuan = self._temuan({"jenis": "batang", "label": label, "seri": [{"nama": "x", "nilai": [1, 2, 3, 4]}], "sumber": "Uji"})
        self.assertTrue(any("bertumpuk" in t for t in temuan))
        self.assertLessEqual(len(temuan), 3)

    def test_teks_keluar_kotak(self):
        temuan = self._temuan({"jenis": "siklus", "langkah": ["Pemantauanberkelanjutanterintegrasiberbasisdata", "B", "C"]})
        self.assertTrue(any("keluar dari kotak" in t for t in temuan))

    def test_huruf_tercetak_terlalu_kecil(self):
        # grafik selebar 40 cm diperkecil ke 14 cm saat dicetak, jadi huruf 9–10 pt menjadi ±3 pt
        besar = {"jenis": "batang", "lebar_cm": 40, "tinggi_cm": 20, "label": ["a", "b"],
                 "seri": [{"nama": "x", "nilai": [1, 2]}], "sumber": "Uji"}
        self.assertTrue(any("huruf terkecil" in t for t in self._temuan(besar)))
        # diagram alur kecil dengan catatan 7,5 pt justru diperbesar ke 14 cm, jadi hurufnya cukup besar
        alur = {"jenis": "alur", "langkah": [{"teks": "Kader mencatat", "catatan": "setiap bulan"}, "Puskesmas merekap"]}
        self.assertFalse(any("huruf terkecil" in t for t in self._temuan(alur)))


# ---------------------------------------------------------------- cek_pptx
try:
    import pptx  # noqa: F401
    ADA_PPTX = True
except ImportError:
    ADA_PPTX = False


@unittest.skipUnless(ADA_PPTX, "python-pptx belum terpasang")
class TesCekPptx(unittest.TestCase):
    def deck(self, folder, kotor):
        from pptx import Presentation
        from pptx.dml.color import RGBColor
        from pptx.util import Inches, Pt
        p = Presentation()
        s = p.slides.add_slide(p.slide_layouts[0])
        s.shapes.title.text = ("\U0001F680 " if kotor else "") + "Verifikasi obat dari kemasan"
        s.notes_slide.notes_text_frame.text = "Pembuka."
        s = p.slides.add_slide(p.slide_layouts[1] if kotor else p.slide_layouts[5])
        s.shapes.title.text = "Latar Belakang" if kotor else "Kasus obat ilegal naik 75% dalam tiga tahun"
        s.notes_slide.notes_text_frame.text = "Naskah."
        if kotor:
            tf = s.placeholders[1].text_frame
            for k in range(6):
                r = tf.add_paragraph().add_run()
                r.text = "Poin panjang nomor %d yang menjelaskan banyak hal sekaligus" % k
                r.font.size = Pt(14)
            sh = s.shapes.add_shape(1, Inches(1), Inches(1), Inches(2), Inches(1))
            sh.fill.gradient()
            sh.fill.gradient_stops[0].color.rgb = RGBColor(0x8B, 0x5C, 0xF6)
            sh.fill.gradient_stops[1].color.rgb = RGBColor(0x3B, 0x82, 0xF6)
        else:
            tb = s.shapes.add_textbox(Inches(1), Inches(5), Inches(6), Inches(1))
            r = tb.text_frame.paragraphs[0].add_run()
            r.text = "Sumber: Kemenkes (2024)"
            r.font.size = Pt(12)
        s = p.slides.add_slide(p.slide_layouts[5])
        s.shapes.title.text = "Satu pindaian cukup untuk tahu obat itu terdaftar"
        s.notes_slide.notes_text_frame.text = "Penutup."
        path = Path(folder) / ("kotor.pptx" if kotor else "bersih.pptx")
        p.save(str(path))
        return path

    def test_kotor_dan_bersih(self):
        import cek_pptx
        with tempfile.TemporaryDirectory() as d:
            temuan = cek_pptx.cek(self.deck(d, True), durasi=5)
            teks = " ".join(m for _, m in temuan)
            for kata in ("emoji", "gradasi bernada ungu", "butir", "14 pt", "judul berupa label"):
                self.assertIn(kata, teks)
            self.assertEqual([t for t, _ in cek_pptx.cek(self.deck(d, False), durasi=5) if t != "INFO"], [])

    def test_gaya(self):
        import cek_pptx
        with tempfile.TemporaryDirectory() as d:
            hasil = cek_pptx.gaya(self.deck(d, True))
            self.assertIn("jumlah slide: 3", hasil)
            self.assertIn("#8B5CF6", hasil)


if __name__ == "__main__":
    unittest.main()
