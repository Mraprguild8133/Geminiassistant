# 🤖 Telegram Bot Usage Guide

Your advanced Gemini AI Telegram bot is now live and ready to use! Here's how to get started and use all its features.

## 🚀 Quick Start

### 1. Find Your Bot on Telegram
- Search for your bot's username in Telegram
- Send `/start` to begin

### 2. Basic Commands
- **`/start`** - Welcome message
- **`/help`** - Show all commands
- **`/status`** - Bot statistics

## 💬 Chat with AI

Simply send any message to have a conversation with Gemini AI:

```
You: "What's the weather like in space?"
Bot: "Space doesn't have weather in the traditional sense..."
```

The bot remembers your conversation context for natural dialogue!

## 🎨 Generate Images

Use the `/generate` command followed by your description:

```
/generate a beautiful sunset over mountains with purple clouds
/generate cute robot dog playing in a garden
/generate abstract art in blue and gold colors
```

The bot will create and send you a unique image based on your prompt.

## 📸 Analyze Images

Send any photo to get detailed AI analysis:

1. **Take or select a photo**
2. **Send it to the bot** (with or without caption)
3. **Receive detailed analysis** including:
   - Objects and people in the image
   - Colors and composition
   - Activities and context
   - Notable features

Example: Send a photo of your meal and get a detailed description of the food, presentation, and setting.

## 👑 Admin Features

If you're the bot admin (configured with ADMIN_ID), you get additional commands:

### Admin Commands
- **`/admin`** - Open control panel with buttons for:
  - 📊 Detailed statistics
  - 👥 User information  
  - 📋 System information
  - ⚙️ Bot settings

- **`/stats`** - Detailed bot statistics including:
  - Uptime and performance
  - Usage metrics
  - Active users
  - Error rates

### Admin Control Panel
The admin panel provides:
- **User Management**: View active users and conversation counts
- **Performance Monitoring**: CPU, memory, disk usage
- **Bot Statistics**: Comprehensive usage analytics
- **System Information**: Platform and version details

## 🔧 Advanced Features

### Context Management
- **`/clear`** - Reset conversation context
- Bot remembers last 20 messages per user
- Context helps maintain natural conversations

### Rate Limiting
- Maximum 10 messages per minute per user
- Prevents spam and abuse
- Admin users have higher limits

### Supported Image Formats
- JPEG, PNG, WebP
- Maximum file size: 20MB
- Auto-preprocessing for optimal analysis

## 📊 Bot Status Monitoring

### Web Interface
Visit `http://your-server:5000` for:
- **`/status`** - Real-time bot statistics
- **`/health`** - Health check status
- **`/metrics`** - Monitoring data

### Status Information
- Bot uptime
- Messages processed
- Images analyzed/generated  
- Active users
- Error rates

## 🎯 Usage Tips

### For Best Chat Experience:
- Be specific in your questions
- Use context from previous messages
- Try different conversation styles

### For Image Generation:
- Be descriptive with your prompts
- Include style, colors, mood
- Mention specific objects or scenes
- Example: "photorealistic sunset over ocean with sailboat, warm colors, peaceful mood"

### For Image Analysis:
- Send high-quality photos
- Add captions for specific questions
- Works well with: food, nature, objects, people, art, documents

## 🚨 Troubleshooting

### Bot Not Responding?
1. Check if bot is online: `/status` or visit status URL
2. Try `/start` to refresh connection
3. Clear context with `/clear` if conversations seem stuck

### Image Issues?
- Ensure images are under 20MB
- Use supported formats (JPEG, PNG, WebP)
- Try resending if first attempt fails

### Getting Rate Limited?
- Wait 60 seconds between message bursts
- Limit to 10 messages per minute
- Admins have higher limits

## 📱 Example Usage Session

```
You: /start
Bot: 🤖 Welcome to Advanced Gemini AI Bot, User!

You: What can you do?
Bot: I can chat, analyze images, and generate pictures...

You: /generate a robot cat
Bot: 🎨 Generating your image, please wait...
Bot: [Sends generated robot cat image]

You: [Sends photo of your garden]
Bot: 🔍 Analyzing your image...
Bot: This image shows a well-maintained garden with...

You: /status
Bot: 🤖 Bot Status
     ✅ Status: Online
     ⏰ Uptime: 0d 2h 15m
     📊 Messages: 1,234
```

## 🎉 Your Bot is Ready!

Your Gemini AI Telegram bot is now fully operational with:
- ✅ AI conversations
- ✅ Image generation  
- ✅ Image analysis
- ✅ Admin controls
- ✅ Status monitoring
- ✅ Rate limiting
- ✅ Error handling

Start chatting and exploring all the features!