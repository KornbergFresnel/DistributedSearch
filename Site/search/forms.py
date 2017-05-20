from django.forms import widgets
from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(required=True, label='search_input', widget=widgets.TextInput(attrs={'placeholder': 'Search text or href', 'class': 'form-control'}))
