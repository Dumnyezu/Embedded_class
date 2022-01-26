import pyrebase
import RPi.GPIO as GPIO
import logging
import time
from datetime import datetime, timezone, timedelta

config = {
    "apiKey": "AIzaSyDZGTI2vQjxRPLlxF0_X9ED8bzdEbi7iQk",
    "authDomain": "embedded-systems-class.firebaseapp.com",
    "databaseURL": "https://embedded-systems-class-default-rtdb.europe-west1.firebasedatabase.app/",
    "storageBucket": "embedded-systems-class.appspot.com"
}
redLED = 12                                                                                    #the "redLED" variable refers to the GPIO pin 12 which the red LED is connected on.
blueLED = 19                                                                                   #the "blueLED" variable refers to the GPIO pin 19 which the blue LED is connected on.
greenLED = 18                                                                                  #the "greenLED" variable refers to the GPIO pin 18 which the green LED is connected on.

GPIO.setmode(GPIO.BCM)                                                                         #Set the GPIO Scheme numbering system to the BCM mode.
GPIO.setwarnings(False)                                                                        #disable warnings

GPIO.setup(redLED,GPIO.OUT)                                                                    #set the "redLED" variable pin (12) as an output pin.
GPIO.setup(blueLED,GPIO.OUT)                                                                   #set the "blueLED" variable pin (19) as an output pin.
GPIO.setup(greenLED,GPIO.OUT)                                                                  #set the "greenLED" variable pin (18) as an output pin.

red_pwm = GPIO.PWM(redLED,1000)                                                                #create PWM instance named "red_pwm" with frequency 1000.
blue_pwm = GPIO.PWM(blueLED,1000)                                                              #create PWM instance named "blue_pwm" with frequency 1000.
green_pwm = GPIO.PWM(greenLED,1000)                                                            #create PWM instance named "green_pwm" with frequency 1000.

red_pwm.start(0)                                                                               #start the program with 0% duty cycle (red LED will be OFF).
blue_pwm.start(0)                                                                              #start the program with 0% duty cycle (blue LED will be OFF).
green_pwm.start(0)

class FirebaseError(Exception):
    def __init__(self, error):
        pass


class FirebaseCom():

    def __init__(self):

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self._log = logging.getLogger('Firebase communication')

    def sampleList(self):

        Sample = self.db.child("TKPdrone").child("Sample").get()
        Mode = self.db.child("TKPdrone").child("Mode").get()
        #self._log.debug("Got value of Mode %s", Mode.val())
        #self._log.debug("Got value of Sample %s", Sample.val())
        Sample_strip = Sample.val().strip(",[]")
        Sample_replace = Sample_strip.replace('"', "")
        self.Sample_list = Sample_replace.split(",", 5)
        #self._log.debug("Got value of Sample %s", Sample_list)
        msg = ','.join(map(str, self.Sample_list)) + ',' + Mode.val() + '\n'
        #self._log.debug("msg: %s", msg)
        COM().writeData(msg.encode())
        self._log.debug("msg %s has sent to ArduinoSerial", msg)
        self.db.child("TKPdrone").child("sent").set("0")

    def SamplerDataGet(self):
        self.Sampler = self.db.child("TKPdrone").child("Sampler").get().val().replace('"', "")
        self._log.debug("Sampler: %s ", self.Sampler)
        self.PurposeOfSampling = self.db.child("TKPdrone").child("Purpose_of_sampling").get().val().replace('"', "")
        self._log.debug("PurposeOfSampling: %s ", self.PurposeOfSampling)
        self.Location = self.db.child("TKPdrone").child("Location").get().val().replace('"', "")
        self._log.debug("Location: %s ", self.Location)




    def SendPayload(self):

        try:
            lon, lat, alt, date_time, speed = gps.read_coordinate()

            payload = {
                "timestamp": int(round(time.time() * 1000)),
                "gps_coordinates": {
                    "latitude": lat,
                    "longitude": lon,
                    "altitude": alt
                },
                "location": self.Location,
                "purpose_of_sampling": self.PurposeOfSampling,
                "sampler": self.Sampler,
                "depths": self.Sample_list
            }

            response = remote_connection.send_data(payload)
            logging.info("GPS data payload %s sent", payload)
            logging.info("remote response %s recieved", response)
        except GpsError:
            logging.fatal("no represented gps data")

    def getData(self):
        if (self.db.child("TKPdrone").child("sent").get().val() == "1" and
                self.db.child("TKPdrone").child("Mode").get().val() == "1"):
            self.sampleList()
            self.SamplerDataGet()
            self.SendPayload()

        elif (self.db.child("TKPdrone").child("sent").get().val() == "1" and
                self.db.child("TKPdrone").child("Mode").get().val() == "3"):
            self.sampleList()
            self.SamplerDataGet()
            self.SendPayload()

        elif (self.db.child("TKPdrone").child("sent").get().val() == "1" and
                self.db.child("TKPdrone").child("Mode").get().val() == "2"):
            self.sampleList()
            self.SamplerDataGet()
            self.SendPayload()

def Timezone_delay(UTC_Date_Time):
    utc_time = datetime.strptime(UTC_Date_Time, '%Y-%m-%d %H:%M:%S')
    Date_Time = utc_time + timedelta(hours=8)
    Date_Time = str(Date_Time)
    return Date_Time

if __name__ == "__main__":
    FirebaseCom().getData()