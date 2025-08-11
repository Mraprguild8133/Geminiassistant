"""
Gemini AI integration handler
"""

import json
import logging
import os
import tempfile
from typing import Optional, Tuple
from io import BytesIO

from google import genai
from google.genai import types
from PIL import Image

logger = logging.getLogger(__name__)

class GeminiHandler:
    """Handler for Google Gemini AI operations"""
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.text_model = "gemini-2.5-flash"
        self.vision_model = "gemini-2.5-pro"
        self.image_gen_model = "gemini-2.0-flash-preview-image-generation"
        
    async def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate text response using Gemini AI"""
        try:
            full_prompt = f"{context}\n\nUser: {prompt}" if context else prompt
            
            response = self.client.models.generate_content(
                model=self.text_model,
                contents=full_prompt
            )
            
            return response.text or "Sorry, I couldn't generate a response."
            
        except Exception as e:
            logger.error(f"Error generating text response: {e}")
            return f"Error: {str(e)}"
    
    async def analyze_image(self, image_bytes: bytes, prompt: str = "") -> str:
        """Analyze image using Gemini Vision"""
        try:
            # Default analysis prompt
            analysis_prompt = (
                prompt if prompt else
                "Analyze this image in detail. Describe what you see, including objects, "
                "people, activities, colors, composition, and any notable aspects. "
                "Provide a comprehensive analysis."
            )
            
            response = self.client.models.generate_content(
                model=self.vision_model,
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg",
                    ),
                    analysis_prompt,
                ],
            )
            
            return response.text or "Sorry, I couldn't analyze this image."
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return f"Error analyzing image: {str(e)}"
    
    async def generate_image(self, prompt: str) -> Tuple[Optional[bytes], str]:
        """Generate image using Gemini"""
        try:
            response = self.client.models.generate_content(
                model=self.image_gen_model,
                contents=f"Generate an image: {prompt}",
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )
            
            if not response.candidates:
                return None, "No image generated"
            
            content = response.candidates[0].content
            if not content or not content.parts:
                return None, "No image content received"
            
            image_data = None
            description = ""
            
            for part in content.parts:
                if part.text:
                    description += part.text
                elif part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
            
            if image_data:
                return image_data, description or "Image generated successfully"
            else:
                return None, "No image data received"
                
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None, f"Error generating image: {str(e)}"
    
    async def chat_with_context(self, messages: list) -> str:
        """Multi-turn conversation with context"""
        try:
            # Format messages for Gemini
            contents = []
            for msg in messages[-10:]:  # Keep last 10 messages for context
                role = "user" if msg.get('role') == 'user' else "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part(text=msg.get('content', ''))]
                    )
                )
            
            response = self.client.models.generate_content(
                model=self.text_model,
                contents=contents
            )
            
            return response.text or "Sorry, I couldn't generate a response."
            
        except Exception as e:
            logger.error(f"Error in chat with context: {e}")
            return f"Error: {str(e)}"
    
    def preprocess_image(self, image_bytes: bytes) -> bytes:
        """Preprocess image for better analysis"""
        try:
            # Open image with PIL
            image = Image.open(BytesIO(image_bytes))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large (max 1920x1920)
            max_size = 1920
            if max(image.size) > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Save back to bytes
            output = BytesIO()
            image.save(output, format='JPEG', quality=85)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return image_bytes  # Return original if preprocessing fails
