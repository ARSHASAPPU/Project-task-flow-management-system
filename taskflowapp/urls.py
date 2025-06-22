from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
   
    path('',views.home,name='home_page'),
    path('role/',views.role,name='role'),
    path('login/',views.user_login,name='user_login'),
    path('admin_access/',views.admin_access,name='admin_access_page'),
    path('admin_login/',views.admin_login,name='admin_login_page'),
    path('register/',views.register_page,name='register_page'),
   
    path('admin_dash/',views.admin_dash,name='admin_dashboard'),
    path('admin_project/',views.admin_project,name='admin_project_page'),
    path('admin_task/',views.admin_task,name='admin_task_page'),
    path('admin_user_manage/',views.admin_user_manage,name='admin_user_manage_page'),
    path('admin_profile/',views.admin_profile,name='admin_profile_page'),
    path('user_dash/',views.user_dash,name='user_dashboard'),
    path('user_task/',views.user_task,name='user_task_page'),
    path('user_profile/',views.user_profile,name='user_profile_page'),
    path('user_notify/',views.user_notify,name='user_notify_page'),
    
    path('landing/',views.landing),
    
]
