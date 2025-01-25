import os
import dotenv
import pytest


# Загрузка переменных окружения из файла .env
@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture
def app_url():
    url = os.getenv("APP_URL")
    return url
