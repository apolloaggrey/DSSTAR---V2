import os
from abc import ABC, abstractmethod
import google.generativeai as genai
import openai

class ModelProvider(ABC):
    """Abstract base class for model providers."""
    
    def __init__(self):
        self.input_tokens = 0
        self.output_tokens = 0
    
    @property
    @abstractmethod
    def env_var_name(self) -> str:
        """The name of the environment variable required for the API key."""
        pass
    
    @abstractmethod
    def generate_content(self, prompt: str) -> str:
        """Generates content based on the prompt."""
        pass

class GeminiProvider(ModelProvider):
    """Provider for Google's Gemini models."""
    
    def __init__(self, api_key: str, model_name: str):
        super().__init__()
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
    @property
    def env_var_name(self) -> str:
        return "GEMINI_API_KEY"
        
    def generate_content(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        if response.usage_metadata:
            self.input_tokens += response.usage_metadata.prompt_token_count
            self.output_tokens += response.usage_metadata.candidates_token_count
        return response.text

class OpenAIProvider(ModelProvider):
    """Provider for OpenAI models."""
    
    def __init__(self, api_key: str, model_name: str):
        super().__init__()
        self.api_key = api_key
        self.model_name = model_name
        self.client = openai.OpenAI(api_key=self.api_key)
        
        
    @property
    def env_var_name(self) -> str:
        return "OPENAI_API_KEY"
        
    def generate_content(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        if response.usage:
            self.input_tokens += response.usage.prompt_tokens
            self.output_tokens += response.usage.completion_tokens
        return response.choices[0].message.content
