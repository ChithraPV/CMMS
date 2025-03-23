# forms.py
from django import forms
from .models import CustomUser, Role, Department,IssueDB,Task,AssetStock,Asset,PreventiveMaintenanceSchedule,Location

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



class AssetStockForm(forms.ModelForm):
    class Meta:
        model = AssetStock
        fields = [
            'asset', 'location', 'prev_maintenance_date', 'status',
            'purchase_date', 'cost', 'maintenance_frequency','maintenance_dept'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepend 'Other' option to asset choices
        self.fields['asset'].queryset = Asset.objects.all()
        asset_choices = [('', 'Select Asset Type')] + [(asset.asset_id, asset.asset_name) for asset in self.fields['asset'].queryset] + [('other', 'Other')]
        self.fields['asset'].choices = asset_choices
        
        # Prepend 'Other' option to location choices
        self.fields['location'].queryset = Location.objects.all()
        location_choices = [('', 'Select Location')] + [(loc.location_id, loc.name) for loc in self.fields['location'].queryset] + [('other', 'Other')]
        self.fields['location'].choices = location_choices
        self.fields['maintenance_dept'].queryset = Department.objects.filter(dept_id__range=(200, 300))

    def clean(self):
        cleaned_data = super().clean()
        asset = cleaned_data.get('asset')
        location = cleaned_data.get('location')

        # Ensure asset and location are properly set
        if asset == 'other' and not cleaned_data.get('new_asset_name'):
            raise forms.ValidationError('Please provide a name for the new asset.')
        if location == 'other' and not cleaned_data.get('new_location_name'):
            raise forms.ValidationError('Please provide a name for the new location.')

        return cleaned_data

# class AssetStockForm(forms.ModelForm):
#     class Meta:
#         model = AssetStock
#         fields = ['asset', 'location', 'prev_maintenance_date', 'status', 'purchase_date', 'cost', 'warranty_expiry_date', 'maintenance_frequency']

#     # Adding a custom field for the new asset name
    

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Adding the 'Other' option dynamically to the asset choices
#         self.fields['asset'].queryset = Asset.objects.all()
#         self.fields['asset'].choices = [
#             ('', 'Select Asset Type'),
#             *[(asset.id, asset.asset_name) for asset in self.fields['asset'].queryset],
#             ('other', 'Other')  # Add 'Other' option to the dropdown
#         ]

#              # Set the queryset for the location field to include all existing locations
#         self.fields['location'].queryset = Location.objects.all()
#         self.fields['location'].choices = [
#             ('', 'Select Location'),
#             *[(location.id, location.location_name) for location in self.fields['location'].queryset],
#            ('other', 'Other')  # 'Other' option for location
#         ]

        
    
#     def clean(self):
#         cleaned_data = super().clean()
#         asset = cleaned_data.get('asset')
#         new_asset_name = cleaned_data.get('new_asset_name')

#         if asset == 'other' and new_asset_name:
#             # If 'Other' is selected and a new asset name is provided, create a new asset
#             asset, created = Asset.objects.get_or_create(asset_name=new_asset_name)
#             cleaned_data['asset'] = asset
#         elif asset == 'other' and not new_asset_name:
#             # If 'Other' is selected but no name is provided, raise an error
#             raise forms.ValidationError('Please provide a name for the new asset.')

#         return cleaned_data


class AssetForm(forms.ModelForm):
    class Meta:
        model = AssetStock
        fields = [
            'asset', 'location', 'prev_maintenance_date', 'status',
            'purchase_date', 'cost', 'maintenance_frequency','maintenance_dept'
        ]
        widgets = {
            'prev_maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=[('Active', 'Active'), ('Inactive', 'Inactive')]),
            'asset': forms.Select(),  # This will generate a dropdown for the Asset (the asset name)
        }




class Assign_prev_Form(forms.ModelForm):
    class Meta:
        model = PreventiveMaintenanceSchedule
        fields = ['worker',]
        widgets = {
            'worker': forms.Select()
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

    
        
class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Select an Excel File')