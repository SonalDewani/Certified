from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


# Manager creates distributor
class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.role = 'distributor'
            if commit:
                user.save()
            return user


# Admin creates manager
class ManagerCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'manager'
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone']
