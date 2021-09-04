from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ['BaseModel']


class BaseModel(models.Model):
    """
        TimeStampModel is a Abstract model referenced by django.db models.Model
    """
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('is active')
    )

    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_('is deleted')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )

    deleted_at = models.DateTimeField(
        verbose_name=_('deleted at'),
        blank=True, null=True
    )

    created_by = models.ForeignKey(
        to='user.User',
        on_delete=models.PROTECT,
        related_name='%(class)ss_creator',
        verbose_name=_('created by'))

    deleted_by = models.ForeignKey(
        to='user.User',
        on_delete=models.PROTECT,
        related_name='%(class)ss_deleted',
        blank=True, null=True,
        verbose_name=_('deleted by'),
    )

    class Meta:
        abstract = True


