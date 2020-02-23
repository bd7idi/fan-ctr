#coding=utf-8
#!/usr/bin/python
import sys
import time
try:
	import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
def cpu_temp():
    with open("/sys/class/thermal/thermal_zone0/temp", 'r') as f:
        return float(f.read())/1000
def main():
    # Simplex use BCM-->4 pin control the fan 
    channel = 4
    # Duplex use BCM-->17 pin control the fan
    #channel = 17

# GPIO.setmode(GPIO.BOARD)#也许使用扩展board导致标注的数字是BCM的，猜测而已。
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # close air fan first
    GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)
    is_close = True
    while True:
        temp = cpu_temp()
        if is_close:
            if temp > 48.0:
                print time.ctime(), temp, '℃ open air fan'
                GPIO.output(channel, 1)
                is_close = False
        else:
            if temp < 47.0:
                print time.ctime(), temp, '℃ close air fan'
                GPIO.output(channel, 0)
                is_close = True
        time.sleep(2.0)
        print time.ctime(), temp, '℃'
if __name__ == '__main__':
    main()
