# Generated by Django 3.2.6 on 2021-09-01 21:32

import apps.base.field
import apps.entertainment.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is deleted')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted at')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.CharField(max_length=255, verbose_name='slug')),
                ('language', models.CharField(choices=[('tr', 'Turkish'), ('en-us', 'English')], max_length=5, verbose_name='language')),
                ('picture', models.ImageField(upload_to=apps.entertainment.models.update_picture, verbose_name='picture')),
            ],
            options={
                'verbose_name': 'channel',
                'verbose_name_plural': 'channels',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is deleted')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted at')),
                ('file', models.FileField(upload_to=apps.entertainment.models.update_file, verbose_name='file')),
                ('filename', models.CharField(max_length=500, verbose_name='original filename')),
                ('file_code', models.UUIDField(verbose_name='file code')),
                ('content_type', models.CharField(max_length=50, verbose_name='mime type')),
            ],
            options={
                'verbose_name': 'content',
                'verbose_name_plural': 'contents',
            },
        ),
        migrations.CreateModel(
            name='MetaData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, verbose_name='key')),
                ('value', models.CharField(max_length=500, verbose_name='value')),
            ],
            options={
                'verbose_name': 'metadata',
                'verbose_name_plural': 'metadatas',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', apps.base.field.IntegerRangeField(verbose_name='rate')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_ratings', to='entertainment.content')),
            ],
            options={
                'verbose_name': 'rating',
                'verbose_name_plural': 'ratings',
            },
        ),
    ]