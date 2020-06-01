from django.db import models


class Admin(models.Model):
    register = models.BooleanField(default=True)
    guild = models.BooleanField(default=True)
    password = models.CharField(max_length=24, default='administrator')

    @property
    def detail(self):
        return {
            'register': self.register,
            'guild': self.guild
        }