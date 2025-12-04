from fastapi import Request, HTTPException

ADMIN_KEY = "mysecret"  # replace or load from env

def validate_admin_key(request: Request):
    key = request.headers.get("x-admin-key")
    if key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin key")
