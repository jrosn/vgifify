from django import forms


class UploadVideoForm(forms.Form):
    file = forms.FileField()
