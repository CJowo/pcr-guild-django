import uuid

from django.db import models


class Battle(models.Model):
    PATTERN_TITLE = r'^.{1,24}$'

    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    title = models.CharField(default='', max_length=24)
    create = models.DateTimeField(auto_now_add=True)
    close = models.DateTimeField(null=True, blank=True)

    @property
    def detail(self):
        return {
            'id': self.id.hex,
            'title': self.title,
            'create': self.create.timestamp(),
            'close': self.close.timestamp() if self.close is not None else None,
            'bosses': [
                boss.id.hex for boss in self.bosses.order_by('index').all()
            ]
        }


class Boss(models.Model):
    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    index = models.IntegerField()
    battle = models.ForeignKey(to='Battle', on_delete=models.CASCADE, related_name='bosses')
    

