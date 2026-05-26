"""
Utilities Module
Helper functions for input validation, formatting, and UI display.
"""

import os
import sys


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    """Print the application header."""
    print("\n" + "=" * 50)
    print("   🛍️  CLI E-COMMERCE APPLICATION 🛍️")
    print("=" * 50)


def print_menu(options):
    """
    Print a formatted menu with options.
    
    Args:
        options (dict): Dictionary of {key: description}
    """
    for key, description in options.items():
        print(f"{key}. {description}")


def get_validated_input(prompt, input_type=str, min_value=None, max_value=None, choices=None):
    """
    Get and validate user input with specific constraints.
    
    Args:
        prompt (str): The input prompt to display
        input_type (type): Expected data type (str, int, float)
        min_value (int/float): Minimum allowed value
        max_value (int/float): Maximum allowed value
        choices (list): List of valid choices
        
    Returns:
        The validated input value
        
    Raises:
        ValueError: If input doesn't meet validation criteria
    """
    while True:
        try:
            user_input = input(prompt).strip()

            if not user_input:
                print("❌ Input cannot be empty. Please try again.")
                continue

            # Convert to specified type
            if input_type == int:
                value = int(user_input)
            elif input_type == float:
                value = float(user_input)
            else:
                value = user_input

            # Validate choices
            if choices and value not in choices:
                print(f"❌ Please choose from: {', '.join(map(str, choices))}")
                continue

            # Validate min value
            if min_value is not None and value < min_value:
                print(f"❌ Value must be at least {min_value}")
                continue

            # Validate max value
            if max_value is not None and value > max_value:
                print(f"❌ Value must not exceed {max_value}")
                continue

            return value

        except ValueError:
            print(f"❌ Please enter a valid {input_type.__name__}.")


def format_price(price):
    """
    Format a price value as currency.
    
    Args:
        price (float): The price to format
        
    Returns:
        str: Formatted price string
    """
    return f"${price:.2f}"


def format_date(date_string):
    """
    Format a date string for display.
    
    Args:
        date_string (str): ISO format date string
        
    Returns:
        str: Formatted date string
    """
    try:
        from datetime import datetime
        date_obj = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return date_obj.strftime("%b %d, %Y at %I:%M %p")
    except Exception:
        return date_string


def print_success(message):
    """Print a success message."""
    print(f"\n✅ {message}")


def print_error(message):
    """Print an error message."""
    print(f"\n❌ {message}")


def print_info(message):
    """Print an info message."""
    print(f"\nℹ️  {message}")


def print_warning(message):
    """Print a warning message."""
    print(f"\n⚠️  {message}")


def print_separator():
    """Print a visual separator line."""
    print("=" * 50)


def create_table(headers, rows):
    """
    Create a simple formatted table.
    
    Args:
        headers (list): List of column headers
        rows (list): List of rows (each row is a list of values)
    """
    # Calculate column widths
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # Print header
    header_row = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))

    # Print rows
    for row in rows:
        print(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))


def pause_execution(message="Press Enter to continue..."):
    """Pause execution until user presses Enter."""
    input(f"\n{message}")


def confirm_action(prompt="Are you sure? (yes/no): "):
    """
    Ask user for confirmation.
    
    Args:
        prompt (str): The confirmation prompt
        
    Returns:
        bool: True if confirmed, False otherwise
    """
    response = input(f"\n{prompt}").strip().lower()
    return response in ("yes", "y")


def get_percentage(value, total):
    """
    Calculate percentage.
    
    Args:
        value (float): The value
        total (float): The total
        
    Returns:
        float: Percentage value
    """
    if total == 0:
        return 0
    return (value / total) * 100
