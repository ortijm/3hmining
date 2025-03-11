# -*- coding: utf-8 -*-
from .models import BridgeTask, Minera, BridgeResponse, BridgeConnectionLog
import json
import base64
import logging
from datetime import datetime, timedelta
import pytz
from .manager3hToken import DataBridge

logger = logging.getLogger(__name__)

class BridgeCore():

    def __init__(self):
        self.originClient = ""

    def taskList(self, originClient):
        minera = Minera.objects.filter(name=originClient, enabled=True)
        #filtra solo tareas habilitadas enabled=True y de la minera del origen del cliente
        taskList = BridgeTask.objects.filter(bridge=minera, enabled=True)
        logger.info("Existen {}, task para minera {}".format(len(taskList), originClient))
        responseJson = []
        i = 0
        for taskBridge in taskList:
            if self.isTimeToWork(taskBridge):
                taskJson = {}
                typeTask = taskBridge.typeTask
                taskID = "{}:{}".format(typeTask.name, i)
                taskJson[taskID] = {}
                taskDef = base64.b64encode(taskBridge.query.encode('utf-8'))
                if taskBridge.typeTask.name == "dbconfig":
                    taskJson[taskID]['config']= taskDef
                else:
                    taskJson[taskID]["query"]= taskDef
                    taskJson[taskID]["rows"]= "{}".format(taskBridge.rows)
                taskJson[taskID]["idtask"]= "{}".format(taskBridge.id)
                taskJson[taskID]["status"]= "stand by"
                taskJson[taskID]["ping"]=  taskBridge.ping
                responseJson.append(taskJson)
        return json.dumps(responseJson)

    def isTimeToWork(self, taskBridge):
        if BridgeResponse.objects.filter(bridgeRequestTask=taskBridge):
            taskBridgeResponse = BridgeResponse.objects.filter(bridgeRequestTask=taskBridge)[0]
            if taskBridgeResponse:
                lastTimeWithPing = self.pingToDate(taskBridge.ping, taskBridgeResponse.dateResponse)
                now = datetime.utcnow().replace(tzinfo=pytz.UTC)
                logger.debug ("isTimeToWork? => task {}, ping {}, if now {} > now + ping {} = {}".format(taskBridge.name, taskBridge.ping,datetime.now(), lastTimeWithPing, (now > lastTimeWithPing)))
                return now > lastTimeWithPing
            else:
                return True
        else:
            return True

    def pingToDate(self, ping3H, time3h):
        when = ""
        exact = False
        value = ""
        typeTime = ""

        for t in ping3H:
            when += t
            if not t.isdigit():
                exact = True
                typeTime = t
            else:
                value += t
            if exact:
                when = ""
                if typeTime =="h":
                   time3h += timedelta(hours=int(value))
                if typeTime == "m":
                   time3h += timedelta(minutes=int(value))
                if typeTime == "s":
                   time3h += timedelta(seconds=int(value))
                value = ""
                exact = False
        return time3h

    def responseTask(self, dataIn):
        resultJson = json.loads(dataIn.content)
        logger.info(u"{}>>idTask [{}] : Status = '{}' \n {}".format(dataIn.mac,resultJson['IdTask'],resultJson['Status'],resultJson['Resulset3h']))
        idTask = resultJson['IdTask']
        bridgeTask = BridgeTask.objects.filter(id=idTask)[0]
        bridgeRsList = BridgeResponse.objects.filter(bridgeRequestTask=bridgeTask)
        if bridgeRsList:
            bridgeRs = bridgeRsList[0]
        else:
            bridgeRs = BridgeResponse()
        bridgeRs.typeTask = bridgeTask.typeTask
        bridgeRs.bridge = bridgeTask.bridge
        bridgeRs.name = bridgeTask.name
        bridgeRs.bridgeRequestTask = bridgeTask
        bridgeRs.status = resultJson['Status']
        if bridgeRs.status == "OK":
            bridgeRs.response = json.dumps(resultJson['Resulset3h'])
            if 'ResultCount' in resultJson.keys():
                bridgeRs.results = resultJson['ResultCount']
            else:
                bridgeRs.results = len(bridgeRs.response)
        bridgeRs.dateResponse = datetime.utcnow().replace(tzinfo=pytz.UTC)
        bridgeRs.save()
        return "OK"

    def saveAccess(self, request):
        bridgeConnectionLog = BridgeConnectionLog()
        content = request.POST.get('post3HToken')
        if content:
            dataIn = DataBridge(content)
            bridgeConnectionLog.remoteId = dataIn.mac
            if dataIn.originClient:
                bridgeConnectionLog.bridgeName = dataIn.originClient
            else:
                bridgeConnectionLog.bridgeName = "DESCONOCIDO"
        else:
            bridgeConnectionLog.bridgeName = "DESCONOCIDO"
            bridgeConnectionLog.remoteId = self.getRemoteIP(request)
        bridgeConnectionLog.request = self.getRemoteInfo(request.META)
        bridgeConnectionLog.accessTime = datetime.utcnow().replace(tzinfo=pytz.UTC)
        bridgeConnectionLog.save()

    def getRemoteIP(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def getRemoteInfo(self, meta):
        jsonRequest = {}
        jsonRequest['HTTP_ACCEPT_LANGUAGE']= meta.get('HTTP_ACCEPT_LANGUAGE')
        jsonRequest['REMOTE_PORT']= meta.get('REMOTE_PORT')
        jsonRequest['HTTP_X_FORWARDED_FOR']= meta.get('HTTP_X_FORWARDED_FOR')
        jsonRequest['HTTP_USER_AGENT']= meta.get('HTTP_USER_AGENT')
        jsonRequest['HTTP_X_REAL_IP']= meta.get('HTTP_X_REAL_IP')
        jsonRequest['REQUEST_METHOD']= meta.get('REQUEST_METHOD')
        jsonRequest['SERVER_PROTOCOL']= meta.get('SERVER_PROTOCOL')
        jsonRequest['REMOTE_PORT']= meta.get('REMOTE_PORT')
        jsonRequest['REMOTE_ADDR']= meta.get('REMOTE_ADDR')
        jsonRequest['REQUEST_SCHEME']= meta.get('REQUEST_SCHEME')
        jsonRequest['HTTP_X_UA_COMPATIBLE']= meta.get('HTTP_X_UA_COMPATIBLE')
        return jsonRequest