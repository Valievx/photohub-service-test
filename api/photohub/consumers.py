import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class PhotoUpdatesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            await self.channel_layer.group_add(
                "photo_updates",
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            logger.error(f"Connection error: {str(e)}", exc_info=True)
            raise

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                "photo_updates",
                self.channel_name
            )
        except Exception as e:
            logger.error(f"Disconnection error: {str(e)}", exc_info=True)
            raise

    async def photo_update(self, event):
        try:
            await self.send(text_data=json.dumps(event))
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}", exc_info=True)
            raise
