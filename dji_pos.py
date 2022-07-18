import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = 'input/dji_flightrecord/'
filename = path + '20220623-17-18.csv' #flight log
out_name = 'output/save.csv' # output data save path

delta_time = 1 #second

df = pd.read_csv(filename, low_memory=False)

for i in range(len(df)):
    #if ((df['time(millisecond)'][i] >0) & (abs(df['height_above_takeoff(meters)'][i]) > 0)):
    if ((df[' OSD.flyTime [s]'][i] >=0)) :
        index = i
        break

print("index= ",index)


# Data Extraction
clock = df[' OSD.flyTime [s]'][index:,].values #timestamp


velN= np.vstack(df[' OSD.xSpeed [MPH]'][index:].values) * 0.44704
#if velN[-1] == 0:
#velN= np.vstack(df[' xSpeed(m/s)'][index:].values)
velE=np.vstack(df[' OSD.ySpeed [MPH]'][index:].values) * 0.44704
velD=np.vstack(df[' OSD.zSpeed [MPH]'][index:].values) * 0.44704

#else:
#    velE=np.vstack(df['IMU_ATTI(0):velE'][index:].values)
#    velD=np.vstack(df['IMU_ATTI(0):velD'][index:].values)

gps_lat = df[' OSD.latitude'][index:].values
gps_long = df[' OSD.longitude'][index:].values
height = abs(df[' OSD.height [ft]'][index:].values) * 0.3048


# Process sensor data
dt = np.diff(clock, prepend=clock[0])

# Calculate position
position = np.zeros((len(clock), 3))

velocity = np.append(np.append(velN, velE, axis =1), velD, axis=1)
for item in range(len(clock)):
    if dt[item] > delta_time:
        dt[item] = delta_time

    position[item] = position[item - 1] + dt[item] * velocity[item]
#print(position)


# Plot position
plt.figure(1)
plt.subplot(311)
plt.plot(clock,position[:,0], "tab:red", label='X')
plt.title("PosN vs time")
plt.ylabel('PosN (m)')
plt.xlabel("Time (s)")
plt.grid()
plt.legend()

plt.subplot(312)
plt.plot(clock, position[:,1], "tab:green", label='Y')
plt.title('PosE vs time')
plt.ylabel('PosE (m)')
plt.xlabel('Time (s)')
plt.grid()
plt.legend()

plt.subplot(313)
plt.plot(clock, abs(position[:,2]), "tab:blue", label = 'Z')
plt.title('Altitude vs time')
plt.ylabel('Alt (m)')
plt.xlabel('Time (s)')
plt.grid()
plt.legend()

# Plot 3D Trajectory
fig3,az = plt.subplots()
fig3.suptitle('Flight trajectory')
az = plt.axes(projection='3d')
az.plot3D(position[:,1],position[:,0],height,c='red', label='imu path')
# Mark start and end point
az.scatter3D(position[:,1][0],position[:,0][0],height[0],color = 'black', marker = '.', label='start point')
az.scatter3D(position[:,1][-1], position[:,0][-1],height[-1],color = 'blue', marker = '.', label='end point')
#az.view_init(28, 130)
az.view_init(27, -109)
az.set_xlabel('Y (m)')
az.set_ylabel('X (m)')
az.set_zlabel('Z (m)')
az.legend()

# Print distance between start and final positions
print("Difference: " + "{:.3f}".format(np.sqrt(position[-1].dot(position[-1]))) + " m")

# Plot GPS data only if it exists
if gps_lat[0] > 0 :
        
    fig5 = plt.figure(3)
    ae = fig5.add_subplot(111, projection = '3d')
    plt.plot(gps_long,gps_lat,height, color = 'blue', label ='gps')
    ae.scatter3D(gps_long[0],gps_lat[0],height[0],color = 'black', marker = '.', label='start point')
    ae.scatter3D(gps_long[-1],gps_lat[-1],height[-1],color = 'red', marker = '.', label='end point')
    ae.view_init(27, -109)
    ae.set_xlabel("long")   
    ae.set_ylabel("lat")
    ae.set_zlabel("altitude")
    ae.set_title("GPS plot")
    plt.legend()


#Write pos data to csv file
headers = ['clock (s)','posX (m)', 'posY (m)', 'posZ (m)']
clock = np.vstack(clock)
position[:,2] = height
out_data = np.append(clock, position, axis = 1)
pd.DataFrame(out_data).to_csv(out_name, header=headers)
print("Position data saved to", out_name)


plt.show()



# 1. intergrate gyro output ( angle += gyro * dt) to get orientation of IMU
# 2. construct rotation matrix that transform accelerometer readings from IMU body frame to world frame
# speed += Acc *dt to get speed
# pos += speed * dt