from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import RegistrationForm, ContactForm
from .forms import RegistrationForm
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError


def landing(request):
    return render(request, 'landing/landing.html')


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/landing')
    else:
        form = RegistrationForm()

    return render(request, 'landing/signup.html', {"form": form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('prototype:dashboard')
        else:
            messages.error(request, 'Email or Password does not exist')

    return HttpResponse(request, 'landing/login.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Inquiry"
            body = {
                'fullname': form.cleaned_data['fullname'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                # feel free to change the email to test##
                send_mail(subject, message, 'email', ['ekendukwe@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse('Success! Thank you for your message.')

    form = ContactForm()
    return render(request, "landing/contact.html", {'form': form})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')
    return render(request, 'landing/contact.html')


def reset(request):
    return render(request, 'landing/reset.html')


def support(request):
    return render(request, 'landing/support.html')


def authTable(request):
    return render(request, 'landing/fileAuthen.html')
