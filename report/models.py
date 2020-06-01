import uuid

from django.db import models


class Report(models.Model):
    PATTERN_DATE = r'^\d\d\d\d-\d\d-\d\d$'
    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    value = models.IntegerField(default=0)
    finish = models.DateField(null=True, blank=True)
    desc = models.CharField(default='', max_length=32)
    round = models.IntegerField(default=0)

    user = models.ForeignKey('user.User', on_delete=models.PROTECT, related_name='reports')
    battle = models.ForeignKey('battle.Battle', on_delete=models.CASCADE, related_name='reports')
    boss = models.ForeignKey('battle.Boss', on_delete=models.CASCADE, related_name='reports')
    guild = models.ForeignKey('guild.Guild', on_delete=models.CASCADE, related_name='reports')

    @property
    def detail(self):
        return {
            'id': self.id.hex,
            'value': self.value,
            'round': self.round,
            'index': self.boss.index+1,
            'finish': self.finish.strftime("%Y-%m-%d") if self.finish is not None else None,
            'desc': self.desc,
            'user': self.user.detail,
        }
    

