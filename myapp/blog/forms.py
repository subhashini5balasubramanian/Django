from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Category, Post


class ContactForm(forms.Form):
    name=forms.CharField(label='Name', max_length='100',required=True)
    email=forms.EmailField(label='Email',required=True)
    message=forms.CharField(label='Message',required=True)
class RegisterForm(forms.ModelForm):
    username=forms.CharField(label='Username',max_length=100,required=True)
    email=forms.CharField(label='email',max_length=100,required=True)
    password=forms.CharField(label='password',max_length=100,required=True)
    password_confirm=forms.CharField(label='confirm_password',max_length=100,required=False)
    
    class Meta:
        model=User
        fields=['username','email','password']
    
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        password_confirm=cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Password do not Match")


class LoginForm(forms.Form):
    username=forms.CharField(label="username",max_length=100,required=True)
    password=forms.CharField(label="password",max_length=100,required=True)

    def clean(self):
        cleaned_data =super().clean()
        username=cleaned_data.get("username") 
        password=cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username,password=password)
            if user is None:
                raise forms.ValidationError("Invalid username and password")
            
class ForgotPasswordForm(forms.Form):
    email=forms.EmailField(label='email', max_length=254, required=True)

    def clean(self):
        cleaned_data=super().clean()
        email=cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user Registered with this email")
        
        return cleaned_data 
        
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='New Password', min_length=8)
    confirm_password = forms.CharField(label='Confirm Password', min_length=8)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class PostForm(forms.ModelForm):
    title=forms.CharField(label='Title', max_length=200, required=True)
    content=forms.CharField(label='content', required=True)
    category=forms.ModelChoiceField(label='Category',required=True,queryset=Category.objects.all())
    img_url=forms.ImageField(label='Image',required=False)
    class Meta:
        model=Post
        fields=['title','content','category','img_url']

    def clean(self):
        cleaned_data=super().clean()
        title=cleaned_data.get('title')
        content=cleaned_data.get('content')
        

        #Custom Validation
        if title and len(title)<5:
            raise forms.ValidationError('Title Must Be at 5 Charactes Long ')
        if content and len(content)<10:
            raise forms.ValidationError('Content Must Be at 5 Charactes Long ')
        return cleaned_data

    def save(self,commit=True):
        post=super().save(commit=False)
        cleaned_data=self.cleaned_data
        if cleaned_data.get('img_url'):
            post.img_url=cleaned_data.get('img_url')
        else:
            img_url='https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?20200913095930'
            post.img_url=img_url
        
        
        if commit:
            post.save()
        return post
        
        
        #return cleaned_data
