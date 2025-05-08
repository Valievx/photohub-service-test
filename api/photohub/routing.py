from django.urls import re_path

from .consumers import PhotoUpdatesConsumer

websocket_urlpatterns = [
    re_path(r'ws/photo-process/$', PhotoUpdatesConsumer.as_asgi()),
]
