from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import StudentParent, SubjectTypes
from .models import Subjects
from .models import ClassStudents, Classes, Users, Mails
import random, time
from django.core.exceptions import ValidationError



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )



class DelSubjectTypeForm(forms.Form):
    typeId = forms.IntegerField(help_text="Wpisz ID przedmiotu do usunięcia.")
    


class SubjectTypeForm(ModelForm):
    class Meta:
        model = SubjectTypes
        fields = ['typeId', 'typeName', 'description']

    def __init__(self, *args, **kwargs):
        super(SubjectTypeForm, self).__init__(*args, **kwargs)
        self.fields['typeId'].widget = forms.HiddenInput()
    
        
class SubjectForm(ModelForm):
    class Meta:
        model = Subjects
        fields = '__all__'



class delGradetypeForm(forms.Form):
    gradetypeId = forms.IntegerField(widget=forms.HiddenInput())



class addGradetypeForm(forms.Form):
    typeName = forms.CharField(max_length=100, label='Nazwa')
    weight = forms.DecimalField(label='Wartość')



class editGradetypeForm(forms.Form):
    typeName = forms.CharField(max_length=100, label='Nazwa')
    weight = forms.DecimalField(label='Wartość')



class SubjectChoice(forms.Form):
    subjects = SubjectTypes.objects.all()
    subjects_choices = [(subject.typeId, subject.typeName) for subject in subjects]
    choosen_subject = forms.ChoiceField(choices=subjects_choices)



class MailForm(forms.ModelForm):
    class Meta:
        model = Mails
        fields = ('toId', 'topic', 'mailText')



class AddClassForm(forms.ModelForm):
    activeFrom = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label = 'Aktywna od')
    activeTo = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label = 'Aktywna do')

    class Meta:
        model = Classes
        fields = ['className', 'homeroomTeacher', 'activeFrom', 'activeTo']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.classId = generate_unique_integer_id()
        if commit:
            instance.save()
        return instance



def generate_unique_integer_id():
    timestamp = int(time.time())
    random_number = random.randint(1000, 9999)
    unique_id = int(f"{timestamp}{random_number}")
    return unique_id



class editClassForm(forms.ModelForm):
    activeFrom = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label = 'Aktywna od')
    activeTo = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label = 'Aktywna do')

    class Meta:
        model = Classes
        fields = ['className', 'homeroomTeacher', 'activeFrom', 'activeTo']



class delClassForm(forms.Form):
    classId = forms.IntegerField(widget=forms.HiddenInput())



class AssignStudentsForm(forms.ModelForm):
    activeFrom = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    activeTo = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = ClassStudents
        fields = ['studentId', 'classId', 'activeFrom', 'activeTo']



class AddStudentParentForm(forms.ModelForm):
    class Meta:
        model = StudentParent
        fields = ['studentId', 'parentId']

    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get('studentId')
        parent_id = cleaned_data.get('parentId')

        if student_id and parent_id and student_id == parent_id:
            raise ValidationError("ID ucznia i rodzica nie mogą być takie same.")

        existing_record = StudentParent.objects.filter(studentId=student_id, parentId=parent_id).exists()
        if existing_record:
            raise ValidationError("Podane dane znajdują się już w bazie.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance




class delStudentParentForm(forms.Form):
    studentId = forms.CharField(widget=forms.HiddenInput())
    parentId = forms.CharField(widget=forms.HiddenInput())