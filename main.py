from fastapi import FastAPI, Path
from typing import Union
from pydantic import BaseModel, Field

warehouse_api = FastAPI()

class Item(BaseModel):
    name: str
    price: int
    quantity: int
    brand: Union[str, None] = None

    #class Config:
        #schema_extra = {
            #"example" : {
                #"name": "Apple",
                #"price": 20,
                #"quantity": 5,
                #"brand": "Chiquita"
            #}
        #}



class UserIn(BaseModel):
    username: str = Field(description="The username that is doing the request", max_length=20)
    user_email: str = Field(description="The email of the user who is doing the reqest")
    _password: str = Field(description="Password of the user who is doing the request")
    _json_token: str = Field(description="The authorization token of the user doing the request")

    class Config: #Config from Pydantic has function/setter than can make private attributes hidden in output (prepended by _)
        underscore_attrs_are_private = True


class UpdateItem(BaseModel):
    name: Union[str, None] = None
    price: Union[int, None] = None
    quantity: Union[int, None] = None
    brand: Union[str, None] = None


@warehouse_api.get("/")
def home():
    return {"message": "This is the home page"}



inventory_db = {}

@warehouse_api.get("/items/inventory/")
def get_items():
    return inventory_db

@warehouse_api.get("/items/{item_id}")
def get_specific_item(item_id: int = Path(description="Provide the item ID", ge=0)):
    return inventory_db[item_id]


@warehouse_api.get("/items/item_name/")
def search_by_name(name: str):
    for item in inventory_db:
        if inventory_db[item].name == name:
            return inventory_db[item]
        else:
            return {"message": "no item by that name in inventory"}


@warehouse_api.post("/items/add/{item_id}")
def add_item(item: Item, item_id: int, user: UserIn):
    inventory_db[item_id] = item

    return {"added_item": item, "by_user": user}
    

@warehouse_api.put("/items/update/{item_id}")
def update_item(item_id: int, item: UpdateItem):

    if item.name != None:
        inventory_db[item_id].name = item.name
    
    if item.price != None:
        inventory_db[item_id].price = item.price

    if item.quantity != None:
        inventory_db[item_id].quantity = item.quantity

    if item.brand != None:
        inventory_db[item_id].brand = item.brand

    return inventory_db




