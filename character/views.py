import json
import uuid

from django.http.response import HttpResponse
from django.db.utils import IntegrityError
import numpy
import cv2
from aip import AipOcr

from pcr.utils import allow, authenticate, parameter, pagination, PATTERN_UUID_HEX
from .models import Character
from .utils import BoxImage
from admin.views import admin

@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
            'pattern': Character.PATTERN_NAME
        },
        'rank': {
            'type': 'number',
            'min': 1
        },
        'star': {
            'type': 'number',
            'min': 1,
            'max': 6
        },
        'exclusive': {
            'type': 'number',
            'min': 0
        }
    },
    'required': ['name']
})
def create(request):
    if request.user.characters.filter(name=request.data.get('name')).exists():
        return HttpResponse(content='Character already exists', status=400)
    try:
        character = Character.objects.create(**request.data, user=request.user)
    except IntegrityError as err:
        return HttpResponse(content=err, status=400)
    return HttpResponse(json.dumps(character.detail), content_type='application/json')


@allow(['POST'])
@authenticate
@parameter({
    'type': 'object',
    'properties': {
        'id': {
            'type': 'string',
            'pattern': PATTERN_UUID_HEX
        },
        'rank': {
            'type': 'number',
            'min': 1
        },
        'star': {
            'type': 'number',
            'min': 1,
            'max': 6
        },
        'exclusive': {
            'type': 'number',
            'min': 0
        }
    },
    'required': ['id']
})
def edit(request):
    try:
        character = request.user.characters.filter(id=uuid.UUID(request.data.get('id')))
        character.update(**request.data)
    except (IntegrityError, Character.DoesNotExist) as err:
        return HttpResponse(content=err, status=400)
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
        character = request.user.characters.get(id=uuid.UUID(request.data.get('id')))
        character.delete()
    except Character.DoesNotExist as err:
        return HttpResponse(content=err, status=400)
    return HttpResponse()


@allow(['POST'])
@authenticate
@admin(False)
def image(request):
    file_obj = request.FILES.get('file')
    buf = numpy.asarray(bytearray(file_obj.read()))
    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    APP_ID = request.admin.APP_ID
    API_KEY = request.admin.API_KEY
    SECRET_KEY = request.admin.SECRET_KEY
    client = None
    if SECRET_KEY and API_KEY and APP_ID:
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    box = BoxImage(image=img, client=client)
    return HttpResponse(json.dumps(box.characters), content_type='application/json')