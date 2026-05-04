from django.db import models


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.TextField()
    is_deleted = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name


class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="blogs"
    )

    blog_title = models.CharField(max_length=500)
    blog_description = models.TextField(max_length=5000)
    publisher_name = models.CharField(max_length=255)
    views = models.IntegerField(default=0)

    is_deleted = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blog_title