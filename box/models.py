from django.db import models


class Character(models.Model):
    c_id = models.CharField(max_length=16)
    rank = models.IntegerField()
    star = models.IntegerField()
    max = models.BooleanField()
    owner = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name='box')

    @property
    def detail(self):
        return {
            'id': self.c_id,
            'rank': self.rank,
            'star': self.star,
            'max': self.max
        }
