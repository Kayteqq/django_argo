from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, TableStyle, Table, HRFlowable, Image
from reportlab.lib.pagesizes import A4
from django.contrib.staticfiles import finders
from reportlab.lib import colors

from datetime import datetime
import time
import os
from django.conf import settings


def get_static_file_path(relative_path):
    """
    Tylko zabezpieczenie: Szuka pliku przez finders, a w razie niepowodzenia
    buduje ścieżkę absolutną na podstawie BASE_DIR. Zwraca None, jeśli plik nie istnieje.
    """
    path = finders.find(relative_path)
    if not path:
        path = os.path.join(settings.BASE_DIR, 'home', 'static', relative_path)
    return path if os.path.exists(path) else None


def generate_pdf(data, mail, lang):
    # ZABEZPIECZENIE CZCIONEK
    font_reg = get_static_file_path("fonts/Archivo-Regular.ttf")
    font_bold = get_static_file_path("fonts/Archivo-SemiBold.ttf")
    font_semi = get_static_file_path("fonts/Archivo_SemiExpanded-SemiBold.ttf")

    if font_reg: pdfmetrics.registerFont(TTFont('Archivo-Regular', font_reg))
    if font_bold: pdfmetrics.registerFont(TTFont('Archivo-SemiBold', font_bold))
    if font_semi: pdfmetrics.registerFont(TTFont('Archivo-SemiExpanded-SemiBold', font_semi))

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=40,
        leftMargin=40,
        rightMargin=40,
        bottomMargin=40
    )
    elements = []

    width, height = A4
    usable_width = width - 80
    usable_height = height - 80

    # SYLE

    normal = ParagraphStyle(
        name='Normal',
        fontName='Archivo-Regular' if font_reg else 'Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#231f20')
    )
    normal_right = ParagraphStyle(
        name='Normal',
        fontName='Archivo-Regular' if font_reg else 'Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#231f20'),
        alignment=TA_RIGHT,
    )
    bold = ParagraphStyle(
        name='Normal',
        fontName='Archivo-SemiBold' if font_bold else 'Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#231f20')
    )
    uppercase = ParagraphStyle(
        name='Bold',
        fontName='Archivo-SemiBold' if font_bold else 'Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#231f20')
    )
    title = ParagraphStyle(
        name='Title',
        fontName='Archivo-SemiExpanded-SemiBold' if font_semi else 'Helvetica-Bold',
        fontSize=12,
        leading=14,
        textColor=colors.HexColor('#231f20')
    )
    subtitle = ParagraphStyle(
        name='Title',
        fontName='Archivo-SemiExpanded-SemiBold' if font_semi else 'Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#231f20')
    )
    keyword = ParagraphStyle(
        name='Keyword',
        fontName='Archivo-SemiExpanded-SemiBold' if font_semi else 'Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#231f20')
    )

    # PRODUKT
    unix_time = int(time.time())
    elements.append(Paragraph("Produkt", title))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f'nr {unix_time}', subtitle))

    half_line = HRFlowable(
        width=usable_width,  # połowa szerokości
        thickness=1,  # grubość linii
        lineCap='round',  # styl zakończeń linii
        color=colors.HexColor('#231f20'),
        spaceBefore=10,  # odstęp przed linią
        spaceAfter=10,  # odstęp po linii
        hAlign='CENTER'  # wyrównanie: 'LEFT', 'CENTER', 'RIGHT'
    )

    elements.append(half_line)

    # Szczegóły

    tab = [line.strip() for line in data['smart'].splitlines() if line.strip()]
    details_data = []

    if lang == 'pl':
        details_data = [
            ["Wybrana linia stylu:", f'{data["styleLine"]}'],
            ["Wybrany kolor ram:", f'{data["color1"]}'],
            ["Wybrane użycie produktu:", f'{data["usecase"]}'],
            ["Wybrany rodzaj produktu:", f'{data["type"]}'],
            ["Wybrane dodatki:", f'{data["additivies"]}'],
            ["Wybrany kolor klamek:", f'{data["color2"]}'],
            ["Naświetla:", f"{'Lewe, ' if data.get('leftWindowEnabled') else ''} "
                           f"{'Prawe, ' if data.get('rightWindowEnabled') else ''} "
                           f"{'Górne' if data.get('topWindowEnabled') else ''} "
                           f"{'Brak' if not data.get('leftWindowEnabled') and not data.get('rightWindowEnabled') and not data.get('topWindowEnabled') else ''} "],
            ["Wysokość:", f'{data["productHeight"] * 45}cm'],
            ['Szerokość:', f'{data["productWidth"] * 45}cm'],
            ["Szerokość Drzwi:", f'{data["doorWidth"] * 45}cm'],
            ["Szerokość Prawego Naświetla:", f'{data["rightWidth"] * 45}cm'],
            ["Szerokość Lewego Naświetla:", f'{data["leftWidth"] * 45}cm'],
            ["Wysokość Górnego Naświetla:", f'{"45" if data.get("topWindowEnabled") else "0"}cm'],
        ]

    if lang == 'en':
        details_data = [
            ["Chosen style line:", f'{data["styleLine"]}'],
            ["Chosen frame color:", f'{data["color1"]}'],
            ["Chosen usecase:", f'{data["usecase"]}'],
            ["Chosen product type:", f'{data["type"]}'],
            ["Chosen additions:", f'{data["additivies"]}'],
            ["Chosen handles color:", f'{data["color2"]}'],
            ["Transoms:", f"{'Left, ' if data.get('leftWindowEnabled') else ''} "
                          f"{'Right, ' if data.get('rightWindowEnabled') else ''} "
                          f"{'Top' if data.get('topWindowEnabled') else ''} "
                          f"{'None' if not data.get('leftWindowEnabled') and not data.get('rightWindowEnabled') and not data.get('topWindowEnabled') else ''} "],
            ["Height:", f'{data["productHeight"] * 45}cm'],
            ['Width:', f'{data["productWidth"] * 45}cm'],
            ["Door Width:", f'{data["doorWidth"] * 45}cm'],
            ["Right Transom Width:", f'{data["rightWidth"] * 45}cm'],
            ["Left Transom Width:", f'{data["leftWidth"] * 45}cm'],
            ["Top Transom Height:", f'{"45" if data.get("topWindowEnabled") else "0"}cm'],
        ]

    for i in range(3):
        if i < len(tab):
            if i == 0 and lang == 'pl':
                details_data.append(["Wybrane elementy smart home:", tab[i]])
            elif i == 0 and lang == 'en':
                details_data.append(["Chosen smart home elements:", tab[i]])
            else:
                details_data.append(["", tab[i]])
        else:
            details_data.append(["", ""])

    formatted_details = []
    for label, value in details_data:
        formatted_details.append([
            Paragraph(label, bold),
            Paragraph(value, normal_right),
        ])

    details_table = Table(
        formatted_details,
        colWidths=[usable_width * 0.55, usable_width * 0.45],
    )

    details_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), -2),
    ]))

    spacer = 240 - 11 * len(tab)
    elements.append(details_table),
    elements.append(Spacer(1, spacer))

    keyword = Paragraph('Comments', keyword)
    elements.append(keyword)
    elements.append(Spacer(1, 10))

    left_temp = ""
    if lang == 'pl':
        left_temp = """Czas wygaśnięcia zgłoszenia: 30 dni
            Cena: do ustalenia
            Sposób płatności: do ustalenia
            Data skompletowania: do ustalenia
            Transport: do ustalenia






            """
    if lang == 'en':
        left_temp = """Order expiration time: 30 days
            Price: to be agreed
            Payment details: to be agreed
            Date of completion: to be agreed
            Transportation: to be agreed






            """
    left_comment = "<br/>".join(left_temp.splitlines())

    if mail == '' and lang == 'pl':
        right_comment = f"""
            Data zgłoszenia: {datetime.now().strftime("%d.%m.%Y. %H:%M:%S")}
        """
    elif mail == '' and lang == 'en':
        right_comment = f"""
            Date of submission: {datetime.now().strftime("%d.%m.%Y. %H:%M:%S")}
        """
    elif lang == 'pl':
        right_comment = f"""
            Zapytanie przygotowne przez: {mail}<br/>
            Data zgłoszenia: {datetime.now().strftime("%d.%m.%Y. %H:%M:%S")}
        """
    elif lang == 'en':
        right_comment = f"""
            Prepared by: {mail}<br/>
            Date of submission: {datetime.now().strftime("%d.%m.%Y. %H:%M:%S")}
        """

    comment_table = Table(
        [[Paragraph(left_comment, normal),
          Paragraph(right_comment, normal_right)]],
        colWidths=[usable_width * 0.50, usable_width * 0.50],
    )
    comment_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), -2),
    ]))

    elements.append(comment_table)
    elements.append(Spacer(1, 100))

    left_footer = """
        <font backColor="#ACCFE1"></font><br/>
        <br/>
        <br/>
    """
    right_footer = """
        <br/>
        <br/>
        PHONE.....................<br/>
    """

    # ZABEZPIECZENIE LOGO
    logo_path = get_static_file_path('logo/Argo-Logo.png')
    if logo_path:
        logo = Image(logo_path, width=38, height=32)
    else:
        logo = Spacer(38, 32)  # Element awaryjny o identycznej wielkości, by nie zmieniać układu tabeli

    footer_data = [
        ["ARGO SP. Z O.O.", "NIP..........................7122293543"],
        ["UL. TOKARSKA 21", "REGON.....................060108877"],
        ["20-210 LUBLIN", "PHONE......................................"],
    ]

    formatted_footer_left = []
    formatted_footer_right = []
    for left, right in footer_data:
        formatted_footer_left.append([
            Paragraph(left, uppercase),
        ])
        formatted_footer_right.append([
            Paragraph(right, uppercase),
        ])

    footer_table = Table(
        [[formatted_footer_left, formatted_footer_right, logo]],
        colWidths=[usable_width * 0.7 - 23, usable_width * 0.3 - 25, 32],
    )

    # footer_table = Table(
    #     [
    #         [
    #             Paragraph(left_footer, uppercase),
    #             Paragraph(right_footer, uppercase),
    #             logo
    #         ]
    #     ],
    #
    #     colWidths=[usable_width*0.7-30, usable_width*0.3-25, 40],
    # )

    footer_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), -2),
        ('RIGHTPADDING', (0, 0), (-1, -1), -2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), -2),
    ]))
    elements.append(footer_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer