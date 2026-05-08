from fastapi import status, Body, APIRouter
from fastapi.responses import JSONResponse

breath_routes = APIRouter()


@breath_routes.get("/healthcheck/live", status_code=status.HTTP_200_OK)
async def healthcheck_live():
    return {"status": "ok"}

"""
TODO: реализовать после интеграции с внешними сервисами и утверждением модели данных
@breath_routes.get("/healthcheck/resources", status_code=status.HTTP_200_OK)
async def healthcheck_resources():
    try:
        pass
    except:
        return {"status": "error"}
    return {"status": "ok"}

@breath_routes.get("/healthcheck/integrations", status_code=status.HTTP_200_OK)
async def healthcheck_integrations():
    # TODO: реализовать после интеграции с внешними сервисами
    pass
    return {"status": "ok"}
"""

@breath_routes.post("/calculate/", status_code=status.HTTP_200_OK)
async def calculate():
    pass