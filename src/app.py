import logging

import betterlogging as bl

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from src.routes import router
from config import config

app = FastAPI()
app.include_router(router)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
log = logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.app.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    message = first_error.get('msg', 'Validation error')
    return JSONResponse(
        status_code=422,
        content={"detail": message}
    )

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=config.app.port)