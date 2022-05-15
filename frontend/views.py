from cgi import test
import datetime
from random import randint
from sqlite3 import connect
from urllib import response
from django.shortcuts import render, redirect
from django.db import connection


def home(request):
    return render(request, 'home_and_dashboard/home.html')


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
        elif (len(var_y) != 0):
            print("KETEMU KAMU ADMIN YA @" + username_form)
            request.session.modified = True
            request.session['username'] = username_form
            request.session['account-type'] = 'admin'
            
            return redirect('frontend:admin-dashboard')
        else:
            print("Sial tidak ditemukan >.<")

    return render(request, 'login_and_authentication/login.html')

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

    return render(request, 'home_and_dashboard/user_dashboard.html', response)

def admin_dashboard(request):
    username = request.session.get('username')
    response = {
        'username': username
    }
    return render(request, 'home_and_dashboard/admin_dashboard.html', response)

def logout(request):
    request.session.clear()
    return render(request, 'home_and_dashboard/home.html')


# Create your views here.

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

def read_misi_utama(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try :
        Role = request.session['account-type']
    except:
        return redirect('/')
    cursor.execute("set search_path to keluarga_yoga")
    cursor.execute("select * from misi_utama ")

    if request.session['account-type'] == 'pemain' :
        print("UHUYY")
        username = request.session.get('username')
        cursor.execute(f"""SELECT MU.nama_misi 
                            FROM misi_utama MU 
                            JOIN menjalankan_misi_utama MMU ON MU.nama_misi = MMU.nama_misi 
                            JOIN Tokoh T ON MMU.nama_tokoh = T.nama 
                            WHERE T.username_pengguna = '{username}';""")
        result = cursor.fetchall()
        return render(request, 'misi_utama/misi_utama_user.html', {'content': result})

    elif request.session['account-type'] == 'admin' :
        username = request.session.get('username')
        cursor.execute(f"""SELECT MU.nama_misi 
                            FROM misi_utama MU 
                            JOIN menjalankan_misi_utama MMU ON MU.nama_misi = MMU.nama_misi 
                            JOIN Tokoh T ON MMU.nama_tokoh = T.nama;""")
        result = cursor.fetchall()
        return render(request, 'misi_utama/misi_utama_admin.html', {'content': result})

def detail_misi_utama(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try :
        Role = request.session['account-type']
    except:
        return redirect('/')
    cursor.execute("set search_path to keluarga_yoga")
    cursor.execute("select * from misi_utama ")
    username = request.session.get('username')
    misi_detail = request.POST.get('misi_detail')
    cursor.execute(f"""SELECT nama, efek_energi,efek_hubungan_sosial, efek_kelaparan, syarat_energi, syarat_hubungan_sosial, syarat_kelaparan, completion_time, reward_koin, reward_xp
                        FROM MISI 
                        WHERE nama = '{misi_detail}' ;""")
    result = cursor.fetchall()
    return render(request, 'misi_utama/detail_misi_utama.html', {'content': result})

def create_misi_utama(request) :
    if request.session['account-type'] == 'admin' :
        return render(request, 'misi_utama/create_misi_utama.html')


def read_menjalankan_misi_utama(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try :
        Role = request.session['account-type']
    except:
        return redirect('/')
    cursor.execute("set search_path to keluarga_yoga")
    cursor.execute("select * from menjalankan_misi_utama")

    if request.session['account-type'] == 'pemain' :
        print("UHUYY")
        username = request.session.get('username')
        cursor.execute(f"""SELECT MMU.nama_tokoh, MMU.nama_misi, MMU.status
                            FROM menjalankan_misi_utama MMU  
                            WHERE MMU.username_pengguna = '{username}';""")
        result = cursor.fetchall()
        return render(request, 'menjalankan_misi_utama/jalankan_misi_utama_user.html', {'content': result})

    elif request.session['account-type'] == 'admin' :
        username = request.session.get('username')
        cursor.execute(f"""SELECT MMU.Username_pengguna, MMU.nama_tokoh, MMU.nama_misi, MMU.status
                            FROM Menjalankan_misi_utama MMU;""")
        result = cursor.fetchall()
        return render(request, 'menjalankan_misi_utama/jalankan_misi_utama_admin.html', {'content': result})

def create_menjalankan_misi_utama(request) :
    username = request.session.get('username')
    cursor = connection.cursor()
    if request.session['account-type'] == 'pemain' :
        cursor.execute("set search_path to keluarga_yoga")
        cursor.execute(f"""SELECT MMU.nama_tokoh, MMU.nama_misi
                            FROM Menjalankan_misi_utama MMU  
                            WHERE MMU.username_pengguna = '{username}';""")
        result = cursor.fetchall()
        return render(request, 'menjalankan_misi_utama/create_menjalankan_misi_utama.html',{'content': result})


def read_makanan(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try :
        Role = request.session['account-type']
    except:
        return redirect('/')
    cursor.execute("set search_path to keluarga_yoga")
    cursor.execute("select * from makanan")

    cursor.execute(f"""SELECT M.nama, M.harga, M.tingkat_energi, M.tingkat_kelaparan
                            FROM Makanan M;""")
    result = cursor.fetchall()
    if request.session['account-type'] == 'pemain' :
        return render(request, 'makanan/makanan_user.html', {'content': result})
    elif request.session['account-type'] == 'admin' :
        return render(request, 'makanan/makanan_admin.html', {'content': result})


def create_makanan(request) :
    if request.session['account-type'] == 'admin' :
        return render(request, 'makanan/create_makanan.html')
    else :
        return redirect('/')

def update_makanan(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try :
        Role = request.session['account-type']
    except:
        return redirect('/')
    cursor.execute("set search_path to keluarga_yoga")
    cursor.execute("select * from makanan ")
    username = request.session.get('username')
    misi_detail = request.POST.get('misi_detail')
    cursor.execute(f"""SELECT nama, efek_energi,efek_hubungan_sosial, efek_kelaparan, syarat_energi, syarat_hubungan_sosial, syarat_kelaparan, completion_time, reward_koin, reward_xp
                        FROM MISI 
                        WHERE nama = '{misi_detail}' ;""")
    result = cursor.fetchall()
    return render(request, 'misi_utama/detail_misi_utama.html', {'content': result})



def read_makan(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try :
        Role = request.session['account-type']
    except:
        return redirect('/')
    cursor.execute("set search_path to keluarga_yoga")
    cursor.execute("select * from makan")

    if request.session['account-type'] == 'pemain' :
        username = request.session.get('username')
        cursor.execute(f"""SELECT M.nama_tokoh, M.nama_makanan, M.Waktu
                            FROM makan M  
                            WHERE M.username_pengguna = '{username}';""")
        result = cursor.fetchall()
        return render(request, 'makan/makan_user.html', {'content': result})

    elif request.session['account-type'] == 'admin' :
        username = request.session.get('username')
        cursor.execute(f"""SELECT M.username_pengguna, M.nama_tokoh, M.nama_makanan, M.Waktu
                            FROM makan M;""")
        result = cursor.fetchall()
        return render(request, 'makan/makan_admin.html', {'content': result})



def create_makan(request) :
    username = request.session.get('username')
    cursor = connection.cursor()
    if request.session['account-type'] == 'pemain' :
        cursor.execute("set search_path to keluarga_yoga")
        cursor.execute(f"""SELECT M.nama_tokoh, M.nama_makanan
                            FROM makan M
                            WHERE M.username_pengguna = '{username}' ;""")
        result = cursor.fetchall()
        return render(request, 'makan/create_makan.html', {'content': result})
    else :
        return redirect('/')


def ubah_makanan(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try :
        Role = request.session['account-type']
    except:
        return redirect('/')
    if request.session['account-type'] == 'admin' :
        cursor.execute("set search_path to keluarga_yoga")
        cursor.execute("select * from makanan ")
        mengubah_makanan = request.POST.get('mengubah_makanan')
        return render(request, 'makanan/ubah_makanan.html', {'content': mengubah_makanan})
    else :
        return redirect('/')

def ubah_menjalankan_misi_utama(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try :
        Role = request.session['account-type']
    except:
        return redirect('/')
    if request.session['account-type'] == 'pemain' :
        cursor.execute("set search_path to keluarga_yoga")
        cursor.execute("select * from menjalankan_misi_utama ")
        ubah_menjalankan_misi_utama = request.POST.get('ubah_menjalankan_misi_utama')
        return render(request, 'makanan/ubah_menjalankan_misi_utama.html', {'content': ubah_menjalankan_misi_utama})
    else :
        return redirect('/')







def read_menggunakan_barang(request):
    role = request.session.get('account-type')
    if (role == 'pemain'):
        nama_pemain = request.session.get('username')
        query_pemain = f"select * from KELUARGA_YOGA.menggunakan_barang where username_pengguna='{nama_pemain}'"
        cursor = connection.cursor()
        cursor.execute(query_pemain)
        hasil = cursor.fetchall()
    elif (role == 'admin'):
        query_admin = f"select * from KELUARGA_YOGA.menggunakan_barang"
        cursor = connection.cursor()
        cursor.execute(query_admin)
        hasil = cursor.fetchall()

    return render(request, 'read_menggunakan_barang.html', {'response': hasil})

def create_menggunakan_barang(request):
    role = request.session.get('account-type')
    if (role == 'pemain'):
        if (request.method == 'POST'):
            form_data = request.POST
            nama_pemain = request.session.get('username')
            nama_tokoh = form_data['nama-tokoh']
            waktu = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            id_barang = form_data['id-barang']
            query_pemain = f"INSERT INTO KELUARGA_YOGA.menggunakan_barang VALUES ('{nama_pemain}','{nama_tokoh}','{waktu}','{id_barang}')"
            print(query_pemain)
            cursor = connection.cursor()
            cursor.execute(query_pemain)
    return render(request, 'create_menggunakan_barang.html')

def read_pekerjaan(request):
    query_read_pekerjaan = f"select * from KELUARGA_YOGA.pekerjaan"
    cursor = connection.cursor()
    cursor.execute(query_read_pekerjaan)
    hasil = cursor.fetchall()

    return render(request, 'read_pekerjaan.html', {'response': hasil})

def read_bekerja(request):
    query_read_bekerja = f"select * from KELUARGA_YOGA.bekerja"
    cursor = connection.cursor()
    cursor.execute(query_read_bekerja)
    hasil = cursor.fetchall()

    return render(request, 'read_bekerja.html', {'response': hasil})

def create_tokoh(request):
    role = request.session.get('account-type')
    username = request.session.get('username')
    if (role == 'pemain'):
        if (request.method == 'POST'):
            form_data2 = request.POST
            print(form_data2['input_id_rumah'])
            create_nama_tokoh = form_data2['create_nama_tokoh']
            jenis_kelamin = form_data2['jenis_kelamin'] #dropdown
            poin_xp = randint(0,1000)
            poin_energi = randint(0,100)
            poin_kelaparan = randint(0,100)
            poin_hubungan_sosial = randint(0,100) 
            warna_kulit = form_data2['warna_kulit'] #dropdown
            sifat = form_data2['sifat'] #dropdown
            id_rambut = form_data2['id_rambut'] #dropdown
            id_mata = form_data2['id_mata'] #dropdown
            id_rumah = form_data2['input_id_rumah'] #dropdown

            query_create_tokoh = f"INSERT INTO KELUARGA_YOGA.tokoh VALUES ('{username}','{create_nama_tokoh}','{jenis_kelamin}','Aktif',{poin_xp},{poin_energi},{poin_kelaparan},{poin_hubungan_sosial},'{warna_kulit}',1,'{sifat}',null,'{id_rambut}','{id_mata}','{id_rumah}')"
            
            cursor = connection.cursor()
            cursor.execute(query_create_tokoh)
    return render(request, 'create_tokoh.html')

def read_tokoh(request):
    role = request.session.get('account-type')
    if (role == 'admin'):
        cursor = connection.cursor()
        query_tokoh_admin = f"select * from KELUARGA_YOGA.tokoh"
        cursor.execute(query_tokoh_admin)
        hasil = cursor.fetchall()
    elif (role == 'pemain'):
        username = request.session.get('username')
        cursor = connection.cursor()
        query_tokoh_pemain = f"select * from KELUARGA_YOGA.tokoh where username_pengguna='{username}'"
        cursor.execute(query_tokoh_pemain)
        hasil = cursor.fetchall()
    return render(request, 'read_tokoh.html', {'response': hasil})

def read_detail_tokoh(request, nama_tokoh):
    cursor = connection.cursor()
    query_detail_tokoh = f"select nama, id_mata, id_rambut, id_rumah, warna_kulit, pekerjaan from KELUARGA_YOGA.tokoh where nama='{nama_tokoh}'"
    cursor.execute(query_detail_tokoh)
    hasil = cursor.fetchall()
    response = {
        'nama_tokoh': hasil[0][0],
        'id_rambut': hasil[0][1],
        'id_mata': hasil[0][2],
        'id_rumah': hasil[0][3],
        'warna_kulit': hasil[0][4],
        'pekerjaan': hasil[0][5]
    }
    return render(request, 'read_detail_tokoh.html', response)
# def create_pekerjaan(request):
#     role = request.session.get('account-type')
#     if (role == 'admin'):
        
#     return()

# def delete_pekerjaan(request):
#     if (role == 'admin'):

#     return()

# def update_pekerjaan(request):
#     if (role == 'admin'):
        
#     return()

