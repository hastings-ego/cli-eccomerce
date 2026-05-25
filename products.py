"""
Product Management Module
Handles product listing and searching functionality.
"""

from api_client import APIClient


class ProductManager:
    """Manages product-related operations."""

    def __init__(self):
        """Initialize the product manager with API client."""
        self.api_client = APIClient()

    def get_all_products(self, page=1, limit=10):
        """
        Fetch all available products.
        
        Args:
            page (int): Page number for pagination (default: 1)
            limit (int): Number of products per page (default: 10)
            
        Returns:
            list: List of product dictionaries
            
        Raises:
            Exception: If API request fails
        """
        try:
            params = {"page": page, "limit": limit}
            response = self.api_client.get("/products", params=params)
            return response.get("products", [])
        except Exception as e:
            raise Exception(f"Failed to fetch products: {str(e)}")

    def get_product_by_id(self, product_id):
        """
        Fetch a specific product by ID.
        
        Args:
            product_id (str): The product ID
            
        Returns:
            dict: Product data
            
        Raises:
            Exception: If API request fails
        """
        try:
            response = self.api_client.get(f"/products/{product_id}")
            return response.get("product", {})
        except Exception as e:
            raise Exception(f"Failed to fetch product: {str(e)}")

    def search_products(self, query, page=1, limit=10):
        """
        Search for products by name or description.
        
        Args:
            query (str): Search query
            page (int): Page number for pagination (default: 1)
            limit (int): Number of results per page (default: 10)
            
        Returns:
            list: List of matching products
            
        Raises:
            Exception: If API request fails
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")

        try:
            params = {"q": query.strip(), "page": page, "limit": limit}
            response = self.api_client.get("/products/search", params=params)
            return response.get("products", [])
        except Exception as e:
            raise Exception(f"Product search failed: {str(e)}")

    def filter_products(self, category=None, min_price=None, max_price=None, page=1, limit=10):
        """
        Filter products by category and price range.
        
        Args:
            category (str): Product category (optional)
            min_price (float): Minimum price filter (optional)
            max_price (float): Maximum price filter (optional)
            page (int): Page number for pagination (default: 1)
            limit (int): Number of results per page (default: 10)
            
        Returns:
            list: List of filtered products
            
        Raises:
            Exception: If API request fails
        """
        try:
            params = {"page": page, "limit": limit}
            if category:
                params["category"] = category
            if min_price is not None:
                params["min_price"] = min_price
            if max_price is not None:
                params["max_price"] = max_price

            response = self.api_client.get("/products/filter", params=params)
            return response.get("products", [])
        except Exception as e:
            raise Exception(f"Product filtering failed: {str(e)}")
