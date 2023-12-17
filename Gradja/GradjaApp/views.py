from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Mails,GradeType, Classes, StudentParent
from GradjaApp.forms import SignUpForm, MailForm
from .forms import AddClassForm, AddStudentParentForm, AssignStudentsForm, delClassForm, delStudentParentForm, editClassForm
from .forms import delGradetypeForm, editGradetypeForm, SubjectChoice, addGradetypeForm
from .decorators import not_logged_in_required, user_with_required_group
from .models import SubjectTypes
from .forms import DelSubjectTypeForm
from .forms import SubjectTypeForm
from .models import SubjectTypes
from .models import Subjects
from .forms import SubjectForm



def home(request):
    return render(request, "home.html", {})



@not_logged_in_required
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



@user_with_required_group('teacher')
def set_grades(request):
    return render(request, 'set_grades.html', {})



@user_with_required_group('admin')
def set_type_subject(request):
    if request.method == 'POST':
        postForm = DelSubjectTypeForm(request.POST)
        if postForm.is_valid():
            type_id = postForm.cleaned_data['typeId']
            subject_type = SubjectTypes.objects.get(typeId=type_id)
            subject_type.delete()

    subject_types = SubjectTypes.objects.all()
    form = DelSubjectTypeForm()
    return render(request, "set_type_subject.html", {'subject_types': subject_types, 'form': form})



@user_with_required_group('admin')
def add_subjecttype(request):
    if request.method == 'POST':
        form = SubjectTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('set_type_subject')
    else:
        form = SubjectTypeForm()

    return render(request, 'add_subjecttype.html', {'form': form})



@user_with_required_group('admin')
def edit_subject_type(request, typeId):
    subject_type = get_object_or_404(SubjectTypes, typeId=typeId)
    if request.method == 'POST':
        form = SubjectTypeForm(request.POST, instance=subject_type)
        if form.is_valid():
            form.save()
            return redirect('set_type_subject')
    else:
        form = SubjectTypeForm(instance=subject_type)

    return render(request, 'edit_subject_type.html', {'form': form})



@user_with_required_group('admin')
def view_subjects(request):
    subjects = Subjects.objects.all()
    return render(request, "view_subjects.html", {'subjects': subjects})



@user_with_required_group('admin')
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_subjects')
    else:
        form = SubjectForm()
    return render(request, 'add_subject.html', {'form': form})



@user_with_required_group('admin')
def edit_subject(request, subjectId):
    subject = get_object_or_404(Subjects, subjectId=subjectId)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('view_subjects')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'edit_subject.html', {'form': form})



@user_with_required_group('admin')
def set_gradetype(request):
    if request.method == 'POST':
        postForm = delGradetypeForm(request.POST)
        if postForm.is_valid():
            gradetype_id = postForm.cleaned_data['gradetypeId']
            gradetypes = GradeType.objects.get(typeId=gradetype_id)
            gradetypes.delete()
    gradetypes = GradeType.objects.all()
    form = delGradetypeForm()
    return render(request, "set_gradetype.html", {'gradetypes' : gradetypes, 'form' : form})



def add_gradetype(request):
    if request.method == 'POST':
        form = addGradetypeForm(request.POST)
        if form.is_valid():
            type_name = form.cleaned_data['typeName']
            weight = form.cleaned_data['weight']

            new_grade_type = GradeType(typeName=type_name, weight=weight)
            new_grade_type.save()

            return redirect('set_gradetype')

    else:
        form = addGradetypeForm()

    context = {'form': form}
    return render(request, "add_gradetype.html", context)



def edit_gradetype(request, gradetype_id):
    gradetype = get_object_or_404(GradeType, typeId=gradetype_id)

    if request.method == 'POST':
        form = editGradetypeForm(request.POST)
        if form.is_valid():
            gradetype.typeName = form.cleaned_data['typeName']
            gradetype.weight = form.cleaned_data['weight']
            gradetype.save()

            return redirect('set_gradetype')

    else:
        form = editGradetypeForm(initial={'typeName': gradetype.typeName, 'weight': gradetype.weight})

    context = {'form': form, 'gradetype': gradetype}
    return render(request, "edit_gradetype.html", context)



def view_mail(request, mail_id):
    mail = get_object_or_404(Mails, mailId=mail_id)
    return render(request, 'view_mail.html', {'mail': mail})



def grade_view(request):
    return render(request, 'grades.html', {})



def add_grade_subject_choice(request):
    if request.method == 'POST':
        form = SubjectChoice(request.POST)
        if form.is_valid():
            pass
    else:
        form = SubjectChoice()

    return render(request, 'grades_choice.html', {'form': form})



def send_mail(request):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            mail = form.save(commit=False)
            mail.fromId = request.user
            mail.sendDate = timezone.now()
            mail.save()
            return redirect('inbox')
    else:
        form = MailForm()

    return render(request, 'send_mail.html', {'form': form})



def inbox(request):
    user_mails = Mails.objects.filter(toId=request.user)
    sent_mails = Mails.objects.filter(fromId=request.user)
    return render(request, 'inbox.html', {'user_mails': user_mails, 'sent_mails': sent_mails})



@user_with_required_group('admin')
def set_class(request):
    if request.method == 'POST':
        postForm = delClassForm(request.POST)
        if postForm.is_valid():
            class_id = postForm.cleaned_data['classId']
            classes = Classes.objects.get(classId=class_id)
            classes.delete()
    classes = Classes.objects.all()
    form = delClassForm()
    return render(request, 'set_class.html', {'classes': classes, 'form' : form})



@user_with_required_group('admin')
def add_class(request):
    if request.method == 'POST':
        form = AddClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_class')
    else:
        form = AddClassForm()

    return render(request, 'add_class.html', {'form': form})



def edit_class(request, class_id):
    instance = get_object_or_404(Classes, classId=class_id)

    if request.method == 'POST':
        form = editClassForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('set_class')

    else:
        form = editClassForm(instance=instance)

    context = {'form': form, 'class': instance}
    return render(request, "edit_class.html", context)



@user_with_required_group('admin')
def assign_students(request):
    if request.method == 'POST':
        form = AssignStudentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assign_students')
    else:
        form = AssignStudentsForm()

    return render(request, 'assign_students.html', {'form': form})


@user_with_required_group('admin')
def set_student_parent(request):
    if request.method == 'POST':
        postForm = delStudentParentForm(request.POST)
        print("blablabla")
        if postForm.is_valid():
            student_id = postForm.cleaned_data['studentId']
            parent_id = postForm.cleaned_data['parentId']
            print('bla', student_id, parent_id)
            student_parent = get_object_or_404(StudentParent, studentId=student_id, parentId=parent_id)
            student_parent.delete()

    student_parent = StudentParent.objects.all()
    form = delStudentParentForm()
    return render(request, 'set_student_parent.html', {'student_parent': student_parent, 'form': form})



@user_with_required_group('admin')
def add_student_parent(request):
    if request.method == 'POST':
        form = AddStudentParentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('set_student_parent')
    else:
        form = AddStudentParentForm()

    return render(request, 'add_student_parent.html', {'form': form})
