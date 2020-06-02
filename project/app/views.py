from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required  #here who hv loged in they can only contact
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Contact, Blogpost
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage


# Create your views here.

def index(request):
    return render(request, 'index.html')


def handleSignup(request):
    if request.method == 'POST':

        # TAKE THE PARAMETERS FROM THE POP UP FORM
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if len(username)>15:
            messages.error(request,"username should be less than 15 characters")
            return redirect('/')

            

        if not username.isalnum():
            return HttpResponse("usernames should contain only letters and numbers") 

        if pass1 != pass2:
            return HttpResponse("your password is incorrect")

           
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Successfully Signup")
        return redirect('/')
        

def handleLogin(request):

    if request.method == "POST":

        # GET PARAMETERS
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:

            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
           
            return redirect('/')




def contact(request):
    if request.method == "POST":
        name=request.POST.get('name')
        usn =request.POST.get('usn')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        #from_email=settings.EMAIL_HOST_USER
        if len(name)<2 or len(usn)<3 or len(phone)<10 or len(desc)<5:
            messages.error(request,"please fill the valid details")

        elif  name == name:
            messages.error(request, 'The user already exists..!')
        else:
            contact=Contact(name=name,usn=usn,phone=phone,desc=desc)
            contact.save()
            messages.success(request,"Your Message Has Been Recorded")    


    return render(request,'contact.html')
 
 
def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('/')
    

def about(request):
    return render(request,'about.html')


def blog(request):
    if not request.user.is_authenticated:
        messages.error(request,"Please Login & Try Again")
        return render(request,'index.html')
    else:
        allPosts= Blogpost.objects.all()
        context= {'allPosts':allPosts}  
        return render(request,'blog.html',context)


def search(request):

    query=request.GET['search']
    if len(query)>78:
        allPosts=Blogpost.objects.none()
    else:
        allPostsTitle=Blogpost.objects.filter(title__icontains=query)
        allPostsContent=Blogpost.objects.filter(content__icontains=query)
        allPosts=allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request,"No search Results")

    params={'allPosts':allPosts,'query':query}  
    return render(request, 'search.html',params)



