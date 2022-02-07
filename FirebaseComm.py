import pyrebase
import RPi.GPIO as GPIO
import logging
import time
from datetime import datetime, timezone, timedelta

config = {
    "apiKey": "AIzaSyAsihnuak9mBCZA-CIFXZNsOjCHjozqRI0",
    "authDomain": "embedded-class2.firebaseapp.com",
    "databaseURL": "https://embedded-class2-default-rtdb.firebaseio.com/",
    "storageBucket": "embedded-class2.appspot.com"
}
redLED = 12                            #the "redLED" variable refers to the GPIO pin 12 which the red LED is connected on.
blueLED = 19                            #the "blueLED" variable refers to the GPIO pin 19 which the blue LED is connected on.
greenLED = 18                           #the "greenLED" variable refers to the GPIO pin 18 which the green LED is connected on.


class FirebaseError(Exception):
    def __init__(self, error):
        pass


class FirebaseCom():

    def __init__(self):

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self._log = logging.getLogger('Firebase communication')
        GPIO.setmode(GPIO.BCM)  # Set the GPIO Scheme numbering system to the BCM mode.
        GPIO.setwarnings(False)  # disable warnings

        GPIO.setup(redLED, GPIO.OUT)  # set the "redLED" variable pin (12) as an output pin.
        GPIO.setup(blueLED, GPIO.OUT)  # set the "blueLED" variable pin (19) as an output pin.
        GPIO.setup(greenLED, GPIO.OUT)  # set the "greenLED" variable pin (18) as an output pin.

        self.red_pwm = GPIO.PWM(redLED, 50)  # create PWM instance named "red_pwm" with frequency 1000.
        self.blue_pwm = GPIO.PWM(blueLED, 50)  # create PWM instance named "blue_pwm" with frequency 1000.
        self.green_pwm = GPIO.PWM(greenLED, 50)  # create PWM instance named "green_pwm" with frequency 1000.

        self.red_pwm.start(0)  # start the program with 0% duty cycle (red LED will be OFF).
        self.blue_pwm.start(0)  # start the program with 0% duty cycle (blue LED will be OFF).
        self.green_pwm.start(0)

    def setLEDs(self):

        self.redValue = self.db.child("LEDctrl").child("RED").get().val()
        self.greenValue = self.db.child("LEDctrl").child("GREEN").get().val()
        self.blueValue = self.db.child("LEDctrl").child("BLUE").get().val()
        self.FreqValue = self.db.child("LEDctrl").child("freq").get().val()
        if (int(self.FreqValue) == 0):
            self.FreqValue = "10"
        elif (int(self.FreqValue) > 0):            
            self.red_pwm.ChangeFrequency(int(self.FreqValue))
            self.green_pwm.ChangeFrequency(int(self.FreqValue))
            self.blue_pwm.ChangeFrequency(int(self.FreqValue))
            self.db.child("LEDctrl").child("ack").set("0")
            self._log.debug("Got value of redValue %s", self.redValue)
            #self._log.debug("Got value of Sample %s", Sample.val())
            while(self.db.child("LEDctrl").child("ack").get().val() == "0"):
                self.red_pwm.ChangeDutyCycle(int(self.redValue))
                self.green_pwm.ChangeDutyCycle(int(self.greenValue))
                self.blue_pwm.ChangeDutyCycle(int(self.blueValue))


    def getData(self):
        self.ack = self.db.child("LEDctrl").child("ack").get().val()
        self.powerstate = self.db.child("LEDctrl").child("powerState").get().val()
        self._log.debug("Got value of powerstate %s", self.powerstate)
        if (self.powerstate == "1" and self.ack == "1"):

            self.setLEDs()
    
    def LEDtest(self):
        
        while True:
            
            redValue = 50
            greenValue = 50
            blueValue = 50
        
            self.red_pwm.ChangeDutyCycle(redValue)
            self.green_pwm.ChangeDutyCycle(greenValue)
            self.blue_pwm.ChangeDutyCycle(blueValue)    


def Timezone_delay(UTC_Date_Time):
    utc_time = datetime.strptime(UTC_Date_Time, '%Y-%m-%d %H:%M:%S')
    Date_Time = utc_time + timedelta(hours=8)
    Date_Time = str(Date_Time)
    return Date_Time

if __name__ == "__main__":
    FirebaseCom().LEDtest()