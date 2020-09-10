from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User

def index(request):
    return render(request, 'register/home.html')

def register(request):
    if request.method=="POST":
        errors = User.objects.validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        first_name=request.POST['first_name']
        last_name=request.POST['last_name'] 
        password=request.POST['password']
        email=request.POST['email']
        phone_number=request.POST['phone_number']
        user_type=request.POST['user_type']
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=first_name,last_name=last_name,password=hashed_password,email=email,phone_number=phone_number,user_type=user_type)
        user.save()
        request.session['id'] = user.id
        messages.success(request, 'registered successfully')
        return redirect('/login')
    return render(request, 'register/register.html')

def login(request):
    if request.method=="POST":
        if (User.objects.filter(email=request.POST['login_email']).exists()):
            email=request.POST['login_email']
            passwd = request.POST['login_password']
            hashed_password = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())
            user = User.objects.filter(email=email).first()
            userd = User.objects.filter(email=email,password=hashed_password).first()
            if user is not None:
                request.session['id'] = user.id
                messages.success(request, 'logged in successfully')
                return redirect('/success')
            else:
                print("user uyu doesn't exists")
                messages.warning(request, 'wrong credentials')
                return redirect('/login')
        else:
            messages.warning(request, 'please register first lo login')
            return redirect('/register')      
    return render(request, 'register/login.html')

def success(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        "user": user
    }
    return render(request, 'register/success.html', context)