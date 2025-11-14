from fastapi.responses import JSONResponse
import uuid
from typing import Any

def _to_serializable(obj: Any):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, dict):
        return {k: _to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_serializable(v) for v in obj]
    return obj

def succes_response(http_status=200, message=None, data=None):
    return JSONResponse(status_code=http_status, content={
        "success": True,
        "message": f"{message}",
        "data": data
    })

def auth_response(http_status=200, message=None, user_id=None, token=None):
    return JSONResponse(status_code=http_status, content={
        "success": True,
        "message": f"{message}",
        "access_token": token,
        "user_id": str(user_id) if user_id is not None else None
    })


def error_response(http_status=400, message=None):
    return JSONResponse(status_code=http_status, content={
        "success": False,
        "message": f"{message}",
    })