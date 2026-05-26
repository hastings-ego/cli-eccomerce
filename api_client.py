"""
API Client Module
Handles all HTTP requests to the backend API with proper error handling.
"""

import requests
import json
from config import Config


class APIClient:
    """Manages API communication with the backend server."""

    def __init__(self):
        """Initialize the API client with configuration."""
        self.base_url = Config.API_BASE_URL
        self.api_key = Config.API_KEY
        self.auth_token = None
        self.session = requests.Session()
        self._setup_headers()

    def _setup_headers(self):
        """Setup default headers for API requests."""
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-API-Key": self.api_key
        })

    def set_auth_token(self, token):
        """
        Set the authentication token for user requests.
        
        Args:
            token (str): JWT or API token
        """
        self.auth_token = token
        if token:
            self.session.headers.update({
                "Authorization": f"Bearer {token}"
            })
        else:
            self.session.headers.pop("Authorization", None)

    def _build_url(self, endpoint):
        """
        Build the complete URL for an endpoint.
        
        Args:
            endpoint (str): API endpoint path
            
        Returns:
            str: Complete URL
        """
        if endpoint.startswith("/"):
            return f"{self.base_url}{endpoint}"
        return f"{self.base_url}/{endpoint}"

    def _handle_response(self, response):
        """
        Handle API response and error cases.
        
        Args:
            response (requests.Response): The response object
            
        Returns:
            dict: Parsed JSON response
            
        Raises:
            Exception: If the request failed or response is invalid
        """
        try:
            if response.status_code == 204:
                return {}

            data = response.json()

            if response.status_code >= 400:
                error_message = data.get("error", {}).get("message", "Unknown error")
                raise Exception(f"API Error ({response.status_code}): {error_message}")

            return data

        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON response from API: {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")

    def get(self, endpoint, params=None):
        """
        Make a GET request to the API.
        
        Args:
            endpoint (str): API endpoint path
            params (dict): Query parameters (optional)
            
        Returns:
            dict: Parsed JSON response
            
        Raises:
            Exception: If the request fails
        """
        try:
            url = self._build_url(endpoint)
            response = self.session.get(url, params=params, timeout=10)
            return self._handle_response(response)
        except Exception as e:
            raise Exception(f"GET request failed: {str(e)}")

    def post(self, endpoint, data=None):
        """
        Make a POST request to the API.
        
        Args:
            endpoint (str): API endpoint path
            data (dict): Request body data
            
        Returns:
            dict: Parsed JSON response
            
        Raises:
            Exception: If the request fails
        """
        try:
            url = self._build_url(endpoint)
            response = self.session.post(url, json=data or {}, timeout=10)
            return self._handle_response(response)
        except Exception as e:
            raise Exception(f"POST request failed: {str(e)}")

    def put(self, endpoint, data=None):
        """
        Make a PUT request to the API.
        
        Args:
            endpoint (str): API endpoint path
            data (dict): Request body data
            
        Returns:
            dict: Parsed JSON response
            
        Raises:
            Exception: If the request fails
        """
        try:
            url = self._build_url(endpoint)
            response = self.session.put(url, json=data or {}, timeout=10)
            return self._handle_response(response)
        except Exception as e:
            raise Exception(f"PUT request failed: {str(e)}")

    def delete(self, endpoint):
        """
        Make a DELETE request to the API.
        
        Args:
            endpoint (str): API endpoint path
            
        Returns:
            dict: Parsed JSON response
            
        Raises:
            Exception: If the request fails
        """
        try:
            url = self._build_url(endpoint)
            response = self.session.delete(url, timeout=10)
            return self._handle_response(response)
        except Exception as e:
            raise Exception(f"DELETE request failed: {str(e)}")

    def close(self):
        """Close the session."""
        self.session.close()
