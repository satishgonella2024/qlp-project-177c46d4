import os
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_version():
    response = client.get('/version')
    assert response.status_code == 200
    assert response.json() == {'version': '1.0.0'}

def test_register_success():
    response = client.post('/register', json={'username': 'test', 'password': 'test123'})
    assert response.status_code == 200
    assert response.json() == {'message': 'User registered successfully'}

def test_register_validation():
    response = client.post('/register', json={'username': '', 'password': ''})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Username and password are required'}

def test_login_success(monkeypatch):
    monkeypatch.setenv('ADMIN_USER', 'admin')
    monkeypatch.setenv('ADMIN_PASSWORD', 'admin123')
    response = client.post('/login', auth=('admin', 'admin123'))
    assert response.status_code == 200
    assert response.json() == {'message': 'Login successful'}

def test_login_failure(monkeypatch):
    monkeypatch.setenv('ADMIN_USER', 'admin')
    monkeypatch.setenv('ADMIN_PASSWORD', 'admin123')
    response = client.post('/login', auth=('admin', 'wrongpassword'))
    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid credentials'}