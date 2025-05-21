# Spy Cat Agency — Backend

This is the backend service for the **Spy Cat Agency** project, built with **FastAPI**, **PostgreSQL**, and **Docker**.

---

## 🚀 Quick Start with Docker

> Make sure you have the following installed:
> - [Docker](https://www.docker.com/)
> - [Docker Compose](https://docs.docker.com/compose/)

### 1. Copy Environment Template

Create a `.env` file from the provided template:

```bash
cp env.dist .env
```
Edit the values in .env as needed (especially database credentials or port).

### 2. Run the Project
Build and start the services using Docker Compose:
```bash
docker-compose up --build -d
```

### 3. Access the API
Base URL: http://<your_machine_host>:<port_from_env>

###### if DEBUG=True
Swagger UI: http://<your_machine_host>:<port_from_env>/docs 

