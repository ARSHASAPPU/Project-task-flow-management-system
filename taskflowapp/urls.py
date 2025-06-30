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
     path('projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),
     path('projects/edit/<int:project_id>/', views.edit_project, name='edit_project'),

    path('admin_task/',views.admin_task,name='admin_task_page'),
    path('admin_task_delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('admin_task_edit/<int:task_id>/', views.edit_task, name='edit_task'),
   
    path('admin_user_manage/',views.admin_user_manage,name='admin_user_manage_page'),
    path('admin_user_delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    path('user_dash/',views.user_dash,name='user_dashboard'),
    path('user_task/',views.user_tasks,name='user_task_page'),
    path('user/update-task/<int:task_id>/', views.update_task_status, name='update_task'),
    path('notification/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'), 
     path('notification/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('user_profile/',views.user_profile,name='user_profile_page'),
    path('user_notify/',views.user_notify,name='user_notify_page'),
    
    path('landing/',views.landing),
    
]
