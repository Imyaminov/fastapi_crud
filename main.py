from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.settings import settings
from app.routers import post, auth

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router, tags=['Post'], prefix='/api/post')
app.include_router(auth.router, tags=['Auth'], prefix='/api/user')

