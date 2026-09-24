"""
Views for the `accounts` app: signup, login/logout, and profile viewing/editing.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, EditProfileForm, StyledPasswordChangeForm, StyledAuthenticationForm
from .models import UserProfile


def register(request):
    """Sign-up form; logs the new user in immediately on success."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}! Your account is ready.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = StyledAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('dashboard')
        messages.error(request, "Invalid username or password.")
    else:
        form = StyledAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile(request):
    from resume.models import Resume, Project, Skill, Certificate
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {
        'profile': profile_obj,
        'resumes': resumes,
        'resumes_count': resumes.count(),
        'projects_count': Project.objects.filter(resume__user=request.user).count(),
        'skills_count': Skill.objects.filter(resume__user=request.user).count(),
        'certificates_count': Certificate.objects.filter(resume__user=request.user).count(),
    })


@login_required
def edit_profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            # Update User model fields
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = EditProfileForm(instance=profile_obj, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    """Change the logged-in user's password (old password required)."""
    if request.method == 'POST':
        form = StyledPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Without this, changing the password invalidates the current
            # session and the user gets logged out immediately after saving.
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StyledPasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
