"""Estilos compartidos por los PDF del framework."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Image, Table, TableStyle, PageBreak,
                                KeepTogether, NextPageTemplate)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# --- Fuentes -----------------------------------------------------------------
F = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DJ",  f"{F}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DJB", f"{F}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DJI", f"{F}/DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DJM", f"{F}/DejaVuSansMono.ttf"))

TINTA   = colors.HexColor("#1F2933")
AZUL    = colors.HexColor("#2B6CB0")
VERDE   = colors.HexColor("#2F855A")
AMBAR   = colors.HexColor("#B7791F")
ROJO    = colors.HexColor("#C53030")
GRIS    = colors.HexColor("#718096")
GRISCL  = colors.HexColor("#E2E8F0")
FONDO   = colors.HexColor("#F7FAFC")

# --- Estilos -----------------------------------------------------------------
S = {}
S['portada_t'] = ParagraphStyle('pt', fontName="DJB", fontSize=27, leading=33,
                                textColor=TINTA, alignment=TA_CENTER)
S['portada_s'] = ParagraphStyle('ps', fontName="DJ", fontSize=13, leading=19,
                                textColor=GRIS, alignment=TA_CENTER)
S['h1'] = ParagraphStyle('h1', fontName="DJB", fontSize=17, leading=21,
                         textColor=AZUL, spaceBefore=2, spaceAfter=9)
S['h2'] = ParagraphStyle('h2', fontName="DJB", fontSize=12.5, leading=16,
                         textColor=TINTA, spaceBefore=13, spaceAfter=5)
S['h3'] = ParagraphStyle('h3', fontName="DJB", fontSize=10.5, leading=14,
                         textColor=GRIS, spaceBefore=9, spaceAfter=3)
S['p'] = ParagraphStyle('p', fontName="DJ", fontSize=9.7, leading=14.6,
                        textColor=TINTA, alignment=TA_JUSTIFY, spaceAfter=7)
S['li'] = ParagraphStyle('li', parent=S['p'], leftIndent=11, bulletIndent=2,
                         spaceAfter=3.5)
S['cap'] = ParagraphStyle('cap', fontName="DJI", fontSize=8.4, leading=11.5,
                          textColor=GRIS, alignment=TA_CENTER, spaceBefore=4,
                          spaceAfter=11)
S['code'] = ParagraphStyle('code', fontName="DJM", fontSize=8.1, leading=11.6,
                           textColor=TINTA, leftIndent=8, spaceAfter=7)
S['th'] = ParagraphStyle('th', fontName="DJB", fontSize=8.6, leading=11.6,
                         textColor=colors.white)
S['td'] = ParagraphStyle('td', fontName="DJ", fontSize=8.6, leading=11.6,
                         textColor=TINTA)
S['tdm'] = ParagraphStyle('tdm', fontName="DJM", fontSize=8.0, leading=11.6,
                          textColor=TINTA)
S['nota'] = ParagraphStyle('nota', fontName="DJ", fontSize=9.2, leading=13.6,
                           textColor=TINTA, alignment=TA_JUSTIFY,
                           leftIndent=9, rightIndent=8, spaceBefore=3, spaceAfter=3)


def P(t, st='p'):
    return Paragraph(t, S[st])


def LI(t):
    return Paragraph(f'<bullet>&bull;</bullet>{t}', S['li'])


def CODE(lineas):
    txt = "<br/>".join(l.replace(" ", "&nbsp;") for l in lineas)
    tb = Table([[Paragraph(txt, S['code'])]], colWidths=[165*mm])
    tb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), FONDO),
        ('BOX', (0,0), (-1,-1), 0.5, GRISCL),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LINEBEFORE', (0,0), (0,-1), 2.2, AZUL),
    ]))
    return tb


def CALLOUT(titulo, texto, color=AMBAR):
    inner = [Paragraph(f"<b>{titulo}</b>", ParagraphStyle(
        'ct', fontName="DJB", fontSize=9.4, leading=13, textColor=color)),
        Paragraph(texto, S['nota'])]
    tb = Table([[inner]], colWidths=[165*mm])
    tb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFDF7")),
        ('BOX', (0,0), (-1,-1), 0.5, color),
        ('LINEBEFORE', (0,0), (0,-1), 2.6, color),
        ('LEFTPADDING', (0,0), (-1,-1), 9), ('RIGHTPADDING', (0,0), (-1,-1), 9),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return tb


def TABLA(datos, anchos, mono_cols=()):
    filas = []
    for i, fila in enumerate(datos):
        f = []
        for j, c in enumerate(fila):
            if i == 0:
                f.append(Paragraph(c, S['th']))
            else:
                f.append(Paragraph(c, S['tdm'] if j in mono_cols else S['td']))
        filas.append(f)
    t = Table(filas, colWidths=anchos, repeatRows=1)
    est = [
        ('BACKGROUND', (0,0), (-1,0), AZUL),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LINEBELOW', (0,0), (-1,-1), 0.4, GRISCL),
        ('BOX', (0,0), (-1,-1), 0.5, GRISCL),
    ]
    for i in range(1, len(datos)):
        if i % 2 == 0:
            est.append(('BACKGROUND', (0,i), (-1,i), FONDO))
    t.setStyle(TableStyle(est))
    return t


def FIG(path, ancho_mm, pie):
    from PIL import Image as PILImage
    w, h = PILImage.open(path).size
    a = ancho_mm * mm
    return [Image(path, width=a, height=a * h / w), P(pie, 'cap')]


