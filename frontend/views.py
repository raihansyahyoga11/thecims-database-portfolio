from cgi import test
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
    
# Create your views here.
def read_kategori_apparel(request):
    cursor = connection.cursor()
    query = f"select nama_kategori from KELUARGA_YOGA.kategori_apparel"
    cursor.execute(query)
    result = cursor.fetchall()
    if request.session['account-type'] == 'pemain':
        return render(request, 'kategori_apparel.html', {'content': result})
    elif request.session['account-type'] == 'admin':
        return render(request, 'kategori_apparel_admin.html', {'content': result})

def create_kategori_apparel(request):
    if request.session['account-type'] == 'pemain':
        return render(request, 'home.html')
    elif request.session['account-type'] == 'admin':
        return render(request, 'create_kategori_apparel.html')

def read_koleksi_tokoh(request):
    username = request.session.get('username')
    cursor = connection.cursor()
    if request.session['account-type'] == 'pemain':
        query = f"select * from keluarga_yoga.koleksi_tokoh WHERE username_pengguna = '{username}' order by username_pengguna"
        cursor.execute(query)
        result = cursor.fetchall()
        return render (request, 'koleksi_tokoh.html', {'content': result})
    elif request.session['account-type'] == 'admin':
        query = f"select * from keluarga_yoga.koleksi_tokoh order by username_pengguna"
        cursor.execute(query)
        result = cursor.fetchall()
        return render (request, 'koleksi_tokoh_admin.html', {'content': result})

def create_koleksi_tokoh(request):
    cursor = connection.cursor() 
    if request.session['account-type'] == 'admin': 
        username = request.session.get('username')
        query_daftar_tokoh = f"select distinct nama_tokoh from keluarga_yoga.koleksi_tokoh WHERE username_pengguna = '{username}'"
        cursor.execute(query_daftar_tokoh)
        result_dt = cursor.fetchall()

        query_id_koleksi = f"select id from keluarga_yoga.koleksi"
        cursor.execute(query_id_koleksi)
        result_ik = cursor.fetchall()
        return render(request, 'create_koleksi_tokoh.html', {'content_dt': result_dt, 'content_ik': result_ik})
    elif request.session['account-type'] == 'pemain': 
        return render(request, 'home.html')