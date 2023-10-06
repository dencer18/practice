from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserBioForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(label = "Your age", min_value=1, max_value=100)
    bio = forms.CharField(label="Biography", widget =forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile)->None:
    if file.name and "virus" in file.name:
        raise ValidationError("file name shoud not contain 'virus'")

def validate_file_size(file: InMemoryUploadedFile)->None:
    print(f"file size {file.size} Bites")
    if file.name and file.size > 1000000:
        raise ValidationError("file size more then 1MB")


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name,
                                        validate_file_size
                                        ])
