from django.shortcuts import redirect, render
from django.urls import reverse
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from store import models
from store.forms import CustomUserForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sign Up Successful! Log in to continue")
            return redirect('/login')
        else:
            messages.success(request, "Something went wrong")
    context = {'form':form}
    return render(request, "store/auth_templates/register.html", context)

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('home')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('pass')

            user = authenticate(request, username=name, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Log in Successful')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
    return render(request, "store/auth_templates/login.html")

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, "Log out successful")
    return redirect('home')

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			user = models.CustomUser.objects.filter(email=data).first()
			if user:
				subject = "Password Reset Requested"
				email_template_name = "password/password_reset_message.txt"
				c = {
                    "name": user.first_name,
				    "email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
				}
				email = render_to_string(email_template_name, c)
				requests.get(f"https://sms.arkesel.com/sms/api?action=send-sms&api_key=WlZGdW9CdUxaeWJsc2hld1BTaU0&to=0{user.phone_number}&from=Colgra&sms={email}")
				return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})
