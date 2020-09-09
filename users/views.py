from django.shortcuts import render, redirect
from .models import RegisterForm
# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
 
            return redirect('web-login') 
        
    else:
        form = RegisterForm()

    return render(request,'users/register.html',{'form':form})
