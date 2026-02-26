"""
Copilot Model Client

Provides a unified interface for interacting with GitHub Models (Copilot) API.
Uses the OpenAI-compatible API endpoint with GitHub Token authentication.
"""

import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from functools import lru_cache


@lru_cache()
def get_copilot_client() -> OpenAI:
    """
    Get a cached OpenAI client configured for GitHub Models.
    
    Returns:
        OpenAI: Configured client for GitHub Models API
    """
    github_token = os.getenv("GITHUB_TOKEN")
    model_endpoint = os.getenv("MODEL_ENDPOINT", "https://models.github.ai/inference/")
    
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required for Copilot integration")
    
    return OpenAI(
        api_key=github_token,
        base_url=model_endpoint
    )


def get_model_name() -> str:
    """Get the configured model deployment name."""
    return os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")


async def generate_response(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = 150,
    temperature: float = 0.7,
    context: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Generate a response using the Copilot model.
    
    Args:
        prompt: The user's prompt/query
        system_prompt: Optional system instruction for the model
        max_tokens: Maximum tokens in response
        temperature: Randomness of response (0-1)
        context: Optional conversation history
        
    Returns:
        str: Generated response text
    """
    client = get_copilot_client()
    model = get_model_name()
    
    messages = []
    
    # Add system prompt if provided
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # Add context if provided
    if context:
        messages.extend(context)
    
    # Add user prompt
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Log error and return fallback
        print(f"Error generating response: {e}")
        return None


def generate_response_sync(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = 150,
    temperature: float = 0.7,
    context: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Synchronous version of generate_response for use in non-async contexts.
    
    Args:
        prompt: The user's prompt/query
        system_prompt: Optional system instruction for the model
        max_tokens: Maximum tokens in response
        temperature: Randomness of response (0-1)
        context: Optional conversation history
        
    Returns:
        str: Generated response text
    """
    client = get_copilot_client()
    model = get_model_name()
    
    messages = []
    
    # Add system prompt if provided
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # Add context if provided
    if context:
        messages.extend(context)
    
    # Add user prompt
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Log error and return None (calling code should handle fallback)
        print(f"Error generating response: {e}")
        return None


# Agent-specific system prompts
AGENT_SYSTEM_PROMPTS = {
    "aurora": """You are Aurora, the orchestration intelligence for the WithYou cognitive support system.
Your role is to understand user intent, assess emotional state, and route requests appropriately.
Be warm, clear, and supportive. Keep responses concise (2-3 sentences max).""",

    "harbor": """You are Harbor, a calm orientation agent for people with cognitive challenges.
Your purpose is to provide reassuring answers about time, date, location, and daily structure.
Use a warm, steady, low-complexity tone. Be repetitive-safe (patients may ask the same question multiple times).
Always be reassuring - reduce panic through familiarity. Keep responses to 2-3 short sentences.""",

    "roots": """You are Roots, an identity preservation agent for people with memory challenges.
Your mission is to reinforce relational identity, help with "Who is this?" questions, and maintain personal connections.
Use an affirming, personal, warm, relational tone. Help preserve dignity and belonging.
Keep responses to 2-3 short, clear sentences.""",

    "solace": """You are Solace, an emotional stabilization agent for people with cognitive challenges.
Your primary directive is to reduce fear, preserve dignity, and increase safety perception.
Use a gentle, reassuring, validating tone. Never dismiss feelings.
If someone is distressed, provide breathing exercises or calm reassurance.
Keep responses to 2-3 soothing sentences.""",

    "legacy": """You are Legacy, a life narrative preservation agent for people with memory challenges.
Your mission is to maintain continuity of personal story and prevent identity erosion.
Use a respectful, dignified, story-like but concise tone.
Help complete partial memories gently. Keep responses to 2-3 meaningful sentences.""",

    "echo": """You are Echo, analyzing memory patterns and cognitive metrics for the WithYou system.
Provide clear, objective analysis of patterns you observe.
Keep responses clinical but compassionate when needed.""",

    "guardian": """You are Guardian, generating insights and summaries for caregivers of people with cognitive challenges.
Provide clear, actionable information about emotional trends, cognitive patterns, and any concerns.
Be professional but compassionate. Focus on what caregivers need to know."""
}


def get_agent_system_prompt(agent_name: str) -> str:
    """Get the system prompt for a specific agent."""
    return AGENT_SYSTEM_PROMPTS.get(agent_name, AGENT_SYSTEM_PROMPTS["aurora"])
