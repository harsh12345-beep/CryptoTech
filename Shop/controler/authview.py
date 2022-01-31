from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages

from typing import List
from importlib.resources import contents

def register(request):
    if request.method=="POST":
        
        last_name = request.POST.get('last_name')
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        user  = User.objects.create_user(username= user_name, password=user_password , email= email,last_name=last_name)
       
        mnemonic: List[str] = node.wallet.create(name='harygbbbk', password='ncosdnoidncolsnd', passphrase='')
        user.save()
        messages.success(request,"Registered Successfully")
        print(user_name,user_password)
 
        return redirect("login")
    return render(request,"Shop/ACCOUNT/register.html")


def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already loggedin')
        return redirect("Index")
    else:
        if request.method == "POST":
            name = request.POST.get('name')
            pwd = request.POST.get('pas')
            
            user = authenticate(request, username=name,password=pwd)
            
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect("Index")
            else:
                messages.error(request,"Invlaid username or password")
                return redirect("login")
            
        return render(request,"SHop/ACCOUNT/login.html") 
    

def logoutpage(request):
    if request.user.is_authenticated:
        
        logout(request)
        messages.success(request,"Logged out successfully")
    return redirect("Index")

