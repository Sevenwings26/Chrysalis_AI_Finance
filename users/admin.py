from django.contrib import admin
from .models import CustomUser

admin.site.site_header = "Chrysalis Admin"
admin.site.site_title = "Chrysalis Investment Portal"
admin.site.index_title = "Welcome to the Chrysalis Management Area"


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    # Columns to show in the list
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    
    # Clickable links
    list_display_links = ('email', 'first_name')
    
    # Sidebar filters
    list_filter = ('is_staff', 'is_active', 'date_joined')
    
    # Search bar (crucial for finding users quickly)
    search_fields = ('email', 'first_name', 'last_name')
    
    # Order by newest first
    ordering = ('-date_joined',)
    
