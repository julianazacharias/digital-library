from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from digital_library.database import get_session
from digital_library.models import Author, User
from digital_library.sanitize import sanitize
from digital_library.schemas import AuthorList, AuthorPublic, AuthorSchema
from digital_library.security import get_current_user

router = APIRouter(prefix='/authors', tags=['authors'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AuthorPublic)
def create_author(author: AuthorSchema, session: Session):
    db_author = session.scalar(
        select(Author).where(Author.name == author.name)
    )

    if not db_author:
        author = Author(
            name=sanitize(author.name),
        )
        session.add(author)
        session.commit()
        session.refresh(author)

        return author

    raise HTTPException(
        status_code=HTTPStatus.CONFLICT,
        detail='Author is already included in the library!',
    )


@router.get('/{author_id}', response_model=AuthorPublic)
def get_author(
    author_id: int,
    session: Session,
):
    db_author = session.scalar(select(Author).where(Author.id == author_id))

    if not db_author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author not in the library',
        )

    return db_author


@router.get('/', response_model=AuthorList)
def list_authors(
    session: Session,
    name: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Author)

    if name:
        query = query.filter(Author.name.contains(name))

    authors = session.scalars(query.offset(offset).limit(limit)).all()

    return {'authors': authors}


@router.patch('/{author_id}', response_model=AuthorPublic)
def patch_author(author_id: int, session: Session, author: AuthorSchema):
    db_author = session.scalar(select(Author).where(Author.id == author_id))

    if not db_author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author not found in the library.',
        )

    for key, value in author.model_dump(exclude_unset=True).items():
        if key == 'name':
            value = sanitize(value)  # noqa
        setattr(db_author, key, value)

    session.add(db_author)
    session.commit()
    session.refresh(db_author)

    return db_author


@router.delete('/{author_id}')
def delete_author(
    author_id: int,
    session: Session,
):
    author = session.scalar(select(Author).where(Author.id == author_id))

    if not author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author not found in the library.',
        )

    session.delete(author)
    session.commit()

    return {'message': 'Author has been deleted successfully.'}
