from django.db import models


class Admin(models.Model):
    register = models.BooleanField(default=True)
    guild = models.BooleanField(default=True)
    password = models.CharField(max_length=24, default='administrator')
    APP_ID = models.CharField(max_length=16, null=True)
    API_KEY = models.CharField(max_length=32, null=True)
    SECRET_KEY = models.CharField(max_length=32, null=True)

    @property
    def detail(self):
        return {
            'register': self.register,
            'guild': self.guild
        }