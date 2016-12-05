import RPi.GPIO as GPIO, sys, threading, time, os
from extra_tools.Adafruit_PWM_Servo_Driver import PWM
from extra_tools.sgh_PCF8591P import sgh_PCF8591P

GPIO.setwarnings(False) 

PGNone = 0
PGFull = 1
PGLite = 2
PGType = PGNone 

# Pins 24 and 26 are for the Left Motor
# Pins 19 and 21 control the Right Motor
L1 = 26
L2 = 24
R1 = 19
R2 = 21

ServosActive = False

def init():
    global p, q, a, b, pwm, pcfADC, PGType
    PGType = PGFull
    # Honestly no idea as to why I need this to work. Adafruit documentation tells me it's so I don't fry my device.
    try:
        pwm = PWM(0x40, debug = False)
        pwm.setPWMFreq(60)  # Set frequency to 60 Hz
    except:
        PGType = PGLite # No PCA9685 so set to Pi2Go-Lite

    GPIO.setmode(GPIO.BOARD)

    # the above powermonitor keeps the output at a safe level.
    GPIO.setup(L1, GPIO.OUT)
    p = GPIO.PWM(L1, 20)
    p.start(0)

    GPIO.setup(L2, GPIO.OUT)
    q = GPIO.PWM(L2, 20)
    q.start(0)

    GPIO.setup(R1, GPIO.OUT)
    a = GPIO.PWM(R1, 20)
    a.start(0)

    GPIO.setup(R2, GPIO.OUT)
    b = GPIO.PWM(R2, 20)
    b.start(0)

    # Follow up code to the Powermonitor from before
    pcfADC = None # ADC object
    try:
        pcfADC = sgh_PCF8591P(1) #i2c, 0x48)
    except:
        PGType = PGLite
        
# cleanup time!
def cleanup():
    stop()
    setAllLEDs(0, 0, 0)
    stopServod()
    time.sleep(1)
    GPIO.cleanup()


def version():
    return PGType

def stop():
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(0)
    
# Speed value is set in the motor file for easy access!

def forward(speed):
    p.ChangeDutyCycle(speed)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(speed)
    b.ChangeDutyCycle(0)
    p.ChangeFrequency(speed + 5)
    a.ChangeFrequency(speed + 5)
    
def reverse(speed):
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(speed)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(speed)
    q.ChangeFrequency(speed + 5)
    b.ChangeFrequency(speed + 5)

def spinLeft(speed):
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(speed)
    a.ChangeDutyCycle(speed)
    b.ChangeDutyCycle(0)
    q.ChangeFrequency(speed + 5)
    a.ChangeFrequency(speed + 5)
    
def spinRight(speed):
    p.ChangeDutyCycle(speed)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(speed)
    p.ChangeFrequency(speed + 5)
    b.ChangeFrequency(speed + 5)
    
def turnForward(leftSpeed, rightSpeed):
    p.ChangeDutyCycle(leftSpeed)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(rightSpeed)
    b.ChangeDutyCycle(0)
    p.ChangeFrequency(leftSpeed + 5)
    a.ChangeFrequency(rightSpeed + 5)
    
def turnReverse(leftSpeed, rightSpeed):
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(leftSpeed)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(rightSpeed)
    q.ChangeFrequency(leftSpeed + 5)
    b.ChangeFrequency(rightSpeed + 5)

def go(leftSpeed, rightSpeed):
    if leftSpeed<0:
        p.ChangeDutyCycle(0)
        q.ChangeDutyCycle(abs(leftSpeed))
        q.ChangeFrequency(abs(leftSpeed) + 5)
    else:
        q.ChangeDutyCycle(0)
        p.ChangeDutyCycle(leftSpeed)
        p.ChangeFrequency(leftSpeed + 5)
    if rightSpeed<0:
        a.ChangeDutyCycle(0)
        b.ChangeDutyCycle(abs(rightSpeed))
        p.ChangeFrequency(abs(rightSpeed) + 5)
    else:
        b.ChangeDutyCycle(0)
        a.ChangeDutyCycle(rightSpeed)
        p.ChangeFrequency(rightSpeed + 5)

def goBoth(speed):
    if speed<0:
        reverse(abs(speed))
    else:
        forward(speed)
witch: True==pressed
def getSwitch():
    if PGType == 1:
        val = GPIO.input(switch)
    else:
        val = GPIO.input(Lswitch)
    return (val == 0)

# These servo functions allow the Adafruit libraries in extra_tools to function correctly. 
# Servo Functions

def setServo(Servo, Degrees):
    if ServosActive == False:
        startServos()
    pinServod (Servo, Degrees) # for now, simply pass on the input values

def stopServos():
    stopServod()
    
def startServos():
    startServod()
    
def startServod():
    global ServosActive
    SCRIPTPATH = os.path.split(os.path.realpath(__file__))[0]
    os.system(SCRIPTPATH +'/servod --idle-timeout=20000 --p1pins="18,22"')
    ServosActive = True

def pinServod(pin, degrees):
    os.system("echo " + str(pin) + "=" + str(50+ ((90 - degrees) * 200 / 180)) + " > /dev/servoblaster")
    
def stopServod():
    global ServosActive
    os.system("sudo pkill -f servod")
    ServosActive = False
        


