# Generated by Django 3.2.10 on 2021-12-28 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=3)),
                ('mode', models.TextField(max_length=3)),
                ('score', models.IntegerField(default=0)),
                ('diff', models.TextField(max_length=6)),
            ],
        ),
    ]
