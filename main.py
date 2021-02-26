from obd import *
import time
import threading
from tkinter import *
import datetime
#obd.logger.setLevel(obd.logging.DEBUG)

glob_rpm = 0
glob_speed = 0
glob_fuel = 0
glob_coolant = 0
glob_air =0
connection=0


class threadOBD(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        

    def run(self):
        global glob_rpm
        global glob_fuel
        global glob_speed
        global glob_coolant
        global connection
        global glob_air
        time_fuel = 0
        time_speed = 0
        while True:
            new_time=time.time()
            glob_rpm=connection.query(obd.commands.RPM).value.magnitude
            glob_speed=connection.query(obd.commands.SPEED).value.magnitude
            
            

            #once every 15 seconds check the fuel level and air temp
            if new_time-time_fuel > 15:
                glob_coolant=connection.query(obd.commands.COOLANT_TEMP).value.magnitude
                glob_fuel=connection.query(obd.commands.FUEL_LEVEL).value.magnitude
                glob_air=connection.query(obd.commands.AMBIANT_AIR_TEMP).value.magnitude
                time_fuel = new_time
                




#function to move rpm
def move(rpm):
        new_y=0
        old_y=canvas.coords(rect)
        
        if rpm >= 0 and rpm < 1000:
                step= float(43/1000)
                new_y=int(-1*step*(rpm))
        elif rpm >= 1000 and rpm < 2000:
                step= float((86-53)/1000)
                new_y=int(-1*step*(rpm-1000))-53
        elif rpm >= 2000 and rpm < 3000:
                step= float((129-96)/1000)
                new_y=int(-1*step*(rpm-2000))-96
        elif rpm >= 3000 and rpm < 4000:
                step= float((174-139)/1000)
                new_y=int(-1*step*(rpm-3000))-139
        elif rpm >= 4000 and rpm < 5000:
                step= float((216-183)/1000)
                new_y=int(-1*step*(rpm-4000))-183
        elif rpm >= 5000 and rpm < 6000:
                step= float((270-225)/1000)
                new_y=int(-1*step*(rpm-5000))-225
        elif rpm >= 6000:
                new_y=-272
        else:
                new_y=0

        delta = old_y[3] -new_y-333
        canvas.move(rect,0,-delta)

def speed_pos():
    global glob_speed
    if glob_speed < 100 and glob_speed >= 20:
        x_speed = 292
        y_speed = 183
    elif glob_speed >=10 and glob_speed<20:
        x_speed = 317
        y_speed = 183
    elif glob_speed < 10:
        x_speed = 330
        y_speed = 183
    else:
        x_speed = 280
        y_speed = 183
    return x_speed,y_speed


def fuel_display():
    global glob_fuel
    if glob_fuel < 10:
        canvas.itemconfigure(b1,state='hidden')
        canvas.itemconfigure(b2,state='hidden')
        canvas.itemconfigure(b3,state='hidden')
        canvas.itemconfigure(b4,state='hidden')
    elif glob_fuel < 25 and glob_fuel >=10:
        canvas.itemconfigure(b1,state='normal')
        canvas.itemconfigure(b2,state='hidden')
        canvas.itemconfigure(b3,state='hidden')
        canvas.itemconfigure(b4,state='hidden')
    elif glob_fuel >= 25 and glob_fuel<50:
        canvas.itemconfigure(b1,state='normal')
        canvas.itemconfigure(b2,state='normal')
        canvas.itemconfigure(b3,state='hidden')
        canvas.itemconfigure(b4,state='hidden')
    elif glob_fuel >= 50 and glob_fuel<75:
        canvas.itemconfigure(b1,state='normal')
        canvas.itemconfigure(b2,state='normal')
        canvas.itemconfigure(b3,state='normal')
        canvas.itemconfigure(b4,state='hidden')
    else:
        canvas.itemconfigure(b1,state='normal')
        canvas.itemconfigure(b2,state='normal')
        canvas.itemconfigure(b3,state='normal')
        canvas.itemconfigure(b4,state='normal')


def time_position(h,m):
    count=0
    x=0
    y=90
    tmp = list(str(h))
    tmp2=list(str(m))
    if h=='00' and m=='00':
        x=325
        return x,y
    
    if tmp[0]=='1':
        count+=1
    if tmp[1]=='1':
        count+=1
    if tmp2[0]=='1':
        count+=1
    if tmp2[1]=='1':
        count+=1
    if count==0:
        x=328
    elif count==1:
        x=332
    elif count==2:
        x=336
    elif count==3:
        x=340
    else:
        x=340
    return x,y

def gear_pos():
    global glob_speed
    global glob_rpm
    
    x=342
    y=235
    gear="N"
    if glob_speed==0 or glob_rpm==0:
        return gear, x, y
    
    res = glob_rpm/glob_speed
    
    if res >= 100:
        x=348
        gear="1"
    elif res>=55 and res <=75:
        gear="2"
    elif res>=33 and res <=45:
        gear="3"
    elif res>=25 and res <=32:
        gear="4"
    elif res>=15 and res <=24:
        gear="5"
    elif res <15:
        gear="N"
    return gear,x,y
        
    

            
   

if __name__=="__main__":
    connection=obd.OBD()


    thread_OBD = threadOBD()
    thread_OBD.start()

    
    

    #GUI
    root = Tk()

    frame = Frame(root)
    frame.pack()


    canvas = Canvas(frame, width=711, height=400)
    canvas.pack()


    wallpaper = PhotoImage(file="Images/wallpaper.png")
    wall=canvas.create_image(0,0,anchor=NW,image=wallpaper)

    tachimetro = PhotoImage(file="Images/tachimetro.png")
    canvas.create_image(0,0,anchor=NW,image=tachimetro)

    rect=canvas.create_rectangle(410,56,558,333,fill="#050b18")


    base = PhotoImage(file="Images/base.png")
    canvas.create_image(0,0,anchor=NW,image=base)

    benza1 = PhotoImage(file="Images/1.png")
    b1=canvas.create_image(0,0,anchor=NW,image=benza1)
    benza2 = PhotoImage(file="Images/2.png")
    b2=canvas.create_image(0,0,anchor=NW,image=benza2)
    benza3 = PhotoImage(file="Images/3.png")
    b3=canvas.create_image(0,0,anchor=NW,image=benza3)
    benza4 = PhotoImage(file="Images/4.png")
    b4=canvas.create_image(0,0,anchor=NW,image=benza4)

    hour_label = canvas.create_text(328,90, anchor=NW, text="", fill="#5cd2ff",font=("Angelinatta Personal Use Only",17))
    
    air_label = canvas.create_text(205,67,anchor=NW,fill="#5cd2ff", font=("Paladins",12))

    cons_label = canvas.create_text(145,128,anchor=NW,fill="#5cd2ff", font=("Paladins",12))

    gear_label = canvas.create_text(348,235,anchor=NW,fill="#5cd2ff", font=("Paladins",15),text=1)
    
    bordi = PhotoImage(file="Images/bordi.png")
    canvas.create_image(0,0,anchor=NW,image=bordi)

    #speed canvas --- paladins
    speed_label=canvas.create_text(0,0,anchor=NW,fill="#50c0ff", font=("Paladins",35))

    time_upd_fuel = 0
    #GUI while loop
    while True:
        #modify rpm position
        move(int(glob_rpm))
        #compute speed position
        x_speed,y_speed = speed_pos()
        canvas.coords(speed_label,x_speed,y_speed)
        #set speed
        canvas.itemconfigure(speed_label, text=str(int(glob_speed)))

        

        #update gear
        gear, x_gear,y_gear = gear_pos()
        canvas.itemconfigure(gear_label,text=str(gear))
        canvas.coords(gear_label,x_gear,y_gear)
            

        #update fuel images every 15 seconds
        if time.time()-time_upd_fuel>15:
            fuel_display()
            time_upd_fuel = time.time()
            #update coolant
            cons = int(glob_coolant)
            canvas.itemconfigure(cons_label, text=str(cons))

            #hour and minute update
            hour = datetime.datetime.now().hour
            if int(hour) < 10 and len(str(hour))<2:
                hour = "0"+str(hour)

            minute = datetime.datetime.now().minute
            if int(minute) < 10 and len(str(minute))<2:
                minute = "0"+str(minute)

            
            full_time = str(hour)+":"+str(minute)
            
            x_time,y_time=time_position(str(hour),str(minute))

            #update position and text of time label
            canvas.itemconfigure(hour_label, text=full_time)
            canvas.coords(hour_label,x_time,y_time)

            
            #air temp update
            canvas.itemconfigure(air_label, text=glob_air)

        

        root.update()

	


    #stop thread obd
    thread_OBD.join()
    
    
