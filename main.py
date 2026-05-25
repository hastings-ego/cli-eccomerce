#!/usr/bin/env python3
"""
CLI E-Commerce Application
Main entry point for the application with user interface and menu handling.
"""

import sys
import os
from getpass import getpass

from auth import AuthManager
from products import ProductManager
from cart import CartManager
from orders import OrderManager
from utils import clear_screen, print_header, print_menu, get_validated_input


class ECommerceApp:
    """Main application controller for the CLI e-commerce platform."""

    def __init__(self):
        """Initialize the application with all managers."""
        self.auth_manager = AuthManager()
        self.product_manager = ProductManager()
        self.cart_manager = CartManager()
        self.order_manager = OrderManager()
        self.current_user = None

    def display_auth_menu(self):
        """Display the initial authentication menu."""
        while True:
            clear_screen()
            print_header()
            print("\n1.  👤 Login")
            print("2.  📝 Register")
            print("3.  🚪 Exit")
            print("=" * 50)

            choice = input("\nEnter your choice (1-3): ").strip()

            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_register()
            elif choice == "3":
                self.exit_app()
            else:
                print("❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def handle_login(self):
        """Handle user login."""
        clear_screen()
        print_header()
        print("\n📝 LOGIN")
        print("=" * 50)

        email = input("Email: ").strip()
        password = getpass("Password: ")

        try:
            user = self.auth_manager.login(email, password)
            self.current_user = user
            print(f"\n✅ Welcome back, {user.get('name', 'User')}!")
            input("Press Enter to continue...")
            self.display_main_menu()
        except Exception as e:
            print(f"\n❌ Login failed: {str(e)}")
            input("Press Enter to try again...")

    def handle_register(self):
        """Handle user registration."""
        clear_screen()
        print_header()
        print("\n✍️  REGISTER")
        print("=" * 50)

        name = input("Full Name: ").strip()
        email = input("Email: ").strip()
        password = getpass("Password: ")
        confirm_password = getpass("Confirm Password: ")

        if password != confirm_password:
            print("\n❌ Passwords do not match!")
            input("Press Enter to try again...")
            return

        try:
            user = self.auth_manager.register(name, email, password)
            print(f"\n✅ Account created successfully! Welcome, {user.get('name')}!")
            input("Press Enter to continue...")
            self.display_auth_menu()
        except Exception as e:
            print(f"\n❌ Registration failed: {str(e)}")
            input("Press Enter to try again...")

    def display_main_menu(self):
        """Display the main application menu after login."""
        while True:
            clear_screen()
            print_header()
            print(f"\n👤 Logged in as: {self.current_user.get('name', 'User')}")
            print("\n1.  🛍️  Browse Products")
            print("2.  🛒 View Shopping Cart")
            print("3.  📦 Checkout")
            print("4.  📋 Order History")
            print("5.  🚪 Logout")
            print("=" * 50)

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == "1":
                self.browse_products()
            elif choice == "2":
                self.view_cart()
            elif choice == "3":
                self.checkout()
            elif choice == "4":
                self.view_orders()
            elif choice == "5":
                self.logout()
                break
            else:
                print("❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def browse_products(self):
        """Browse and manage products."""
        while True:
            clear_screen()
            print_header()
            print("\n🛍️  BROWSE PRODUCTS")
            print("=" * 50)

            try:
                products = self.product_manager.get_all_products()

                if not products:
                    print("\n❌ No products available at the moment.")
                    input("Press Enter to continue...")
                    break

                for idx, product in enumerate(products, 1):
                    print(f"\n{idx}. {product.get('name')}")
                    print(f"   Price: ${product.get('price', 0):.2f}")
                    print(f"   Description: {product.get('description', 'N/A')}")
                    print(f"   Stock: {product.get('stock', 0)} units")

                print("\n" + "=" * 50)
                print("0. Back to Main Menu")
                print("=" * 50)

                choice = input("\nEnter product number to add to cart (0 to go back): ").strip()

                if choice == "0":
                    break

                try:
                    product_idx = int(choice) - 1
                    if 0 <= product_idx < len(products):
                        product = products[product_idx]
                        quantity = get_validated_input(
                            "Enter quantity: ",
                            input_type=int,
                            min_value=1,
                            max_value=product.get('stock', 1)
                        )
                        self.cart_manager.add_to_cart(
                            product.get('id'),
                            product.get('name'),
                            product.get('price'),
                            quantity
                        )
                        print(f"✅ Added {quantity}x {product.get('name')} to cart!")
                        input("Press Enter to continue...")
                    else:
                        print("❌ Invalid product number.")
                        input("Press Enter to try again...")
                except ValueError:
                    print("❌ Please enter a valid number.")
                    input("Press Enter to try again...")

            except Exception as e:
                print(f"❌ Error loading products: {str(e)}")
                input("Press Enter to continue...")
                break

    def view_cart(self):
        """Display and manage shopping cart."""
        while True:
            clear_screen()
            print_header()
            print("\n🛒 SHOPPING CART")
            print("=" * 50)

            cart_items = self.cart_manager.get_cart()

            if not cart_items:
                print("\n🛒 Your cart is empty!")
                input("Press Enter to continue...")
                break

            total = 0
            for idx, item in enumerate(cart_items, 1):
                item_total = item['price'] * item['quantity']
                total += item_total
                print(f"\n{idx}. {item['name']}")
                print(f"   Price: ${item['price']:.2f}")
                print(f"   Quantity: {item['quantity']}")
                print(f"   Subtotal: ${item_total:.2f}")

            print("\n" + "=" * 50)
            print(f"Total: ${total:.2f}")
            print("=" * 50)
            print("\n1. Update Quantity")
            print("2. Remove Item")
            print("3. Back to Menu")
            print("=" * 50)

            choice = input("\nEnter your choice (1-3): ").strip()

            if choice == "1":
                self.update_cart_item(cart_items)
            elif choice == "2":
                self.remove_cart_item(cart_items)
            elif choice == "3":
                break
            else:
                print("❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def update_cart_item(self, cart_items):
        """Update quantity of a cart item."""
        try:
            item_num = get_validated_input(
                "Enter item number to update: ",
                input_type=int,
                min_value=1,
                max_value=len(cart_items)
            )
            item = cart_items[item_num - 1]
            new_quantity = get_validated_input(
                f"Enter new quantity (current: {item['quantity']}): ",
                input_type=int,
                min_value=1
            )
            self.cart_manager.update_cart_item(item['id'], new_quantity)
            print(f"✅ Updated {item['name']} quantity to {new_quantity}!")
            input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter valid numbers.")
            input("Press Enter to try again...")

    def remove_cart_item(self, cart_items):
        """Remove item from cart."""
        try:
            item_num = get_validated_input(
                "Enter item number to remove: ",
                input_type=int,
                min_value=1,
                max_value=len(cart_items)
            )
            item = cart_items[item_num - 1]
            self.cart_manager.remove_from_cart(item['id'])
            print(f"✅ Removed {item['name']} from cart!")
            input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter a valid number.")
            input("Press Enter to try again...")

    def checkout(self):
        """Process order checkout."""
        clear_screen()
        print_header()
        print("\n💳 CHECKOUT")
        print("=" * 50)

        cart_items = self.cart_manager.get_cart()

        if not cart_items:
            print("\n🛒 Your cart is empty! Add items before checking out.")
            input("Press Enter to continue...")
            return

        total = sum(item['price'] * item['quantity'] for item in cart_items)

        print("\n📦 Order Summary:")
        print("=" * 50)
        for item in cart_items:
            item_total = item['price'] * item['quantity']
            print(f"{item['name']} x{item['quantity']}: ${item_total:.2f}")

        print("=" * 50)
        print(f"Total Amount: ${total:.2f}")
        print("=" * 50)

        confirm = input("\nProceed with checkout? (yes/no): ").strip().lower()

        if confirm == "yes":
            try:
                order = self.order_manager.create_order(
                    user_id=self.current_user.get('id'),
                    items=cart_items,
                    total=total
                )
                self.cart_manager.clear_cart()
                print(f"\n✅ Order created successfully!")
                print(f"Order ID: {order.get('id')}")
                print(f"Total: ${total:.2f}")
                input("Press Enter to continue...")
            except Exception as e:
                print(f"\n❌ Checkout failed: {str(e)}")
                input("Press Enter to try again...")
        else:
            print("\n⏸️  Checkout cancelled.")
            input("Press Enter to continue...")

    def view_orders(self):
        """View user's order history."""
        clear_screen()
        print_header()
        print("\n📋 ORDER HISTORY")
        print("=" * 50)

        try:
            orders = self.order_manager.get_user_orders(
                user_id=self.current_user.get('id')
            )

            if not orders:
                print("\n📭 No orders found.")
                input("Press Enter to continue...")
                return

            for idx, order in enumerate(orders, 1):
                print(f"\n{idx}. Order #{order.get('id')}")
                print(f"   Date: {order.get('created_at', 'N/A')}")
                print(f"   Total: ${order.get('total', 0):.2f}")
                print(f"   Status: {order.get('status', 'Unknown')}")

            input("\nPress Enter to continue...")

        except Exception as e:
            print(f"❌ Error loading orders: {str(e)}")
            input("Press Enter to continue...")

    def logout(self):
        """Handle user logout."""
        clear_screen()
        print_header()
        print("\n👋 Thank you for shopping! See you next time.")
        print("=" * 50)
        self.current_user = None
        input("Press Enter to continue...")

    def exit_app(self):
        """Exit the application."""
        clear_screen()
        print_header()
        print("\n👋 Thank you for using CLI E-Commerce App!")
        print("=" * 50)
        sys.exit(0)

    def run(self):
        """Run the main application loop."""
        try:
            self.display_auth_menu()
        except KeyboardInterrupt:
            print("\n\n⚠️  Application interrupted by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    app = ECommerceApp()
    app.run()
