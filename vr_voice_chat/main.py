from chat import LangChainChat
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Query

app = FastAPI()

# CORS設定
origins = [
    "*"
]

@app.get("/")
async def root():
  return {"greeting": "Hello World!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat = LangChainChat()

@app.post("/api/v1/chat")
async def create_reply(query: Query):
    reply = chat.conversation(query.text)
    return {"response": reply["response"]}

def main():
    chat = LangChainChat()
    while True:
        command = input("You：")
        if command == "exit":
            sys.exit()
        output = chat.conversation(command)
        print("AI：", output["response"])

if __name__ == "__main__":
    main() 