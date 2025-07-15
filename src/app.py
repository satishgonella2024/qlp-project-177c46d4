import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import bcrypt
import secrets
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Setup rate limiting
limiter = Limiter(key_func=lambda: secrets.token_urlsafe(16))
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Setup CORS
origins = [
    os.getenv('FRONTEND_URL', 'https://example.com')
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Security setup
security = HTTPBasic()

# Load secrets from env
ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Hash admin password
hashed_password = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt(rounds=12))

# Input models
class User(BaseModel):
    username: str
    password: str

@app.post('/register')
@limiter.limit('10/minute')
def register(user: User):
    # Validate and sanitize inputs
    username = user.username.strip()
    password = user.password.strip()

    if not username or not password:
        raise HTTPException(status_code=400, detail='Username and password are required')

    # Hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))

    # Store user in database (not shown)
    # ...

    return {'message': 'User registered successfully'}

@app.get('/health')
def health_check():
    return {'status': 'ok'}

@app.get('/version')
def get_version():
    return {'version': '1.0.0'}

@app.post('/login')
@limiter.limit('10/minute')
def login(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password.encode('utf-8')

    # Validate admin credentials
    if username != ADMIN_USER or not bcrypt.checkpw(password, hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')

    # Generate and return access token (not shown)
    # ...

    return {'message': 'Login successful'}

# Catch-all error handler
@app.exception_handler(Exception)
def handle_exceptions(request, exc):
    return {'error': str(exc)}