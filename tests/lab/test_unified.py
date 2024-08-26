import pytest
import os
import asyncio
from aiforge.lab.unified import UnifiedApis
import logging

logger = logging.getLogger(__name__)

@pytest.fixture
def api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        pytest.skip("OPENAI_API_KEY not set in environment variables")
    return key

@pytest.fixture
def openai_api(api_key):
    return UnifiedApis(provider="openai", api_key=api_key, model="gpt-3.5-turbo", stream=False)

def test_openai_chat(openai_api):
    response = openai_api.chat("Hello, how are you?")
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_openai_chat_async(api_key):
    openai_api = UnifiedApis(provider="openai", api_key=api_key, model="gpt-3.5-turbo", use_async=True, stream=False)
    response = await openai_api.chat_async("What's the capital of France?")
    assert isinstance(response, str)
    assert "Paris" in response

@pytest.mark.parametrize("json_mode", [True, False])
def test_openai_json_mode(api_key, json_mode):
    openai_api = UnifiedApis(provider="openai", api_key=api_key, model="gpt-3.5-turbo", json_mode=json_mode)
    response = openai_api.chat("What's the capital of Spain?")
    
    if json_mode:
        assert isinstance(response, dict)
        assert 'response' in response or 'answer' in response
        content = response.get('response') or response.get('answer')
        assert isinstance(content, str)
        assert "Madrid" in content
    else:
        assert isinstance(response, str)
        assert "Madrid" in response

def test_openai_stream_mode(openai_api):
    openai_api.stream = True
    response = openai_api.chat("Count from 1 to 5.")
    assert isinstance(response, str)
    assert "1" in response and "5" in response

def test_openai_system_message(openai_api):
    openai_api.set_system_message("You are a helpful assistant that speaks like a pirate.")
    response = openai_api.chat("Hello, how are you?")
    assert isinstance(response, str)
    assert "arr" in response.lower() or "matey" in response.lower()