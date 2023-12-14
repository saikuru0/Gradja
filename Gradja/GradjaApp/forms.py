from django import forms
from django.contrib.auth.forms import UserCreationForm
from GradjaApp.models import Users
from django.forms import ModelForm
from .models import SubjectTypes
from .models import Subjects

# Forma do rejestracji
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )
        
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )

# Forma do usuwania typu przedmiotu
class DelSubjectTypeForm(forms.Form):
    typeId = forms.IntegerField(help_text="Enter the ID of the subject type to delete")
    
# Form do dodawania
class SubjectTypeForm(ModelForm):
    class Meta:
        model = SubjectTypes
        fields = ['typeId', 'typeName', 'description']
        
class SubjectForm(ModelForm):
    class Meta:
        model = Subjects
        fields = '__all__'
        