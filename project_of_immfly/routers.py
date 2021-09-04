from rest_framework import routers

from apps.entertainment.views import ChannelAPIViewSet, ContentAPIViewSet

router = routers.SimpleRouter()


router.register(r'channels', ChannelAPIViewSet)
router.register(r'contents', ContentAPIViewSet)

urlpatterns = []

urlpatterns += router.urls
