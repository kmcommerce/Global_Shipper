

# Register your models here.
from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'service_type',
        'origin',
        'destination_country',
        'base_price',
        'shipping_time_days',
        'is_active',
    )

    list_filter = (
        'service_type',
        'origin',
        'destination_country',
        'is_active',
    )

    search_fields = ('name',)
