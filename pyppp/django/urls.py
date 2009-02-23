from django.conf.urls.defaults import *

from pyppp.django.forms import AuthenticationForm, PasscodeForm, LoginWizard

urlpatterns = patterns('',
    url(r'^login/$', LoginWizard([AuthenticationForm, PasscodeForm])),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^card/((?P<card>\d+)/)?$', 'pyppp.django.views.card', name="pyppp_card"),
)