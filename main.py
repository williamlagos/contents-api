from odmantic import AIOEngine, Model, ObjectId
from fastapi import FastAPI, HTTPException
from typing import List

class Content(Model):
    title: str
    content: str

app = FastAPI()

engine = AIOEngine()

@app.get("/")
async def root():
    return { "health": "OK" }

@app.put("/contents/", response_model=Content)
async def create_content(content: Content):
    await engine.save(content)
    return content


@app.get("/contents/", response_model=List[Content])
async def get_contents():
    contents = await engine.find(Content)
    return contents


@app.get("/contents/count", response_model=int)
async def count_contents():
    count = await engine.count(Content)
    return count


@app.get("/contents/{id}", response_model=Content)
async def get_content_by_id(id: ObjectId):
    content = await engine.find_one(Content, Content.id == id)
    if content is None:
        raise HTTPException(404)
    return content