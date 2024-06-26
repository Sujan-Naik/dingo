"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from tasks.forms import CreateTaskForm1
from tasks.forms import CreateTaskForm2
from tasks.views import TaskDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('create_task/', views.CreateTaskWizard.as_view([CreateTaskForm1, CreateTaskForm2]), name='create_task'),
    path('team', views.TeamView.as_view(), name='team'),
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/modify', views.ModifyTaskView.as_view(), name='modify_task'),
    path('tasks/<int:pk>/delete', views.DeleteTaskView.as_view(), name='delete_task'),
    path('teams/', views.TeamListView.as_view(), name='team_list'),
    path('teams/<str:team_name>/delete', views.DeleteTeamView.as_view(), name='delete_team'),
    path('timelogging/<int:pk>/', views.TaskDetailView.as_view(), name='time_logging'),
    path('teams/<str:team_name>', views.TeamDetailView.as_view(), name='team_detail'),
    path('timeline/', views.TimelineView.as_view(), name='timeline'),
    path('timeline/<int:year>/', views.TimelineYearView.as_view(), name='timeline_year'),
    path('timeline/<int:year>/<int:month>/', views.TimelineMonthView.as_view(), name='timeline_month'),
    path('timezone', views.timezone_select, name='timezone'),
    path('Inbox', views.InboxPageView.as_view(), name='inbox'),
]