from fastapi import FastAPI

from app.routes.routers import breath_routes

app = FastAPI()

app.include_router(breath_routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

#TODO: провести миграцию