from django.contrib.auth.backends import ModelBackend
from pyppp.django.models import UserPPP

class PPPBackend(ModelBackend):
    def authenticate(self, username=None, passcode=''):
        try:
            p = UserPPP.objects.get(user__username=username)
            if p.check_passcode(passcode):
                return p.user
        except UserPPP.DoesNotExist:
            return None
        return None
