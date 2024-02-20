from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('', views.company_list, name='company_list'),
    path('create/', views.company_create, name='company_create'),
    path('update/<int:company_id>/', views.company_update, name='company_update'),
    path('delete/<int:company_id>/', views.company_delete, name='company_delete'),
    path('company_url_update/<int:company_url_id>/', views.update_company_url, name='update_company_url'),
    path('bod/create/', views.board_of_director_create, name='board_of_director_create'),
    path('bod/update/<int:bod_id>/', views.board_of_director_update, name='board_of_director_update'),
    path('bod/delete/<int:bod_id>/', views.board_of_director_delete, name='board_of_director_delete'),
    path('category/list', views.category_list, name='category_list'),
    path('category/create', views.category_create, name='category_create'),
    path('category/update/<int:category_id>/', views.category_update, name='category_update'),
    path('category/delete/<int:category_id>/', views.category_delete, name='category_delete'),
    path('floorsheet/list', views.floorsheet_list, name='floorsheet_list'),
    path('floorsheet/create', views.floorsheet_create, name='floorsheet_create'),
    path('floorsheet/update/<int:floorsheet_id>/', views.floorsheet_update, name='floorsheet_update'),
    path('floorsheet/delete/<int:floorsheet_id>/', views.floorsheet_delete, name='floorsheet_delete'),
    path('market/today/', views.today_market, name='today_market'),
    path('chart/data/<int:company_id>/', views.company_data_chart, name='company_data_chart'),
]