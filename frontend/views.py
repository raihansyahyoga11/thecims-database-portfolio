from cgi import test
from django.shortcuts import render
from django.db import connection

def home(request):
    cursor = connection.cursor()
    cursor.execute("select * from auth_user;")
    test_manggil = cursor.fetchall()
    print(test_manggil)
    return render(request, 'home.html')
# Create your views here.
