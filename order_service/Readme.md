# Order Service

This microservice handles order management. It includes functionalities such as creating orders, fetching orders by ID, and retrieving orders for a specific user. The service also integrates with RabbitMQ for event-driven messaging (e.g., order creation events).

## Features

- **Create Order**: Allows users to place new orders.
- **Get Order by ID**: Retrieves the details of an order by its ID.
- **Get Orders by User**: Fetches all orders associated with a specific user.

## Setup Instructions

### Technologies
- Python
- PostgreSQL 
- Docker 
- RabbitMQ

### Running the Service Locally

1. Clone the repository and navigate to the order service directory:

    ```bash
    cd order_service
    ```

2. Create a virtual environment:

    ```bash
    python -m venv ordervenv
    source ordervenv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Before running the service, update the database configuration in `config.py` to point to your local PostgreSQL instance (e.g., update the `SQLALCHEMY_DATABASE_URI` to `postgresql://localhost/yourdb`).

5. Run the database migrations:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

6. Ensure RabbitMQ is installed and running on your system. Update the RabbitMQ configuration in `config.py` to point to your local RabbitMQ instance.

7. Run the message consumer:

    ```bash
    python consumer.py
    ```

8. Now, run the service:

    ```bash
    python manage.py
    ```

    The service will be available at http://localhost:5000/orders

### Running with Docker

1. Build and run the Docker container:

    ```bash
    docker-compose up --build
    ```

    The service will now be available at http://localhost:5003/orders

## API Endpoints

The following endpoints are available for interacting with the order service:

- **Create Order**
  - **URL**: `/create_order`
  - **Method**: `POST`
  
- **Get Order by ID**
  - **URL**: `/order/<int:order_id>`
  - **Method**: `GET`
  
- **Get Orders by User**
  - **URL**: `/user/<int:user_id>`
  - **Method**: `GET`

## Notes
- Ensure that the configurations for both the `product_service` and `order_service` are correctly set to point to the local RabbitMQ instance for messaging.
