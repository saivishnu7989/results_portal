from django import forms
from captcha.fields import CaptchaField

class UploadResultsForm(forms.Form):
    file = forms.FileField(label="Select Excel file")
    regulation = forms.CharField(max_length=10)
    branch = forms.CharField(max_length=100)
    captcha = CaptchaField()
    

class CheckResultForm(forms.Form):
    roll_number = forms.CharField(max_length=20)
    captcha = CaptchaField()
