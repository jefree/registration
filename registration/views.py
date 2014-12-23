from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse
from django.conf import settings

from . import util
from .models import ActivationRecord
from .forms import RegistrationForm

from datetime import datetime

def register_view(request):

    if request.method == 'GET':
        return render(request, 'registration/register.html')

    elif request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():
            
            user = util.create_inactive_user(form)
            record = util.create_activation_record(user)

            util.send_activation_mail(request, record)

            return render(request, 'registration/register_success.html', {'user': user})

        else:
            return render(request, 'registration/register.html', {'form': form})

def activation_view(request, key):

    try:
        record = ActivationRecord.objects.get(key=key)
    except ActivationRecord.DoesNotExist:
        return HttpResponse('Bad Request', status=404)

    user = record.user

    if user.is_active:
        return HttpResponse('Bad Request', status=404)

    user.is_active = True
    user.date_joined = datetime.now().date()

    user.save()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    if hasattr(settings, 'ACTIVATION_REDIRECT_URL'):
        url = settings.ACTIVATION_REDIRECT_URL
    else:
        url = '/'

    return redirect(url)


def login_view(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')

            else:
                return render(request, 'registration/login.html', {'inactive': True})
        else:
            return render(request, 'registration/login.html', {'error': True})

def logout_view(request):
    logout(request)
    return redirect('landing')
