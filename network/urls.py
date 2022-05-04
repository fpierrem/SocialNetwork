from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("profile/<str:user_name>", views.profile, name="profile"),
    path("posts",views.posts, name="posts"),
    path("post/<int:post_id>", views.post, name="post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("my_profile", views.my_profile, name="my_profile"),
    path("write_post", views.write_post, name="write_post"),
    path("write_comment", views.write_comment, name="write_comment"),
    path("count_followers/<str:user_name>", views.count_followers, name="count_followers"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("edit", views.edit, name="edit"),
    path("delete", views.delete, name="delete"),
    path("check_like_status", views.check_like_status, name="check_like_status"),
    path("count_likes", views.count_likes, name="count_likes"),
    path("like", views.like, name="like"),
    path("unlike", views.unlike, name="unlike"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)