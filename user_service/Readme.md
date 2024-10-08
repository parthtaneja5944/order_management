# User Service

This microservice handles user management for the e-commerce platform. It includes functionalities such as user registration, authentication, profile management, updating user details, and password management.

## Features

- **User Registration**: Allows new users to sign up.
- **User Login**: Generates JWT tokens for authenticated users.
- **Profile Management**: Fetches and updates user details.
- **Password Update**: Allows users to update their password.
- **User Listing**: Fetches all users and retrieves individual user details.

## Setup Instructions

### Technologies
- Python
- PostgreSQL
- Docker
- RabbitMQ

### Running the Service Locally

1. Clone the repository and navigate to the user service directory:

    ```bash
    cd user_service
    ```

2. Create a virtual environment:

    ```bash
    python -m venv uservenv
    source uservenv/bin/activate
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

6. Now, run the service:

    ```bash
    python manage.py
    ```

    The service will be available at http://localhost:5000/users

### RabbitMQ Installation and Configuration

To handle messaging between services (like `order_service` and `product_service`), you'll need to install RabbitMQ.

1. Install RabbitMQ on your system:

2. Update the `config.py` in both `order_service` and `product_service` to point to your local RabbitMQ instance:
   
   - Example:
     ```python
     RABBITMQ_URI = 'amqp://localhost'
     ```

3. Run RabbitMQ in the background using the following command:

    ```bash
    sudo rabbitmq-server
    ```

### Running `consumer.py` for Messaging

1. Navigate to the respective directories for `order_service` and `product_service`:

    ```bash
    cd order_service
    cd product_service
    ```

2. In each service, run the `consumer.py` file to start listening to RabbitMQ messages:

    ```bash
    python consumer.py
    ```

3. Make sure that RabbitMQ is running, and both consumers are connected to handle messages between the services.

### Running with Docker

1. Build and run the Docker container:

    ```bash
    docker-compose up --build
    ```

    The service will now be available at http://localhost:5001/users
