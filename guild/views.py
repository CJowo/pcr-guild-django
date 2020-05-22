import json

from django.http.response import HttpResponse
from django.db.utils import IntegrityError

from pcr.utils import allow, authenticate, parameter
from user.models import User
from .models import Guild, Application

@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
            'pattern': Guild.PATTERN_NAME
        }
    },
    'required': ['name']
})
def create(request):
    if request.user.guild is not None:
        return HttpResponse(content=u'Already have a guild', status=400)
    try:
        guild = Guild.objects.create(**request.data, owner=request.user)
    except IntegrityError as err:
        return HttpResponse(content=err, status=400)
    request.user.guild = guild
    request.user.operate = guild
    request.user.save()
    return HttpResponse()


@allow(['DELETE'])
@authenticate
def delete(request):
    try:
        request.user.manage.delete()
    except User.manage.RelatedObjectDoesNotExist:
        return HttpResponse(content=u'Guild dose not exist', status=400)
    return HttpResponse()


@allow(['GET'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'page': {
            'type': 'number',
            'min': 1,
            'default': 1
        },
        'size': {
            'type': 'number',
            'min': 1,
            'max': 20,
            'default': 10
        }
    }
})
def guild_list(request):
    page = request.data.get('page')
    size = request.data.get('size')
    start = size * (page - 1)
    end = size * (page - 1) + size
    response = {
        'count': Guild.objects.count(),
        'data': [
            guild.detail for guild in Guild.objects.order_by('-create').all()[start: end]
        ]
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


@allow(['GET'])
@authenticate
def users(request):
    if request.user.guild is None:
        return HttpResponse('Guild does not exist', status=400)
    guild = request.user.guild
    response = {
        'users': [
            user.detail for user in guild.users.all()
        ],
        'operaters': [
            operater.detail for operater in guild.operaters.all()
        ],
        'owner': guild.owner.detail
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'id': {
            'type': 'string'
        },
        'password': {
            'type': 'string',
            'default': ''
        },
        'desc': {
            'type': 'string',
            'default': ''
        }
    },
    'required': ['id']
})
def join(request):
    if request.user.guild is not None:
        return HttpResponse(content=u'Already have a guild', status=400)
    try:
        guild = Guild.objects.get(id=request.data.get('id'))
    except Guild.DoesNotExist as err:
        return HttpResponse(content=err, status=400)
    if guild.join == Guild.JOIN_FORBID:
        return HttpResponse('Forbidden to join', status=400)
    if guild.join == Guild.JOIN_VALIDATE:
        if Application.objects.filter(user=request.user, guild=guild, status=None).exists():
            return HttpResponse('Application already exists', status=400)
        guild.apply(request.user, request.data.get('desc'))
        return HttpResponse('Application sent')
    if guild.join == Guild.JOIN_PASSWORD:
        if request.data.get('password') == guild.password:
            request.user.guild = guild
            return HttpResponse('Successfully joined')
        else:
            return HttpResponse('Incorrect password', status=400)
    if guild.join == Guild.JOIN_AUTO:
        request.user.guild = guild
        return HttpResponse('Successfully joined')
    return HttpResponse(status=500)


@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string'
        }
    },
    'required': ['username']
})
def kick(request):
    if request.user.operate is None:
        return HttpResponse('No permission', status=403)
    try:
        user = User.objects.get(username=request.data.get('username'), guild=request.user.operate)
    except User.DoesNotExist as err:
        return HttpResponse(content=err, status=400)
    if user.operate is not None:
        return HttpResponse(content=u'This user cannot be kicked', status=400)
    user.guild = None
    user.save()
    return HttpResponse()


@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string'
        },
        'set': {
            'type': 'boolean'
        }
    },
    'required': ['username', 'set']
})
def operate(request):
    if request.user.manage is None:
        return HttpResponse('No permission', status=403)
    try:
        user = User.objects.get(username=request.data.get('username'), guild=request.user.manage)
    except User.DoesNotExist as err:
        return HttpResponse(content=err, status=400)
    if user == request.user:
        return HttpResponse(content=u'This user cannot be changed', status=400)
    if request.data.get('set') is True:
        user.operate = user.guild
    else:
        user.operate = None
    user.save()
    return HttpResponse()


@allow(['GET'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'page': {
            'type': 'number',
            'min': 1,
            'default': 1
        },
        'size': {
            'type': 'number',
            'min': 1,
            'max': 20,
            'default': 10
        }
    }
})
def applications(request):
    user = request.user
    if user.operate is None:
        return HttpResponse('No permission', status=403)
    page = request.data.get('page')
    size = request.data.get('size')
    start = size * (page - 1)
    end = size * (page - 1) + size
    applications = user.operate.applications.filter(status=None)
    response = {
        'count': applications.count(),
        'data': [
            application.detail for application in applications.order_by('-create').all()[start: end]
        ]
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'id': {
            'type': 'string'
        },
        'allow': {
            'type': 'boolean',
            'pattern': Application.PATTERN_DESC
        },
        'reason': {
            'type': 'string',
            'pattern': Application.PATTERN_REASON,
            'default': ''
        }
    },
    'required': ['id', 'allow']
})
def validate(request):
    try:
        application = Application.objects.get(id=request.data.get('id'), status=None)
    except Application.DoesNotExist as err:
        return HttpResponse(content=err, status=400)
    if request.data.get('allow') is True:
        application.user.guild = application.guild
        application.user.save()
    application.status = request.data.get('allow')
    application.reason = request.data.get('reason')
    application.save()
    return HttpResponse()