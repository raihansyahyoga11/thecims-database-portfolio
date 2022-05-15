from cgitb import html
from django.urls import path

from . import views

app_name = 'frontend'

urlpatterns = [

    #authentication
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    #home
    path('user-dashboard/', views.user_dashboard, name='user-dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),

    #misi utama
    path('misi-utama/', views.read_misi_utama, name='read_misi_utama'),
    path('detail-misi-utama/',views.detail_misi_utama,name='detail_misi_utama'),
    path('create-misi-utama/',views.create_misi_utama,name='create_misi_utama'),

    # menjalankan misi utama
    path('menjalankan-misi-utama/',views.read_menjalankan_misi_utama, name='read_menjalankan_misi_utama'),
    path('create-menjalankan-misi-utama/',views.create_menjalankan_misi_utama, name='create_menjalankan_misi_utama'),
    path('update-menjalankan-misi-utama/', views.ubah_menjalankan_misi_utama, name='ubah_menjalankan_misi_utama'),

    # makanan
    path('makanan/',views.read_makanan, name='read_makanan'),
    path('create-makanan/',views.create_makanan, name='create_makanan'),
    path('update-makanan/',views.ubah_makanan, name='create_makanan'),


    # makan 
    path('makan/',views.create_makanan, name='read_amakan'),
    path('create-makan/', views.create_makan, name='create_makan')
]