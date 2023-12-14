from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from GradjaApp.forms import SignUpForm
from .decorators import not_logged_in_required, user_with_required_group
from .models import SubjectTypes
from .forms import DelSubjectTypeForm
from .forms import SubjectTypeForm
from .forms import SubjectTypeForm

from .models import SubjectTypes
from django.shortcuts import get_object_or_404

from .models import Subjects
from .forms import SubjectForm


# Create your views here.

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

#Start: Subject types:
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
#End: Subject types

#Start: Subjects
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
#End: Subjects