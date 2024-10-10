from fastapi import APIRouter, HTTPException, Body
from ...core.config import supabase

router = APIRouter()

@router.post("/login/")
async def login_user(email: str = Body(...), password: str = Body(...)):
    """
    Authenticate a user and return access and refresh tokens along with user details.

    Args:
        email (str): The email address of the user.
        password (str): The password of the user.

    Returns:
        dict: A dictionary containing the access token, refresh token, token type, expiration time, and user details.

    Raises:
        HTTPException: If authentication fails.
    """
    # Authenticate the user with Supabase
    response, error = await supabase.auth.sign_in(email=email, password=password)
    if error:
        raise HTTPException(status_code=400, detail=str(error.message))
    
    # Extract token details from the session
    session_info = response.get('session', {})
    access_token = session_info.get('access_token')
    refresh_token = session_info.get('refresh_token')
    token_type = session_info.get('token_type')  # Typically "bearer"
    expires_in = session_info.get('expires_in')
    
    # Include user details
    user_info = response.get('user', {})

    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": token_type,
        "expires_in": expires_in,
        "user": user_info
    }

