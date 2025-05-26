# Ecommerce Website

![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange)
[![Swagger](https://img.shields.io/badge/API-Swagger-orange)](http://authb.onrender.com/api)

This projects consist of a 

frontend => (https://github.com/RobertFacundo/eCommerceF)

&

backend => (https://github.com/RobertFacundo/eCommerceB)

working together to provide an eCommerce.


## Deployment
-Frontend: Deployed to Vercel via the web interface, communicates with the backend API.

-Backend: Deployed to Render using the VSC CLI, handles authentication and data processing.

---

# Backend

### DataBase
The project uses a dynamic database configuration. By default, it runs on SQLite for local development.
If the DATABASE_URL environment variable is set, it connects automatically to a PostgreSQL database.

### 📦 Environment Variables
In Django, environment variables are managed through the settings.py file using Python’s built-in os.environ. This allows different configurations based on the environment (e.g., development vs. production).

In production, variables like DATABASE_URL are expected to be set in the environment.

In local development, fallback values (like SQLite) are used if DATABASE_URL is not defined.

You can use packages like django-environ to load .env files automatically (similar to NestJS's ConfigModule).

### 🔌 DataBase Connection
Django uses its built-in ORM to interact with databases (similar to TypeOrmModule in NestJS).

The dj_database_url package is used to parse the DATABASE_URL environment variable and automatically configure the database connection.

If DATABASE_URL is not found, Django defaults to using SQLite for local development.

### Module & Endpoints
This API is built with Django and Django REST Framework. It provides the following endpoints:

🛍️ Product
Base route: /products/
Available Methods:

GET /products/ – Retrieve a list of all products

GET /products/:id/ – Retrieve details of a specific product

POST /products/ – Create a new product (admin or authorized users only)

PUT /products/:id/ – Update an existing product (admin or authorized users only)

DELETE /products/:id/ – Delete a product (admin or authorized users only)

-------


🛒 Cart
Base route: /cart/
Available Methods:

GET /cart/ – Retrieve the authenticated user's cart

POST /cart/add_product/ – Add a product to the cart
Request Body:
```json
{
  "product_id": <int>,
  "quantity": <int>
}
```
POST /cart/remove_product/ – Remove a product from the cart
Request Body:
```json
{
  "product_id": <int>
}
```
POST /cart/clear/ – Remove all items from the cart

🔐 All cart endpoints require user authentication.

-----------

👤 Authentication
Routes:

POST /register/ – Register a new user
Request Body:
```json
{
  "username": "yourUsername",
  "email": "yourEmail@example.com",
  "password": "yourPassword"
}
```
POST /login/ – Log in an existing user
Request Body:
```json
{
  "username": "yourUsername",
  "password": "yourPassword"
}
```
📌 The login response includes user credentials. If you're using JWT, the token should be used for authorized requests.

------------
### Documentation
This project uses Swagger (drf-yasg) to automatically generate interactive API documentation.

The documentation can be accessed via the following routes:

/swagger/ – Swagger UI (interactive API explorer)
If you'll try the swagger endpoints first login and then retrieve the Token for authentication

/redoc/ – ReDoc UI (alternative API documentation)

/swagger.json – Raw OpenAPI schema (JSON format)

---
Created By Robert Facundo
---