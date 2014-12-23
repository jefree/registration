from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User

from .models import ActivationRecord

from datetime import datetime

def send_activation_mail(request, record):

    html = render_to_string('registration/activation_email.html', {'record': record, 'site': get_current_site(request)})

    send_mail('Activacion de tu cuenta en Gamestery Platform', '', 'Gamestery UD', [record.user.email], fail_silently=True, html_message=html)

def create_inactive_user(form):
    
    user = User.objects.create_user(username=form.cleaned_data['email'], password=form.cleaned_data['password'])

    user.first_name=form.cleaned_data['name'] 
    user.last_name=form.cleaned_data['lastname']
    user.email=form.cleaned_data['email'] 
    user.is_active=False

    user.save()

    return user

def create_activation_record(user):
    record = ActivationRecord(user=user, registration_date=datetime.now().date())

    record.create_key()
    record.save()

    return record
