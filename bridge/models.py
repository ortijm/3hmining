from django.db import models
from django.core.exceptions import ValidationError


class Minera(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=150)
    desc = models.TextField(blank=True, null=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TypeBridgeTask(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=150)
    function = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class BridgeTask(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    typeTask = models.ForeignKey(TypeBridgeTask, blank=True, null=True, default=2, on_delete=models.SET_NULL)
    name = models.CharField(max_length=150)
    desc = models.CharField(max_length=512, null=True)
    query = models.TextField(blank=True, null=True)
    ping = models.CharField(max_length=16, null=True)
    init = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    bridge = models.ForeignKey(Minera, blank=True, null=True, on_delete=models.SET_NULL)
    enabled = models.BooleanField(default=True)
    rows = models.IntegerField(default=300)

    def save(self, force_insert=False, force_update=False):
        #if not self.query.upper().startswith("SELECT"):
        #    raise ValidationError({'query': ('JUST SELECT QUERY!!')})
        # this can, of course, be made more generic
        models.Model.save(self, force_insert, force_update)

    def __str__(self):
        return self.name


class BridgeResponse(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    typeTask = models.ForeignKey(TypeBridgeTask, blank=True, null=True, on_delete=models.SET_NULL)
    bridge = models.ForeignKey(Minera, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=512, null=True)
    name = models.CharField(max_length=150)
    response = models.TextField(blank=True, null=True)
    bridgeRequestTask = models.ForeignKey(BridgeTask, blank=True, null=True, on_delete=models.SET_NULL)
    dateResponse = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    results = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class BridgeConnectionLog(models.Model):
    remoteId = models.CharField(primary_key=True,blank=True,max_length=255)
    bridgeName = models.CharField(max_length=150)
    accessTime = models.DateTimeField(auto_now_add=True)
    request = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.bridgeName
