"""
Configuration management for the Telegram bot
"""

import os
from typing import Optional

class Config:
    """Configuration class to manage all bot settings"""
    
    def __init__(self):
        # Required configuration
        self.telegram_token: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.gemini_api_key: str = os.getenv('GEMINI_API_KEY', '')
        self.admin_id: int = int(os.getenv('ADMIN_ID', '0'))
        
        # Optional configuration with defaults
        self.webhook_url: Optional[str] = os.getenv('WEBHOOK_URL')
        self.webhook_port: int = int(os.getenv('WEBHOOK_PORT', '5000'))
        self.bot_username: str = os.getenv('BOT_USERNAME', 'GeminiAIBot')
        
        # Bot settings
        self.max_message_length: int = 4096
        self.max_image_size: int = 20 * 1024 * 1024  # 20MB
        self.allowed_image_types: list = ['image/jpeg', 'image/png', 'image/webp']
        
        # Rate limiting
        self.rate_limit_messages: int = 10
        self.rate_limit_window: int = 60  # seconds
        
        # Logging
        self.log_level: str = os.getenv('LOG_LEVEL', 'INFO')
        
    def validate(self) -> bool:
        """Validate required configuration"""
        if not self.telegram_token:
            return False
        if not self.gemini_api_key:
            return False
        if not self.admin_id:
            return False
        return True
    
    def get_bot_info(self) -> dict:
        """Get bot information for status endpoint"""
        return {
            'bot_username': self.bot_username,
            'webhook_configured': bool(self.webhook_url),
            'admin_id': self.admin_id,
            'max_message_length': self.max_message_length,
            'allowed_image_types': self.allowed_image_types
        }
