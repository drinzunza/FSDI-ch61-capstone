from django.urls import path
from .views import PostList, PostCreate, PostDetail, toggle_like
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path("create/", PostCreate.as_view(), name="post_create"),
    path("details/<int:pk>/", PostDetail.as_view(), name="post_details"),
    path("likes/toggle", toggle_like, name="like_post"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
