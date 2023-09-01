from django.urls import path
from .views import (
    PostList,
    PostDetail,
    PostCreate,
    PostUpdate,
    PostDelete,
    PostCategoryList,
    PostCategoryDetails,
    UserDetail,
    CommentList,
    CommentStatus,
    CommentDelete,
)


urlpatterns = [
    path("", PostList.as_view(), name="posts"),
    path("post/<slug:slug>/", PostDetail.as_view(), name="post"),
    path("add/", PostCreate.as_view(), name="post_create"),
    path("post/<slug:slug>/edit/", PostUpdate.as_view(), name="post_update"),
    path("post/<slug:slug>/delete/", PostDelete.as_view(), name="post_delete"),
    path("categories/", PostCategoryList.as_view(), name="categories"),
    path(
        "category/<slug:slug>/", PostCategoryDetails.as_view(), name="posts_in_category"
    ),
    path("user/<int:pk>", UserDetail.as_view(), name="user_posts"),
    path(
        "comments/",
        CommentList.as_view(template_name="board/com_new.html"),
        name="comments_new",
    ),
    path(
        "comments/accepted/",
        CommentList.as_view(template_name="board/com_accepted.html"),
        name="comments_accepted",
    ),
    path(
        "comments/rejected/",
        CommentList.as_view(template_name="board/com_rejected.html"),
        name="comments_rejected",
    ),
    path(
        "comments/<int:pk>/accept",
        CommentStatus.as_view(choice="accept"),
        name="comment_accept",
    ),
    path(
        "comments/<int:pk>/reject",
        CommentStatus.as_view(choice="reject"),
        name="comment_reject",
    ),
    path("comments/<int:pk>/delete/", CommentDelete.as_view(), name="comment_delete"),
]
