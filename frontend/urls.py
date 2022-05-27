from cgitb import html
from django.urls import path

from . import views

app_name = 'frontend'

urlpatterns = [

    #authenticationubah
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user-dashboard/', views.user_dashboard, name='user-dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),

    #misi utama
    path('misi-utama/', views.read_misi_utama, name='read_misi_utama'),
    path('detail-misi-utama/',views.detail_misi_utama,name='detail_misi_utama'),
    path('create-misi-utama/',views.create_misi_utama,name='create_misi_utama'),
    path('read-menggunakan-barang/', views.read_menggunakan_barang, name='read-menggunakan-barang'),
    path('create-menggunakan-barang/', views.create_menggunakan_barang, name='create-menggunakan-barang'),
    path('read-pekerjaan/', views.read_pekerjaan, name='read-pekerjaan'),
    path('read-bekerja/', views.read_bekerja, name='read-bekerja'),
    path('create-tokoh/', views.create_tokoh, name='create-tokoh'),
    path('read-tokoh/', views.read_tokoh, name='read-tokoh'),
    path('read-tokoh/<nama_tokoh>', views.read_detail_tokoh, name='read-tokoh'),
    # menjalankan misi utama
    path('menjalankan-misi-utama/',views.read_menjalankan_misi_utama, name='read_menjalankan_misi_utama'),
    path('create-menjalankan-misi-utama/',views.create_menjalankan_misi_utama, name='create_menjalankan_misi_utama'),
    path('update-menjalankan-misi-utama/', views.ubah_menjalankan_misi_utama, name='ubah_menjalankan_misi_utama'),
    # makanan
    path('makanan/',views.read_makanan, name='read_makanan'),
    path('create-makanan/',views.create_makanan, name='create_makanan'),
    path('update-makanan/',views.ubah_makanan, name='create_makanan'),
    # makan 
    path('makan/',views.read_makan, name='read_amakan'),
    path('create-makan/', views.create_makan, name='create_makan'),
    path('warna-kulit/', views.warna_kulit, name='warna_kulit'),
    path('create-warna-kulit/', views.create_warna_kulit, name='create_warna_kulit'),
    path('level/', views.level, name='level'),
    path('create-level/', views.create_level, name='create_level'),
    path('update-level/', views.update_level, name='update_level'),
    path('menggunakan-apparel/', views.menggunakan_apparel, name='menggunakan_apparel'),
    path('create-menggunakan-apparel/', views.create_menggunakan_apparel, name='create_menggunakan_apparel'),
    path('read-kategori-apparel/', views.read_kategori_apparel, name = 'read-kategori-apparel'),
    path('create-kategori-apparel/', views.create_kategori_apparel, name ='create-kategori-apparel'),
    path('read-koleksi-tokoh/', views.read_koleksi_tokoh, name ='read-koleksi-tokoh'),
    path('create-koleksi-tokoh/', views.create_koleksi_tokoh, name ='create-koleksi-tokoh'),
    path('read-koleksi/', views.read_koleksi, name ='read-koleksi'),
    path('create-koleksi/', views.create_koleksi, name ='create-koleksi'),
    path('update-koleksi/', views.ubah_koleksi, name = 'ubah_koleksi')
]