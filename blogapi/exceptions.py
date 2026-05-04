from rest_framework.exceptions import APIException
from rest_framework import status


class CategoryNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Category not found"
    default_code = "CATEGORY_NOT_FOUND"


class BlogNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Blog not found"
    default_code = "BLOG_NOT_FOUND"