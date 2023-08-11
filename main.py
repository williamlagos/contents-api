from odmantic import Model
from fastapi import FastAPI

app = FastAPI()

class Page(Model):
    title: str
    content: str

@app.get("/")
async def root():
    return { "message": "Hello World" }