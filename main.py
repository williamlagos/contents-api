"""
This module provides a FastAPI application for managing content items.

It defines a `Content` model using ODMantic, a MongoDB ODM for Python, and 
provides various endpoints to create, retrieve, update, and delete content items.

Endpoints:
- GET /: Health check endpoint.
- PUT /contents/: Create a new content item.
- GET /contents/: Retrieve all content items.
- GET /contents/count: Count the number of content items.
- GET /contents/{id}: Retrieve a content item by its ID.
- PATCH /contents/{id}: Update a content item by its ID.
- DELETE /contents/{id}: Delete a content item by its ID.

Additionally, it includes a test client and a test case for the root endpoint.
"""

from typing import List, Optional
from datetime import datetime
from odmantic import AIOEngine, Model, ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient


class Content(Model):
    """Model representing a content item."""
    title: str
    content: str
    author: str
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None


app = FastAPI()

engine = AIOEngine()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"health": "OK"}


@app.put("/contents/", response_model=Content)
async def create_content(content: Content):
    """Create a new content item."""
    await engine.save(content)
    return content


@app.get("/contents/", response_model=List[Content])
async def get_contents():
    """Retrieve all content items."""
    contents = await engine.find(Content)
    return contents


@app.get("/contents/count", response_model=int)
async def count_contents():
    """Count the number of content items."""
    count = await engine.count(Content)
    return count


@app.get("/contents/{id}", response_model=Content)
async def get_content_by_id(content_id: ObjectId):
    """Retrieve a content item by its ID."""
    content = await engine.find_one(Content, Content.id == content_id)
    if content is None:
        raise HTTPException(404)
    return content


@app.patch("/contents/{id}", response_model=Content)
async def update_content(content_id: ObjectId, content_data: Content):
    """Update a content item by its ID."""
    content = await engine.find_one(Content, Content.id == content_id)
    if content is None:
        raise HTTPException(404)
    content_data.updated_at = datetime.utcnow()
    await engine.save(content_data)
    return content_data


@app.delete("/contents/{id}", response_model=dict)
async def delete_content(content_id: ObjectId):
    """Delete a content item by its ID."""
    content = await engine.find_one(Content, Content.id == content_id)
    if content is None:
        raise HTTPException(404)
    await engine.delete(content)
    return {"message": "Content deleted successfully"}

client = TestClient(app)


def test_read_main():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health": "OK"}
