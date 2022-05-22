from cgi import test
import datetime
from http.client import HTTPResponse
from random import randint
from sqlite3 import connect
from time import strftime
from urllib import response
from django.shortcuts import render, redirect
from django.db import connection
from datetime import datetime

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
    role = request.session.get('account-type')
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
        'koin': user_terpilih[0][3],
        'account_type':role
    }

    return render(request, 'home_and_dashboard/user_dashboard.html', response)

def admin_dashboard(request):
    username = request.session.get('username')
    role = request.session.get('account-type')
    response = {
        'username': username,
        'account_type':role
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
        role = request.session.get('account-type')
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

        response = {
            'content' : result,
            'account_type': role
        }
        return render(request, 'misi_utama/misi_utama_user.html', response)

    elif request.session['account-type'] == 'admin' :
        username = request.session.get('username')
        cursor.execute(f"""SELECT nama_misi FROM misi_utama;""")
        result = cursor.fetchall()

        response = {
            'content' : result,
            'account_type': role
        }
        return render(request, 'misi_utama/misi_utama_admin.html', response)

def detail_misi_utama(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try :
        role = request.session.get('account-type')
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
    response = {
            'content' : result,
            'account_type': role
        }
    return render(request, 'misi_utama/detail_misi_utama.html', response)

def create_misi_utama(request) :
    cursor = connection.cursor()
    try :
        role = request.session.get('account-type')
    except:
        return redirect('/')
    cursor.execute("set search_path to keluarga_yoga")
    response = {
        'account_type' : role,
    }
    if request.session['account-type'] == 'admin' :
        print('anjay')
        if (request.method == 'POST'):
            print('uhuy')
            nama = request.POST.get('nama')
            efek_energi = request.POST.get('efek_energi')
            efek_hubungan_sosial = request.POST.get('efek_hubungan_sosial')
            efek_kelaparan = request.POST.get('efek_kelaparan')
            syarat_energi = request.POST.get('syarat_energi')
            syarat_hubungan_sosial = request.POST.get('syarat_hubungan_sosial')
            syarat_kelaparan = request.POST.get('syarat_kelaparan')
            completion_time = datetime.strptime(request.POST.get('completion_time'), '%H:%M')
            time = "{:d}:{:02d}:{:02d}".format(completion_time.hour, completion_time.minute, completion_time.second)

            print(time)
            reward_koin = request.POST.get('reward_koin')
            reward_xp = request.POST.get('reward_xp')
            deskripsi = request.POST.get('deskripsi')
            # s = strftime("%H:%M:%S")
            cursor.execute(f""" INSERT INTO misi (nama, efek_energi, efek_hubungan_sosial, efek_kelaparan, syarat_energi, syarat_hubungan_sosial, syarat_kelaparan, completion_time, reward_koin, reward_xp, deskripsi) 
                                VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                            """ %(nama,efek_energi,efek_hubungan_sosial, efek_kelaparan, syarat_energi, syarat_hubungan_sosial, syarat_kelaparan, time, reward_koin, reward_xp, deskripsi))


            cursor.execute(f""" insert into misi_utama (nama_misi) 
                                values('%s')""" %(nama))
            return redirect("/misi-utama")
        return render(request, 'misi_utama/create_misi_utama.html', response)
    elif request.session['account-type'] == 'pemain' :
        return redirect('/')


def read_menjalankan_misi_utama(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try :
        role = request.session.get('account-type')
    except:
        return redirect('/')
    cursor.execute("set search_path to keluarga_yoga")
    cursor.execute("select * from menjalankan_misi_utama")
    if request.session['account-type'] == 'pemain' :
        username = request.session.get('username')
        cursor.execute(f"""SELECT MMU.nama_tokoh, MMU.nama_misi, MMU.status
                            FROM menjalankan_misi_utama MMU  
                            WHERE MMU.username_pengguna = '{username}';""")
        result = cursor.fetchall()
        response = {
            'content' : result,
            'account_type': role
        }
        if (request.method == 'POST') :
            ubah_nama_tokoh = request.POST.get("ubah_menjalankan_misi_utama_tokoh")
            ubah_nama_misi_utama = request.POST.get("ubah_menjalankan_misi_utama_misi")
            # global passing1
            # def passing1():
            #     return HTTPResponse(ubah_nama_tokoh)

            # global passing2
            # def passing2():
            #     return HTTPResponse(ubah_nama_misi_utama)
            # request.session['nama_tokoh_menjalankan_misi_utama'] = ubah_nama_tokoh
            # request.session['misi_utama_status_diubah'] = ubah_nama_misi_utama
            response = {
                'account_type': role,
                'ubah_nama_tokoh' :ubah_nama_tokoh,
                'ubah_nama_misi_utama' :ubah_nama_misi_utama
            }
            return render(request,'menjalankan_misi_utama/ubah_menjalankan_misi_utama.html', response)

        return render(request, 'menjalankan_misi_utama/jalankan_misi_utama_user.html', response)

    elif request.session['account-type'] == 'admin' :
        username = request.session.get('username')
        cursor.execute(f"""SELECT MMU.Username_pengguna, MMU.nama_tokoh, MMU.nama_misi, MMU.status
                            FROM Menjalankan_misi_utama MMU;""")
        result = cursor.fetchall()
        response = {
            'content' : result,
            'account_type': role
        }
        return render(request, 'menjalankan_misi_utama/jalankan_misi_utama_admin.html', response)

def create_menjalankan_misi_utama(request) :
    username = request.session.get('username')
    cursor = connection.cursor()
    try :
        role = request.session['account-type']
    except:
        return redirect('/')
    cursor.execute("set search_path to keluarga_yoga")
    if request.session['account-type'] == 'pemain' :
        cursor.execute(f"""SELECT nama
                            FROM tokoh
                            WHERE username_pengguna = '{username}' ;""")
        tokoh_misi = cursor.fetchall()
        cursor.execute(f"""SELECT nama_misi
                            FROM misi_utama;""")
        pilihan_misi = cursor.fetchall()
        response = {
            'content1' : tokoh_misi,
            'account_type': role,
            'content2' : pilihan_misi
        }
        # print(tokoh_misi)
        # print(pilihan_misi)
        if (request.method == 'POST'):
            tokoh_menjalankan_misi_baru = request.POST.get('nama-tokoh-misi')
            print(tokoh_menjalankan_misi_baru)
            cursor.execute(f"""SELECT DISTINCT tokoh.username_pengguna
                            FROM tokoh, menjalankan_misi_utama
                            WHERE tokoh.nama= '%s';""" %(tokoh_menjalankan_misi_baru))
            username_pengguna = cursor.fetchone()[0]   
            print(username_pengguna)               
            misi_baru_dipilih = request.POST.get('nama-misi-dipilih')
            cursor.execute(f""" INSERT INTO menjalankan_misi_utama (username_pengguna, nama_tokoh, nama_misi, status) 
                    VALUES('%s', '%s', '%s', '%s')
                """ %(username_pengguna, tokoh_menjalankan_misi_baru, misi_baru_dipilih, "Belum selesai"))
            return redirect("/menjalankan-misi-utama")
        return render(request, 'menjalankan_misi_utama/create_menjalankan_misi_utama.html', response)


def read_makanan(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    role = request.session.get('account-type')
  
    cursor.execute("set search_path to keluarga_yoga")
    cursor.execute("select * from makanan")

    cursor.execute(f"""SELECT M.nama, M.harga, M.tingkat_energi, M.tingkat_kelaparan
                            FROM Makanan M;""")
    result = cursor.fetchall()
    response = {
            'content' : result,
            'account_type': role
    }
    if request.session['account-type'] == 'pemain' :
        return render(request, 'makanan/makanan_user.html', response)
    if request.session['account-type'] == 'admin' :
        if request.method == 'POST' :
            makanan_diubah = request.POST.get('mengubah_makanan')
            response = {
                'makanan_diubah' : makanan_diubah,
                'account_type': role
            }
            return render(request, 'makanan/ubah_makanan.html', response)
        return render(request, 'makanan/makanan_admin.html', response)


def create_makanan(request) :
    cursor = connection.cursor()
    try :
        role = request.session.get('account-type')
    except:
        return redirect('/')
    response = {
        'account_type' : role
    }
    cursor.execute("set search_path to keluarga_yoga")
    if request.session['account-type'] == 'admin' :
        if (request.method == 'POST'):
            print("anjaayyyyyyyyyyyy")
            nama_makanan = request.POST.get('nama_makanan')
            harga = request.POST.get('harga')
            tingkat_energi = request.POST.get('tingkat_energi')
            tingkat_kelaparan = request.POST.get('tingkat_kelaparan')
            cursor.execute(f""" INSERT INTO makanan (nama, harga, tingkat_energi, tingkat_kelaparan) 
                                VALUES('%s', '%s', '%s', '%s')
                            """ %(nama_makanan, harga, tingkat_energi, tingkat_kelaparan))
            return redirect("/makanan")
        return render(request, 'makanan/create_makanan.html', response)
    else :
        return redirect('/')

def read_makan(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try :
        role = request.session.get('account-type')
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
        response = {
            'content' : result,
            'account_type': role
        }
        return render(request, 'makan/makan_user.html', response)

    elif request.session['account-type'] == 'admin' :
        username = request.session.get('username')
        cursor.execute(f"""SELECT M.username_pengguna, M.nama_tokoh, M.nama_makanan, M.Waktu
                            FROM makan M;""")
        result = cursor.fetchall()
        response = {
            'content' : result,
            'account_type': role
        }
        return render(request, 'makan/makan_admin.html', response)



def create_makan(request) :
    
    username = request.session.get('username')
    try :
        role = request.session.get('account-type')
    except:
        return redirect('/')
    cursor = connection.cursor()
    response = {
            'account_type': role,
    }
    cursor.execute("set search_path to keluarga_yoga")
    if request.session['account-type'] == 'pemain' :
        cursor.execute(f"""SELECT nama
                            FROM tokoh
                            WHERE username_pengguna = '{username}' ;""")
        tokoh_makan = cursor.fetchall()
        cursor.execute(f"""SELECT nama
                            FROM Makanan;""")
        daftar_makanan = cursor.fetchall()
        response = {
            'content' : tokoh_makan,
            'account_type': role,
            'daftar_makanan' : daftar_makanan
            }

        if (request.method == 'POST'):
            print('samoe')
            tokoh_baru = request.POST.get('nama-tokoh')
            cursor.execute(f"""SELECT tokoh.username_pengguna
                                FROM tokoh JOIN makan on tokoh.nama = makan.nama_tokoh
                                WHERE makan.nama_tokoh= '%s';""" %(tokoh_baru))
            username_pengguna = cursor.fetchone()[0]
            makanan_baru = request.POST.get('nama-makanan')
            waktu_sekarang = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(f""" INSERT INTO makan (username_pengguna, nama_tokoh, waktu, nama_makanan) 
                    VALUES('%s', '%s', '%s', '%s')
                """ %(username_pengguna, tokoh_baru, waktu_sekarang, makanan_baru))
            return redirect("/makan")

        return render(request, 'makan/create_makan.html', response)
    else :
        return redirect('/')


def ubah_makanan(request) :
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    try :
        role = request.session.get('account-type')
    except:
        return redirect('/')
    if request.session['account-type'] == 'admin' :
        cursor.execute("set search_path to keluarga_yoga")
        cursor.execute("select * from makanan ")
        
        # response = {
        #     'content' : mengubah_makanan,
        #     'account_type': role
        # }
        if (request.method =="POST") :
            makanan_terubah = request.POST.get('makanan_terubah')
            harga_makanan_baru = request.POST.get("harga_makanan_baru")
            tingkat_energi_baru = request.POST.get("tingkat_energi_batu")
            tingkat_kelaparan_baru = request.POST.get("tingkat_kelaparan_baru")
            print(makanan_terubah)
            print(harga_makanan_baru)
            print(tingkat_energi_baru)
            print(tingkat_kelaparan_baru)
            cursor.execute(f"""UPDATE makanan 
                                SET harga = '{harga_makanan_baru}', tingkat_energi = '{tingkat_energi_baru}', tingkat_kelaparan = '{ tingkat_kelaparan_baru }'
                                WHERE nama = '{ makanan_terubah }' ;""")
            return redirect('/makanan/')
        return render(request, 'makanan/ubah_makanan.html', response)
    else :
        return redirect('/')

def ubah_menjalankan_misi_utama(request) :
    username = request.session.get('username')
    cursor = connection.cursor()
    try :
        role = request.session.get('account-type')
    except:
        return redirect('/')
    cursor.execute("set search_path to keluarga_yoga")
    response = {
        'account-type' : role
    }
    if request.session['account-type'] == 'pemain' :
        if (request.method == 'POST') :
            ubah_nama_tokoh = request.POST.get("nama_tokoh_menjalankan_misi_utama")
            ubah_nama_misi_utama = request.POST.get("misi_utama_status_diubah")
            status_misi_baru = request.POST.get("status_misi_baru")
            cursor.execute(f""" UPDATE menjalankan_misi_utama 
                                SET status = '{status_misi_baru}'
                                WHERE username_pengguna = '{username}' 
                                    AND nama_tokoh = '{ubah_nama_tokoh}' 
                                    AND nama_misi = '{ubah_nama_misi_utama}';
                            """ )
            return redirect("/menjalankan-misi-utama/")
        
        return render(request, 'menjalankan_misi_utama/ubah_menjalankan_misi_utama.html', response)
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

def read_koleksi(request):
    cursor = connection.cursor()

    query_rambut = f"select * from keluarga_yoga.rambut as R, keluarga_yoga.koleksi as K where R.id_koleksi = K.id"
    cursor.execute(query_rambut)   
    result_rambut = cursor.fetchall()

    query_mata = f"select * from keluarga_yoga.mata as M, keluarga_yoga.koleksi as K where M.id_koleksi = K.id"
    cursor.execute(query_mata)
    result_mata = cursor.fetchall()

    query_rumah = f"select * from keluarga_yoga.rumah as R, keluarga_yoga.koleksi_jual_beli as KJB, keluarga_yoga.koleksi as K where R.id_koleksi = KJB.id_koleksi AND KJB.id_koleksi = K.id"
    cursor.execute(query_rumah)
    result_rumah = cursor.fetchall()

    query_barang = f"select * from keluarga_yoga.barang as B, keluarga_yoga.koleksi_jual_beli as KJB, keluarga_yoga.koleksi as K where B.id_koleksi = KJB.id_koleksi AND KJB.id_koleksi = K.id"
    cursor.execute(query_barang)
    result_barang = cursor.fetchall()

    query_apparel = f"select * from keluarga_yoga.apparel as A, keluarga_yoga.koleksi_jual_beli as KJB, keluarga_yoga.koleksi as K where A.id_koleksi = KJB.id_koleksi AND KJB.id_koleksi = K.id"
    cursor.execute(query_apparel)
    result_apparel = cursor.fetchall()

    if request.session['account-type'] == 'admin':
        return render(request, 'koleksi_admin.html', {'content_rambut': result_rambut, 'content_mata': result_mata, 'content_rumah': result_rumah, 'content_barang': result_barang, 'content_apparel': result_apparel})
    elif request.session['account-type'] == 'pemain':
        return render(request, 'koleksi.html', {'content_rambut': result_rambut, 'content_mata': result_mata, 'content_rumah': result_rumah, 'content_barang': result_barang, 'content_apparel': result_apparel})

def create_koleksi(request):
    cursor = connection.cursor() 
    if request.session['account-type'] == 'admin': 
        query_apparel = f"select nama_kategori from keluarga_yoga.kategori_apparel"
        cursor.execute(query_apparel)
        result_app = cursor.fetchall()

        query_pekerjaan = f"select nama from keluarga_yoga.pekerjaan"
        cursor.execute(query_pekerjaan)
        result_pek = cursor.fetchall()

        return render(request, 'create_koleksi.html', {'content_app': result_app, 'content_pek': result_pek})
    elif request.session['account-type'] == 'pemain': 
        return render(request, 'home.html')
