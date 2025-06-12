# API Summary

## Overview
This document provides comprehensive summaries of all external APIs used in the TermSage project. It serves as a quick reference for understanding API capabilities, authentication requirements, and usage patterns.

## APIs Used

### 1. AI Model APIs

#### Ollama API
- **Purpose**: Local AI model inference for privacy (primary provider)
- **Base URL**: `http://localhost:11434`
- **Authentication**: None (local)
- **Key Endpoints**:
  - `/api/generate` - Text generation
  - `/api/chat` - Chat completions
  - `/api/tags` - List available models
- **Usage Example**:
  ```bash
  curl http://localhost:11434/api/generate -d '{
    "model": "llama2",
    "prompt": "Why is the sky blue?"
  }'
  ```
- **Integration Notes**:
  - Primary provider for privacy-conscious users
  - No internet required after model download
  - Supports multiple models (llama2, codellama, mistral, etc.)
  - Auto-fallback to cloud providers if unavailable

#### OpenAI API
- **Purpose**: GPT models for complex reasoning and advanced features
- **Base URL**: `https://api.openai.com/v1`
- **Authentication**: API Key (Bearer token)
- **Key Endpoints**:
  - `/chat/completions` - Chat interactions
  - `/completions` - Text completion
  - `/models` - List available models
- **Rate Limits**: Varies by subscription tier
- **Integration Notes**:
  - Used for complex reasoning tasks
  - Fallback when local models insufficient
  - Supports GPT-4, GPT-3.5-turbo
  - Streaming responses for better UX

#### Anthropic API (Claude)
- **Purpose**: Claude models for detailed explanations and analysis
- **Base URL**: `https://api.anthropic.com/v1`
- **Authentication**: API Key (x-api-key header)
- **Key Endpoints**:
  - `/messages` - Send messages to Claude
  - `/complete` - Text completion
- **Model Versions**: claude-3-opus, claude-3-sonnet, claude-3-haiku
- **Integration Notes**:
  - Best for detailed technical explanations
  - Strong reasoning capabilities
  - Good for code analysis and debugging
  - Supports large context windows

### 2. System APIs

#### Terminal/Shell APIs
- **subprocess**: Python's subprocess module for command execution
- **pty**: Pseudo-terminal interface for interactive commands
- **termios**: Terminal I/O control

### 3. AI Provider Configuration

#### Provider Selection Strategy
```python
# Priority order for AI providers
PROVIDER_PRIORITY = [
    "ollama",      # Local, privacy-first
    "openai",      # Cloud, advanced features
    "anthropic",   # Cloud, detailed analysis
]

# Auto-fallback mechanism
def get_ai_provider():
    for provider in PROVIDER_PRIORITY:
        if provider.is_available():
            return provider
    return None
```

#### Performance Tiers
- **High**: Full AI features, large context windows
- **Medium**: Balanced performance and features
- **Basic**: Essential AI features only
- **Minimal**: Terminal-only mode with basic AI

### 4. Future API Integrations
- **Google Gemini**: For multimodal capabilities
- **Cohere**: For specialized NLP tasks
- **Local GGML Models**: For fully offline operation
- **Custom Fine-tuned Models**: For domain-specific assistance

## API Best Practices

### Error Handling
- Always implement retry logic with exponential backoff
- Handle rate limiting gracefully
- Provide fallback options when APIs are unavailable

### Security
- Never hardcode API keys
- Use environment variables or secure config files
- Implement request signing where applicable
- Validate all API responses

### Performance
- Cache API responses when appropriate
- Batch requests where possible
- Monitor API usage and costs
- Implement request pooling for high-frequency calls

## API Configuration Template
```python
API_CONFIG = {
    "provider_name": {
        "base_url": "",
        "auth_type": "bearer|api_key|oauth",
        "timeout": 30,
        "retry_count": 3,
        "rate_limit": {
            "requests_per_minute": 60,
            "tokens_per_minute": 90000
        }
    }
}
```

## Troubleshooting Common API Issues

### Connection Errors
- Check network connectivity
- Verify API endpoint URLs
- Ensure proper SSL/TLS configuration

### Authentication Failures
- Verify API key validity
- Check key permissions/scopes
- Ensure proper header formatting

### Rate Limiting
- Implement exponential backoff
- Use request queuing
- Monitor usage dashboards

## Notes
- Update this document whenever new APIs are integrated
- Include example requests and responses
- Document any API-specific quirks or limitations