from fastapi import FastAPI, Depends, HTTPException, Header
from dotenv import load_dotenv
import os
import ollama

app = FastAPI()
load_dotenv()

API_KEY_CREDITS= {os.getenv("SECRET_KEY"), 5}

def verify_api_key(x_api_key: str = Header(None)):
    credits = API_KEY_CREDITS.get(x_api_key, 0)
    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API Key, or no credits")

    return x_api_key

@app.get("/")
def read_root():
    return {"Hello World"}

@app.get("/generate")
def generate(prompt: str, x_api_key: str = Depends(verify_api_key)):
    API_KEY_CREDITS[x_api_key] -= 1
    response = ollama.chat(model="deepseek-r1", messages=[{"role": "user", "content": prompt}])
    return {"response": response["message"]["content"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)