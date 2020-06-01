import json
import uuid
import datetime

from django.http.response import HttpResponse
from django.db.utils import IntegrityError
from django.db.models import Q

from pcr.response import HttpResponseIncorrectParameter
from pcr.utils import allow, authenticate, parameter, pagination, PATTERN_UUID_HEX
from admin.views import admin
from .models import Battle, Boss


@allow(['POST'])
@admin()
@parameter({
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
            'pattern': Battle.PATTERN_TITLE
        }
    },
    'required': ['title']
})
def create(request):
    Battle.objects.filter(close=None).update(close=datetime.datetime.now())
    battle = Battle.objects.create(title=request.data.get('title'))
    for i in range(5):
        Boss.objects.create(index=i, battle=battle)
    return HttpResponse(json.dumps(battle.detail), content_type='application/json')


@allow(['POST'])
@admin()
def close(request):
    Battle.objects.filter(close=None).update(close=datetime.datetime.now())
    return HttpResponse()


@allow(['GET'])
@parameter({
    'type': 'object',
    'properties': {
        'id': {
            'type': 'string',
            'pattern': PATTERN_UUID_HEX
        }
    },
    'required': []
})
def info(request):
    id = request.data.get('id')
    try:
        if id:
            battle = Battle.objects.get(id=request.data.get('id'))
        else:
            battle = Battle.objects.get(close=None)
    except Battle.DoesNotExist as err:
        return HttpResponse('{}', content_type='application/json')
    return HttpResponse(json.dumps(battle.detail), content_type='application/json')


@allow(['GET'])
@authenticate
@pagination()
def battle_list(request):
    page = request.page
    size = request.size
    start = size * (page - 1)
    end = size * (page - 1) + size
    response = {
        'count': Battle.objects.count(),
        'data': [
            battle.detail for battle in battle.objects.order_by('-create').all()[start: end]
        ]
    }
    return HttpResponse(json.dumps(response), content_type='application/json')