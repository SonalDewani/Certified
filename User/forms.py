from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


# Manager creates distributor
class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'role', 'password1', 'password2']


# Admin creates manager
class ManagerCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'manager'
        if commit:
            user.save()
        return user