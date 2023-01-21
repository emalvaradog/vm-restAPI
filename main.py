from fastapi import FastAPI, HTTPException, UploadFile, File
from pydub import AudioSegment
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from os import path

app = FastAPI()

origins = [
  "http://localhost:5173"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

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

@app.post("/files")
def post_files(file: UploadFile = File(...)):
  if (file.filename.find(".wav") == -1):
    output_file = AudioSegment.from_mp3(file.file)
    output_file.export(f"{file.filename}.wav", format="wav")
  return {"status": "ok", "body": file.filename}
