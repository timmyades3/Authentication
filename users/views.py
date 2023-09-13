from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm
from django.contrib.auth.models import User


# Create your views here.
class Home(LoginRequiredMixin,View):
  login_url = '/login/'
  redirect_field_name = 'login'

  def get(self,request,*args,**kwargs):
    return render(request,'home.html')

class Register(View):
  def post(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('home')
    else:
      form = UserForm(request.POST)
      if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(request,f'Welcome {username}')
        return redirect('login')
      
    return render(request, 'register.html',{'form':form})
  
  def get(self,request,*args,**kwargs):
    if request.user.is_authenticated:
      return redirect('home')
    else:
      form = UserForm()  
    return render(request, 'register.html', {'form':form})

class Login(View):
  def post(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('home')
    else:
      username = request.POST.get('username')
      password = request.POST.get('password')

      user = authenticate(request,username = username,password = password)
      user_exist=User.objects.filter(username=username).exists()
      if user is not None:
        login(request, user)
        return redirect('home')
      elif user is None and user_exist == True: 
        error_message ='Incorrect password.' 
      elif user is None:
        error_message = 'User does not exist.'
      print(user_exist)
    return render(request, 'login.html',{'error_message':error_message})
  
  def get(self,request,*args,**kwargs):
    if request.user.is_authenticated:
      return redirect('home')
    return render(request, 'login.html')
  
class Logout(LoginRequiredMixin, View):
  login_url = '/login/'
  redirect_field_name = 'login'
  def get(self,request):
      logout(request)
      return render(request, 'logout.html')


    



  
  