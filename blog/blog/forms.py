from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import Field

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'placeholder': 'Search'}))

