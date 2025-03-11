#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import json

from django.http import HttpResponse
from .manager3hToken import Encript3hTokenUtil, DataBridge
from .bridge3h import BridgeCore
import logging

logger = logging.getLogger(__name__)


def taskUp(request):
    return HttpResponse("OK")

def hi3H(request):
    bridge = BridgeCore()
    bridge.saveAccess(request)
    dataIn = DataBridge(request.POST.get('post3HToken'))
    token3H = Encript3hTokenUtil()
    response = token3H.encript3h("Hi {}".format(dataIn.originClient))
    return HttpResponse(response)

def taskIn(request):
    content = request.POST.get('post3HToken')
    bridge = BridgeCore()
    bridge.saveAccess(request)
    dataIn = DataBridge(content)
    response = bridge.responseTask(dataIn)
    return HttpResponse(response)

def taskOut(request):
    token3H = Encript3hTokenUtil()
    dataOut = DataBridge(request.POST.get('post3HToken'))
    bridge = BridgeCore()
    task_list = bridge.taskList(dataOut.originClient)
    if task_list:
        response3hToken = task_list
        return HttpResponse(token3H.encript3h(response3hToken))
    else:
        return HttpResponse("")
