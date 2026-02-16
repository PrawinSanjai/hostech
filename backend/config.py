from fastapi.security import OAuth2PasswordBearer

from services.utils import get_env


class Configuration:
    DATABASE_URL = get_env("DATABASE_URL", default="")
    SECRET_KEY = get_env("SECRET_KEY", default=None)
    HOSTECH_API_KEY = get_env("HOSTECH_API_KEY", default='None')


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')