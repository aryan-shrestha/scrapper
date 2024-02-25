from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
from django.contrib.auth import get_user_model

from company.models import AGM, Company

# Create your models here.

class MyAccountManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        
        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)        
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # required 
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_company_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='users', related_query_name='users', verbose_name='groups')
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return self.is_active

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class WatchList(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    companies = models.ManyToManyField(Company, related_name='companies')

    def __str__(self):
        return f'{self.user.email}'
    

class UserAGMInteraction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    agm = models.ForeignKey(AGM, on_delete=models.CASCADE, null=True, blank=True)
    show_again = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.email} - {self.agm.title}'
    