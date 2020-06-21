import uuid

from django.db import models


class Character(models.Model):
    PATTERN_NAME = r'^[a-z_]{1,32}$'

    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    name = models.CharField(max_length=32)
    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE, related_name='characters')
    rank = models.IntegerField(default=1)
    star = models.IntegerField(default=1)
    exclusive = models.IntegerField(default=0)

    @property
    def detail(self):
        return {
            'id': self.id.hex,
            'name': self.name,
            'rank': self.rank,
            'star': self.star,
            'exclusive': self.exclusive
        }