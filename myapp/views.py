from django.shortcuts import render,redirect, get_object_or_404
from .models import CustomUser, Role, Department,IssueDB
from .forms import UserForm,IssueForm 
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from datetime import datetime


from django.utils import timezone
from datetime import datetime, timedelta




# Create your views here.
def admin_dashboard(request):
    return render(request, 'admin.html')# Render the admin dashboard template

def reporter_dashboard(request):
   return render(request, 'reporter.html')# Render the reporter dashboard template

def foreman_dashboard(request):
    return render(request, 'foreman.html')# Render the admin dashboard template

def worker_dashboard(request):
    return render(request, 'worker.html')# Render the admin dashboard template

# List all users
def user_management(request):
    users = CustomUser.objects.all()  # Fetch all users from the custom model
    return render(request, 'user_management.html', {'users': users})

# Search for a user
def search_user(request):
    query = request.GET.get('q', '')
    if query:
        users = CustomUser.objects.filter(username__icontains=query)
    else:
        users = CustomUser.objects.all()
    return render(request, 'user_management.html', {'users': users})

# Add a new user
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save the user just yet
            user.password = make_password(user.password)  # Hash the password
            form.save()
            messages.success(request, "User added successfully!")
            return redirect('user_management')
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

# Edit a user
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect('user_management')
    else:
        form = UserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form, 'user': user})

# Delete a user
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('user_management')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on the user's role
            if user.role_id == 4:
                return redirect('admin_dashboard')  # Redirect to your custom admin dashboard
            elif user.role_id == 3:
                return redirect('foreman_dashboard')  # Redirect to your custom admin dashboard
            elif  user.role_id == 2:
                return redirect('worker_dashboard')  # Redirect to your custom admin dashboard
            else:
                return redirect('reporter_dashboard')  # Redirect to user dashboard (or another page)
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('user_login')
        
    return render(request, 'login.html')

def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)  # Include request.FILES for image uploads
        if form.is_valid():
            issue = form.save(commit=False)
            issue.reporter = request.user  # Set the logged-in user as the reporter
            issue.reported_dept_id = request.user.department  # Automatically assign the department from the logged-in user
            issue.save()
            messages.success(request, 'Issue reported successfully!')
            return redirect('reporter_dashboard')  # Redirect to user dashboard or another page
    else:
        form = IssueForm()
    return render(request, 'report_issue.html', {'form': form})



# List all issues by admin
def issue_management(request):
    issues = IssueDB.objects.all()  # Fetch all users from the custom model
     #Update the priority of each issue based on age
    for issue in issues:
        adjusted_priority = issue.adjusted_priority()  # Get the adjusted priority
        if issue.priority != adjusted_priority:  # Only update if the priority has changed
            issue.priority = adjusted_priority
            issue.save()  # Save the updated issue
    return render(request, 'issue_management.html', {'issues': issues})


def user_details(request, id):
    user = get_object_or_404(CustomUser, id=id)
    return render(request, 'user_details.html', {'user': user})

def search_issue(request):
    search_by = request.GET.get('search_by')  # Get the search criterion from the dropdown
    query = request.GET.get('q', '')  # Get the search term

    if search_by and query:
        if search_by == 'id':
            issues = IssueDB.objects.filter(issue_id__icontains=query)
        elif search_by == 'location':
            issues = IssueDB.objects.filter(location__icontains=query)
        elif search_by == 'reporter':
            issues = IssueDB.objects.filter(reporter__first_name__icontains=query) | \
                     IssueDB.objects.filter(reporter__last_name__icontains=query)
        elif search_by == 'department':
            issues = IssueDB.objects.filter(reporter__department__dept_name__icontains=query)
        elif search_by == 'date':
              try:
        # Parse the query date in 'YYYY-MM-DD' format
                search_date = datetime.strptime(query, '%Y-%m-%d').date()

        # Convert the search_date to a timezone-aware datetime at midnight in 'Asia/Kolkata'
                search_datetime_start = timezone.make_aware(datetime.combine(search_date, datetime.min.time()), timezone.get_current_timezone())

        # Get the next day's start time to ensure the full day is covered
                search_datetime_end = search_datetime_start + timedelta(days=1)

        # Filter issues by date range
                issues = IssueDB.objects.filter(reported_date__gte=search_datetime_start, reported_date__lt=search_datetime_end)
              except ValueError:
                issues = IssueDB.objects.none()  # Return no results if the date is invalid
        else:
               issues = IssueDB.objects.none()  # Return no results if no valid search criteria

    else:
        issues = IssueDB.objects.all()  # If no search, show all issues
    
    return render(request, 'issue_management.html', {'issues': issues})


from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import UpdateView

class UpdatePriorityView(UpdateView):
    model = IssueDB
    fields = ['priority']  # Only allow changing the priority
    template_name = 'update_priority.html'  # Create this template
    success_url = '/issue-management/'  # Redirect after updating
   

    def form_valid(self, form):
        # Add additional validation logic if needed
        return super().form_valid(form)










