from __future__ import print_function
import json, uuid
from django.shortcuts import render,render_to_response
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from .models import *
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import *
from .models import *
from wms import settings
from .fiware import fiware
import random , string

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
    values = {}
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
            service = Service.objects.get(name="fiwareservice")
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