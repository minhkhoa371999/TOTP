
import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .templates.pyotp.genOTP import genOTP
from .forms import RegisterForm, OTPForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import OTP


def register_request(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("users:login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterForm()
    return render(request=request, template_name="Register/register.html", context={"register_form": form})


def login_request(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                otp_user = OTP.objects.get(user_id=user.id)
                _user = User.objects.get(id=user.id)
                start = _user.date_joined.timestamp()
                otp_user.otp = genOTP(start, otp_user.serial)
                otp_user.save()
                storage = messages.get_messages(request)
                storage.used = True
                return redirect("users:otp", int(user.id))
            else:
                messages.error(request, "No exits account with this username or this password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="Login/login.html", context={"login_form": form})


def otp_request(request, id):
    storage = messages.get_messages(request)
    storage.used = True
    otp_dt = OTP.objects.get(user_id=id)
    user = User.objects.get(id=id)
    date = user.date_joined
    start = date.timestamp()
    otp_gen = genOTP(start, otp_dt.serial)
    otp_dt.otp = otp_gen
    otp_dt.save()
    print(otp_gen)
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            if otp == genOTP(start, otp_dt.serial):
                otp_dt.otp = otp
                otp_dt.save()
                login(request, user)
                messages.info(request, "You login success !")
                storage = messages.get_messages(request)
                storage.used = True
                return redirect("users:homepage")
            else:
                messages.error(request, "Invalid OTP!")
        else:
            messages.error(request, "Invalid OTP!")
    form = OTPForm()
    return render(request=request, template_name="Login/totp.html", context={"otp_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    
    storage = messages.get_messages(request)
    storage.used = True
    return redirect("users:login")


class homepage(LoginRequiredMixin, TemplateView):
    template_name = 'Login/home.html'
