"""
Model Router
Routes requests to appropriate provider based on configuration
"""

from typing import Optional, List, Dict, Any
from .base import BaseModelProvider
from .modelark import ModelArkProvider


class ModelRouter:
    """
    Routes model requests to appropriate provider.
    
    Supports multiple providers:
    - ModelArk (BytePlus)
    - OpenRouter (future)
    - Gemini (future)
    - Other OpenAI-compatible providers (future)
    
    Allows Aurora coding agent to switch providers without code changes.
    """
    
    def __init__(self, default_provider: str = "modelark"):
        """
        Initialize router with default provider.
        
        Args:
            default_provider: Name of default provider ('modelark', etc.)
        """
        self.default_provider = default_provider
        self.providers: Dict[str, BaseModelProvider] = {}
        
        # Initialize default provider
        if default_provider == "modelark":
            try:
                self.providers["modelark"] = ModelArkProvider()
            except Exception as e:
                raise RuntimeError(
                    f"Failed to initialize ModelArk provider: {e}\n"
                    "Ensure ARK_API_KEY and ARK_MODEL are set."
                )
    
    def register_provider(self, name: str, provider: BaseModelProvider) -> None:
        """
        Register a new provider.
        
        Args:
            name: Provider identifier
            provider: Instance of BaseModelProvider
        """
        if not isinstance(provider, BaseModelProvider):
            raise TypeError(
                f"Provider must inherit from BaseModelProvider, got {type(provider)}"
            )
        self.providers[name] = provider
    
    def get_provider(self, name: Optional[str] = None) -> BaseModelProvider:
        """
        Get provider by name.
        
        Args:
            name: Provider name (uses default if None)
            
        Returns:
            BaseModelProvider instance
            
        Raises:
            ValueError: If provider not registered
        """
        provider_name = name or self.default_provider
        if provider_name not in self.providers:
            available = ", ".join(self.providers.keys())
            raise ValueError(
                f"Provider '{provider_name}' not registered. "
                f"Available: {available}"
            )
        return self.providers[provider_name]
    
    def list_providers(self) -> List[str]:
        """Get list of registered provider names."""
        return list(self.providers.keys())
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        provider: Optional[str] = None,
        **kwargs
    ) -> str:
        """Route chat request to provider."""
        return self.get_provider(provider).chat(messages, **kwargs)
    
    def stream(
        self,
        messages: List[Dict[str, str]],
        provider: Optional[str] = None,
        **kwargs
    ):
        """Route stream request to provider."""
        return self.get_provider(provider).stream(messages, **kwargs)
    
    def vision(
        self,
        messages: List[Dict[str, Any]],
        provider: Optional[str] = None,
        **kwargs
    ) -> str:
        """Route vision request to provider."""
        return self.get_provider(provider).vision(messages, **kwargs)
    
    def tool_calling(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        provider: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Route tool calling request to provider."""
        return self.get_provider(provider).tool_calling(messages, tools, **kwargs)
    
    def structured_output(
        self,
        messages: List[Dict[str, str]],
        schema: Dict[str, Any],
        provider: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Route structured output request to provider."""
        return self.get_provider(provider).structured_output(
            messages, schema, **kwargs
        )
    
    def get_info(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """Get information about a provider."""
        return self.get_provider(provider).get_model_info()


# Global router instance (singleton)
_global_router: Optional[ModelRouter] = None


def get_router(default_provider: str = "modelark") -> ModelRouter:
    """
    Get or create global router instance.
    
    Args:
        default_provider: Default provider for first initialization
        
    Returns:
        ModelRouter instance
    """
    global _global_router
    if _global_router is None:
        _global_router = ModelRouter(default_provider)
    return _global_router
