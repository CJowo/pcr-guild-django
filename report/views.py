import json
import uuid
import datetime

from django.http.response import HttpResponse
from django.db.utils import IntegrityError

from pcr.utils import allow, authenticate, parameter, pagination, PATTERN_UUID_HEX
from battle.models import Battle
from .models import Report


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
            'type': 'number'
        },
        'finish': {
            'type': 'string',
            'pattern': Report.PATTERN_DATE
        },
        'value': {
            'type': 'number',
            'default': 0
        },
        'desc': {
            'type': 'string',
            'maxLength': 32
        }
    },
    'required': ['index', 'round', 'finish', 'desc']
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
    if 'finish' in request.data:
        finish = datetime.date(*map(int, request.data.get('finish').split('-')))
    else:
        finish = None
    desc = request.data.get('desc')
    value = request.data.get('value')
    round = request.data.get('round')
    Report.objects.create(battle=battle, value=value, boss=boss, round=round, finish=finish, desc=desc, guild=request.user.guild, user=request.user)
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
            'type': 'number'
        },
        'finish': {
            'type': 'string',
            'pattern': Report.PATTERN_DATE
        },
        'value': {
            'type': 'number',
            'default': 0
        },
        'desc': {
            'type': 'string',
            'maxLength': 32
        }
    },
    'required': ['id', 'index', 'round', 'desc']
})
def edit(request):
    try:
        battle = Battle.objects.get(close=None)
    except Battle.DoesNotExist as err:
        return HttpResponse(err, status=400)
    try:
        report = Report.objects.get(id=uuid.UUID(request.data.get('id')), battle=battle)
    except Report.DoesNotExist as err:
        return HttpResponse(err, status=400)
    if request.user.operate is None:
        if request.user != report.user:
            return HttpResponse('No permission', status=403)
    else:
        if request.user.guild != report.guild:
            return HttpResponse('No permission', status=403)
    index = request.data.get('index')
    data = {
        'desc':request.data.get('desc'),
        'value': request.data.get('value'),
        'round': request.data.get('round'),
        'desc': request.data.get('desc'),
    }
    if 'finish' in request.data:
        data['finish'] = datetime.date(*map(int, request.data.get('finish').split('-')))
    report.__dict__.update(**data)
    report.boss = report.battle.bosses.all()[index-1]
    report.save()
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
        report = Report.objects.get(id=uuid.UUID(request.data.get('id')), battle=battle)
    except Report.DoesNotExist as err:
        return HttpResponse(err, status=400)
    if request.user.operate is None:
        if request.user != report.user:
            return HttpResponse('No permission', status=403)
    else:
        if request.user.guild != report.guild:
            return HttpResponse('No permission', status=403)
    report.delete()
    return HttpResponse()


@allow('GET')
@authenticate
@pagination()
def report_list(request):
    try:
        battle = Battle.objects.get(close=None)
    except Battle.DoesNotExist as err:
        return HttpResponse(err, status=400)
    if request.user.guild is None:
        return HttpResponse('Guild does not exist', status=400)
    page = request.page
    size = request.size
    start = size * (page - 1)
    end = size * (page - 1) + size
    reports = request.user.guild.reports.filter(battle=battle)
    response = {
        'count': reports.count(),
        'data': [
            report.detail for report in reports.order_by('-finish').all()[start: end]
        ]
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


@allow('GET')
@authenticate
@pagination()
def my_list(request):
    page = request.page
    size = request.size
    start = size * (page - 1)
    end = size * (page - 1) + size
    reports = request.user.reports
    response = {
        'count': reports.count(),
        'data': [
            report.detail for report in reports.order_by('-finish').all()[start: end]
        ]
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


@allow('GET')
@authenticate
@pagination()
def today(request):
    try:
        battle = Battle.objects.get(close=None)
    except Battle.DoesNotExist as err:
        return HttpResponse(err, status=400)
    if request.user.guild is None:
        return HttpResponse('Guild does not exist', status=400)
    page = request.page
    size = request.size
    start = size * (page - 1)
    end = size * (page - 1) + size
    now = (datetime.datetime.now() - datetime.timedelta(hours=5)).date()
    response = []
    for user in request.user.guild.users.all():
        count = user.reports.filter(battle=battle, guild=request.user.guild, finish=now).count()
        response.append({
            **user.detail,
            'count': count
        })
    return HttpResponse(json.dumps(response), content_type='application/json')