from request import Request

class Fiware():
    def __init__(self, serviceapi, workspaceapi, cbroker):
        self.requester = Request(serviceapi, workspaceapi, cbroker)

    def registerService(self):
        return True

    def registerWorkspace(self):
        return True