import logging
from pprint import pprint

def msg_stip(value, prefix):
    return value[len(prefix):].strip("/").split('/')

def send_key(key, tvclient):
    logger = logging.getLogger('sendkey')
    logger.info(f'send {key} to tv.')
    return tvclient.send_key(key)


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

