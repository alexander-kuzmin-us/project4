from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import json

from .models import User, Post, Like


def index(request):
    """
    Display all posts with pagination
    """
    # Handle new post creation
    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get("content", "").strip()
        if content:
            Post.objects.create(user=request.user, content=content)
            return HttpResponseRedirect(reverse("index"))
    
    # Get all posts
    posts = Post.objects.all()
    
    # Add liked info for authenticated users
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    else:
        liked_posts = []
    
    # Paginate the posts - 10 per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts,
    })


@login_required
def following(request):
    """
    Display posts from users that the current user follows
    """
    # Get users that the current user follows
    following_users = request.user.following.all()
    
    # Get posts from those users
    posts = Post.objects.filter(user__in=following_users)
    
    # Add liked info for the user
    liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    
    # Paginate the posts - 10 per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts,
    })


def profile(request, username):
    """
    Display user profile and handle follow/unfollow
    """
    # Get the profile user
    profile_user = get_object_or_404(User, username=username)
    
    # Handle follow/unfollow
    if request.method == "POST" and request.user.is_authenticated:
        if request.POST.get("action") == "follow":
            profile_user.followers.add(request.user)
        elif request.POST.get("action") == "unfollow":
            profile_user.followers.remove(request.user)
        return HttpResponseRedirect(reverse("profile", args=[username]))
    
    # Check if current user follows this profile
    is_following = request.user.is_authenticated and profile_user.followers.filter(id=request.user.id).exists()
    
    # Get profile user's posts
    posts = Post.objects.filter(user=profile_user)
    
    # Add liked info for authenticated users
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    else:
        liked_posts = []
    
    # Paginate the posts - 10 per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj,
        "followers_count": profile_user.followers.count(),
        "following_count": profile_user.following.count(),
        "is_following": is_following,
        "liked_posts": liked_posts,
    })


@login_required
def edit_post(request, post_id):
    """
    API endpoint to edit a post
    """
    # Get the post
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the current user is the author
    if post.user != request.user:
        return JsonResponse({"error": "You cannot edit this post"}, status=403)
    
    # Process the edit
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            content = data.get("content", "").strip()
            
            if not content:
                return JsonResponse({"error": "Content cannot be empty"}, status=400)
            
            post.content = content
            post.save()
            return JsonResponse({"success": "Post updated", "content": post.content})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "PUT request required"}, status=400)


@login_required
def like_post(request, post_id):
    """
    API endpoint to like/unlike a post
    """
    # Get the post
    post = get_object_or_404(Post, id=post_id)
    
    # Process the like/unlike
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            action = data.get("action")
            
            if action == "like":
                # Add like if it doesn't exist
                Like.objects.get_or_create(user=request.user, post=post)
                return JsonResponse({"success": "Post liked", "likes": post.like_count})
            elif action == "unlike":
                # Remove like if it exists
                Like.objects.filter(user=request.user, post=post).delete()
                return JsonResponse({"success": "Post unliked", "likes": post.like_count})
            else:
                return JsonResponse({"error": "Invalid action"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "PUT request required"}, status=400)


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
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    