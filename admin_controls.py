"""
Admin controls for the Telegram bot
"""

import logging
from datetime import datetime
from typing import Dict, List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)

class AdminControls:
    """Admin control panel for bot management"""
    
    def __init__(self, admin_id: int):
        self.admin_id = admin_id
    
    async def show_admin_panel(self, update: Update, context) -> None:
        """Show main admin control panel"""
        keyboard = [
            [
                InlineKeyboardButton("📊 Detailed Stats", callback_data="admin_stats"),
                InlineKeyboardButton("👥 User Info", callback_data="admin_users")
            ],
            [
                InlineKeyboardButton("🔄 Restart Bot", callback_data="admin_restart"),
                InlineKeyboardButton("🗑️ Clear Logs", callback_data="admin_clear_logs")
            ],
            [
                InlineKeyboardButton("⚙️ Bot Settings", callback_data="admin_settings"),
                InlineKeyboardButton("📋 System Info", callback_data="admin_system")
            ],
            [InlineKeyboardButton("❌ Close", callback_data="admin_close")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        admin_text = (
            "🔧 **Admin Control Panel**\n\n"
            "Select an option to manage the bot:"
        )
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                admin_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                admin_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def show_detailed_stats(self, update: Update, context, stats: Dict, user_contexts: Dict) -> None:
        """Show detailed bot statistics"""
        uptime = datetime.now() - stats['uptime_start']
        active_users = len(user_contexts)
        total_conversations = sum(len(contexts) for contexts in user_contexts.values())
        
        stats_text = (
            f"📊 **Detailed Bot Statistics**\n\n"
            f"⏰ **Uptime:** {uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m\n"
            f"🚀 **Started:** {stats['uptime_start'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"📈 **Usage Statistics:**\n"
            f"• Messages Processed: {stats['messages_processed']}\n"
            f"• Images Analyzed: {stats['images_analyzed']}\n"
            f"• Images Generated: {stats['images_generated']}\n"
            f"• Total Errors: {stats['errors']}\n\n"
            f"👥 **User Statistics:**\n"
            f"• Active Users: {active_users}\n"
            f"• Total Conversations: {total_conversations}\n\n"
            f"💾 **Performance:**\n"
            f"• Error Rate: {(stats['errors'] / max(stats['messages_processed'], 1) * 100):.2f}%\n"
            f"• Avg Messages/User: {(stats['messages_processed'] / max(active_users, 1)):.1f}"
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Admin Panel", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                stats_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                stats_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def show_user_info(self, update: Update, context, user_contexts: Dict) -> None:
        """Show user information"""
        if not user_contexts:
            user_text = "👥 **User Information**\n\nNo active users found."
        else:
            user_text = f"👥 **User Information**\n\n**Active Users:** {len(user_contexts)}\n\n"
            
            # Show top 10 most active users
            sorted_users = sorted(
                user_contexts.items(), 
                key=lambda x: len(x[1]), 
                reverse=True
            )[:10]
            
            for i, (user_id, contexts) in enumerate(sorted_users, 1):
                user_text += f"{i}. User ID: `{user_id}` - {len(contexts)} messages\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Admin Panel", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            user_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def show_system_info(self, update: Update, context) -> None:
        """Show system information"""
        import sys
        import platform
        import psutil
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Escape problematic characters for Telegram markdown
            platform_info = platform.platform().replace('_', '\\_').replace('*', '\\*')
            python_version = sys.version.split()[0]
            
            system_text = (
                f"📋 **System Information**\n\n"
                f"🖥️ **System:**\n"
                f"• Platform: {platform_info}\n"
                f"• Python: {python_version}\n\n"
                f"⚡ **Performance:**\n"
                f"• CPU Usage: {cpu_percent:.1f}%\n"
                f"• Memory: {memory.percent:.1f}% ({memory.used//1024//1024}MB / {memory.total//1024//1024}MB)\n"
                f"• Disk: {disk.percent:.1f}% ({disk.used//1024//1024//1024}GB / {disk.total//1024//1024//1024}GB)\n"
            )
        except Exception as e:
            error_msg = str(e).replace('_', '\\_').replace('*', '\\*')
            system_text = f"📋 **System Information**\n\nError retrieving system info: {error_msg}"
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Admin Panel", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            system_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def show_settings(self, update: Update, context) -> None:
        """Show bot settings"""
        settings_text = (
            f"⚙️ **Bot Settings**\n\n"
            f"🔧 **Current Configuration:**\n"
            f"• Max Message Length: 4096 chars\n"
            f"• Max Image Size: 20MB\n"
            f"• Rate Limit: 10 msgs/min\n"
            f"• Supported Formats: JPEG, PNG, WebP\n\n"
            f"📝 **Note:** Settings are configured via environment variables."
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Admin Panel", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            settings_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_callback(self, update: Update, context) -> None:
        """Handle callback queries from admin panel"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        if user_id != self.admin_id:
            await query.edit_message_text("❌ Access denied. Admin only.")
            return
        
        data = query.data
        
        try:
            if data == "admin_back":
                await self.show_admin_panel(update, context)
            elif data == "admin_stats":
                # This would need access to bot stats - handled in bot.py
                await query.edit_message_text(
                    "📊 Use /stats command for detailed statistics."
                )
            elif data == "admin_users":
                # This would need access to user contexts - handled in bot.py
                await query.edit_message_text(
                    "👥 User information feature requires bot context."
                )
            elif data == "admin_system":
                await self.show_system_info(update, context)
            elif data == "admin_settings":
                await self.show_settings(update, context)
            elif data == "admin_restart":
                await query.edit_message_text(
                    "🔄 **Restart Bot**\n\n"
                    "⚠️ Bot restart functionality requires manual intervention.\n"
                    "Please restart the bot process manually."
                )
            elif data == "admin_clear_logs":
                await query.edit_message_text(
                    "🗑️ **Clear Logs**\n\n"
                    "⚠️ Log clearing requires manual file system access.\n"
                    "Please clear log files manually if needed."
                )
            elif data == "admin_close":
                await query.edit_message_text("🔧 Admin panel closed.")
            
        except Exception as e:
            logger.error(f"Error in admin callback: {e}")
            await query.edit_message_text(f"❌ Error: {str(e)}")
