from django import forms
from django.contrib.auth.forms import UserCreationForm
from GradjaApp.models import Users


# Forma do rejestracji
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )

class delGradetypeForm(forms.Form):
    gradetypeId = forms.IntegerField(widget=forms.HiddenInput())

class addGradetypeForm(forms.Form):
    field1 = forms.CharField(max_length=100)