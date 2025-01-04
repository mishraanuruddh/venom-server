from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'

    id = Column(String(255), primary_key=True)
    chat_id = Column(String(255), nullable=False, index=True)
    sender_id = Column(String(255), nullable=False, index=True)
    recipient_id = Column(String(255), nullable=False)
    message_type = Column(String(50), nullable=False)
    text_content = Column(Text)
    media_key = Column(String(255))
    media_s3_path = Column(Text)
    status = Column(String(50), nullable=False)
    deleted = Column(Boolean, default=False)
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)