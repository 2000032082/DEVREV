from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Flight, Booking
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm

def loginpage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')#if the user is already logged in ...then wont be allowed to the login page
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "User doesnt exist")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password doesnt exist')
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')
def registerPage(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False) #In Django, the form.save() method is used to save the data submitted through a form to the database. When commit=False is passed as an argument to form.save(), it tells Django not to save the object to the database immediately, but to return an unsaved instance of the object instead.
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'an error occurred during registrartion')
    return render(request,'base/login_register.html',{'form':form})
@login_required
def add_flight(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        flight = Flight.objects.create(name=name, description=description, host=request.user)
        flight.save()
        return redirect('flight_list') 
    return render(request, 'add_flight.html')

@staff_member_required
def remove_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    flight.delete()
    return redirect('flight_list') 

@login_required
def view_bookings(request, flight_id, flight_time):
    bookings = Booking.objects.filter(flight_id=flight_id, time=flight_time)
    return render(request, 'view_bookings.html', {'bookings': bookings})
