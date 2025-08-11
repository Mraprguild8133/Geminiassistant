"""
Telegram Bot implementation with Gemini AI integration
"""

import asyncio
import logging
import os
import tempfile
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram.constants import ChatAction, ParseMode

from gemini_handler import GeminiHandler
from admin_controls import AdminControls
from utils import format_message, is_admin, rate_limit_check
from config import Config

logger = logging.getLogger(__name__)

class TelegramBot:
    """Main Telegram bot class"""
    
    def __init__(self, config: Config):
        self.config = config
        self.gemini = GeminiHandler(config.gemini_api_key)
        self.admin_controls = AdminControls(config.admin_id)
        self.application = None
        self.start_time = datetime.now()
        
        # User contexts and rate limiting
        self.user_contexts: Dict[int, List[Dict]] = defaultdict(list)
        self.user_requests: Dict[int, List[datetime]] = defaultdict(list)
        
        # Bot statistics
        self.stats = {
            'messages_processed': 0,
            'images_analyzed': 0,
            'images_generated': 0,
            'errors': 0,
            'uptime_start': self.start_time
        }
    
    async def start_command(self, update: Update, context) -> None:
        """Handle /start command"""
        user = update.effective_user
        welcome_message = (
            f"🤖 Welcome to Advanced Gemini AI Bot, {user.first_name}!\n\n"
            "🌟 **Features:**\n"
            "• 💬 Chat with Gemini AI\n"
            "• 🖼️ Generate images with /generate\n"
            "• 🔍 Analyze images (just send a photo)\n"
            "• 📊 Get bot status with /status\n\n"
            "Simply send me a message to start chatting!"
        )
        
        if is_admin(user.id, self.config.admin_id):
            welcome_message += "\n🔧 **Admin Commands:**\n"
            welcome_message += "• /admin - Admin panel\n"
            welcome_message += "• /stats - Detailed statistics\n"
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def help_command(self, update: Update, context) -> None:
        """Handle /help command"""
        help_text = (
            "🤖 **Bot Commands:**\n\n"
            "🔹 `/start` - Welcome message\n"
            "🔹 `/help` - This help message\n"
            "🔹 `/generate <prompt>` - Generate an image\n"
            "🔹 `/status` - Bot status information\n"
            "🔹 `/clear` - Clear conversation context\n\n"
            "💬 **Chat Features:**\n"
            "• Send any text message to chat with Gemini AI\n"
            "• Send photos for detailed image analysis\n"
            "• Context is maintained for better conversations\n\n"
            "📸 **Image Analysis:**\n"
            "• Send any image and I'll analyze it in detail\n"
            "• Supports JPEG, PNG, and WebP formats\n"
            "• Max file size: 20MB\n\n"
            "🎨 **Image Generation:**\n"
            "• Use `/generate` followed by your prompt\n"
            "• Example: `/generate a sunset over mountains`"
        )
        
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def generate_command(self, update: Update, context) -> None:
        """Handle /generate command for image generation"""
        user_id = update.effective_user.id
        
        # Rate limiting check
        if not rate_limit_check(user_id, self.user_requests, self.config):
            await update.message.reply_text(
                "⚠️ You're sending requests too quickly. Please wait a moment."
            )
            return
        
        # Get prompt from command
        prompt = " ".join(context.args) if context.args else ""
        if not prompt:
            await update.message.reply_text(
                "Please provide a prompt for image generation.\n"
                "Example: `/generate a beautiful sunset over mountains`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Send "generating" message
        await update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
        generating_msg = await update.message.reply_text(
            "🎨 Generating your image, please wait..."
        )
        
        try:
            # Generate image
            image_data, description = await self.gemini.generate_image(prompt)
            
            if image_data:
                # Send the generated image
                await update.message.reply_photo(
                    photo=image_data,
                    caption=f"🎨 **Generated Image**\n\n**Prompt:** {prompt}\n\n{description}",
                    parse_mode=ParseMode.MARKDOWN
                )
                self.stats['images_generated'] += 1
                
                # Delete generating message
                await generating_msg.delete()
                
            else:
                await generating_msg.edit_text(
                    f"❌ Failed to generate image: {description}"
                )
                self.stats['errors'] += 1
                
        except Exception as e:
            logger.error(f"Error in generate command: {e}")
            await generating_msg.edit_text(
                f"❌ Error generating image: {str(e)}"
            )
            self.stats['errors'] += 1
    
    async def status_command(self, update: Update, context) -> None:
        """Handle /status command"""
        uptime = datetime.now() - self.start_time
        
        status_text = (
            f"🤖 **Bot Status**\n\n"
            f"✅ Status: Online\n"
            f"⏰ Uptime: {uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m\n"
            f"📊 Messages: {self.stats['messages_processed']}\n"
            f"🖼️ Images Analyzed: {self.stats['images_analyzed']}\n"
            f"🎨 Images Generated: {self.stats['images_generated']}\n"
            f"❌ Errors: {self.stats['errors']}\n"
            f"🚀 Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        await update.message.reply_text(
            status_text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def clear_command(self, update: Update, context) -> None:
        """Handle /clear command to clear conversation context"""
        user_id = update.effective_user.id
        self.user_contexts[user_id].clear()
        
        await update.message.reply_text(
            "🗑️ Conversation context cleared! Starting fresh."
        )
    
    async def handle_message(self, update: Update, context) -> None:
        """Handle regular text messages"""
        user = update.effective_user
        user_id = user.id
        message_text = update.message.text
        
        # Rate limiting check
        if not rate_limit_check(user_id, self.user_requests, self.config):
            await update.message.reply_text(
                "⚠️ You're sending requests too quickly. Please wait a moment."
            )
            return
        
        # Send typing action
        await update.message.reply_chat_action(ChatAction.TYPING)
        
        try:
            # Add user message to context
            self.user_contexts[user_id].append({
                'role': 'user',
                'content': message_text,
                'timestamp': datetime.now()
            })
            
            # Keep only recent messages for context (last 20)
            self.user_contexts[user_id] = self.user_contexts[user_id][-20:]
            
            # Generate response with context
            if len(self.user_contexts[user_id]) > 1:
                response = await self.gemini.chat_with_context(
                    self.user_contexts[user_id]
                )
            else:
                response = await self.gemini.generate_response(message_text)
            
            # Add bot response to context
            self.user_contexts[user_id].append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now()
            })
            
            # Format and send response
            formatted_response = format_message(response, self.config.max_message_length)
            await update.message.reply_text(
                formatted_response,
                parse_mode=ParseMode.MARKDOWN
            )
            
            self.stats['messages_processed'] += 1
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                f"❌ Sorry, I encountered an error: {str(e)}"
            )
            self.stats['errors'] += 1
    
    async def handle_photo(self, update: Update, context) -> None:
        """Handle photo messages for image analysis"""
        user = update.effective_user
        user_id = user.id
        
        # Rate limiting check
        if not rate_limit_check(user_id, self.user_requests, self.config):
            await update.message.reply_text(
                "⚠️ You're sending requests too quickly. Please wait a moment."
            )
            return
        
        await update.message.reply_chat_action(ChatAction.TYPING)
        analyzing_msg = await update.message.reply_text(
            "🔍 Analyzing your image, please wait..."
        )
        
        try:
            # Get the largest photo
            photo = update.message.photo[-1]
            
            # Check file size
            if photo.file_size > self.config.max_image_size:
                await analyzing_msg.edit_text(
                    "❌ Image is too large. Maximum size is 20MB."
                )
                return
            
            # Download photo
            file = await photo.get_file()
            image_bytes = await file.download_as_bytearray()
            
            # Preprocess image
            processed_image = self.gemini.preprocess_image(bytes(image_bytes))
            
            # Get caption as additional prompt
            caption = update.message.caption or ""
            analysis_prompt = f"User caption: {caption}\n\nPlease analyze this image." if caption else ""
            
            # Analyze image
            analysis = await self.gemini.analyze_image(processed_image, analysis_prompt)
            
            # Format and send analysis
            analysis_text = f"🔍 **Image Analysis**\n\n{analysis}"
            if caption:
                analysis_text = f"📝 **Your caption:** {caption}\n\n{analysis_text}"
            
            formatted_analysis = format_message(analysis_text, self.config.max_message_length)
            await analyzing_msg.edit_text(
                formatted_analysis,
                parse_mode=ParseMode.MARKDOWN
            )
            
            self.stats['images_analyzed'] += 1
            
        except Exception as e:
            logger.error(f"Error analyzing photo: {e}")
            await analyzing_msg.edit_text(
                f"❌ Error analyzing image: {str(e)}"
            )
            self.stats['errors'] += 1
    
    async def admin_command(self, update: Update, context) -> None:
        """Handle /admin command"""
        user_id = update.effective_user.id
        
        if not is_admin(user_id, self.config.admin_id):
            await update.message.reply_text("❌ Access denied. Admin only.")
            return
        
        await self.admin_controls.show_admin_panel(update, context)
    
    async def stats_command(self, update: Update, context) -> None:
        """Handle /stats command (admin only)"""
        user_id = update.effective_user.id
        
        if not is_admin(user_id, self.config.admin_id):
            await update.message.reply_text("❌ Access denied. Admin only.")
            return
        
        await self.admin_controls.show_detailed_stats(
            update, context, self.stats, self.user_contexts
        )
    
    def setup_handlers(self) -> None:
        """Setup bot command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("generate", self.generate_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("clear", self.clear_command))
        self.application.add_handler(CommandHandler("admin", self.admin_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        
        # Callback query handler for admin controls
        self.application.add_handler(CallbackQueryHandler(self.admin_controls.handle_callback))
    
    async def start(self) -> None:
        """Start the bot"""
        self.application = Application.builder().token(self.config.telegram_token).build()
        self.setup_handlers()
        
        logger.info("Bot handlers setup complete")
        
        # Initialize and start polling
        await self.application.initialize()
        await self.application.start()
        
        # Start polling
        await self.application.updater.start_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
        logger.info("Bot is now polling for updates...")
        
        # Keep the bot running
        try:
            # For the newer python-telegram-bot, we need to run until stopped
            import asyncio
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Bot stopped by keyboard interrupt")
        finally:
            await self.application.stop()
