# Generated by Django 3.0.6 on 2020-05-22 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20200522_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default='9528de249bde11ea86ddd46d6df5224b', max_length=36, primary_key=True, serialize=False),
        ),
    ]
