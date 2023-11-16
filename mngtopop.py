from customclass import ONOS
import json
onos_obj = ONOS()

def get_devices():
    hosts = onos_obj.getmethod("hosts")
    #same pass flows in getmethod()
    #print("GET METHOD----------")
    #print(hosts)
    return hosts

#returns the JSON for that particular user. 
def flag_hosts(user):
    hosts = get_devices()
    #print("FLAG METHOD----------------")
    #print(hosts[user])
    return hosts[user]

def flow_rules(deviceID):
    data = {
                "priority": 40000,
                "timeout": 0,
                "isPermanent": "true",
                "deviceId": "",
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
    data["deviceId"]= str(deviceID)
    
    device_url = deviceID.replace('of:','of%3A')
    response = onos_obj.postmethod(device_url,data)
    return response