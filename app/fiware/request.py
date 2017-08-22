import requests
from django.conf import settings

class Request():
    def __init__(self, serviceAPI, workspace_api, cbroker):
        self.service_api = serviceAPI
        self.workspace_api = workspace_api
        self.cbroker = cbroker

    def sendPostRequest(self, header, data, domain):
        r = requests.post(url=domain, headers=header, data=data)
        if r.text:
            return r.text
        return False

    def sendGetRequest(self, header, domain):
        return True
