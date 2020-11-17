

import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
import time
from datetime import datetime
import json
import random
#from colorit import *
# import boto3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

# datetime object containing current date and time

airConditioningIsOn = False;
temp = random.choice([-65, -70])
DELTA = 0.75
dist=random.uniform(1000,2000)
deviceId='12343212'

connflag = False


# /**
#  * This function will decrease the temperature by the DELTA
#  * value set. It also rounds the number to the nearest
#  * 2 decimal places.
#  */

# def shadowState():
#     response = client.get_thing_shadow(
#     thingName=thingName)
#     print(response)
def increaseTemperature(temp):
    temp = round((temp + DELTA) * 100) / 100;  
    print("Temperature is rising")
    return temp
def decreaseTemperature(temp):
    temp = round((temp - DELTA) * 100) / 100;
    print("Cooling down the temperature")
    return temp
    
def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
# def text(temp):
#     if(temp>-70):
#         print("Temperature rising")
#     else:
#         print("Temperature is ok")

#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))
# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
  print()
  print('UPDATE: $aws/things/' + SHADOW_HANDLER +
    '/shadow/update/#')
  print("payload = " + payload)
  print("responseStatus = " + responseStatus)
  print("token = " + token)
  
# def run():
#     now = datetime.now()
#     d = now.strftime("%m/%d/%Y, %H:%M:%S")
#     if(airConditioningIsOn):
#         decreaseTemperature(temp)
#     else:
#         increaseTemperature(temp)
#     listu={'deviceId':deviceId,'time':d,'temp':temp,'dist':dist}
#     payload = json.dumps(listu, separators=(',', ':'))
#     mqttc.publish("rfid", payload, qos=1)
#     print(temp,airConditioningIsOn)
    

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log
SHADOW_CLIENT = "Thermostat"
SHADOW_HANDLER = "Thermostat"
awshost = "a34shxdjresocf-ats.iot.us-west-2.amazonaws.com"
awsport = 8883
clientId = "Thermostat"
thingName = "Thermostat"
caPath = "AmazonRootCA1.pem.txt"
certPath = "certificate.pem"
keyPath = "private.key"
# client=boto3.client('iot-data')

myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(awshost, 8883)
myShadowClient.configureCredentials(caPath, keyPath,
  certPath)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()
myDeviceShadow = myShadowClient.createShadowHandlerWithName(SHADOW_HANDLER, True)

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

while 1==1:
    if connflag == True:
        
        # temp= str(round(random.normalvariate(mean_temp, 10),1))
        now = datetime.now()
        d = now.strftime("%m/%d/%Y, %H:%M:%S")
        if(airConditioningIsOn):
            temp=decreaseTemperature(temp)
        else:
            temp=increaseTemperature(temp)
        listu={'deviceId':deviceId,'temp':temp,'dist':dist,'time':d}
        payload = json.dumps(listu, separators=(',', ':'))
        mqttc.publish("readings", payload, qos=1)
        dist-=7
        print(temp,airConditioningIsOn)
        if(temp>-65):
            myDeviceShadow.shadowUpdate('{"state":{"reported":{"airConditioningIsOn": true}}}',myShadowUpdateCallback, 5)
            airConditioningIsOn=True
        elif(temp<-75):
            myDeviceShadow.shadowUpdate('{"state":{"reported":{"airConditioningIsOn": false}}}', myShadowUpdateCallback, 5)
            airConditioningIsOn=False
        time.sleep(8)
        
    else:
        print("waiting for connection...")
        




