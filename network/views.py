from cProfile import Profile
import json, time
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Exists, Count
from django.forms import model_to_dict
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *

def index(request):
    return render(request, "network/index.html")

def posts(request):
    context = request.GET.get("context")
    if context == "all_users":
        all_posts = Post.objects.all()
    elif context == "followed_users":
        user = request.user
        followed_users = [follow.followed for follow in Follow.objects.filter(follower = user)]
        all_posts = Post.objects.filter(user__in=followed_users)
    else:        
        profile_user = User.objects.get(username=context)
        all_posts = Post.objects.filter(user=profile_user)
    paginator = Paginator(all_posts,per_page=10)
    page_num = int(request.GET.get("page",1))
    if page_num > paginator.num_pages:
        raise Http404
    if page_num > 1:
        time.sleep(1)    
    posts = paginator.page(page_num)
    return render(request,"network/post_list.html", {
        "posts": posts
    })

def post(request, post_id):
    return render(request, "network/post_detailed_view.html",{
        "post" : Post.objects.get(id = int(post_id))
    })

def profile(request, user_name):
    profile_user = User.objects.get(username=user_name)

    return render(request, "network/profile.html",{
        "profile_user" : profile_user,
        "follower_count" : profile_user.followers.count(),
        "following" : request.user.is_authenticated and Follow.objects.filter(follower = request.user, followed = profile_user).exists(),
    })

def count_followers(request, user_name):
    time.sleep(0.1)
    c = User.objects.get(username = user_name).followers.count()
    return JsonResponse(c, safe=False)

@login_required
def following(request):
    return render(request, "network/index.html")

@login_required
def write_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    post = Post(
        user=request.user,
        text=json.loads(request.body).get('text'),
        timestamp = datetime.now(),
    )
    post.save()    
    return JsonResponse({"message": "Post received successfully."}, status=201)

@login_required
def write_comment(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    comment = Comment(
        user=request.user,
        post=Post.objects.get(id = int(json.loads(request.body).get('post_id'))),
        text=json.loads(request.body).get('text'),
        timestamp = datetime.now(),
    )
    comment.save()
    return JsonResponse({"message": "Comment received successfully."}, status=201)

@login_required
def follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    user = request.user
    target = User.objects.get(username=data['target'])
    follow = Follow(follower = user, followed = target)
    follow.save()
    return JsonResponse({"message":"followed."},status=201)

@login_required
def unfollow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    user = request.user
    target = User.objects.get(username=data['target'])
    follow = Follow.objects.get(follower = user, followed = target)
    follow.delete()
    return JsonResponse({"message":"unfollowed."},status=201)

@login_required
def check_like_status(request):
    user = request.user
    target_type = request.GET.get('target_type')
    target_id = request.GET.get('target_id')
    if target_type == 'post':
        like_status = Like.objects.filter(user = user, post = Post.objects.get(id=target_id)).exists()
    elif target_type == 'comment':
        like_status = Like.objects.filter(user = user, comment = Comment.objects.get(id=target_id)).exists()

    return JsonResponse(like_status, safe=False)

@csrf_exempt
def count_likes(request):
    time.sleep(0.1)
    target_type = request.GET.get('target_type')
    target_id = request.GET.get('target_id')
    if target_type == 'post':
        c = Post.objects.get(id = target_id).post_likes.count()
    elif target_type == 'comment':
        c = Comment.objects.get(id = target_id).comment_likes.count()

    return JsonResponse(c, safe=False)

@login_required
def like(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    user = request.user
    data = json.loads(request.body)

    if data['target_type'] == 'post':
        like = Like(user = user, post = Post.objects.get(id=data['target_id']))

    elif data['target_type'] == 'comment':
        like = Like(user = user, comment = Comment.objects.get(id=data['target_id']))

    like.save()
    return JsonResponse({"message":"liked."},status=201)

@login_required
def unlike(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    user = request.user
    data = json.loads(request.body)

    if data['target_type'] == 'post':
        like = Like.objects.get(user = user, post = Post.objects.get(id=data['target_id']))

    elif data['target_type'] == 'comment':
        like = Like.objects.get(user = user, comment = Comment.objects.get(id=data['target_id']))

    like.delete()
    return JsonResponse({"message":"unliked."},status=201)

@login_required
def edit(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    target_id = data["target_id"]
    edited_text = data["edited_text"]
    
    if data['target_type'] == 'post':
        target = Post.objects.get(id = target_id)
    elif data['target_type'] == 'comment':
        target = Comment.objects.get(id = target_id)

    if request.user != target.user:
        return JsonResponse({"error": "You do not have permission to edit this."}, status=400)

    target.text = edited_text
    target.edited = True
    target.save()
    return JsonResponse({"message": "Successfully edited."}, status=201)

@login_required
def delete(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    target_id = data["target_id"]
    
    if data['target_type'] == 'post':
        target = Post.objects.get(id = target_id)
    elif data['target_type'] == 'comment':
        target = Comment.objects.get(id = target_id)

    if request.user != target.user:
        return JsonResponse({"error": "You do not have permission to delete this."}, status=400)

    target.delete()
    return JsonResponse({"message": "Successfully deleted."}, status=201)
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords don't match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user_profile = UserProfile(user = user)
            user_profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return render(request, "network/create_profile.html")

    else:
        return render(request, "network/register.html")

@login_required
def my_profile(request):
    if request.method == 'GET':
        return render(request, "network/update_profile.html")
    if request.method == 'POST':
        user_profile = request.user.user_profile
        if request.FILES:
            user_profile.avatar = request.FILES['user-photo']
        user_profile.bio = request.POST['bio']
        user_profile.save()
        return HttpResponseRedirect(reverse("index"))