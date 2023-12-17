from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import StudentParent, SubjectTypes
from .models import ClassStudents, Classes, Users, Mails, GradeType, GradeValue, Grades, SubjectTypes, Subjects
import random, time



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
    chosen_subject = forms.ModelChoiceField(
        queryset=Subjects.objects.all(),
        label='Przedmiot'
    )



class AddOneGrade(forms.ModelForm):
    gradeId = forms.IntegerField(widget=forms.HiddenInput())
    classId = forms.ModelChoiceField(
        queryset=Subjects.objects.all(),
        label='Przedmiot',
        widget=forms.HiddenInput()
    )
    studentId = forms.ModelChoiceField(
        queryset=Users.objects.all(),
        label='Student'
    )

    typeId = forms.ModelChoiceField(
        queryset=GradeType.objects.all(),
        empty_label=None,
        label='Za co'
    )

    gradeValueId = forms.ModelChoiceField(
        queryset=GradeValue.objects.all(),
        empty_label=None,  # Bez opcji pustej
        label='Ocena'
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}),  # Dostosuj liczność wierszy i kolumn
        label='Opis'
    )

    class Meta:
        model = Grades
        fields = ('gradeId', 'classId', 'studentId', 'gradeValueId', 'typeId', 'description')

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['gradeId'] = generate_unique_integer_id()

        if 'classId' in self.initial:
            class_id = self.initial['classId'].classId
            self.fields['studentId'].queryset = Users.objects.filter(
                id__in=ClassStudents.objects.filter(classId=class_id).values('studentId')
            )



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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['homeroomTeacher'].queryset = Users.objects.filter(groups__name='teacher')

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['homeroomTeacher'].queryset = Users.objects.filter(groups__name='teacher')



class delClassForm(forms.Form):
    classId = forms.IntegerField(widget=forms.HiddenInput())



class AssignStudentsForm(forms.ModelForm):
    activeFrom = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    activeTo = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = ClassStudents
        fields = ['studentId', 'classId', 'activeFrom', 'activeTo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['studentId'].queryset = Users.objects.filter(groups__name='student')



class AddStudentParentForm(forms.ModelForm):
    class Meta:
        model = StudentParent
        fields = ['studentId', 'parentId']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['studentId'].queryset = Users.objects.filter(groups__name='student')
        self.fields['parentId'].queryset = Users.objects.filter(groups__name='parent')

    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get('studentId')
        parent_id = cleaned_data.get('parentId')

        existing_record = StudentParent.objects.filter(studentId=student_id, parentId=parent_id).exists()
        if existing_record:
            raise forms.ValidationError("Podane dane znajdują się już w bazie.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



class delStudentParentForm(forms.Form):
    studentId = forms.CharField(widget=forms.HiddenInput())
    parentId = forms.CharField(widget=forms.HiddenInput())