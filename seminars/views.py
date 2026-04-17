from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SeminarForm
from User.decorators import role_required
from .models import Seminar, SeminarRegistration
from django.shortcuts import get_object_or_404
from django.contrib import messages

from .utils.email_service import send_id_card_email
from .utils.id_card_generator import generate_id_card


# 🔹 Manager creates seminar
@login_required
@role_required(['manager'])
def create_seminar(request):
    if request.method == 'POST':
        form = SeminarForm(request.POST)
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
@role_required(['manager'])
def manager_seminars(request):
    seminars = Seminar.objects.filter(created_by=request.user)
    return render(request, 'manager_seminars.html', {'seminars': seminars})


# 🔹 Users view all seminars
@login_required
def user_seminars(request):
    seminars = Seminar.objects.all()
    return render(request, 'user_seminars.html', {'seminars': seminars})


@login_required
@role_required(['distributor'])
def register_seminar(request, seminar_id):
    seminar = Seminar.objects.get(id=seminar_id)
    user = request.user

    # Prevent duplicate registration
    if SeminarRegistration.objects.filter(user=user, seminar=seminar).exists():
        return redirect('dashboard')

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
@role_required(['manager'])
def seminar_registrations(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id)

    registrations = SeminarRegistration.objects.filter(seminar=seminar)

    return render(request, 'seminar_registrations.html', {
        'seminar': seminar,
        'registrations': registrations
    })
