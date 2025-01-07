"""
URL configuration for cmms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myapp import views

# urls.py
#from django.conf.urls.i18n import urlpatterns as i18n_urls



urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('admin/', admin.site.urls),
    path('_admin/', views.admin_dashboard, name='admin_dashboard'),
    path('_reporter/', views.reporter_dashboard, name='reporter_dashboard'),
    path('_foreman/', views.foreman_dashboard, name='foreman_dashboard'),
    path('_worker/', views.worker_dashboard, name='worker_dashboard'),
    path('user-management/', views.user_management, name='user_management'),
    path('user-management/search/', views.search_user, name='search_user'),
    path('user-management/add/', views.add_user, name='add_user'),
    path('user-management/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user-management/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('issue-management/', views.issue_management, name='issue_management'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('issue-management/search/', views.search_issue, name='search_issue'),
    path('assigned_tasks/search/', views.search_tasks, name='search_tasks'),
    path('update-priority/', views.update_priority, name='update_priority'),
    path('issue-management/<int:pk>/assign-issue/', views.assign_issue.as_view(), name='assign_issue'),
    path('assigned_issues/', views.assigned_issues, name='assigned_issues'),
    path('assigned_tasks/', views.assigned_tasks, name='assigned_tasks'),
    path('in_progress_issues/', views.in_progress_issues, name='in_progress_issues'),
    path('completed_issues/', views.completed_issues, name='completed_issues'),
    path('completed_tasks/', views.completed_tasks, name='completed_tasks'),
    path('pending_tasks/', views.pending_tasks, name='pending_tasks'),
    path('extended_tasks/', views.extended_tasks, name='extended_tasks'),
    path('escalated_tasks/', views.escalated_tasks, name='escalated_tasks'),
    path('escalated_issues/', views.escalated_issues, name='escalated_issues'),
    path('reporter_assigned_tasks/', views.reporter_assigned_tasks, name='reporter_assigned_tasks'),
    path('reporter_pending_tasks/', views.reporter_pending_tasks, name='reporter_pending_tasks'),
    path('reporter_completed_tasks/', views.reporter_completed_tasks, name='reporter_completed_tasks'),
    path('reporter_escalated_tasks/', views.reporter_escalated_tasks, name='reporter_escalated_tasks'),
    path('worker_assigned_tasks/', views.worker_assigned_tasks, name='worker_assigned_tasks'),
    path('worker_extended_tasks/', views.worker_extended_tasks, name='worker_extended_tasks'),
    path('worker_escalated_tasks/', views.worker_escalated_tasks, name='worker_escalated_tasks'),
    path('worker_in_progress_tasks/', views.worker_in_progress_tasks, name='worker_in_progress_tasks'),
    path('worker_completed_tasks/', views.worker_completed_tasks, name='worker_completed_tasks'),
    path('assign_tasks/', views.assign_tasks, name='assign_tasks'),
    path('assign_tasks/<int:pk>/foreman_assign/',views.foreman_assign, name='foreman_assign'),
    path('view_tasks/',views.view_tasks, name='view_tasks'),
    path('view_tasks/<int:pk>/view_details/',views.details, name='details'),
    path('update-status/<int:pk>/', views.update_status, name='update_status'),
    path('extension_update_status/<int:pk>/', views.extension_update_status, name='extension_update_status'),
    path('escalate-task/<int:pk>/', views.escalate_task, name='escalate_task'),
    path('extend-due-date/<int:pk>/', views.extend_due_date, name='extend_due_date'),
    path('upload-image/<int:pk>/', views.upload_image, name='upload_image'),
    path('track_issue/', views.track_issue, name='track_issue'),
    path('issue_history/', views.issue_history, name='issue_history'),
    path('logout/', views.logout_view, name='logout'),
    path('calendar/',views.calendar,name='calendar'),
    path('issue_details/<int:pk>/', views.issue_details, name='issue_details'),
    path('extension_details/<int:pk>/extension_details/', views.extension_details, name='extension_details'),
    path('escalation_details/<int:pk>/extension_details/', views.escalation_details, name='escalation_details'),
    path('reports/', views.reports, name='reports'),
    path('generate_report/', views.generate_pdf_report, name='generate_pdf_report'),
    path('bulk_upload_users/', views.bulk_upload_users, name='bulk_upload_users'),
    path('password_change/',views.password_change,name='password_change'),
    


]#+ i18n_urls   Include the language switcher URLs

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



