from django.db import models
from django.contrib.auth.models import User

import hashlib

class ActivationRecord(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=32)
    registration_date = models.DateField(null=True)

    def create_key(self):

        md5 = hashlib.md5()
        md5.update(self.user.email)

        self.key = md5.hexdigest()

        self.save()
