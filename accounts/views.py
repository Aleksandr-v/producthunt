from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):
    if request.method == 'POST':
        #Check matches password and confirm_password
        if request.POST['password'] == request.POST['confirm_password']:
            #Check if exists user with this username
            try:
                user = User.objects.get(username = request.POST['username'])
                return render(request, 'accounts/signup.html', {'error':'This username has already been taken'})
            except User.DoesNotExist:
                # if user not exists greate new user and save in db
                user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                auth.login(request, user)
                return redirect('home')
        else:
            #Both passwords did not matches
            return render(request, 'accounts/signup.html', {'error':'Passwords must match. Try again'})
    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print(request.POST)
            if request.POST['next_page'] is not '':
                return redirect(request.POST['next_page'])
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'accounts/login.html', {'error':'Incorrect username or password'})
    else:
        next = request.GET.get('next', '')
        return render(request, 'accounts/login.html', {'next':next})

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    else:
        return redirect('home')
