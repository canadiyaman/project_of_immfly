import os
from datetime import datetime

from django.contrib import admin
from django.contrib.admin.utils import unquote

from apps.entertainment.models import (
    Channel,
    Content,
    MetaData,
    Rating,
    Group
)

__all__ = [
    'ChannelAdmin',
    'ContentAdmin',
    'MetaDataAdmin',
    'RatingAdmin'
]


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    search_fields = ('title', 'creator',)
    autocomplete_fields = ('contents', 'groups')
    readonly_fields = (
        'slug',
        'created_by',
        'deleted_by',
        'deleted_at',
        'created_at',
        'is_deleted'
    )

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'language',
                'picture',
                'parent',
                'is_active',
                'contents',
                'groups'
            )
        }),
        ('Information', {
            'classes': ('collapse',),
            'fields': (
                'created_at',
                'created_by',
                'is_deleted',
                'deleted_by',
                'deleted_at'
            ),
        }),
    )
    _groups = []

    def change_view(self, request, object_id, form_url='', extra_context=None):
        _object = self.get_object(request, unquote(object_id))
        self._groups = list(_object.groups.all().values_list('id', flat=True))
        self._groups.sort()
        return super().change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)

        updated_group_list = list(form.cleaned_data['groups'].values_list('id', flat=True))
        updated_group_list.sort()
        if self._groups != updated_group_list:
            if len(self._groups) > len(updated_group_list):
                insert = False
                group_ids = set(self._groups) - set(updated_group_list)

            else:
                insert = True
                group_ids = set(updated_group_list) - set(self._groups)
            obj.update_group_channels(group_ids, insert)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    search_fields = ('filename',)
    readonly_fields = (
        'filename',
        'file_code',
        'content_type',
        'created_by',
        'deleted_by',
        'deleted_at',
        'created_at',
        'is_deleted'
    )

    fieldsets = (
        (None, {
            'fields': (
                'file',
                'is_active'
            )
        }),
        ('Information', {
            'classes': ('collapse',),
            'fields': (
                'filename',
                'file_code',
                'content_type',
                'created_at',
                'created_by',
                'is_deleted',
                'deleted_by',
                'deleted_at'
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            file_name = os.path.basename(obj.file.name).split('.')
            file_name.pop()
            obj.filename = ''.join(file_name)
            obj.content_type = obj.file.file.content_type
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.is_deleted = True
        obj.deleted_at = datetime.now()
        obj.deleted_by = request.user
        obj.save()


@admin.register(MetaData)
class MetaDataAdmin(admin.ModelAdmin):
    search_fields = ('key', 'value')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    search_fields = ('content__filename', 'user__username')


class ChannelGroupInline(admin.TabularInline):
    model = Channel.groups.through


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    inlines = (ChannelGroupInline, )
