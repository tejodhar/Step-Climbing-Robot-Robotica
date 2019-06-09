import smbus
import time 
from gpiozero import Motor
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 8
#
GPIO_TRIGGER1 = 25
GPIO_ECHO1 = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
#set gpio pin direction for 2nd ultrasonic sensor

GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
#motors initialization
motor1=Motor(17,27)
motor2=Motor(18,22)
motor3=Motor(12,26)
motor4=Motor(21,20)
motor5=Motor(19,13)
motor6=Motor(5,6)
#steps counting global variable I
i=0
#declaration for MPU6050 sensor
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
kon=2
def MPU_Init():
    
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)
def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)

    #concatenate higher and lower value
    value = ((high << 8) | low)
    
    #to get signed value from mpu6050
    if(value > 32768):
            value = value - 65536
    return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print (" Reading Data of Accelerometer")
#balancing function
def balance(x):
    kon=0
    print("kon= "+str(kon))
    if(x<-0.02):
        motor1.backward(speed=0.28000)
        time.sleep(0.05)
        motor1.stop()
        #time.sleep(1)
        acc_x = read_raw_data(ACCEL_XOUT_H)
        x = acc_x/16384.0
        print("adjusting motor 1...")
        print("\tAx=%.2f g" %x)
        #time.sleep(0.5)
        balance(x)
    elif(x>0.02):
        
        motor2.backward(speed=0.28000)
        time.sleep(0.05)
        motor2.stop()
        #time.sleep(0.5)
        acc_x = read_raw_data(ACCEL_XOUT_H)
        x = acc_x/16384.0
        print("adjusting motor 2")
        print("\tAx=%.2f g" %x)
        #time.sleep(0.5)
        balance(x)
    elif (-0.02<=x<=0.02):
        print("adjusted and returning 1")
        print("\tAx=%.2f g" %x)
        kon=2
        print("kon= "+str(kon))

#finding distance using ultrasonic sensor 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance1 = (TimeElapsed * 34300) / 2
 
    return distance1
def distance_2():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER1, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER1, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO1) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO1) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance2 = (TimeElapsed * 34300) / 2
 
    return distance2

# Main step climbing code 
tim=distance2()
while(tim>=35.0):
    motor3.forward(speed=0.3)
    motor4.forward(speed=0.3)
    motor5.forward(speed=0.3)
    motor6.forward(speed=0.3)
    tim=distance2()

motor3.stop()
motor4.stop()
motor5.stop()
motor6.stop()
time.sleep(0.2)
    
for i in range(1):
    motor1.forward(speed=0.28000)
    motor2.forward(speed=0.30000)
    time.sleep(1.2)
    print("step :"+str(i+1)+" went halfway")
    motor1.stop()
    motor2.stop()
    time.sleep(3)
    acc_x = read_raw_data(ACCEL_XOUT_H)
    Ax = acc_x/16384.0
    print("reading after step "+str(i+1)+" half step .....")
    print("\tAx=%.2f g" %Ax)
    p=Ax
    balance(p)
    time.sleep(1)
    ric=distance()
    print(ric)
    if(0.2<=ric<=15.0 and kon==2):
        print("print afer step"+str(i+1)+"half way system is in equilibrium")
        while(0.2<=ric<=15.5):
            motor1.forward(speed=0.28000)
            motor2.forward(speed=0.30000)
            time.sleep(0.5)
            motor1.stop()
            motor2.stop()
            acc_x = read_raw_data(ACCEL_XOUT_H)
            Ax = acc_x/16384.0
            print("reading after step "+str(i+1)+" half step .....")
            print("\tAx=%.2f g" %Ax)
            y=Ax
            balance(y)
            if kon==2:
                ric=distance()
                print(str(ric)+"distance still")
                acc_x = read_raw_data(ACCEL_XOUT_H)
                Ax = acc_x/16384.0
        print("step :"+str(i+1)+" went full way")
        print(".........")
        #first part of step climbing
        diss_1=distance_2()
        print(diss_1)
        time.sleep(1)
        while(diss_1>=23.0):
            motor3.forward(speed=0.3000)
            motor4.forward(speed=0.3000)
            motor5.forward(speed=0.3000)
            motor6.forward(speed=0.3000)
            diss_1=distance_2()
            print("distance remainig"+str(diss_1))
        #time.sleep(2.5)
        print("1111111")
        motor3.stop()
        motor4.stop()
        motor5.stop()
        motor6.stop()
        #2nd part lifting half part
        time.sleep(1)
        motor2.backward(speed=0.3000)
        time.sleep(7.5)
        motor2.stop()
        print("22222")
        #2nd part forward motion
        diss_2=distance_2()
        while(diss_2>=7.9):
            motor3.forward(speed=0.3000)
            motor5.forward(speed=0.3000)
            motor4.forward(speed=0.3000)
            motor6.forward(speed=0.3000)
            diss_2=distance_2()
        
        #time.sleep(2.4)
        motor3.stop()
        motor4.stop()
        motor5.stop()
        motor6.stop()
        print("33333")
        #2nd motor lifting
       
        

        motor1.backward(speed=0.3000)
        time.sleep(8)
        motor1.stop()
        print("44444")
        #4th actioin of step functioning
        diss_3=distance_2()
        while(diss_3>=32.0):
            motor3.forward(speed=0.3000)
            motor4.forward(speed=0.3000)
            motor5.forward(speed=0.3000)
            motor6.forward(speed=0.3000)
            diss_3=distance_2()
        motor3.stop()
        motor4.stop()
        motor5.stop()
        motor6.stop()
        print("555555")
        print("                                           ")
        print("reading after step "+str(i+1)+" full step")
        print("\tAx=%.2f g" %Ax)
        print("system in equilibrium ")
        print("print step+"+str(i+1)+"climbed succesfully")
        acc_x = read_raw_data(ACCEL_XOUT_H)
        Ax = acc_x/16384.0
        

        print("reading after step "+str(i+1)+" full step")
        print("\tAx=%.2f g" %Ax)
        ric=distance()
        i=i+1
        

        
'''print("completed all "+str(i+1)+"steps")
motor3.forward(speed=0.3000)
motor4.forward(speed=0.3000)
motor5.forward(speed=0.3000)
motor6.forward(speed=0.3000)

time.sleep(0.5)
motor3.stop()
motor4.stop()
motor5.stop()
motor6.stop()'''

print("achieved atep climbing")


        #q=Ax
        #balance(q)
        #time.sleep(2)
        
        #if(kon==2):
            #print("system in equilibrium after step :"+str(i+1))'''


            
            
            
    
        






