import jwt
import os
from dotenv import load_dotenv
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

# 1. Load the key and fix the line breaks so the cryptography library can read it
CLERK_PUBLIC_KEY = os.getenv("CLERK_PUBLIC_KEY", "").replace("\\n", "\n")

security = HTTPBearer()


def get_user_id_from_request(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Takes the token from the Next.js request and verifies it using the static Public Key.
    """
    token = credentials.credentials

    if not CLERK_PUBLIC_KEY:
        raise HTTPException(status_code=500, detail="Server configuration error: Missing Public Key")

    try:    
        # 2. Decode the token using your static key directly
        payload = jwt.decode(
            token,
            CLERK_PUBLIC_KEY,
            algorithms=["RS256"]
        )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID missing from token")

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")