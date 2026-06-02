# routes/auth_routes.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from database import get_session
from controllers.auth_controller import AuthController
from schemas.auth_schema import TokenPair, RefreshRequest, User
from security import get_current_active_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/token", response_model=TokenPair)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """Login. Retorna access_token (30 min) + refresh_token (7 dias)."""
    return AuthController.login(session, form_data.username, form_data.password)

@router.post("/refresh", response_model=TokenPair)
async def refresh(body: RefreshRequest):
    """Renova o access_token silenciosamente usando o refresh_token."""
    return AuthController.refresh(body.refresh_token)

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
):
    return current_user

