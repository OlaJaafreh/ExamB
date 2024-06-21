from django.shortcuts import render ,redirect
from .models import Users 
import bcrypt
from django.contrib import messages

def loginPage(request):
    return render(request,'login.html')


def login(request):
    email = request.POST['emailLog']
    password = request.POST['pass']
    user = Users.objects.filter(email=email)
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect("dashboard")
        else:
            messages.error(request, 'Incorrect User name or Password')
    else:
        messages.error(request, 'Incorrect User name or Password')
    return redirect('loginPage')


def register(request):
    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:
        messages.error(request, 'Registration failed.')
        return render(request,'login.html', {'errors': errors})
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        Users.objects.create(first_name=first_name,last_name=last_name,email=email,password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())
        messages.success(request, 'Registration successful. You can now log in.')
        return render(request ,"login.html")
    
