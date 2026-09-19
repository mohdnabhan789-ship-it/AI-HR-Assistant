from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agent import ask_ai


# Create FastAPI application
app = FastAPI()


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the format of chat requests
class ChatRequest(BaseModel):
    employee_id: str
    message: str


# Home route
@app.get("/")
def home():
    return {
        "message": "AI HR Assistant is running!"
    }


# Health check route
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# Chat route
@app.post("/chat")
def chat(request: ChatRequest):

    answer = ask_ai(
        request.message,
        request.employee_id
    )

    return {
        "response": answer
    }