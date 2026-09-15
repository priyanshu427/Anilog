from fastapi import FastAPI

app = FastAPI()

@app.get("/")
@app.get("/home") 
async def home():
    return "hello"

@app.get("/anime/{anime_id}")
async def get_anime(anime_id :int):
    return [{1:"haikyuu"},{2:"tomodachi game"}]