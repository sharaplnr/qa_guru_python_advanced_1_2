from http import HTTPStatus

import pytest
import requests
from models.User import User, UserPagination


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()["items"]


def test_users_validate(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK

    UserPagination.model_validate(response.json())


def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_user(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK

    user = response.json()
    User.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

@pytest.mark.parametrize("page, size", [(1, 3), (2, 5), (2, 11), (3, 5), (1, 13)])
def test_count_users_in_page(app_url, page, size):
    response = requests.get(f"{app_url}/api/users/?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK
    json_data = response.json()
    total = json_data["total"]
    actual_count_users = len(json_data.get("items"))
    expected_count_users = total - (page - 1) * size if page * size >= total else size
    assert actual_count_users == expected_count_users

@pytest.mark.parametrize("page, size", [(2, 2), (1, 5), (1, 12)])
def test_count_pages(app_url, page, size):
    response = requests.get(f"{app_url}/api/users/?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK

    json_data = response.json()

    total = json_data["total"]
    actual_pages = json_data.get("pages")

    expected_pages_count = (total + size - 1) // size

    assert actual_pages == expected_pages_count

@pytest.mark.parametrize("page1, page2, size", [(1, 2, 3)])
def test_different_users_info_on_pages(app_url, page1, page2, size):
    first_page = requests.get(f"{app_url}/api/users/?page={page1}&size={size}")
    assert first_page.status_code == HTTPStatus.OK

    second_page = requests.get(f"{app_url}/api/users/?page={page2}&size={size}")
    assert second_page.status_code == HTTPStatus.OK

    user_info_1 = first_page.json().get("items")
    user_info_2 = second_page.json().get("items")

    # Извлечение id пользователей
    ids_first_page = {user['id'] for user in user_info_1}
    ids_second_page = {user['id'] for user in user_info_2}

    assert ids_first_page.isdisjoint(ids_second_page)
