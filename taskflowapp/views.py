from django.shortcuts import render

# Create your views here.
def register_page(request):
    return render(request,'register.html')

def admin_dash(request):
    return render(request,'admin_dashboard.html')
def admin_project(request):
    return render(request,'admin_project_page.html')
def admin_task(request):
    return render(request,'admin_task_page.html')

def admin_profile(request):
    return render(request,'admin_profile.html')
# def user_dash(request):
#     return render(request,'user_dashboard.html')
def user_task(request):
    return render(request,'user_task_page.html')
def user_profile(request):
    return render(request,'user_profile.html')
def user_notify(request):
    return render(request,'user_notification_page.html')
def landing(request):
    return render(request,'landing_page.html')
def home(request):
    return render(request,'home.html')
def role(request):
    return render(request,'role.html')
def admin_access(request):
    return render(request,'admin_access.html')

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



def admin_user_manage(request):
    if request.method == 'POST':
        name = request.POST.get('fullName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('roleSelect')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'User already exists.')
        else:
            User.objects.create(
                full_name=name,
                email=email,
                password=password,
                role=role
            )
            messages.success(request, 'User added successfully.')

        return redirect('admin_user_manage_page')

    users = User.objects.all()
    return render(request, 'admin_user_management_page.html', {'users': users})

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

    context = {
        'user': user,
    }
    return render(request, 'user_dashboard.html', context)

