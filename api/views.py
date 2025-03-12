#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random

from importlib import import_module

from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse, JsonResponse, Http404

from bridge.models import BridgeResponse
from users.models import UserProfile
from .models import DynamicEndpoint
from .utils import get_graph_data

def usuarios_ingreso(request):
    """
    Vista de login que sera consumida desde el App Android/IOS
    """
    output = {}
    user_login = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        session_mobile = request.POST.get('session_mobile')
        if session_mobile:
            # Validate session_id
            engine = import_module(settings.SESSION_ENGINE)
            session = engine.SessionStore(session_mobile)
            try:
                user_id = session[auth.SESSION_KEY]
                backend_path = session[auth.BACKEND_SESSION_KEY]
                backend = auth.load_backend(backend_path)
                user = backend.get_user(user_id) or auth.models.AnonymousUser()
            except KeyError:
                user = auth.models.AnonymousUser()
            if user.is_authenticated():
                output['status'] = 'ok'
                output['feedback'] = 'Usuario loggeado'
                return HttpResponse(json.dumps(output))

        user = auth.authenticate(username=username, password=password)
        if user:
            if not user.is_active:
                # El usuario fue deshabilitado por algun motivo
                output['error'] = 'Su cuenta se encuentra deshabilitada. Si cree que esto es un error por favor contáctenos.'
            else:
                user_login = True
        else:
            # Password invalido, retornar aviso
            output['error'] = "Email o Contraseña incorrectos."

        if user_login:
            auth.login(request, user)
            profile = UserProfile.objects.get(user=user)
            output['session_mobile'] = request.session.session_key
            output['profile'] = {'first_name': user.first_name, 'last_name': user.last_name,
                                 'app_theme': profile.app_theme, 'bridge_id': profile.bridge.id,
                                 'bridge_name': profile.bridge.name.title()}
            dynamic_endpoints = DynamicEndpoint.objects.filter(bridge=profile.bridge)
            output['endpoints'] = [{'title':e.title, 'url': e.url, 'icon': e.icon} for e in dynamic_endpoints]
            output['status'] = 'ok'
        else:
            output['status'] = 'error'

        return HttpResponse(json.dumps(output))
    else:
        return HttpResponse(status=400)


def logout(request):
    auth.logout(request)
    output = {'status': 'ok'}
    response = HttpResponse(json.dumps(output))
    response.delete_cookie('sessionid')
    return response


def get_endpoints(request):
    user = request.user
    result = {}
    if user:
        profile = UserProfile.objects.get(user=request.user)
        dynamic_endpoints = DynamicEndpoint.objects.filter(bridge=profile.bridge)
        result['endpoints'] = [{'slug':e.slug, 'url': e.url, 'icon': e.icon} for e in dynamic_endpoints]
    return JsonResponse(result)


def overview(request):
    output = {}
    output['main_data'] = [{'title': 'Confluencia', 'value': random.randint(180, 750)},
                           {'title': 'Bronces', 'value': random.randint(250, 900)}]
    mov_mina = random.randint(195, 290)
    alimentacion = mov_mina * 0.3
    output['data'] = {
        'MovMina' : mov_mina,
        'ExMina' : round(mov_mina * 0.8620),
        'MinPlanta' : round(alimentacion),
        'LeyMina' : random.randint(5, 16)/12,
        'MinExtraido' : round(alimentacion * 0.9),
        'ArsenicoPPm' : random.randint(300, 1500)
        }

    return JsonResponse(output, status=200)


def mineview(request):
    output = {
        "lat": -24.271132,
        "lon": -69.070514,
        "name": "MEL",
        "trucks": [
            {
                "lat": -24.271132,
                "lon": -69.070514,
                "title": "SHE055 Tons: 18.345",
                "subtitle": "Ub: F5-3100-234/L1"
            },
            {
                "lat": -24.262866,
                "lon": -69.07605,
                "title": "SHE069 Tons: 25.556",
                "subtitle": "Ub: F5N-3100-123/Mx"
            },
            {
                "lat": -24.271132,
                "lon": -69.070514,
                "title": "SHE075 Tons: 25.556",
                "subtitle": "Ub: F5N-3100-123/Mx"
            },
            {
                "lat": -24.270105,
                "lon": -69.062206,
                "title": "SHE080 Tons: 33.512",
                "subtitle": "Ub: F5N-3100-123/Mx"
            },
            {
                "lat": -24.274512,
                "lon": -69.075206,
                "title": "SHE068 Tons: 45.234",
                "subtitle": "Ub: FXX-3115-123/Mx"
            }
            ]
        }

    return JsonResponse(output, status=200)


def bridgeResponse(request, responseTaskName):
    taskResponse = BridgeResponse.objects.filter(name=responseTaskName)[0]
    #responseJson = json.dumps(taskResponse.response)
    #return JsonResponse(responseJson)
    return HttpResponse(taskResponse.response)


def dynamic_endpoint(request, endpoint):
    user = request.user
    output = {'items': []}
    if user.is_authenticated and user.is_active or (user.is_staff and request.GET['bridge']):
        profile = UserProfile.objects.get(user=request.user)
        bridge = profile.bridge
        if user.is_staff and request.GET.get('bridge'):
            bridge = request.GET.get('bridge')
        if bridge:
            endpoint = DynamicEndpoint.objects.get(slug=endpoint, bridge=bridge)
            graphs = endpoint.graphs.all().order_by('order')
            for graph in graphs:
                extra = json.loads(graph.extra) if graph.extra else {}
                item = {"title": graph.title, "order": graph.order, "type": graph.type, 'decimals': graph.decimals,
                        "min_x": graph.min_x, "max_x": graph.max_x, "min_y": graph.min_y, "max_y": graph.max_y, 'extra': extra}
                item['data'] = get_graph_data(graph.type, graph.data, extra)
                output['items'].append(item)
        else:
            raise Http404
    else:
        raise Http404

    return JsonResponse(output)
