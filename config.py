"""
Configuration Module
Loads environment variables and application configuration.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration settings."""

    # API Configuration
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000/api")
    API_KEY = os.getenv("API_KEY", "your_api_key_here")

    # Application Settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))

    # Pagination Defaults
    DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", 10))

    @classmethod
    def validate(cls):
        """
        Validate that all required configuration values are set.
        
        Raises:
            ValueError: If required configuration is missing
        """
        if not cls.API_BASE_URL:
            raise ValueError("API_BASE_URL environment variable is not set")
        if not cls.API_KEY:
            raise ValueError("API_KEY environment variable is not set")


if __name__ == "__main__":
    print("Configuration Settings:")
    print(f"API Base URL: {Config.API_BASE_URL}")
    print(f"Debug Mode: {Config.DEBUG}")
    print(f"Request Timeout: {Config.TIMEOUT}s")
    print(f"Default Page Size: {Config.DEFAULT_PAGE_SIZE}")
