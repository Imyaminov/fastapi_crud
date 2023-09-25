from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.orm import Session
from models import Post
from core.database import get_db
from schemas import PostSchema

router = APIRouter()


@router.get('/all', response_model=PostSchema)
def get_post_list(db: Session=Depends(get_db)):
    posts = db.query(Post).group_by(Post.id).all()
    return {'success': True, 'result': posts}


@router.get('detail/{id}', response_model=PostSchema)
def get_post_list(id: str, db: Session=Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id-'{id}' is not found")
    return {'success': True, 'result': post}


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=PostSchema)
def create_post(post: PostSchema, db: Session = Depends(get_db)):
    new_post = Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put('/update/{id}', response_model=PostSchema)
def update_post(id: str, post: PostSchema, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id==id)
    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id-"{id}" is not found')

    post_query.update(post.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_post


@router.put('/delete/{id}', response_model=PostSchema)
def delete_post(id: str, post: PostSchema, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id-"{id}" is not found')

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

