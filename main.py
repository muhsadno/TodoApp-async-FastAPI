from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from api import todo

app = FastAPI(title="TodoApp", version="1.0.0", swagger_ui_parameters={"defaultModelsExpandDepth": -1})

origins = [
    "http://localhost:8000",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo.router, prefix="/api", tags=["Todos"])

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)