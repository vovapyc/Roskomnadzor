from django.db import models


class ProhibitedIP(models.Model):
    address = models.GenericIPAddressField('IP address', unique=True)
    approved = models.BooleanField('Approved', default=False)

    def approve(self):
        self.approved = True
        self.save()
