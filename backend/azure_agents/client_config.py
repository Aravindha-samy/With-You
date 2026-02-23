"""
Azure AI Client Configuration for WithYou Agents
Simplified implementation using OpenAI SDK directly
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Load environment variables
load_dotenv(override=True)


def get_openai_client():
    """
    Get configured OpenAI client for AI interactions
    
    Supports two modes:
    1. GitHub Models (free, recommended for development)
    2. Azure OpenAI (production)
    
    Returns:
        OpenAI or AzureOpenAI: Configured client instance
    """
    
    # Check for GitHub Models configuration (preferred for development)
    github_token = os.getenv('GITHUB_TOKEN')
    model_endpoint = os.getenv('MODEL_ENDPOINT', 'https://models.inference.ai.azure.com')
    
    # Check for Azure OpenAI configuration
    azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    azure_key = os.getenv('AZURE_OPENAI_KEY')
    
    if github_token and not github_token.startswith('your_'):
        # Use GitHub Models
        print(f"🔗 Using GitHub Models endpoint")
        client = OpenAI(
            base_url=model_endpoint,
            api_key=github_token
        )
    elif azure_endpoint and not azure_endpoint.startswith('https://your-'):
        # Use Azure OpenAI
        print(f"🔗 Using Azure OpenAI endpoint: {azure_endpoint}")
        if azure_key:
            client = AzureOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=azure_key,
                api_version="2024-02-15-preview"
            )
        else:
            # Use DefaultAzureCredential
            token_provider = get_bearer_token_provider(
                DefaultAzureCredential(),
                "https://cognitiveservices.azure.com/.default"
            )
            client = AzureOpenAI(
                azure_endpoint=azure_endpoint,
                azure_ad_token_provider=token_provider,
                api_version="2024-02-15-preview"
            )
    else:
        # Return None to allow graceful fallback
        print("⚠️  No AI configuration found. Using mock responses.")
        return None
    
    return client


def get_model_deployment_name() -> str:
    """
    Get the model deployment name from environment
    
    Returns:
        str: Model deployment name (e.g., 'gpt-4o-mini', 'gpt-4o')
    """
    return os.getenv('MODEL_DEPLOYMENT_NAME', 'gpt-4o-mini')
