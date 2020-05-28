import json
import uuid

from django.http.response import HttpResponse
from django.db.utils import IntegrityError

from pcr.utils import allow, authenticate, parameter
from .models import User


@allow(['POST'])
@parameter({
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string',
            'pattern': User.USER_PATTERN_USERNAME
        },
        'password': {
            'type': 'string',
            'pattern': User.USER_PATTERN_PASSWORD
        },
        'nickname': {
            'type': 'string',
            'pattern': User.USER_PATTERN_NICKNAME
        }
    },
    'required':['username', 'password', 'nickname']
})
def register(request):
    try:
        user = User.objects.create(**request.data)
    except IntegrityError as err:
        return HttpResponse(content=err, status=400)
    user.set_password(request.data.get('password'))
    return HttpResponse()


@allow(['POST'])
@parameter({
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        }
    },
    'required':['username', 'password']
})
def login(request):
    username = request.data.get('username')
    password =request.data.get('password')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(content='Username does not exist', status=400)
    if user.check_password(password) is False:
        return HttpResponse(content='Incorrect username or password', status=400)
    request.session['user_id'] = user.id.hex
    return HttpResponse(json.dumps(user.detail), content_type='application/json')


@allow(['POST', 'GET'])
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return HttpResponse()


@allow(['GET'])
@authenticate
def info(request):
    return HttpResponse(json.dumps(request.user.detail), content_type='application/json')


@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'nickname': {
            'type': 'string',
            'pattern': User.USER_PATTERN_NICKNAME
        },
        'desc': {
            'type': 'string',
            'pattern': User.USER_PATTERN_DESC
        },
    }
})
def edit(request):
    try:
        request.user.__dict__.update(**request.data)
        request.user.save()
    except IntegrityError as err:
        return HttpResponse(content=err, status=400)
    return HttpResponse()


@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'password': {
            'type': 'string',
            'pattern': User.USER_PATTERN_PASSWORD
        },
        'new_password': {
            'type': 'string',
            'pattern': User.USER_PATTERN_PASSWORD
        },
    },
    'required':['password', 'new_password']
})
def set_password(request):
    password = request.data.get('password')
    new_password = request.data.geet('new_password')
    if request.user.check_password(password) is False:
        return HttpResponse(content='Incorrect password', status=400)
    request.user.set_password(new_password)
    return HttpResponse()


@allow(['POST', 'GET'])
@authenticate
def refresh_token(request):
    token = request.user.refresh_token()
    return HttpResponse(json.dumps({'token': token}), content_type='application/json')
