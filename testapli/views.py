from cgi import test
from django.shortcuts import render, redirect
from .models import student 

def home(request):
    
    std = student.objects.all()
    
    
    return render(request, 'appli\home.html', context={'std':std})

def std_add(request):
    
    if request.method=='POST':
        stds_roll = request.POST.get("std_roll")
        stds_name = request.POST.get("std_name")
        stds_email = request.POST.get("std_email")
        stds_address = request.POST.get("std_address")
        stds_phone = request.POST.get("std_phone")
        
        s=student()
        s.roll=stds_roll
        s.name=stds_name
        s.email=stds_email
        s.address=stds_address
        s.phone=stds_phone
        
        s.save()
        return redirect("/test/home")
    
    return render(request, 'appli/add_std.html')

def delete_std(request, roll):
    s=student.objects.get(pk=roll)
    s.delete()
    return redirect('/test/home')

def update_std(request, roll):
    std=student.objects.get(pk=roll)
    return render(request, 'appli/update_std.html', context={'std':std})

def do_update_std(request, roll):
    std_roll = request.POST.get("std_roll")
    std_name = request.POST.get("std_name")
    std_email = request.POST.get("std_email")
    std_address = request.POST.get("std_address")
    std_phone = request.POST.get("std_phone")
    
    
    std=student.objects.get(pk=roll)
    
    std.roll=std_roll
    std.name=std_name
    std.email=std_email
    std.address=std_address
    std.phone=std_phone
    
    std.save()
    return redirect('/test/home')
    
    