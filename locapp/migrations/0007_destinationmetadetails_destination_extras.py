# Generated by Django 3.0.8 on 2021-04-10 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locapp', '0006_destinationmetadetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='destinationmetadetails',
            name='destination_extras',
            field=models.CharField(default='hi', max_length=200),
            preserve_default=False,
        ),
    ]
