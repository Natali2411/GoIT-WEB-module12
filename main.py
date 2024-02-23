from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.responses import JSONResponse

from src.routes import contacts, channels, contacts_channels, auth

app = FastAPI()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(contacts.router, prefix='/api')
app.include_router(channels.router, prefix='/api')
app.include_router(contacts_channels.router, prefix='/api')
app.include_router(auth.router, prefix='/api')

#
# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}

