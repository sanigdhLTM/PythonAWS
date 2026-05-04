from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

class BaseModelViewSet(ModelViewSet):
    """
    Project-level Base ViewSet
    Centralizes success responses for ALL CRUD APIs
    """

    success_messages = {
        "list": "Records fetched successfully",
        "retrieve": "Record fetched successfully",
        "create": "Created successfully",
        "update": "Updated successfully",
        "partial_update": "Updated successfully",
        "destroy": "Deleted successfully",
    }

    def get_success_message(self):
        return self.success_messages.get(
            self.action, "Operation successful"
        )

    # ✅ LIST (GET all)
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "success": True,
                "message": self.get_success_message(),
                "data": response.data,
            },
            status=status.HTTP_200_OK,
        )

    # ✅ RETRIEVE (GET one)
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            {
                "success": True,
                "message": self.get_success_message(),
                "data": response.data,
            },
            status=status.HTTP_200_OK,
        )

    # ✅ CREATE (POST)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "success": True,
                "message": self.get_success_message(),
                "data": response.data,
            },
            status=status.HTTP_201_CREATED,
        )

    # ✅ UPDATE (PUT/PATCH)
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "success": True,
                "message": self.get_success_message(),
                "data": response.data,
            },
            status=response.status_code,
        )

    # ✅ DELETE
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {
                "success": True,
                "message": self.get_success_message(),
                "data": None,
            },
            status=status.HTTP_200_OK,
        )
