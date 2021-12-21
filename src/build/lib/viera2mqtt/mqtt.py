import logging
import requests
from pprint import pprint

def msg_stip(value, prefix):
    return value[len(prefix):].strip("/").split('/')

def send_key(key, tvclient):
    logger = logging.getLogger('sendkey')
    logger.info(f'send {key} to tv.')
    return tvclient.send_key(key)

def check_tv_online(ip):
    logger = logging.getLogger('tvon')
    response = requests.get(f'http://{ip}:55000/dmr/ddd.xml')
    if  len(response.text) == 0:
        logger.info(f'tv off with status_code {response.status_code}')
        return False
    elif len(response.text) > 0 and response.status_code == 200:
        logger.info(f'tv on with status_code {response.status_code}')
        return True


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logger = logging.getLogger('on_con')
    logger.info("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    config, tvclient = userdata

    logger = logging.getLogger('message')
    payload = msg.payload.decode('utf-8')
    logger.info(f"{msg.topic} - {payload}")
    logger.info(config.mqtt.prefix)
    # print(f"{msg.topic} {str(msg.payload)}")
    action, actiontype, *rest = msg_stip(msg.topic, config.mqtt.prefix)
    
    key = None
    if action == 'set':
        if actiontype == 'hdmi':
            key = f'NRC_HDMI{payload}-ONOFF'.upper()
            send_key(key, tvclient)

        if actiontype == 'volume':
            if rest[0] == 'up':
                key = 'NRC_VOLUP-ONOFF'
            if rest[0] == 'down':
                key = 'NRC_VOLDOWN-ONOFF'

            for x in range(0, int(payload)):
                send_key(key, tvclient)

        if actiontype == 'key':    
            send_key(payload, tvclient)

        if actiontype == 'power':
            key = "NRC_POWER-ONOFF"   
            if payload == "on":
                if not check_tv_online(config.tv.address):
                    send_key(key, tvclient)
            elif payload == "off":
                if check_tv_online(config.tv.address):
                    send_key(key, tvclient)
