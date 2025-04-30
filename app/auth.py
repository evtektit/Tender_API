from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

class Settings(BaseModel):
    authjwt_secret_key: str = "supersecretkey"

@AuthJWT.load_config
def get_config():
    return Settings()

def require_auth(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except AuthJWTException as e:
        raise HTTPException(status_code=401, detail="Unauthorized")