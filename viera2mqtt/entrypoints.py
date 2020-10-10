import click
import os
import panasonic_viera
import json
import logging
from .config import Config
from pprint import pprint
import paho.mqtt.client as mqtt
from .mqtt import on_connect, on_message

@click.group()
@click.option('--tv', '-t', default=os.environ.get('V2M_HOST', None), help='TV Hostname or ip')
@click.option('--mqttbroker', '-b', default=os.environ.get('V2M_MQTTBROKER', None), help='MQTT Broker hostname ip')
@click.option('--mqttport', '-p', default=os.environ.get('V2M_MQTTPORT', None), help='MQTT Port')
@click.option('--mqttprefix', default=os.environ.get('V2M_MQTTPREFIX', None), help='MQTT Port')
@click.option('--authid', default=os.environ.get('V2M_AUTHID', None), help='TV Authid')
@click.option('--authkey', default=os.environ.get('V2M_AUTHKEY', None), help='TV Authkey')
@click.pass_context
def cli(ctx, tv, mqttbroker, mqttport, mqttprefix, authid, authkey):
    ctx.obj = dict()
    ctx.obj['config'] = Config("v2m_config.json")

    ctx.obj['config'].set('tv', {}, overwrite=False)
    ctx.obj['config'].tv.set('address', tv)


    if authid:
        ctx.obj['config'].tv.set('id', authid)

    if authkey:
        ctx.obj['config'].tv.set('key', authkey)


    ctx.obj['config'].set('mqtt', {}, overwrite=False)
    ctx.obj['config'].mqtt.set('broker', mqttbroker)

    if not mqttport:
        if not ctx.obj['config'].mqtt.port:
            ctx.obj['config'].mqtt.set('port', 1883)
    else:
        ctx.obj['config'].mqtt.set('port', int(mqttport))


    if not mqttprefix:
        if not ctx.obj['config'].mqtt.prefix:
            ctx.obj['config'].mqtt.set('prefix', "viera2mqtt")
    else:
        ctx.obj['config'].mqtt.set('prefix', mqttprefix.strip('/'))

    ctx.obj['config'].write()


@cli.command()
@click.pass_context
def start(ctx):
    logger = logging.getLogger('start')

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    tv_connection = panasonic_viera.RemoteControl(ctx.obj['config'].tv.address, app_id=ctx.obj['config'].tv.id, encryption_key=ctx.obj['config'].tv.key)


    client.user_data_set([ctx.obj['config'], tv_connection])
    client.connect(ctx.obj['config'].mqtt.broker, ctx.obj['config'].mqtt.port, 60)

    set_topic = os.path.join(ctx.obj['config'].mqtt.prefix, 'set', "#")
    logger.info(f'subscribe to "{set_topic}"')

    client.subscribe(set_topic, qos=1)

    client.loop_forever()



@cli.command()
@click.pass_context
def login(ctx):
    """ Request interactiv login key from TV."""
    if get_auth_config(ctx.obj['config']):
        if click.confirm('There is already an auth pair configured'):
            rc = panasonic_viera.RemoteControl(ctx.obj['tv'])
            rc.request_pin_code()
            pin = click.prompt('Enter the displayed pin code', type=int)

            rc.authorize_pin_code(pincode=pin)
            ctx.obj['config'].set('auth', {}, overwrite=False)

            ctx.obj['config'].set('tv', {}, overwrite=False)
            ctx.obj['config'].tv.set('id', rc.app_id)
            ctx.obj['config'].tv.set('key', rc.enc_key)
            ctx.obj['config'].write()
