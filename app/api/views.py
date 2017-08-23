from app.models import *
from app.fiware import fiware
from wms import settings
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class UpdateStatus(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self,request, format=None):
        try:
            apikey = request.GET.get('apikey')
            device_id = request.GET.get('devid')
            type = request.GET.get('type')
            workspace = WorkSpace.objects.get(ws_id=device_id)
            service = Service.objects.get(apikey=apikey)
            fiware_obj = fiware.Fiware(settings.service_api, settings.workspace_api, settings.cbroker)
            fiware_obj.updateWorkspaceData(service.name, workspace.entity_name, apikey,
                                           device_id, type)
        except:
           return Response({'status':False})
        return Response({'status': True})
