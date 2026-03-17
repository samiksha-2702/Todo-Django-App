from django.shortcuts import redirect, render
from .models import Task
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    # ✅ Show only logged-in user's tasks
    task = Task.objects.filter(user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        # ✅ Save task with logged-in user
        Task.objects.create(title=title, user=request.user)
        
        return redirect('index')
    
    return render(request, 'todo/index.html', {'task': task})

@login_required
def complete_task(request, id):
    task = Task.objects.get(id=id)
    task.completed = not task.completed   # Toggle
    task.save()
    return redirect('index')

@login_required
def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('index')

@login_required
def edit_task(request, id):
    task = Task.objects.get(id=id)

    if request.method == 'POST':
        title = request.POST.get('title')
        task.title = title
        task.save()
        return redirect('index')
    
    return render(request, 'todo/edit.html', {'task': task})
    

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'registration/signup.html')
        
        # create user
        User.objects.create_user(username=username, password=password)

        messages.success(request, "Account created successfully!")
        return redirect('login')

    
    return render(request, 'registration/signup.html')