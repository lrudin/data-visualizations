"""
Build the static-project report as a PDF, with every chart embedded as vector SVG.
 
Setup (once):   uv add reportlab svglib
Run (from static-project/, after the notebook has saved the SVGs to figures/):
                uv run python make_report.py
Output:         report.pdf
 
How it works:
  1. TEXT (below) lists the report's content in order: headings, paragraphs and figures.
  2. build() turns each item into a PDF element ("flowable") and lays them out page by page.
  3. Each figure is read from figures/<name>.svg, scaled to fit the page, and kept
     together with its caption so a chart is never split from its caption across pages.
 
Edit the TEXT below freely. Lines marked "# CHECK" quote figures read off earlier
versions of the charts: confirm them against the current charts before submitting.
"""
from datetime import date
from pathlib import Path
 
# reportlab builds the PDF; svglib converts each SVG into a reportlab drawing (kept as vectors)
 
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (KeepTogether, Paragraph, SimpleDocTemplate, Spacer)
from svglib.svglib import svg2rlg
 
# Paths are relative to the folder you run the script from (static-project/)
FIG_DIR = Path("figures")    # where the notebook saved the SVGs
OUT = Path("report.pdf")     # the PDF this script writes (overwritten on each run)
 
# Title block
AUTHOR = "Lily Rudin"
TITLE = "Exposed, but adopting? Generative AI across economic divides"
R_VALUE = "0.45"   # CHECK: replace with the r value the scatter cell prints
 
# ---------------------------------------------------------------------------
# Content, in the order it appears in the PDF. Each item is one of:
#   ("h", "Heading text")
#   ("p", "Paragraph text")
#   ("fig", "svg_name", "Caption", "Source")   -> figures/svg_name.svg, numbered automatically
# Paragraph text accepts simple tags: <b>bold</b>, <i>italic</i>, <br/> for a line break.
# To reorder the report, move items around; figure numbers update by themselves.
# Note: "&" must be written as "&amp;" inside text, because reportlab reads it as markup.
# ---------------------------------------------------------------------------
TEXT = [
    # --- Introduction: the research question and the data ---
    ("p", "Generative AI has spread faster than almost any previous technology, but adoption is uneven "
          "across countries. This report asks two questions: does AI adoption follow existing economic "
          "divides, and are the countries whose workforces are most exposed to generative AI the ones "
          "adopting it least? It combines occupational employment data from the International Labour "
          "Organization (ILO), the OECD's survey of AI use by businesses, and World Bank income data."),
 
    # --- Part 1: exposure (ILOSTAT charts 1-4) ---
    ("h", "1. Where is the workforce exposed?"),
    ("p", "The ILO's 2025 index scores each occupation by how many of its tasks generative AI could "
          "potentially perform. Clerical support work, such as data entry, bookkeeping and general office "
          "work, scores highest. <i>Exposure</i> measures that potential; it does not predict job loss, "
          "and the ILO expects most exposed jobs to be transformed rather than eliminated. Because clerical "
          "work is the clearest case, the first charts use its share of employment as a proxy for exposure."),
    ("fig", "clerical_map",
     "Clerical jobs make up a much larger share of employment in high-income countries in Europe, North "
     "America, East Asia and Oceania than in most of Africa and South Asia.",
     "ILOSTAT, employment by occupation (ISCO-08); ILO Working Paper 140 (2025)."),
    ("p", "The pattern follows a broader shift in what work looks like as countries get richer. In low-income "
          "countries, most people work in agriculture; in high-income countries, employment is concentrated "
          "in professional, technical and clerical occupations, which are exactly the jobs generative AI can "
          "reach. Clerical work alone rises from about 1% of employment in low-income countries to about 10% "
          "in high-income ones."),   # CHECK
    ("fig", "occupation_heatmap",
     "Agriculture falls from 57% of employment in low-income countries to 2% in high-income countries, "   # CHECK
     "while professional, technical and clerical work grows.",
     "ILOSTAT; World Bank income classifications."),
    ("p", "Exposure is also unevenly distributed between women and men. In every economy shown, women are "
          "far more likely than men to work in clerical jobs. In the most extreme cases, around a quarter of "
          "employed women work in clerical roles, against well under a tenth of men."),   # CHECK
    ("fig", "sex_clerical_jobs",
     "Women's share of employment in clerical jobs is several times men's in the economies with the "
     "largest gaps.",
     "ILOSTAT, employment by sex and occupation."),
    ("p", "The difference between income groups is not a snapshot. Averaged across countries in each "
          "World Bank income group, the clerical share has stayed well apart between high- and low-income "
          "countries throughout 2012–2024."),   # CHECK: describe any trend you see in the chart
    ("fig", "clerical_lines",
     "Average share of employment in clerical jobs by income group, 2012–2024.",
     "ILOSTAT; World Bank income classifications."),
 
    # --- Part 2: adoption (OECD charts 5-8) ---
    ("h", "2. Who is adopting AI?"),
    ("p", "Business adoption varies enormously, even among wealthy countries. In Denmark, about 42% of firms "
          "with ten or more employees use AI, roughly double the EU-27 average of about 20%. At the other "
          "end, adoption is in the single digits in countries such as Romania, Türkiye and Canada."),   # CHECK
    ("fig", "business_ai",
     "Share of businesses using AI, the 10 highest and 10 lowest countries in the OECD survey.",
     "OECD, ICT Access and Usage by Businesses."),
    # f-string, so R_VALUE (set at the top) is inserted into the text
    (
        "p", f"Countries with higher GDP per capita tend to adopt more, but the relationship is only "
             f"moderate (r = {R_VALUE}). Countries with similar output per person differ widely: Denmark "
             f"and Finland adopt far more than Switzerland or Ireland. Income sets the stage, but it does not "
             f"determine adoption."),
    ("fig", "gdp_ai_scatter",
     "AI adoption against GDP per capita (adjusted for purchasing power parity).",
     "OECD, ICT Access and Usage by Businesses; World Bank, World Development Indicators."),
    ("p", "Within countries, the divide runs along firm size. Large firms are far more likely to use AI than "
          "small ones in every country, and the gap is widest among the leading adopters."),
    ("fig", "ai_firm_size",
     "AI use in small (10–49 employees) and large (250+) firms.",
     "OECD, ICT Access and Usage by Businesses."),
    ("p", "Adoption also depends heavily on the industry. Information and communication firms are by far the "
          "heaviest users, followed by professional and scientific services, while construction, transport, "
          "and hotels and food service lag well behind."),
    ("fig", "ai_by_industry",
     "Average share of businesses using AI by industry, across countries in the OECD survey.",
     "OECD, ICT Access and Usage by Businesses."),
 
    # --- Conclusion and limitations ---
    # CHECK: make sure this reading matches your final charts
    ("h", "3. What this means"),
    ("p", "The data point to a layered divide rather than a simple one. Exposure is concentrated in "
          "high-income countries, in office work, and among women. Adoption, where it can be measured, also "
          "rises with income, but varies widely among countries at similar income levels, between large and "
          "small firms, and between industries. Among the countries where both can be observed, the most "
          "exposed workforces are not systematically the slowest adopters; the larger gap may be between "
          "large digital-sector firms and everyone else."),
    ("p", "<b>Limitations.</b> The OECD adoption survey covers about 30 countries, mostly in Europe, while "
          "the occupation data cover much of the world, so the two can only be compared for a small, "
          "high-income set of countries. Adoption in low- and middle-income countries remains largely "
          "unmeasured. Clerical share is a proxy for exposure, and exposure is not impact. Adoption figures "
          "from before 2023 are excluded because generative AI spread after late 2022, and each country's "
          "latest year differs."),
 
    # --- Sources ---
    ("h", "Data and sources"),
    ("p", "ILO, ILOSTAT: employment by sex and occupation (ISCO-08 major groups).<br/>"
          "Gmyrek, P., Berg, J., et al. (2025). <i>Generative AI and Jobs: A Refined Global Index of "
          "Occupational Exposure</i>. ILO Working Paper 140.<br/>"
          "OECD, ICT Access and Usage by Businesses database: share of enterprises using AI.<br/>"
          "World Bank, World Development Indicators: GDP per capita, PPP (current international $); "
          "country income classifications.<br/>"
          "Map boundaries: Natural Earth, via vega-datasets."),
]
 
# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
# Text colors: near-black for body text, gray for secondary text (same grays as the charts)
INK, INK_2 = colors.HexColor("#0b0b0b"), colors.HexColor("#52514e")
 
# Text styles. fontSize = letter size in points; leading = line height; spaceBefore/After = gaps
# around the block. Helvetica is built into every PDF reader, so no font files are needed.
styles = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=INK,
                            spaceAfter=6),
    "byline": ParagraphStyle("byline", fontName="Helvetica", fontSize=10, textColor=INK_2, spaceAfter=18),
    "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=13.5, leading=17, textColor=INK,
                        spaceBefore=14, spaceAfter=6),
    "p": ParagraphStyle("p", fontName="Helvetica", fontSize=10.5, leading=15, textColor=INK,
                        alignment=TA_LEFT, spaceAfter=8),
    # Figure caption ("Figure 1. ...") and the smaller italic source line under it
    "cap": ParagraphStyle("cap", fontName="Helvetica", fontSize=9, leading=12, textColor=INK, spaceBefore=4),
    "src": ParagraphStyle("src", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=INK_2,
                          spaceAfter=14),
}
 
# Page geometry (US Letter, 8.5 x 11 in). Use reportlab.lib.pagesizes.A4 instead for A4 paper.
PAGE_W, PAGE_H = letter
MARGIN = 0.85 * inch
FRAME_W = PAGE_W - 2 * MARGIN   # usable width between the margins: charts are scaled to fit this
# Maximum chart size. Smaller values = smaller charts and fewer page breaks, but smaller chart text.
MAX_FIG_W = 0.88 * FRAME_W   # widest a chart may be (fraction of the text width)
MAX_FIG_H = 3.6 * inch       # tallest a chart may be
 
 
def svg_flowable(name):
    """Load figures/<name>.svg and scale it to fit the page, keeping its proportions."""
    path = FIG_DIR / f"{name}.svg"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found - run the notebook's SVG export cell first")
    drawing = svg2rlg(str(path))   # SVG -> reportlab vector drawing
 
    # Scale factor: as large as possible without exceeding MAX_FIG_W or MAX_FIG_H
    s = min(MAX_FIG_W / drawing.width, MAX_FIG_H / drawing.height)
    drawing.width, drawing.height = drawing.width * s, drawing.height * s
    drawing.scale(s, s)            # scale the contents, not just the bounding box
    drawing.hAlign = "CENTER"      # center charts narrower than the page
    return drawing
 
 
def footer(canvas, doc):
    """Draw the page number at the bottom right of every page."""
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(INK_2)
    canvas.drawRightString(PAGE_W - MARGIN, 0.5 * inch, str(doc.page))
    canvas.restoreState()
 
 
def build():
    """Turn TEXT into PDF elements and write report.pdf."""
    # The "story" is reportlab's list of elements, laid out top to bottom across pages.
    # %-d prints the day without a leading zero (macOS/Linux; use %d on Windows).
    story = [Paragraph(TITLE, styles["title"]),
             Paragraph(f"{AUTHOR} · {date.today():%B %-d, %Y}", styles["byline"])]
    fig_n = 0   # running figure number
    for item in TEXT:
        kind = item[0]
        if kind == "h":
            story.append(Paragraph(item[1], styles["h"]))
        elif kind == "p":
            story.append(Paragraph(item[1], styles["p"]))
        elif kind == "fig":
            fig_n += 1
            _, name, caption, source = item
            # KeepTogether moves the chart, caption and source to the next page together
            # if they don't all fit in the space left on the current page
            story.append(KeepTogether([
                Spacer(1, 4), svg_flowable(name),
                Paragraph(f"<b>Figure {fig_n}.</b> {caption}", styles["cap"]),
                Paragraph(f"Source: {source}", styles["src"]),
            ]))
    # Page setup; title and author are also stored in the PDF's document properties
    doc = SimpleDocTemplate(str(OUT), pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=MARGIN, title=TITLE, author=AUTHOR)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUT.resolve()}")
 
 
if __name__ == "__main__":
    build()
 