from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Vehicle, Driver, Booking, Review, ServiceArea, FAQ, Contact

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'type', 'plate_number', 'seats', 'status')
    list_filter = ('type', 'status', 'brand')
    search_fields = ('brand', 'model', 'plate_number')
    ordering = ('brand', 'model')

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'experience_years', 'rating', 'is_available')
    list_filter = ('is_available', 'experience_years')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'license_number')
    ordering = ('-rating',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vehicle', 'driver', 'pickup_time', 'status', 'price')
    list_filter = ('status', 'pickup_time')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'pickup_location', 'destination')
    ordering = ('-pickup_time',)
    date_hierarchy = 'pickup_time'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('booking__user__username', 'comment')
    ordering = ('-created_at',)

@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')
    ordering = ('order', 'category')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def mark_as_processed(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_processed=True, processed_at=timezone.now())
    mark_as_processed.short_description = _("标记为已处理")

    actions = [mark_as_processed]
