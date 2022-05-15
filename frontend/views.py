from cgi import test
from tkinter import ON
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

def warna_kulit(request):
    cursor = connection.cursor()
    query = f"select kode from KELUARGA_YOGA.WARNA_KULIT"
    cursor.execute(query)

    if request.session['account-type'] == 'pemain' :
        result = cursor.fetchall()
        return render(request, 'R_warna_kulit_pengguna.html', {'content' : result})

    elif request.session['account-type'] == 'admin' :
        result = cursor.fetchall()
        return render(request, 'R_warna_kulit_admin.html', {'content' : result})
          
    
def create_warna_kulit(request) :
    if request.session['account-type'] == 'admin' :
        return render(request, 'C_warna_kulit.html')
    else :
         return redirect('/')

def level(request):
    cursor = connection.cursor()
    query = f"select * from KELUARGA_YOGA.LEVEL"
    cursor.execute(query)

    if request.session['account-type'] == 'pemain' :
        result = cursor.fetchall()
        return render(request, 'R_level_pengguna.html', {'content' : result})

    elif request.session['account-type'] == 'admin' :
        result = cursor.fetchall()
        return render(request, 'R_level_admin.html', {'content' : result})

def create_level(request) :
    if request.session['account-type'] == 'admin' :
        return render(request, 'C_level.html')
    else :
         return redirect('/')

def update_level(request) :
    if request.session['account-type'] == 'admin' :
        return render(request, 'U_level.html')
    else :
         return redirect('/')

def create_menggunakan_apparel(request) :
    cursor = connection.cursor()
    query = f"select * from KELUARGA_YOGA.KOLEKSI_TOKOH"
    cursor.execute(query)

    if request.session['account-type'] == 'pemain' :
        username = request.session.get('username')
        cursor.execute(f"""SELECT KT.nama_tokoh, KT.id_koleksi
                           FROM KELUARGA_YOGA.KOLEKSI_TOKOH KT 
                           WHERE KT.id_koleksi LIKE 'A%' AND KT.username_pengguna = '{username}';""")

        result = cursor.fetchall()
        return render(request, 'C_menggunakan_apparel.html', {'content' : result})
    else :
         return redirect('/')


def menggunakan_apparel(request) :
    cursor = connection.cursor()
    query = f"select * from KELUARGA_YOGA.MENGGUNAKAN_APPAREL"
    cursor.execute(query)

    if request.session['account-type'] == 'pemain' :
        username = request.session.get('username')
        cursor.execute(f"""SELECT MA.nama_tokoh, KJB.nama, A.warna_apparel, A.nama_pekerjaan, A.kategori_apparel
                            FROM KELUARGA_YOGA.APPAREL A 
                            FULL OUTER JOIN KELUARGA_YOGA.MENGGUNAKAN_APPAREL MA ON
                            A.id_koleksi = MA.id_koleksi
                            JOIN KELUARGA_YOGA.KOLEKSI_JUAL_BELI KJB ON
                            A.id_koleksi = KJB.id_koleksi
                            WHERE MA.username_pengguna = '{username}';""")
        result = cursor.fetchall()
        return render(request, 'R_menggunakan_apparel_pengguna.html', {'content' : result})

    if request.session['account-type'] == 'admin' :
        cursor.execute(f"""SELECT MA.username_pengguna, MA.nama_tokoh, KJB.nama, A.warna_apparel, A.nama_pekerjaan, A.kategori_apparel
                            FROM KELUARGA_YOGA.APPAREL A 
                            FULL OUTER JOIN KELUARGA_YOGA.MENGGUNAKAN_APPAREL MA ON
                            A.id_koleksi = MA.id_koleksi
                            JOIN KELUARGA_YOGA.KOLEKSI_JUAL_BELI KJB ON
                            A.id_koleksi = KJB.id_koleksi;""")
        result = cursor.fetchall()
        return render(request, 'R_menggunakan_apparel_admin.html', {'content' : result})
    

