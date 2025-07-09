from django.shortcuts import render

# Create your views here.
def register_page(request):
    return render(request,'register.html')

def admin_project(request):
    return render(request,'admin_project_page.html')

def user_profile(request):
    return render(request,'user_profile.html')

def landing(request):
    return render(request,'landing_page.html')
def home(request):
    return render(request,'home.html')
def role(request):
    return render(request,'role.html')
def admin_access(request):
    return render(request,'admin_access.html')

from django.utils import timezone
from django.shortcuts import render
from .models import Project, Task, User  # Replace `User` if you're using a custom model

def admin_dash(request):
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    today = timezone.now().date()
    tasks_due_today = Task.objects.filter(deadline=today).count()

    projects = Project.objects.order_by('-id')[:2]  # Show only latest 2
    tasks = Task.objects.order_by('-id')[:2]        # Show only latest 2
    users = User.objects.order_by('-id')[:2]        # Show only latest 2 users

    context = {
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'tasks_due_today': tasks_due_today,
        'projects': projects,
        'tasks': tasks,
        'users': users,
    }

    return render(request, 'admin_dashboard.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdminUser,User

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        secret_code = request.POST.get('secret_code')

        try:
            # Check if matching user exists
            user = AdminUser.objects.get(username=username, password=password, secret_code=secret_code)
            
            return redirect('admin_dashboard')  # Make sure this name exists in your URLconf
        except AdminUser.DoesNotExist:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'admin_login.html')  # Your template name here


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User  # Use your actual User model

def admin_user_manage(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')
        name = request.POST.get('fullName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('roleSelect')

        if user_id:
            user = User.objects.get(id=user_id)
            user.full_name = name
            user.email = email
            user.role = role
            if password:
                user.password = password
            user.save()
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'User already exists.')
            else:
                User.objects.create(
                    full_name=name,
                    email=email,
                    password=password,
                    role=role
                )

        return redirect('admin_user_manage_page')

    users = User.objects.all()
    return render(request, 'admin_user_management_page.html', {'users': users})

def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('admin_user_manage_page')


def user_login(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email_or_username')
        password = request.POST.get('password')

        if not email_or_username or not password:
            messages.error(request, "Please fill in all fields.")
            return redirect('user_login')

        try:
            if '@' in email_or_username:
                # Login using email
                user = User.objects.get(email=email_or_username, password=password)
            else:
                # Login using full name
                user = User.objects.get(full_name=email_or_username, password=password)

            # Save session
            request.session['user_id'] = user.id
            request.session['user_role'] = user.role

            # if user.role == 'Admin':
            #     return redirect('admin_dashboard')
            if user.role.lower() == 'team member':
                return redirect('user_dashboard')
            else:
                messages.error(request, "Invalid role.")
                return redirect('user_login')

        except User.DoesNotExist:
            messages.error(request, "Invalid login credentials.")
            return redirect('user_login')

    return render(request, 'user_login.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import User, Task, Project, Notification

def user_dash(request):
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id:
        messages.error(request, "Please log in first.")
        return redirect('user_login')

    if user_role.lower() != 'team member':
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('user_login')

    # Get total number of projects the user is involved in
    total_projects = Project.objects.filter(task__assigned_to=user).distinct().count()

    # Get all tasks assigned to the user
    user_tasks = Task.objects.filter(assigned_to=user)

    # Count total tasks
    total_tasks = user_tasks.count()

    # Tasks due today
    today = timezone.now().date()
    tasks_due_today = user_tasks.filter(deadline=today).count()

    # Unread notifications
    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()

    # Latest 5 notifications (FIXED: use 'timestamp' instead of 'created_at')
    recent_notifications = Notification.objects.filter(user=user).order_by('-timestamp')[:5]

    # Latest 2 assigned tasks
    recent_tasks = user_tasks.order_by('-deadline')[:2]

    context = {
        'user': user,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'tasks_due_today': tasks_due_today,
        'unread_notifications': unread_notifications,
        'recent_tasks': recent_tasks,
        'recent_notifications': recent_notifications,
    }

    return render(request, 'user_dashboard.html', context)

         
from .models import Project, User, Task, Notification  # add Notification
from django.utils import timezone

def admin_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        assigned_to_id = request.POST.get('assigned_to')
        project_id = request.POST.get('project')

        assigned_to = User.objects.get(id=assigned_to_id)
        project = Project.objects.get(id=project_id)

        task = Task.objects.create(
            title=title,
            description=description,
            deadline=deadline,
            priority=priority,
            status=status,
            assigned_to=assigned_to,
            project=project
        )

        # ✅ Create assignment notification
        Notification.objects.create(
            user=assigned_to,
            message=f'Task "{title}" assigned to you.',
            type='assignment'
        )

        return redirect('admin_task_page')

    users = User.objects.filter(role='Team Member')
    projects = Project.objects.all()
    tasks = Task.objects.select_related('assigned_to', 'project')
    return render(request, 'admin_task_page.html', {
        'users': users,
        'projects': projects,
        'tasks': tasks
    })



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Task

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request, "Task deleted successfully.")
    return redirect('admin_task_page')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.deadline = request.POST.get('deadline')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')
        assigned_to_id = request.POST.get('assigned_to')
        project_id = request.POST.get('project')

        task.assigned_to = User.objects.get(id=assigned_to_id)
        task.project = Project.objects.get(id=project_id)

        task.save()

        messages.success(request, "Task updated successfully.")
        return redirect('admin_task_page')

    users = User.objects.filter(role='Team Member')
    projects = Project.objects.all()

    return render(request, 'edit_task_page.html', {
        'task': task,
        'users': users,
        'projects': projects
    })




from django.shortcuts import render, redirect
from .models import Project, User
from django.contrib import messages

def admin_project(request):
    if request.method == 'POST':
        name = request.POST.get('projectTitle')
        description = request.POST.get('projectDescription')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        member_ids = request.POST.getlist('teamMembers')  # List of user IDs (must match option values)

        if not (name and description and start_date and end_date and member_ids):
            messages.error(request, "All fields are required.")
            return redirect('admin_project_page')

        project = Project.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )
        project.team_members.set(member_ids)
        messages.success(request, "Project added successfully.")
        return redirect('admin_project_page')

    users = User.objects.filter(role='Team Member')
    projects = Project.objects.all()

    return render(request, 'admin_project_page.html', {
        'users': users,
        'projects': projects
    })

from django.shortcuts import get_object_or_404
# DELETE Project
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, "Project deleted successfully.")
    return redirect('admin_project_page')

def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        name = request.POST.get('projectTitle')
        description = request.POST.get('projectDescription')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        member_ids = request.POST.getlist('teamMembers')

        if name:
            project.name = name
        if description:
            project.description = description
        if start_date:
            project.start_date = start_date
        if end_date:
            project.end_date = end_date
        if member_ids:
            project.team_members.set(member_ids)

        project.save()
        messages.success(request, "Project updated successfully.")
        return redirect('admin_project_page')

    return redirect('admin_project_page')



from django.shortcuts import render, redirect
from .models import Task, Project, User
from django.contrib.auth.decorators import login_required
from django.db.models import Count

def user_tasks(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to view tasks.")
        return redirect('user_login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('user_login')

    selected_project = request.GET.get('project')
    selected_priority = request.GET.get('priority')

    tasks = Task.objects.filter(assigned_to=user)

    if selected_project and selected_project.isdigit():
        tasks = tasks.filter(project__id=int(selected_project))

    if selected_priority:
        tasks = tasks.filter(priority__iexact=selected_priority)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks else 0

    context = {
        'tasks': tasks,
        'projects': Project.objects.all(),
        'progress': progress,
        'completed_tasks': completed_tasks,
        'total_tasks': total_tasks,
        'selected_project': selected_project,
        'selected_priority': selected_priority,
        'user': user, 
    }
    return render(request, 'user_task_page.html', context)


def update_task_status(request, task_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "You must be logged in.")
            return redirect('user_login')

        new_status = request.POST.get('status')
        try:
            user = User.objects.get(id=user_id)
            task = Task.objects.get(id=task_id, assigned_to=user)
            task.status = new_status
            task.save()
            messages.success(request, "Task status updated.")
        except (User.DoesNotExist, Task.DoesNotExist):
            messages.error(request, "Failed to update task.")
    
    return redirect('user_task_page')


from .models import Notification

def user_notify(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to view notifications.")
        return redirect('user_login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('user_login')

    notifications = Notification.objects.filter(user=user).order_by('-timestamp')

    return render(request, 'user_notification_page.html', {
        'notifications': notifications,
        'user': user
    })


from django.http import JsonResponse
from .models import Notification

def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)


from django.http import JsonResponse
from .models import Notification

def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.delete()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def user_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        user.full_name = request.POST.get('fullname')
        user.email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if password and password == confirm_password:
            user.password = password  # ⚠️ You should hash this
        elif password:
            messages.error(request, "Passwords do not match.")
            return redirect('user_profile_page')

        if 'profile-image-upload' in request.FILES:
            user.profile_picture = request.FILES['profile-image-upload']

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('user_profile_page')

    return render(request, 'user_profile.html', {'user': user})



