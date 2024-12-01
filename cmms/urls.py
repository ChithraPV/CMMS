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
    path('user/<int:id>/details/', views.user_details, name='user_details'),
    path('issue_management/search/', views.search_issue, name='search_issue'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



