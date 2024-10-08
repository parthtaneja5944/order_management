# Product Service

This microservice handles product management. It includes functionalities such as product creation, inventory updates, fetching product details, and deleting products. It also integrates with RabbitMQ for event-driven messaging (e.g., product deletion events).

## Features

- **Product Creation**: Allows the creation of new products.
- **Inventory Update**: Updates the inventory of existing products.
- **Get Product by ID**: Retrieves the details of a product by its ID.
- **Product Deletion**: Deletes a product from the inventory.
- **Get All Products**: Fetches a list of all products.

## Setup Instructions

### Technologies
- Python
- PostgreSQL 
- Docker 
- RabbitMQ

### Running the Service Locally

1. Clone the repository and navigate to the product service directory:

    ```bash
    cd product_service
    ```

2. Create a virtual environment:

    ```bash
    python -m venv productvenv
    source productvenv/bin/activate
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

    The service will be available at http://localhost:5000/products

### Running with Docker

1. Build and run the Docker container:

    ```bash
    docker-compose up --build
    ```

    The service will now be available at http://localhost:5002/products

## API Endpoints

The following endpoints are available for interacting with the product service:

- **Create Product**
  - **URL**: `/create`
  - **Method**: `POST`
  
- **Update Inventory**
  - **URL**: `/<int:product_id>/update_inventory`
  - **Method**: `PUT`
  
- **Get Product by ID**
  - **URL**: `/<int:product_id>`
  - **Method**: `GET`
  
- **Delete Product**
  - **URL**: `/<int:product_id>/delete`
  - **Method**: `DELETE`
  
- **Get All Products**
  - **URL**: `/`
  - **Method**: `GET`

## Notes
- Ensure that the configurations for both the `order_service` is correctly set to point to the local RabbitMQ instance for messaging.
