from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Blog, Category
from .serializers import BlogSerializer, CategorySerializer
from blogapi.exceptions import BlogNotFound, CategoryNotFound
from configurations.base_viewset import BaseModelViewSet




class CategoryViewSet(BaseModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        qs = Category.objects.filter(is_deleted=False)
        if not qs.exists():
            raise CategoryNotFound("No categories available")
        return qs

    def get_object(self):
        try:
            return Category.objects.get(
                pk=self.kwargs["pk"],
                is_deleted=False
            )
        except Category.DoesNotExist:
            raise CategoryNotFound("Category with given id does not exist")

    def perform_destroy(self, instance):
        # soft delete
        instance.is_deleted = True
        instance.save()


        



class BlogViewSet(BaseModelViewSet):
    serializer_class = BlogSerializer

    def get_queryset(self):
        qs = Blog.objects.filter(is_deleted=False)
        if not qs.exists():
            raise BlogNotFound("No blogs available")
        return qs.select_related("category")
    
    
    def get_object(self):
        try:
            return Blog.objects.get(
                pk=self.kwargs["pk"],
                is_deleted=False
            )
        except Blog.DoesNotExist:
            raise BlogNotFound("Blog with given id does not exist")


    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


