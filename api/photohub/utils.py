import logging
from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from apps.photohub.models import Photo

logger = logging.getLogger(__name__)


def send_photo_update(photo):
    channel_layer = get_channel_layer()

    try:
        total = Photo.objects.count()
        completed = Photo.objects.filter(status='completed').count()
        pending = Photo.objects.filter(status__in=['pending', 'processing']).count()

        async_to_sync(channel_layer.group_send)(
            "photo_updates",
            {
                "type": "photo_update",
                "data": {
                    "id": photo.id,
                    "status": photo.status,
                    "number": photo.number,
                    "filename": photo.filename,
                    "uploaded_at": photo.uploaded_at.isoformat(),
                    "stats": {
                        "total": total,
                        "completed": completed,
                        "pending": pending
                    }
                }
            }
        )
        logger.info(f"Update sent to group 'photo_updates' for photo {photo.id}")
    except Exception as e:
        logger.error(f"Error sending photo update: {str(e)}", exc_info=True)
        raise
