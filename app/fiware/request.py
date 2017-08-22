import requests
from django.conf import settings

class Request():
    def __init__(self, serviceAPI, workspace_api, cbroker):
        self.service_api = serviceAPI
        self.workspace_api = workspace_api
        self.cbroker = cbroker

    def sendPostRequest(self):
        return True

    def sendGetRequest(self):
        return True
