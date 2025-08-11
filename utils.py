"""
Utility functions for the Telegram bot
"""

import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List

logger = logging.getLogger(__name__)

def format_message(text: str, max_length: int = 4096) -> str:
    """Format message text with proper length limits and markdown escaping"""
    if not text:
        return "No response generated."
    
    # Basic markdown escaping for common characters
    # Preserve intentional markdown formatting while escaping problematic characters
    text = re.sub(r'([_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', text)
    
    # If text is too long, truncate it properly
    if len(text) > max_length:
        # Try to truncate at a sentence boundary
        truncated = text[:max_length-100]
        last_period = truncated.rfind('.')
        last_newline = truncated.rfind('\n')
        
        cut_point = max(last_period, last_newline)
        if cut_point > max_length * 0.7:  # Only use sentence boundary if it's not too short
            text = text[:cut_point + 1] + "\n\n... (truncated)"
        else:
            text = text[:max_length-15] + "\n\n... (truncated)"
    
    return text

def is_admin(user_id: int, admin_id: int) -> bool:
    """Check if user is admin"""
    return user_id == admin_id

def rate_limit_check(user_id: int, user_requests: Dict[int, List[datetime]], config) -> bool:
    """Check if user is within rate limits"""
    now = datetime.now()
    window_start = now - timedelta(seconds=config.rate_limit_window)
    
    # Clean old requests
    if user_id in user_requests:
        user_requests[user_id] = [
            req_time for req_time in user_requests[user_id] 
            if req_time > window_start
        ]
    else:
        user_requests[user_id] = []
    
    # Check if within limit
    if len(user_requests[user_id]) >= config.rate_limit_messages:
        return False
    
    # Add current request
    user_requests[user_id].append(now)
    return True

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove or replace unsafe characters
    filename = re.sub(r'[^\w\-_\.]', '_', filename)
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + ('.' + ext if ext else '')
    
    return filename

def format_uptime(start_time: datetime) -> str:
    """Format uptime duration"""
    uptime = datetime.now() - start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    
    return " ".join(parts) if parts else "0m"

def validate_image_type(mime_type: str, allowed_types: list) -> bool:
    """Validate image MIME type"""
    return mime_type.lower() in [t.lower() for t in allowed_types]

def log_user_action(user_id: int, username: str, action: str, details: str = ""):
    """Log user actions for monitoring"""
    logger.info(
        f"User {user_id} (@{username or 'unknown'}) - {action}" + 
        (f" - {details}" if details else "")
    )

def get_file_size_mb(size_bytes: int) -> float:
    """Convert bytes to megabytes"""
    return round(size_bytes / (1024 * 1024), 2)

def create_progress_bar(current: int, total: int, width: int = 20) -> str:
    """Create a simple progress bar"""
    if total == 0:
        return "█" * width
    
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int(100 * current / total)
    
    return f"{bar} {percentage}%"

def escape_markdown_v2(text: str) -> str:
    """Escape text for Telegram's MarkdownV2"""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
