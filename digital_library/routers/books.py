from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from digital_library.database import get_session
from digital_library.models import Author, Book, User
from digital_library.sanitize import sanitize
from digital_library.schemas import BookList, BookPatch, BookPublic, BookSchema
from digital_library.security import get_current_user

router = APIRouter(prefix='/books', tags=['books'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
def create_book(book: BookSchema, session: Session):
    db_book = session.scalar(select(Book).where(Book.title == book.title))
    db_author = session.scalar(
        select(Author).where(Author.id == book.author_id)
    )

    if not db_author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author does not exist in this library',
        )

    if not db_book:
        book = Book(
            title=sanitize(book.title), year=book.year, author_id=db_author.id
        )
        session.add(book)
        session.commit()
        session.refresh(book)

        return book

    raise HTTPException(
        status_code=HTTPStatus.CONFLICT,
        detail='Book is already included in the library!',
    )


@router.get('/{book_id}', response_model=BookPublic)
def get_book(
    book_id: int,
    session: Session,
):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not in the library',
        )

    return db_book


@router.get('/', response_model=BookList)
def list_books(  # noqa
    session: Session,
    title: str = Query(None),
    year: int = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Book)

    if title:
        query = query.filter(Book.title.contains(title))

    if year:
        query = query.filter(Book.year == year)

    books = session.scalars(query.offset(offset).limit(limit)).all()

    return {'books': books}


@router.patch('/{book_id}', response_model=BookPublic)
def patch_book(book_id: int, session: Session, book: BookPatch):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found.'
        )

    for key, value in book.model_dump(exclude_unset=True).items():
        if key == 'title':
            value = sanitize(value)  # noqa
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.delete('/{book_id}')
def delete_book(book_id: int, session: Session):
    book = session.scalar(select(Book).where(Book.id == book_id))

    if not book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found.'
        )

    session.delete(book)
    session.commit()

    return {'message': 'Book has been deleted successfully.'}
