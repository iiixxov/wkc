from django import forms
from .models import *

class Words_input(forms.Form):
    words = forms.CharField(max_length=250)
    size = forms.IntegerField(max_value=50, min_value=20)
    difinition = forms.ChoiceField(choices=(
        (1, 'Одно'),
        (2, 'Несколько'),
        (0, 'Нет'),
    ))