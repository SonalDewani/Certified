import base64
from datetime import timedelta
from io import BytesIO

import qrcode
from Certified import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SeminarForm
from User.decorators import role_required
from .models import Seminar, SeminarRegistration
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField
from .utils.email_service import send_id_card_email
from .utils.id_card_generator import generate_id_card
from django.utils import timezone
import random
import string


# 🔹 Manager creates seminar
@login_required
@role_required(['manager'])
def create_seminar(request):
    if request.method == 'POST':
        form = SeminarForm(request.POST, request.FILES)
        if form.is_valid():
            seminar = form.save(commit=False)
            seminar.created_by = request.user
            seminar.save()
            return redirect('manager_seminars')
    else:
        form = SeminarForm()

    return render(request, 'create_seminar.html', {'form': form})


# 🔹 Manager view own seminars
@login_required
@role_required(['manager', 'admin'])
def manager_seminars(request):
    seminars = Seminar.objects.filter(
        created_by=request.user
    ).order_by('-created_at')  # newest first

    return render(request, 'manager_seminars.html', {
        'seminars': seminars
    })


# 🔹 Users view all seminars
@login_required
def user_seminars(request):
    seminars = Seminar.objects.all()

    status = request.GET.get('status')

    registered_seminars = (
        SeminarRegistration.objects.filter(
            user=request.user
        ).values_list(
            'seminar_id',
            flat=True
        )
    )

    if status == 'upcoming':

        seminars = seminars.filter(
            date_time__date__gt=timezone.now().date()
        )

    elif status == 'completed':

        seminars = seminars.filter(
            date_time__date__lt=timezone.now().date()
        )

    return render(request, 'user_seminars.html', {
        'seminars': seminars,
        'registered_seminars':registered_seminars,
    })


@login_required
@role_required(['distributor'])
def register_seminar(request, seminar_id):
    seminar = Seminar.objects.get(id=seminar_id)
    user = request.user
    if not seminar.registration_open:
        messages.error(
            request,
            "Registration is closed."
        )

        return redirect(
            'seminar_detail',
            seminar_id=seminar.id
        )

    # Prevent duplicate registration
    if SeminarRegistration.objects.filter(
            user=user,
            seminar=seminar
    ).exists():
        messages.warning(
            request,
            "You have already registered for this seminar."
        )

        return redirect('user_seminars')

    registration = SeminarRegistration.objects.create(
        user=user,
        seminar=seminar
    )

    # ✅ Generate ID Card
    file_path = generate_id_card(user, seminar, registration)

    # Save file path in model
    registration.id_card = f"id_cards/id_card_{registration.id}.pdf"
    registration.save()

    # ✅ Send Email
    print("Sending email...")
    send_id_card_email(user, seminar, file_path)
    print("Email function called")

    return redirect('dashboard')


@login_required
@role_required(['manager', 'admin'])
def seminar_registrations(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id)

    registrations = SeminarRegistration.objects.filter(seminar=seminar)

    return render(request, 'seminar_registrations.html', {
        'seminar': seminar,
        'registrations': registrations
    })


@login_required
@role_required(['distributor'])
def my_registrations(request):
    registrations = SeminarRegistration.objects.filter(user=request.user).order_by('-registered_at')

    return render(request, 'my_registrations.html', {
        'registrations': registrations
    })


def generate_attendance_code(length=6):
    return ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=length
        )
    )


@login_required
@role_required(['manager', 'admin'])
def generate_attendance_qr(request, seminar_id):

    seminar = get_object_or_404(Seminar, id=seminar_id)

    # If QR already exists → reuse it
    if not seminar.attendance_code:
        code = generate_attendance_code()

        seminar.attendance_code = code
        seminar.attendance_code_created_at = timezone.now()
        seminar.save()
    else:
        code = seminar.attendance_code

    # URL inside QR
    url = f"{settings.Base_Url}/seminars/mark-attendance/{seminar.id}/?code={code}"

    # Generate QR image
    qr = qrcode.make(url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(
        request,
        'attendance_qr.html',
        {
            'qr': qr_base64,
            'seminar': seminar
        }
    )


@login_required
def mark_attendance(request, seminar_id):
    code = request.GET.get('code')

    seminar = get_object_or_404(Seminar, id=seminar_id)

    # Validate code
    if not code or code != seminar.attendance_code:
        return HttpResponse("Invalid QR Code ❌")

    # expiry = 60 minutes
    if not seminar.attendance_code_created_at or \
            timezone.now() - seminar.attendance_code_created_at > timedelta(minutes=60):
        return HttpResponse("Attendance Closed ❌")

    registration = get_object_or_404(
        SeminarRegistration,
        user=request.user,
        seminar=seminar
    )

    if registration.attended:
        return HttpResponse("Already marked ✅")

    registration.attended = True
    registration.save()

    return HttpResponse("Attendance marked successfully ✅")


def verify_idcard(request, token):

    registration = get_object_or_404(
        SeminarRegistration,
        verification_token=token
    )

    return render(
        request,
        'verify_idcard.html',
        {
            'registration': registration
        }
    )