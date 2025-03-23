# path('asset-management/activeassets/',views.activeassets,name='activeassets'),
    # path('asset-management/inactiveassets/',views.inactiveassets,name='inactiveassets'),
    # path('asset-management/maintenance_due/',views.maintenance_due,name='maintenance_due'),
    # path('asset-management/maintenance_due/asset_assign',views.asset_assign,name='asset_assign'),
    # path('asset-management/maintenance_due/prev_schedules_admin',views.prev_schedules_admin,name='prev_schedules_admin'),
    # path('asset-management/bulk_upload_assets',views.bulk_upload_assets,name='bulk_upload_assets'),
    # path('asset-management/bulk_upload_stocks',views.bulk_upload_stocks,name='bulk_upload_stocks'),
    # path('asset-management/preventive_foreman',views.preventive_foreman,name='preventive_foreman'),
    # path('asset-management/<int:pk>/foreman_prev_assign/',views.foreman_prev_assign,name='foreman_prev_assign'),
    # path('prev_task_worker/',views.prev_task_worker,name='prev_task_worker'),
    # path('prev_task_worker/<int:pk>/prev_details/',views.prev_details,name='prev_details'),
    # path('asset_management/edit_asset/<str:stock_id>/', views.edit_asset, name='edit_asset'),
    # path('asset_management/delete_asset/<str:stock_id>/', views.delete_asset, name='delete_asset'),






























def asset_management(request):
    assets = AssetStock.objects.all()  # Fetch all users from the custom model
    # return render(request, 'asset_management.html', {'assets': assets})
    next_due_dates = []

    # Calculate the next maintenance date for each asset
    for i in assets:
        # Calculate the next maintenance date
        due_date = i.prev_maintenance_date + timedelta(days=i.asset.maintenance_frequency)
        
        # Append the calculated due date to the list
        next_due_dates.append(due_date)

    # Optional: Flag variable (set to 0 for now)
    flag = 0  

    return render(request, 'asset_management.html', {
    'assets_with_due_dates': zip(assets, next_due_dates),
    'flag': flag
})


from django.shortcuts import render, redirect
from .forms import Asset, AssetForm  # Assuming AssetForm is already defined.

def add_asset_and_stock(request):
    if request.method == 'POST':
        # Handle Add Asset Form
        asset_form = Assetaddform(request.POST)
        stock_form = AssetForm(request.POST)

        if 'add_asset' in request.POST and asset_form.is_valid():  # Checking which form is being submitted
            asset_form.save()
            return redirect('asset_management')

        if 'add_stock' in request.POST and stock_form.is_valid():  # Checking which form is being submitted
            stock_form.save()
            return redirect('asset_management')
    else:
        asset_form = Assetaddform()
        stock_form = AssetForm()
    
    return render(request, 'add_asset.html', {'form_asset': asset_form, 'form_stock': stock_form})





from datetime import timedelta

def activeassets(request):     
    # Get all assets with status 'Active'
    assets = AssetStock.objects.filter(status='Active')  
    
    # List to store the next maintenance due dates
    next_due_dates = []

    # Calculate the next maintenance date for each asset
    for i in assets:
        # Calculate the next maintenance date
        due_date = i.prev_maintenance_date + timedelta(days=i.asset.maintenance_frequency)
        
        # Append the calculated due date to the list
        next_due_dates.append(due_date)

    # Optional: Flag variable (set to 0 for now)
    flag = 0  

    # Render the data to the template
    return render(request, 'asset_management.html', {
    'assets_with_due_dates': zip(assets, next_due_dates),
    'flag': flag
})

def inactiveassets(request):     
    assets = AssetStock.objects.filter(status='Inactive') 
    next_due_dates = []

    # Calculate the next maintenance date for each asset
    for i in assets:
        # Calculate the next maintenance date
        due_date = i.prev_maintenance_date + timedelta(days=i.asset.maintenance_frequency)
        
        # Append the calculated due date to the list
        next_due_dates.append(due_date)
    flag = 0 # Fetch all users from the custom model
    return render(request, 'asset_management.html', {'assets': assets,'flag':flag})




from datetime import timedelta, date

def maintenance_due(request):
    assets = AssetStock.objects.all()  # Fetch all assets from the model
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
    category_data = []
    category_labels = []
    for category_key, category_label in CATEGORY_CHOICES:
        category_labels.append(category_label)
    today = date.today()
    due_assets = [] 
    assets_with_due_dates = []  # Store tuples of asset and its due date
    flag = 0  # Initialize flag

    # Calculate the next maintenance date for each asset
    for i in assets:
        due_date = i.prev_maintenance_date + timedelta(days=i.asset.maintenance_frequency)
        
        # Check if the maintenance is due within a 7-day grace period
        if due_date - timedelta(days=7) <= today:
            due_assets.append(i)  # Add asset to the due list
            assets_with_due_dates.append((i, due_date))  # Pair asset and due date
            flag = 1

    return render(request, 'asset_management.html', {
        'assets_with_due_dates': assets_with_due_dates,  # Pass filtered assets with dates
        'flag': flag,
        'department': category_labels,
    })

def asset_assign(request):
    if request.method == 'POST':
        stock_id = request.POST.get('asset_id')
        department = request.POST.get('department')
          # Validate and fetch related objects
        stock = get_object_or_404(AssetStock, stock_id=stock_id)
        category_to_dept_map = {
                'Electrical Maintenance': 'ELECTRONICS',
                'Plumbing Maintenance': 'Plumbing Department',
                'HVAC': 'HVAC Department',
                'Building Maintenance': 'Building Department',
                'Furniture Maintenance': 'CARPENTRY',
                'IT & Computer Equipment Maintenance': 'IT Department',
                'Landscape & Groundskeeping': 'Groundskeeping Department',
            }
        department_name = category_to_dept_map.get(department)
        if department_name:
            department = Department.objects.get(dept_name=department_name)
        preventive_schedule = PreventiveMaintenanceSchedule.objects.create(
                asset=stock.asset,
                stock=stock,
                assigned_dept=department,
                status='Assigned to Foreman'
            )
        messages.success(request, "Asset assigned successfully!")
        return redirect('asset_management')
    return render(request, 'asset_management.html')

        
def prev_schedules_admin(request):
    schedules = PreventiveMaintenanceSchedule.objects.all()
    schedule_data = []
    for schedule in schedules:
        # Calculate due date based on stock and asset maintenance frequency
        due_date = schedule.stock.prev_maintenance_date + timedelta(days=schedule.asset.maintenance_frequency)
        schedule_data.append({
            'schedule': schedule,
            'due_date': due_date,
        })

    return render(request, 'prev_schedules_admin.html', {'schedule_data': schedule_data})

# def bulk_upload_assets(request):
#     if request.method == 'POST' and request.FILES.get('excelFile'):
#         excel_file = request.FILES['excelFile']

       
#             # Read the Excel file
#         data = pd.read_excel(excel_file)

#             # Validate required columns
#         required_columns = ['asset_id', 'asset_name', 'maintenance_frequency']
#         for column in required_columns:
#                 if column not in data.columns:
#                     messages.error(request, f'Missing required column: {column}')
#                     return redirect('bulk_upload_users')

#         for _, row in data.iterrows():
#                 asset = Asset.objects.create(
#                            asset_id=row['asset_id'],
#                            asset_name=row['asset_name'],
#                             maintenance_frequency=row['maintenance_frequency'],
              
#         )

#         # Set the password (hashed password)
#                 asset.save()
#                 print(f"Asset {asset.asset_name} created successfully")
#         return render(request, 'add_asset.html')  # Fallback if GET request



from django.contrib import messages
from django.shortcuts import render, redirect
import pandas as pd
from .models import Asset

def bulk_upload_assets(request):
    if request.method == 'POST' and request.FILES.get('excelFile'):
        excel_file = request.FILES['excelFile']
        
        try:
            # Read the Excel file
            data = pd.read_excel(excel_file)
            
            # Validate required columns
            required_columns = ['asset_id', 'asset_name', 'maintenance_frequency']
            for column in required_columns:
                if column not in data.columns:
                    messages.error(request, f'Missing required column: {column}')
                    return redirect('bulk_upload_assets')  # The correct URL to return for error handling

            # Create asset objects from the Excel rows
            for _, row in data.iterrows():
                asset = Asset.objects.create(
                    asset_id=row['asset_id'],
                    asset_name=row['asset_name'],
                    maintenance_frequency=row['maintenance_frequency'],
                )
                asset.save()
                print(f"Asset {asset.asset_name} created successfully")
            
            # Show a success message
            messages.success(request, 'Assets uploaded successfully!')
            return redirect('add_asset_and_stock')  # Redirect to an asset list or another view after success

        except Exception as e:
            # If any exception occurs during file processing, show an error message
            messages.error(request, f"Error processing the file: {str(e)}")
            return redirect('bulk_upload_assets')  # The correct URL to return on error
    else:
        asset_form = Asset()
        stock_form = AssetForm()
    
        return render(request, 'add_asset.html', {'form_asset': asset_form, 'form_stock': stock_form})

        
# def bulk_upload_stocks(request):
#     if request.method == 'POST' and request.FILES.get('excelFile'):
#         excel_file = request.FILES['excelFile']
        
#         try:
#             # Read the Excel file
#             data = pd.read_excel(excel_file)
            
#             # Validate required columns
#             required_columns = ['stock_id', 'asset_id', 'location','prev_maintenance_date','status']
#             for column in required_columns:
#                 if column not in data.columns:
#                     messages.error(request, f'Missing required column: {column}')
#                     return redirect('bulk_upload_assets')  # The correct URL to return for error handling

#             # Create asset objects from the Excel rows
#             for _, row in data.iterrows():
#                 assetstock = AssetStock.objects.create(
#                     stock_id=row['stock_id'],
#                     asset_id=row['asset_id'],
#                     location=row['location'],
#                     prev_maintenance_date=row['prev_maintenance_date'],
#                     status=row['status'],
#                 )
#                 assetstock.save()
#                 print(f"Asset {assetstock.stock_id} created successfully")
            
#             # Show a success message
#             messages.success(request, 'Stocks uploaded successfully!')
#             return redirect('add_asset')  # Redirect to an asset list or another view after success

#         except Exception as e:
#             # If any exception occurs during file processing, show an error message
#             messages.error(request, f"Error processing the file: {str(e)}")
#             return redirect('bulk_upload_stocks')  # The correct URL to return on error
#     else:
#         asset_form = Asset()
#         stock_form = AssetForm()
    
#         return render(request, 'add_asset.html', {'form_asset': asset_form, 'form_stock': stock_form})


from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from .models import AssetStock, Asset

# def bulk_upload_stocks(request):
#     if request.method == 'POST' and request.FILES.get('excelFile'):
#         excel_file = request.FILES['excelFile']
        
#         try:
#             # Read the Excel file
#             data = pd.read_excel(excel_file)

#             # Validate required columns
#             required_columns = ['stock_id', 'asset_id','asset_name', 'location', 'prev_maintenance_date', 'status']
#             missing_columns = [col for col in required_columns if col not in data.columns]
#             if missing_columns:
#                 messages.error(request, f'Missing required columns: {", ".join(missing_columns)}')
#                 return redirect('bulk_upload_stocks')

#             # Create a list to hold validated AssetStock objects
#             stock_objects = []
#             for _, row in data.iterrows():
#                 try:
#                     # Check if the Asset exists
#                     if not AssetStock.objects.filter(pk=row['asset_id']).exists():
#                         messages.warning(request, f"Asset ID {row['asset_id']} not found. Skipping row.")
#                         continue

#                     # Check for duplicates in stock_id
#                     if AssetStock.objects.filter(stock_id=row['stock_id']).exists():
#                         messages.warning(request, f"Stock ID {row['stock_id']} already exists. Skipping row.")
#                         continue

#                     # Create the AssetStock object
#                     stock_objects.append(
#                         AssetStock(
#                             stock_id=row['stock_id'],
#                             asset_id=Asset.objects.get(pk=row['asset_id']),
#                             location=row['location'],
#                             prev_maintenance_date=pd.to_datetime(row['prev_maintenance_date'], errors='coerce'),
#                             status=row['status']
#                         )
#                     )
#                 except Exception as row_error:
#                     messages.error(request, f"Error processing row {row}: {str(row_error)}")

#             # Bulk create all valid objects
#             AssetStock.objects.bulk_create(stock_objects)

#             # Show success message
#             messages.success(request, f'Successfully uploaded {len(stock_objects)} stock items!')
#             return redirect('add_asset_and_stock')

#         except Exception as e:
#             # Handle general exceptions
#             messages.error(request, f"Error processing the file: {str(e)}")
#             return redirect('bulk_upload_stocks')

#     else:
#         # Handle GET requests
#         asset_form = Asset()
#         stock_form = AssetForm()
#         return render(request, 'add_asset.html', {'form_asset': asset_form, 'form_stock': stock_form})

# def bulk_upload_stocks(request):
#     if request.method == 'POST' and request.FILES.get('excelFile'):
#         excel_file = request.FILES['excelFile']

#         try:
#             # Read the Excel file
#             data = pd.read_excel(excel_file)

#             # Validate required columns
#             required_columns = ['stock_id', 'asset_id', 'location', 'prev_maintenance_date', 'status']
#             for column in required_columns:
#                 if column not in data.columns:
#                     messages.error(request, f'Missing required column: {column}')
#                     return redirect('bulk_upload_stocks')

#             for _, row in data.iterrows():
#                 try:
#         # Generate a random password
                 

#         # Retrieve the Role instance based on the name in the Excel file
#                   asset_instance = Asset.objects.get(asset_id=row['asset_id'])
#                   stock = AssetStock.objects.create(
#                 stock_id=row['stock_id'],
#                 asset=asset_instance,
#                 location=row['location'],
#                 prev_maintenance_date=row['prev_maintenance_date'],
#                 status=row['status'],
#                 )

#         # Create the user, assigning the role instance
               

#         # Set the password (hashed password)
#                   stock.save()
#                   print(f"Stock {stock.stock_id} created successfully")
#                 except Asset.DoesNotExist:
#                   print(f"Error: Asset '{row['asset_id']}' does not exist. Please add it to the database.")
                
#         except Exception as e:
#          print(f"An error occurred while creating the stock: {e}")

# #     return render(request, 'add_asset.html')
# def bulk_upload_stocks(request):
#     if request.method == 'POST' and request.FILES.get('excelFile'):
#         excel_file = request.FILES['excelFile']

#         try:
#             # Read the Excel file
#             data = pd.read_excel(excel_file)

#             # Validate required columns
#             required_columns = ['stock_id', 'asset_id', 'location', 'prev_maintenance_date', 'status']
#             for column in required_columns:
#                 if column not in data.columns:
#                     messages.error(request, f'Missing required column: {column}')
#                     return redirect('bulk_upload_stocks')

#             for _, row in data.iterrows():
#                 try:
#                     # Ensure asset_id refers to an existing Asset instance
#                     asset_instance = Asset.objects.get(asset_name=row['asset'].asset_name)
                    
#                     # Create the AssetStock instance, referencing the related Asset instance
#                     stock = AssetStock.objects.create(
#                         stock_id=row['stock_id'],
#                         asset=asset_instance,  # Foreign key relationship (asset_id is linked to asset)
#                         location=row['location'],
#                         prev_maintenance_date=row['prev_maintenance_date'],
#                         status=row['status'],
#                     )

#                     stock.save()
#                     print(f"Stock {stock.stock_id} created successfully")

#                 except Asset.DoesNotExist:
#                     # Handle the case where the Asset does not exist
#                     print(f"Error: Asset with asset_id '{row['asset_id']}' does not exist. Please add it to the database.")

#         except Exception as e:
#             print(f"An error occurred while processing the file: {e}")

#     return render(request, 'add_asset.html')




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Asset, AssetStock  # Replace with your app's import path
import pandas as pd
from datetime import datetime

def bulk_upload_stocks2(request):
    if request.method == 'POST' and request.FILES.get('excelFile'):
        excel_file = request.FILES['excelFile']

        try:
            # Read the Excel file
            data = pd.read_excel(excel_file)
            required_columns = ['stock_id', 'asset_id', 'location', 'prev_maintenance_date', 'status', 'asset_name', 'maintenance_frequency']
            for column in required_columns:
                if column not in data.columns:
                    messages.error(request, f'Missing required column: {column}')
                    return redirect('bulk_upload_stocks')

            for _, row in data.iterrows():
                try:
        

        # Retrieve the Role instance based on the name in the Excel file
                 
                  stock = AssetStock.objects.create(
                        stock_id=row['stock_id'],
                        asset_id = row['asset_id'],
                        asset_name = row['asset_name'],   # Foreign key relationship (asset_id is linked to asset)
                        location=row['location'],
                        maintenance_frequency=row['maintenance_frequency'],
                        prev_maintenance_date=row['prev_maintenance_date'],
                        status=row['status'],
                     )
                  

        # Create the user, assigning the role instance
                  

        # Set the password (hashed password)
                 
                  stock.save()
                
                except Asset.DoesNotExist:
                    print(f"Error: Role '{row['asset_id']}' does not exist. Please add it to the database.")
        except Exception as e:
         print(f"An error occurred while creating the stock: {e}")


            # Validate required columns
            

    return render(request, 'add_asset.html')

def bulk_upload_stocks(request):
    if request.method == 'POST' and request.FILES.get('excelFile'):
        excel_file = request.FILES['excelFile']

        try:
            # Read the Excel file
            data = pd.read_excel(excel_file)

            # Validate required columns
            required_columns = ['stock_id', 'asset_name', 'maintenance_frequency', 'location', 'prev_maintenance_date', 'status']
            for column in required_columns:
                if column not in data.columns:
                    messages.error(request, f"Missing required column: {column}")
                    return redirect('bulk_upload_stocks')

            for _, row in data.iterrows():
                try:
                    # Get or create the Asset instance
                    asset, created = Asset.objects.get_or_create(
                        asset_name=row['asset_name'],
                        defaults={
                            'asset_id': row['asset_id'],  # Assuming asset_id is also in the file
                            'maintenance_frequency': row['maintenance_frequency'],
                        },
                    )
                    if created:
                        print(f"Created new Asset: {asset.asset_name}")

                    # Ensure `prev_maintenance_date` is in the correct format
                    prev_maintenance_date = row['prev_maintenance_date']
                    if isinstance(prev_maintenance_date, pd.Timestamp):
                        prev_maintenance_date = prev_maintenance_date.date()
                    elif isinstance(prev_maintenance_date, str):
                        prev_maintenance_date = datetime.strptime(prev_maintenance_date, "%Y-%m-%d").date()

                    # Create or update AssetStock instance
                    stock, stock_created = AssetStock.objects.update_or_create(
                        stock_id=row['stock_id'],
                        defaults={
                            'asset': asset,  # Reference the asset instance
                            'location': row['location'],
                            'prev_maintenance_date': prev_maintenance_date,
                            'status': row['status'],
                        },
                    )
                    if stock_created:
                        print(f"Created new AssetStock: {stock.stock_id}")
                    else:
                        print(f"Updated AssetStock: {stock.stock_id}")

                except Exception as e:
                    print(f"Error processing row {row['stock_id']}: {e}")
                    messages.error(request, f"Error processing row {row['stock_id']}: {e}")

            messages.success(request, "File processed successfully!")

        except Exception as e:
            print(f"Error reading file: {e}")
            messages.error(request, f"An error occurred while processing the file: {e}")

    return render(request, 'add_asset.html')


def preventive_foreman(request):
    # schedules = PreventiveMaintenanceSchedule.objects.filter(assigned_dept=request.user.department)
    # return render(request, 'prev_schedules_foreman.html', {'schedules': schedules})
    schedules = PreventiveMaintenanceSchedule.objects.all()

    # Prepare schedule data with due dates
    schedule_data = []
    for schedule in schedules:
        # Calculate due date based on stock and asset maintenance frequency
        due_date = schedule.stock.prev_maintenance_date + timedelta(days=schedule.asset.maintenance_frequency)
        schedule_data.append({
            'schedule': schedule,
            'due_date': due_date,
        })

    return render(request, 'prev_schedules_foreman.html', {'schedule_data': schedule_data})


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from myapp.models import PreventiveMaintenanceSchedule  # Ensure correct import

def foreman_prev_assign(request, pk):
    foreman = request.user  # Assuming the logged-in user is the foreman
    dept_id = foreman.department_id  # Ensure 'dept_id' is available
    assets = AssetStock.objects.all()  # Fetch all assets from the model
    for i in assets:
        due_date = i.prev_maintenance_date + timedelta(days=i.asset.maintenance_frequency)
    # Retrieve the specific schedule instance
    schedule = get_object_or_404(PreventiveMaintenanceSchedule, pk=pk)
    
    if request.method == 'POST':
        # Pass dept_id for filtering workers
        form = Assign_prev_Form(request.POST, dept_id=dept_id)
        if form.is_valid():
            # Save the form and update schedule status
            worker = form.cleaned_data['worker']
            schedule.worker = worker
            schedule.status = 'Assigned to Worker'  # Replace with your status constant if defined
            schedule.save()

            messages.success(request, 'Work assigned successfully!')
            return redirect('preventive_foreman')  # Redirect to the desired page
    else:
        # Instantiate the form with dynamic worker options
        form = Assign_prev_Form(dept_id=dept_id)

    return render(request, 'prev_assign-foreman.html', {'form': form, 'schedule': schedule})


def prev_task_worker(request):
    worker = request.user
    schedules = PreventiveMaintenanceSchedule.objects.filter(worker_id=worker)
    schedule_data = []
    for schedule in schedules:
        # Calculate due date based on stock and asset maintenance frequency
        due_date = schedule.stock.prev_maintenance_date + timedelta(days=schedule.asset.maintenance_frequency)
        schedule_data.append({
            'schedule': schedule,
            'due_date': due_date,
        })

    return render(request, 'prev_task_worker.html', {'schedule_data': schedule_data})


# def prev_details(request,pk):
#     schedules = PreventiveMaintenanceSchedule.objects.filter(schedule_id=pk)
#     schedule_data = []
#     for schedule in schedules:
#         # Calculate due date based on stock and asset maintenance frequency
#         due_date = schedule.stock.prev_maintenance_date + timedelta(days=schedule.asset.maintenance_frequency)
#         asset = AssetStock.objects.filter(stock_id=schedule.stock_id).first()
#         schedule_data.append({
#             'schedule': schedule,
#             'due_date': due_date,
#             'asset': asset,
#         })
    
#     return render(request, 'prev_task_details.html',{'schedule_data':schedule_data})
    
from datetime import timedelta
from django.shortcuts import render, get_object_or_404

def prev_details(request, pk):
    schedules = PreventiveMaintenanceSchedule.objects.filter(schedule_id=pk).select_related('stock', 'asset')
    schedule_data = []

    for schedule in schedules:
        # Calculate the due date
        due_date = schedule.stock.prev_maintenance_date + timedelta(days=schedule.asset.maintenance_frequency)
        
        # Add data to the schedule_data list
        schedule_data.append({
            'schedule': schedule,
            'due_date': due_date,
            'asset': schedule.stock,  # Directly use the stock relation
        })

    return render(request, 'prev_task_details.html', {'schedule_data': schedule_data})

def update_status_prev(request, pk):
    if request.method == 'POST':
        # Fetch the issue only once to reduce overhead
        schedule = get_object_or_404(PreventiveMaintenanceSchedule, pk=pk)
        status_updated = False  # Track if status was updated
        stock_id = schedule.stock_id

        # Update task status if provided
        new_status = request.POST.get('status')
        if new_status:
            schedule.status = new_status
            schedule.save()
            status_updated = True
        if new_status =="Resolved":
            schedule.completed_date = datetime.now()
            schedule.save()
            status_updated = True
            #asset_stock = AssetStock.objects.filter(stock_id=schedule.stock_id)
            # asset_stock= get_object_or_404(AssetStock, stock_id=stock_id)
            # asset_stock.prev_maintenance_date = datetime.now()
            # asset_stock.save()
            asset_stock = AssetStock.objects.filter(id=stock_id).first()
            if asset_stock:
              asset_stock.prev_maintenance_date = datetime.now()
              asset_stock.save()
            else:
              messages.error(request, f"No AssetStock found with stock_id: {stock_id}.")




        # Feedback messages for status and comment updates
        if status_updated:
            messages.success(request, "Status updated successfully.")
       

        # If no valid inputs, show error
        if not (new_status  or 'image' in request.FILES):
            messages.error(request, "No changes detected. Please provide status, comment, or image.")

        return redirect('prev_details',pk=pk)

    # Optional: Handle GET request fallback
    messages.error(request, "Invalid request method.")
    return redirect('prev_details',pk=pk)


def edit_asset(request,stock_id):
    
    asset = get_object_or_404(AssetStock, stock_id=stock_id)  # Fetch the asset using the provided stock_id

    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, "Asset updated successfully!")
            return redirect('asset_management')
    else:
        form = AssetForm(instance=asset)

    # Provide asset details to populate the modal
    return render(request, 'edit_asset.html', {'form_stock': form, 'asset': asset})


def delete_asset(request, stock_id):
    asset = get_object_or_404(AssetStock, stock_id=stock_id)
    asset.delete()
    messages.success(request, "Asset deleted successfully!")
    return redirect('asset_management')