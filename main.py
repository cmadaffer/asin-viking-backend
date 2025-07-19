
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import httpx

app = FastAPI()

CLIENT_ID = "amzn1.application-oa2-client.f6542d3481a64723a227d8edd73e6199"
CLIENT_SECRET = "amzn1.oa2-cs.v1.bec64e9614743740db183d9f28c795aadefaced37efeadc403d4470c5c368a46"
REDIRECT_URI = "https://your-app.onrender.com/api/auth/callback"

AUTH_URL = (
    "https://sellercentral.amazon.com/apps/authorize/consent?"
    f"application_id={CLIENT_ID}&"
    f"state=asin_viking_state&"
    f"redirect_uri={REDIRECT_URI}&version=beta"
)

TOKEN_URL = "https://api.amazon.com/auth/o2/token"

@app.get("/login")
def login():
    return RedirectResponse(url=AUTH_URL)

@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("spapi_oauth_code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing spapi_oauth_code")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=data)

    if response.status_code != 200:
        return JSONResponse(content={"error": response.text}, status_code=response.status_code)

    token_data = response.json()
    return {
        "refresh_token": token_data.get("refresh_token"),
        "access_token": token_data.get("access_token")
    }
