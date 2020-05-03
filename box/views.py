import json

from django.http.response import HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse

from .models import Character


class HttpUnauthorized(HttpResponse):
    status_code = 401


def character_add(request):
    """
    添加人物
    URL: /api/character_add/
    Method: POST
    Permission: 登录用户
    Param:
        id: 人物id
    """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # 未登录 401
            return HttpUnauthorized()
        try:
            query = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            # 参数错误 400
            return HttpResponseBadRequest()
        c_id = query.get('id')
        if request.user.box.filter(c_id=c_id):
            # 参数错误
            return HttpResponseBadRequest()
        Character.objects.create(c_id=c_id, rank=8, star=3, max=True, owner=request.user)
        return HttpResponse()
    return HttpResponseNotFound()


def character_remove(request):
    """
    删除人物
    URL: /api/character_remove/
    Method: POST
    Permission: 登录用户
    Param:
        id: 人物id
    """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # 未登录 401
            return HttpUnauthorized()
        try:
            query = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            # 参数错误 400
            return HttpResponseBadRequest()
        c_id = query.get('id')
        if not Character.objects.filter(c_id=c_id):
            # 参数错误
            return HttpResponseBadRequest()
        request.user.box.filter(c_id=c_id).delete()
        return HttpResponse()
    return HttpResponseNotFound()


def character_edit(request):
    """
    修改人物
    URL: /api/character_edit/
    Method: POST
    Permission: 登录用户
    Param:
        id: 人物id
        rank: number
        star: number
        max: boolean 是否满强
    """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # 未登录 401
            return HttpUnauthorized()
        try:
            query = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            # 参数错误 400
            return HttpResponseBadRequest()
        c_id = query.get('id')
        if not Character.objects.filter(c_id=c_id):
            # 参数错误 400
            return HttpResponseBadRequest()
        rank = query.get('rank')
        star = query.get('star')
        maxx = query.get('max')
        character = request.user.box.get(c_id=c_id)
        try:
            character.rank = rank
            character.star = star
            character.max = maxx
            character.save()
            return HttpResponse()
        except ValueError:
            # 参数错误 400
            return HttpResponseBadRequest()
    return HttpResponseNotFound()

