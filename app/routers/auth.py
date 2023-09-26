from datetime import timedelta
from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from .. import schemas, models, utils
from sqlalchemy.orm import Session
from app.oauth2 import AuthJWT
from ...core.settings import settings
from ...core.database import get_db


router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=schemas.AuthorResponse)
async def create_user(payload: schemas.CreateAuthorSchema, db: Session = Depends(get_db)):
    # Check if user already exist
    user = db.query(models.Author).filter(
        models.Author.username == payload.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Account already exist')

    # Compare password and passwordConfirm
    if payload.password != payload.passwordConfirm:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')

    #  Hash the password
    payload.password = utils.hash_password(payload.password)
    del payload.passwordConfirm
    payload.verified = True
    payload.username = payload.username
    new_author = models.Author(**payload.dict())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@router.post('/login')
def login(payload: schemas.LoginAuthorSchema, response: Response, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = db.query(models.Author).filter(models.Author.username == payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect Email or Password')
    if not user.verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your email address')
    if not utils.verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect Email or Password')

    access_token = Authorize.create_access_token(subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    refresh_token = Authorize.create_refresh_token(subject=str(user.id), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60, ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token, REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60, ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    return {'success': True, 'result': {'access_token': access_token, 'refresh_token': refresh_token}}


@router.get('/refresh')
def refresh_token(response: Response, request: Request, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()
        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not refresh access token')
        user = db.query(models.Author).filter(models.Author.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='The user belonging to this token no logger exist')
        access_token = Authorize.create_access_token(subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60, ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'new_access_token': access_token}


@router.get('/logout')
def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()

    return {'success': True, 'message': 'User successfully logged out!'}



