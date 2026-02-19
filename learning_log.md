# Day 1 – Setup & Foundation

## What I did

- Understood RBAC problem
- Set up FastAPI project
- Created virtual environment
- Connected SQLite database

## What I learned

- How to connect to database
- How FastAPI app starts and runs

## Challenges

- Understanding project structure
- VS Code showed deprecation warning for @app.on_event("startup")

## How I solved them

- Studied real-world backend folder layouts
- Studied documentation

# Day 2 – Data Models & Many-to-Many Relationships

## What I did

- Designed and implemented the three core SQLAlchemy models: User, Role, Permission
- Created two bridge (association) tables: user_roles and role_permissions
- Set up relationship() fields to navigate between models

## What I learned

- How SQLAlchemy handles many-to-many relationships using the secondary parameter on relationship().
- How Base.metadata.create_all() automatically creates all tables on startup.

## Challenges

Initially confused about where to define the bridge tables — inside the model file or separately.

## How I solved them

Defined each bridge table in the same file as the "owning" model (e.g., role_permissions lives in role.py) to keep things co-located and avoid circular imports.

# Day 3 – Password Hashing & JWT Authentication

## What I did

- Implemented hashing.py using passlib with the bcrypt scheme for secure password storage.
- Built jwt_handler.py to create and verify JWT access tokens using python-jose.
- Loaded secrets (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES) from a .env file via python-dotenv.

## What I learned

- How bcrypt one-way hashing works — you never store or compare plain-text passwords.
- The structure of a JWT: header, payload (sub, exp), and signature.
- How dt.timezone.utc is required for timezone-aware expiry — naive datetimes cause issues with JWT validation.

## Challenges

- The token expiry initially used a naive datetime.utcnow() which caused deprecation warnings.
- Understanding the difference between encoding and decoding a JWT and when each step happens.

## How I solved them

- Switched to dt.datetime.now(dt.timezone.utc) for timezone-aware timestamps.
- Traced the full auth flow: login → encode token → client sends token → decode token → extract sub → look up user.

# Day 4 – Repository & Service Layers

## What I did

- Built user_repo.py.
- Built auth_service.py with register_user_service() and login_user_service() containing all business logic.

## What I learned

- The purpose of the repository pattern — it separates SQL queries from business logic, making both easier to test and change independently.
- How db.add(), db.commit(), and db.refresh() work together: add stages the object, commit writes it, refresh re-reads it from the DB.
- How to raise meaningful HTTPException errors (e.g., 409 Conflict for duplicate usernames, 401 Unauthorized for wrong passwords) instead of generic 500 errors.

## Challenges

- The service layer needed access to Role to assign a default role to new users, which felt like it was mixing concerns.
- Deciding what counts as "business logic" vs. "data access".

# Day 5 – Auth Routes

## What I did

- Created Pydantic schemas (UserRegisterRequest, UserLoginRequest, TokenResponse) in user_schema.py.
- Built auth_routes.py with three endpoints: POST /auth/register, POST /auth/login, GET /auth/me.
- Switched the login endpoint from a custom JSON body to OAuth2PasswordRequestForm so it works with FastAPI's built-in Swagger UI "Authorize" button.

## What I learned

- How Pydantic models auto-validate incoming request bodies — if a required field is missing or the wrong type, FastAPI returns a 422 Unprocessable Entity before the function even runs.
- The difference between accepting JSON (BaseModel) and form data (OAuth2PasswordRequestForm).
- How Depends() is FastAPI's dependency injection system — clean, testable, and reusable.

## Challenges

- The Swagger UI "Authorize" button didn't work when the login endpoint accepted a JSON body — it expects form data
- Understanding why Depends(get_db_session) works as a generator (using yield) rather than returning a value

## How I solved them

- Replaced UserLoginRequest with OAuth2PasswordRequestForm = Depends() on the login endpoint
- Learned that yield-based dependencies allow FastAPI to run cleanup code (like db.close()) after the request finishes — similar to a finally block


# Day 6 – Authorization Middleware & Protected Routes

## What I did

- Built dependencies.py.
- Built authorization.py with require_permission().
- Created protected_routes.py with two permission-gated routes: GET /test/read and POST /test/delete

Challenges

Understanding why require_permission needed to be a function that returns a function, rather than just a regular dependency
SQLAlchemy lazy loading: role.permissions sometimes returned an empty list even when permissions existed in the database

# Day 7 – Seeding, Router Registration & Final Wiring

## What I did

- Built seed.py to populate the database with default roles, permissions, and an admin user on every startup.
- Registered all routers in app/api/__init__.py and included them in main.py


- Added securegate.db and myenv/ to .gitignore