from rest_framework import mixins, viewsets
from rest_framework.generics import RetrieveAPIView, ListAPIView

from apps.entertainment.models import (
    Channel,
    Content
)
from apps.entertainment.serializers import (
    ChannelSerializer,
    ContentSerializer
)

__all__ = ['ChannelAPIViewSet', 'ContentAPIViewSet']


class ChannelAPIViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """
        ChannelAPIView
        -> GET returns a list of channels
    """
    queryset = Channel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ChannelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if 'group_ids' in self.request.query_params:
            id_list = self.request.query_params.get('group_id').split(',')
            queryset = queryset.filter(
                groups__id__in=id_list
            )
        return queryset


class ContentAPIViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """
        ContentAPIView
        -> GET returns a list of contents
    """
    queryset = Content.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ContentSerializer
