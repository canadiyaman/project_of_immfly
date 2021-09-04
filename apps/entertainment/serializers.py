from rest_framework import serializers

from apps.entertainment.models import Channel, Content, Group, Rating

__all__ = [
    'ChannelSerializer',
    'ContentSerializer',
    'GroupSerializer'
    # 'MetaDataSerializer',
    # 'RatingSerializer'
]


class ContentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField('prepare_created_at')
    created_by = serializers.SerializerMethodField('prepare_created_by')

    def prepare_created_at(self, instance):
        return instance.created_at.strftime('%d/%m/%y %h:%m:%s')

    def prepare_created_by(self, instance):
        return instance.created_by.username

    class Meta:
        model = Content
        fields = (
            'file',
            'filename',
            'file_code',
            'content_type',
            'created_at',
            'created_by'
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('title',)


class ChannelSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    groups = GroupSerializer(many=True)
    created_at = serializers.SerializerMethodField('prepare_created_at')
    created_by = serializers.SerializerMethodField('prepare_created_by')

    def prepare_created_at(self, instance):
        return instance.created_at.strftime('%d/%m/%Y, %H:%M:%S')

    def prepare_created_by(self, instance):
        return instance.created_by.username

    class Meta:
        model = Channel
        fields = (
            'title',
            'slug',
            'language',
            'picture',
            'created_at',
            'created_by',
            'parent',
            'contents',
            'groups',
        )




# class MetaDataSerializer(ModelSerializer):
#     class Meta:
#         model = MetaData
#
#
# class RatingSerializer(ModelSerializer):
#     class Meta:
#         model = Rating

