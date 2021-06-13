# Generated by Django 3.2 on 2021-06-10 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MainCycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coinsCount', models.IntegerField(default=0)),
                ('clickPower', models.IntegerField(default=1)),
                ('level', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cycle', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Boost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('power', models.IntegerField(default=1)),
                ('price', models.IntegerField(default=10)),
                ('mainCycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boosts', to='user_profile.maincycle')),
            ],
        ),
    ]
