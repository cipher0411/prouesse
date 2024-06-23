from django.contrib import admin
from .models import Profile, otp_Profile
from django.contrib.admin import AdminSite
from .models import Contact





class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'postcode', 'country')
    search_fields = ('user__username', 'address', 'city', 'postcode', 'country')
    list_filter = ('country', 'city')


class SafeSite(AdminSite):
    site_header = 'Safe Admin Site'
    site_title = 'Safe Admin Site'
    index_title = 'Dashboard'
    
safe_site = SafeSite(name='safe')

class StaffSite(AdminSite):
    site_header = 'Staff Admin Site'
    site_title = 'Staff Admin Site'
    index_title = 'Dashboard'
    
staff_site = StaffSite(name='staff')




admin.site.register(Profile, ProfileAdmin)


@admin.register(otp_Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp')




@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'service', 'submitted_at')
    search_fields = ('name', 'email', 'service')
    list_filter = ('service', 'submitted_at')