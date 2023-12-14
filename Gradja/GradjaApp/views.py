from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Mails

from GradjaApp.forms import SignUpForm, MailForm
from .decorators import not_logged_in_required, user_with_required_group

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
