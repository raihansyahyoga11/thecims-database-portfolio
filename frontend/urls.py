from django.urls import path

from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user-dashboard/', views.user_dashboard, name='user-dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('read-kategori-apparel/', views.read_kategori_apparel, name = 'read-kategori-apparel'),
    path('create-kategori-apparel/', views.create_kategori_apparel, name ='create-kategori-apparel'),
    path('read-koleksi-tokoh/', views.read_koleksi_tokoh, name ='read-koleksi-tokoh'),
    path('create-koleksi-tokoh/', views.create_koleksi_tokoh, name ='create-koleksi-tokoh'),
]