import json
import uuid
import datetime

from django.http.response import HttpResponse
from django.db.utils import IntegrityError

from pcr.utils import allow, authenticate, parameter, pagination, PATTERN_UUID_HEX
from battle.models import Battle
from user.models import User
from .models import Strategy



@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'index': {
            'type': 'number',
            'min': 1,
            'max': 5
        },
        'round': {
            'type': 'number',
            'min': 1,
            'max': 26
        },
        'name': {
            'type': 'string',
        },
        'es_damage': {
            'type': 'number',
            'default': 0
        },
        'content': {
            'type': 'string'
        }
    },
    'required': ['index', 'round', 'name', 'content']
})
def create(request):
    try:
        battle = Battle.objects.get(close=None)
    except Battle.DoesNotExist as err:
        return HttpResponse(err, status=400)
    if request.user.guild is None:
        return HttpResponse(content='Guild does not exist', status=400)
    index = request.data.get('index')
    boss = battle.bosses.all()[index-1]
    name = request.data.get('name')
    content = request.data.get('content')
    es_damage = request.data.get('es_damage')
    round = request.data.get('round')
    Strategy.objects.create(battle=battle, boss=boss, round=round, name=name, es_damage=es_damage, content=content)
    return HttpResponse()


@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'id': {
            'type': 'string',
            'pattern': PATTERN_UUID_HEX
        },
        'index': {
            'type': 'number',
            'min': 1,
            'max': 5
        },
        'round': {
            'type': 'number',
            'min': 1,
            'max': 26
        },
        'name': {
            'type': 'string',
        },
        'es_damage': {
            'type': 'number',
            'default': 0
        },
        'content': {
            'type': 'string'
        }
    },
    'required': ['id', 'index', 'round', 'name', 'content']
})
def edit(request):
    try:
        battle = Battle.objects.get(close=None)
    except Battle.DoesNotExist as err:
        return HttpResponse(err, status=400)
    try:
        strategy = Strategy.objects.get(id=uuid.UUID(request.data.get('id')), battle=battle)
    except Strategy.DoesNotExist as err:
        return HttpResponse(err, status=400)      
    index = request.data.get('index')
    data = {
        'name':request.data.get('name'),
        'content': request.data.get('content'),
        'round': request.data.get('round'),
        'es_damage': request.data.get('es_damage'),
    }
    strategy.__dict__.update(**data)
    strategy.boss = strategy.battle.bosses.all()[index-1]
    strategy.save()
    return HttpResponse()


@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'id': {
            'type': 'string',
            'pattern': PATTERN_UUID_HEX
        }
    },
    'required': ['id']
})
def delete(request):
    try:
        battle = Battle.objects.get(close=None)
    except Battle.DoesNotExist as err:
        return HttpResponse(err, status=400)
    try:
        strategy = Strategy.objects.get(id=uuid.UUID(request.data.get('id')), battle=battle)
    except Strategy.DoesNotExist as err:
        return HttpResponse(err, status=400)
    strategy.delete()
    return HttpResponse()


@allow('GET')
@authenticate
def strategy_list(request):
    try:
        battle = Battle.objects.get(close=None)
    except Battle.DoesNotExist as err:
        return HttpResponse('无正在进行的工会战', status=400)
    if request.user.guild is None:
        return HttpResponse('Guild does not exist', status=400)
    
    boss_index = int(request.GET.get('index', default='1'))
    boss = battle.bosses.all()[boss_index-1]
    strategies = boss.strategies.all()
    print(strategies)
    response = {
        'count': strategies.count(),
        'data': [
            strategy.detail for strategy in strategies.order_by('-create').all()
        ]
    }
    return HttpResponse(json.dumps(response), content_type='application/json')