from http import HTTPStatus


def test_create_book(client, token, author):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 2024,
            'title': 'New Book',
            'author_id': author.id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'year': 2024,
        'title': 'new book',
        'author_id': 1,
    }


def test_create_book_author_doesnt_exist(client, token):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 2024, 'title': 'New Book', 'author_id': 999},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'Author does not exist in this library'
    }


def test_delete_book(client, book, token):
    response = client.delete(
        f'/books/{book.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Book has been deleted successfully.'
    }


def test_delete_book_error(client, token):
    response = client.delete(
        f'/books/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found.'}


def test_get_book_by_id(client, book):
    response = client.get(f'/books/{book.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'title': 'fake title',
        'year': 2024,
        'author_id': 1,
    }


def test_get_book_by_id_error(client):
    response = client.get(f'/books/{999}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not in the library'}


def test_patch_book(client, book, token):
    response = client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Teste Titulo', 'year': 2000},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'title': 'teste titulo',
        'year': 2000,
        'author_id': 1,
    }


def test_patch_book_error(client, token):
    response = client.patch(
        f'/books/{10}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Teste Change', 'year': 2000},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found.'}
