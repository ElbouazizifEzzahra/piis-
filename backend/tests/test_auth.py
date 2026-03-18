import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Adjust these imports based on where  FastAPI 'app' instance is defined
from app.main import app 
from app.core.database import get_session

# 1. Setup an In-Memory SQLite Database for testing
sqlite_url = "sqlite://"
engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

# 2. Pytest Fixtures to reset the database and client for every test
@pytest.fixture(name="session")
def session_fixture():
    # Create tables in the in-memory database
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Drop tables after the test finishes to ensure a clean slate
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    # Override the database dependency to use our test database
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# --- THE UNIT TESTS ---

def test_register_user_success(client: TestClient):
    """Test standard registration with a CIN."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "cin": "AB123456",
            "tel": "0612345678",
            "email": "zakaria@vpp-advisory.ma",
            "full_name": "Zakaria",
            "password": "strongpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register_duplicate_cin(client: TestClient):
    """Test that the system rejects a duplicate CIN."""
    # First registration
    user_data = {
        "cin": "EE987654",
        "full_name": "Zakaria",
        "password": "testpassword"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Second registration with the exact same CIN
    response = client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "A user with this CIN is already registered"

def test_login_with_cin_success(client: TestClient):
    """Test the Auth v2.3 logic using CIN as the identifier."""
    # 1. Create the user
    client.post(
        "/api/v1/auth/register",
        json={
            "cin": "CD112233",
            "full_name": "Zakaria",
            "password": "mysecretpassword"
        }
    )
    
    # 2. Attempt login using CIN
    response = client.post(
        "/api/v1/auth/login",
        json={
            "identifier": "CD112233",
            "password": "mysecretpassword"
        }
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_with_tel_success(client: TestClient):
    """Test the Auth v2.3 logic using Telephone as the identifier."""
    client.post(
        "/api/v1/auth/register",
        json={
            "cin": "ZT998877",
            "tel": "0600000000",
            "full_name": "Zakaria",
            "password": "securepass"
        }
    )
    
    # Attempt login using the phone number instead of CIN
    response = client.post(
        "/api/v1/auth/login",
        json={
            "identifier": "0600000000",
            "password": "securepass"
        }
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client: TestClient):
    """Test that invalid credentials get rejected safely."""
    client.post(
        "/api/v1/auth/register",
        json={
            "cin": "BK445566",
            "full_name": "Zakaria",
            "password": "correctpassword"
        }
    )
    
    response = client.post(
        "/api/v1/auth/login",
        json={
            "identifier": "BK445566",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect CIN/TEL or password"