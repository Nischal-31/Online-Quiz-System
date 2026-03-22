from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.forms import CustomUserCreationForm


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('quiz_list')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid credentials'})

    return render(request, 'user/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    form = CustomUserCreationForm(request.POST or None)  # ← use custom form

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz_list')

    return render(request, 'user/register.html', {'form': form})