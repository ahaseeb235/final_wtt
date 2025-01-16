''' models.py for noticeboard app '''

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    """
    Model representing a post in the noticeboard (like a blog post).
    """
    title = models.CharField(max_length=200, help_text="Enter the title of the post.")
    content = models.TextField(max_length=1000, help_text="Write the content of the post here. max 1000 characters.")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noticeboard_posts')
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the Post model."""
        return self.title

    class Meta:
        ordering = ['-date_posted']  # Orders posts by most recent first