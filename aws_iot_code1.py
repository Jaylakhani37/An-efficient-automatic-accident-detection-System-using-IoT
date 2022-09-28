# importing libraries
import paho.mqtt.client as paho
import os
import socket
import ssl
import random
import string
import json
import RPi.GPIO as GPIO
import time
from time import sleep
from random import uniform

connflag = False


def on_connect(client, userdata, flags, rc):  # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc))


def on_message(client, userdata, msg):  # Func for Sending msg
    print(msg.topic + " " + str(msg.payload))


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str


def getMAC(interface='eth0'):
    # Return the MAC address of the specified interface
    try:
        str = open('/sys/class/net/%s/address' % interface).read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]


def getEthName():
    # Get name of the Ethernet interface
    try:
        for root, dirs, files in os.walk('/sys/class/net'):
            for dir in dirs:
                if dir[:3] == 'enx' or dir[:3] == 'eth':
                    interface = dir
    except:
        interface = "None"
    return interface


# def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()  # mqttc object
mqttc.on_connect = on_connect  # assign on_connect func
mqttc.on_message = on_message  # assign on_message func
# mqttc.on_log = on_log

#### Change following parameters ####
awshost = "a3ctdkc91s6vwj-ats.iot.us-east-1.amazonaws.com"  # Endpoint
awsport = 8883  # Port no.
clientId = "Raspberry"  # Thing_Name
thingName = "Raspberry"  # Thing_Name
caPath = "/home/pi/certs/raspberry.cert.pem"  # Root_CA_Certificate_Name
certPath = "/home/pi/certs/cd9e4ec2f27a1ecec09093690d774d9509e77bc174487354469c37c223aeccea-certificate.pem.crt"  # <Thing_Name>.cert.pem
keyPath = "/home/pi/certs/cd9e4ec2f27a1ecec09093690d774d9509e77bc174487354469c37c223aeccea-private.pem.key"  # <Thing_Name>.private.key

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)  # pass parameters

mqttc.connect(awshost, awsport, keepalive=60)  # connect to aws server

mqttc.loop_start()  # Start the loop

BUTTON_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        time.sleep(0.1)
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button is pressed")
            while 1 == 1:
                sleep(5)
                if connflag == True:
                    latitude = 23.186752
                    longitude = 72.629168

                    message = "Your Vehicle is crashed and Your Vehicle Number is :  GJ-XXXX-XX"
                    
                    

                    paylodmsg0 = "{"
                    paylodmsg1 = "\"latitude\": \""
                    paylodmsg2 = "\", \"longitude\":"
                    paylodmsg3 = ", \"Message\": \""
                    paylodmsg4 = "\"}"
                    paylodmsg = "{} {} {} {} {} {} {} {}".format(paylodmsg0, paylodmsg1, latitude, paylodmsg2, longitude,
                                                                 paylodmsg3, message, paylodmsg4)
                    paylodmsg = json.dumps(paylodmsg)
                    paylodmsg_json = json.loads(paylodmsg)
                    mqttc.publish("ElectronicsInnovation", paylodmsg_json,
                                  qos=1)  # topic: temperature # Publishing Temperature values
                    print("msg sent: ElectronicsInnovation")  # Print sent temperature msg on console
                    print(paylodmsg_json)

                else:
                    print("waiting for connection...")
            else:
                print("Please press button.")
except KeyboardInterrupt:
    GPIO.cleanup()