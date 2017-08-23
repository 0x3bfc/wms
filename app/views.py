from __future__ import print_function
from django.shortcuts import render,render_to_response
from django.template.context_processors import csrf
from django.template import RequestContext
from .forms import *
from .models import *
from wms import settings
from .fiware import fiware
import random , string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def registerService(request):
    values = {}
    if request.method == 'GET':
        values = {"form": ServiceForm()}
        values.update(csrf(request))
        return render_to_response('registerService.html', values, context_instance=RequestContext(request))
    elif request.method=='POST':
        form = ServiceForm(request.POST)
        if form.is_valid():

            # register service on Orion
            fiware_obj = fiware.Fiware(settings.service_api, settings.workspace_api, settings.cbroker)
            service_data = fiware_obj.registerService(form.cleaned_data['name'])
            if service_data:
                service = Service()
                service.name = form.cleaned_data["name"]
                service.apikey = service_data['apikey']
                service.entity_type = service_data["entity_type"]
                service.resource = service_data["resource"]
                service.cbroker = service_data["cbroker"]
                service.save()
                values["success"] = True
            else:
                values["success"] = False
                form._errors["name"] = ["unable to register service"]
            values["form"] = form
            values.update(csrf(request))
            return render_to_response("registerService.html", values, context_instance=RequestContext(request))



def userView(request):
    servicename = request.GET.get('service', '')
    if servicename == '':
        values = {'noservice':{
                                    'data':'Please provide a service in order to use the system!',
                                    'status':True
                               }
                  }
        return render_to_response("userView.html", values, context_instance=RequestContext(request))
    try:
        service = Service.objects.get(name=servicename)

    except:
        values = {'notfound': {
            'data': '%s is not found' % (servicename),
            'status': True
        }
        }
        return render_to_response("userView.html", values, context_instance=RequestContext(request))

    fiware_obj = fiware.Fiware(settings.service_api, settings.workspace_api, settings.cbroker)
    workspaces = WorkSpace.objects.filter(service=service)
    ws = []
    data = []

    for w in workspaces:
        ws.append(w.entity_name)
    if len(ws) >=1:
        data = fiware_obj.listWorkspaces(servicename, ws)
        if not data:
            data = []
        else:
            data = fiware_obj.filterData(data)


    values = {'data':data,
            'service': servicename}
    return render_to_response("userView.html", values, context_instance=RequestContext(request))



def adminView(request):
    values = {}

    if request.method=='GET':
        values={"form":RegisterForm()}
        values.update(csrf(request))
        return render_to_response("adminView.html", values, context_instance=RequestContext(request))

    elif request.method == 'POST':
        form = RegisterForm(request.POST)


        if form.is_valid():
            fiware_obj = fiware.Fiware(settings.service_api, settings.workspace_api, settings.cbroker)
            service_name = form.cleaned_data['services']
            service = Service.objects.get(name=service_name)
            workspace = WorkSpace()
            workspace.service = service
            ws_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
            workspace.ws_id = ws_id
            workspace_obj = fiware_obj.registerWorkspace(service.apikey,
                                         service.name ,
                                         form.cleaned_data['entity_name'],
                                         settings.entity_type,
                                         ws_id,
                                         settings.protocol,
                                         settings.timezone,
                                         form.cleaned_data['maxsize'],
                                         form.cleaned_data['address'],
                                         form.cleaned_data['location_long'],
                                         form.cleaned_data['location_lat']
                                         )
            if workspace_obj:
                workspace.entity_name = form.cleaned_data['entity_name']
                workspace.protocol = settings.protocol
                workspace.timezone = settings.timezone
                workspace.maxsize = form.cleaned_data['maxsize']
                workspace.address = form.cleaned_data['address']
                workspace.location_long = form.cleaned_data['location_long']
                workspace.location_lat = form.cleaned_data['location_lat']
                workspace.save()
                values["success"] = True
            else:
                values["success"] = False
                form._errors["entity_name"] = ["unable to register workspace"]
        else:
            values["success"] = False
            form._errors["entity_name"] = ["Invalid form!!"]

        values["form"] = form
        values.update(csrf(request))
        return render_to_response("adminView.html", values, context_instance=RequestContext(request))



def device(request):
    values = {}
    # collect api_key and device id
    devices = []
    for s in Service.objects.all():
        for d in WorkSpace.objects.filter(service=s):
            devices.append({'apikey':s.apikey, 'device_id':d.ws_id, 'workspace':d.entity_name, 'address':d.address, 'maxsize':d.maxsize})
    paginator = Paginator(devices, 11)
    try:
        page = request.GET.get('page')
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    values = {'results':results}
    return render_to_response("RFID.html", values, context_instance=RequestContext(request))