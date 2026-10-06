"""Generate past-paper PDFs (question papers + mark schemes) and a ZIP of everything.
Output: ../assets/docs/past-papers/    Requires: reportlab and the DejaVu Sans fonts."""
import os
import zipfile

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

from papers import PAPERS, part_b_marks, total_marks

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "docs", "past-papers")
GREEN = colors.HexColor("#0a6b3d")
BLUE = colors.HexColor("#0b5394")
INK = colors.HexColor("#10231a")
MUTED = colors.HexColor("#3d5247")

FONT_DIRS = ["/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu", "/Library/Fonts", os.path.expanduser("~/Library/Fonts")]


def find_font(file):
    return next((os.path.join(d, file) for d in FONT_DIRS if os.path.exists(os.path.join(d, file))), None)


def register_fonts():
    """DejaVu Sans covers Greek letters and maths symbols. Italic faces are optional:
    if they are not installed, italics fall back to the upright face."""
    regular, bold = find_font("DejaVuSans.ttf"), find_font("DejaVuSans-Bold.ttf")
    if not (regular and bold):
        raise SystemExit("DejaVu Sans not found. Install it (e.g. apt install fonts-dejavu-core) and run again.")
    italic = find_font("DejaVuSans-Oblique.ttf") or regular
    bold_italic = find_font("DejaVuSans-BoldOblique.ttf") or bold
    for name, path in [("DejaVu", regular), ("DejaVu-Bold", bold), ("DejaVu-Oblique", italic),
                       ("DejaVu-BoldOblique", bold_italic)]:
        pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold",
                                  italic="DejaVu-Oblique", boldItalic="DejaVu-BoldOblique")


def styles():
    base = dict(fontName="DejaVu", textColor=INK)
    return {
        "brand": ParagraphStyle("brand", fontSize=13, leading=18, textColor=GREEN, fontName="DejaVu-Bold"),
        "title": ParagraphStyle("title", fontSize=24, leading=30, textColor=GREEN, fontName="DejaVu-Bold", spaceAfter=6),
        "sub": ParagraphStyle("sub", fontSize=14, leading=20, textColor=BLUE, fontName="DejaVu-Bold", spaceAfter=4),
        "h2": ParagraphStyle("h2", fontSize=14, leading=19, textColor=GREEN, fontName="DejaVu-Bold", spaceBefore=10, spaceAfter=6),
        "h3": ParagraphStyle("h3", fontSize=11.5, leading=16, textColor=BLUE, fontName="DejaVu-Bold", spaceBefore=8, spaceAfter=3),
        "body": ParagraphStyle("body", fontSize=10.5, leading=15.5, spaceAfter=4, **base),
        "opt": ParagraphStyle("opt", fontSize=10.5, leading=15, leftIndent=26, firstLineIndent=-16, **base),
        "marks": ParagraphStyle("marks", fontSize=10.5, leading=15.5, alignment=2, fontName="DejaVu-Bold", textColor=MUTED),
        "small": ParagraphStyle("small", fontSize=9, leading=13, textColor=MUTED, fontName="DejaVu"),
        "scheme": ParagraphStyle("scheme", fontSize=9.5, leading=13.5, textColor=MUTED, fontName="DejaVu-Oblique",
                                 leftIndent=12, spaceAfter=6),
        "sol": ParagraphStyle("sol", fontSize=10.5, leading=15.5, leftIndent=12, spaceAfter=2, **base),
    }


def edition_title(p):
    return f"Sustainable Olympiad {p['year']}"


def footer_fn(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("DejaVu", 8.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(20 * mm, 12 * mm, text)
        canvas.drawRightString(190 * mm, 12 * mm, f"Page {doc.page}")
        canvas.setStrokeColor(colors.HexColor("#c9dbd0"))
        canvas.line(20 * mm, 16 * mm, 190 * mm, 16 * mm)
        canvas.restoreState()
    return draw


def marked(text, marks, S, prefix=""):
    """A question line with the mark allocation right-aligned."""
    t = Table([[Paragraph(prefix + text, S["body"]), Paragraph(f"[{marks}]", S["marks"])]],
              colWidths=[150 * mm, 15 * mm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def answer_space(marks):
    rows = max(2, marks + 1)
    t = Table([[""]] * rows, colWidths=[165 * mm], rowHeights=[7.5 * mm] * rows)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#b9cbbf"))]))
    return t


def file_names(p):
    stem = f"sustainable-olympiad-{p['id']}-round1"
    return f"{stem}-paper.pdf", f"{stem}-solutions.pdf"


def cover(p, S, kind):
    total = total_marks(p)
    s = [Paragraph("SUSTAINABLE OLYMPIAD", S["brand"]), Spacer(1, 30 * mm),
         Paragraph(f"{edition_title(p)}", S["title"]),
         Paragraph("Round 1: Online Knowledge Challenge", S["sub"]),
         Paragraph(f"{p['division']} Division (ages {p['ages']})", S["sub"]),
         Spacer(1, 6 * mm)]
    if kind == "paper":
        facts = [["Time allowed", f"{p['duration']} minutes"], ["Total marks", str(total)],
                 ["Part A", f"{len(p['part_a'])} multiple-choice questions, {2 * len(p['part_a'])} marks"],
                 ["Part B", f"{len(p['part_b'])} structured problems, {part_b_marks(p)} marks"]]
        t = Table([[Paragraph(f"<b>{a}</b>", S["body"]), Paragraph(b, S["body"])] for a, b in facts],
                  colWidths=[40 * mm, 125 * mm])
        t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9dbd0")),
                               ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        s += [t, Spacer(1, 8 * mm), Paragraph("Instructions", S["h2"])]
        for line in ["Answer <b>all</b> questions. Work together as a team.",
                     "Part A: choose <b>one</b> answer (A, B, C or D) for each question. There are no negative marks.",
                     "Part B: show all your working. Marks are given for correct method even if the final answer is wrong.",
                     "Give numerical answers to an appropriate number of significant figures, with units.",
                     "Scientific calculators are allowed. Internet access and AI tools are not allowed during the round.",
                     "A data sheet is provided on the next page."]:
            s.append(Paragraph("•  " + line, S["opt"]))
        s += [Spacer(1, 10 * mm)]
        t = Table([[Paragraph("<b>Team name</b>", S["body"]), ""], [Paragraph("<b>School</b>", S["body"]), ""]],
                  colWidths=[40 * mm, 125 * mm], rowHeights=[11 * mm, 11 * mm])
        t.setStyle(TableStyle([("BOX", (1, 0), (1, -1), 0.6, MUTED), ("INNERGRID", (1, 0), (1, -1), 0.6, MUTED),
                               ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        s.append(t)
    else:
        s += [Paragraph("Mark scheme and worked solutions", S["h2"]),
              Paragraph(f"Total: {total} marks. Accept answers within rounding and correct alternative methods. "
                        "Apply error carried forward (ECF): if a wrong value from an earlier part is used correctly "
                        "in a later part, award the method marks.", S["body"])]
    s.append(PageBreak())
    return s


def question_paper(p, S):
    s = cover(p, S, "paper")
    s.append(Paragraph("Data sheet", S["h2"]))
    s += [Paragraph("•  " + d, S["opt"]) for d in p["data"]]
    s.append(Spacer(1, 4 * mm))
    s.append(Paragraph(f"Part A: Multiple choice ({2 * len(p['part_a'])} marks)", S["h2"]))
    s.append(Paragraph("Each question is worth 2 marks. Choose one answer.", S["small"]))
    for i, q in enumerate(p["part_a"], 1):
        block = [Spacer(1, 3 * mm), marked(q["q"], 2, S, f"<b>A{i}.</b>  ")]
        block += [Paragraph(f"<b>{letter}</b>    {opt}", S["opt"]) for letter, opt in zip("ABCD", q["options"])]
        s.append(KeepTogether(block))
    s.append(PageBreak())
    s.append(Paragraph(f"Part B: Structured problems ({part_b_marks(p)} marks)", S["h2"]))
    for i, q in enumerate(p["part_b"], 1):
        qm = sum(x["marks"] for x in q["parts"])
        s.append(KeepTogether([Paragraph(f"B{i}. {q['title']}  ({qm} marks)", S["h3"]), Paragraph(q["stem"], S["body"])]))
        for j, part in enumerate(q["parts"]):
            s.append(KeepTogether([marked(part["text"], part["marks"], S, f"<b>({'abcdefg'[j]})</b>  "),
                                   answer_space(part["marks"]), Spacer(1, 2 * mm)]))
    s += [Spacer(1, 8 * mm), Paragraph("<b>END OF PAPER</b>", ParagraphStyle("end", parent=S["body"], alignment=1))]
    return s


def solutions(p, S):
    s = cover(p, S, "solutions")
    s.append(Paragraph("Part A: Answer key", S["h2"]))
    rows = [[Paragraph("<b>Question</b>", S["body"]), Paragraph("<b>Answer</b>", S["body"]), Paragraph("<b>Correct option</b>", S["body"])]]
    for i, q in enumerate(p["part_a"], 1):
        rows.append([Paragraph(f"A{i}", S["body"]), Paragraph(f"<b>{q['answer']}</b>", S["body"]),
                     Paragraph(q["options"]["ABCD".index(q["answer"])], S["body"])])
    t = Table(rows, colWidths=[25 * mm, 20 * mm, 120 * mm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6f2eb")),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9fb5a8")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s += [t, Paragraph("Part A: Worked solutions", S["h2"])]
    for i, q in enumerate(p["part_a"], 1):
        s.append(KeepTogether([Paragraph(f"A{i}. Answer {q['answer']}", S["h3"]), Paragraph(q["solution"], S["sol"])]))
    s.append(PageBreak())
    s.append(Paragraph("Part B: Worked solutions and mark scheme", S["h2"]))
    for i, q in enumerate(p["part_b"], 1):
        qm = sum(x["marks"] for x in q["parts"])
        s.append(Paragraph(f"B{i}. {q['title']}  ({qm} marks)", S["h3"]))
        for j, part in enumerate(q["parts"]):
            s.append(KeepTogether([
                Paragraph(f"<b>({'abcdefg'[j]})</b> [{part['marks']} mark{'s' if part['marks'] > 1 else ''}]  {part['solution']}", S["sol"]),
                Paragraph("Marking: " + part["scheme"], S["scheme"])]))
    return s


def build_pdf(path, story, title, subject, foot):
    doc = SimpleDocTemplate(path, pagesize=A4, title=title, author="Sustainable Olympiad", subject=subject, lang="en",
                            leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=22 * mm)
    doc.build(story, onFirstPage=foot, onLaterPages=foot)


def main():
    register_fonts()
    os.makedirs(OUT, exist_ok=True)
    S = styles()
    made = []
    for p in PAPERS:
        paper, sol = file_names(p)
        label = f"{edition_title(p)} · {p['division']} · Round 1"
        build_pdf(os.path.join(OUT, paper), question_paper(p, S), f"{label}: Question paper",
                  "Past paper", footer_fn(label + " · Question paper"))
        build_pdf(os.path.join(OUT, sol), solutions(p, S), f"{label}: Mark scheme and solutions",
                  "Mark scheme", footer_fn(label + " · Mark scheme"))
        made += [paper, sol]
    with zipfile.ZipFile(os.path.join(OUT, "sustainable-olympiad-past-papers.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in made:
            z.write(os.path.join(OUT, f), f)


if __name__ == "__main__":
    main()
