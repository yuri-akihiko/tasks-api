from datetime import timedelta
from sqlmodel import Session
from services.auth_services import (
    AuthServices,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from schemas.auth_schema import TokenPair

class AuthController:
    @staticmethod
    def login(session: Session, username: str, password: str) -> TokenPair:
        user = AuthServices.authenticate_user(session, username, password)
        access_token = AuthServices.create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = AuthServices.create_refresh_token(user.username)
        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def refresh(refresh_token: str) -> TokenPair:
        username = AuthServices.decode_refresh_token(refresh_token)
        access_token = AuthServices.create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        new_refresh = AuthServices.create_refresh_token(username)
        return TokenPair(access_token=access_token, refresh_token=new_refresh)
