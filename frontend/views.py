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
        elif (len(var_y) != 0):
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
        return render(request, 'misi_utama.html', {'content': result})

    elif request.session['account-type'] == 'admin' :
        username = request.session.get('username')
        cursor.execute(f"""SELECT MU.nama_misi 
                            FROM misi_utama MU 
                            JOIN menjalankan_misi_utama MMU ON MU.nama_misi = MMU.nama_misi 
                            JOIN Tokoh T ON MMU.nama_tokoh = T.nama;""")
        result = cursor.fetchall()
        return render(request, 'misi_utama_admin.html', {'content': result})



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
    cursor.execute(f"""SELECT nama, efek_energi,efek_hubungan_sosial, efek_kelaparan, syarat_energi, syarat_hubungan_sosial, syarat_kelaparan, completition_time, reward_koin, reward_xp
                        FROM MISI 
                        WHERE """)
    result = cursor.fetchall()
    return render(request, 'misi_utama.html', {'content': result})








