#!/usr/bin/env python3
"""
Moon Studio – Quote PDF Generator (v10)
Uses libfribidi for proper Hebrew BiDi + ReportLab canvas for design.
Matches the original Moon Studio template with black header/footer bars,
logo, and proper RTL text rendering.
"""

import re, sys, os, ctypes, ctypes.util
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Fonts ──────────────────────────────────────────────────────────────────
F      = 'DejaVu'
FB     = 'DejaVu-Bold'
import platform
def _font_path(linux_path, mac_fallback):
    if platform.system() == 'Darwin':
        return mac_fallback
    return linux_path

pdfmetrics.registerFont(TTFont(F,  _font_path(
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf')))
pdfmetrics.registerFont(TTFont(FB, _font_path(
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/System/Library/Fonts/Supplemental/Arial Bold.ttf')))

# ── Font size hierarchy (4 fixed levels) ──────────────────────────────────
S1 = 36   # Page title:  "הצעת מחיר"
S2 = 14   # Sub-title:   client name "לכבוד: ..."
S3 = 11   # Body labels, amounts, project title, date
S4 = 9    # Small text:  description, bullets, company info, totals text

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS     = os.path.join(SCRIPT_DIR, '..', 'assets')
LOGO       = os.path.join(ASSETS, 'logo_white.png')

# ── FriBidi ────────────────────────────────────────────────────────────────
_lib = ctypes.util.find_library('fribidi')
if not _lib:
    # Homebrew on Apple Silicon
    for _candidate in ['/opt/homebrew/lib/libfribidi.dylib', '/usr/local/lib/libfribidi.dylib']:
        if os.path.exists(_candidate):
            _lib = _candidate
            break
_fribidi = ctypes.CDLL(_lib)

def visual(text):
    """Convert logical Unicode text → visual order using GNU FriBidi (RTL base)."""
    if not text:
        return text
    n = len(text)
    inp = (ctypes.c_uint32 * n)(*[ord(c) for c in text])
    out = (ctypes.c_uint32 * n)()
    d   = ctypes.c_int32(1)          # FRIBIDI_PAR_RTL
    _fribidi.fribidi_log2vis(inp, n, ctypes.byref(d), out, None, None, None)
    return ''.join(chr(out[i]) for i in range(n))


# ── Input parser ───────────────────────────────────────────────────────────
def parse(text):
    def get(pat, default=''):
        m = re.search(pat, text, re.DOTALL)
        return m.group(1).strip() if m else default
    amt_s = get(r'סכום\s*:\s*([\d,]+)').replace(',', '')
    try:    amt = float(amt_s)
    except: amt = 0.0
    return dict(
        client = get(r'שם לקוח\s*:\s*(.+?)(?:\n|$)'),
        date   = get(r'תאריך\s*:\s*(.+?)(?:\n|$)'),
        title  = get(r'כותרת הפרויקט\s*:\s*(.+?)(?:\n|$)'),
        amount = amt,
        desc   = get(r'פירוט\s*:\s*(.+?)(?:הערות|תנאי תשלום|$)'),
        notes  = get(r'הערות\s*:\s*(.+?)(?:תנאי תשלום|$)'),
        terms  = get(r'תנאי תשלום\s*:\s*(.+?)$'),
    )

def calc(a):
    v = round(a * 0.18)
    return a, v, a + v

def fmt(n):
    return f"{int(n):,}" if n == int(n) else f"{n:,.2f}"

# ── Drawing helpers ────────────────────────────────────────────────────────
def rtxt(c, x, y, txt, font=F, sz=S3, clr=colors.black):
    """Draw right-aligned RTL text (visual order)."""
    c.setFont(font, sz); c.setFillColor(clr)
    c.drawRightString(x, y, visual(txt))

def ltxt(c, x, y, txt, font=F, sz=S3, clr=colors.black):
    """Draw left-aligned LTR text."""
    c.setFont(font, sz); c.setFillColor(clr)
    c.drawString(x, y, txt)

def hline(c, x1, x2, y, w=0.5, clr=colors.HexColor('#cccccc')):
    c.setStrokeColor(clr); c.setLineWidth(w); c.line(x1, y, x2, y)

def wrap_rtl(c, rx, y, text, font=F, sz=S4, maxw=430, lh=14):
    """Word-wrap RTL paragraph; returns new y."""
    c.setFont(font, sz)
    words = text.split()
    lines, cur = [], []
    for w in words:
        test = ' '.join(cur + [w])
        if pdfmetrics.stringWidth(visual(test), font, sz) > maxw and cur:
            lines.append(' '.join(cur)); cur = [w]
        else:
            cur.append(w)
    if cur: lines.append(' '.join(cur))
    for line in lines:
        c.setFillColor(colors.black)
        c.drawRightString(rx, y, visual(line))
        y -= lh
    return y

# ── PDF generator ──────────────────────────────────────────────────────────
def generate(info, output):
    W, H = A4                      # 595 × 842
    ML, MR = 45, W - 45            # margins
    BW = MR - ML
    CREAM  = colors.HexColor('#F8F4EE')
    BLACK  = colors.HexColor('#111111')
    R      = 18                    # corner radius

    # Logo x — pushed close to page edge; info text slightly indented
    LOGO_X   = 4
    INFO_X   = 30

    c = rl_canvas.Canvas(output, pagesize=A4)

    # ── Cream page background ─────────────────────────────────────────────
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=True, stroke=False)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # BLACK HEADER BAR – rounded bottom corners
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    BAR_H = 178
    c.setFillColor(BLACK)
    c.rect(0, H - BAR_H + R, W, BAR_H - R, fill=True, stroke=False)
    c.roundRect(0, H - BAR_H, W, BAR_H, R, fill=True, stroke=False)

    # ── Logo ──────────────────────────────────────────────────────────────
    LOGO_W, LOGO_H = 180, 90
    logo_y = H - LOGO_H - 14          # 14pt top padding inside bar
    if os.path.exists(LOGO):
        c.drawImage(LOGO, LOGO_X, logo_y, width=LOGO_W, height=LOGO_H,
                    mask='auto', preserveAspectRatio=True)

    # ── Company info (left, white) – y aligned with client name on right ──
    ix, iy = INFO_X, H - 96
    c.setFillColor(colors.white)
    c.setFont(FB, S4 + 1); c.drawString(ix, iy, 'MoonStudio'); iy -= 13
    c.setFont(F, S4 - 1); c.setFillColor(colors.HexColor('#cccccc'))
    for line in [
        visual('עוסק מורשה') + ': 301448288',
        visual('נייד') + ': 0504533388',
        'dvirgolanmusic@gmail.com',
        'www.moonstudio.com',
    ]:
        c.drawString(ix, iy, line); iy -= 11

    # ── Title + Client + Date (right, white) ──────────────────────────────
    c.setFillColor(colors.white)

    # S1 / bold — "הצעת מחיר"
    c.setFont(FB, S1)
    c.drawRightString(MR, H - 56, visual('הצעת מחיר'))

    # S2 / regular — client name
    c.setFont(F, S2)
    c.drawRightString(MR, H - 96, visual('לכבוד: ' + info['client']))

    # S3 / regular — date
    c.setFont(F, S3)
    c.drawRightString(MR, H - 116, visual('תאריך: ' + info['date']))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TABLE HEADER
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    y = H - BAR_H - 25
    hline(c, ML, MR, y + 14, w=0.8, clr=colors.black)

    rtxt(c, MR - 10, y, 'תיאור הפריט', font=FB, sz=S3)
    ltxt(c, ML + 10, y, visual('עלות'), font=FB, sz=S3)

    hline(c, ML, MR, y - 8, w=0.8, clr=colors.black)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PROJECT TITLE + AMOUNT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    y -= 25
    rtxt(c, MR - 10, y, info['title'], font=FB, sz=S3)
    ltxt(c, ML + 10, y, fmt(info['amount']), font=F, sz=S3)   # regular weight

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # DESCRIPTION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if info['desc']:
        y -= 18
        rtxt(c, MR - 10, y, 'פירוט:', font=FB, sz=S3)
        y -= 14
        y = wrap_rtl(c, MR - 10, y, info['desc'], font=F, sz=S4, maxw=BW - 30, lh=13)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TOTALS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    sub, vat, total = calc(info['amount'])
    y -= 14
    hline(c, ML, MR, y + 8, w=0.8, clr=colors.black)

    # Subtotal (excl. VAT) — regular weight
    y -= 10
    rtxt(c, MR - 10, y, 'סה"כ ללא מע"מ:', font=F, sz=S3)
    ltxt(c, ML + 10, y, f'₪{fmt(sub)}', font=F, sz=S3)

    hline(c, ML, MR, y - 10)

    # VAT — regular weight
    y -= 26
    rtxt(c, MR - 10, y, 'מע"מ (18%):', font=F, sz=S3)
    ltxt(c, ML + 10, y, f'₪{fmt(vat)}', font=F, sz=S3)

    hline(c, ML, MR, y - 10)

    # Final total — BOLD (only this number is bold)
    y -= 26
    rtxt(c, MR - 10, y, 'סה"כ כולל מע"מ:', font=FB, sz=S3)
    ltxt(c, ML + 10, y, f'₪{fmt(total)}', font=FB, sz=S3)

    hline(c, ML, MR, y - 12, w=0.8, clr=colors.black)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # NOTES  (user input + always-on default notes from template)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    DEFAULT_NOTES = [
        'כולל שני סבבי תיקונים לבקשת הלקוח',
        'הצעת המחיר תקפה ל-14 יום',
    ]
    # Collect user notes lines + default notes
    all_notes = []
    if info['notes']:
        for line in info['notes'].split('\n'):
            line = line.strip(' -•\t')
            if line:
                all_notes.append(line)
    all_notes.extend(DEFAULT_NOTES)

    y -= 26
    rtxt(c, MR - 10, y, 'הערות:', font=FB, sz=S3)
    y -= 16
    for line in all_notes:
        rtxt(c, MR - 10, y, '\u2022 ' + line, font=F, sz=S4)
        y -= 13

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PAYMENT TERMS  (user input, falls back to default from template)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    DEFAULT_TERMS = [
        '50% מקדמה להתנעת עבודה',
        '50% בסיום הפרויקט',
    ]
    all_terms = []
    if info['terms']:
        for line in info['terms'].split('\n'):
            line = line.strip(' -•\t')
            if line:
                all_terms.append(line)
    if not all_terms:
        all_terms = DEFAULT_TERMS

    y -= 20
    rtxt(c, MR - 10, y, 'תנאי תשלום:', font=FB, sz=S3)
    y -= 16
    for line in all_terms:
        rtxt(c, MR - 10, y, '\u2022 ' + line, font=F, sz=S4)
        y -= 13

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # FOOTER SIGNATURE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    y -= 26
    c.setFillColor(colors.black)
    c.setFont(F, S4);  c.drawString(ML, y, visual('מצפה לעבוד יחד')); y -= 13
    c.setFont(F, S4);  c.drawString(ML, y, visual('תודה מראש'));       y -= 15
    c.setFont(FB, S3); c.drawString(ML, y, visual('דביר גולן'))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # BLACK FOOTER BAR – rounded top corners
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    FOOTER_H = 35
    c.setFillColor(BLACK)
    c.rect(0, 0, W, FOOTER_H - R, fill=True, stroke=False)
    c.roundRect(0, 0, W, FOOTER_H, R, fill=True, stroke=False)

    c.save()


# ── CLI ────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: generate_quote.py '<text>' [output.pdf]"); sys.exit(1)
    text   = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else 'quote.pdf'
    info   = parse(text)
    missing = [f for f, v in [('שם לקוח', info['client']), ('תאריך', info['date']),
               ('כותרת', info['title']), ('סכום', info['amount'])] if not v]
    if missing:
        print(f"❌ חסרים: {', '.join(missing)}"); sys.exit(1)
    generate(info, output)
    s, v, t = calc(info['amount'])
    print(f"✅ הצעת מחיר נוצרה: {output}")
    print(f"   לקוח: {info['client']}  |  {info['date']}")
    print(f"   סכום: ₪{fmt(s)}  מעמ: ₪{fmt(v)}  סה\"כ: ₪{fmt(t)}")

if __name__ == '__main__':
    main()
