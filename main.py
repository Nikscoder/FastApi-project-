from fastapi import FastAPI, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[str] = None
    brand: Optional[str] = None


inventory = {}


@app.get("/get-item/{item_id}")
def get_item(item_id: int):
    if item_id not in inventory:
        return {"ERROR": "ID does not exist in inventory"}
    return inventory[item_id]

#GET request
@app.get("/get-by-name/{item_id}")
def get_by_name(*, item_id: int, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")


# POST = update request
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item ID already exists")

    inventory[item_id] = item
    return inventory[item_id]


# put=update request
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item with mentioned ID not found")

    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]


#Delete request
@app.delete("/delete-item")
def delete_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item cannot be deleted, Item not found")

    del inventory[item_id]
    return {"SUCCESS": "Item deleted"}

@app.get("/")
def home():
    return {"Data": "Testing"}


@app.get("/about")
def about():
    return {"Data": "About"}


@app.get("/all_invent")
def all_invent():
    return inventory

# unicorn is a webserver for fast api

# http://127.0.0.1:8000/docs#/
#& "C:\Users\Nikita\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\uvicorn.exe" main:app --reload
