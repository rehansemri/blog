from django.core.paginator import Paginator

from .models import Profile,Post,Comment,Message
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def home(request):
    contact_list = Post.objects.all()
    paginator = Paginator(contact_list, 4)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        'posts':posts

    }
    return render(request,'index.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user =User.objects.get(username=username)
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('home')
            else :
                messages.error(request, 'Password is incorrect')
        except:
            messages.info(request,'User not Found')

        return redirect('home')
    return render(request,'login.html',)


def register(request):
    if request.method == 'POST':
        first_name =  request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password==password1 :
            if User.objects.filter(username=username).exists():
                messages.info(request,"User Name Already Exist")
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Taken')
            else :
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                user.save()
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                user_model = User.objects.get(username=username)
                name = first_name + ' ' + last_name
                email=email
                new_profile = Profile.objects.create(user=user_model,name=name,email=email)
                new_profile.save()
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username,password=password)
                auth.login(request,user)
                return redirect('home')

        else : 
            messages.info(request,"Password not Match")
        
    return render(request,'register.html')
def logout(request):
    auth.logout(request)
    return redirect('home')

def upload_post(request):
    user_info = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        desc = request.POST['desc']
        post_img = request.FILES.get('post_img')
        user = user_info
        new_post = Post.objects.create(user=user,desc=desc,post_img=post_img)
        new_post.save()
        return redirect('home')
    return redirect('home')

def comment(request,pk):
    user_info = Profile.objects.get(user=request.user)
    post_info = Post.objects.get(id=pk)
    if request.method == 'POST':
        txt = request.POST['txt']
        current_path =request.POST['current_path']
        user = user_info
        post_commnet = post_info
        new_comment = Comment.objects.create(txt=txt,user=user,post_commnet=post_commnet)
        new_comment.save()
        return redirect(current_path)
    return redirect(current_path)

def post(request,pk):
    post = Post.objects.get(id=pk)
    context ={'post':post}
    return render(request,'post.html',context)
def add_post(request):
    user_info = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        desc = request.POST['desc']
        title = request.POST['title']
        post_img = request.FILES.get('post_img')
        user = user_info
        new_post = Post.objects.create(user=user.user,desc=desc,post_img=post_img,title=title)
        new_post.save()
        return redirect('home')
    return render(request,'Add_post.html')
def profile(request,pk):
    user_profile = Profile.objects.get(id=pk)
    contact_list = Post.objects.filter(user=user_profile.user)
    paginator = Paginator(contact_list, 4)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'user_profile':user_profile,
        'posts':posts
    }
    return render(request,'profile.html',context)
def delete_post(request,pk):
    Post.objects.get(id=pk).delete()
    current_path =request.POST['current_path']
    return redirect(current_path)
