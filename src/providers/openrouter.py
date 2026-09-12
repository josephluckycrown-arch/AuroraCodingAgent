"""
OpenRouter Provider Implementation
Implements BaseModelProvider using OpenRouter API
"""

import os
import json
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

from .base import BaseModelProvider


class OpenRouterProvider(BaseModelProvider):
    """
    OpenRouter implementation of BaseModelProvider.
    
    Uses OpenRouter API for multi-model routing.
    
    Environment variables:
    - OPENROUTER_API_KEY: API key for OpenRouter
    - OPENROUTER_MODEL: Model identifier (e.g., "openai/gpt-4")
    - OPENROUTER_REFERER: (optional) Referrer header
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize OpenRouter provider.
        
        Args:
            api_key: API key (uses OPENROUTER_API_KEY env var if None)
            model: Model name (uses OPENROUTER_MODEL env var if None)
        """
        try:
            import requests
        except ImportError:
            raise ImportError("requests not installed. Run: pip install requests")
        
        load_dotenv()
        
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        self.model = model or os.environ.get("OPENROUTER_MODEL")
        self.base_url = "https://openrouter.io/api/v1"
        self.referer = os.environ.get("OPENROUTER_REFERER", "Aurora-Coding-Agent")
        
        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not provided and not in environment. "
                "Pass api_key parameter or set OPENROUTER_API_KEY env var."
            )
        
        if not self.model:
            raise ValueError(
                "OPENROUTER_MODEL not provided and not in environment. "
                "Pass model parameter or set OPENROUTER_MODEL env var."
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.referer,
        })
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """Send chat request to OpenRouter."""
        response = self.session.post(
            f"{self.base_url}/chat/completions",
            json={
                "model": model or self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                **kwargs
            }
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    
    def stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        **kwargs
    ):
        """Stream from OpenRouter."""
        response = self.session.post(
            f"{self.base_url}/chat/completions",
            json={
                "model": model or self.model,
                "messages": messages,
                "stream": True,
                **kwargs
            },
            stream=True
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith("data: "):
                    line = line[6:]
                    if line == "[DONE]":
                        break
                    try:
                        data = json.loads(line)
                        if "choices" in data and data["choices"]:
                            delta = data["choices"][0].get("delta", {})
                            if "content" in delta and delta["content"]:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        pass
    
    def vision(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        **kwargs
    ) -> str:
        """Vision request to OpenRouter."""
        response = self.session.post(
            f"{self.base_url}/chat/completions",
            json={
                "model": model or self.model,
                "messages": messages,
                **kwargs
            }
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    
    def tool_calling(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Tool calling with OpenRouter."""
        response = self.session.post(
            f"{self.base_url}/chat/completions",
            json={
                "model": model or self.model,
                "messages": messages,
                "tools": tools,
                **kwargs
            }
        )
        response.raise_for_status()
        data = response.json()
        
        message = data["choices"][0]["message"]
        return {
            "message": message,
            "tool_calls": message.get("tool_calls", None)
        }
    
    def structured_output(
        self,
        messages: List[Dict[str, str]],
        schema: Dict[str, Any],
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Structured output from OpenRouter (if supported by model)."""
        response = self.session.post(
            f"{self.base_url}/chat/completions",
            json={
                "model": model or self.model,
                "messages": messages,
                "response_format": {"type": "json_schema", "schema": schema},
                **kwargs
            }
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        # Parse JSON if it's a string
        if isinstance(content, str):
            return json.loads(content)
        return content
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the configured model."""
        return {
            "provider": "openrouter",
            "model": self.model,
            "base_url": self.base_url,
            "capabilities": {
                "chat": True,
                "streaming": True,
                "vision": True,
                "tool_calling": True,
                "structured_output": True,
            }
        }
