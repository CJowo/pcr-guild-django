from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uid = models.CharField(max_length=16, default=u'player')
    level = models.IntegerField(default=0)
    
    @property
    def detail(self):
        return {
            'username': self.username,
            'staff': self.is_staff,
            'superuser': self.is_superuser,
            'id': self.uid,
            'level': self.level,
            'box': [i.detail for i in self.box.all()]
        }