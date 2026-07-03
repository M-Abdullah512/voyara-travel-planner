from django.contrib import admin
from .models import Package, Booking


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display  = ['name', 'country', 'region', 'price_pkr',
                     'price_usd', 'duration_days', 'is_featured']
    list_filter   = ['region', 'is_featured']
    search_fields = ['name', 'country']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['full_name', 'email', 'phone', 'package',
                     'num_passengers', 'total_price_pkr', 'status', 'booked_at']
    list_filter   = ['status', 'package']
    search_fields = ['full_name', 'email', 'phone']