from cgi import test
from django.shortcuts import render
from django.db import connection

def home(request):
    cursor = connection.cursor()
    cursor.execute("select * from auth_user;")
    test_manggil = cursor.fetchall()
    print(test_manggil)
    return render(request, 'home.html')

def login(request):
    if (request.method == 'POST'):
        finder = request.POST
        cursor = connection.cursor()
        user_form = finder['email']
        search_query = "select username from KELUARGA_YOGA.akun where username='" + user_form + "';"
        cursor.execute(search_query)
        varx = cursor.fetchall()
        if (len(varx) == 0):
            print("Sial tidak ditemukan >.<")
        else:
            print("KETEMU KAMU: " + user_form)
    
    
    return render(request, 'login.html')
# Create your views here.
