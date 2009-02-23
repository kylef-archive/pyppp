from django.contrib.auth import login as auth_login
from pyppp.django.models import UserPPP

def login(request, user):
    try:
        p = UserPPP.objects.get(user=user)
        p.count += 1
        p.save()
        auth_login(request, user)
    except UserPPP.DoesNotExist:
        return