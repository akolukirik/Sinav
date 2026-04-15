# -*- coding: utf-8 -*-
"""
MEB İlk Yardım soru bankası PDF -> data/meb/meb-*.json + assets/meb-veriler.js
Çalıştır: PYTHONPATH=.pdf_tools python3 scripts/import_meb_bank.py [pdf_yolu]
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    from pypdf import PdfReader
except ImportError:
    sys.path.insert(0, os.path.join(ROOT, ".pdf_tools"))
    from pypdf import PdfReader

DEFAULT_PDF = os.path.expanduser("~/Downloads/22211745_SORU_BANKASI_2.pdf")
PER_EXAM = 20
OUT_DIR = os.path.join(ROOT, "data", "meb")
ASSETS = os.path.join(ROOT, "assets")


def parse_pdf(path):
    r = PdfReader(path)
    key_text = r.pages[-1].extract_text() or ""
    answers = {int(m.group(1)): m.group(2) for m in re.finditer(r"(\d+)\.([A-D])\b", key_text)}
    full = "\n".join((r.pages[i].extract_text() or "") for i in range(len(r.pages) - 2))
    LET = {"A": 0, "B": 1, "C": 2, "D": 3}
    parts = re.split(r"(?:^|\n)\s*(\d+)\.\s+", full)
    parsed = []
    for i in range(1, len(parts), 2):
        qid = int(parts[i])
        chunk = parts[i + 1].strip()
        segs = re.split(r"(?=[ABCD]\)\s*)", chunk)
        if len(segs) < 5:
            raise ValueError("Soru %s: A-D şıkları eksik (%d parça)" % (qid, len(segs)))
        stem = re.sub(r"\s+", " ", segs[0].strip())
        opts = []
        for j in range(1, 5):
            t = re.sub(r"^[ABCD]\)\s*", "", segs[j].strip())
            t = re.sub(r"\s+", " ", t)
            opts.append(t)
        letter = answers.get(qid)
        if not letter:
            raise ValueError("Soru %s: cevap anahtarında yok" % qid)
        parsed.append({"id": qid, "text": stem, "options": opts, "correct": LET[letter]})
    parsed.sort(key=lambda x: x["id"])
    return parsed


def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF
    if not os.path.isfile(pdf):
        print("PDF bulunamadı:", pdf)
        sys.exit(1)
    all_q = parse_pdf(pdf)
    n = len(all_q)
    usable = (n // PER_EXAM) * PER_EXAM
    chunks = [all_q[i : i + PER_EXAM] for i in range(0, usable, PER_EXAM)]
    print("Toplam soru:", n, "->", len(chunks), "sınav x", PER_EXAM, "(kullanılmayan son", n - usable, "soru)")

    os.makedirs(OUT_DIR, exist_ok=True)
    embedded = []
    for idx, questions in enumerate(chunks, start=1):
        title = "MEB Soru Bankası — Set %d/%d" % (idx, len(chunks))
        payload = {"title": title, "questions": [{k: v for k, v in q.items() if k != "id"} for q in questions]}
        fn = "meb-%d.json" % idx
        with open(os.path.join(OUT_DIR, fn), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        embedded.append({"id": str(idx), "title": title, "questions": payload["questions"]})

    out_js = os.path.join(ASSETS, "meb-veriler.js")
    with open(out_js, "w", encoding="utf-8") as f:
        f.write("// MEB soru bankası — import_meb_bank.py ile üretildi\n")
        f.write("window.MEB_EXAMS = ")
        json.dump(embedded, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("Yazıldı:", OUT_DIR, "ve", out_js)


if __name__ == "__main__":
    main()
