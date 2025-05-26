from fastapi import FastAPI

from api.routers import task, done

app = FastAPI()
# ルーターを登録（APIの入り口）
app.include_router(task.router)
app.include_router(done.router)


# オマケの /hello エンドポイントも追加してOK
@app.get("/hello")
async def hello():
    return {"message": "hello world!"}