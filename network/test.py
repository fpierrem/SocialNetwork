from models import User, Post, Comment, Like, Follow

test_post = Post.objects.get(id = 16)
comments = test_post.post_comments

print(comments)