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

## ⚙️ Database Configuration

This project uses **PostgreSQL running inside a Docker container**.  
The database is initialized automatically when you run `docker-compose up`.  

There are **two sets of environment variables** to understand:

| Variable | Purpose |
|----------|---------|
| `POSTGRES_USER` | Username **created inside the PostgreSQL container** at initialization. |
| `POSTGRES_PASSWORD` | Password for the PostgreSQL user. Only used when the container is first created. |
| `POSTGRES_DB` | Database created inside the container at startup. |
| `DB_USER` | Username your **application** uses to connect to the database. |
| `DB_PASSWORD` | Password your application uses to connect. |
| `DB_NAME` | Database your application connects to. |
| `DB_HOST` | Hostname of the database (in Docker Compose, this is usually `db`). |
| `DB_PORT` | Port your application connects to (default: 5432). |

### How it works

1. **Container initialization**  
   When PostgreSQL starts for the first time, it reads `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` and creates the database and user.  
   After that, these variables are **not used again** unless the container is destroyed and recreated.

2. **Application connection**  
   Your FastAPI app uses `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_HOST`, and `DB_PORT` to connect to the database.  
   These values **must match an existing database and user** in PostgreSQL. Typically, for local development, you can use the same values as `POSTGRES_*`.

3. **Changing values**  
   - Changing `POSTGRES_*` after the database is created has **no effect** on the existing database.  
   - Changing `DB_*` will make your app try to connect with different credentials. If the user or database does not exist, the connection will fail.

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

POSTGRES_USER=ttt_user
POSTGRES_PASSWORD=ttt_pass
POSTGRES_DB=ttt_db
```

3. When using Docker Compose, the .env file will be automatically loaded.
You can also access these environment variables in your local setup without Docker.


## 🚀 Deployment and Execution

> ⚠️ **Important**: Make sure **Docker is running** before starting the application or running tests, as some services (like the database in integration tests) depend on containers.

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

## Future Improvements – User Management

### 1️⃣ Feature Overview – Users

**Goal:** Introduce a **User** concept to the service to manage player identities.  
**Assumptions:**  
- Minimal authentication with `username` + `password`.  
- Each user can create matches and track their own games.  
- Players are linked to a `User` entity rather than anonymous identifiers.

**Features:**
- User registration and optional profile info (email, display name).  
- User login / authentication (basic).  
- Assigning matches to users.  
- Querying match history per user.

### 2️⃣ API Changes

**Existing endpoints** remain, but must now include `userId` to identify players.

#### New Endpoints:

1. **POST /users/register**  
   - Registers a new user.  
   - Payload:
   ```json
   {
     "username": "player1",
     "password": "secret123",
     "email": "player1@example.com"  // optional
   }
   ```

   - Response:
   ```json
    {
    "userId": "uuid",
    "username": "player1",
    "email": "player1@example.com"
    }
   ```

2. **POST /users/login**
   - Authenticates a user.  
   - Payload:
   ```json
   {
     "username": "player1",
     "password": "secret123"
   }
   ```

   - Response:
   ```json
    {
    "userId": "uuid",
    "authToken": "token123"
    }
   ```

3. **GET /users/{userId}/matches**
    - Returns the list of matches associated with the user.

#### **Updated Endpoints:**
- **POST /create** → now accepts `userId` of the creator.
- **POST /move** → validated against `userId` to ensure correct player moves.
- **GET /status** → optionally include player information.

### 3️⃣ Database Structure

#### **Users Table:**

| Column      | Type       | Notes                  |
|------------|-----------|-----------------------|
| id         | UUID      | Primary key           |
| username   | VARCHAR   | Unique                |
| password   | VARCHAR   | Hashed                |
| email      | VARCHAR   | Optional              |
| created_at | TIMESTAMP | Default now()         |

#### **Games Table:**


| Column       | Type       | Notes                                           |
|-------------|-----------|-----------------------------------------------|
| id          | UUID      | Primary key                                   |
| player_x_id | UUID      | FK → users.id                                 |
| player_o_id | UUID      | FK → users.id                                 |
| board       | JSON      | Current state of the board (3x3 list)         |
| next_player | VARCHAR   | "X" or "O", None if game finished             |
| winner      | VARCHAR   | "X", "O" or None                              |
| is_finished | BOOLEAN   | True or False                                |
| created_at  | TIMESTAMP | Default now()                                 |

### 4️⃣ Architectural Design Notes

- Introduce a **UserRepository** following **DDD** and **Hexagonal Architecture** principles to handle user-related operations.  
- Minimal authentication is stored in the **infrastructure layer**, separate from business logic.  
- The **Match service** now references `userId` instead of anonymous marks.  
- The service **remains stateless**, no major infrastructure changes required for this step.  
- Logging and observability extend naturally to user actions (e.g., user registration, login, match creation).  
- This design allows **future horizontal scalability**, enabling multiple instances of the service to run concurrently.  
- All proposed changes are backward-compatible with existing games and gameplay logic.  
