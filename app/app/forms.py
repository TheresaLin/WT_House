from django import forms

class img_text_form(forms.Form):
    img_path = forms.CharField(max_length=100000)
    text = forms.CharField(max_length=100000)