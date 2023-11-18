from customclass import ONOS
import json

onos_obj = ONOS()


def get_hosts():
    hosts = onos_obj.getmethod("hosts")
    # same pass flows in getmethod()
    # print("GET METHOD----------")
    # print(hosts)
    return hosts


def get_switches():
    devices = onos_obj.getmethod("devices")
    # same pass flows in getmethod()
    # print("GET METHOD----------")
    # print(devices)
    return devices


# returns the JSON for that particular user.
def get_host(user):
    hosts = get_hosts()
    # print("FLAG METHOD----------------")
    # print(hosts[user])
    return hosts[user]


def enable_flow_rules(host_IP, device_ID, port):
    IP_host = host_IP + "/32"
    postdata = {
        "priority": 41000,
        "timeout": 0,
        "isPermanent": "true",
        "state": "ADD",
        "deviceId": str(device_ID),
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
                    "ethType": "0x800"
                },
                {
                    "type": "IPV4_SRC",
                    "ip": str(IP_host)
                }, 
                {
                    "type": "IN_PORT",
                    "port": str(port)
                }
            ]
        }
    }
    # Update of the device URL
    device_url = device_ID.replace('of:', 'of%3A')
    # Sending the POST request to enable traffic from the specified host to any other host
    response = onos_obj.postmethod(device_url, postdata)
    return response


def disable_flow_rules(host_IP, device_ID, port):
    IP_host = host_IP + "/32"
    postdata = {
        "priority": 40010,
        "timeout": 0,
        "isPermanent": "true",
        "state": "ADD",
        "deviceId": str(device_ID),
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
                    "ethType": "0x800"
                },
                {
                    "type": "IPV4_SRC",
                    "ip": str(IP_host)
                }, 
                {
                    "type": "IN_PORT",
                    "port": str(port)
                }
            ]
        }
    }
    
    print(device_ID)
    # Update of the device URL
    device_url = device_ID.replace('of:', 'of%3A')
    # Sending the POST request in order to disable the traffic
    response = onos_obj.postmethod(device_url, postdata)

    return response
