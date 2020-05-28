import uuid

from django.db import models


class Guild(models.Model):
    # 长度1~16
    PATTERN_NAME = r'^.{1,16}$'
    # 长度0~32
    PATTERN_DESC = r'^[\s\S]{0,32}$'
    # 允许数字、字母、特殊符号，长度1~16
    PATTERN_PASSWORD = r'^[a-zA-Z\d\x21-\x7e]{1,16}$'

    # 自动同意
    JOIN_AUTO = 0
    # 密码加入
    JOIN_PASSWORD = 1
    # 验证申请
    JOIN_VALIDATE = 2
    # 禁止加入
    JOIN_FORBID = 3
    JOIN_CHOICES = (
        (JOIN_AUTO, u'Auto'),
        (JOIN_PASSWORD, u'Password'),
        (JOIN_VALIDATE, u'Validate'),
        (JOIN_FORBID, u'Forbid'),
    )

    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    name = models.CharField(max_length=16)
    desc = models.CharField(max_length=32, default=u'')
    create = models.DateTimeField(auto_now_add=True)
    # 加入方式
    join = models.IntegerField(choices=JOIN_CHOICES, default=JOIN_VALIDATE)
    password = models.CharField(max_length=16, null=True, blank=True)
    # 所有者
    owner = models.OneToOneField(to='user.User', on_delete=models.PROTECT, related_name='manage')

    def apply(self, user, desc=u''):
        return Application.objects.create(user=user, guild=self, desc=desc)

    @property
    def detail(self):
        return {
            'id': self.id.hex,
            'name': self.name,
            'desc': self.desc,
            'create': int(self.create.timestamp()),
            'join': self.join,
            'owner': self.owner.detail,
            'number': self.users.count(),
        }
    
    @property
    def members(self):
        def serialize(user):
            detail = user.detail
            detail.update({
            })
            return detail
        
        return [
            serialize(user) for user in self.users
        ]


class Application(models.Model):
    PATTERN_DESC = r'^.{0,32}$'

    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    # 申请描述
    desc = models.CharField(max_length=32)
    # 申请状态
    status = models.BooleanField(null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    guild = models.ForeignKey(to='Guild', on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE, related_name='applications')

    @property
    def detail(self):
        return {
            'id': self.id.hex,
            'status': self.status,
            'user': self.user.detail,
            'guild': self.guild.detail,
            'create': int(self.create.timestamp()),
            'desc': self.desc
        }
    
