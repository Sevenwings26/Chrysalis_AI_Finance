from django.shortcuts import render, redirect
from django.contrib.auth import (
    login, 
    logout, 
    authenticate
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegistrationForm, 
    UserLoginForm, 
    CustomPasswordResetForm, 
    CustomSetPasswordForm
)
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from learn.models import Video

# landing page 
def index(requests):
    all_videos = Video.objects.select_related('category').all()
    context = {
        'all_videos': all_videos,
    }
    return render(requests, 'index.html', context)

# def about(requests):
#     return render(requests, 'about.html')

# ============== REGISTER ==============
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.email}")
            return redirect('login')
        else:
            # If form is invalid, the 'form' object now contains error messages
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/auth.html', {
        'register_form': form, 
        'show_signup': True
    })


# ============== LOGIN ==============
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        print(request.POST) 
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user is not None:
                login(request, user)
                messages.success(
                    request,
                    f"Welcome back, {user.first_name}!"
                )
                return redirect('/')
        messages.error(request, "Invalid email or password")
    else:
        form = UserLoginForm()
    return render(
        request,
        'auth/auth.html',
        {
            'login_form': form,
            'show_login': True
        }
    )


# ============== LOGOUT ==============
@login_required
def logout_view(request):
    """User Logout"""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


# ====================== PASSWORD RESET VIEWS ======================
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'auth/password_reset.html'
    email_template_name = 'auth/password_reset_email.html'
    subject_template_name = 'auth/password_reset_subject.txt'
    success_url = '/login/password-reset/done/'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'auth/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'auth/password_reset_confirm.html'
    success_url = '/login/password-reset/complete/'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'auth/password_reset_complete.html'

