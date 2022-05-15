from cgitb import html
from django.urls import path

from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user-dashboard/', views.user_dashboard, name='user-dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('misi-utama/', views.read_misi_utama, name='read_misi_utama'),
    path('detail-misi-utama/',views.detail_misi_utama,name='detail_misi_utama'),
    path('create-misi-utama/',views.create_misi_utama,name='create_misi_utama')
    
]