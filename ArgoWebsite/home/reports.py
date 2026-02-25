from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, TableStyle, Table, HRFlowable, Image
from reportlab.lib.pagesizes import A4
from django.contrib.staticfiles import finders
from reportlab.lib import colors

import time



def generate_pdf(data, mail):
    pdfmetrics.registerFont(TTFont('Archivo-Regular', finders.find("fonts/Archivo-Regular.ttf")))
    pdfmetrics.registerFont(TTFont('Archivo-SemiBold', finders.find("fonts/Archivo-SemiBold.ttf")))
    pdfmetrics.registerFont(TTFont('Archivo-SemiExpanded-SemiBold', finders.find("fonts/Archivo_SemiExpanded-SemiBold.ttf")))
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
        fontName='Archivo-Regular',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#231f20')
    )
    normal_right = ParagraphStyle(
        name='Normal',
        fontName='Archivo-Regular',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#231f20'),
        alignment=TA_RIGHT,
    )
    bold = ParagraphStyle(
        name='Normal',
        fontName='Archivo-SemiBold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#231f20')
    )
    uppercase = ParagraphStyle(
        name='Bold',
        fontName='Archivo-SemiBold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#231f20')
    )
    title = ParagraphStyle(
        name='Title',
        fontName='Archivo-SemiExpanded-SemiBold',
        fontSize=12,
        leading=14,
        textColor=colors.HexColor('#231f20')
    )
    subtitle = ParagraphStyle(
        name='Title',
        fontName='Archivo-SemiExpanded-SemiBold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#231f20')
    )
    keyword = ParagraphStyle(
        name='Keyword',
        fontName='Archivo-SemiExpanded-SemiBold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#231f20')
    )

    # PRODUKT
    unix_time = int(time.time())
    elements.append(Paragraph("Produkt", title))
    elements.append(Spacer(1,10))
    elements.append(Paragraph(f'nr {unix_time}',subtitle))

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

    details_data = [
        ["Wybrana linia stylu:", f'{data["styleLine"]}'],
        ["Wybrane użycie produktu:", f'{data["usecase"]}'],
        ["Wybrany rodzaj produktu:", f'{data["type"]}'],
        ["Wybrane dodatki:", f'{data["additivies"]}'],
        ["Wybrany kolor:", f'{data["color"]}'],
    ]

    if tab[0]:
        details_data.append(["wybrane elementy smart home:", f'{tab[0]}'])
    else:
        details_data.append(["", ""])
        details_data.append(["", ""])
        details_data.append(["", ""])
    if tab[1]:
        details_data.append(["", f'{tab[1]}'])
    else:
        details_data.append(["", ""])
        details_data.append(["", ""])
    if tab[2]:
        details_data.append(["", f'{tab[2]}'])
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
        colWidths=[usable_width*0.55, usable_width*0.45],
    )

    details_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), -2),
    ]))

    elements.append(details_table),
    elements.append(Spacer(1,340))

    keyword = Paragraph('Comments', keyword)
    elements.append(keyword)
    elements.append(Spacer(1,10))



    left_comment = """
        VAT is not added to the above prices.<br/>
        The offer does not include transport.<br/>
        The offer does not include assembly.<br/>
        Expiry date: 30 days<br/>
        Payment terms: to be agreed<br/>
        Completion date: to be agreed<br/><br/>
        Powyższe przykładowe z aktualnej „Oferty” -<br/>
        potencjalnie do dodania komentarze w pdf jeżeli dotyczy<br/>
    """

    if mail== '':
        right_comment = """
            05.02.2026 
        """
    else:
        right_comment = f"""
            Zapytanie przygotowne przez: {mail}<br/>
            05.02.2026 
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
    elements.append(Spacer(1,100))


    left_footer = """
        <font backColor="#ACCFE1"></font><br/>
        <br/>
        <br/>
    """
    right_footer = """
        <br/>
        <br/>
        PHONE..........(+48) 81 749 23 10<br/>
    """
    logo = Image(finders.find('logo/Argo-Logo.png'),
                 width=38,
                 height=32)

    footer_data = [
        ["ARGO SP. Z O.O.", "NIP.........................7122293543"],
        ["UL. TOKARSKA 21", "REGON.....................060108877"],
        ["20-210 LUBLIN", "PHONE..........(+48) 81 749 23 10"],
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
        colWidths=[usable_width*0.7-23, usable_width*0.3-25, 32],
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
        ('LEFTPADDING', (0,0), (-1,-1), -2),
        ('RIGHTPADDING', (0,0), (-1,-1), -2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), -2),
    ]))
    elements.append(footer_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

