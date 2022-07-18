import tkinter as tk 
from tkinter import filedialog
import matplotlib.pyplot as plt
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ctypes

# @csv reader
header = []
clock = []

imu_posN = []
imu_posE = []
imu_h= []

gps_lat = []
gps_long = []
gps_h =[]

imu1_posN = []
imu1_posE= []
imu1_posD = []

imu_lat = []
imu_long = []


#Window Config
window = tk.Tk()
window.title('FPview v1.0')
window.geometry('720x480')
window.iconbitmap('drone.ico')

#canvas = tk.Canvas(window, height=480, width=720, bg ='#263D42')
#canvas.pack()

frame = tk.Frame(window,bg='white')
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

#Open CSV file
def opf():

    #clear display
    for widget in frame.winfo_children():
        widget.destroy()

    global filename 
    filename = filedialog.askopenfilename(initialdir='/', title = 'Select File',filetypes=(('CSV file', '*.csv'), ('All Files', '*.*')))

    with open(filename, 'r') as f:
        csvreader = csv.DictReader(f)
        global header 
        header = next(csvreader)
        i=0
        for row in csvreader: 
            if float(dict(row)['Clock:offsetTime']) >= 0 & i < 10:
                clock.append(float(dict(row)['Clock:offsetTime']))
                imu_posN.append(float(dict(row)['IMUCalcs(0):PosN:C']))
                imu_posE.append(float(dict(row)['IMUCalcs(0):PosE:C']))
                imu_h.append(abs(float(dict(row)['IMUCalcs(0):height:C'])))

                gps_lat.append(float(dict(row)['GPS:Lat']))
                gps_long.append(float(dict(row)['GPS:Long']))
                gps_h.append(abs(float(dict(row)['GPS:heightMSL'])))

                imu1_posN.append(float(dict(row)['IMUCalcs(1):PosN:C']))
                imu1_posE.append(float(dict(row)['IMUCalcs(1):PosE:C']))
                imu1_posD.append(abs(float(dict(row)['IMUCalcs(1):height:C'])))

                imu_lat.append(float(dict(row)['IMUCalcs(0):Lat:C']))
                imu_long.append(float(dict(row)['IMUCalcs(0):Long:C']))

        i+=1

    label = tk.Label(frame, text=filename, bg='white')
    label.pack()

def plot_imu():
    # 建立 3D 圖形
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    color_code = '#3B80D0'

    z = imu_h
    x = imu_posN
    y = imu_posE

    ax.scatter3D(x[0],y[0],z[0],color = 'green', marker = '.', label='start point')
    ax.scatter3D(x[-1],y[-1],z[-1],color = 'purple', marker = '.', label='end point')
    plt.plot(imu_posN,imu_posE,imu_h,color_code, label = 'imu_0')
    plt.plot(imu1_posN,imu1_posE,imu1_posD, 'red', label = 'imu_1')
    ax.set_xlabel("imu_posN")   
    ax.set_ylabel("imu_posE")
    ax.set_zlabel("imu_height")

    ax.view_init(20, 132)

    plt.title('IMU Flight trajectory')
    plt.legend(loc = 'upper right')
    plt.show()

def xyz_ot():
    # X, Y , Z vs time
    plt.figure(2)
    plt.subplot(131)
    plt.title("posN vs t")
    plt.ylabel('posN')
    plt.xlabel("Time (s)")
    plt.plot(clock,imu_posN)
  

    plt.subplot(132)
    plt.title('posE vs t')
    plt.ylabel('posE')
    plt.xlabel('Time (s)')
    plt.plot(clock, imu_posE)

    plt.subplot(133)
    plt.title('Altitude vs t')
    plt.ylabel('Alt')
    plt.xlabel('Time (s)')
    plt.plot(clock, imu_h)

    plt.show()
    
def plot_gps():
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
    
    plt.title('GPS vs IMU Flight trajectory')
    plt.legend(loc = 'upper right')

    plt.show()

#Title
label = tk.Label(window, text = 'Flight Path Viewer', font = ('Arial', 18), anchor = 'n')
label.place(x=10, y=0)

#Buttons
openFile = tk.Button(window, text = 'Open CSV', padx=10, pady=5,
 fg='white', bg = '#263D42', command = opf)
openFile.place(x=620, y = 0)

b1=tk.Button(window, text="IMU plot", padx=10, pady=5, fg='white', bg='#263D42', command=plot_imu)
b1.place(x=150, y=440)

b2=tk.Button(window, text="Time Series plot", padx=10, pady=5, fg='white', bg='#263D42', command=xyz_ot)
b2.place(x=325, y=440)


b3=tk.Button(window, text="GPS plot", padx=10, pady=5, fg='white', bg='#263D42', command=plot_gps)
b3.place(x=500, y=440)



window.resizable(0, 0) 

# Main
#ctypes.windll.shcore.SetProcessDpiAwareness(1)
window.mainloop()