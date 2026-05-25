# CLI E-Commerce Application & HTML Store

A complete e-commerce solution with a robust Python CLI application and a modern HTML store interface.

## 📦 What's Included

### Python CLI Application
- **main.py** - Entry point with interactive menu system
- **auth.py** - User authentication (login/register)
- **products.py** - Product management and searching
- **cart.py** - Shopping cart operations
- **orders.py** - Order creation and history
- **api_client.py** - HTTP API communication layer
- **config.py** - Configuration management
- **utils.py** - Helper functions and utilities
- **requirements.txt** - Python dependencies
- **.env.example** - Environment variable template

### HTML Store Interface
- **store.html** - Modern, responsive web store with:
  - Product catalog with filtering and search
  - Shopping cart sidebar
  - Category and price filtering
  - Product sorting options
  - Responsive design for mobile and desktop
  - 12 sample products

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- A backend API (or modify config for your preferred endpoint)

### Installation

1. **Clone/Download the files**
   ```bash
   # Create a project directory
   mkdir cli-ecommerce
   cd cli-ecommerce
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your API configuration
   # API_BASE_URL=http://localhost:5000/api
   # API_KEY=your_secret_api_key_here
   ```

## 🎯 Using the Applications

### Python CLI Application

Run the main application:
```bash
python main.py
```

**Features:**
- ✅ User registration and login
- ✅ Browse product catalog
- ✅ Add items to shopping cart
- ✅ Update item quantities
- ✅ Remove items from cart
- ✅ Checkout and create orders
- ✅ View order history
- ✅ Secure authentication

**Main Menu Flow:**
```
1. Login/Register
   ↓
2. Browse Products
   ↓
3. Manage Cart (Add/Update/Remove items)
   ↓
4. Checkout (Create order)
   ↓
5. View Order History
```

### HTML Store Interface

1. Open `store.html` in any modern web browser
2. No server required - runs entirely client-side for demo purposes

**Features:**
- 🛍️ Browse 12 sample products
- 🔍 Search products by name or description
- 📂 Filter by category (Electronics, Fashion, Home, Beauty)
- 💰 Filter by price range
- 📊 Sort by price, newest, or featured
- 🛒 Shopping cart with real-time updates
- 📱 Responsive mobile design
- ✨ Modern, elegant UI

**Navigation:**
1. Use search bar to find products
2. Apply filters and sorting
3. Click "Add to Cart" to add items
4. Click cart icon in header to view cart
5. Items are shown with live quantity and total

## 📋 API Integration

The Python CLI communicates with a REST API backend. Expected endpoints:

| Action | Method | Endpoint | Purpose |
|--------|--------|----------|---------|
| Register | POST | `/auth/register` | Create new user account |
| Login | POST | `/auth/login` | Authenticate user |
| Get Products | GET | `/products` | List all products |
| Search Products | GET | `/products/search` | Search product catalog |
| Add to Cart | POST | `/cart/add` | Add item to cart |
| Update Cart | PUT | `/cart/update/<id>` | Update item quantity |
| Remove from Cart | DELETE | `/cart/item/<id>` | Remove item from cart |
| Clear Cart | POST | `/cart/clear` | Empty shopping cart |
| Create Order | POST | `/orders` | Place an order |
| Get User Orders | GET | `/users/<id>/orders` | Fetch order history |

### Setting Up a Mock API (Optional)

For testing without a backend:

```python
# Use Flask or FastAPI to create a quick mock API
# Example with Flask:

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify({
        "products": [
            {"id": 1, "name": "Product 1", "price": 29.99, "stock": 10},
            {"id": 2, "name": "Product 2", "price": 49.99, "stock": 5}
        ]
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    return jsonify({
        "user": {"id": 1, "name": "John Doe", "email": "john@example.com"},
        "token": "fake_jwt_token_here"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## 📁 Project Structure

```
cli-ecommerce/
├── main.py                 # CLI application entry point
├── auth.py                 # Authentication manager
├── products.py             # Product management
├── cart.py                 # Cart operations
├── orders.py               # Order management
├── api_client.py           # API communication
├── config.py               # Configuration
├── utils.py                # Helper functions
├── store.html              # Web store interface
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🧪 Testing

The project includes test file placeholders. To add tests:

```bash
# Create test files in a tests/ directory
mkdir tests
touch tests/test_auth.py tests/test_cart.py tests/test_api_client.py

# Run tests
pytest tests/ -v
```

Example test structure:
```python
# tests/test_auth.py
import pytest
from auth import AuthManager

def test_email_validation():
    auth = AuthManager()
    assert auth.validate_email("test@example.com") == True
    assert auth.validate_email("invalid-email") == False

def test_password_validation():
    auth = AuthManager()
    assert auth.validate_password("short") == False
    assert auth.validate_password("validpassword123") == True
```

## 🔐 Security Considerations

1. **API Keys**: Never commit `.env` file with real keys
2. **Passwords**: Always hash passwords server-side
3. **Tokens**: Use JWT or similar for authentication
4. **HTTPS**: Use HTTPS in production
5. **Input Validation**: All inputs are validated client-side and should be validated server-side too
6. **CORS**: Configure CORS properly for your domain

## 🎨 Customization

### Modify Store Products (HTML)
Edit the `sampleProducts` array in `store.html`:
```javascript
const sampleProducts = [
    {
        id: 1,
        name: "Your Product",
        price: 99.99,
        category: "your-category",
        image: "🎯",
        description: "Product description",
        stock: 10
    }
];
```

### Customize CLI Colors and Styling
Edit the emojis and text in `main.py`:
```python
print("1.  🛍️  Browse Products")
print("2.  🛒 View Shopping Cart")
```

### Configure API Endpoints
Edit `.env` file:
```
API_BASE_URL=https://your-api.com/api
API_KEY=your_production_key
```

## 📚 Key Features Explained

### Authentication Flow
1. User registers with email and password
2. Server validates and creates account
3. Login returns authentication token
4. Token is used for subsequent requests

### Shopping Cart
- Items stored in memory (Python) or localStorage (HTML)
- Quantities can be updated
- Cart persists during session
- Clear on successful checkout

### Order Processing
1. User adds items to cart
2. Reviews cart total
3. Confirms checkout
4. Order created via API
5. Cart cleared after success
6. Order appears in history

## 🚨 Troubleshooting

**"Connection refused" error**
- Ensure API server is running
- Check API_BASE_URL in .env file
- Verify port number (default: 5000)

**"Invalid API key" error**
- Check API_KEY in .env file
- Regenerate key if expired

**Products not loading**
- Verify API_BASE_URL is correct
- Check network connectivity
- Enable debug mode in config.py

**Cart not persisting**
- In HTML: Check browser localStorage
- In Python CLI: Cart exists only during session

## 📖 Resources

- [Python Requests Documentation](https://docs.python-requests.org/)
- [REST API Design Best Practices](https://restfulapi.net/)
- [HTML/CSS Best Practices](https://developer.mozilla.org/en-US/docs/Web/)

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to:
- Add new features
- Improve error handling
- Enhance UI/UX
- Optimize performance
- Add comprehensive tests

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Verify environment configuration
4. Check Python and dependency versions

---

**Happy Coding! 🚀**

Built with Python and vanilla JavaScript. Fully functional e-commerce solution ready for customization.
