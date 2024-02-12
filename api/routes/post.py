from datetime import datetime
import random

from fastapi import APIRouter, Depends
from typing import Annotated

from api.validation_schemas.post import PostCreateQueryParamsSchema
from api.controllers.post_controller import PostController
from api.utils import make_response_async
from api.dependencies import get_user

from logger import log_func_async

router = APIRouter(
    prefix="/post",
    tags=["post"],
)


@router.post("/")
@log_func_async
@make_response_async
async def create(query: PostCreateQueryParamsSchema, user_id: Annotated[int, Depends(get_user)]) -> None:
    content: str = query.content
    post_data = {
        "user_id": user_id,
        "created_at": datetime.now(),
        "content": content,
    }
    PostController.validate_user_post_schema(post_data)
    PostController.create_new_user_post(post_data)


@router.put("/like")
@log_func_async
@make_response_async
async def like_post(user_id: Annotated[int, Depends(get_user)]) -> None:
    posts = PostController.get_posts()
    while True:
        n = random.randrange(0, len(posts))
        user_post = posts[n]
        post_data = {
            "user_id": user_id,
            "post_id": int(user_post.id),
            "created_at": datetime.now().date(),
        }
        PostController.validate_like_post_schema(post_data)
        is_liked: bool = PostController.check_if_post_already_liked_by_user(user_id, int(user_post.id))
        if not is_liked:
            PostController.like_post(post_data)
            break


@router.put("/dislike")
@log_func_async
@make_response_async
async def dislike_post(user_id: Annotated[int, Depends(get_user)]) -> None:
    posts = PostController.get_posts()
    while True:
        n = random.randrange(0, len(posts))
        user_post = posts[n]
        is_liked = PostController.check_if_post_already_liked_by_user(user_id, int(user_post.id))
        if is_liked:
            PostController.dislike_post(user_id, int(user_post.id))
            break


@router.get("/analytics")
@log_func_async
@make_response_async
async def get_analytics(start_at: str, end_at: str) -> list:
    start_at: datetime = datetime.strptime(start_at, "%Y-%m-%d")
    end_at: datetime = datetime.strptime(end_at, "%Y-%m-%d")
    posts_likes = []
    raw_posts_likes = PostController.get_posts_likes(start_at, end_at)
    for raw_post in raw_posts_likes:
        posts_likes.append({
            "count": raw_post.count,
            "created_at": raw_post.created_at
        })
    return posts_likes
