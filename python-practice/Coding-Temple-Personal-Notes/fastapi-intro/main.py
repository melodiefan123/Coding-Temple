from fastapi import FastAPI
from pydantic import BaseModel



# Create a FastAPI instance
app = FastAPI()


# Define a GET endpoint at the root path "/"
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Define a GET endpoint with a path parameter
@app.get("/greet/{name}")
def greet_user(name: str):
    return {"message": f"Hello, {name}! Welcome to FastAPI."}


# Define what valid data looks like
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True  # Optional with default value

@app.post("/items")
def create_item(item: Item):
    return {
        "message": f"Created item: {item.name}",
        "item": item.model_dump()  # Convert Pydantic model to dict
    }