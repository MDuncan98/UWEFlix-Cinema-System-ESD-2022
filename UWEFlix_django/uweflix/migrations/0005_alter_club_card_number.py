# Generated by Django 4.0.3 on 2022-03-19 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uweflix', '0004_club_screen_showing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='card_number',
            field=models.IntegerField(),
        ),
    ]
