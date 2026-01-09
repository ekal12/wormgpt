import os

# API Configuration
AI_MODEL = "cognitivecomputations/dolphin-mistral-24b-venice-edition:free"
API_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# API Keys - PUBLIC FREE KEYS (Provided for GitHub use)
API_KEYS = [
    "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", # Primary
    "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"  # Backup
]

API_TIMEOUT = 30 # seconds
API_RETRY_COUNT = 3

# Scanner Config
DEFAULT_SCAN_ARGS = "-T4 -F" # Default fast scan
RESULTS_DIR = "results"
LOGS_DIR = "logs"

# Shell Config
PROMPT_SYMBOL = "└─>"
BANNER_TEXT = "AI-SEC TOOL v1.0"
