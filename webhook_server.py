"""
Flask webhook server for bot status and webhook handling
"""

import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.serving import run_simple
import os

from config import Config

logger = logging.getLogger(__name__)

class WebhookServer:
    """Flask server for webhook and status endpoints"""
    
    def __init__(self, config: Config, bot=None):
        self.config = config
        self.bot = bot
        self.app = Flask(__name__, template_folder='templates')
        self.setup_routes()
        
        # Disable Flask's default logging
        self.app.logger.disabled = True
        logging.getLogger('werkzeug').disabled = True
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/', methods=['GET'])
        def home():
            """Advanced dashboard homepage"""
            try:
                # Get bot status for template
                uptime = datetime.now() - (self.bot.start_time if self.bot else datetime.now())
                uptime_formatted = f"{uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m"
                
                template_data = {
                    'bot_name': 'Advanced Gemini AI Bot',
                    'uptime': uptime_formatted,
                    'stats': {
                        'messages_processed': self.bot.stats.get('messages_processed', 0) if self.bot else 0,
                        'images_analyzed': self.bot.stats.get('images_analyzed', 0) if self.bot else 0,
                        'images_generated': self.bot.stats.get('images_generated', 0) if self.bot else 0,
                        'errors': self.bot.stats.get('errors', 0) if self.bot else 0,
                        'active_users': len(self.bot.user_contexts) if self.bot else 0
                    },
                    'bot_info': self.config.get_bot_info()
                }
                
                return render_template('index.html', **template_data)
                
            except Exception as e:
                logger.error(f"Error rendering dashboard: {e}")
                # Fallback to JSON response
                return jsonify({
                    'status': 'online',
                    'bot_name': 'Advanced Gemini AI Bot',
                    'version': '1.0.0',
                    'error': 'Dashboard template error',
                    'endpoints': {
                        'status': '/status',
                        'health': '/health',
                        'webhook': '/webhook',
                        'metrics': '/metrics'
                    }
                })
        
        @self.app.route('/dashboard', methods=['GET'])
        def dashboard():
            """Alternative dashboard route"""
            return home()
        
        @self.app.route('/status', methods=['GET'])
        def status():
            """Bot status endpoint"""
            try:
                uptime = datetime.now() - (self.bot.start_time if self.bot else datetime.now())
                
                status_data = {
                    'status': 'online',
                    'uptime_seconds': int(uptime.total_seconds()),
                    'uptime_formatted': f"{uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m",
                    'bot_info': self.config.get_bot_info(),
                    'timestamp': datetime.now().isoformat()
                }
                
                if self.bot:
                    status_data['statistics'] = {
                        'messages_processed': self.bot.stats.get('messages_processed', 0),
                        'images_analyzed': self.bot.stats.get('images_analyzed', 0),
                        'images_generated': self.bot.stats.get('images_generated', 0),
                        'errors': self.bot.stats.get('errors', 0),
                        'active_users': len(self.bot.user_contexts)
                    }
                
                return jsonify(status_data)
                
            except Exception as e:
                logger.error(f"Error in status endpoint: {e}")
                return jsonify({
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @self.app.route('/health', methods=['GET'])
        def health():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'services': {
                    'bot': 'running' if self.bot else 'unknown',
                    'gemini_api': 'configured' if self.config.gemini_api_key else 'missing',
                    'telegram_api': 'configured' if self.config.telegram_token else 'missing'
                }
            })
        
        @self.app.route('/webhook', methods=['POST'])
        def webhook():
            """Webhook endpoint for Telegram"""
            try:
                # This is a placeholder for webhook functionality
                # In a full implementation, this would process Telegram updates
                data = request.get_json()
                logger.info(f"Received webhook data: {data}")
                
                return jsonify({
                    'status': 'received',
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Error processing webhook: {e}")
                return jsonify({
                    'status': 'error',
                    'error': str(e)
                }), 500
        
        @self.app.route('/metrics', methods=['GET'])
        def metrics():
            """Metrics endpoint for monitoring"""
            try:
                if not self.bot:
                    return jsonify({'error': 'Bot not available'}), 503
                
                uptime = datetime.now() - self.bot.start_time
                stats = self.bot.stats
                
                metrics_data = {
                    'uptime_seconds': int(uptime.total_seconds()),
                    'messages_total': stats.get('messages_processed', 0),
                    'images_analyzed_total': stats.get('images_analyzed', 0),
                    'images_generated_total': stats.get('images_generated', 0),
                    'errors_total': stats.get('errors', 0),
                    'active_users': len(self.bot.user_contexts),
                    'context_size_total': sum(len(ctx) for ctx in self.bot.user_contexts.values())
                }
                
                return jsonify(metrics_data)
                
            except Exception as e:
                logger.error(f"Error in metrics endpoint: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.errorhandler(404)
        def not_found(error):
            """Handle 404 errors"""
            return jsonify({
                'error': 'Not found',
                'message': 'The requested endpoint was not found.',
                'available_endpoints': ['/status', '/health', '/webhook', '/metrics']
            }), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            """Handle 500 errors"""
            return jsonify({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred.'
            }), 500
        
        @self.app.route('/api/info', methods=['GET'])
        def api_info():
            """API information endpoint"""
            return jsonify({
                'api_version': '1.0.0',
                'bot_name': 'Advanced Gemini AI Bot',
                'description': 'Telegram bot with Gemini AI integration',
                'features': [
                    'AI-powered conversations',
                    'Image generation with Gemini',
                    'Image analysis and recognition',
                    'Admin control panel',
                    'Real-time status monitoring',
                    'Rate limiting and security'
                ],
                'endpoints': {
                    'dashboard': '/',
                    'status': '/status',
                    'health': '/health',
                    'metrics': '/metrics',
                    'webhook': '/webhook',
                    'api_info': '/api/info'
                },
                'documentation': 'https://github.com/your-repo/telegram-bot',
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/api/stats/summary', methods=['GET'])
        def stats_summary():
            """Simplified stats endpoint"""
            try:
                if not self.bot:
                    return jsonify({'error': 'Bot not available'}), 503
                
                uptime = datetime.now() - self.bot.start_time
                stats = self.bot.stats
                
                return jsonify({
                    'online': True,
                    'uptime_hours': round(uptime.total_seconds() / 3600, 2),
                    'total_messages': stats.get('messages_processed', 0),
                    'total_images_processed': stats.get('images_analyzed', 0) + stats.get('images_generated', 0),
                    'active_users': len(self.bot.user_contexts),
                    'error_rate': round(stats.get('errors', 0) / max(stats.get('messages_processed', 1), 1) * 100, 2),
                    'last_updated': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Error in stats summary: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/favicon.ico')
        def favicon():
            """Favicon endpoint"""
            return '', 204
        
        @self.app.route('/docs', methods=['GET'])
        def api_documentation():
            """API Documentation page"""
            try:
                return render_template('api_docs.html')
            except Exception as e:
                logger.error(f"Error rendering API docs: {e}")
                return jsonify({
                    'error': 'Documentation not available',
                    'message': 'API documentation template error',
                    'available_endpoints': {
                        'api_info': '/api/info',
                        'status': '/status',
                        'health': '/health',
                        'metrics': '/metrics'
                    }
                }), 500
        
        @self.app.route('/live', methods=['GET'])
        def live_status():
            """Live status page with auto-refresh"""
            try:
                return render_template('status.html')
            except Exception as e:
                logger.error(f"Error rendering live status: {e}")
                # Fallback to JSON
                return jsonify({'error': 'Template not available'}), 500
    
    def run(self):
        """Run the Flask server"""
        try:
            logger.info(f"Starting webhook server on 0.0.0.0:{self.config.webhook_port}")
            
            # Use werkzeug's run_simple for better control
            run_simple(
                hostname='0.0.0.0',
                port=self.config.webhook_port,
                application=self.app,
                use_reloader=False,
                use_debugger=False,
                threaded=True
            )
            
        except Exception as e:
            logger.error(f"Failed to start webhook server: {e}")
            raise
