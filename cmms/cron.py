from django.utils import timezone
from django.db import transaction

from myapp.models import AssetStock, PreventiveMaintenanceSchedule,CustomUser
def assign_maintenance_tasks():
    today = timezone.now().date()
    
    # Get assets that are due for maintenance
    assets_due_for_maintenance = AssetStock.objects.filter(
        prev_maintenance_date__lt=today,
        status='Active',  # Ensure the asset is active
    )

    with transaction.atomic():  # To ensure atomic updates
        for asset in assets_due_for_maintenance:
            next_maintenance_date = asset.prev_maintenance_date + timezone.timedelta(days=asset.maintenance_frequency)
            if today >= next_maintenance_date:
                try:
                    # Create preventive maintenance schedule
                    preventive_schedule = PreventiveMaintenanceSchedule.objects.create(
                        asset=asset.asset,
                        stock=asset,
                        assigned_dept=asset.maintenance_dept,
                        status='Assigned to Foreman'
                    )

                    # Assign worker
                    worker = CustomUser.objects.filter(department=asset.maintenance_dept).first()
                    if worker:
                        preventive_schedule.worker = worker
                        preventive_schedule.status = 'Assigned to Worker'
                        preventive_schedule.save()

                    # Update asset status and last maintenance date in a single update
                    asset.status = 'Maintenance Scheduled'
                    asset.prev_maintenance_date = today
                    asset.save()

                except Exception as e:
                    print(f"Error while assigning maintenance task for asset {asset.stock_id}: {e}")
