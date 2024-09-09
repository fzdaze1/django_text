from .models import Queries

from django import forms


class QueryCreateForm(forms.ModelForm):

    class Meta:
        model = Queries
        fields = ['query']
        labels = {
            'query': 'Введите текст для видео',
        }
        widgets = {
            'query': forms.TextInput(attrs={'placeholder': 'Введите текст до 100 символов'}),
        }
