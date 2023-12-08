from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404

from GradjaApp.forms import SignUpForm
from .decorators import not_logged_in_required, user_with_required_group

# Create your views here.
from .models import GradeType
from .forms import delGradetypeForm
from .forms import addGradetypeForm


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

def add_gradetype(request):
    if request.method == 'POST':
        form = addGradetypeForm(request.POST)
        if form.is_valid():
            # Obsługa poprawnego wypełnienia formularza
            # (np. zapis danych do bazy danych)
            return redirect('sukces')
    else:
        form = addGradetypeForm()
    return render(request, "add_gradetype.html", {'form' : form})
