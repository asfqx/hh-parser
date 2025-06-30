from app.services.get_tokens import tokens
import httpx


async def get_access_token_from_refresh_token():
    url = "https://hh.ru/oauth/token"

    headers = {
        "User-Agent": "api-test-agent",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": tokens.refresh_token,
    }

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(url, data=data, headers=headers)
        access_token = response.json()["access_token"]
        refresh_token = response.json()["refresh_token"]
    tokens.save_tokens(access_token, refresh_token)
