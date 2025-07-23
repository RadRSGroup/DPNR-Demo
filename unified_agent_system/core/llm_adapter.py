"""
Multi-Provider LLM Adapter with Model Versioning
Supports OpenAI, Anthropic, Google Gemini with automatic fallback
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime
import openai
import anthropic
import google.generativeai as genai

logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    LOCAL = "local"

@dataclass
class LLMConfig:
    provider: LLMProvider
    model_name: str
    api_key: Optional[str]
    max_tokens: int = 2000
    temperature: float = 0.7
    timeout: int = 30
    retry_attempts: int = 3
    fallback_providers: List[LLMProvider] = None

@dataclass
class LLMResponse:
    content: str
    provider: LLMProvider
    model: str
    tokens_used: int
    latency_ms: float
    timestamp: datetime

class BaseLLMAdapter(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = self._initialize_client()
    
    @abstractmethod
    def _initialize_client(self):
        pass
    
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        pass
    
    @abstractmethod
    def get_latest_models(self) -> List[str]:
        """Return list of available models for this provider"""
        pass

class OpenAIAdapter(BaseLLMAdapter):
    """OpenAI GPT models adapter"""
    
    def _initialize_client(self):
        return openai.AsyncOpenAI(api_key=self.config.api_key)
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        start_time = asyncio.get_event_loop().time()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                timeout=self.config.timeout
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            return LLMResponse(
                content=content,
                provider=LLMProvider.OPENAI,
                model=self.config.model_name,
                tokens_used=tokens_used,
                latency_ms=(asyncio.get_event_loop().time() - start_time) * 1000,
                timestamp=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise
    
    def get_latest_models(self) -> List[str]:
        return [
            "gpt-4-turbo-preview",
            "gpt-4-0125-preview", 
            "gpt-4-1106-preview",
            "gpt-4",
            "gpt-3.5-turbo-0125",
            "gpt-3.5-turbo"
        ]

class AnthropicAdapter(BaseLLMAdapter):
    """Anthropic Claude models adapter"""
    
    def _initialize_client(self):
        return anthropic.AsyncAnthropic(api_key=self.config.api_key)
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        start_time = asyncio.get_event_loop().time()
        
        try:
            message = await self.client.messages.create(
                model=self.config.model_name,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_prompt or "",
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = message.content[0].text
            tokens_used = message.usage.input_tokens + message.usage.output_tokens
            
            return LLMResponse(
                content=content,
                provider=LLMProvider.ANTHROPIC,
                model=self.config.model_name,
                tokens_used=tokens_used,
                latency_ms=(asyncio.get_event_loop().time() - start_time) * 1000,
                timestamp=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Anthropic generation failed: {e}")
            raise
    
    def get_latest_models(self) -> List[str]:
        return [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-2.1",
            "claude-2.0"
        ]

class GeminiAdapter(BaseLLMAdapter):
    """Google Gemini models adapter"""
    
    def _initialize_client(self):
        genai.configure(api_key=self.config.api_key)
        return genai.GenerativeModel(self.config.model_name)
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Gemini doesn't have explicit system prompts, so prepend to user prompt
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            response = await asyncio.to_thread(
                self.client.generate_content,
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.config.max_tokens,
                    temperature=self.config.temperature
                )
            )
            
            content = response.text
            # Gemini doesn't provide token count in response, estimate it
            tokens_used = len(full_prompt.split()) + len(content.split())
            
            return LLMResponse(
                content=content,
                provider=LLMProvider.GEMINI,
                model=self.config.model_name,
                tokens_used=tokens_used,
                latency_ms=(asyncio.get_event_loop().time() - start_time) * 1000,
                timestamp=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            raise
    
    def get_latest_models(self) -> List[str]:
        return [
            "gemini-1.5-pro-latest",
            "gemini-1.5-flash-latest",
            "gemini-pro",
            "gemini-pro-vision"
        ]

class LLMOrchestrator:
    """
    Orchestrates multiple LLM providers with fallback support
    and model version management
    """
    
    def __init__(self, configs: Dict[LLMProvider, LLMConfig]):
        self.adapters: Dict[LLMProvider, BaseLLMAdapter] = {}
        self.configs = configs
        self._initialize_adapters()
    
    def _initialize_adapters(self):
        adapter_classes = {
            LLMProvider.OPENAI: OpenAIAdapter,
            LLMProvider.ANTHROPIC: AnthropicAdapter,
            LLMProvider.GEMINI: GeminiAdapter
        }
        
        for provider, config in self.configs.items():
            if provider in adapter_classes:
                self.adapters[provider] = adapter_classes[provider](config)
    
    async def generate_with_fallback(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        preferred_provider: Optional[LLMProvider] = None,
        assessment_type: Optional[str] = None
    ) -> LLMResponse:
        """
        Generate response with automatic fallback to other providers
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            preferred_provider: Primary provider to try first
            assessment_type: Type of assessment for specialized routing
        """
        
        # Route to specialized models based on assessment type
        if assessment_type:
            preferred_provider = self._route_by_assessment_type(assessment_type)
        
        providers_to_try = []
        
        # Start with preferred provider
        if preferred_provider and preferred_provider in self.adapters:
            providers_to_try.append(preferred_provider)
        
        # Add remaining providers as fallbacks
        for provider in self.adapters.keys():
            if provider not in providers_to_try:
                providers_to_try.append(provider)
        
        last_error = None
        for provider in providers_to_try:
            try:
                logger.info(f"Attempting generation with {provider.value}")
                adapter = self.adapters[provider]
                response = await adapter.generate(prompt, system_prompt)
                logger.info(f"Successfully generated with {provider.value}")
                return response
            except Exception as e:
                logger.warning(f"Provider {provider.value} failed: {e}")
                last_error = e
                continue
        
        raise Exception(f"All LLM providers failed. Last error: {last_error}")
    
    def _route_by_assessment_type(self, assessment_type: str) -> LLMProvider:
        """Route to appropriate provider based on assessment type"""
        
        # Clinical assessments prefer OpenAI for GPT-4's analytical capabilities
        clinical_types = ["big_five", "emotional_intelligence", "cognitive_style"]
        if assessment_type.lower() in clinical_types:
            return LLMProvider.OPENAI
        
        # Soul-level assessments prefer Anthropic for nuanced understanding
        soul_types = ["sefirot", "shadow_work", "ifs", "pardes"]
        if assessment_type.lower() in soul_types:
            return LLMProvider.ANTHROPIC
        
        # General assessments can use Gemini for cost efficiency
        return LLMProvider.GEMINI
    
    def get_available_models(self) -> Dict[LLMProvider, List[str]]:
        """Get all available models across providers"""
        available_models = {}
        for provider, adapter in self.adapters.items():
            available_models[provider] = adapter.get_latest_models()
        return available_models
    
    async def update_model_version(self, provider: LLMProvider, new_model: str):
        """Update model version for a specific provider"""
        if provider in self.configs:
            self.configs[provider].model_name = new_model
            # Reinitialize adapter with new model
            self._initialize_adapters()
            logger.info(f"Updated {provider.value} to model {new_model}")

# Factory function to create orchestrator with default configuration
def create_llm_orchestrator(
    openai_key: str,
    anthropic_key: str,
    gemini_key: str
) -> LLMOrchestrator:
    """Create LLM orchestrator with standard configuration"""
    
    configs = {
        LLMProvider.OPENAI: LLMConfig(
            provider=LLMProvider.OPENAI,
            model_name="gpt-4-turbo-preview",
            api_key=openai_key,
            fallback_providers=[LLMProvider.ANTHROPIC, LLMProvider.GEMINI]
        ),
        LLMProvider.ANTHROPIC: LLMConfig(
            provider=LLMProvider.ANTHROPIC,
            model_name="claude-3-opus-20240229",
            api_key=anthropic_key,
            fallback_providers=[LLMProvider.OPENAI, LLMProvider.GEMINI]
        ),
        LLMProvider.GEMINI: LLMConfig(
            provider=LLMProvider.GEMINI,
            model_name="gemini-1.5-pro-latest",
            api_key=gemini_key,
            fallback_providers=[LLMProvider.OPENAI, LLMProvider.ANTHROPIC]
        )
    }
    
    return LLMOrchestrator(configs)