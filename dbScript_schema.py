import serial
import sys
import datetime
import time
import sqlite3
import random
import uuid
import re
import threading


dataqlock = threading.Lock()

def dataqcycle(dataq):
    conn = sqlite3.connect("data_acquisition.db")
    cursor = conn.cursor()
    while 1:
        time.sleep(0.1)
        dataqlock.acquire()
        print("len = %d" % len(dataq))
        if len(dataq) > 0:
            cursor.executemany(
                            """
                        INSERT INTO sensor_data (
                            sessionID, timestamp, latitude, longitude, altitude,
                            accel_x, accel_y, accel_z,
                            gyro_x, gyro_y, gyro_z,
                            dac_1, dac_2, dac_3, dac_4
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                            dataq,
                        )
            dataq.clear()
            conn.commit()
        dataqlock.release()



''' 
def convert_to_decimal(coord, direction):
    coord = float(coord)
    degrees = int(coord / 100)
    minutes = coord - degrees * 100
    decimal = degrees + (minutes / 60)

    if direction in ['S', 'W']:
        decimal *= -1

    return decimal
'''
 
def generate_gps():
    lat = random.uniform(-90.0, 90.0)
    lon = random.uniform(-100.0, 100.0)
    alt = random.uniform(0, 1000)
    return lat, lon, alt

def generate_accel_gyro():
    accel = [random.uniform(-10, 10) for _ in range(3)]
    gyro = [random.uniform(-500, 500) for _ in range(3)]
    return accel, gyro

def generate_dac():
    return [random.uniform(0, 5) for _ in range(4)]

def create_database():
    conn = sqlite3.connect("data_acquisition.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sessionID INTEGER DEFAULT NULL,
        timestamp TEXT,
        latitude REAL,
        longitude REAL,
        altitude REAL,
        accel_x REAL,
        accel_y REAL,
        accel_z REAL,
        gyro_x REAL,
        gyro_y REAL,
        gyro_z REAL,
        dac_1 REAL,
        dac_2 REAL,
        dac_3 REAL,
        dac_4 REAL
    )
    """
    )

    conn.commit()
    conn.close()

def strtof(s):
    fmatch = re.match(r'-?([0-9]*\.[0-9]+)', s, re.S)
    if fmatch is not None:
        return float(fmatch.group(0))
    else:
        return float("NaN")
def read_sensors():
    

    # Force
    ser = serial.Serial('/dev/ttyACM0', 250000)
    # GPS
    #ser1 = serial.Serial('/dev/ttyACM1', 115200)
    # Potentiometers
    ser2 = serial.Serial('/dev/ttyACM2', 115200)
    # 9DOF
    ser3 = serial.Serial('/dev/ttyUSB0', 115200)

    startTime = time.time()
    while (time.time() - startTime) < 1:
        if ser.in_waiting > 0:
            line = ser.readline()
        #if ser1.in_waiting > 0:
            #line1 = ser1.readline()
        if ser2.in_waiting > 0:
            line2 = ser2.readline()
        if ser3.in_waiting > 0:
            line3 = ser3.readline()
    lat, lon, alt = generate_gps()
    accel, gyro = generate_accel_gyro()
    dac = generate_dac()

    session_id = int(datetime.datetime.now().timestamp())
    dataq = []
    dataqthread = threading.Thread(target=dataqcycle, args=(dataq,))
    dataqthread.start()
    try:
        while True:
            timestamp = datetime.datetime.now().isoformat(timespec='milliseconds')
            '''
            if ser.in_waiting > 0:# and ser3.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                sensor = line.split(",")
                dac[2] = sensor[0]
            else:
                dac[2] = "NULL"
            if ser1.in_waiting > 0:
                line1 = ser1.readline().decode('utf-8').rstrip()
                sensor1 = line1.split(",")
                lat = convert_to_decimal(sensor1[1], sensor1[2])
                lon = convert_to_decimal(sensor1[3], sensor1[4]) 
            else:
                lat = "NULL"
                lon = "NULL"
            if ser2.in_waiting > 0:
                line2 = ser2.readline().decode('utf-8').rstrip()
                sensor2 = line2.split(",")
                dac[0] = sensor2[0]
                dac[1] = sensor2[1]
            else:
                dac[0] = "NULL"
                dac[1] = "NULL"
            '''
                #line3 = ser3.readline().decode('utf-8').rstrip()
                #sensor = float(line)
                #sensor3 = line3.split(", ")
            if ser.in_waiting > 0 and ser2.in_waiting > 0 and ser3.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                sensor = line.split(",")
                dac[2] = strtof(sensor[0])
                #line1 = ser1.readline().decode('utf-8').rstrip()
                #sensor1 = line1.split(",")
                #lat = convert_to_decimal(sensor1[1], sensor1[2])
                #lat = sensor1[1]
                #lon = sensor1[3]
                #lon = convert_to_decimal(sensor1[3], sensor1[4]) 
                line2 = ser2.readline().decode('utf-8').rstrip()
                sensor2 = line2.split(",")
                dac[0] = sensor2[0]
                dac[1] = sensor2[1] 
                #print(f"{line2}")           
                line3 = ser3.readline().decode('utf-8').rstrip()
                #sensor = float(line)
                sensor3 = line3.split(",")
                accel[0] = sensor3[0]
                accel[1] = sensor3[1]
                accel[2] = sensor3[2]
                gyro[0] = sensor3[3]
                gyro[1] = sensor3[4]
                gyro[2] = sensor3[5]
                #print(f"{timestamp},{lat},{lon},{accel[0]},{accel[1]},{accel[2]},{dac[0]},{dac[1]},{dac[2]}")
                #print(f"{dac[0]}")
                print(f"{dac[0]},{dac[1]},{dac[2]},{accel[0]},{accel[1]},{accel[2]},{gyro[0]},{gyro[1]},{gyro[2]}")
                dataqlock.acquire()
                dataq.append((
                        session_id,
                        timestamp,
                        lat,
                        lon,
                        alt,
                        accel[0],
                        accel[1],
                        accel[2],
                        gyro[0],
                        gyro[1],
                        gyro[2],
                        dac[0],
                        dac[1],
                        dac[2],
                        dac[3],
                    ))
                dataqlock.release()



    except KeyboardInterrupt:
        print(f"\nTerminated with keyboard interrupt\n")
        sys.exit(0)

if __name__ == "__main__":
    create_database()
    read_sensors()
    print("Database created")
