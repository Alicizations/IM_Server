# Generated by Django 2.2 on 2019-05-06 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content_image',
            name='Cimage',
            field=models.ImageField(upload_to='img'),
        ),
    ]
