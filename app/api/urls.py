from django.conf.urls import include, url
from .views import UpdateStatus

urlpatterns = [
    url(r'^update/$', UpdateStatus.as_view(), name='update status'),
]