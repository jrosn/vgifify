from django import forms


class UploadVideoForm(forms.Form):
    file = forms.FileField()

class ConvertForm(forms.Form):
    framerate = forms.IntegerField(min_value=1, max_value=20)
