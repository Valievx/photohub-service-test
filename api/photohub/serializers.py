from rest_framework import serializers

from apps.photohub.models import Photo


class PhotoResultSerializer(serializers.ModelSerializer):
    uploaded_at = serializers.DateTimeField(format='%d %b %Y %H:%M')

    class Meta:
        model = Photo
        fields = ['filename', 'number', 'status', 'uploaded_at']
