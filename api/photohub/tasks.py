import time
import random
import logging

from celery import shared_task

from .utils import send_photo_update
from apps.photohub.models import Photo

logger = logging.getLogger(__name__)


@shared_task
def process_image_task(photo_id):
    try:
        photo = Photo.objects.get(id=photo_id)

        photo.status = 'processing'
        photo.save(update_fields=['status'])
        send_photo_update(photo)

        time.sleep(20)

        photo.number = random.randint(1, 1000)
        photo.status = 'completed'
        photo.save(update_fields=['number', 'status'])
        send_photo_update(photo)

    except Exception as e:
        logger.error(f"Error processing photo {photo_id}: {str(e)}", exc_info=True)
        photo.status = 'failed'
        photo.save(update_fields=['status'])
        send_photo_update(photo)
        raise
