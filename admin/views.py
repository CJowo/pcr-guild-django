import functools
import json

from django.http.response import HttpResponse

from pcr.response import HttpResponseIncorrectParameter
from pcr.utils import parameter, allow
from .models import Admin


def admin(validate=True):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            if Admin.objects.count() == 0:
                admin = Admin.objects.create()
            else:
                admin = Admin.objects.all()[0]
            request.admin = admin
            if validate:
                if request.META.get('CONTENT_TYPE') == 'application/json':
                    try:
                        data = json.loads(request.body)
                    except json.decoder.JSONDecodeError as err:
                        return HttpResponseIncorrectParameter(content=err)
                else:
                    data = request.POST
                password = data.get('password')
                if admin.password != password:
                    return HttpResponse('Incorrect password', status=400)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


@allow(['POST'])
@admin()
def validate(request):
    return HttpResponse()


@allow(['GET'])
@admin(False)
def info(request):
    return HttpResponse(json.dumps(request.admin.detail), content_type='application/json')


@allow(['POST'])
@admin()
@parameter({
    'type': 'object',
    'properties': {
        'newPassword': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 24
        }
    },
    'required': ['newPassword']
})
def password(request):
    request.admin.password = request.data.get('newPassword')
    request.admin.save()
    return HttpResponse()


@allow(['POST'])
@admin()
@parameter({
    'type': 'object',
    'properties': {
        'register': {
            'type': 'boolean'
        },
        'guild': {
            'type': 'boolean'
        },
        'APP_ID': {
            'type': 'string',
            'maxLength': 16
        },
        'API_KEY': {
            'type': 'string',
            'maxLength': 32
        },
        'SECRET_KEY': {
            'type': 'string',
            'maxLength': 32
        },
    },
    'required': []
})
def edit(request):
    request.admin.__dict__.update(**request.data)
    request.admin.save()
    return HttpResponse(json.dumps(request.admin.detail), content_type='application/json')