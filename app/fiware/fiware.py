from request import Request
from wms import settings
import random, string


class Fiware():
    def __init__(self, serviceapi, workspaceapi, cbroker):
        self.requester = Request(serviceapi, workspaceapi, cbroker)

    def registerService(self, name):
        try:
            apikey = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
            entity_type = settings.entity_type
            resource = settings.resouce
            cbroker = settings.cbroker
            header = {"Content-type": "application/json",
                      "Fiware-Service": name,
                      "Fiware-ServicePath": "/"}
            data = '{"services":[{"apikey":"%s","cbroker":"%s","entity_type":"%s","resource":"%s"}]}'%(apikey, cbroker, entity_type, resource)
            #raise Exception(data)
            self.requester.sendPostRequest(header, data, settings.service_api)
            return {"apikey":apikey,
                    "entity_type": entity_type,
                    "cbroker": cbroker,
                    "resource": resource,
                    "name":name}
        except:
            return False

    def registerWorkspace(self, apikey, service, workspace, entity, device_id, protocol, timezone, maxsize, address, long, lat):
        try:
            header = {"Content-type": "application/json",
                      "Fiware-Service": service,
                      "Fiware-ServicePath": "/"}
            data = '{"devices": [{"device_id": "%s","entity_name": "%s","entity_type": "%s","protocol": "%s","timezone": "%s","attributes": [{"object_id": "n","name": "name","type": "string"},{"object_id": "a","name": "address","type": "string"},{"object_id": "lat","name": "latitude","type": "string"},{"object_id": "long","name": "longitude","type": "string"},{"object_id": "max","name": "maximumnumber", "type": "int"},{"object_id": "cur","name": "currentstatus","type": "int"}]}]}'%(device_id, workspace, entity, protocol, timezone)

            if self.requester.sendPostRequest(header, data, settings.workspace_api):
                print ("REGISTER DONE!")
                # curl "http://130.206.126.55:7896/iot/d?k=4jggokgpepnvsb2uv4s40d0000&i=112255"
                # -d 'n|cairo lib#a|5 ahmed zewil#lat|25.3#long|23.6#max|50' -H "Content-type: text/plain"
                header = {"Content-type": "text/plain"}
                data = 'n|%s#a|%s#lat|%s#long|%s#max|%s'%(workspace, address, long, lat, maxsize)
                try:
                    self.requester.sendPostRequest(header, data, '%s?k=%s&i=%s'%(settings.device_api, apikey, device_id))
                except:
                    return False
                return True
        except:
            return False

    def listWorkspaces(self):
        return True

    def updateDevices(self):
        return True