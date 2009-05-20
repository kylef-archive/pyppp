from django.conf.urls.defaults import *
from django.conf import settings
from pyppp.django.forms import AuthenticationForm, PasscodeForm, LoginWizard

urlpatterns = patterns('',
    url(r'^login/$', LoginWizard([AuthenticationForm, PasscodeForm])),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^card/((?P<card>\d+)/)?$', 'pyppp.django.views.card', name="pyppp_card"),
)

PYPPP_INFO_PAGE = getattr(settings, 'PYPPP_INFO_PAGE', False)
if PYPPP_INFO_PAGE:
    urlpatterns += patterns('pyppp.django.views',
        url(r'^info/$', 'info', name='pyppp_info'),
    )
