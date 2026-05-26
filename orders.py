"""
Order Management Module
Handles order creation and retrieval functionality.
"""

from api_client import APIClient


class OrderManager:
    """Manages order-related operations."""

    def __init__(self):
        """Initialize the order manager with API client."""
        self.api_client = APIClient()

    def create_order(self, user_id, items, total):
        """
        Create a new order from cart items.
        
        Args:
            user_id (str): The user ID
            items (list): List of cart items
            total (float): Order total amount
            
        Returns:
            dict: Created order data
            
        Raises:
            ValueError: If validation fails
            Exception: If API request fails
        """
        if not user_id:
            raise ValueError("User ID is required")

        if not items or len(items) == 0:
            raise ValueError("Order must contain at least one item")

        if total <= 0:
            raise ValueError("Order total must be greater than zero")

        payload = {
            "user_id": user_id,
            "items": items,
            "total": total
        }

        try:
            response = self.api_client.post("/orders", payload)
            return response.get("order", {})
        except Exception as e:
            raise Exception(f"Failed to create order: {str(e)}")

    def get_user_orders(self, user_id, page=1, limit=10):
        """
        Fetch all orders for a specific user.
        
        Args:
            user_id (str): The user ID
            page (int): Page number for pagination (default: 1)
            limit (int): Number of orders per page (default: 10)
            
        Returns:
            list: List of orders
            
        Raises:
            Exception: If API request fails
        """
        try:
            params = {"page": page, "limit": limit}
            response = self.api_client.get(f"/users/{user_id}/orders", params=params)
            return response.get("orders", [])
        except Exception as e:
            raise Exception(f"Failed to fetch orders: {str(e)}")

    def get_order_by_id(self, order_id):
        """
        Fetch a specific order by ID.
        
        Args:
            order_id (str): The order ID
            
        Returns:
            dict: Order data
            
        Raises:
            Exception: If API request fails
        """
        try:
            response = self.api_client.get(f"/orders/{order_id}")
            return response.get("order", {})
        except Exception as e:
            raise Exception(f"Failed to fetch order: {str(e)}")

    def cancel_order(self, order_id):
        """
        Cancel an order (if eligible).
        
        Args:
            order_id (str): The order ID
            
        Returns:
            dict: Updated order data
            
        Raises:
            Exception: If API request fails or order cannot be cancelled
        """
        try:
            response = self.api_client.put(f"/orders/{order_id}/cancel", {})
            return response.get("order", {})
        except Exception as e:
            raise Exception(f"Failed to cancel order: {str(e)}")

    def get_order_status(self, order_id):
        """
        Get the current status of an order.
        
        Args:
            order_id (str): The order ID
            
        Returns:
            str: Order status (e.g., 'pending', 'processing', 'shipped', 'delivered')
            
        Raises:
            Exception: If API request fails
        """
        try:
            order = self.get_order_by_id(order_id)
            return order.get("status", "unknown")
        except Exception as e:
            raise Exception(f"Failed to get order status: {str(e)}")
