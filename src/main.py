from venom_bot import WhatsApp
from loguru import logger
from datetime import datetime
import asyncio
import tempfile
import os
from pathlib import Path

from .controllers.storage_controller import StorageController
from .utils.database import get_db, engine
from .models.message import Base
from .config.settings import settings

class WhatsAppIngestion:
    def __init__(self):
        self.storage = StorageController()
        # Create database tables
        Base.metadata.create_all(bind=engine)
        self.setup_venom()

    def setup_venom(self):
        self.bot = WhatsApp(
            session=settings.VENOM_SESSION_NAME,
            multidevice=settings.MULTIDEVICE_MODE
        )
        
        @self.bot.on_message
        async def handle_message(message):
            try:
                # Extract message data
                message_data = {
                    'id': message.id,
                    'chat_id': message.chat.id,
                    'sender_id': message.sender.id,
                    'recipient_id': message.to,
                    'message_type': message.type,
                    'text_content': message.content if message.type == 'text' else None,
                    'media_key': getattr(message, 'mediaKey', None),
                    'timestamp': message.timestamp or datetime.utcnow(),
                    'is_view_once': getattr(message, 'isViewOnce', False)
                }

                # Handle media
                media_path = None
                if message.type in ['image', 'video', 'audio', 'document'] and not message_data['is_view_once']:
                    with tempfile.NamedTemporaryFile(delete=False) as tmp:
                        await message.download_media(tmp.name)
                        media_path = Path(tmp.name)

                # Store message
                db = next(get_db())
                try:
                    self.storage.store_message(db, message_data, media_path)
                finally:
                    if media_path and media_path.exists():
                        os.unlink(media_path)

            except Exception as e:
                logger.error(f"Error handling message: {e}")

        @self.bot.on_message_status
        async def handle_status(status):
            try:
                db = next(get_db())
                self.storage.update_message_status(db, status.id, status.status)
            except Exception as e:
                logger.error(f"Error handling status update: {e}")

    async def start(self):
        """Start the WhatsApp bot."""
        try:
            await self.bot.start()
            logger.info("WhatsApp bot started successfully")
            # Keep the bot running
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error starting WhatsApp bot: {e}")
            raise

def main():
    ingestion = WhatsAppIngestion()
    asyncio.run(ingestion.start())

if __name__ == "__main__":
    main()