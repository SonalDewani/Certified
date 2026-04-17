from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserCreateForm, ProfileUpdateForm
from .forms import ManagerCreateForm
from .decorators import role_required
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy



def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

# 🔹 Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# 🔹 Logout
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'profile.html', {
        'user': request.user
    })


@login_required
def edit_profile(request):
    form = ProfileUpdateForm(request.POST or None, instance=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully")
        return redirect('profile')

    return render(request, 'edit_profile.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('profile')



@login_required
def dashboard_view(request):
    if request.user.role == 'admin':
        return render(request, 'admin_dashboard.html')

    elif request.user.role == 'manager':
        return render(request, 'manager_dashboard.html')

    else:
        return render(request, 'user_dashboard.html')


@login_required
@role_required(['admin'])
def create_manager(request):
    if request.method == 'POST':
        form = ManagerCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ManagerCreateForm()

    return render(request, 'create_manager.html', {'form': form})


@login_required
@role_required(['manager'])
def create_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'distributor'  # force role
            user.save()
            return redirect('dashboard')
    else:
        form = UserCreateForm()

    return render(request, 'create_user.html', {'form': form})