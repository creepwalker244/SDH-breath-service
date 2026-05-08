from fastapi import FastAPI

from app.routes.routers import breath_routes

app = FastAPI()

app.include_router(breath_routes)

#TODO: создать бд в облачном инстансе
#TODO: провериь целостность моделей
#TODO: проверить работу АПИ
#TODO: накидать функцию коэфециена сжатия
#TODO: провести миграцию