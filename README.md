# Advanced Telegram Bot with Gemini AI Integration

A comprehensive Telegram bot powered by Google's Gemini AI, featuring text conversations, image generation, image analysis, and advanced admin controls with concurrent webhook server operation.

## 🌟 Features

### Core AI Features
- **💬 Gemini AI Chat**: Natural conversations with Google's Gemini 2.5 Flash
- **🎨 Image Generation**: Create images using Gemini 2.0 Flash Preview Image Generation
- **🔍 Image Analysis**: Detailed analysis of uploaded photos using Gemini 2.5 Pro Vision
- **🧠 Context Awareness**: Maintains conversation context for better interactions
- **📸 Smart Image Processing**: Automatic image preprocessing and format conversion

### Bot Management & Monitoring
- **📊 Real-time Status**: Live monitoring via webhook endpoints (`/status`, `/health`, `/metrics`)
- **🔧 Admin Controls**: Comprehensive admin panel accessible to authorized users
- **⚡ Rate Limiting**: Built-in protection against spam and abuse (10 msgs/min per user)
- **📈 Analytics**: Detailed usage statistics and performance metrics
- **👥 User Management**: Track active users and conversation statistics

### Technical Features
- **🌐 Concurrent Operation**: Bot polling and Flask webhook server run simultaneously on port 5000
- **🔄 Dual Architecture**: Supports both polling and webhook modes
- **🛡️ Robust Error Handling**: Comprehensive error handling with detailed logging
- **📝 Production Logging**: File and console logging with configurable levels
- **🐳 Docker Ready**: Full containerization support with health checks
- **📊 System Monitoring**: CPU, memory, and disk usage monitoring

## 🚀 Quick Start

### Method 1: Direct Python Execution

1. **Get Required API Keys:**
   - **Telegram Bot Token**: Message @BotFather on Telegram → `/newbot`
   - **Gemini API Key**: Visit [Google AI Studio](https://ai.google.dev) → Get API Key
   - **Admin ID**: Message @userinfobot on Telegram → `/start`

2. **Set Environment Variables:**
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token"
   export GEMINI_API_KEY="your_gemini_key" 
   export ADMIN_ID="your_telegram_user_id"
   ```

3. **Install Dependencies:**
   ```bash
   pip install python-telegram-bot[job-queue] google-genai flask pillow psutil
   ```

4. **Run the Bot:**
   ```bash
   python main.py
   ```

### Method 2: Docker Deployment

1. **Clone and Setup:**
   ```bash
   git clone <repository>
   cd telegram-bot
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Build and Run:**
   ```bash
   docker-compose up -d
   ```

3. **Check Status:**
   ```bash
   curl http://localhost:5000/health
   ```

## 📋 Environment Variables

### Required
```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
ADMIN_ID=your_telegram_user_id_here
```

### Optional
```bash
BOT_USERNAME=YourBotUsername           # Bot display name
WEBHOOK_URL=https://domain.com/webhook # For webhook mode
WEBHOOK_PORT=5000                      # Server port (default: 5000)
LOG_LEVEL=INFO                         # Logging level
```

## 🤖 Bot Commands & Usage

### User Commands
- **`/start`** - Welcome message and bot introduction
- **`/help`** - Display all available commands and features
- **`/generate <prompt>`** - Generate images (e.g., `/generate sunset over mountains`)
- **`/status`** - Show bot uptime and statistics
- **`/clear`** - Clear conversation context

### Admin Commands (Admin ID only)
- **`/admin`** - Open admin control panel
- **`/stats`** - Display detailed bot statistics

### Interactive Features
- **💬 Text Chat**: Send any message for AI conversation
- **📸 Image Analysis**: Send photos for detailed AI analysis
- **🎨 Image Generation**: Use `/generate` with descriptive prompts
- **🔄 Context Memory**: Bot remembers conversation history

## 📊 Monitoring & Status

### Webhook Endpoints
The bot runs a Flask server on port 5000 with these endpoints:

- **`GET /`** - Basic bot information
- **`GET /status`** - Detailed bot status and statistics
- **`GET /health`** - Health check (returns healthy/unhealthy)
- **`GET /metrics`** - Metrics for monitoring tools
- **`POST /webhook`** - Telegram webhook endpoint

### Example Status Response
```json
{
    "status": "online",
    "uptime_seconds": 1234,
    "uptime_formatted": "0d 0h 20m",
    "statistics": {
        "messages_processed": 15,
        "images_analyzed": 3,
        "images_generated": 2,
        "errors": 0,
        "active_users": 5
    },
    "bot_info": {
        "bot_username": "GeminiAIBot",
        "admin_id": 123456789,
        "webhook_configured": false
    }
}
```

## 🐳 Docker Configuration

### docker-compose.yml Features
- **Auto-restart**: Container restarts automatically on failure
- **Health checks**: Built-in monitoring with curl-based health checks
- **Volume mounting**: Persistent logs directory
- **Resource limits**: Memory limits for production deployment
- **Network isolation**: Dedicated Docker network

### Production Deployment
```bash
# Production environment
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f telegram-bot

# Scale for high availability (if needed)
docker-compose up -d --scale telegram-bot=2
```

## 🏗️ Architecture Overview

### Core Components
1. **TelegramBot** (`bot.py`) - Main bot logic and command handling
2. **GeminiHandler** (`gemini_handler.py`) - AI integration layer
3. **WebhookServer** (`webhook_server.py`) - Flask server for monitoring
4. **AdminControls** (`admin_controls.py`) - Admin management interface
5. **Config** (`config.py`) - Configuration management

### Concurrent Design
```
┌─────────────────┐    ┌──────────────────┐
│   Main Process  │    │   Webhook Thread │
│                 │    │                  │
│ ┌─────────────┐ │    │ ┌──────────────┐ │
│ │ Telegram    │ │    │ │ Flask Server │ │
│ │ Bot Polling │ │    │ │ Port 5000    │ │
│ │             │ │    │ │              │ │
│ └─────────────┘ │    │ └──────────────┘ │
└─────────────────┘    └──────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
            ┌────────▼─────────┐
            │   Shared State   │
            │ (Stats, Config,  │
            │  User Contexts)  │
            └──────────────────┘
```

## 🛠️ Development

### Project Structure
```
├── main.py                 # Application entry point
├── bot.py                  # Main bot implementation
├── gemini_handler.py       # Gemini AI integration
├── webhook_server.py       # Flask webhook server
├── admin_controls.py       # Admin panel functionality
├── config.py              # Configuration management
├── utils.py               # Utility functions
├── requirements.txt       # Dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env.example         # Environment variables template
└── README.md            # This file
```

### Adding New Features
1. **New Commands**: Add handlers in `bot.py` → `setup_handlers()`
2. **AI Features**: Extend `GeminiHandler` class methods
3. **Monitoring**: Add endpoints in `WebhookServer.setup_routes()`
4. **Admin Functions**: Extend `AdminControls` class

## 🚨 Troubleshooting

### Common Issues

**Bot not responding:**
- Check environment variables are set correctly
- Verify Telegram bot token with @BotFather
- Check logs: `docker-compose logs telegram-bot`

**Gemini API errors:**
- Verify API key at [Google AI Studio](https://ai.google.dev)
- Check API quotas and usage limits
- Review error messages in logs

**Webhook server not accessible:**
- Ensure port 5000 is open and not blocked
- Check firewall settings
- Verify Docker port mapping: `-p 5000:5000`

**Memory issues:**
- Monitor with `docker stats telegram-bot`
- Adjust memory limits in docker-compose.yml
- Check for memory leaks in user contexts

## 📝 Logging

### Log Levels
- **INFO**: General bot operations and user interactions
- **ERROR**: Failed operations and error conditions  
- **DEBUG**: Detailed debugging information (set LOG_LEVEL=DEBUG)

### Log Files
- **Console**: Real-time logging to stdout/stderr
- **File**: `bot.log` (when running without Docker)
- **Docker**: Access via `docker-compose logs`

## 🔒 Security Features

- **Rate Limiting**: 10 messages per minute per user
- **Admin Verification**: Commands restricted by Telegram user ID
- **Input Validation**: File size and type checking for images
- **Error Handling**: Prevents information leakage in error messages
- **Environment Variables**: Sensitive data stored securely
