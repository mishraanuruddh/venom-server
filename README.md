# WhatsApp Message Ingestion System

This system automatically ingests WhatsApp messages using Venom, storing message metadata in PostgreSQL and media files in a private S3 bucket.

## Features

- Automatic ingestion of WhatsApp messages (text, images, videos, etc.)
- Configurable exclusion list for private conversations
- Media storage in private S3 bucket
- Message status tracking
- Support for deleted message detection
- Skip view-once messages
- Multi-device mode support

## Requirements

- Python 3.8+
- PostgreSQL database
- AWS S3 bucket
- WhatsApp account

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/whatsapp-ingestion.git
cd whatsapp-ingestion
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the example environment file and configure it:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python -m src.main
```

## Configuration

Configure the following in your `.env` file:

- Database credentials
- S3 credentials and bucket
- Venom session name
- List of excluded WhatsApp IDs

## Database Schema

The system uses a PostgreSQL database with the following schema:

### Messages Table
- `id`: Message ID (Primary Key)
- `chat_id`: Chat identifier
- `sender_id`: Sender's WhatsApp ID
- `recipient_id`: Recipient's WhatsApp ID
- `message_type`: Type of message
- `text_content`: Message text content
- `media_key`: Media decryption key
- `media_s3_path`: S3 path for media files
- `status`: Message status
- `deleted`: Deletion flag
- `timestamp`: Message timestamp
- `created_at`: Record creation timestamp

## Security Notes

- Keep your `.env` file secure and never commit it to version control
- Ensure S3 bucket permissions are properly restricted
- Follow WhatsApp's terms of service
- Regularly review and update excluded users list

## License

MIT License