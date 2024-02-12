from fastapi import FastAPI

from api.routes import post, user


app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
