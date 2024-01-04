from django import forms

class AccessForm(forms.Form):
    password = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter access code'}),
        label=False 
    )