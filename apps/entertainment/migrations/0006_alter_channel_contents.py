# Generated by Django 3.2.6 on 2021-09-04 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entertainment', '0005_alter_channel_contents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='contents',
            field=models.ManyToManyField(blank=True, related_name='channels', to='entertainment.Content', verbose_name='contents'),
        ),
    ]