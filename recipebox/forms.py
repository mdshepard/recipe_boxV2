from django import forms

from recipebox.models import *


class AuthorAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(AuthorAddForm, self).__init__(*args, **kwargs)
        if user.is_staff:
            self.fields["user"].queryset = Author.objects.all()
        else:
            self.fields["user"].queryset = Author.objects.filter(user=user)

    user = forms.ModelChoiceField(queryset=None)
    bio = forms.CharField(widget=forms.Textarea)


class RecipeAddForm(forms.Form):
    title = forms.CharField(max_length=160)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    time_required = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class UpdateForm(forms.Form):
    """version 2"""
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    time = forms.IntegerField()
    instructions = forms.CharField(widget=forms.Textarea)
