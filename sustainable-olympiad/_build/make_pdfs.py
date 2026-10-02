"""Generate the downloadable PDFs and the .ics calendar from content.py.
Output: ../assets/docs/   Requires: pip install reportlab"""
import os
from datetime import date, timedelta

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (ListFlowable, ListItem, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

from content import (CATEGORIES, DIVISIONS, DOWNLOADS, EVENT, GUIDELINES, JUDGING,
                     RULES, TIMELINE, TIPS)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "assets", "docs")

GREEN = colors.HexColor("#0a6b3d")
BLUE = colors.HexColor("#0b5394")
INK = colors.HexColor("#10231a")

base = getSampleStyleSheet()
STY = {
    "title": ParagraphStyle("t", parent=base["Title"], textColor=GREEN, fontSize=26, leading=32, alignment=TA_LEFT),
    "sub": ParagraphStyle("s", parent=base["Normal"], textColor=BLUE, fontSize=13, leading=18, spaceAfter=10),
    "h2": ParagraphStyle("h2", parent=base["Heading2"], textColor=GREEN, fontSize=15, leading=20, spaceBefore=12),
    "h3": ParagraphStyle("h3", parent=base["Heading3"], textColor=BLUE, fontSize=12, leading=16),
    "body": ParagraphStyle("b", parent=base["BodyText"], textColor=INK, fontSize=11, leading=16, spaceAfter=6),
}


def bullets(items):
    return ListFlowable([ListItem(Paragraph(t, STY["body"]), leftIndent=12) for t in items],
                        bulletType="bullet", start="•", leftIndent=14)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#3d5247"))
    canvas.drawString(20 * mm, 12 * mm, f"{EVENT['name']} {EVENT['edition']}")
    canvas.drawRightString(190 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build(filename, title, subject, story):
    path = os.path.join(DOCS, filename)
    doc = SimpleDocTemplate(path, pagesize=A4, title=title, author=EVENT["name"], subject=subject,
                            leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=20 * mm,
                            lang="en")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def table(rows, widths):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("GRID", (0, 0), (-1, -1), .5, colors.HexColor("#6b8577")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef7f1")]),
    ]))
    return t


def cell(text):
    return Paragraph(text, STY["body"])


def rulebook():
    s = [Paragraph(f"{EVENT['name']} {EVENT['edition']}: Official Rulebook", STY["title"]),
         Paragraph(f"{EVENT['tagline']} Global Finals: {EVENT['finals_dates']}, {EVENT['venue']}.", STY["sub"])]
    for _id, heading, paras, items in RULES:
        s.append(Paragraph(heading, STY["h2"]))
        s += [Paragraph(p, STY["body"]) for p in paras]
        if items:
            s.append(bullets(items))
    s.append(Paragraph("Divisions", STY["h2"]))
    s.append(table([["Division", "Who can enter"]] + [list(d) for d in DIVISIONS], [45 * mm, 125 * mm]))
    s.append(Paragraph("Judging criteria", STY["h2"]))
    s.append(table([["Criterion", "Weight", "What judges look for"]] +
                   [[cell(a), b, cell(c)] for a, b, c in JUDGING], [45 * mm, 20 * mm, 105 * mm]))
    s.append(Paragraph("Competition categories", STY["h2"]))
    for c in CATEGORIES:
        s.append(Paragraph(c["name"], STY["h3"]))
        s.append(Paragraph(c["description"], STY["body"]))
        s.append(Paragraph(f"<b>2027 challenge brief:</b> {c['brief']}", STY["body"]))
    s.append(Paragraph("Key dates", STY["h2"]))
    s.append(table([["Date", "Milestone"]] + [[fmt_range(t), cell(t["title"])] for t in TIMELINE],
                   [55 * mm, 115 * mm]))
    build(DOWNLOADS[0][2], f"{EVENT['name']} {EVENT['edition']} Rulebook", "Official competition rules", s)


def guidelines():
    s = [Paragraph("Participant Guidelines", STY["title"]),
         Paragraph(f"Practical advice for teams and mentors taking part in the {EVENT['name']} {EVENT['edition']}.",
                   STY["sub"])]
    for heading, items in GUIDELINES:
        s.append(Paragraph(heading, STY["h2"]))
        s.append(bullets(items))
    s.append(Paragraph("Need help?", STY["h2"]))
    s.append(Paragraph("Contact the organising team through the Contact page on our website. "
                       "We are happy to answer questions from students, mentors and parents.", STY["body"]))
    build(DOWNLOADS[1][2], "Participant Guidelines", "Guidance for teams and mentors", s)


def tips():
    s = [Paragraph("Sustainability Tips", STY["title"]),
         Paragraph("Small everyday actions that add up, for students, schools and families.", STY["sub"])]
    for heading, items in TIPS:
        s.append(Paragraph(heading, STY["h2"]))
        s.append(bullets(items))
    build(DOWNLOADS[2][2], "Sustainability Tips", "Everyday sustainability actions", s)


def fmt(d):
    return date.fromisoformat(d).strftime("%-d %B %Y")


def fmt_range(t):
    if not t.get("end"):
        return fmt(t["start"])
    a, b = date.fromisoformat(t["start"]), date.fromisoformat(t["end"])
    if a.month == b.month:
        return f"{a.day}–{b.strftime('%-d %B %Y')}"
    return f"{a.strftime('%-d %B')} – {b.strftime('%-d %B %Y')}"


def ics():
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Sustainable Olympiad//Schedule 2027//EN",
             "CALSCALE:GREGORIAN", "X-WR-CALNAME:Sustainable Olympiad 2027"]
    for t in TIMELINE:
        start = date.fromisoformat(t["start"])
        end = date.fromisoformat(t.get("end", t["start"])) + timedelta(days=1)
        lines += ["BEGIN:VEVENT", f"UID:{t['id']}-2027@sustainable-olympiad",
                  "DTSTAMP:20260901T000000Z",
                  f"DTSTART;VALUE=DATE:{start:%Y%m%d}", f"DTEND;VALUE=DATE:{end:%Y%m%d}",
                  f"SUMMARY:Sustainable Olympiad: {t['title']}",
                  "DESCRIPTION:" + t["desc"].replace(",", "\\,").replace(";", "\\;"), "END:VEVENT"]
    lines.append("END:VCALENDAR")
    with open(os.path.join(DOCS, "sustainable-olympiad-2027.ics"), "w", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")


def main():
    os.makedirs(DOCS, exist_ok=True)
    rulebook()
    guidelines()
    tips()
    ics()


if __name__ == "__main__":
    main()
