from envparse import Env
from pathlib import Path


ROOT_DIR = Path(".").absolute()
APP_DIR = ROOT_DIR / 'app'

env = Env()
env.read_envfile(ROOT_DIR / ".env")

DEBUG = env.bool("DEBUG", default=True)

DB_HOST = env.str("DB_HOST", default="localhost")
DB_NAME = env.str("DB_NAME", default="todo")
DB_USERNAME = env.str("DB_USERNAME", default="postgres")
DB_PASSWORD = env.str("DB_PASSWORD", default="postgres")
DB_PORT = env.int("DB_PORT", default=5432)

SECRET_KEY = env.str("SECRET_KEY")
ALGORITHM = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)

DATABASE_URL = env.str(
    "DB_URL",
    default=f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
