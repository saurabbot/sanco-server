from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate_user(self, email: str, password: str):
        if email == "admin@sanco.com" and password == "password":
            return True
        return False
