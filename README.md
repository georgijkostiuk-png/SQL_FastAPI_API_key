# Vacation Planner – REST API (FastAPI + MySQL)

A REST API for planning vacations. A **user** creates **todos** (one todo = one planned trip:
from city A to city B on certain dates). For every todo the API can search real **flights** and
**hotels** using SerpApi (Google Flights / Google Hotels) and store the results in a MySQL database.

---

## 1. Requirements

- **Python 3.14** (the project was developed with 3.14; `schema.py` relies on 3.14's lazy type
  annotations, so older versions fail with `NameError: name 'TodoRead' is not defined`)
- **MySQL / MariaDB** running on `localhost:3306`, user `root`, empty password
  (e.g. via **XAMPP**)
- Internet connection (for the flight/hotel search)

---

## 2. Installation

Open a terminal in the project folder (`11_FinalProject_RestAPI_v01`).

**(Optional but recommended) create a virtual environment:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Install all packages from `requirements.txt`:**

```powershell
pip install -r requirements.txt
```

This installs: `fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`, `pymysql`, `cryptography`,
`argon2-cffi`, `bcrypt`, `requests`.

---

## 3. Set up the database (MySQL on localhost:3306)

`localhost:3306` is the **MySQL server port**. It is not a web page, so opening it in the
browser shows nothing useful. You manage the database with **phpMyAdmin** instead.

1. Start **XAMPP Control Panel** → click **Start** for **Apache** and **MySQL**.
   MySQL now listens on port `3306`.
2. Open phpMyAdmin in the browser: **http://localhost/phpmyadmin**
3. Create the database (the program creates the *tables* automatically, but **not** the
   database itself). Click the **SQL** tab and run:

   ```sql
   CREATE DATABASE db_vacations;
   ```

The connection is configured in [database.py](database.py):

```python
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/db_vacations"
#                            user:password@host:port/database
```

If your MySQL user has a password, change it to `root:YOUR_PASSWORD@localhost...`.
For a quick test without MySQL you can switch to the commented‑out SQLite line
`sqlite:///vacations.db`.

---

## 4. Run the program

```powershell
python main.py
```

You should see `Uvicorn running on http://127.0.0.1:8000`. On startup,
`Base.metadata.create_all(...)` creates the tables `user`, `todos`, `flights` and `hotels`
in `db_vacations` if they don't exist yet.

Now open the interactive API page (Swagger UI):

**http://localhost:8000/docs**

There you can try every endpoint: click an endpoint → **Try it out** → fill in the
fields → **Execute**.

Stop the server with `Ctrl + C`.

---

## 5. How to use it (step by step)

### 5.1 Create users

Endpoint: **`POST /users/`**

In `/docs` open *User → POST /users/*, click *Try it out* and paste a JSON body.
Example users are in [users.txt](users.txt):

```json
{
  "username": "max",
  "password": "12345"
}
```

- The password must be 5–20 characters long.
- The password is stored **hashed** with bcrypt (see `util.py`), never in plain text.
- The response contains the new user's `id` – you need it to create todos.

Show all users: **`GET /users/`**

### 5.2 Create todos (planned trips)

Endpoint: **`POST /todo/?user_id=1`**

In `/docs` open *Todos → POST /todo/*, enter the `user_id` (e.g. `1`) and paste a body.
Example todos are in [todos.txt](todos.txt):

```json
{
  "home_city": "Dortmund",
  "departure_id": "DTM",
  "destination_city": "Mallorca",
  "arrival_id": "PMI",
  "vacation_start": "2026-07-20",
  "vacation_end": "2026-07-27"
}
```

- `departure_id` / `arrival_id` are **IATA airport codes** (DTM = Dortmund, PMI = Palma).
- Dates use the format `YYYY-MM-DD`.
- The response contains the todo `id` – you need it to search flights and hotels.

### 5.3 Search flights for a todo

Endpoint: **`POST /flights/{id}/flights2`** (`id` = todo id)

Searches one‑way flights on Google Flights from `departure_id` to `arrival_id` on
`vacation_start` (2 adults, 2 children, economy, non‑stop, prices in EUR) and saves them.
Calling it again deletes the old flights of that todo and saves fresh results.

### 5.4 Search hotels for a todo

Endpoint: **`POST /hotels/hotels?id=1`** (`id` = todo id)

Searches hotels in `destination_city` from `vacation_start` to `vacation_end` on Google Hotels
and saves them. Calling it again replaces the old hotels of that todo.

### 5.5 Look at the data

- In the browser via the `GET` endpoints below, or
- in phpMyAdmin: **http://localhost/phpmyadmin** → `db_vacations` → tables
  `user`, `todos`, `flights`, `hotels`.

---

## 6. All endpoints

| Method | URL | What it does |
|---|---|---|
| **Users** | | |
| POST | `/users/` | Create a user (body: `username`, `password`) |
| GET | `/users/` | List all users (with their todos) |
| POST | `/users/authenticate` | Log in (body: `username`, `password`) |
| **Todos** | | |
| POST | `/todo/?user_id={user_id}` | Create a todo for a user |
| GET | `/todo/todos5` | List all todos |
| GET | `/todo/{user_id}/todos1` | List all todos of one user |
| GET | `/todo/{id}/todos2` | Get one todo by its id |
| GET | `/todo/todos3?id={id}&departure_id={code}` | Change the departure airport of a todo |
| POST | `/todo/todos4?id={id}` | Delete a todo (its flights and hotels are deleted too) |
| **Flights** | | |
| POST | `/flights/{id}/flights2` | Search and save flights for todo `id` |
| GET | `/flights/flights` | List all saved flights |
| GET | `/flights/flights2?departure_id={code}` | List flights from one airport |
| POST | `/flights/flights3?todo_id={id}` | Delete all flights of a todo |
| **Hotels** | | |
| POST | `/hotels/hotels?id={id}` | Search and save hotels for todo `id` |
| GET | `/hotels/hotels2` | List all saved hotels |
| POST | `/hotels/hotels3?todo_id={id}` | Delete all hotels of a todo |

---

## 7. Project structure – how the files work together

```
 Browser / Swagger UI (http://localhost:8000/docs)
                 │  HTTP request (JSON)
                 ▼
            main.py            starts FastAPI + uvicorn, creates tables, registers routers
                 │
                 ▼
           routers.py          URLs/endpoints  ──uses──►  schema.py  (validates JSON in/out)
                 │  calls
                 ▼
             crud.py           repositories: business logic + DB queries + SerpApi calls
            │    │    │
            │    │    └──────► util.py      (bcrypt password hashing)
            │    └───────────► SerpApi      (Google Flights / Google Hotels via requests)
            ▼
        models.py              SQLAlchemy tables: User, Todo, Flight, Hotel
            │
            ▼
       database.py             engine + session (connection to MySQL db_vacations)
            │
            ▼
   MySQL on localhost:3306
```

### Main application files

| File | Role |
|---|---|
| [main.py](main.py) | **Entry point.** Creates the `FastAPI` app, creates all tables (`Base.metadata.create_all`), includes the 4 routers and starts uvicorn on port 8000. |
| [database.py](database.py) | Database connection: `DATABASE_URL`, `engine`, `SessionLocal`, `Base` (parent class for all models) and `get_db()`, which gives every request its own DB session and closes it afterwards. |
| [models.py](models.py) | **Database tables** as SQLAlchemy classes. Relationships: one `User` → many `Todo`; one `Todo` → many `Flight` and many `Hotel`. Deleting a user/todo also deletes its children (cascade). |
| [schema.py](schema.py) | **Pydantic schemas** – describe what JSON the API accepts (`UserCreate`, `TodoCreate`, `UserLogin`) and returns (`UserRead`, `TodoRead`, `FlightRead`, `HotelRead`). Invalid input (e.g. password too short) is rejected automatically with error 422. |
| [routers.py](routers.py) | **REST endpoints.** Four `APIRouter`s (`/users`, `/todo`, `/flights`, `/hotels`). Each endpoint gets a DB session via `Depends(get_db)`, calls a repository from `crud.py` and returns the result in the shape of a schema. |
| [crud.py](crud.py) | **Repositories** (`UserRepository`, `TodoRepository`, `FlightRepository`, `HotelRepository`) – Create/Read/Update/Delete on the database. `FlightRepository` and `HotelRepository` also call the SerpApi web API, convert the JSON results into `Flight`/`Hotel` objects and save them. |
| [util.py](util.py) | Helper functions `hash_password()` and `verify_password()` (bcrypt). Used by `UserRepository`. |

### Test / learning scripts (not used by the API)

| File | Role |
|---|---|
| [search_flight.py](search_flight.py) | Standalone test of a Google Flights search via SerpApi; prints the JSON result. Run with `python search_flight.py`. |
| [search_hotel.py](search_hotel.py) | Standalone test of a Google Hotels search via SerpApi. |
| [crud_flight_test.py](crud_flight_test.py) | Earlier test version of `FlightRepository`. |
| [encode_decode.py](encode_decode.py) | Demo of password hashing with bcrypt and argon2. |

### Data / notes

| File | Role |
|---|---|
| [users.txt](users.txt) | Example JSON bodies for creating users. |
| [todos.txt](todos.txt) | Example JSON bodies for creating todos. |
| [requirements.txt](requirements.txt) | Python packages to install. |
| [readme2.md](readme2.md) | Feature planning notes. |

### Example flow of one request

`POST /flights/3/flights2`:

1. **main.py** has registered `flights_router` → FastAPI sends the request to
   `create_flight_by_todoid_or_update()` in **routers.py**.
2. `Depends(get_db)` from **database.py** opens a DB session.
3. The router calls `FlightRepository(db).new_flight_by_todoid_or_update(3)` in **crud.py**.
4. The repository loads `Todo` #3 (**models.py**), deletes its old flights, sends a request to
   SerpApi with the todo's airports and date, and creates new `Flight` objects.
5. The flights are committed to MySQL and returned.
6. FastAPI converts them to JSON using `FlightRead` from **schema.py**.

---

## 8. Models vs. Schemas

The project has two kinds of "data classes" that look similar but have different jobs:

**`models.py` = the database.  `schema.py` = the API.**

- **Model** (SQLAlchemy): describes a **table in MySQL**. Used to create tables and to
  save/load rows.
- **Schema** (Pydantic): describes the **JSON that the API accepts and returns**. Used to
  validate input and to choose which fields go out.

> Analogy: the model is the filing cabinet in the back office (everything is stored there);
> the schema is the form at the front desk (what the customer must fill in, and what they are
> allowed to see).

| | `models.py` (SQLAlchemy) | `schema.py` (Pydantic) |
|---|---|---|
| Describes | Tables and columns in MySQL | JSON request/response bodies |
| Inherits from | `Base` (from `database.py`) | `BaseModel` (from pydantic) |
| Field types | `Column(String(50))`, `Column(Integer, ForeignKey(...))` | Plain Python types: `str`, `int`, `date` |
| Main job | Store, load and link data (`relationship`, cascade delete) | Validate input, filter output |
| Used in | `crud.py` (queries), `main.py` (`create_all` creates tables) | `routers.py` (request bodies and `response_model=`) |
| Per entity | One class per table (`User`) | Several classes per purpose (`UserCreate`, `UserRead`, `UserLogin`) |

### Example: `User`

```python
# models.py – what the table stores
class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(100))          # bcrypt hash
    todos = relationship("Todo", ...)
```

```python
# schema.py – what the API accepts / returns
class UserCreate(UserBase):                 # INPUT for POST /users/
    password: str = Field(min_length=5, max_length=20)

class UserRead(UserBase):                   # OUTPUT
    id: int
    todos: list[TodoRead] = []              # no password field!
```

Why the schemas differ from the model:

- **`UserCreate` has no `id`** – the database assigns it, the client must not send one.
- **`UserCreate` validates** – a password shorter than 5 characters is rejected with
  error 422 before any of our code runs.
- **`UserRead` has no `password`** – the table stores the hash, but
  `response_model=UserRead` guarantees it is never sent to the client.

### Example: `Todo` and `Flight`

- `TodoCreate` has no `id` and no `user_id` – the user id comes from the URL
  (`POST /todo/?user_id=1`). `TodoRead` adds `id` and `user_id` to the output.
- Flights are created from SerpApi results, never from client input, so only `FlightRead`
  is used (to shape the output).

### How they work together in one request (`POST /users/`)

```
JSON body ──► UserCreate (schema: validate) ──► User(...) (model) ──► crud.py saves to MySQL
                                                                            │
JSON response ◄── UserRead (schema: filter) ◄── User object from DB ◄──────┘
```

In `routers.py` this looks like:

```python
@user_router.post("/", response_model=UserRead)          # output schema
def create_user(user_create: UserCreate, db=Depends(get_db)):   # input schema
    new_user = User(username=user_create.username,       # schema → model
                    password=user_create.password)
    return UserRepository(db).create(new_user)           # model → converted to UserRead
```

Short rule: **models = what is stored, schemas = what is exchanged.**

---

## 9. Troubleshooting

| Problem | Solution |
|---|---|
| `Can't connect to MySQL server on 'localhost'` | Start MySQL in XAMPP. |
| `Unknown database 'db_vacations'` | Run `CREATE DATABASE db_vacations;` in phpMyAdmin. |
| `Access denied for user 'root'` | Put your MySQL password into `DATABASE_URL` in `database.py`. |
| `ModuleNotFoundError: No module named ...` | Run `pip install -r requirements.txt` (in the activated venv). |
| `NameError: name 'TodoRead' is not defined` | Use Python 3.14. |
| Flight/hotel search returns `[]` | No results for that route/date, the date is in the past, or the SerpApi key has no searches left (error is printed in the terminal). |
| Port 8000 already in use | Stop the other server, or change `port=8000` in `main.py`. |

---

## 10. Known limitations

- **`POST /users/authenticate` does not check the password yet** – it only checks that the
  username exists. `UserRepository.find_user_by_credentials_2()` already contains the
  password check with `verify_password()` and could be used instead.
- The **SerpApi key is hard‑coded** in `crud.py`, `search_flight.py`, `search_hotel.py` and
  `crud_flight_test.py`. For a real project it should be read from an environment variable
  (e.g. `os.getenv("SERPAPI_KEY")`) and not be committed to git.
- Some delete/update endpoints use `POST`/`GET` instead of `DELETE`/`PUT`, and the endpoint
  names (`todos1`…`todos5`, `flights2`, `hotels3`) are numbered rather than descriptive.
