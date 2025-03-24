from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Extended User model that inherits from Django's AbstractUser.
    Added a many-to-many relationship for followers.
    """
    followers = models.ManyToManyField(
        'self', 
        symmetrical=False,
        related_name='following',
        blank=True
    )


class Post(models.Model):
    """
    Post model to store user posts.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=280)  # Similar to Twitter/Threads character limit
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']  # Default to newest posts first
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}..."
    
    @property
    def like_count(self):
        return self.likes.count()


class Like(models.Model):
    """
    Like model to track post likes.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        # Ensure a user can only like a post once
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_like')
        ]
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"
    