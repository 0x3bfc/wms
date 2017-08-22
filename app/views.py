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
from django.conf import  settings
from .fiware import fiware

def registerService(request):

    if request.method == 'GET':
        values = {"form": ServiceForm()}
        values.update(csrf(request))
        return render_to_response('registerService.html')
    elif request.method=='POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            #TODO
            # register service on Orion
            fiware_obj = fiware.Fiware(settings.service_api, settings.workspace_api, settings.cbroker)
            service = Service()
            service.name = form.cleaned_data["name"]
            service.apikey = "jlkajlkdfdsoifsdfsdfsjdoi"
            service.entity_type = settings.entity_type
            service.resource = settings.resouce
            service.cbroker = settings.cbroker
            service.save()



"""
    name = models.CharField(max_length=50, null=True)
    apikey=models.CharField(max_length=100, null=True)
    cbroker = models.CharField(max_length=50, null=True)
    entity_type = models.CharField(max_length=50, null=True)
    resource = models.CharField(max_length=50, null=True)


"""


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
            print ("hello")
            #TODO
        return render_to_response("adminView.html", values, context_instance=RequestContext(request))




"""
def register(request):
    values={}
    if request.method=="GET":
        values={"form":RegisterForm()}
        values.update(csrf(request))
        return render_to_response("pages/register.html",values,
        context_instance=RequestContext(request))
    elif request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password1"]==form.cleaned_data["password2"]:
                from .models import adminUser, User
                user=adminUser()
                user.username=form.cleaned_data["username"]
                user.email=form.cleaned_data["email"]
                user.first_name=form.cleaned_data["firstname"]
                user.last_name=form.cleaned_data["lastname"]
                user.set_password(form.cleaned_data["password1"])
                user.save()
                uuid_value = uuid.uuid4()

                subscription = Subscription.objects.create(uuid="%.32x" %uuid_value,
                                                           name="DilenySubscription")
                subscription.save()
                subscription_id = Subscription.objects.get(uuid="%.32x" %uuid_value)

                ourUser = User()
                ourUser.user = user
                ourUser.subscription_id = subscription_id
                ourUser.save()
                values["success"]=True
            else:
                form._errors["password2"]=["The passwords don't match."]
        values["form"]= form
        values.update(csrf(request))
        return render_to_response("pages/register.html",values,context_instance = RequestContext(request))

"""