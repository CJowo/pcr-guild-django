from django.http.response import HttpResponse

from .settings import DEBUG


class HttpResponseIncorrectParameter(HttpResponse):
    """
    参数错误http响应
    
    Debug == False 时关闭详细错误信息
    """
    status_code = 400

    def __init__(self, content=b'Incorrect parameter', *args, **kwargs):
        if DEBUG is False:
            content = b'Incorrect parameter'
        super().__init__(content=content, *args, **kwargs)