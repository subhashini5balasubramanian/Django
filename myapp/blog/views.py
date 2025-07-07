from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from .models import Category, Post,AboutUs
from django.http import Http404
from django.core.paginator import Paginator
from .forms import ContactForm, ForgotPasswordForm, LoginForm, PostForm,RegisterForm, ResetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.tokens  import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group






'''
statis data
posts=[
        {'id':1,'title': 'post 1','content':'content of Post 1'},
        {'id':2,'title': 'post 2','content':'content of Post 2'},
        {'id':3,'title': 'post 3','content':'content of Post 3'},
        {'id':4,'title': 'post 4','content':'content of Post 4'}
    ]
'''
# Create your views here.
def welcome(request):
    return render(request, 'blog/welcome.html')

def index(request):
    blog_title="Latest Posts"
    all_posts=Post.objects.filter(is_published=True)

    paginator=Paginator(all_posts,5)
    page_number=request.GET.get('page')
    page_object=paginator.get_page(page_number)
    return render(request,"blog/index.html",{'blog_title': blog_title, 'page_obj':page_object})

def detail(request,slug):
    if not request.user.has_perm('blog.view_post'):
        messages.error(request,"You Have No Permission to view any post")
        return redirect("blog:index")
    # Getting static data
    # post=next((item for item in posts if item['id'] == int(post_id)),None)
   # logger=logging.getLogger("TESTING")
   # logger.debug(f'Post Variable is {post}')

    try:
   # getting data from model by post id 
        post=Post.objects.get(slug=slug)
        related_post=Post.objects.filter(category=post.category).exclude(pk=post.id)
    except Post.DoesNotExist:
        raise Http404("Post Doesnot Exists")


    return render(request,"blog/details.html",{'post':post,'related_post':related_post})

def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))

def new_url_view(request):
    return HttpResponse("This is The New url")

def contact(request):
    if request.method == 'POST':
        form=ContactForm(request.POST)
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        logger=logging.getLogger("TESTING")
        if form.is_valid():
            logger.debug(f'Post DATA is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            success_message= 'Your Email Has Been Sent!!'
            return render(request,"blog/contact.html",{'form':form,'success_message':success_message})
        else:
            logger.debug('Form validation failure')
        return render(request,"blog/contact.html",{'form':form,'name':name,'email':email,'message':message})
    return render(request,"blog/contact.html")
def about(request):
    about_content=AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content="Default content goes here."
    else:
        about_content=about_content.content
      
    return render(request,"blog/about.html",{'about_content':about_content})
def register(request):
    form=RegisterForm()
    if request.method =='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False) #user data
            user.set_password(form.cleaned_data['password'])
            user.save()
            #add user to readers group
            readers_group,created=Group.objects.get_or_create(name="Readers")
            user.groups.add(readers_group)
            # print("Registeration Successfull!!")
            messages.success(request,"Registration Successfull.You Can Login")
            return redirect("blog:login") 
       
    return render(request,'blog/register.html',{'form':form})


def login(request):
    form=LoginForm()
    if request.method=='POST':
        #login form
        form =LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                auth_login(request,user)
                return redirect("blog:dashboard")  #redirect to dashboard

            print("LOGIN SUCCESS")
        
    return render(request, 'blog/login.html',{'form':form})

def dashboard(request):
    blog_title="My posts"
    #getting user posts
    all_posts=Post.objects.filter(user=request.user)
    #pagination
    paginator=Paginator(all_posts,5)
    page_number=request.GET.get('page')
    page_object=paginator.get_page(page_number)

    return render(request,'blog/dashboard.html',{"blog_title":blog_title,"page_obj":page_object})

def logout(request):
    auth_logout(request)
    return redirect('blog:index')

def forgot_password(request):
    form=ForgotPasswordForm()

    if request.method=='POST':
        form=ForgotPasswordForm(request.POST)

        if form.is_valid():
            email =form.cleaned_data['email']

            user = User.objects.get(email=email)
            # send the rest email
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            current_site=get_current_site(request)
            domain=current_site.domain

            subject="Reset Password Requested"
            message=render_to_string("blog/reset_password_email.html",{'domain':domain,'uid':uid,'token':token})

            send_mail(subject,message,'subhashini.saveetha@gmail.com',[email])
            messages.success(request,"Email Has Been Sent")


    return render(request,'blog/forgot_password.html',{'form':form})

def reset_password(request,uidb64,token):
    form=ResetPasswordForm()
    if request.method == 'POST':
        form=ResetPasswordForm(request.POST)
        if form.is_vaild():
            new_password = form.cleaned_data['new_password']
            try:
                uid=urlsafe_base64_decode(uidb64)
                user=User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user=None

            if user is not None and default_token_generator.check_token(user,token):
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password Reset Successfully')
                return redirect('blog:login')
            else:
                messages.error(request,'password reset link is expired')
    
    return render(request,'blog/reset_password.html')

@login_required
@permission_required("blog.add_post",raise_exception=True)
def new_post(request):
    categories=Category.objects.all()
    form=PostForm()
    if request.method == 'POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('blog:dashboard')
    return render(request,'blog/new_post.html',{'categories':categories,'form':form})


@login_required
def edit_post(request,post_id):
    categories=Category.objects.all()
    post=get_object_or_404(Post,id=post_id)
    form=PostForm()

    if request.method == 'POST':
        # FORM 
        form=PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,"Post Successfully Updated")
            return redirect('blog:dashboard')

    return render(request,'blog/edit_post.html',{'categories':categories,'post':post,'form':form})

@login_required
@permission_required("blog.delete_post",raise_exception=True)
def delete_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    post.delete()
    messages.success(request,'Post Successfully Deleted!')
    return redirect('blog:dashboard')

@login_required
@permission_required("blog.can_publish",raise_exception=True)
def publish_post(request,post_id):
    post= get_object_or_404(Post, id=post_id)
    post.is_published=True
    post.save()
    messages.success(request,'Post Published Successfully!')
    return redirect('blog:dashboard')