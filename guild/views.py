import json
import uuid

from django.http.response import HttpResponse
from django.db.utils import IntegrityError

from pcr.utils import allow, authenticate, parameter, pagination, PATTERN_UUID_HEX
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
@pagination()
def guild_list(request):
    page = request.page
    size = request.size
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
            user.detail for user in guild.users.filter(operate=None).all()
        ],
        'operaters': [
            operater.detail for operater in guild.operaters.all()
        ],
        'owner': guild.owner.detail
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


@allow(['GET'])
@authenticate
def info(request):
    if request.user.guild is None:
        return HttpResponse('Guild does not exist', status=400)
    return HttpResponse(json.dumps(request.user.guild.detail), content_type='application/json')


@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'id': {
            'type': 'string',
            'pattern': PATTERN_UUID_HEX
        },
        'password': {
            'type': 'string',
            'default': Guild.PATTERN_PASSWORD
        },
        'desc': {
            'type': 'string',
            'default': '',
            'pattern': Application.PATTERN_DESC
        }
    },
    'required': ['id']
})
def join(request):
    if request.user.guild is not None:
        return HttpResponse(content=u'Already have a guild', status=400)
    try:
        guild = Guild.objects.get(id=uuid.UUID(request.data.get('id')))
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
            Application.objects.create(guild=guild, user=request.user, status=True)
            request.user.save()
            request.user.applications.filter(status=None).delete()
            return HttpResponse('Successfully joined')
        else:
            return HttpResponse('Incorrect password', status=400)
    if guild.join == Guild.JOIN_AUTO:
        request.user.guild = guild
        Application.objects.create(guild=guild, user=request.user, status=True)
        request.user.save()
        request.user.applications.filter(status=None).delete()
        return HttpResponse('Successfully joined')
    return HttpResponse(status=500)


@allow(['POST', 'GET'])
@authenticate
def leave(request):
    try:
        request.user.manage
    except User.manage.RelatedObjectDoesNotExist:
        request.user.guild = None
        request.user.operate = None
        request.user.save()
        return HttpResponse()
    else:
        return HttpResponse(content=u"You can't leave", status=400)


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
    try:
        request.user.manage
    except User.manage.RelatedObjectDoesNotExist:
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


@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
            'pattern': Guild.PATTERN_NAME
        },
        'desc': {
            'type': 'string',
            'pattern': Guild.PATTERN_DESC
        },
        'join': {
            'type': 'number',
            'min': 0,
            'max': 3
        },
        'password': {
            'type': 'string',
            'pattern': Guild.PATTERN_PASSWORD
        }
    }
})
def edit(request):
    try:
        request.user.manage
    except User.manage.RelatedObjectDoesNotExist:
        return HttpResponse('No permission', status=403)
    try:
        request.user.manage.__dict__.update(**request.data)
        request.user.manage.save()
    except IntegrityError as err:
        return HttpResponse(content=err, status=400)
    return HttpResponse()


@allow(['GET'])
@authenticate
@pagination()
def applications(request):
    user = request.user
    if user.operate is None:
        return HttpResponse('No permission', status=403)
    page = request.page
    size = request.size
    start = size * (page - 1)
    end = size * (page - 1) + size
    applications = user.operate.applications.filter()
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
            'type': 'string',
            'pattern': PATTERN_UUID_HEX
        },
        'allow': {
            'type': 'boolean'
        }
    },
    'required': ['id', 'allow']
})
def validate(request):
    try:
        application = Application.objects.get(id=uuid.UUID(request.data.get('id')), status=None)
    except Application.DoesNotExist as err:
        return HttpResponse(content=err, status=400)
    if request.data.get('allow') is True:
        application.user.guild = application.guild
        application.user.save()
        application.user.applications.filter(status=None).delete()
    application.status = request.data.get('allow')
    application.save()
    return HttpResponse()