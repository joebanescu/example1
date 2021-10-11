import uuid
from django.db import models

# Create your models here.

class RawData(models.Model):

    date = models.DateField(auto_now_add=True)
    network_app = models.TextField()
    network_campaign = models.TextField(null=True, blank=True)
    network_adgroup = models.TextField(null=True, blank=True)
    taps = models.IntegerField()
    views = models.IntegerField()
    cost = models.FloatField()
    earnings = models.FloatField()

class ParsedData(models.Model):

    internal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.ForeignKey(RawData, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    app = models.TextField()
    campaign = models.TextField(null=True, blank=True)
    ad_group = models.TextField(null=True, blank=True)
    clicks = models.IntegerField()
    impressions = models.IntegerField()
    ad_spend = models.FloatField()
    revenues = models.FloatField()


