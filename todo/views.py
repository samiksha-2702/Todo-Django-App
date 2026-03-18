from django.shortcuts import redirect, render,  get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.
@login_required
def index(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')

        Task.objects.create(
            title=title,
            user=request.user,
            due_date=due_date if due_date else None,
            priority=priority
        )
        return redirect('index')

    query = request.GET.get('q')
    if query:
        tasks = Task.objects.filter(user=request.user, title__icontains=query)
    else:
        tasks = Task.objects.filter(user=request.user)

    # ✅ Stats
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()

    context = {
        'tasks': tasks,
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': pending_tasks,
        'today': timezone.now().date()
    }

    return render(request, 'todo/index.html', context)

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
    task = Task.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.due_date = request.POST.get('due_date')
        task.priority = request.POST.get('priority')
        task.save()
        return redirect('index')

    return render(request, 'todo/edit.html', {'task': task})
    

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


def logout_view(request):
    logout(request)
    return redirect('login')  # redirect to login page

