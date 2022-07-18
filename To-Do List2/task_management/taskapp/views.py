from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from taskapp.models import Task

# Create your views here.
def home(request):
    return render(request,'home.html')

def admin_signup(request):
    if request.method=="POST":
        fm=UserCreationForm(request.POST)
        print(fm)
        if fm.is_valid():
            uname=fm.cleaned_data['username']
            upass=fm.cleaned_data['password1']
            #print(uname)
            #print(upass)
            u=User.objects.create_user(username=uname,password=upass,is_superuser=True,is_staff=True)
            u.save()
            return HttpResponseRedirect('/user_login')
            
    else:
        fm=UserCreationForm()
    return render(request,'admin_signup.html',{'form':fm})

def signup(request):
    if request.method=="POST":
        fm=UserCreationForm(request.POST)
        #print(fm)
        if fm.is_valid():
            uname=fm.cleaned_data['username']
            upass=fm.cleaned_data['password1']
            #print(uname)
            #print(upass)
            u=User.objects.create_user(username=uname,password=upass,is_staff=True)
            u.save()
            return HttpResponseRedirect('/user_login')
            
    else:
        fm=UserCreationForm()
    return render(request,'signup.html',{'form':fm})
    

def user_login(request):
    if request.method=="POST":
        fm=AuthenticationForm(request=request,data=request.POST)
        #print(fm)
        if fm.is_valid():
            uname=fm.cleaned_data['username']
            upass=fm.cleaned_data['password']
            #print(uname)
            #print(upass)
            u=authenticate(username=uname,password=upass)
            if u is not None:
                #print("valid user")
                login(request,u)
                return HttpResponseRedirect('/dashboard')
    else:
        fm=AuthenticationForm()

    return render(request,'user_login.html',{'form':fm})

def user_logout(request):
     logout(request)
     return HttpResponseRedirect('/')

def dashboard(request):

    #collecting authenticated user id from the session
    c=request.user
    cuid=c.id
    #print(cuid)
    u=User.objects.get(id=cuid)
    #print(u.is_superuser)
    b=Task.objects.all()
    content={}
    content['data']=b
    content['is_superuser']=u.is_superuser
    return render(request,'dashboard.html',content)   

def add_task(request): 
    if request.method=="POST":
        tname=request.POST['tname']
        tdesc=request.POST['tdesc']
        
        t=Task.objects.create(task_name=tname,task_description=tdesc)
        t.save()
        return HttpResponseRedirect('/dashboard')

    else:
        return render(request,'add_task.html')

def delete_task(request,rid):
    b=Task.objects.filter(id=rid)
    b.delete()
    return HttpResponseRedirect('/dashboard/')

def edit_task(request,rid):
    if request.method=="POST":
        #print(rid)
        tuname=request.POST['tuname']
        tudesc=request.POST['tudesc']
        tu=Task.objects.filter(id=rid)
        tu.update(task_name=tuname,task_description=tudesc)
        return HttpResponseRedirect('/dashboard/')

    else:
        b=Task.objects.filter(id=rid) 
        content={}
        content['data']=b
        return render(request, 'edit_task.html',content)
         