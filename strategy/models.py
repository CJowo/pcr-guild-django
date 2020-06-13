import uuid

from django.db import models

# Create your models here.
class Strategy(models.Model):
    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    name = models.CharField(max_length=50)
    es_damage = models.IntegerField(default=0) # 预估伤害,单位万
    content = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    

    battle = models.ForeignKey('battle.Battle', on_delete=models.CASCADE, related_name='strategies')
    boss = models.ForeignKey('battle.Boss', on_delete=models.CASCADE, related_name='strategies')
    round = models.IntegerField(default=1) # 周目

    @property
    def detail(self):
        return {
            'id': self.id.hex,
            'name': self.name,
            'es_damage': self.es_damage,
            'content': self.content,
            'round': self.round,
            'create': self.create.timestamp(),
        }