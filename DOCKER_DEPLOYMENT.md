# 🐳 Docker Deployment Guide - Simultaneous Services

This guide shows how to deploy your Advanced Telegram Bot where **both webhook server and main bot run simultaneously** in Docker.

## 🔄 How Both Services Work Together

### Current Architecture
```
┌─────────────────────────────────────┐
│        Docker Container             │
│  ┌─────────────────────────────────┐ │
│  │         main.py                 │ │
│  │                                 │ │
│  │  ┌─────────────┐ ┌─────────────┐ │ │
│  │  │ Webhook     │ │ Telegram    │ │ │
│  │  │ Server      │ │ Bot         │ │ │
│  │  │ (Thread)    │ │ (Main)      │ │ │
│  │  │ Port 5000   │ │ Polling API │ │ │
│  │  └─────────────┘ └─────────────┘ │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Service Coordination
1. **main.py** starts both services
2. **Webhook server** runs in separate thread on port 5000
3. **Telegram bot** runs in main thread with polling
4. **Both services share** the same bot instance and statistics
5. **Health check** verifies both are running

## 🚀 Quick Deployment

### Step 1: Environment Setup
```bash
# Create .env file
cat > .env << EOF
TELEGRAM_BOT_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_key_here
ADMIN_ID=your_telegram_user_id
EOF
```

### Step 2: Build and Run
```bash
# Build and start both services simultaneously
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### Step 3: Verify Both Services
```bash
# Check if both services are running
docker-compose ps

# Test webhook server
curl http://localhost:5000/health

# Check logs for both services
docker-compose logs -f
```

## 📊 Service Monitoring

### Health Check Endpoints
```bash
# Overall health (both services)
curl http://localhost:5000/health
# Response: {"status":"healthy","services":{"bot":"running","webhook":"running"}}

# Detailed status
curl http://localhost:5000/status

# Interactive dashboard
open http://localhost:5000/
```

### Docker Health Check
The container has built-in health checks that verify both services:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 15s
```

## 🔧 Docker Commands

### Basic Operations
```bash
# Start both services
docker-compose up -d

# Stop both services
docker-compose down

# Restart both services
docker-compose restart

# View logs from both services
docker-compose logs -f telegram-bot
```

### Development Mode
```bash
# Run with live code changes
docker-compose up --build

# Debug mode with interactive shell
docker-compose exec telegram-bot bash
```

### Production Mode
```bash
# Run with nginx proxy
docker-compose --profile production up -d

# Scale for high availability
docker-compose up -d --scale telegram-bot=2
```

## 📈 Service Verification

### Check Both Services Status
```bash
# 1. Container status
docker-compose ps
# Should show: telegram-bot running

# 2. Health check
curl -s http://localhost:5000/health | jq
# Should show both services healthy

# 3. Bot functionality
# Send message to your bot on Telegram
# Check webhook dashboard at http://localhost:5000/

# 4. Logs verification
docker-compose logs --tail=50 telegram-bot
# Should show both webhook server and bot polling logs
```

### Expected Log Output
```
telegram-bot | 2025-08-11 17:45:00 - __main__ - INFO - Starting Advanced Telegram Bot with Gemini AI...
telegram-bot | 2025-08-11 17:45:00 - __main__ - INFO - Starting webhook server on port 5000...
telegram-bot | 2025-08-11 17:45:00 - __main__ - INFO - Starting Telegram bot...
telegram-bot | 2025-08-11 17:45:00 - bot - INFO - Bot handlers setup complete
telegram-bot | 2025-08-11 17:45:01 - bot - INFO - Bot is now polling for updates...
```

## 🛠 Troubleshooting

### Both Services Not Starting
```bash
# Check environment variables
docker-compose config

# Check container logs
docker-compose logs telegram-bot

# Verify ports are available
netstat -lan | grep 5000
```

### Webhook Server Not Responding
```bash
# Test internal connectivity
docker-compose exec telegram-bot curl http://localhost:5000/health

# Check if Flask is bound correctly
docker-compose exec telegram-bot netstat -lan | grep 5000
```

### Bot Not Polling
```bash
# Check Telegram token
docker-compose exec telegram-bot python -c "
import os
from config import Config
config = Config()
print('Token configured:', bool(config.telegram_token))
"

# Test API connectivity
docker-compose exec telegram-bot curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe
```

## 🔄 Production Deployment

### With Load Balancer
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  telegram-bot-1:
    build: .
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - ADMIN_ID=${ADMIN_ID}
    ports:
      - "5001:5000"
  
  telegram-bot-2:
    build: .
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - GEMINI_API_KEY=${GEMINI_API_KEY}  
      - ADMIN_ID=${ADMIN_ID}
    ports:
      - "5002:5000"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### Environment Variables for Production
```bash
# Production .env
TELEGRAM_BOT_TOKEN=your_production_token
GEMINI_API_KEY=your_production_key
ADMIN_ID=your_admin_id
WEBHOOK_URL=https://yourdomain.com/webhook
LOG_LEVEL=INFO
```

## 📋 Verification Checklist

✅ **Docker Container**: Running and healthy
✅ **Webhook Server**: Responding on port 5000
✅ **Telegram Bot**: Polling for messages
✅ **Health Check**: Both services healthy
✅ **Dashboard**: Accessible at http://localhost:5000/
✅ **API Endpoints**: All responding correctly
✅ **Logs**: Both services logging properly
✅ **Bot Functionality**: Responding to messages
✅ **Admin Panel**: Working for authorized users
✅ **Image Generation**: Gemini AI integration working

## 🎯 Key Points

1. **Single Command**: `docker-compose up` starts both services
2. **Shared Resources**: Both services share bot instance and stats  
3. **Health Monitoring**: Built-in checks for both services
4. **Auto-restart**: Container restarts if either service fails
5. **Production Ready**: Includes nginx proxy and scaling options
6. **Easy Debugging**: Clear logs from both services

Your bot now runs both services simultaneously in Docker with full monitoring and production deployment capabilities!