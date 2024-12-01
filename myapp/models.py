from django.db import models
from django.contrib.auth.models import AbstractUser

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
    issue_id = models.AutoField(primary_key=True)# Issue ID (Primary Key)
    CATEGORY_CHOICES = [
        ('Electrical Maintenance','Electrical Maintenance'),
        ('Plumbing Maintenance','Plumbing Maintenance'),
        ('HVAC (Heating, Ventilation, and Air Conditioning)','HVAC (Heating, Ventilation, and Air Conditioning)'),
        ('Building & Structural Maintenance','Building & Structural Maintenance'),
        ('Furniture Maintenance','Furniture Maintenance'),
        ('IT & Computer Equipment Maintenance','IT & Computer Equipment Maintenance'),
        ('Landscape & Groundskeeping','Landscape & Groundskeeping'),
        ('Others','Others')
    ]
    issue_category = models.CharField(max_length=255,choices=CATEGORY_CHOICES, default='Electrical Maintenance')# Issue category (e.g., Plumbing, Electrical, etc.)
    reported_dept_id = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)  # Automatically set from user
    # reported_dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='issues')# Reported department (ForeignKey to Department)
    reporter = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_issues') # Reporter (ForeignKey to User model)
    location = models.CharField(max_length=255)# Location of the issue (e.g., Building A, Room 101)
    issue_description = models.TextField() # Description of the issue
    # Priority of the issue (Low, Medium, High)
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    # Status of the issue (Pending, In Progress, Resolved)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    image = models.ImageField(upload_to='issues/', null=True, blank=True)# Optional image associated with the issue (e.g., a photo of the issue)
    reported_date = models.DateTimeField(auto_now_add=True) # Date when the issue was reported
    def __str__(self):
        reporter_username = self.reporter.username if self.reporter else "No reporter"
        return f"{self.issue_category} - {reporter_username} - {self.issue_id}"
        # return f"{self.issue_category} - {self.issue_id}"

    class Meta:
        ordering = ['-reported_date']  # Order by most recent issues

    
