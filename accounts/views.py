# accounts/views.py
from audioop import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.messages import error

from .forms import CustomUserCreationForm

from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test



def register_view(request):
    if request.user.is_authenticated:

        return redirect('user_home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True  # Set user as active directly
            user.save()

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('user_login')
        else:
            messages.error(request, 'Registration failed. Please check the form for errors.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if not request.user.is_authenticated:
        error = None  # Initialize the error variable
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_staff:
                    error ="ad"
                    # Redirect admin users or show an message admin portal.
                else:
                    login(request, user)
                    error = "no"  # Indicate successful login
                      # Redirect to user home page if needed
            else:
                error = "yes"  # Indicate login error login cadinate

        context = {'error': error}
        return render(request, 'accounts/user_login.html', context)
    else:
        if request.user.is_staff:
            return redirect('home')
        else:
            return redirect('user_home')


def logout_view(request):
        logout(request)
        return redirect('user_login')



@login_required
def user_home(request):
    if not request.user.is_staff:
        return render(request, 'accounts/user_home.html')
    else:
        return redirect('home')

@login_required
def strength_training(request):
    if not request.user.is_staff:
        return render(request, 'accounts/strength_training.html')
    else:
        return redirect('home')
@login_required
def cardio_blast(request):
    if not request.user.is_staff:
        return render(request, 'cardio_blast.html')
    else:
        return redirect('home')

@login_required
def flexibility_mobility(request):
    if not request.user.is_staff:
        return render(request, 'flexibility_mobility.html')
    else:
        return redirect('home')


