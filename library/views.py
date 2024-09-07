from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

# Create your views here.

def home_page(request):
    context={'page':'BIT'}
    return render(request, 'homee/index.html', context)

@login_required(login_url="/login/")
def books(request):
    return render(request, 'homee/BookSec.html')

def login_page(request):
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not User.objects.filter(email = email).exists():
                messages.info(request, "Invalid email..!")
                return redirect('/login/')
            
            user = authenticate(email = email, password = password)

            if user is None:
                messages.info(request, "Invalid passward..!")
                return redirect('/login/')
            else:
                login(request, user)
                return redirect('/home_page/')

        return render(request, 'homee/login_page.html')

# def logout_page(request):
#     logout(request)
#     return redirect('homee/login_page/') 


# def register(request):

#     if request.method == "POST":
#         full_name = request.POST.get('full_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')

#         if password and confirm_password and password != confirm_password:
#             messages.error(request, "Passwords do not match.")
#             return redirect('/register/')
        
#         try:
#             validate_password(password)
#         except ValidationError as e:
#             messages.error(request, "Password does not meet the requirements: " + "; ".join(e.messages))
#             return redirect('/register/')

#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email is already in use.")
#             return redirect('/register/')

#         user = User.objects.create_user(
#             full_name=full_name,
#             username=username,
#             email=email,
#             password=password
#         )

#         messages.success(request, "Account created successfully!")
#         return redirect('/login_page/')

#     return render(request, 'homee/register.html')

def register(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if any fields are empty
        if not all([full_name, username, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect('/register/')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect('/register/')

        # Validate password and confirm password
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/register/')

        # Validate the password strength
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, "Use a stronger password.")
            return redirect('/register/')
        
        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "Username is not available..!")
            return redirect('/register/')

        # Create user
        user = User.objects.create_user(
            full_name=full_name,
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully!")
        return redirect('/login_page/')

    return render(request, 'homee/register.html')
