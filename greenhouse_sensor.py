import pyfirmata.util
import pyrebase
import pyfirmata
from pyfirmata import util, Arduino
import time

# Declare Database
config = {
    "apiKey": "AIzaSyCFpxNB5tkosVBf26FinfxF7OrGYFsq8ko",
    "authDomain": "test-4247d.firebaseapp.com",
    "databaseURL": "https://test-4247d-default-rtdb.firebaseio.com",
    "projectId": "test-4247d",
    "storageBucket": "test-4247d.appspot.com",
    "messagingSenderId": "838790103779",
    "appId": "1:838790103779:web:063b7c6e563b8151937bd6",
    "measurementId": "G-V4XXE4ZWT0"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

data = {
    "kapasitas_ruangan": 10,
    "orang_didalam": 0,
    "orang_keluar": 0,
}

port = "COM4"
board = Arduino(port)

# Variabel Declaration
HIGH = True
LOW = False
program_jalan = True

value_masuk = 0
value_keluar = 0
# detect_order = ""
last_detect_status = True
first_detect_status = False
base_value = 0

pin_sensorIn1 = board.get_pin('a:0:i') #for light sensor 1
pin_sensorIn2 = board.get_pin('a:1:i') #for light sensor 2
pir_sensor = board.get_pin('d:2:i') #for pir sensor
tulis_lampu1 = board.get_pin('d:8:o') #for nyalakan lampu 1
tulis_lampu2 = board.get_pin('d:9:o') #for nyalakan lampu 2
tulis_AC = board.get_pin('d:10:o') #for nyalakan AC (lampu 3)
nyala_infrared1 = board.get_pin('d:6:o') #for nyalakan led inframerah 1
nyala_infrared2 = board.get_pin('d:7:o') #for nyalakan led inframerah 2

# Start Program
it = pyfirmata.util.Iterator(board)
it.start()
time.sleep(1.0)

try :

    db.child('Data_Ruangan').set(data)

    nyala_laser1 = nyala_infrared1.write(HIGH)
    nyala_laser2 = nyala_infrared2.write(HIGH)
    lampu1 = tulis_lampu1.write(LOW)
    lampu2 = tulis_lampu2.write(LOW)
    AC = tulis_AC.write(LOW)

    light_value1 = pin_sensorIn1.read()
    time.sleep(0.1)
    light_value2 = pin_sensorIn2.read()
    time.sleep(0.1)
    pir_value = pir_sensor.read()
    time.sleep(0.1)

    print(f'light1: {light_value1}')
    print(f'light2: {light_value2}')
    print(f'pir: {pir_value}')

    # get_value1 = db.child('Data_Ruangan').get()
    # orang_dalam_ruangan = get_value1.val()['orang_didalam']
    # print(f'dalam: {orang_dalam_ruangan}')
    # orang_luar_ruangan = get_value1.val()['orang_keluar']
    # print(f'luar: {orang_luar_ruangan}')
    # kapasitas_orang = get_value1.val()['kapasitas_ruangan']
    # time.sleep(0.1)

    while True:

        # light_value1 = pin_sensorIn1.read()
        # time.sleep(0.1)
        # light_value2 = pin_sensorIn2.read()
        # time.sleep(0.1)
        # pir_value = pir_sensor.read()
        # time.sleep(0.1)

        print(f'light1: {light_value1}')
        print(f'light2: {light_value2}')
        # print(f'pir: {pir_value}')
        
        get_value1 = db.child('Data_Ruangan').get()
        orang_dalam_ruangan = get_value1.val()['orang_didalam']
        # print(f'dalam: {orang_dalam_ruangan}')
        orang_luar_ruangan = get_value1.val()['orang_keluar']
        # print(f'luar: {orang_luar_ruangan}')
        kapasitas_orang = get_value1.val()['kapasitas_ruangan']

        if orang_dalam_ruangan>0: 
            pir_value = pir_sensor.read()
            lampu1 = tulis_lampu1.write(HIGH)
            lampu2 = tulis_lampu2.write(HIGH)
            AC = tulis_AC.write(HIGH)
        elif orang_dalam_ruangan<=0:
            pir_value = pir_sensor.read()
            lampu1 = tulis_lampu1.write(LOW)
            lampu2 = tulis_lampu2.write(LOW)
            AC = tulis_AC.write(LOW)
            db.child('Data_Ruangan').update({'orang_didalam':base_value})
            db.child('Data_Ruangan').update({'orang_keluar':base_value})
            value_keluar=0
            value_masuk=0


        light_value1 = pin_sensorIn1.read()
        light_value2 = pin_sensorIn2.read()
        if light_value1 < 0.9:
            light_value2 = pin_sensorIn2.read()
            if light_value2 < 0.9:
                value_masuk+=1
                db.child('Data_Ruangan').update({'orang_didalam':value_masuk})
                if orang_dalam_ruangan>kapasitas_orang:
                    print("Jumlah orang melebihi kapasitas ruangan")
                if value_keluar>0:
                    value_keluar-=1
                    db.child('Data_Ruangan').update({'orang_keluar':value_keluar})

        else:
            light_value2 = pin_sensorIn2.read()
            if light_value2 < 0.9:
                value_keluar+=1
                value_masuk-=1
                db.child('Data_Ruangan').update({'orang_keluar':value_keluar})
                db.child('Data_Ruangan').update({'orang_didalam':value_masuk})



except:
    board.exit()