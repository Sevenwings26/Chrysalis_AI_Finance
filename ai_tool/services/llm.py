import os
from typing import List, Dict, Any
from google import genai
from google.genai import types
from google.genai.errors import APIError
from django.conf import settings
from decouple import config   

class LLMClient:
    """
    LLM Client for Gemini using the official google-genai SDK.
    Optimized for financial analysis and RAG system integration.
    """

    def __init__(self):
        # Fallbacks: Django settings -> Environment variable
        self.api_key = getattr(settings, 'GEMINI_API_KEY', config('GEMINI_API_KEY'))
        
        # Recommended default for RAG and swift chat agents
        self.model = "gemini-2.5-flash" 
        
        # Initialize the Google GenAI client if key is available
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 800) -> str:
        """
        Main method to get a text response from Gemini.
        """
        if not self.client:
            return "⚠️ Gemini API key is not configured. Please add GEMINI_API_KEY to your settings/environment."

        try:
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )
            
            return response.text.strip()

        except APIError as e:
            print(f"Gemini API Error: {e}")
            return "Sorry, I'm having trouble connecting to my brain right now. Please try again in a moment."
        except Exception as e:
            print(f"Unexpected LLM Error: {e}")
            return "I encountered an error while processing your request."

    def generate_with_history(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 800) -> str:
        """
        Supports conversation history.
        Expects OpenAI-style formats: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        and converts them seamlessly to Gemini's expected types.Content format.
        """
        if not self.client:
            return "⚠️ Gemini API key is not configured."

        try:
            # Transform OpenAI/Grok message format into Gemini SDK Native Contents
            gemini_contents = []
            for msg in messages:
                # Map standard 'assistant' role string to Gemini's expected 'model' role
                role = "model" if msg['role'] == "assistant" else "user"
                
                gemini_contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg['content'])]
                    )
                )

            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )

            response = self.client.models.generate_content(
                model=self.model,
                contents=gemini_contents,
                config=config,
            )
            
            return response.text.strip()

        except APIError as e:
            print(f"Gemini History API Error: {e}")
            return "Sorry, I couldn't process the conversation context."
        except Exception as e:
            print(f"Unexpected Gemini History Error: {e}")
            return "Sorry, I couldn't process that request."
        
