from django.contrib import admin
from django.utils.html import format_html
from .models import Company, CompanyData, CompanyUrls, BoardOfDirector
# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('logo_display', 'name', 'symbol', 'created_at', 'updated_at')
    search_fields = ['name','symbol']
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'logo')
        }),
        ('Contact Information', {
            'fields': ('address', 'contact_person', 'email', 'phone', 'symbol')
        }),
        ('Color Theme', {
            'fields': ('primary_color', 'secondary_color')
        })
    )
    readonly_fields = ['created_at', 'updated_at']

    def logo_display(self, obj):
        # Display a thumbnail of the logo in the list view
        if obj.logo:
            return format_html('<img src="{}" height="50" width="80" style="object-fit:cover;" />'.format(obj.logo.url))
        else:
            return ''
    logo_display.allow_tags = True
    logo_display.short_description = 'Logo'

class CompanyDataAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'last_scrapped_from', 'created_at', 'updated_at')
    search_fields = ['company_name', 'last_scrapped_from']
    list_filter = [ 'last_scrapped_from', 'created_at', 'updated_at']
    sortable_by = ['company_name', 'last_scrapped_from', 'created_at', 'updated_at']

class BoardOfDirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'designation')
    search_fields = ['name', 'company']
    

admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyUrls)
admin.site.register(CompanyData, CompanyDataAdmin)
admin.site.register(BoardOfDirector, BoardOfDirectorAdmin)