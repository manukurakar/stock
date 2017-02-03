from __future__ import unicode_literals

from django.db import models

# Create your models here.

class historical_date(models.Model):
    date = models.DateField(default=None,null=True)
    open = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    high = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    low = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    close = models.DecimalField(default=0.0,max_digits=10, decimal_places=2)
    vol = models.IntegerField(default=0)
    type = models.CharField(max_length=5)

    def __unicode__(self):
        return self.type