"""
Authentication Module
Handles user login and registration via API integration.
"""

from api_client import APIClient
import re


class AuthManager:
    """Manages user authentication and registration."""

    def __init__(self):
        """Initialize the authentication manager with API client."""
        self.api_client = APIClient()
        self.auth_token = None

    def validate_email(self, email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_password(self, password):
        """Validate password strength (minimum 6 characters)."""
        return len(password) >= 6

    def register(self, name, email, password):
        """
        Register a new user.
        
        Args:
            name (str): User's full name
            email (str): User's email address
            password (str): User's password
            
        Returns:
            dict: User data if successful
            
        Raises:
            ValueError: If validation fails
            Exception: If API request fails
        """
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")

        if not self.validate_email(email):
            raise ValueError("Invalid email format")

        if not self.validate_password(password):
            raise ValueError("Password must be at least 6 characters long")

        payload = {
            "name": name.strip(),
            "email": email.strip(),
            "password": password
        }

        try:
            response = self.api_client.post("/auth/register", payload)
            user_data = response.get("user", {})
            self.auth_token = response.get("token")
            self.api_client.set_auth_token(self.auth_token)
            return user_data
        except Exception as e:
            raise Exception(f"Registration failed: {str(e)}")

    def login(self, email, password):
        """
        Login an existing user.
        
        Args:
            email (str): User's email address
            password (str): User's password
            
        Returns:
            dict: User data if successful
            
        Raises:
            ValueError: If validation fails
            Exception: If API request fails
        """
        if not self.validate_email(email):
            raise ValueError("Invalid email format")

        if not password:
            raise ValueError("Password cannot be empty")

        payload = {
            "email": email.strip(),
            "password": password
        }

        try:
            response = self.api_client.post("/auth/login", payload)
            user_data = response.get("user", {})
            self.auth_token = response.get("token")
            self.api_client.set_auth_token(self.auth_token)
            return user_data
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")

    def logout(self):
        """Logout the current user."""
        self.auth_token = None
        self.api_client.set_auth_token(None)
