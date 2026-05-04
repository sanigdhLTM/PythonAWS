from rest_framework import serializers
from .models import Blog, Category


class CategorySerializer(serializers.ModelSerializer):
    
    category_name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "category_name is required",
            "blank": "category_name cannot be empty",
        }
    )

    class Meta:
        model = Category
        fields = ["category_id", "category_name"]
        read_only_fields = ("category_id", "created_on", "modified_on")

    
    def validate_category_name(self, value):
        """
        Prevent duplicate category names (case-insensitive),
        ignoring soft-deleted records.
        """
        qs = Category.objects.filter(
            category_name__iexact=value,
            is_deleted=False
        )

        # Exclude self during update
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "Category with this name already exists"
            )

        return value



class BlogSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.category_name")

    
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",   # ✅ THIS LINE IS CRITICAL
        queryset=Category.objects.filter(is_deleted=False),
        required=True,
        error_messages={
            "required": "category_id is required",
            "does_not_exist": "Invalid category_id",
            "incorrect_type": "Invalid category_id",
        }
    )

    
    blog_title = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=500,
        error_messages={
            "required": "blog_title is required",
            "blank": "blog_title cannot be empty",
        }
    )

    blog_description = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=5000,
        error_messages={
            "required": "blog_description is required",
            "blank": "blog_description cannot be empty",
        }
    )
    
    publisher_name = serializers.CharField(
        required=False,
        allow_blank=False,
        default="Sanigdh"
    )



    class Meta:
        model = Blog
        fields = [
            "blog_id",
            "category_id",
            "category_name",
            "blog_title",
            "blog_description",
            "publisher_name",
            "views",
        ]

        read_only_fields = (
            "blog_id",
            "views",
            "created_on",
            "modified_on",
        )