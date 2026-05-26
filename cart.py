"""
Shopping Cart Module
Handles cart operations: add, remove, update items.
"""

from api_client import APIClient


class CartManager:
    """Manages shopping cart operations."""

    def __init__(self):
        """Initialize the cart manager with API client and local cache."""
        self.api_client = APIClient()
        self.cart = []

    def add_to_cart(self, product_id, product_name, price, quantity):
        """
        Add an item to the shopping cart.
        
        Args:
            product_id (str): The product ID
            product_name (str): The product name
            price (float): The product price
            quantity (int): Quantity to add
            
        Returns:
            dict: Updated cart item
            
        Raises:
            ValueError: If quantity is invalid
            Exception: If API request fails
        """
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")

        # Check if product already in cart
        existing_item = None
        for item in self.cart:
            if item['id'] == product_id:
                existing_item = item
                break

        if existing_item:
            existing_item['quantity'] += quantity
        else:
            self.cart.append({
                'id': product_id,
                'name': product_name,
                'price': price,
                'quantity': quantity
            })

        try:
            payload = {
                "product_id": product_id,
                "quantity": quantity
            }
            response = self.api_client.post("/cart/add", payload)
            return response.get("item", {})
        except Exception as e:
            raise Exception(f"Failed to add item to cart: {str(e)}")

    def remove_from_cart(self, product_id):
        """
        Remove an item from the shopping cart.
        
        Args:
            product_id (str): The product ID to remove
            
        Raises:
            Exception: If API request fails
        """
        self.cart = [item for item in self.cart if item['id'] != product_id]

        try:
            self.api_client.delete(f"/cart/item/{product_id}")
        except Exception as e:
            raise Exception(f"Failed to remove item from cart: {str(e)}")

    def update_cart_item(self, product_id, new_quantity):
        """
        Update the quantity of an item in the cart.
        
        Args:
            product_id (str): The product ID
            new_quantity (int): The new quantity
            
        Raises:
            ValueError: If quantity is invalid
            Exception: If API request fails
        """
        if new_quantity < 1:
            raise ValueError("Quantity must be at least 1")

        # Update local cart
        for item in self.cart:
            if item['id'] == product_id:
                item['quantity'] = new_quantity
                break

        try:
            payload = {"quantity": new_quantity}
            self.api_client.put(f"/cart/update/{product_id}", payload)
        except Exception as e:
            raise Exception(f"Failed to update cart item: {str(e)}")

    def get_cart(self):
        """
        Retrieve the current shopping cart.
        
        Returns:
            list: List of items in the cart
        """
        return self.cart

    def get_cart_total(self):
        """
        Calculate the total price of items in the cart.
        
        Returns:
            float: Total cart value
        """
        return sum(item['price'] * item['quantity'] for item in self.cart)

    def get_cart_item_count(self):
        """
        Get the total number of items in the cart.
        
        Returns:
            int: Total number of items
        """
        return sum(item['quantity'] for item in self.cart)

    def clear_cart(self):
        """
        Clear all items from the cart.
        
        Raises:
            Exception: If API request fails
        """
        try:
            self.api_client.post("/cart/clear", {})
            self.cart = []
        except Exception as e:
            raise Exception(f"Failed to clear cart: {str(e)}")

    def is_empty(self):
        """
        Check if the cart is empty.
        
        Returns:
            bool: True if cart is empty, False otherwise
        """
        return len(self.cart) == 0
