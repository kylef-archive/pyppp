from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from pyppp import PyPPP

class UserPPP(models.Model, PyPPP):
    user = models.ForeignKey(User, unique=True)
    key = models.CharField(max_length=64, blank=True)
    count = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.generate_random_sequence_key()
        super(UserPPP, self).save(*args, **kwargs)
    
    def get_current_sequence_info(self):
        return self.get_sequence_info(self.count)
    
    def check_passcode(self, passcode):
        return (passcode == self.retrieve_passcode(self.count))

def create_ppp(sender, instance=None, **kwargs):
    if instance:
        ppp, created = UserPPP.objects.get_or_create(user=instance)

post_save.connect(create_ppp, sender=User)