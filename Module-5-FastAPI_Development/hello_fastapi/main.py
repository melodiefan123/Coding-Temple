from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# GET /
@app.get("/")
def read_root():
    return {"message": "Welcome to my first API"}

# GET /about
@app.get("/about")
def about_me():
    return {
        "name": "Your Name",
        "module": "Module 5 - FastAPI Practice",
        "fun_fact": "I love coding and learning new technologies!"
    }

# GET /greet/{name}
@app.get("/greet/{name}")
def greet_user(name: str):
    return {"message": f"Hello, {name}! Welcome to FastAPI."}

# POST /echo 
class EchoRequest(BaseModel):
    message: str
    shout: bool = False

@app.post("/echo")  
def echo_message(request: EchoRequest):
    if request.shout:
        return {"echo": request.message.upper()}
    return {"echo": request.message}