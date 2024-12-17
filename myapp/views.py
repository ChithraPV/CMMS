from django.shortcuts import render,redirect, get_object_or_404
from .models import CustomUser, Role, Department,IssueDB,Task,ExtensionRequest,Escalation,TaskImage,IssueStatusChange
from .forms import UserForm,IssueForm,AssignIssueForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count

def admin_dashboard(request):
    user_name = request.user.first_name  # Get the first name of the user
    
    total_issues = IssueDB.objects.count()
    in_progress = IssueDB.objects.filter(status__in=["Assigned to Worker","In Progress"]).count()
    completed = IssueDB.objects.filter(status="Completed").count()
    extended = IssueDB.objects.filter(status__in=["Extension Approved","Extension Rejected","Extension Pending"]).count()
    escalated = IssueDB.objects.filter(status__in=['Escalation Pending','Escalation Approved','Escalation Rejected']).count()
    
    CATEGORY_CHOICES = [
        ('Electrical Maintenance', 'Electrical Maintenance'),
        ('Plumbing Maintenance', 'Plumbing Maintenance'),
        ('HVAC (Heating, Ventilation, and Air Conditioning)', 'HVAC (Heating, Ventilation, and Air Conditioning)'),
        ('Building & Structural Maintenance', 'Building & Structural Maintenance'),
        ('Furniture Maintenance', 'Furniture Maintenance'),
        ('IT & Computer Equipment Maintenance', 'IT & Computer Equipment Maintenance'),
        ('Landscape & Groundskeeping', 'Landscape & Groundskeeping'),
        ('Others', 'Others'),
    ]
    
    # Dynamically compute counts for each category
    category_data = []
    category_labels = []
    for category_key, category_label in CATEGORY_CHOICES:
        count = IssueDB.objects.filter(issue_category__iexact=category_key).count()
        category_labels.append(category_label)
        category_data.append(count)

    high_priority = IssueDB.objects.filter(priority='3').count()
    medium_priority = IssueDB.objects.filter(priority='2').count()
    low_priority = IssueDB.objects.filter(priority='1').count()
    issues_data = list(
        IssueDB.objects.values('reported_date', 'priority', 'issue_category','reported_dept_id')
        .annotate(issues_count=Count('issue_id'))
        .order_by('reported_date')
    )
    for issue in issues_data:
        issue['reported_date'] = issue['reported_date'].isoformat()
    department_names = Department.objects.filter(dept_id__range=(100, 200)).values_list('dept_name', flat=True)
    department_ids = Department.objects.filter(dept_id__range=(100, 200)).values_list('dept_id', flat=True)

    department_dict = dict(zip(department_names, department_ids))
    context = {
        'issues': total_issues,
        'in_progress': in_progress,
        'completed': completed,
        'extended': extended,
        'escalated': escalated,
        'category_labels': category_labels,
        'category_data': category_data,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'departments': department_dict,
        'user_name': user_name,
        #'issues_data': list(issues_data),
        'issues_data': json.dumps(list(issues_data)),  # Convert QuerySet to list for JSON serialization
    }
    
    return render(request, 'admin.html', context)

def reporter_dashboard(request):
    total_issues=IssueDB.objects.filter(reporter=request.user).count()
    #total_issues = IssueDB.objects.fileter(reported_dept_id="request.user.dept_id").count()
    in_progress = IssueDB.objects.filter(status__in=["Assigned to Worker","In Progress","Escalation Rejected","Extension Rejected"],reporter=request.user).count()
    completed = IssueDB.objects.filter(status="Completed",reporter=request.user).count()
    extended = IssueDB.objects.filter(status__in=["Extension Approved","Extension Pending"],reporter=request.user).count()
    escalated = IssueDB.objects.filter(status__in=["Escalation Approved","Escalation Pending"],reporter=request.user).count()
    
    CATEGORY_CHOICES = [
        ('Electrical Maintenance', 'Electrical Maintenance'),
        ('Plumbing Maintenance', 'Plumbing Maintenance'),
        ('HVAC (Heating, Ventilation, and Air Conditioning)', 'HVAC (Heating, Ventilation, and Air Conditioning)'),
        ('Building & Structural Maintenance', 'Building & Structural Maintenance'),
        ('Furniture Maintenance', 'Furniture Maintenance'),
        ('IT & Computer Equipment Maintenance', 'IT & Computer Equipment Maintenance'),
        ('Landscape & Groundskeeping', 'Landscape & Groundskeeping'),
        ('Others', 'Others'),
    ]
    
    # Dynamically compute counts for each category
    category_data = []
    category_labels = []
    for category_key, category_label in CATEGORY_CHOICES:
        count = IssueDB.objects.filter(issue_category__iexact=category_key,reporter=request.user).count()
        category_labels.append(category_label)
        category_data.append(count)

    high_priority = IssueDB.objects.filter(priority='3',reporter=request.user).count()
    medium_priority = IssueDB.objects.filter(priority='2',reporter=request.user).count()
    low_priority = IssueDB.objects.filter(priority='1',reporter=request.user).count()

    issues_data = list(
        IssueDB.objects.values('reported_date', 'priority', 'issue_category',).filter(reporter=request.user).annotate(issues_count=Count('issue_id')).order_by('reported_date')
    )
    for issue in issues_data:
        issue['reported_date'] = issue['reported_date'].isoformat()
    # department_names = Department.objects.filter(dept_id__range=(100, 200)).values_list('dept_name', flat=True)
    # department_ids = Department.objects.filter(dept_id__range=(100, 200)).values_list('dept_id', flat=True)

    # department_dict = dict(zip(department_names, department_ids))
    context = {
        'issues': total_issues,
        'in_progress': in_progress,
        'completed': completed,
        'extended': extended,
        'escalated': escalated,
        'category_labels': category_labels,
        'category_data': category_data,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
       # 'departments': department_dict,
        'issues_data': json.dumps(list(issues_data)),  # Convert QuerySet to list for JSON serialization
    }
    return render(request, 'reporter.html',context)# Render the reporter dashboard template

def foreman_dashboard(request):
    foreman=request.user
    dept = request.user.department
    #issues = IssueDB.objects.filter(assigned_dept_id=dept) 
    total_issues = IssueDB.objects.filter(assigned_dept_id=dept).count()
    in_progress = IssueDB.objects.filter(status__in=["Assigned to Worker","In Progress"],assigned_dept_id=dept).count()
    completed = IssueDB.objects.filter(status="Completed",assigned_dept_id=dept).count()
    extended = IssueDB.objects.filter(status="Extension Approved",assigned_dept_id=dept).count()
    escalated = IssueDB.objects.filter(status="Escalation Approved",assigned_dept_id=dept).count()
    
    CATEGORY_CHOICES = [
        ('Electrical Maintenance', 'Electrical Maintenance'),
        ('Plumbing Maintenance', 'Plumbing Maintenance'),
        ('HVAC (Heating, Ventilation, and Air Conditioning)', 'HVAC (Heating, Ventilation, and Air Conditioning)'),
        ('Building & Structural Maintenance', 'Building & Structural Maintenance'),
        ('Furniture Maintenance', 'Furniture Maintenance'),
        ('IT & Computer Equipment Maintenance', 'IT & Computer Equipment Maintenance'),
        ('Landscape & Groundskeeping', 'Landscape & Groundskeeping'),
        ('Others', 'Others'),
    ]
    
    # Dynamically compute counts for each category
    category_data = []
    category_labels = []
    for category_key, category_label in CATEGORY_CHOICES:
        count = IssueDB.objects.filter(issue_category__iexact=category_key).count()
        category_labels.append(category_label)
        category_data.append(count)

    high_priority = IssueDB.objects.filter(priority='3',assigned_dept_id=dept).count()
    medium_priority = IssueDB.objects.filter(priority='2',assigned_dept_id=dept).count()
    low_priority = IssueDB.objects.filter(priority='1',assigned_dept_id=dept).count()

    issues_data = list(
        IssueDB.objects.values('reported_date', 'priority', 'issue_category','reported_dept_id').filter(assigned_dept_id=dept)
        .annotate(issues_count=Count('issue_id'))
        .order_by('reported_date')
    )
    for issue in issues_data:
        issue['reported_date'] = issue['reported_date'].isoformat()
    department_names = Department.objects.filter(dept_id__range=(100, 200)).values_list('dept_name', flat=True)
    department_ids = Department.objects.filter(dept_id__range=(100, 200)).values_list('dept_id', flat=True)

    department_dict = dict(zip(department_names, department_ids))
    context = {
        'issues': total_issues,
        'in_progress': in_progress,
        'completed': completed,
        'extended': extended,
        'escalated': escalated,
        'category_labels': category_labels,
        'category_data': category_data,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'departments': department_dict,
        'issues_data': json.dumps(list(issues_data)),  # Convert QuerySet to list for JSON serialization
    }
    return render(request, 'foreman.html',context)# Render the admin dashboard template

def worker_dashboard(request):
    worker = request.user
    #tasks = Task.objects.select_related('issue_id').filter(worker=worker,issue_id__status='Assigned to Worker')
    total_issues = Task.objects.filter(worker=worker).count()
    #in_progress = Task.objects.filter(status="In progress",worker=worker).count()
    in_progress = Task.objects.filter(issue_id__status="In progress", worker=worker).count()

    completed = Task.objects.filter(issue_id__status="Completed",worker=worker).count()
    extended = Task.objects.filter(issue_id__status="Extension Approved",worker=worker).count()
    escalated = Task.objects.filter(issue_id__status="Escalation Approved",worker=worker).count()
    
    CATEGORY_CHOICES = [
        ('Electrical Maintenance', 'Electrical Maintenance'),
        ('Plumbing Maintenance', 'Plumbing Maintenance'),
        ('HVAC (Heating, Ventilation, and Air Conditioning)', 'HVAC (Heating, Ventilation, and Air Conditioning)'),
        ('Building & Structural Maintenance', 'Building & Structural Maintenance'),
        ('Furniture Maintenance', 'Furniture Maintenance'),
        ('IT & Computer Equipment Maintenance', 'IT & Computer Equipment Maintenance'),
        ('Landscape & Groundskeeping', 'Landscape & Groundskeeping'),
        ('Others', 'Others'),
    ]
    
    # Dynamically compute counts for each category
    category_data = []
    category_labels = []
    for category_key, category_label in CATEGORY_CHOICES:
        count = IssueDB.objects.filter(issue_category__iexact=category_key).count()
        category_labels.append(category_label)
        category_data.append(count)

    high_priority =  Task.objects.filter(issue_id__priority='3',worker=worker).count()
   
    medium_priority =  Task.objects.filter(issue_id__priority='2',worker=worker).count()
    low_priority =  Task.objects.filter(issue_id__priority='1',worker=worker).count()

    issues_data = list(
        IssueDB.objects.values('reported_date', 'priority', 'issue_category','reported_dept_id').filter(task__worker=worker).annotate(issues_count=Count('issue_id'))
        .order_by('reported_date')
    )
    for issue in issues_data:
        issue['reported_date'] = issue['reported_date'].isoformat()
    department_names = Department.objects.filter(dept_id__range=(100, 200)).values_list('dept_name', flat=True)
    department_ids = Department.objects.filter(dept_id__range=(100, 200)).values_list('dept_id', flat=True)

    department_dict = dict(zip(department_names, department_ids))
    context = {
        'issues': total_issues,
        'in_progress': in_progress,
        'completed': completed,
        'extended': extended,
        'escalated': escalated,
        'category_labels': category_labels,
        'category_data': category_data,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'departments': department_dict,
        'issues_data': json.dumps(list(issues_data)),  # Convert QuerySet to list for JSON serialization
    }
    return render(request, 'worker.html',context)# Render the admin dashboard template

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
            user = form.save(commit=False)  # Don't save the user just yet
            user.password = make_password(user.password)  # Hash the password
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
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.reporter = request.user
            issue.reported_dept_id = request.user.department

            # Check for categories that map to departments
            category_to_dept_map = {
                'Electrical Maintenance': 'ELECTRONICS',
                'Plumbing Maintenance': 'Plumbing Department',
                'HVAC': 'HVAC Department',
                'Building Maintenance': 'Building Department',
                'Furniture Maintenance': 'CARPENTRY',
                'IT & Computer Equipment Maintenance': 'IT Department',
                'Landscape & Groundskeeping': 'Groundskeeping Department',
            }

            # If it's "Others," leave unassigned for admin to assign
            if issue.issue_category != 'Others':
                department_name = category_to_dept_map.get(issue.issue_category)
                if department_name:
                    try:
                        department = Department.objects.get(dept_name=department_name)
                        issue.assigned_dept = department
                        issue.status = 'Assigned to Foreman' 
                    except Department.DoesNotExist:
                        messages.error(request, f"Could not find the department for {department_name}.")
                        return redirect('report_issue')
                else:
                    messages.error(request, "Invalid issue category selected.")
                    return redirect('report_issue')
            else:
                # Leave unassigned or pending review for admin assignment
                issue.status = 'Pending'  # This status can later be updated by admin

            # Save the issue
            issue.save()

            # Log the status change (indicating it's reported and pending review)
            IssueStatusChange.objects.create(
                issue=issue,
                status=issue.status,
                changed_by=request.user
            )

            messages.success(request, 'Issue reported successfully!')
            return redirect('reporter_dashboard')

    else:
        form = IssueForm()

    return render(request, 'report_issue.html', {'form': form})

def assigned_issues(request):
     issues = IssueDB.objects.filter(status='Assigned to Foreman')
     return render(request, 'issue_management.html', {'issues': issues})
def in_progress_issues(request):
    issues = IssueDB.objects.filter(status__in=['Assigned to Worker','In Progress'])
    return render(request, 'issue_management.html', {'issues': issues})
def completed_issues(request):
    issues = IssueDB.objects.filter(status='Completed')
    return render(request, 'issue_management.html', {'issues': issues})
def escalated_issues(request):
    issues = IssueDB.objects.filter(status__in=['Escalation Pending','Escalation Approved','Escalation Rejected'])
    return render(request, 'issue_management.html', {'issues': issues})

# List all issues by admin
def issue_management(request):
   # issues = IssueDB.objects.all()  # Fetch all users from the custom model
    issues = IssueDB.objects.all()
 
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

def search_tasks(request):
    search_by = request.GET.get('search_by')  # Get the search criterion from the dropdown
    query = request.GET.get('q', '')  # Get the search term

    if search_by and query:
        if search_by == 'id' :
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
    
    return render(request, 'assign_tasks.html', {'issues': issues})

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import UpdateView


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import IssueDB

@csrf_exempt  # Only use this if you're bypassing CSRF for simplicity
def update_priority(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            issue_id = data.get('issue_id')
            priority_str = data.get('priority')

            # Map priority string to integer (adjust if needed)
            priority_map = {'High': 3, 'Medium': 2, 'Low': 1}
            priority_value = priority_map.get(priority_str)  # Convert string to number

            if priority_value is None:
                return JsonResponse({'success': False, 'error': 'Invalid priority value'})

            # Get the issue and update the priority
            issue = IssueDB.objects.get(pk=issue_id)
            issue.priority = priority_value  # Store the numeric value
            issue.save()

            return JsonResponse({'success': True})  # Return success response
        except IssueDB.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Issue not found'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

from .forms import AssignDeptForm
from django.urls import reverse_lazy 
class assign_issue(UpdateView):
    
    model = IssueDB
    form_class = AssignDeptForm  
   # fields = ['assigned_dept']  # Allow updating the assigned department
    template_name = 'assign_issue.html'  # Create this template
    success_url = reverse_lazy('issue_management')  # Use reverse_lazy for cleaner URL management

    def form_valid(self, form):
        issue = form.save(commit=False)  # Save the form but delay committing to the database
        
        # Update the status
        previous_status = issue.status
        issue.status = 'Assigned to Foreman'
        issue.save()  # Save changes to the database

        # Log the status change
        IssueStatusChange.objects.create(
            issue=issue,
            status='Assigned to Foreman',
            changed_by=self.request.user  # Log the user making the change
        )

        # Add a success message
        messages.success(self.request, f"Issue assigned to department and status updated from '{previous_status}' to 'Assigned to Foreman'.")
        
        return super().form_valid(form)


def assign_tasks(request):
    if request.method == 'POST':
        form = AssignIssueForm(request.POST, request.FILES)  # Include request.FILES for image uploads
    foreman=request.user
    dept = request.user.department
    issues = IssueDB.objects.filter(assigned_dept_id=dept) # Fetch all users from the custom model
    tasks = Task.objects.filter(assigned_dept_id=dept)
    return render(request, 'assign_tasks.html', {'issues': issues,'task':tasks})

def assigned_tasks(request):
    dept = request.user.department
    issues = IssueDB.objects.filter(assigned_dept_id=dept,status__in=["Assigned to Worker","In Progress"]) 
    return render(request, 'assign_tasks.html', {'issues': issues})

def pending_tasks(request):
     dept = request.user.department
     issues = IssueDB.objects.filter(assigned_dept_id=dept,status="Assigned to Foreman")
     return render(request, 'assign_tasks.html', {'issues': issues})

def completed_tasks(request):
     dept = request.user.department
     issues = IssueDB.objects.filter(assigned_dept_id=dept,status='Completed')
     return render(request, 'assign_tasks.html', {'issues': issues})

def escalated_tasks(request):
     # = IssueDB.objects.filter(status='Escalation Pending' or 'Escalation Rejected')
     dept = request.user.department
     issues = IssueDB.objects.filter(assigned_dept_id=dept,status__in=['Escalation Pending', 'Escalation Approved'])
     return render(request, 'assign_tasks.html', {'issues': issues})

def extended_tasks(request):
      dept = request.user.department
      issues = IssueDB.objects.filter(assigned_dept_id=dept,status='Extension Pending')
      return render(request, 'assign_tasks.html', {'issues': issues})

def foreman_assign(request,pk):
    foreman = request.user  # Assuming the logged-in user is the foreman
    dept_id = foreman.department_id   # Ensure 'dept_id' is available
    if request.method == 'POST':
        form = AssignIssueForm(request.POST, request.FILES,dept_id=dept_id)  # Include request.FILES for image uploads
        if form.is_valid():
            Task = form.save(commit=False)
            Task.issue_id  = get_object_or_404(IssueDB, issue_id=pk)
            Task.issue_id.status = 'Assigned to Worker'  # Update the status
            Task.issue_id.save()
           # task.issue_id = pk  # Set the logged-in user as the reporter
            Task.assigned_dept = request.user.department # Automatically assign the department from the logged-in user
            Task.save()
            IssueStatusChange.objects.create(
                issue=Task.issue_id,
                status='Assigned to Worker',
                changed_by=request.user
            )
            messages.success(request, 'Issue reported successfully!')
            return redirect('assign_tasks')  # Redirect to user dashboard or another page
    else:
        # Instantiate the form with dept_id
        form = AssignIssueForm(dept_id=dept_id)
    return render(request, 'real_task.html', {'form': form})



def view_tasks(request):
    worker = request.user
    tasks = Task.objects.select_related('issue_id').filter(worker=worker,issue_id__status='Assigned to Worker')
    tasks_json = [
        {
            
            "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None
        }
        for task in tasks if task.due_date
    ]  
    context = {
        'tasks': tasks, 
        'tasks_json': json.dumps(tasks_json)  # Convert the list to JSON string
    }
   
    return render(request, 'view_tasks.html', context)

def details(request,pk):
    details=Task.objects.select_related('issue_id').filter(task_id=pk)
    status_changes = IssueStatusChange.objects.all().order_by('changed_at')
    context = {
        'details': details,
        'status_changes': status_changes, 
         # Convert the list to JSON string
    }
    return render(request, 'task_details.html',context)

def extension_update_status(request, pk):
   if request.method == 'POST':
        # Get the new status and progress description
        new_status = request.POST.get('status')
        issue = get_object_or_404(IssueDB, pk=pk)
        # Update task status and progress
        issue.status = new_status
        issue.save()
        IssueStatusChange.objects.create(
            issue=issue,
            status=new_status,
            changed_by=request.user  # Assumes request.user is the one updating the status
        )
        messages.success(request, "Status updated successfully!")
        
       # Handle image upload if present
        if request.FILES.get('image'):
            image_file = request.FILES['image']
            task = Task.objects.filter(issue_id=pk).first()
            TaskImage.objects.create(task=task, image=image_file)
            messages.success(request, "Image uploaded successfully!")
        return redirect('extended_tasks')
from django.http import JsonResponse

# def update_status(request, pk):
#     if request.method == 'POST':
#         # Get the new status from the form data
#         new_status = request.POST.get('status')
        
#         if new_status:  # Ensure new status is provided
#             # Fetch the issue by primary key (pk)
#             issue = get_object_or_404(IssueDB, pk=pk)
            
#             # Update task status
#             issue.status = new_status
#             issue.save()

#             # Create a new IssueStatusChange to record this change
#             IssueStatusChange.objects.create(
#                 issue=issue,
#                 status=new_status,
#                 changed_by=request.user  # Assumes request.user is the one updating
#             )
#         new_comment = request.POST.get('comment')
#         if new_comment:
#             issue = get_object_or_404(IssueDB, pk=pk)
#             issue.comment = new_comment
#             issue.save()
#             # Handle image upload if present
#         if 'image' in request.FILES:
#             image_file = request.FILES['image']
#             task = Task.objects.filter(issue_id=pk).first()
#             if task:  # Ensure the task exists
#                 TaskImage.objects.create(task=task, image=image_file)
#                 messages.success(request, "Image uploaded successfully!")
#             else:
#                 messages.error(request, "Task not found.")
#             messages.success(request, " Status updated.")
#             return redirect('view_tasks')

#         else:
#             messages.error(request, "Status is required.")
    
#     # Optional: If not a POST request, handle accordingly
#     return redirect('view_tasks')  # Default action if method isn't POST

def update_status(request, pk):
    if request.method == 'POST':
        # Fetch the issue only once to reduce overhead
        issue = get_object_or_404(IssueDB, pk=pk)
        status_updated = False  # Track if status was updated
        comment_added = False   # Track if comment was added

        # Update task status if provided
        new_status = request.POST.get('status')
        if new_status:
            issue.status = new_status
            issue.save()
            IssueStatusChange.objects.create(
                issue=issue,
                status=new_status,
                changed_by=request.user
            )
            status_updated = True

        # Update the comment if provided
        new_comment = request.POST.get('comment')
        if new_comment:
            issue.comment = new_comment
            issue.save()
            comment_added = True

        # Handle image upload if present
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            task = Task.objects.filter(issue_id=pk).first()  # Fetch related task
            if task:
                TaskImage.objects.create(task=task, image=image_file)
                messages.success(request, "Image uploaded successfully!")
            else:
                messages.error(request, "Task not found. Image not saved.")

        # Feedback messages for status and comment updates
        if status_updated:
            messages.success(request, "Status updated successfully.")
        if comment_added:
            messages.success(request, "Comment added successfully.")

        # If no valid inputs, show error
        if not (new_status or new_comment or 'image' in request.FILES):
            messages.error(request, "No changes detected. Please provide status, comment, or image.")

        return redirect('view_tasks')

    # Optional: Handle GET request fallback
    messages.error(request, "Invalid request method.")
    return redirect('view_tasks')


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
 
def escalate_task(request, pk):
    task = get_object_or_404(Task,pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        other_reason = request.POST.get('other_reason')

        # Use the custom reason if "Other" is selected
        final_reason = other_reason if reason == 'Other' else reason
        task.issue_id.status='Escalation Pending'
        task.issue_id.save()
        Escalation.objects.create(
            task=task,
            worker=request.user,
            reason=final_reason
        )
        IssueStatusChange.objects.create(
            issue=task.issue_id,
            status='Escalation Pending',
            changed_by=request.user
        )

        messages.success(request, 'Task escalation request submitted.')
        return redirect('details', pk=task.task_id)
    return render(request, 'escalate_task.html', {'task': task})
def extend_due_date(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        new_due_date = request.POST.get('new_due_date')
        reason = request.POST.get('reason')
        other_reason = request.POST.get('other_reason')

        # Use the custom reason if "Other" is selected
        final_reason = other_reason if reason == 'Other' else reason
        task.issue_id.status='Extension Pending'
        task.issue_id.save()
        ExtensionRequest.objects.create(
            task=task,
            worker=request.user,
            new_due_date=new_due_date,
            reason=final_reason
        )
        IssueStatusChange.objects.create(
            issue=task.issue_id,
            status='Extension Pending',
            changed_by=request.user
        )

        messages.success(request, 'Due date extension request submitted.')
        return redirect('details', pk=pk)
    return render(request, 'extend_due_date.html', {'task': task})

def upload_image(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST' and request.FILES.get('image'):
        # Save uploaded image to database
        image_file = request.FILES['image']
        TaskImage.objects.create(task=task, image=image_file)

        messages.success(request, "Image uploaded successfully!")
        return redirect('details', pk=pk)

    # return render(request, 'upload_image.html', {'task': task})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import IssueDB, Task

@login_required  # Ensure only logged-in users can access this view
def track_issue(request):
    """
    Fetch issue data and ensure only the reporter can view their issues.
    """
    issue_id_query = request.GET.get("issueId")  # Capture query from search box
    
    if issue_id_query:
        # Query for the issue
        issue = IssueDB.objects.filter(issue_id=issue_id_query).first()

        # Ensure issue exists and that the logged-in user is the reporter
        if issue and issue.reporter == request.user:
            # Query task safely
            task = Task.objects.filter(issue_id=issue_id_query).first()
            # Fetch status change history for the issue
            status_history = IssueStatusChange.objects.filter(issue_id=issue_id_query).order_by('changed_at')
            
            context = {
                'issue': issue,
                'issue_status': issue.status,
                'task': task if task else None,
                'status_history': status_history,  # Pass the timeline data
                'error': None
            }
        elif not issue:
            context = {
                'error': "Issue ID not found.",
            }
        else:
            # Unauthorized access
            context = {
                'error': "You are not authorized to view this issue.",
            }
   
    else:
            # Unauthorized access
            context = {
                'error': "Please enter the Issue ID  to track the status and progress of your request",
            }

    return render(request, 'track_issues.html', context)
def issue_details(request,pk):
   
    issue_id_query=pk
    if issue_id_query:
        # Query for the issue
            issue = IssueDB.objects.filter(issue_id=issue_id_query).first()

        
            task = Task.objects.filter(issue_id=issue_id_query).first()
            # Fetch status change history for the issue
            status_history = IssueStatusChange.objects.filter(issue_id=issue_id_query).order_by('changed_at')
            
            context = {
                'issue': issue,
                'issue_status': issue.status,
                'task': task if task else None,
                'status_history': status_history,  # Pass the timeline data
                'error': None
            }
        

    return render(request, 'forman_details.html', context)
def my_issue_details(request,pk):
   
    issue_id_query=pk
    if issue_id_query:
        # Query for the issue
            issue = IssueDB.objects.filter(issue_id=issue_id_query).first()

        
            task = Task.objects.filter(issue_id=issue_id_query).first()
            # Fetch status change history for the issue
            status_history = IssueStatusChange.objects.filter(issue_id=issue_id_query).order_by('changed_at')
            
            context = {
                'issue': issue,
                'issue_status': issue.status,
                'task': task if task else None,
                'status_history': status_history,  # Pass the timeline data
                'error': None
            }
        

    return render(request, 'reporter_details.html', context)

def autocomplete_category(request):
    """
    Returns a list of issue categories and their descriptions based on the user's search query.
    """
    query = request.GET.get('query', '')  # Search term from the client (entered in the input)
    if query:
        # Fetch categories and descriptions matching the query
        categories = IssueDB.objects.filter(issue_category__icontains=query).values('issue_category', 'issue_description').distinct()
        category_list = [{'category': category['issue_category'], 'description': category['issue_description']} for category in categories]
    else:
        category_list = []

    return JsonResponse({'categories': category_list})
    # """
    # Returns a list of issue categories based on the user's search query.
    # """
    # query = request.GET.get('query', '')  # Search term from the client (entered in the input)
    # if query:
    #     # Fetch categories matching the query
    #     categories = IssueDB.objects.filter(issue_category__icontains=query).values('issue_category').distinct()
    #     category_list = [category['issue_category'] for category in categories]
    # else:
    #     category_list = []

    # return JsonResponse({'categories': category_list})
def issue_history(request):
    issues=IssueDB.objects.filter(reporter=request.user).all()
    return render(request, 'issue_history.html', {'issues':issues})
   
def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('user_login')  # Redirect to the login page

def review_extension(request):
    extension=ExtensionRequest.objects.filter(reporter=request.user).all()






import json
from datetime import datetime
from django.shortcuts import render
from .models import Task




def calendar(request):
    worker = request.user
    # Select tasks that belong to the worker with a valid due date
    tasks = Task.objects.select_related('issue_id').filter(worker=worker)

    # Filter only future due dates and extract necessary data
    tasks_json = [
        {
            "due_date": task.due_date.strftime('%Y-%m-%d'),
            "task_id": task.task_id,
            "description": task.issue_id.issue_description,
            "priority": task.issue_id.priority,
            "assigned_date": task.assigned_date.strftime('%Y-%m-%d') if task.assigned_date else None,
        }
        for task in tasks 
        if task.due_date and task.due_date >= datetime.now().date()
    ]
    
    context = {
        'tasks': tasks, 
        'tasks_json': json.dumps(tasks_json)  # Pass the due dates and relevant data as JSON to the frontend
    }
   
    return render(request, 'tasks.html', context)


def extension_details(request, pk):
    issues = IssueDB.objects.filter(issue_id=pk)
    tasks = Task.objects.filter(issue_id=pk)
    
    # Ensure that you're using the task_id value correctly
    extension = ExtensionRequest.objects.filter(task_id__in=tasks.values('task_id'))

    return render(request, 'extension_details.html', {'issues': issues, 'task': tasks, 'extension': extension})

def escalation_details(request, pk):
    issues = IssueDB.objects.filter(issue_id=pk)
    tasks = Task.objects.filter(issue_id=pk)
    
    # Ensure that you're using the task_id value correctly
    escalation = Escalation.objects.filter(task_id__in=tasks.values('task_id'))

    return render(request, 'escalation_details.html', {'issues': issues, 'task': tasks, 'escalation': escalation})











def reporter_assigned_tasks(request):
    dept = request.user.department
    issues = IssueDB.objects.filter(reported_dept_id_id=dept) 
    return render(request, 'issue_history.html', {'issues': issues})

def reporter_pending_tasks(request):
     dept = request.user.department
     issues = IssueDB.objects.filter(reported_dept_id_id=dept,status__in=["Assigned to Worker","In Progress",'Escalation Rejected'])
     return render(request, 'issue_history.html', {'issues': issues})

def reporter_completed_tasks(request):
     dept = request.user.department
     issues = IssueDB.objects.filter(reported_dept_id_id=dept,status='Completed')
     return render(request, 'issue_history.html', {'issues': issues})
def reporter_escalated_tasks(request):
     # = IssueDB.objects.filter(status='Escalation Pending' or 'Escalation Rejected')
     dept = request.user.department
     issues = IssueDB.objects.filter(reported_dept_id_id=dept,status__in=['Escalation Pending', 'Escalation Approved'])

     return render(request, 'issue_history.html', {'issues': issues})

def worker_assigned_tasks(request):
    worker = request.user
    tasks = Task.objects.select_related('issue_id').filter(worker=worker)
    tasks_json = [
        {
            
            "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None
        }
        for task in tasks if task.due_date
    ]  
    context = {
        'tasks': tasks, 
        'tasks_json': json.dumps(tasks_json)  # Convert the list to JSON string
    }
   
    return render(request, 'view_tasks.html', context)
def worker_extended_tasks(request):
    worker = request.user
    tasks = Task.objects.select_related('issue_id').filter(worker=worker,issue_id__status='Extension Approved')
    tasks_json = [
        {
            
            "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None
        }
        for task in tasks if task.due_date
    ]  
    context = {
        'tasks': tasks, 
        'tasks_json': json.dumps(tasks_json)  # Convert the list to JSON string
    }
   
    return render(request, 'view_tasks.html', context)
def worker_escalated_tasks(request):
    worker = request.user
    tasks = Task.objects.select_related('issue_id').filter(worker=worker,issue_id__status='Escalation Approved')
    tasks_json = [
        {
            
            "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None
        }
        for task in tasks if task.due_date
    ]  
    context = {
        'tasks': tasks, 
        'tasks_json': json.dumps(tasks_json)  # Convert the list to JSON string
    }
   
    return render(request, 'view_tasks.html', context)
def worker_in_progress_tasks(request):
    worker = request.user
    tasks = Task.objects.select_related('issue_id').filter(worker=worker,issue_id__status='In Progress')
    tasks_json = [
        {
            
            "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None
        }
        for task in tasks if task.due_date
    ]  
    context = {
        'tasks': tasks, 
        'tasks_json': json.dumps(tasks_json)  # Convert the list to JSON string
    }
   
    return render(request, 'view_tasks.html', context)
def worker_completed_tasks(request):
    worker = request.user
    tasks = Task.objects.select_related('issue_id').filter(worker=worker,issue_id__status='Completed')
    tasks_json = [
        {
            
            "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None
        }
        for task in tasks if task.due_date
    ]  
    context = {
        'tasks': tasks, 
        'tasks_json': json.dumps(tasks_json)  # Convert the list to JSON string
    }
   
    return render(request, 'view_tasks.html', context)

