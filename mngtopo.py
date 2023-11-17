from customclass import ONOS
import json
onos_obj = ONOS()

def get_hosts():
    hosts = onos_obj.getmethod("hosts")
    #same pass flows in getmethod()
    #print("GET METHOD----------")
    #print(hosts)
    return hosts

def get_switches():
    devices = onos_obj.getmethod("devices")
    #same pass flows in getmethod()
    #print("GET METHOD----------")
    #print(devices)
    return devices

#returns the JSON for that particular user. 
def get_host(user):
    hosts = get_hosts()
    #print("FLAG METHOD----------------")
    #print(hosts[user])
    return hosts[user]

def enable_flow_rules(deviceID):
    data = {
                "priority": 40000,
                "timeout": 0,
                "isPermanent": "true",
                "deviceId": str(deviceID),
                "treatment": {
                    "instructions": [
                    {
                        "type": "OUTPUT",
                        "port": "CONTROLLER"
                    }
                    ]
                },
                "selector": {
                    "criteria": [
                    {
                        "type": "ETH_TYPE",
                        "ethType": "0x88cc"
                    }
                    ]
                }
    }
    # Update of the device URL
    device_url = deviceID.replace('of:','of%3A')

    # Sending the POST request in order to enable the traffic
    response = onos_obj.postmethod(device_url,data)
    return response


def disable_flow_rules(deviceID):
    data = {
        "priority": 40000,
        "timeout": 0,
        "isPermanent": "true",
        "deviceId": str(deviceID),
        "treatment": {
            "instructions": [
                {
                    "type": "NOACTION"
                }
            ]
        },
        "selector": {
            "criteria": [
                {
                    "type": "ETH_TYPE",
                    "ethType": "0x0"  # We set a non-valid value in order to block all the traffic
                }
            ]
        }
    }

    # Update of the device URL
    device_url = deviceID.replace('of:', 'of%3A')

    # Sending the POST request in order to disable the traffic
    response = onos_obj.postmethod(device_url, data)

    return response