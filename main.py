import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException, MissingTokenError
from starlette.responses import JSONResponse

from src.routes import contacts, channels, contacts_channels, auth
from src.schemas import Settings

app = FastAPI()

app.include_router(contacts.router, prefix='/api')
app.include_router(channels.router, prefix='/api')
app.include_router(contacts_channels.router, prefix='/api')
app.include_router(auth.router, prefix='/api')


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=401,
        content={"message": f"Invalid user authorization credentials or token is "
                            f"expired"},
    )


@app.exception_handler(MissingTokenError)
async def missing_token_exception_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=401,
        content={"message": "Authorization token wasn't sent"},
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
