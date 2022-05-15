from cgi import test
import email
from random import randint
from urllib import response
from django.shortcuts import render, redirect
from django.db import connection


def home(request):
    return render(request, 'home.html')


def login(request):
    if (request.method == 'POST'):
        # To get data from login.html
        login_form = request.POST
        cursor = connection.cursor()
        username_form = login_form['username']
        password_form = login_form['user-password']

        # Testing whether var_x is a valid pemain
        search_query_x = f"select username from KELUARGA_YOGA.pemain where username='{username_form}' and password='{password_form}'"
        cursor.execute(search_query_x)
        var_x = cursor.fetchall()

        # Testing whether var_y is a valid admin
        search_query_y = f"select username from KELUARGA_YOGA.admin where username='{username_form}' and password='{password_form}'"
        cursor.execute(search_query_y)
        var_y = cursor.fetchall()

        if (len(var_x) != 0):
            print("KETEMU KAMU USER YA @" + username_form)
            request.session.modified = True
            request.session['username'] = username_form
            request.session['account-type'] = 'pemain'

            return redirect('frontend:user-dashboard')
        elif (len(var_y) == 0):
            print("KETEMU KAMU ADMIN YA @" + username_form)
            request.session.modified = True
            request.session['username'] = username_form
            request.session['account-type'] = 'admin'
            
            return redirect('frontend:admin-dashboard')
        else:
            print("Sial tidak ditemukan >.<")

    return render(request, 'login.html')

def user_dashboard(request):
    username = request.session.get('username')
    print(username)
    cursor = connection.cursor()
    query = f"select username, email, no_hp, koin from KELUARGA_YOGA.pemain where username='{username}'"
    cursor.execute(query)
    user_terpilih = cursor.fetchall()
    print(user_terpilih)
    
    response = {
        'username': user_terpilih[0][0],
        'email': user_terpilih[0][1],
        'no_hp':"0" + user_terpilih[0][2],
        'koin': user_terpilih[0][3]
    }

    return render(request, 'user_dashboard.html', response)

def admin_dashboard(request):
    username = request.session.get('username')
    response = {
        'username': username
    }
    return render(request, 'admin_dashboard.html', response)

def logout(request):
    request.session.clear()
    return render(request, 'home.html')

def register(request):
    if (request.method == 'POST'):
        form_data = request.POST
        register_username = form_data['user-username']
        register_email = form_data['user-email']
        register_user_password = form_data['user-password']
        register_no_hp = form_data['user-no-hp']
        koin = randint(1,100)

        akun_query = f"INSERT INTO KELUARGA_YOGA.AKUN VALUES ('{register_username}')"
        pemain_query = f"INSERT INTO KELUARGA_YOGA.PEMAIN VALUES('{register_username}','{register_email}','{register_user_password}',{register_no_hp},{koin})"

        cursor = connection.cursor()
        cursor.execute(akun_query)
        cursor.execute(pemain_query)

        return redirect('frontend:login')
        
    return render(request, 'register.html')
