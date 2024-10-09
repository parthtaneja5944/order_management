# GraphQL Gateway Service

This service acts as a gateway that consolidates data from multiple microservices (User Service, Product Service, and Order Service) and exposes a unified GraphQL API for querying and managing users, products, and orders.

## Features

- **Unified GraphQL API**: Combines user, product, and order services into a single GraphQL schema.
- **JWT Authentication**: Secures protected endpoints using JWT tokens.
- **Asynchronous Communication**: Utilizes RabbitMQ for event-driven messaging between services.


## Setup Instructions

### Running the Service Locally

1. Clone the repository and navigate to the GraphQL Gateway service directory:

    ```bash
    cd api_gateway
    ```

2. Create a virtual environment:

    ```bash
    python -m venv apivenv
    source apivenv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the GraphQL Gateway:

    ```bash
    python manage.py
    ```

### Running with Docker

1. Build and run the Docker container:

    ```bash
    docker compose build
    docker compose up
    ```

    The service will now be available at:

    - http://localhost:6000/graphql for local setup
    - http://localhost:6001/graphql after Dockerizing the application

## GraphQL Endpoints

### User Queries

- **Register User**

    ```bash
    mutation {
      registerUser(input: {
        username: "parth", 
        email: "parth146@gmail.com", 
        password: "password123", 
        address: "rewari", 
        type: "admin"
      }) {
        id
        username
        email
        address
      }
    }
    ```

- **Login User (Generate Bearer Token)**

    ```bash
    mutation {
      loginUser(input: {
        email: "parth45@gmail.com", 
        password: "password123"
      })
    }
    ```

- **Get User Profile** (Requires Authorization Header: Bearer token)

    ```bash
    query {
      user(id: 4) {
        id
        username
        email
      }
    }
    ```

- **Get All Users** (Requires Authorization Header: Bearer token)

    ```bash
    query {
      users {
        id
        username
        email
      }
    }
    ```

### Product Queries

- **Create Product** (Requires Authorization Header: Bearer token)

    ```bash
    mutation {
      createProduct(input: {
        name: "pepsi3", 
        price: 50, 
        description: "pepsi", 
        inventory: 20
      }) {
        id
        name
        price
        inventory
        description
      }
    }
    ```

- **Get All Products**

    ```bash
    query {
      products {
        id
        name
        price
      }
    }
    ```

- **Get Product by ID** (Requires Authorization Header: Bearer token)

    ```bash
    query {
      product(id: 3) {
        id
        name
        price
      }
    }
    ```

### Order Queries

- **Place Order** (Requires Authorization Header: Bearer token)

    ```bash
    mutation {
      placeOrder(input: {
        userId: 21, 
        products: [
          {productId: 1, quantity: 1}, 
          {productId: 2, quantity: 1}
        ]
      }) {
        id
        products {
          productId
          quantity
        }
      }
    }
    ```

- **Get All Orders for User** (Requires Authorization Header: Bearer token)

    ```bash
    query {
      orders {
        id
        userId
        products {
          productId
          quantity
        }
      }
    }
    ```

- **Get Order by ID**

    ```bash
    query {
      orders {
        id
        userId
        products {
          productId
          quantity
        }
      }
    }
    ```

