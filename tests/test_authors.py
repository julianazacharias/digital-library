from http import HTTPStatus


def test_create_author(client, token):
    response = client.post(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Test Author',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'test author',
    }


def test_create_duplicate_author(client, author, token):
    response = client.post(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': author.name,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Author is already included in the library!'
    }


def test_delete_author(client, author, token):
    response = client.delete(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Author has been deleted successfully.'
    }


def test_delete_author_error(client, token):
    response = client.delete(
        f'/authors/{10}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in the library.'}


def test_patch_author(client, author, token):
    response = client.patch(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Changed'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'test changed'


def test_patch_author_error(client, token):
    response = client.patch(
        f'/authors/{10}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test!'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in the library.'}


def test_get_author_by_id(client, author):
    response = client.get(
        f'/authors/{author.id}',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'name': 'test3'}


def test_get_author_by_id_error(client):
    response = client.get(f'/authors/{9999}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not in the library'}
