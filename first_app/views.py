from django.shortcuts import render,redirect,HttpResponse
import bcrypt
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render (request,"registration_login.html")

def create_user(request):
    if(request.method=='POST'):
        errors=User.objects.create_validator(request.POST)
        if len(errors)>=1:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/') 
        else: 
            password = request.POST['password'] 
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            confirm_password = request.POST['confirm_password'] 
            confirm_pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            dk=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=pw_hash,confirm_password=confirm_pw_hash,birthday=request.POST['birthday'])
            request.session['user_id']=dk.id
            return redirect('/welcome')

def login(request):
    if(request.method=="POST"):
        user = User.objects.filter(email=request.POST['email'])
        if len(user)!=0:
            logged_user=user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/welcome')
        messages.error(request, "email and password don't match")
    return redirect('/')

def welcome(request):
    if('user_id' not in request.session):
        return redirect('/')
    context={
        'user':User.objects.get(id=request.session['user_id'])
    }
    return render(request,"welcome.html",context)

def logout(request):
    request.session.flush()
    return redirect('/')