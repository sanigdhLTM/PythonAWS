from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
import traceback



def custom_exception_handler(exc, context):
    
    print("🔥 EXCEPTION CAUGHT 🔥")
    print(traceback.format_exc())

    response = exception_handler(exc, context)

    # Unexpected server error
    if response is None:
        return Response(
            {
                "success": False,
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "Something went wrong",
                "data": None,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # ✅ HANDLE ALL VALIDATION ERRORS AT ONCE
    if isinstance(exc, ValidationError):
        errors = {}

        for field, messages in exc.detail.items():
            # messages can be list or string
            if isinstance(messages, list):
                errors[field] = messages[0]
            else:
                errors[field] = messages

        return Response(
            {
                "success": False,
                "error_code": "VALIDATION_ERROR",
                "message": "Validation failed",
                "data": errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Other API exceptions (404, permission, etc.)
    return Response(
        {
            "success": False,
            "error_code": getattr(exc, "default_code", "ERROR"),
            "message": str(exc.detail),
            "data": None,
        },
        status=response.status_code,
    )
