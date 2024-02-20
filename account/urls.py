from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.loginView, name='login_view'),
    path('create/', views.user_create_view, name='user_create'),
    path('user_list/', views.user_list, name='user_list'),
    path('update/<int:user_id>/', views.user_update, name='user_update'),
    path('delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('logout/', views.logout_view, name='logout_view'),
    path('group/list/', views.group_list, name='group_list'),
    path('group/create/', views.group_create, name='group_create'),
    path('group/update/<int:group_id>/', views.group_update, name='group_update'),
    path('group/delete/<int:group_id>/', views.group_delete, name='group_delete'),
]