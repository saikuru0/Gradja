from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .decorators import not_logged_in_required, user_with_required_group
from GradjaApp.forms import SignUpForm
from .forms import AddClassForm, AssignStudentsForm

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
def add_class(request):
    if request.method == 'POST':
        form = AddClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddClassForm()

    return render(request, 'add_class.html', {'form': form})


@user_with_required_group('admin')
def assign_students(request):
    if request.method == 'POST':
        form = AssignStudentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AssignStudentsForm()

    return render(request, 'assign_students.html', {'form': form})
