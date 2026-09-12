"""
Configuration settings for the E-Commerce Product Data Web Scraper.
"""

import os
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Load environment variables from .env file
def _load_env_file(env_path):
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    if key and key not in os.environ:
                        os.environ[key] = val

_load_env_file(BASE_DIR / ".env")

# Support Streamlit Cloud Secrets when deployed to Streamlit Community Cloud
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        for k, v in st.secrets.items():
            if k not in os.environ and isinstance(v, str):
                os.environ[k] = v
except Exception:
    pass

# Ensure runtime directories exist
# Vercel's deployed filesystem is read-only, so use /tmp there.
if os.getenv("VERCEL"):
    RUNTIME_DIR = Path("/tmp")
    OUTPUT_DIR = RUNTIME_DIR / "output"
    LOGS_DIR = RUNTIME_DIR / "logs"
else:
    OUTPUT_DIR = BASE_DIR / "output"
    LOGS_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Scraper default parameters
DEFAULT_MAX_PRODUCTS = 20
MAX_PAGES_TO_SCRAPE = 10
DEFAULT_TIMEOUT = 10
REQUEST_DELAY = 1  # Polite delay between requests in seconds

# Standard User-Agent for requests
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# Website Configuration
TEST_SITE_NAME = "Test Site"
TEST_SITE_BASE_URL = "https://books.toscrape.com/"
TEST_SITE_CATALOGUE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

AMAZON_SOURCE_NAME = "Amazon"
AMAZON_BASE_URL = "https://www.amazon.com/"
AMAZON_SEARCH_URL = "https://www.amazon.com/s"

FLIPKART_SOURCE_NAME = "Flipkart"
FLIPKART_BASE_URL = "https://www.flipkart.com/"
FLIPKART_SEARCH_URL = "https://www.flipkart.com/search"

ALIBABA_SOURCE_NAME = "Alibaba"
ALIBABA_BASE_URL = "https://www.alibaba.com/"
ALIBABA_SEARCH_URL = "https://www.alibaba.com/trade/search"

# Output configuration
CSV_OUTPUT = str(OUTPUT_DIR / "products.csv")
EXCEL_OUTPUT = str(OUTPUT_DIR / "products.xlsx")
LOG_FILE = str(LOGS_DIR / "scraper.log")

# Environment Variable Keys for Authorized APIs
ENV_AMAZON_API_KEY = "AMAZON_API_KEY"
ENV_FLIPKART_API_KEY = "FLIPKART_API_KEY"
ENV_ALIBABA_API_KEY = "ALIBABA_API_KEY"

# Retrieve current API keys
AMAZON_API_KEY = os.getenv(ENV_AMAZON_API_KEY)
FLIPKART_API_KEY = os.getenv(ENV_FLIPKART_API_KEY)
ALIBABA_API_KEY = os.getenv(ENV_ALIBABA_API_KEY)