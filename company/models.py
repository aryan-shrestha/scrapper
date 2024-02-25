import os
from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
def rename_image(instance, filename):
    new_filename = f'{instance.name}/{filename}'
    return os.path.join('company/logo/', new_filename)

class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Company(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(null=True, upload_to='company/logo/', blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    symbol = models.CharField(max_length=255, null=True, blank=True)
    primary_color = models.CharField(max_length=255, null=True, blank=True)
    secondary_color = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['name', 'created_at', 'symbol'])]
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name
    
class BoardOfDirector(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='board_of_director', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='company/bod/')
    designation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.company.name} - {self.name}'
    
class CompanyUrls(models.Model):
    company = models.OneToOneField(Company, null=True, blank=True, on_delete=models.CASCADE, related_name='urls')
    nepse_url = models.CharField(max_length=255, null=True, blank=True)
    mero_lagani_url = models.CharField(max_length=255, null=True, blank=True)
    share_sansar_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.company.name
    
    class Meta:
        verbose_name = 'Company Url'
        verbose_name_plural = 'Company Urls'

class CompanyData(models.Model):
    last_scrapped_from = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE, related_name='company_data')
    last_traded_price = models.CharField(max_length=255, null=True, blank=True)
    total_traded_quantity = models.CharField(max_length=255, null=True, blank=True)
    total_trades = models.CharField(max_length=255, null=True, blank=True)
    previous_day_close_price = models.CharField(max_length=255, null=True, blank=True)
    high_price_low_price = models.CharField(max_length=255, null=True, blank=True)
    week_high_week_low = models.CharField(max_length=255, null=True, blank=True)
    open_price = models.CharField(max_length=255, null=True, blank=True)
    close_price = models.CharField(max_length=255, null=True, blank=True)
    total_listed_shares = models.CharField(max_length=255, null=True, blank=True)
    total_paid_up_value = models.CharField(max_length=255, null=True, blank=True)
    market_capitalization = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.company.name}'
    
    @property
    def company_name(self):
        return f'{self.company.name}'
    
    class Meta:
        verbose_name = 'Company Data'
        verbose_name_plural = 'Company Data'

class Floorsheet(models.Model):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    buyer = models.CharField(max_length=255, null=True, blank=True)
    seller = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    rate = models.CharField(max_length=255, null=True, blank=True)
    amount = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.company.name}'
    
class News(models.Model):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='company/files/')

    def __str__(self):
        return f'{self.company.name}'

class AGM(models.Model):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    file = models.FileField(max_length=255, upload_to='company/agm/', null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.slug = f"{self.slug}-{timestamp}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.company.name}'
