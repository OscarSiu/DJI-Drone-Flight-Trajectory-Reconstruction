import pandas as pd
import matplotlib.pyplot as plt


filename = 'FLY061.csv'

df = pd.read_csv(filename, low_memory=False)
i=0
for i in range(len(df)):
    if df['Clock:offsetTime'][i] >0:
        index = i
        break
print("index= ",index)

clock = df['Clock:offsetTime'][index:].values

imu_posN = df['IMUCalcs(0):PosN:C'][index:].values
imu_posE = df['IMUCalcs(0):PosE:C'][index:].values
imu_h = df['IMUCalcs(0):height:C'][index:].values

gps_lat = df['GPS:Lat'][index:].values
gps_long = df['GPS:Long'][index:].values
gps_h = abs(df['GPS:heightMSL'][index:].values)

imu1_posN = df['IMUCalcs(1):PosN:C'][index:].values
imu1_posE = df['IMUCalcs(1):PosE:C'][index:].values
imu1_posD = abs(df['IMUCalcs(1):height:C'][index:].values)

imu_lat = df['IMUCalcs(0):Lat:C'][index:].values
imu_long = df['IMUCalcs(0):Long:C'][index:].values

roll,pitch,yaw = [], [], []
magX,magY,magZ = [], [], []
gyroX, gyroY, gyroZ = [], [], []
accX, accY, accZ = [], [], []
velN, velE, velD = [], [], []


roll = df['IMU_ATTI(0):roll:C'][index:].values
pitch= df['IMU_ATTI(0):pitch:C'][index:].values
yaw = df['IMU_ATTI(0):yaw:C'][index:].values

accX = df['IMU_ATTI(0):accelX'][index:].values
accY =df['IMU_ATTI(0):accelY'][index:].values
accZ =df['IMU_ATTI(0):accelZ'][index:].values

gyroX = df['IMU_ATTI(0):gyroX'][index:].values
gyroY =df['IMU_ATTI(0):gyroY'][index:].values
gyroZ =df['IMU_ATTI(0):gyroZ'][index:].values
            
magX =df['IMU_ATTI(0):magX'][index:].values
magY =df['IMU_ATTI(0):magY'][index:].values
magZ =df['IMU_ATTI(0):magZ'][index:].values

velN= df['IMU_ATTI(0):velN'][index:].values
velE=df['IMU_ATTI(0):velE'][index:].values
velD=df['IMU_ATTI(0):velD'][index:].values

# 建立 3D 圖形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
color_code = '#3B80D0'


 # 產生 3D 座標資料
z = imu_h
x = imu_posN
y = imu_posE

# 繪製 3D 座標點
ax.scatter3D(x[0],y[0],z[0],color = 'green', marker = '.', label='start point')
ax.scatter3D(x[-1],y[-1],z[-1],color = 'purple', marker = '.', label='end point')
plt.plot(x,y,z,color_code, label = 'imu_0')
plt.plot(imu1_posN,imu1_posE,imu1_posD, 'red', label = 'imu_1')
ax.set_xlabel("imu_posN")   
ax.set_ylabel("imu_posE")
ax.set_zlabel("imu_height")

ax.view_init(20, 132)

plt.title('IMU Flight trajectory')
plt.legend(loc = 'upper right')


# X, Y , Z vs time
plt.figure(2)
plt.subplot(131)
plt.title("posN over time")
plt.ylabel('posN')
plt.xlabel("clock")
plt.plot(clock,x)
  

plt.subplot(132)
plt.title('posE over time')
plt.ylabel('posE')
plt.xlabel('clock')
plt.plot(clock, y)

plt.subplot(133)
plt.title('height over time')
plt.ylabel('Height')
plt.xlabel('clock')
plt.plot(clock, z)

#GPS plot
fig3 = plt.figure(3)
az = fig3.add_subplot(111, projection = '3d')
plt.plot(gps_lat,gps_long,gps_h, color = 'green', label ='gps')
plt.plot(imu_lat, imu_long,imu_h,color = 'blue', label = 'imu')

az.scatter3D(gps_lat[0],gps_long[0],gps_h[0],color = 'black', marker = '.', label='start point')
az.scatter3D(gps_lat[-1],gps_long[-1],gps_h[-1],color = 'red', marker = '.', label='end point')
az.view_init(28, 130)
az.set_xlabel("lat")   
az.set_ylabel("long")
az.set_zlabel("altitude")

#az.set_xlim([22.3758, 22.3766])
#az.set_ylim([114.1798,114.18])

plt.title('GPS vs IMU Flight trajectory')
plt.legend(loc = 'upper right')


#yaw, pitch, roll, vel plot
plt.figure(4)
plt.subplot(231)
plt.title("pitch over time")
plt.ylabel('pitch')
plt.xlabel("clock")
plt.plot(clock,pitch)
  

plt.subplot(232)
plt.title('Roll over time')
plt.ylabel('roll')
plt.xlabel('clock')
plt.plot(clock, roll)

plt.subplot(233)
plt.title('Yaw over time')
plt.ylabel('Yaw')
plt.xlabel('clock')
plt.plot(clock, yaw)

plt.subplot(234)
plt.title('VelN over time')
plt.ylabel('VelN')
plt.xlabel('clock')
plt.plot(clock, velN)

plt.subplot(235)
plt.title("velE over time")
plt.ylabel('velE')
plt.xlabel("clock")
plt.plot(clock,velE)
  
plt.subplot(236)
plt.title('velD over time')
plt.ylabel('velD')
plt.xlabel('clock')
plt.plot(clock, velD)


#acc, gyro,mag 2d plot
plt.figure(5)
plt.subplot(331)
plt.title("AccelX over time")
plt.ylabel('Accel X')
plt.xlabel("clock")
plt.plot(clock,accX)
  

plt.subplot(332)
plt.title('AccelY over time')
plt.ylabel('Accel Y')
plt.xlabel('clock')
plt.plot(clock, accY)

plt.subplot(333)
plt.title('Accel Z over time')
plt.ylabel('AccelZ')
plt.xlabel('clock')
plt.plot(clock, accZ)

plt.subplot(334)
plt.title("gyroX over time")
plt.ylabel('gyroX')
plt.xlabel("clock")
plt.plot(clock,gyroX)

plt.subplot(335)
plt.title('gyroY over time')
plt.ylabel('gyroY')
plt.xlabel('clock')
plt.plot(clock, gyroY)

plt.subplot(336)
plt.title('gyroZ over time')
plt.ylabel('gyroZ')
plt.xlabel('clock')
plt.plot(clock, gyroZ)

plt.subplot(337)
plt.title("magX over time")
plt.ylabel('magX')
plt.xlabel("clock")
plt.plot(clock,magX)
  

plt.subplot(338)
plt.title('magY over time')
plt.ylabel('magY')
plt.xlabel('clock')
plt.plot(clock, magY)

plt.subplot(339)
plt.title('magZ over time')
plt.ylabel('magZ')
plt.xlabel('clock')
plt.plot(clock, magZ)



plt.show()