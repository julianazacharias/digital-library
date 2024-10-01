from sqlalchemy import select

from digital_library.models import Author, Book, User


def test_create_user(session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'


def test_create_author(session):
    author = Author(
        name='Test Name',
    )

    session.add(author)
    session.commit()

    author = session.scalar(select(Author).where(Author.name == 'Test Name'))

    assert author.id == 1


def test_create_book(session, author: Author):
    book = Book(title='Test title', year=1000, author_id=author.id)

    session.add(book)
    session.commit()
    session.refresh(book)

    author = session.scalar(select(Author).where(Author.id == author.id))
