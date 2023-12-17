from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Mails, GradeType, Classes, SubjectTypes, Subjects
from .forms import SignUpForm, MailForm
from .forms import AddClassForm, AssignStudentsForm, delClassForm, editClassForm
from .forms import delGradetypeForm, editGradetypeForm, SubjectChoice, addGradetypeForm, AddOneGrade, Grades
from .decorators import not_logged_in_required, user_with_required_group

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


# Przyklad uzycia dekoratora -> do zmiany lub calkowitego usuniecia.
@user_with_required_group('teacher')
def set_grades(request):
    return render(request, 'set_grades.html', {})



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


@user_with_required_group('admin')
def add_gradetype(request):
    if request.method == 'POST':
        form = addGradetypeForm(request.POST)
        if form.is_valid():
            # Jeśli formularz jest poprawny, pobierz dane z formularza
            type_name = form.cleaned_data['typeName']
            weight = form.cleaned_data['weight']

            # Stwórz nowy obiekt modelu GradeType i zapisz go w bazie danych
            new_grade_type = GradeType(typeName=type_name, weight=weight)
            new_grade_type.save()

            return redirect('set_gradetype')

    else:
        form = addGradetypeForm()

    context = {'form': form}
    return render(request, "add_gradetype.html", context)


@user_with_required_group('admin')
def edit_gradetype(request, gradetype_id):
    gradetype = get_object_or_404(GradeType, typeId=gradetype_id)

    if request.method == 'POST':
        form = editGradetypeForm(request.POST)
        if form.is_valid():
            gradetype.typeName = form.cleaned_data['typeName']
            gradetype.weight = form.cleaned_data['weight']
            gradetype.save()

            # Przekieruj gdzieś po zakończeniu edycji
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
            chosen = form.cleaned_data['chosen_subject']
            selected_subject = chosen.subjectId
            request.session['chosen_subject'] = selected_subject
            return redirect('add_one_grade')
    else:
        form = SubjectChoice()

    return render(request, 'grades_choice.html', {'form': form})


def add_one_grade(request):
    if request.method == 'POST':
        form = AddOneGrade(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect('grades_choice')

    else:
        selected_subject = request.session.get('chosen_subject', None)
        subject = Subjects.objects.filter(subjectId=selected_subject).first()
        form = AddOneGrade(initial={'classId': subject})

    context = {'form': form, 'selected_subject': selected_subject, }
    return render(request, "add_one_grade.html", context)



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