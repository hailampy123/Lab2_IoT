import paho.mqtt.client as mqttclient
import time
import json
import math
import random

print("Hello ThingBoard")

TOPICS = ["/bkiot/1913917/status","/bkiot/1913917/led","/bkiot/1913917/pump"]
BROKER_ADDRESS = "mqttserver.tk"
PORT = 1883
USERNAME = "bkiot"
PASSWORD = "12345678"

collect_data = {"temperature" : 0, "humidity" : 0, "min_temperature" : 15.0, "max_temperature" : 60.0, "device_status" : 0}
led_data = {"device" : "LED", "status" : "OFF"}
pump_data = {"device" : "PUMP", "status" : "OFF"}

def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    if message.topic == TOPICS[0]:
        jsonobj = json.loads(message.payload)
        try:
            if jsonobj["device_access"] == 1:
                client.publish(TOPICS[0], json.dumps(collect_data), 1)
                print("line 30 publish:")
                client.publish(TOPICS[1], json.dumps(led_data), 1)
                print("line 32 publish:")
                client.publish(TOPICS[2], json.dumps(pump_data), 1)
        except:
            pass
        collect_data["max_temperature"] = jsonobj["max_temperature"]
        collect_data["min_temperature"] = jsonobj["min_temperature"]
    if message.topic == TOPICS[1]:
        jsonobj = json.loads(message.payload)
        led_data["status"] = jsonobj["status"]
    if message.topic == TOPICS[2]:
        jsonobj = json.loads(message.payload)
        pump_data["status"] = jsonobj["status"]


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        for topic in TOPICS:
            client.subscribe(topic)
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(USERNAME,PASSWORD)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message



while True:
    collect_data["temperature"] = random.randint(0,100)
    collect_data["humidity"] = random.randint(0,100)
    client.publish(TOPICS[0], json.dumps(collect_data), 1)
    time.sleep(5)