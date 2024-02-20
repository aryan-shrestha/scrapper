from django.urls import path
from . import views

app_name = 'scrapper'

urlpatterns = [
    path('detail/', views.company_detail, name='company_detail'),
    path('detail/admin/<int:company_id>/', views.company_detail_admin, name='company_detail_admin'),
    path('nepse/<int:company_id>/', views.scrap_from_nepse, name='scrap_from_nepse'),
    path('merolagani/<int:company_id>/', views.scrap_from_mero_lagani, name='scrap_from_mero_lagani'),
    path('sharesansar/<int:company_id>/', views.scrap_from_share_sansar, name='scrap_from_share_sansar'),
]