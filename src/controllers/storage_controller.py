import boto3
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional

from ..models.message import Message
from ..config.settings import settings

class StorageController:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION
        )
        self.bucket = settings.S3_BUCKET

    def store_message(self, db: Session, message_data: dict, media_path: Optional[Path] = None) -> Message:
        """Store a message and its media (if any) in the database and S3."""
        
        # Skip if sender or chat is in exclude list
        if (message_data['sender_id'] in settings.EXCLUDED_IDS or 
            message_data['chat_id'] in settings.EXCLUDED_IDS):
            logger.info(f"Skipping excluded sender/chat: {message_data['sender_id']}")
            return None

        # Skip if it's a view-once message
        if message_data.get('is_view_once'):
            logger.info(f"Skipping view-once message from: {message_data['sender_id']}")
            return None

        # Upload media to S3 if present
        s3_path = None
        if media_path and media_path.exists():
            s3_path = self._upload_to_s3(media_path, message_data['id'])

        # Create message record
        message = Message(
            id=message_data['id'],
            chat_id=message_data['chat_id'],
            sender_id=message_data['sender_id'],
            recipient_id=message_data['recipient_id'],
            message_type=message_data['message_type'],
            text_content=message_data.get('text_content'),
            media_key=message_data.get('media_key'),
            media_s3_path=s3_path,
            status='received',
            timestamp=message_data['timestamp'] or datetime.utcnow(),
        )

        try:
            db.add(message)
            db.commit()
            db.refresh(message)
            logger.info(f"Stored message {message.id} successfully")
            return message
        except Exception as e:
            db.rollback()
            logger.error(f"Error storing message: {e}")
            raise

    def update_message_status(self, db: Session, message_id: str, status: str) -> bool:
        """Update the status of a message."""
        try:
            message = db.query(Message).filter(Message.id == message_id).first()
            if message:
                message.status = status
                if status == 'deleted':
                    message.deleted = True
                db.commit()
                logger.info(f"Updated message {message_id} status to {status}")
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating message status: {e}")
            raise

    def _upload_to_s3(self, file_path: Path, message_id: str) -> str:
        """Upload a file to S3 and return its path."""
        today = datetime.utcnow()
        s3_key = f"media/{today.year}/{today.month:02d}/{today.day:02d}/{message_id}_{file_path.name}"
        
        try:
            self.s3_client.upload_file(
                str(file_path),
                self.bucket,
                s3_key
            )
            logger.info(f"Uploaded {file_path} to S3: {s3_key}")
            return s3_key
        except Exception as e:
            logger.error(f"Error uploading to S3: {e}")
            raise