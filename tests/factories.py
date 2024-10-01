import factory
import factory.fuzzy

from digital_library.models import Author, Book, User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class AuthorFactory(factory.Factory):
    class Meta:
        model = Author

    name = factory.Sequence(lambda n: f'test{n}')


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    title = factory.Sequence(lambda n: f'contos test{n}')
    year = factory.Sequence(lambda n: n)
    author_id = factory.SubFactory(AuthorFactory)
