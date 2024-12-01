# forms.py
from django import forms
from .models import CustomUser, Role, Department,IssueDB

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password','email', 'role', 'department']
        widgets = {
            'role': forms.Select(),
            'department': forms.Select(),
        }

class IssueForm(forms.ModelForm):
    class Meta:
        model = IssueDB
        fields = ['issue_category', 'location', 'issue_description', 'priority', 'image']



