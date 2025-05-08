from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from apps.photohub.models import Photo
from api.photohub import swagger
from .serializers import PhotoResultSerializer
from .tasks import process_image_task


class ProcessImageView(APIView):
    @swagger_auto_schema(**swagger.process_image)
    def post(self, request):
        file = request.FILES.get('image')
        if not file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        photo = Photo.objects.create(filename=file.name, status='pending')
        process_image_task.delay(photo.id)
        serializer = PhotoResultSerializer(photo)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class ImageResultsView(APIView):
    @swagger_auto_schema(**swagger.image_results)
    def get(self, request):
        photos = Photo.objects.all().order_by('-uploaded_at')
        return Response({
            'photos': PhotoResultSerializer(photos, many=True).data,
            'stats': {
                'total': photos.count(),
                'completed': photos.filter(status='completed').count(),
                'pending': photos.filter(status__in=['pending', 'processing']).count()
            }
        })
