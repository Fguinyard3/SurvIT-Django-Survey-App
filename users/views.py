#create a django view that will be used to register a new user
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout
from django.contrib.auth.views import password_reset as django_password_reset
from django.contrib.auth.views import password_reset_confirm as django_password_reset_confirm
from django.contrib.auth.views import password_reset_complete as django_password_reset_complete
from django.contrib.auth.views import password_reset_done as django_password_reset_done
from django.contrib.auth.views import password_reset_done as django_password_reset_done
from django.contrib.auth.views import password_reset_confirm as django_password_reset_confirm
from django.urls import reverse_lazy

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

#create a django view that will be used to reset a user's password
def password_reset(request):
    return django_password_reset(request,
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',
        redirect = reverse_lazy('users:password_reset_done'),