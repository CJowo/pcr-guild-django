import json
import uuid

from django.http.response import HttpResponse
from django.db.utils import IntegrityError

from pcr.utils import allow, authenticate, parameter, pagination, PATTERN_UUID_HEX
from .models import Character

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