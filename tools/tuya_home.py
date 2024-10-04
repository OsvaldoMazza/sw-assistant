import os
import tinytuya

from management.utils import set_local_value, get_local_value

_device_id = os.getenv('tuya_iot_id')
_device_local_key = os.getenv('tuya_iot_local_key')

class Device:
    def __init__(self, device_id, address=None, local_key=None, data=None):
        self.id = device_id
        self.address = address
        self.local_key = local_key
        self.data = data

class Device:
    def __init__(self, device_id, address, local_key, data=None):
        self.id = device_id
        self.address = address
        self.local_key = local_key
        self.data = data

def get_device(device):
    device = tinytuya.Device(device.id, device.address, device.local_key, version=3.3)
    device.data = device.status()
    
    print('{device.id} status: %r' % device.data['dps']['1'])

    return device

def switch_state(device):
    switch_state = device.data['dps']['1']
    data = device.set_status(not switch_state)
    if data:
        print('Device status changed: %r' % device.data)

def scan():
    return tinytuya.deviceScan()

def get_ip_from_gwId(devices, id):
    for device in devices.values():
        if device.get('gwId') == id:
            return device.get('ip')
    return None

def get_ip(id):
   return get_ip_from_gwId(scan(), id)

def switch_device():
    device_address = get_local_value('iot_device_address')
    if device_address == None:
         print(f"Getting the IP of {_device_id}")
         device_address = get_ip(_device_id)
         print(f"Ip found: {device_address}")
         set_local_value('iot_device_address',device_address)

    device = Device(_device_id, device_address, _device_local_key)

    switch_state(get_device(device))
    