from django.shortcuts import render, redirect
from .models import User
from datetime import datetime
from django.contrib import messages
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'login_registration/index.html')

def validate(request):
    if request.method == 'POST':
        error_flag = False
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        birthday = request.POST.get('birthday')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if len(first_name) < 3:
            messages.add_message(request, messages.ERROR,
            'First Name must be at least 3 letters long.')
            error_flag = True
        if not re.match(r'^[A-z]+$', first_name):
            messages.add_message(request, messages.ERROR,
            'First Name can only consist of letters.')
            error_flag = True
        if len(last_name) < 3:
            messages.add_message(request, messages.ERROR,
            'Last Name must be at least 3 letters long.')
            error_flag = True
        if not re.match(r'^[A-z]+$', last_name):
            messages.add_message(request, messages.ERROR,
            'Last Name can only consist of letters.')
            error_flag = True
        if len(email) < 1:
            messages.add_message(request, messages.ERROR,
            'Email cannot be blank.')
            error_flag = True
        elif not re.match(EMAIL_REGEX, email):
            messages.add_message(request, messages.ERROR,
            'Email must be in the correct format.')
            error_flag = True
        if len(password) < 8:
            messages.add_message(request, messages.ERROR,
            'Password must be at least 8 characters.')
            error_flag = True
        if not password == password_confirm:
            messages.add_message(request, messages.ERROR,
            'Passwords must match.')
            error_flag = True
        if error_flag == True:
            return redirect('login_reg:index')
        else:
            user = User.objects.register_user(request.POST) # UserManager method
            request.session['id'] = user.id
            return redirect('travel_buddy:index')
    else:
        return redirect('login_reg:index')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email') # validate email before query
        if not re.match(EMAIL_REGEX, email):
            messages.add_message(request, messages.ERROR,
            'Email must be in the correct format.')
            return redirect('login_reg:index')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email) # query database for email
        except:
            messages.add_message(request, messages.ERROR,
            'User does not exist.')
            return redirect('login_reg:index')
        hashed = user.password # if email exists in database go to success page
        if bcrypt.hashpw(str(password), str(hashed)) == hashed:
            request.session['id'] = user.id
            return redirect('travel_buddy:index')
        else:
            messages.add_message(request, messages.ERROR,
            'Password is incorrect.')
            return redirect('login_reg:index')
    else:
        request.session['id'] = user.id
        return redirect('travel_buddy:index')

def logout(request):
    request.session.pop('id')
    return render(request, 'login_registration/index.html')
