"""Unduh poster lomba dan baca semua QR code di dalamnya.

Pemakaian:
  python -I qr.py <folder_output> <nama> <url1> [<url2> ...]
      Unduh tiap URL gambar ke <folder_output>/<nama>_<i>.jpg, pindai semua QR,
      dan buat salinan kecil (lebar 720 px) di <folder_output>/small/ untuk dibaca.

  python -I qr.py --crop <gambar.jpg> <x0> <y0> <x1> <y1>
      Pindai QR hanya di satu kotak (koordinat pecahan 0..1 dari lebar/tinggi).
      Dipakai untuk menentukan QR mana yang "Guidebook/Juknis" kalau poster punya banyak QR.

  python -I qr.py --small <gambar.jpg> [...]
      Buat salinan 720 px saja (hemat token saat membaca poster).

Butuh: pip install opencv-python-headless
"""
import os
import sys
import urllib.request

import cv2
import numpy as np


def _detectors():
    dets = [cv2.QRCodeDetector()]
    try:
        dets.append(cv2.QRCodeDetectorAruco())
    except Exception:
        pass
    return dets


def decode_all(img):
    """Kembalikan semua teks QR yang terbaca dari beberapa variasi gambar."""
    found = set()
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variants = [
        img,
        cv2.resize(img, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC),
        cv2.cvtColor(cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1], cv2.COLOR_GRAY2BGR),
    ]
    # Potongan 3x3 yang saling tumpang-tindih supaya QR kecil ikut terbaca
    for ty in range(3):
        for tx in range(3):
            tile = img[ty * h // 3: min(h, (ty + 2) * h // 3), tx * w // 3: min(w, (tx + 2) * w // 3)]
            if tile.size:
                variants.append(cv2.resize(tile, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC))
    for v in variants:
        for d in _detectors():
            try:
                ok, texts, _, _ = d.detectAndDecodeMulti(v)
                if ok:
                    found.update(t for t in texts if t)
            except Exception:
                pass
            try:
                t, _, _ = d.detectAndDecode(v)
                if t:
                    found.add(t)
            except Exception:
                pass
    return found


def make_small(path, outdir=None):
    im = cv2.imread(path)
    h, w = im.shape[:2]
    outdir = outdir or os.path.join(os.path.dirname(path), "small")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, os.path.basename(path))
    cv2.imwrite(out, cv2.resize(im, (720, int(h * 720 / w)), interpolation=cv2.INTER_AREA),
                [cv2.IMWRITE_JPEG_QUALITY, 80])
    return out


def crop_decode(path, x0, y0, x1, y1):
    im = cv2.imread(path)
    h, w = im.shape[:2]
    c = im[int(h * y0): int(h * y1), int(w * x0): int(w * x1)]
    c = cv2.resize(c, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    return decode_all(c)


def main(argv):
    if not argv:
        print(__doc__)
        return
    if argv[0] == "--crop":
        path, *box = argv[1:6]
        print(sorted(crop_decode(path, *map(float, box))) or "QR tidak terbaca")
        return
    if argv[0] == "--small":
        for p in argv[1:]:
            print(make_small(p))
        return
    outdir, name, urls = argv[0], argv[1], argv[2:]
    os.makedirs(outdir, exist_ok=True)
    for i, url in enumerate(urls, 1):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=30).read()
        img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        path = os.path.join(outdir, f"{name}_{i}.jpg")
        cv2.imwrite(path, img)
        make_small(path)
        qrs = decode_all(img)
        print(f"{name}_{i}: {img.shape[1]}x{img.shape[0]} QR={sorted(qrs) if qrs else 'tidak ada'}")


if __name__ == "__main__":
    main(sys.argv[1:])
