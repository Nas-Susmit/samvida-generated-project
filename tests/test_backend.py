import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from backend.main import app
from backend.database import Base, get_db
from backend.models import Item # Import Item model directly for test setup/teardown

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create an engine for the test database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool, # Required for in-memory SQLite with multiple connections
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="session")
def session_fixture():
    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test to ensure a clean slate
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
async def client_fixture(session: Session):
    # Override the get_db dependency to use the test session
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    
    # Use AsyncClient for making HTTP requests to the FastAPI app
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    # Clear dependency overrides after the test
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_read_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI Item Manager API!"}

@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    response = await client.post(
        "/items/",
        json={"name": "Test Item", "description": "This is a test item."}, # description is optional
    )
    assert response.status_code == 201 # HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item."
    assert data["is_completed"] is False
    assert "id" in data

@pytest.mark.asyncio
async def test_read_items_empty(client: AsyncClient):
    response = await client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_read_items(client: AsyncClient, session: Session):
    # Add items directly to the session for testing listing functionality
    item1 = Item(name="Item 1", description="Desc 1", is_completed=False)
    item2 = Item(name="Item 2", description="Desc 2", is_completed=True)
    session.add_all([item1, item2])
    session.commit()
    session.refresh(item1)
    session.refresh(item2)

    response = await client.get("/items/")
    assert response.status_code == 200
    items_data = response.json()
    assert len(items_data) == 2
    assert any(item["name"] == "Item 1" and item["is_completed"] is False for item in items_data)
    assert any(item["name"] == "Item 2" and item["is_completed"] is True for item in items_data)

@pytest.mark.asyncio
async def test_read_single_item(client: AsyncClient, session: Session):
    item = Item(name="Single Item", description="Unique item", is_completed=False)
    session.add(item)
    session.commit()
    session.refresh(item)

    response = await client.get(f"/items/{item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Single Item"
    assert data["description"] == "Unique item"
    assert data["id"] == item.id

@pytest.mark.asyncio
async def test_read_single_item_not_found(client: AsyncClient):
    response = await client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

@pytest.mark.asyncio
async def test_update_item(client: AsyncClient, session: Session):
    item = Item(name="Old Name", description="Old Desc", is_completed=False)
    session.add(item)
    session.commit()
    session.refresh(item)

    response = await client.put(
        f"/items/{item.id}",
        json={
            "name": "New Name", 
            "description": "New Desc updated", 
            "is_completed": True
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item.id
    assert data["name"] == "New Name"
    assert data["description"] == "New Desc updated"
    assert data["is_completed"] is True

    # Verify the update in the database
    updated_item = session.query(Item).filter(Item.id == item.id).first()
    assert updated_item.name == "New Name"
    assert updated_item.description == "New Desc updated"
    assert updated_item.is_completed is True

@pytest.mark.asyncio
async def test_update_item_not_found(client: AsyncClient):
    response = await client.put(
        "/items/999",
        json={
            "name": "Non Existent", 
            "description": "Foo", 
            "is_completed": False
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient, session: Session):
    item = Item(name="To Delete", description="Delete me", is_completed=False)
    session.add(item)
    session.commit()
    session.refresh(item)

    response = await client.delete(f"/items/{item.id}")
    assert response.status_code == 204 # HTTP_204_NO_CONTENT

    # Verify the item is deleted from the database
    deleted_item = session.query(Item).filter(Item.id == item.id).first()
    assert deleted_item is None

@pytest.mark.asyncio
async def test_delete_item_not_found(client: AsyncClient):
    response = await client.delete("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
