from django import forms
from .models import Seminar


class SeminarForm(forms.ModelForm):
    class Meta:
        model = Seminar
        fields = ['title', 'topic', 'description', 'date_time', 'location']

        widgets = {
            "date_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
