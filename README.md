# E-Commerce Platform

## Overview

This project is an E-Commerce platform built using a microservices architecture. It includes user management, product management, and order processing services, all of which communicate through a GraphQL gateway. The services are containerized using Docker for easy deployment and scalability.

## Features

- **User Service**: Handles user registration, authentication, and profile management.
- **Product Service**: Manages product creation, updates, inventory management, and fetching product details.
- **Order Service**: Processes user orders, manages order statuses, and integrates with inventory management.
- **API Gateway**: Provides a unified GraphQL API for interacting with all services.
- **JWT Authentication**: Secures API endpoints with JSON Web Tokens.
- **Event-Driven Architecture**: Uses message queues for asynchronous communication between services.

## Technologies Used

- Python (Flask)
- PostgreSQL
- Docker
- GraphQL (Graphene)
- JWT (Flask-JWT-Extended)
- RabbitMQ for messaging


## Setup Instructions


### Running the Project
- git clone 
-  docker-compose up --build


   

