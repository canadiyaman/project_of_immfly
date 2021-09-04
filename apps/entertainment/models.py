import uuid
import os

from django.db import models
from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.base.model import BaseModel
from apps.base.field import IntegerRangeField


__all__ = ['Channel', 'Content', 'MetaData', 'Rating', 'Group']


def update_picture(instance, filename):
    path = os.path.join('pictures', f'pic_{filename}')
    return path


class Channel(BaseModel):
    """
        Channel Model referenced BaseModel
    """

    title = models.CharField(
        max_length=255,
        verbose_name=_('title')
    )
    slug = models.CharField(
        max_length=255,
        verbose_name=_('slug')
    )
    language = models.CharField(
        max_length=5,
        choices=settings.LANGUAGES,
        verbose_name=_('language')
    )
    picture = models.ImageField(
        upload_to=update_picture,
        verbose_name=_('picture')
    )
    parent = models.ForeignKey(
        "self",
        related_name='subchannels',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    contents = models.ManyToManyField(
        to='entertainment.Content',
        verbose_name=_('contents'),
        related_name='channels',
        blank=True
    )

    groups = models.ManyToManyField(
        to='entertainment.Group',
        verbose_name=_('groups'),
        related_name='channels_by_group',
        blank=True
    )

    def __str__(self):
        return f'{self.title}'

    def get_all_subchannels(self, include_self=True):
        channels = []
        if include_self:
            channels.append(self)
        for c in self._meta.model.objects.filter(parent=self):
            _c = c.get_all_subchannels(include_self=True)
            if 0 < len(_c):
                channels.extend(_c)
        return channels

    def update_group_channels(self, group_ids, insert):
        subchannels = self.get_all_subchannels()
        for group in Group.objects.filter(id__in=group_ids):
            for subchannel in subchannels:
                if insert:
                    subchannel.groups.add(group)
                else:
                    subchannel.groups.remove(group)

    class Meta:
        verbose_name = _('channel')
        verbose_name_plural = _('channels')


@receiver(pre_save, sender=Channel)
def populate_slug_field(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


def update_file(instance, filename):
    ext = filename.split('.')[-1]
    if ext in ['mp4', 'avi']:
        path = os.path.join('videos', f'file_{filename}')
    elif ext in ['jpg', 'png', 'jpeg']:
        path = os.path.join('images', f'file_{filename}')
    elif ext in ['docx', 'txt', 'pdf']:
        path = os.path.join('documents', f'file_{filename}')
    else:
        path = os.path.join('general', f'file_{filename}')
    return path


class Content(BaseModel):
    """
        Content Model referenced BaseModel
    """

    file = models.FileField(
        upload_to=update_file,
        verbose_name=_('file')
    )
    filename = models.CharField(
        max_length=500,
        verbose_name=_('original filename')
    )
    file_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('file code')
    )
    content_type = models.CharField(
        max_length=50,
        verbose_name=_('mime type')
    )

    def __str__(self):
        return f'{self.filename} - {self.content_type}'

    class Meta:
        verbose_name = _('content')
        verbose_name_plural = _('contents')


class MetaData(models.Model):
    """
        MetaData Model referenced from django.db models.Model
    """
    content = models.ForeignKey(
        to='Content',
        on_delete=models.CASCADE,
        related_name='metadatas'
    )
    key = models.CharField(max_length=255, verbose_name=_('key'))
    value = models.CharField(max_length=500, verbose_name=_('value'))

    def __str__(self):
        return f'{self.key}'

    class Meta:
        unique_together = ('content_id', 'key')
        verbose_name = _('metadata')
        verbose_name_plural = _('metadatas')


class Rating(models.Model):
    """
        Rating Model referenced from django.db models.Model
    """
    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE, related_name='user_ratings')
    content = models.ForeignKey(to='Content', on_delete=models.CASCADE, related_name='content_ratings')
    rate = IntegerRangeField(min_value=0, max_value=10, verbose_name=_('rate'))

    def __str__(self):
        return f'{self.content_id}-{self.user_id}: {self.rate}'

    class Meta:
        unique_together = ('user_id', 'content_id')
        verbose_name = _('rating')
        verbose_name_plural = _('ratings')


class Group(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
