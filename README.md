https://www.loom.com/share/b591d636142544fbb407759731c1f834?sid=0cb94b61-9e37-496d-bbf4-91f8e2004081

# MSME E-commerce Platform

## Project Overview
This project is an e-commerce platform tailored for Micro, Small, and Medium Enterprises (MSMEs). It provides a seller portal where businesses can manage their products and interact with customers.

## Features
- Seller registration and authentication
- Product management (CRUD operations)
- Automated product description generation using AI
- Celery task queue for background processing

## Tech Stack
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker

## Getting Started

### Prerequisites
- Docker and Docker Compose

### Installation
1. Clone the repository:
   ```
   git clone [your-repository-url]
   cd msmeEcomm
   ```

2. Create a `.env` file in the root directory and add your environment variables:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

4. The application should now be running at `http://localhost:8000`

## Project Structure
- `msmeEcomm/`: Main Django project directory
- `sellerPortal/`: Django app for seller-related functionality
- `docker-compose.yaml`: Docker Compose configuration
- `Dockerfile`: Docker configuration for the web application

## API Endpoints
- `/signup/`: Register a new seller
- `/login/`: Authenticate a seller
- `/products/`: List and create products
- `/products/<id>/`: Retrieve, update, or delete a specific product

## Running Tests
To run the test suite: