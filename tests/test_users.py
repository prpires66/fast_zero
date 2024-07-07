from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'newusername',
            'email': 'newteste@email.com',
            'password': 'newsenha123',
        },
    )

    # Voltou o status code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic
    assert response.json() == {
        'username': 'newusername',
        'email': 'newteste@email.com',
        'id': 2,
    }


def test_create_user_username_allready_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'testeusername',
            'email': 'someemail@email.com',
            'password': 'senha123',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Username already exists'


def test_create_user_username_allready_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'someusername',
            'email': 'teste@email.com',
            'password': 'senhateste123',
        },
    )

    # Voltou o status code correto?
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Email already exists'


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_by_id(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testeusername',
        'email': 'teste@email.com',
        'id': 1,
    }


def test_read_user_by_id_not_found(client, user):
    response = client.get('/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': '123',
            'username': 'testusername2',
            'email': 'test@test.com',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testusername2',
        'email': 'test@test.com',
        'id': user.id,
    }


def test_update_wrong_user(client, user, token):
    response = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': '123',
            'username': 'testusername2',
            'email': 'test@test.com',
            'id': -1,
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.json() == {'message': 'User deleted'}


def test_delete_wrong_user(client, user, token):
    response = client.delete(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}
