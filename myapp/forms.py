# forms.py
from django import forms
from .models import CustomUser, Role, Department,IssueDB,Task

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # fields = ['username', 'first_name', 'last_name', 'password','email', 'role', 'department']
        fields = ['username', 'first_name', 'last_name','email', 'role', 'department']
        widgets = {
            'role': forms.Select(),
            'department': forms.Select(),
        }

class IssueForm(forms.ModelForm):
    class Meta:
        model = IssueDB
        # fields = ['issue_category', 'location', 'issue_description', 'priority', 'image']
        fields = ['issue_category', 'location', 'issue_description', 'priority', 'image']

class AssignIssueForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['worker', 'due_date']
        widgets = {
            'worker': forms.Select(),
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }
    def __init__(self, *args, **kwargs):
        # Get the department ID of the foreman (the logged-in user)
        dept_id = kwargs.pop('dept_id', None)  # Retrieve department ID passed via kwargs

        # Call the parent class constructor
        super().__init__(*args, **kwargs)

        # Filter workers by department if dept_id is available
        if dept_id:
            self.fields['worker'].queryset = CustomUser.objects.filter(department_id=dept_id,role_id=2)
            self.fields['worker'].label_from_instance = lambda obj: f'{obj.first_name} {obj.last_name}'  # Use custom worker's full name
            
class AssignDeptForm(forms.ModelForm):
    class Meta:
        model = IssueDB
        fields = ['assigned_dept']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Modify the queryset to show only some departments
        # Example: Only departments where the name starts with 'A'
        self.fields['assigned_dept'].queryset = Department.objects.filter(dept_id__range=(200, 300))

