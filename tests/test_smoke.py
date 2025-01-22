from http import HTTPStatus
import pytest
import requests
from models.app_status import AppStatus  # Предполагаем, что модель AppStatus находится в models.user


@pytest.fixture
def users_list(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    return data['items'] if 'items' in data else []


# Вспомогательная функция для выполнения GET-запроса и проверки статуса
def get_and_check_response(url, params=None):
    response = requests.get(url, params=params)
    assert response.status_code == HTTPStatus.OK
    return response.json()


# Smoke тест для эндпоинта /status
def test_status_endpoint(app_url, users_list):
    url = f"{app_url}/status"
    response = requests.get(url)
    assert response.status_code == HTTPStatus.OK

    # Проверка, что ответ соответствует модели AppStatus
    data = response.json()
    try:
        status = AppStatus(**data)
    except Exception as e:
        pytest.fail(f"Failed to validate response against AppStatus model: {e}")

    # Проверка значений полей в ответе
    if len(users_list) > 0:
        assert status.users is True
    else:
        assert status.users is False


# Дополнительные smoke тесты
def test_status_response_structure(app_url):
    url = f"{app_url}/status"
    response = requests.get(url)
    assert response.status_code == HTTPStatus.OK

    # Проверка наличия ключей в ответе
    data = response.json()
    assert 'users' in data


def test_status_invalid_methods(app_url):
    url = f"{app_url}/status"

    # Проверка метода POST
    response = requests.post(url)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    # Проверка метода PUT
    response = requests.put(url)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    # Проверка метода DELETE
    response = requests.delete(url)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    # Проверка метода PATCH
    response = requests.patch(url)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
