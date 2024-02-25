from django.contrib import admin
from import_export import resources, fields

from company.models import Company, CompanyData

# Register your models here.

class CompanyDataResource(resources.ModelResource):
    source = fields.Field(attribute='last_scrapped_from', column_name='Source')
    company = fields.Field(attribute='company__name', column_name='Company')
    symbol = fields.Field(attribute='company__symbol', column_name='symbol')
    ltp = fields.Field(attribute='last_traded_price', column_name='LTP')

    class Meta:
        model = CompanyData
        fields = ('company', 'symbol','ltp', 'source')

class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company
        fields = ('name', 'address', 'contact_person', 'email', 'phone', 'symbol', 'category__name')



