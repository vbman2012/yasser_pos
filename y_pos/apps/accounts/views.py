from django.http import request
from django.shortcuts import render , redirect
from .models import Profile
from .forms import UserForm , ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


@login_required
def home(request):
    user = request.user
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'dash_board.html' , {'profile':profile})
    else:
        return render(request, 'registration/login.html')


@login_required
def acc_dashboard(request):
    user = request.user
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'dash_board.html' , {'profile':profile})
    else:
        return render(request, 'registration/login.html')


@login_required
def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile/profile.html', {'profile':profile})


@login_required
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        userform = UserForm(request.POST , instance=request.user)
        profile_form = ProfileForm(request.POST , instance=profile)
        if userform.is_valid() and profile_form.is_valid():
            userform.save()
            myform = profile_form.save(commit=False)
            myform.user = request.user
            myform.save()
            return redirect('/accounts/profile')

    else:  ## show
        userform = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profile/profile_edit.html', {
        'userform': userform ,
        'profileform': profile_form ,
        })
