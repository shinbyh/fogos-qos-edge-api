import paho.mqtt.client as mqtt
tempDevID = 1
def on_connect (client, userdata, flags, rc):
    print ("connected with result code " +str(rc))
    client.subscribe("/configuration/join_ack/#")
    client.subscribe("/configuration/leave_ack/#")
    client.subscribe("/configuration/update_ack/#")
    client.subscribe("/configuration/register_ack/#")
    client.subscribe("/utilization/reply/#")

def on_message(client, userdata, msg):
    print('topic:'+msg.topic + '\nMessage:' + str(msg.payload))

client = mqtt.Client()        # MQTT Client 오브젝트 생성
client.on_connect = on_connect     # on_connect callback 설정
client.on_message = on_message   # on_message callback 설정

client.connect("iot.eclipse.org", 1883, 60)   # MQTT 서버에 연결

client.loop_forever()

