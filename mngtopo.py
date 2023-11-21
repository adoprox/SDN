from customclass import ONOS

onos_obj = ONOS()


# Fetches all hosts
def get_hosts():
    hosts = onos_obj.getmethod("hosts")
    return hosts


# Fetches all switches/devices
def get_switches():
    devices = onos_obj.getmethod("devices")
    return devices


# Fetches JSON data for a particular host
def get_host(user):
    hosts = get_hosts()
    return hosts[user]


# Enables flow rules for traffic from a specified host to any other host
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
    device_url = device_ID.replace('of:', 'of%3A')
    response = onos_obj.postmethod(device_url, postdata)
    return response


# Disables flow rules for a specified host to stop traffic
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
    device_url = device_ID.replace('of:', 'of%3A')
    response = onos_obj.postmethod(device_url, postdata)
    return response


# Removes NOACTION flow for a specific login ID and device ID
def disable_no_action(login_ID, deviceID):
    response = onos_obj.autodeletmethod(key="flows", device_ID=deviceID, loginID=login_ID)
    return response
