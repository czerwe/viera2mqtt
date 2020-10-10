# viera2mqtt
VieraTV to mqtt

Controll basics with mqtt on an VieraTV. 
Based on https://github.com/florianholzapfel/panasonic-viera


## Topics

topic:
    <prefix>/set/hdmi
payload:
    int - number of hdmi to switch


### Volume Up

topic:
    <prefix>/set/volume/up
payload:
    int - number of times the volume up should be pressed


### Volume Down

topic:
    <prefix>/set/volume/down
payload:
    int - number of times the volume down should be pressed


### Send a key


topic:
    <prefix>/set/key
payload:
    str - key to send see https://github.com/florianholzapfel/panasonic-viera/blob/master/panasonic_viera/__init__.py#L44


