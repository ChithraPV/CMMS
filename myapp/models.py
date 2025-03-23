from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
from django.conf import settings  # This imports the custom user model

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)  # Dept ID is an auto-incrementing primary key
    dept_name = models.CharField(max_length=100)  # Department name
    def __str__(self):
        return self.dept_name
    
    
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    role_name = models.CharField(max_length=100)  # Role name (e.g., Admin, User, etc.)
    def __str__(self):
        return self.role_name

class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)# Foreign Key to Role model
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)# Foreign Key to Department model
    def __str__(self):
        return self.username
    
class IssueDB(models.Model):
    issue_id = models.AutoField(primary_key=True)  # Issue ID (Primary Key)
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
    issue_category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='Electrical Maintenance')  # Issue category
    reported_dept_id = models.ForeignKey(Department, related_name='reported_issues',   on_delete=models.SET_NULL, null=True, blank=True)  # Reported department (ForeignKey to Department)
    reporter = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_issues')  # Reporter (ForeignKey to User model)
    location = models.CharField(max_length=255)  # Location of the issue
    issue_description = models.TextField()  # Description of the issue

    # Priority of the issue (Low, Medium, High) stored as integers (3, 2, 1)
    PRIORITY_CHOICES = [
        (3, 'High'),
        (2, 'Medium'),
        (1, 'Low'),
    ]
    priority = models.IntegerField(choices=PRIORITY_CHOICES, null=True, blank=True,)  # Default set to 'Medium' (value 2)

    # Status of the issue (Pending, In Progress, Resolved, Closed)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Assigned to Foreman', 'Assigned to Foreman'),
        ('Assigned to Worker', 'Assigned to Worker'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
        ('Escalation Pending', 'Escalation Pending'),
        ('Escalation Approved', 'Escalation Approved'),
        ('Escalation Rejected', 'Escalation Rejected'),
        ('Extension Pending', 'Extension Pending'),
        ('Extension Approved', 'Extension Approved'),
        ('Extension Rejected', 'Extension Rejected'),
        ('Overdue', 'Overdue'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    comment = models.CharField(max_length=100,null=True, blank=True)
    image = models.ImageField(upload_to='issues/', null=True, blank=True)  # Optional image
    reported_date = models.DateTimeField(auto_now_add=True)  # Date when the issue was reported
    assigned_dept = models.ForeignKey(Department,  null=True, blank=True,related_name='assigned_issues', on_delete=models.CASCADE)  
  

    def __str__(self):
        reporter_username = self.reporter.username if self.reporter else "No reporter"
        return f"{self.issue_category} - {reporter_username} - {self.issue_id}"
     # Add the adjusted_priority method here
   
    def adjusted_priority(self):
        age_in_days = (timezone.localtime(timezone.now()) - self.reported_date).days

        #age_in_days = (timezone.now() - self.reported_date).days
        adjusted_priority = self.priority

        if self.priority == 1:  # Low priority
            if age_in_days >10 :  # If unresolved for more than 15 days
                adjusted_priority = 2  # Promote to Medium
        
        elif self.priority == 2:  # Medium priority
            if age_in_days > 7:  # If unresolved for more than 7 days
                adjusted_priority = 3  # Promote to High
        
        # No adjustment needed for High priority (priority == 3)
        
        return adjusted_priority
    # Method to display priority as 'High', 'Medium', 'Low'
    def get_priority_display(self):
        return dict(self.PRIORITY_CHOICES).get(self.priority, 'Unknown')
    
    class Meta:
        ordering = ['-reported_date']  # Order by most recent issues


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    issue_id = models.ForeignKey(IssueDB, on_delete=models.CASCADE)  # Foreign key to Issue table
    assigned_dept = models.ForeignKey(Department, on_delete=models.CASCADE)  # Foreign key to Department table
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Foreign key to Worker table
    due_date = models.DateField()
    assigned_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"Task {self.task_id} for Issue {self.issue.issue_id}"
    def __str__(self):
        # Corrected the reference to `issue_id`
        return f"Task {self.task_id} for Issue {self.issue_id.issue_id}"
    


class Escalation(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)  # Link to Task
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to Worker
    reason = models.TextField()  # Reason for escalation
    status = models.CharField(max_length=20, choices=[
        ('Escalation Pending', 'Escalation Pending'),
        ('Escalation Approved', 'Escalation Approved'),
      
        ('Escalation Rejected', 'Escalation Rejected'),
    ], default='Extension Pending')  # Status of escalation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class ExtensionRequest(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)  # Link to Task
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to Worker
    new_due_date = models.DateField()  # Requested new due date
    reason = models.TextField()  # Reason for extension
    status = models.CharField(max_length=20, choices=[
        ('Extension Pending', 'Extension Pending'),
        ('Extension Approved', 'Extension Approved'),
        ('Extension Rejected', 'Extension Rejected'),
    ], default='Extension Pending')  # Status of extension
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

class TaskImage(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='task_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.task_id} - {self.image.url}"



class IssueStatusChange(models.Model):
    issue = models.ForeignKey(IssueDB, on_delete=models.CASCADE, related_name='status_changes')
    status = models.CharField(max_length=255)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Issue {self.issue.issue_id} - {self.status} on {self.changed_at}"
    

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)  # Auto-increment ID
    name = models.CharField(max_length=100, unique=True)  # Location name (e.g., "Library", "Lab A")
    # Choices for buildings and floors
    block = models.CharField(max_length=100, blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.name

    
# Asset type (e.g., Computer, Printer)
class Asset(models.Model):
    asset_id = models.AutoField(unique=True, primary_key=True)  # Unique ID for asset type
    asset_name = models.CharField(max_length=100)  # Name of the asset type (e.g., Computer)
   
    def __str__(self):
        return self.asset_name
    
# Individual asset instance (e.g., a specific computer, printer)
class AssetStock(models.Model):
    stock_id = models.AutoField(unique=True, primary_key=True)  # Unique ID for each individual asset
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)  # Asset type reference
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # ForeignKey to Location    prev_maintenance_date = models.DateField()  # Last maintenance date for this specific asset
    prev_maintenance_date = models.DateField(default=timezone.now)    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Maintenance Due', 'Maintenance Due'),
        ('Maintenance Scheduled', 'Maintenance Scheduled'),
    
    ]
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Active')  # Status of the asset
    purchase_date = models.DateField(default=timezone.now)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Cost of the asset
    maintenance_frequency = models.IntegerField(default=30)  # Frequency of maintenance (in days)
    maintenance_dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)  

    
    
    def __str__(self):
        return f'{self.asset.asset_name} ({self.stock_id})'
    





# Preventive maintenance schedule
class PreventiveMaintenanceSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True) # Primary Key
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="maintenance_schedules")
    stock = models.ForeignKey(AssetStock, on_delete=models.CASCADE, related_name="maintenance_schedules")
    assigned_dept = models.ForeignKey(Department,  null=True, blank=True,related_name='prev_issues', on_delete=models.CASCADE)
    worker = models.ForeignKey(CustomUser,null=True, blank=True,on_delete=models.CASCADE)  # Foreign key to Worker table
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Assigned to Foreman', 'Assigned to Foreman'),
        ('Assigned to Worker', 'Assigned to Worker'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    scheduled_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ['scheduled_date']
        verbose_name = "Preventive Maintenance Schedule"
        verbose_name_plural = "Preventive Maintenance Schedules"
    def __str__(self):
        return f"Schedule {self.schedule_id} - Asset {self.asset.asset_name} (Stock: {self.stock.stock_id}) - Status: {self.status}"



class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    issue_link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"


