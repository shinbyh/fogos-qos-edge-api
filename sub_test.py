# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import mqtt_config

mqtt_broker_addr = mqtt_config.mqtt_broker_addr
mqtt_port = mqtt_config.mqtt_port
tempDevID = 1

def on_connect (client, userdata, flags, rc):
    print ("connected with result code " +str(rc))
    client.subscribe("/configuration/join/#")
    client.subscribe("/configuration/leave/#")
    client.subscribe("/configuration/update/#")
    client.subscribe("/configuration/register/#")
    client.subscribe("/utilization/query/#")

def on_message(client, userdata, msg):
    print('topic: '+msg.topic + '\nMessage: ' + str(msg.payload))

    if('/configuration/join/' in msg.topic):
        split_topic = msg.topic.split('/')
        temp_device_id = split_topic[len(split_topic)-1]
        device_id = 'hfureiwqaghuwf547326'
        payload = {
            'error':0,
            'id': device_id,
            'relay': 'none'
        }
        publish.single("/configuration/join_ack/"+temp_device_id, json.dumps(payload), hostname=mqtt_broker_addr)

    if('/configuration/register/' in msg.topic):
        split_topic = msg.topic.split('/')
        device_id = split_topic[len(split_topic)-1]
        recv_payload = json.loads(str(msg.payload.decode('utf-8')))
        register_id = recv_payload['registerID']

        payload = {
            'error':0,
            'registerID': register_id,
            'idList': [{'0':'3413412vsa'}, {'1':'re34423gdv'},{'2':'3413412vsa'}, {'3':'re34423gdv'}],
            'relay': 'none'
        }
        publish.single("/configuration/register_ack/"+device_id, json.dumps(payload), hostname=mqtt_broker_addr)

def connect_to_msg_bus():
    client = mqtt.Client()        # MQTT Client 오브젝트 생성
    client.on_connect = on_connect     # on_connect callback 설정
    client.on_message = on_message   # on_message callback 설정
    client.connect(mqtt_broker_addr, mqtt_port, 60)   # MQTT 서버에 연결
    client.loop_forever()

#
# Debug: test code
#
if __name__ == '__main__':
    connect_to_msg_bus()
