import requests
import json
import time
from tool.config import API_KEYS, API_ENDPOINT, AI_MODEL, API_TIMEOUT, API_RETRY_COUNT
from tool.utils.logger import logger
from tool.utils.formatter import print_error, print_warning

class OpenRouterClient:
    def __init__(self):
        self.api_keys = API_KEYS
        self.current_key_index = 0
        self.headers = {
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/AI-Sec-Tool", # Required by OpenRouter for stats
            "X-Title": "AI-Sec-Tool"
        }

    def _get_current_key(self):
        return self.api_keys[self.current_key_index]
    
    def _switch_key(self):
        """Switches to the next available API key."""
        if self.current_key_index < len(self.api_keys) - 1:
            self.current_key_index += 1
            logger.info(f"Switching to backup API key index: {self.current_key_index}")
            print_warning(f"Primary key failed. Switching to backup key (Index {self.current_key_index})...")
            return True
        else:
            logger.error("All API keys exhausted.")
            return False

    def chat(self, user_input, system_prompt=None):
        """
        Sends a chat request to OpenRouter with automatic fallback and retries.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_input})
        
        payload = {
            "model": AI_MODEL,
            "messages": messages
        }
        
        # Outer loop for key rotation
        while True:
            current_key = self._get_current_key()
            self.headers["Authorization"] = f"Bearer {current_key}"
            
            # Inner loop for retries on the same key
            for attempt in range(API_RETRY_COUNT):
                try:
                    logger.debug(f"Sending request to OpenRouter (Attempt {attempt+1}/{API_RETRY_COUNT}) with key index {self.current_key_index}")
                    response = requests.post(
                        API_ENDPOINT,
                        headers=self.headers,
                        data=json.dumps(payload),
                        timeout=API_TIMEOUT
                    )
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            content = data['choices'][0]['message']['content']
                            logger.info("Successfully received AI response")
                            return content
                        except (KeyError, IndexError, json.JSONDecodeError) as e:
                            logger.error(f"Failed to parse API response: {e}")
                            print_error("Failed to parse AI response.")
                            return None
                            
                    elif response.status_code in [401, 403]:
                        logger.warning(f"Authentication failed (Status {response.status_code}). Key index {self.current_key_index} might be invalid.")
                        break # Break inner loop to switch key
                        
                    elif response.status_code == 429: # Rate limit
                        logger.warning(f"Rate limited (Status {response.status_code}). Retrying...")
                        time.sleep(2) # Wait a bit before retry
                        continue
                        
                    elif response.status_code >= 500:
                        logger.warning(f"Server error (Status {response.status_code}). Retrying...")
                        time.sleep(2)
                        continue
                    else:
                        logger.error(f"Unexpected API error: {response.status_code} - {response.text}")
                        # Don't switch keys for client errors (400, etc) unless auth related, but here we treat as generally retryable or stopping?
                        # For now, if it's not success and not handled above, we might just return error
                        return f"Error: Received status code {response.status_code}"

                except requests.exceptions.Timeout:
                    logger.warning("Request timed out. Retrying...")
                    continue
                except requests.exceptions.RequestException as e:
                    logger.error(f"Network error: {e}")
                    time.sleep(1)
                    continue
            
            # If we are here, it means retries failed for current key OR we deliberately broke out (401/403)
            # Try switching key
            if not self._switch_key():
                print_error("All API keys failed. Please check your network or update config.py.")
                return None
            
            # If switch successful, loop continues with new key

