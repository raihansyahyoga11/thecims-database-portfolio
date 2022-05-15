from django.urls import path

from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user-dashboard/', views.user_dashboard, name='user-dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('warna-kulit/', views.warna_kulit, name='warna_kulit'),
    path('create-warna-kulit/', views.create_warna_kulit, name='create_warna_kulit'),
    path('level/', views.level, name='level'),
    path('create-level/', views.create_level, name='create_level'),
    path('update-level/', views.update_level, name='update_level'),
    path('menggunakan-apparel/', views.menggunakan_apparel, name='menggunakan_apparel'),
    path('create-menggunakan-apparel/', views.create_menggunakan_apparel, name='create_menggunakan_apparel')
]