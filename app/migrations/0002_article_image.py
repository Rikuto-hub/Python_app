# Generated by Django 3.2 on 2021-04-10 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='イマージ画像'),
        ),
    ]
