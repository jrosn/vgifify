from django import forms


class UploadVideoForm(forms.Form):
    file = forms.FileField()

class ConvertForm(forms.Form):
    pass
