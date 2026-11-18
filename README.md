# FerreStock Backend

A Django REST Framework API for inventory management system designed for hardware stores (ferretería). This backend provides comprehensive endpoints for managing products, suppliers, orders, and multi-location inventory tracking.

## Features

- **User Management**: Custom user authentication with support for multiple store locations
- **Product Management**: Full CRUD operations for product inventory
- **Stock Tracking**: Real-time stock management with pending stock functionality
- **Supplier Management**: Manage supplier information and relationships
- **Order Management**: Create and track orders with automatic stock updates
- **Multi-Location Support**: Manage inventory across different store locations
- **JWT Authentication**: Secure API endpoints with token-based authentication

## Tech Stack

- **Django 4.2.6**: Web framework
- **Django REST Framework 3.14.0**: API development
- **PostgreSQL**: Database
- **JWT (SimpleJWT)**: Authentication
- **Gunicorn**: Production server
- **CORS Headers**: Cross-origin resource sharing

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FerreStock_Backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgres://user:password@localhost:5432/ferrestock_db
   SECRET_KEY=your-secret-key
   DEBUG=True
   ```

5. **Set up the database**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## Database Configuration

The project uses PostgreSQL. Update the database settings in `backend/settings.py` or use the `DATABASE_URL` environment variable.

**Local Development:**
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ferrestock_db",
        "USER": "postgres",
        "PASSWORD": "your-password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

## API Endpoints

### Authentication
- `POST /inventory/create/` - Register new user
- `POST /inventory/api/token/` - Obtain authentication token
- `POST /inventory/api/logout/` - Logout (invalidate token)

### Users
- `GET /inventory/users/` - List all registered locations/users
- `GET /inventory/users/?user=<id>` - Filter by specific user

### Products
- `GET /inventory/products/` - List products (filtered by authenticated user)
- `POST /inventory/products/` - Create new product
- `GET /inventory/products/<id>/` - Get product details
- `PUT /inventory/products/<id>/` - Update product
- `DELETE /inventory/products/<id>/` - Delete product
- `GET /inventory/products/users/` - List all products (with optional user filter)
- `PUT /inventory/products/pending/` - Update pending stock status
- `PUT /inventory/products/sales/` - Update stock after sales

### Suppliers
- `POST /inventory/supplier/register/` - Create supplier
- `GET /inventory/suppliers/` - List all suppliers
- `PUT /inventory/supplier/<pk>/edit/` - Update supplier

### Orders
- `POST /inventory/order/create/` - Create order with items
- `GET /inventory/orders/` - List orders (filtered by authenticated user)
- `GET /inventory/orders/?status=<status>` - Filter by status (Pendiente/Entregado)
- `GET /inventory/orders/?supplier=<id>` - Filter by supplier
- `GET /inventory/orders/?id=<id>` - Get specific order
- `POST /inventory/order/update-order-status/` - Update order status and stock
- `DELETE /inventory/order/delete/<pk>/` - Delete order
- `DELETE /inventory/order-item/delete/<pk>/` - Delete order item

## Authentication

All endpoints (except registration and token obtain) require authentication. Include the token in the request header:

```
Authorization: Token <your-token-here>
```

## Models

### CustomUser
- `username`: Unique username
- `email`: Unique email (used for login)
- `password`: Hashed password
- `address`: Store address
- `contact`: Contact information
- `nit`: Tax identification number
- `manager`: Manager name

### Product
- `name`: Product name
- `description`: Product description
- `price`: Product price (Decimal)
- `stock`: Available stock quantity
- `pending_stock`: Units sold but not delivered
- `global_pending`: Boolean flag for pending status
- `category`: Product category
- `user`: Associated user/location

### Supplier
- `company_name`: Supplier company name
- `contact_name`: Contact person name
- `address`: Supplier address
- `tel`: Telephone number
- `email`: Email address

### Order
- `user`: Associated user who created the order
- `date`: Order creation date
- `status`: Order status (Pendiente/Entregado)
- `supplier`: Associated supplier
- `items`: Related order items

### OrderItem
- `order`: Associated order
- `product`: Associated product
- `quantity`: Quantity ordered

## Stock Management Flow

1. **Pending Stock**: When a product is sold but not delivered, it moves to pending stock
   ```
   PUT /inventory/products/pending/
   {
     "product_id": 1,
     "is_pending": "true",
     "quantity": 5
   }
   ```

2. **Sales**: Direct stock reduction for completed sales
   ```
   PUT /inventory/products/sales/
   {
     "product_id": 1,
     "quantity": 3
   }
   ```

3. **Order Delivery**: When an order is marked as delivered, stock is automatically updated
   ```
   POST /inventory/order/update-order-status/
   {
     "order_id": 1
   }
   ```

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Accessing Django Admin
Visit `http://localhost:8000/admin/` and login with your superuser credentials.

## Deployment

The project is configured for deployment on platforms like Render. Make sure to:

1. Set `DEBUG=False` in production
2. Configure `ALLOWED_HOSTS`
3. Set secure `SECRET_KEY`
4. Use environment variables for sensitive data
5. Configure PostgreSQL database URL
6. Set up static files serving

## Project Structure

```
FerreStock_Backend/
├── backend/              # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── inventory/           # Main application
│   ├── models.py        # Database models
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   ├── urls.py          # App URL patterns
│   └── migrations/      # Database migrations
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is private and proprietary.

## Support

For issues and questions, please open an issue in the repository.
