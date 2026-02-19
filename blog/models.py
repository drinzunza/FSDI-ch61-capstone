from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2) # REMOVE default
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=2) # REMOVE default
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="posts/")
    created_on = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.user}"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"by: {self.author} on: {self.post.title}"
