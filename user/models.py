import hashlib
import uuid

from django.db import models


class User(models.Model):
    # 允许字母、数字、下划线(_)，长度4~24
    USER_PATTERN_USERNAME = r'^[a-zA-Z\d_]{4,24}$'
    # 至少一位字母，至少一位数字，允许特殊符号，长度8~24
    USER_PATTERN_PASSWORD = r'^(?=.*[a-z])(?=.*\d)[a-zA-Z\d\x21-\x7e]{8,24}$'
    # 长度1~16
    USER_PATTERN_NICKNAME = r'^.{1,16}$'
    # 长度0~32
    USER_PATTERN_DESC = r'^.{0,32}$'

    id = models.CharField(max_length=36, default=lambda: uuid.uuid1().hex, primary_key=True)
    username = models.CharField(max_length=24, unique=True)
    password = models.CharField(max_length=64)
    desc = models.CharField(max_length=32, default=u'')
    # 昵称
    nickname = models.CharField(max_length=16)
    # 创建时间
    create = models.DateTimeField(auto_now_add=True)
    # 单次认证token
    token = models.UUIDField(default=uuid.uuid1, unique=True)
    # 绑定QQ
    qq = models.IntegerField(unique=True, blank=True, null=True)
    # 所属公会
    guild = models.ForeignKey(to='guild.Guild', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    # 管理公会
    operate = models.ForeignKey(to='guild.Guild', on_delete=models.SET_NULL, null=True, blank=True, related_name='operaters')

    def set_password(self, password):
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.save(update_fields=['password'])
        return self

    def check_password(self, password) -> bool:
        return self.password == hashlib.sha256(password.encode()).hexdigest()

    def refresh_token(self):
        self.token = uuid.uuid1()
        self.save(update_fields=['token'])
        return str(self.token)

    def check_token(self, token):
        if str(self.token) == token:
            self.refresh_token()
            return True
        return False

    def set_operater(self):
        self.operate = self.guild
        self.save()
    
    def undo_operater(self):
        self.operate = None
        self.save()

    @property
    def detail(self):
        return {
            'username': self.username,
            'nickname': self.nickname,
            'create': int(self.create.timestamp()),
            'desc': self.desc,
            'guild': None if self.guild is None else {
                'id': self.guild.id,
                'name': self.guild.name
            }
        }