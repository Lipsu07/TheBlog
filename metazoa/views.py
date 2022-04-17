from django.shortcuts import render,redirect
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from metazoa.models import BlogModel
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
# Create your views here.

def home(request):
    #return render(request ,'index.html')
    recent_blogs = BlogModel.objects.all().order_by("-updated_at")[:3]
    best_blogs = BlogModel.objects.all().exclude(id__in = recent_blogs.values('id')).order_by("?")[:2]
    context={
        "recent_blogs":recent_blogs,
        "best_blogs":best_blogs

    }
    return render(request,'index.html',context)
def Login(request):
    #return render(request , 'login.html')
    if request.user.is_authenticated:
        return redirect('authorblog')
    if request.method == 'POST':
       
        username = request.POST.get('username')
        password = request.POST.get('password')
       
        user = authenticate(username=username,password=password)
        print("user is",user)
        if user is not None:
            login(request,user)
            return redirect(reverse('authorblog'))
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request,'login.html')
def Signup(request):
    #return render(request , 'signup.html')
    #if request.user.is_authenticated:
        #return redirect(reverse('authorblog'))
    if request.method =='POST':
        username= request.POST['username']
       
        if request.POST['password1']==request.POST['password2']:

            password = request.POST['password1']
            myuser = User.objects.create_user(username=username)
            myuser.set_password(password)
            myuser.save()
            
            messages.success(request, 'User Created')
            return redirect('home')
        else:
            messages.error(request, 'Confirm Password not matched')
            return redirect('login')
    else:
        return redirect('login')




@login_required
def Logout(request):
    logout(request)
    return redirect(reverse('home'))

def Allblog(request):
    allblog = BlogModel.objects.all().order_by("-created_at")
    return render(request,'allblog.html',{"blogs":allblog})

def Blog(request,id):
    blog = BlogModel.objects.get(id = id)
    allblog = BlogModel.objects.all().exclude(id=id).order_by("?")[:5]
    return render(request,'blog.html',{"blogs":allblog,"blog":blog})


@login_required
def AddBlog(request):
    #return render(request ,'addblog.html')
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        image = request.FILES.get("image")
        if title and desc and image:
            blog = BlogModel(title = title,decs =  desc,image = image,author = request.user)
            blog.save()
            messages.success(request, 'Blog created')
            return redirect(reverse('addblog'))
        else:
            messages.error(request, 'Please Fill All the fileds')
            return redirect(reverse('addblog'))
    else:
        return render(request,"addblog.html")

@login_required
def AuthorBlog(request):
    if request.method == "POST":
        title = request.POST.get("title")
        blog_id = request.POST.get("blog_id")
        desc = request.POST.get("desc")
        image = request.FILES.get("image")
        if title and desc:
            blog = BlogModel.objects.get(id = blog_id)
            blog.title = title
            blog.decs = desc
            if image:
                blog.image = image
            blog.save()
            messages.success(request, 'Blog Updated')
            return redirect(reverse('authorblog'))
        else:
            messages.error(request, 'Please Fill All the fileds')
            return redirect(reverse('authorblog'))
    else:
        allblog = BlogModel.objects.filter(author = request.user.id).order_by("-updated_at")
        return render(request,'authorblogs.html',{"blogs":allblog})


@login_required
def DeleteBlog(request,id):
    blog = BlogModel.objects.filter(id = id,author = request.user.id)
    if blog.exists():
        blog.first().delete()
        messages.success(request, 'Blog Deleted')
        return redirect(reverse('authorblog'))
    else:
        messages.error(request, 'Can not find any blog')
        return redirect(reverse('authorblog'))
