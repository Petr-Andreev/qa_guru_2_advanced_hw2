from http import HTTPStatus
import pytest
import requests
from models.user import User  # Предполагаем, что модель User находится в models/user.py


# Тест пагинации с параметризацией
@pytest.mark.parametrize("page, size", [
    (1, 5),  # Первая страница, 5 пользователей на странице
    (2, 5),  # Вторая страница, 5 пользователей на странице
    (1, 10),  # Первая страница, 10 пользователей на странице
    (3, 4),  # Третья страница, 4 пользователя на странице
])
def test_users_with_pagination(app_url, page, size):
    url = f"{app_url}/api/users/"
    data = get_and_check_response(url, {"page": page, "size": size})

    # Проверка наличия ключей total и items
    assert 'total' in data
    assert 'items' in data

    # Проверка количества страниц
    if 'pages' in data:
        expected_pages = (data['total'] + size - 1) // size  # Округление вверх
        assert data['pages'] == expected_pages

    if data['total'] > 0:
        items = data['items']
        if page * size >= data['total']:
            expected_items_count = data['total'] - (page - 1) * size
        else:
            expected_items_count = size
        assert len(items) == expected_items_count

        for user in items:
            check_user_fields(user)

    # Проверка уникальности данных для разных страниц
    if page > 1:
        prev_data = get_and_check_response(url, {"page": page - 1, "size": size})
        prev_items = prev_data['items'] if 'items' in prev_data else []
        current_ids = {user['id'] for user in items}
        prev_ids = {user['id'] for user in prev_items}
        assert not current_ids.intersection(prev_ids)


# Вспомогательная функция для выполнения GET-запроса и проверки статуса
def get_and_check_response(url, params=None):
    response = requests.get(url, params=params)
    assert response.status_code == HTTPStatus.OK
    return response.json()


# Вспомогательная функция для проверки полей пользователя
def check_user_fields(user):
    assert 'id' in user
    assert 'email' in user
    assert 'first_name' in user
    assert 'last_name' in user
    assert 'avatar' in user


# Дополнительный тест для проверки количества страниц
def test_total_pages(app_url):
    url = f"{app_url}/api/users/"
    data = get_and_check_response(url)
    total = data['total']

    for size in [5, 10, 20]:
        expected_pages = (total + size - 1) // size  # Округление вверх
        data = get_and_check_response(url, {"size": size})
        if 'pages' in data:
            assert data['pages'] == expected_pages


def test_users_no_duplicates(app_url):
    url = f"{app_url}/api/users/"
    response = requests.get(url)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    users_list = data['items'] if 'items' in data else []
    users_ids = [user["id"] for user in users_list]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_user(app_url, user_id):
    url = f"{app_url}/api/users/{user_id}"
    data = get_and_check_response(url)
    User(**data)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(app_url, user_id):
    url = f"{app_url}/api/users/{user_id}"
    response = requests.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(app_url, user_id):
    url = f"{app_url}/api/users/{user_id}"
    response = requests.get(url)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
