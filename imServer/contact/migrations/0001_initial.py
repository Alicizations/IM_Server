# Generated by Django 2.2 on 2019-04-27 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('UserID', models.AutoField(primary_key=True, serialize=False)),
                ('Friends', models.CharField(max_length=200)),
            ],
        ),
    ]
