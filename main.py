from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
  name: str
  description: str | None = None
  price: float

itemList = []

@app.get("/")
def read_root():
  return {"status": "ok", "message": "Hello, world!"}

@app.get("/items")
def get_products():
  return {"status": "ok", "message": itemList}

@app.get("/items/{item_id}")
def get_product(item_id: int):
  if len(itemList) - 1 < item_id:
    raise HTTPException(status_code=404, detail="Item not found")
  return {"status": "ok", "message": itemList[item_id]}

@app.post("/items", status_code=201)
def post_products(item: Item):
  itemList.append(item)
  return {"status": "ok", "message": "Product created successfully with id: " + str(itemList.index(item))}

