from django.db import models
from authentication.models import Account
from django import utils

class Task(models.Model):
    task_heading = models.CharField(max_length=200)
    task_description = models.CharField(max_length=200)
    task_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    author = models.ForeignKey(Account, related_name="requestedTasks", blank=True, null=True)
    courier = models.ForeignKey(Account, related_name="acceptedTasks", blank=True, null=True)
    pub_date = models.DateTimeField('date published', default=utils.timezone.now)
    is_completed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    def __unicode__(self):
        return self.task_heading
