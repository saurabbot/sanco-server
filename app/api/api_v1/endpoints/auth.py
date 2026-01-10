from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import create_access_token
from fastapi.responses import JSONResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login")
async def login(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return JSONResponse(
                status_code=400, content={"message": "Email and password are required"}
            )
        auth_service = AuthService(db)
        is_authenticated = await auth_service.authenticate_user(email, password)
        if not is_authenticated:
            return JSONResponse(
                status_code=400, content={"message": "Invalid email or password"}
            )
        # create a session toke and set it in the response cookie
        session_token = create_access_token(email)
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        return JSONResponse(
            status_code=200, content={"message": "Login successful", "user": email}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error", "error": str(e)},
        )
