from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from properties.models import Property


def login_view(request):
    if request.user.is_authenticated:
        return redirect('properties:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'أهلاً {user.username}!')
            return redirect(request.GET.get('next', 'properties:home'))
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غلط')

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('properties:home')

    if request.method == 'POST':
        username  = request.POST.get('username')
        email     = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'كلمتا المرور غير متطابقتين')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'اسم المستخدم موجود بالفعل')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'البريد الإلكتروني مستخدم بالفعل')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            login(request, user)
            messages.success(request, f'أهلاً {username}! تم إنشاء حسابك بنجاح')
            return redirect('properties:home')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    return redirect('properties:home')


@login_required
def profile_view(request):
    my_properties = Property.objects.filter(owner=request.user).order_by('-created_at')
    context = {'my_properties': my_properties}
    return render(request, 'accounts/profile.html', context)