import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from django.conf import settings


def generate_certificate(registration):

    seminar = registration.seminar
    user = registration.user

    file_name = f'certificate_{registration.id}.pdf'

    file_path = os.path.join(
        settings.MEDIA_ROOT,
        'certificates',
        file_name
    )

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    # LANDSCAPE A4
    c = canvas.Canvas(
        file_path,
        pagesize=landscape(A4)
    )

    width, height = landscape(A4)

    # =========================
    # DOUBLE BORDER
    # =========================

    c.setLineWidth(4)
    c.rect(
        30,
        30,
        width-60,
        height-60
    )

    c.setLineWidth(1.5)
    c.rect(
        45,
        45,
        width-90,
        height-90
    )

    # =========================
    # TOP LOGOS
    # =========================

    if seminar.certificate_logo_left:
        c.drawImage(
            seminar.certificate_logo_left.path,
            80,
            height-140,
            width=90,
            height=90,
            preserveAspectRatio=True
        )

    if seminar.certificate_logo_right:
        c.drawImage(
            seminar.certificate_logo_right.path,
            width-170,
            height-140,
            width=90,
            height=90,
            preserveAspectRatio=True
        )

    # =========================
    # ORGANIZATION NAME
    # =========================

    c.setFont("Helvetica-Bold",18)

    c.drawCentredString(
        width/2,
        height-90,
        "CERTIFIED SEMINAR MANAGEMENT"
    )

    # =========================
    # MAIN TITLE
    # =========================

    c.setFont("Helvetica-Bold",34)

    c.drawCentredString(
        width/2,
        height-180,
        "CERTIFICATE OF PARTICIPATION"
    )

    # =========================
    # BODY TEXT
    # =========================

    c.setFont("Helvetica",18)

    c.drawCentredString(
        width/2,
        height-260,
        "This certificate is proudly presented to"
    )

    # Recipient Name Highlight
    c.setFont("Helvetica-Bold",30)

    full_name = (
        f"{user.first_name} {user.last_name}"
    ).strip()

    if not full_name:
        full_name = user.username

    c.drawCentredString(
        width/2,
        height-320,
        full_name
    )

    # Participation text
    c.setFont("Helvetica",18)

    c.drawCentredString(
        width/2,
        height-390,
        "for successful participation in"
    )

    # Seminar Name
    c.setFont("Helvetica-Bold",24)

    c.drawCentredString(
        width/2,
        height-440,
        seminar.title
    )

    # Optional date if available
    if hasattr(seminar, 'date') and seminar.date:
        c.setFont("Helvetica",16)

        c.drawCentredString(
            width/2,
            height-490,
            f"Conducted on {seminar.date}"
        )

    # =========================
    # SIGNATURE SECTION
    # =========================

    # Signature line
    c.line(
        width-260,
        120,
        width-120,
        120
    )

    # Signature image
    if seminar.certificate_signature:
        c.drawImage(
            seminar.certificate_signature.path,
            width-230,
            125,
            width=100,
            height=50,
            preserveAspectRatio=True
        )

    c.setFont("Helvetica",14)

    c.drawCentredString(
        width-190,
        100,
        "Authorized Signature"
    )

    # Left date line
    c.drawCentredString(
        190,
        120,
        f"{seminar.date_time.date()}"
    )

    c.drawCentredString(
        190,
        100,
        "Date"
    )

    # =========================
    # SAVE PDF
    # =========================

    c.save()

    return file_name