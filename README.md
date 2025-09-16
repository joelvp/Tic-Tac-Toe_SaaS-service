# Tic-Tac-Toe SaaS Service

**Author:** Joel Valverde de Pedro

---

## 📖 Project Description

This project is a **web-based SaaS Tic-Tac-Toe service** implemented in Python using FastAPI.  
It allows creating matches, making moves, and checking game status while enforcing game rules:

- Three in a row horizontally, vertically, or diagonally wins.  
- Convention used: **X plays first**.  
- Error handling for invalid moves without breaking the match.

The project follows **Domain-Driven Design (DDD)** principles, **Hexagonal Architecture**, and **Clean Architecture** concepts, along with **Twelve-factor App** guidelines to ensure maintainability and scalability.

---

## 🛠 Technologies and Technical Decisions

- **Python 3.12**  
- **FastAPI** as the web framework  
- **SQLAlchemy** for database persistence (PostgreSQL)  
- **Logging**: traces logged to `stderr` using appropriate levels (`INFO`, `ERROR`, `WARNING`, `DEBUG`)  
- **Testing**: pytest for unit tests and code coverage (`coverage`)  
- **Docker**: optional, image available for local or production-like deployment  

**Key technical decisions:**

1. **Domain-Driven Design (DDD)** and **Hexagonal Architecture** to separate domain logic, infrastructure, and API layers.  
2. **Stateless architecture**, each request does not depend on previous server state.  
3. **Match repository pattern** to separate business logic from persistence.  
4. Strict validation of moves and turn control to maintain match integrity.  
5. Clean, modular code following **Clean Architecture** principles.  
6. Logging and thorough tests to ensure observability and reliability.

---


> ⚠️ **Important**: Make sure **Docker is running** before starting the application or running tests, as some services (like the database in integration tests) depend on containers.

## 🔧 Environment Variables

This project requires an `.env` file with configuration details for the application and database.  
**Do not commit your real `.env` file** to GitHub; instead, an example file is provided as `.env.example`.

### Steps:

1. Copy the example file to create your own `.env`:

```bash
copy .env.example .env   # Windows
```

2. Edit the .env file to match your local setup. For example:

```bash
DB_USER=ttt_user
DB_PASSWORD=ttt_pass
DB_HOST=db
DB_PORT=5432
DB_NAME=ttt_db
```

3. When using Docker Compose, the .env file will be automatically loaded.
You can also access these environment variables in your local setup without Docker.


## 🚀 Deployment and Execution

### Locally with Python

1. Build and start the service:

```bash
docker-compose up --build
```

2. Access the API documentation:

```bash
http://localhost:8000/docs
```

3. To stop the service:

```bash
docker-compose down
```

### Notes

- No need to manually install Python dependencies locally.  
- The service runs stateless and uses a database container for persistence.  
- All logs are output to `stderr` and visible in the Docker Compose logs.

## 🧪 Testing

This project includes both **unit tests** and **integration tests** to ensure correctness and reliability.  
Tests rely on [pytest](https://docs.pytest.org/), [coverage](https://coverage.readthedocs.io/), and [testcontainers](https://testcontainers-python.readthedocs.io/) for containerized Postgres databases.

### 1. Install development dependencies
Create and activate a virtual environment, then install the development requirements:

```bash
python -m venv venv
source venv\Scripts\activate # Windows
pip install -r requirements-dev.txt
```

### 2. Run all tests

```bash
coverage run -m pytest
```

### 3. HTML Coverage

```bash
coverage html
```