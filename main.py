#!/usr/bin/env python3
"""
Advanced Telegram Bot with Gemini AI Integration
Main entry point for the bot application
"""

import asyncio
import logging
import os
import threading
from datetime import datetime

from bot import TelegramBot
from webhook_server import WebhookServer
from config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BotManager:
    """Manages both webhook server and Telegram bot"""
    
    def __init__(self):
        self.config = Config()
        self.bot = TelegramBot(self.config)
        self.webhook_server = WebhookServer(self.config, self.bot)
        self.start_time = datetime.now()
        
    def start_webhook_server(self):
        """Start the Flask webhook server in a separate thread"""
        try:
            logger.info("Starting webhook server on port 5000...")
            self.webhook_server.run()
        except Exception as e:
            logger.error(f"Failed to start webhook server: {e}")
    
    async def start_bot(self):
        """Start the Telegram bot"""
        try:
            logger.info("Starting Telegram bot...")
            await self.bot.start()
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
    
    def run(self):
        """Run both webhook server and bot concurrently"""
        logger.info("Starting Advanced Telegram Bot with Gemini AI...")
        logger.info(f"Bot started at: {self.start_time}")
        
        # Start webhook server in a separate thread
        webhook_thread = threading.Thread(
            target=self.start_webhook_server,
            daemon=True
        )
        webhook_thread.start()
        
        # Start the bot in the main thread
        asyncio.run(self.start_bot())

def main():
    """Main function"""
    try:
        # Validate required environment variables
        required_vars = ['TELEGRAM_BOT_TOKEN', 'GEMINI_API_KEY', 'ADMIN_ID']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            logger.error("Please set the following environment variables:")
            logger.error("- TELEGRAM_BOT_TOKEN: Your Telegram bot token")
            logger.error("- GEMINI_API_KEY: Your Google Gemini API key")
            logger.error("- ADMIN_ID: Your Telegram user ID for admin controls")
            return
        
        bot_manager = BotManager()
        bot_manager.run()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {e}")

if __name__ == "__main__":
    main()
