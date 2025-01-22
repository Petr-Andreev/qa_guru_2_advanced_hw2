import os
import dotenv
import pytest


# Загрузка переменных окружения из файла .env
@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


# Фикстура для получения app_url с областью видимости session
@pytest.fixture
def app_url():
    url = os.getenv("APP_URL")
    if not url:
        pytest.fail("Environment variable APP_URL is not set.")
    return url
